#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import argparse
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import pandas as pd


def is_na(x) -> bool:
    try:
        return pd.isna(x)
    except Exception:
        return x is None


def esc_sql(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "''")


def to_datetime_str(x) -> str:
    """Return 'YYYY-MM-DD HH:MM:SS' or None."""
    if is_na(x):
        return None
    dt = pd.to_datetime(x, errors="coerce")
    if pd.isna(dt):
        return None
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def to_decimal_str(x, scale=2) -> str:
    """Return decimal string with given scale or None."""
    if is_na(x):
        return None
    s = str(x).strip().replace(",", "")
    if not s:
        return None
    try:
        d = Decimal(s)
    except (InvalidOperation, ValueError):
        return None
    q = Decimal("1." + "0" * scale)
    d = d.quantize(q, rounding=ROUND_HALF_UP)
    # 输出为普通数字字符串
    return format(d, "f")


def to_int_volume(x):
    """Convert excel volume cell to int; return None if empty/invalid."""
    if is_na(x):
        return None
    # 有些Excel会把数字读成 float/Decimal/str
    if isinstance(x, (int,)):
        return x
    if isinstance(x, float):
        if x != x:  # NaN
            return None
        return int(x)
    if isinstance(x, Decimal):
        return int(x)
    s = str(x).strip()
    if not s:
        return None
    # 去掉可能的逗号千分位
    s = s.replace(",", "")
    # 防止 "4000.0"
    if "." in s:
        try:
            return int(float(s))
        except Exception:
            return None
    if s.isdigit() or (s.startswith("-") and s[1:].isdigit()):
        return int(s)
    return None

def normalize_symbol(x) -> str:
    """Keep leading zeros; strip trailing .0."""
    if is_na(x):
        return None
    s = str(x).strip()
    if not s:
        return None
    if s.endswith(".0"):
        s = s[:-2]
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="Excel path")
    ap.add_argument("-o", "--out", default="trade_ledger_insert.sql", help="Output SQL file")
    ap.add_argument("--sheet", default=None, help="Sheet name (default: first sheet)")
    ap.add_argument("--table", default="trade_ledger", help="Target table name")
    ap.add_argument("--no-fee", action="store_true", help="Ignore tax_and_fee even if present")
    args = ap.parse_args()

    xl = pd.ExcelFile(args.input)
    sheet = args.sheet or xl.sheet_names[0]
    df = xl.parse(sheet_name=sheet, dtype={"symbol": str})

    # 统一列名：去空格、转小写
    df.columns = [str(c).strip().lower() for c in df.columns]

    required = ["occurred_at", "biz_type_code", "amount", "volume", "symbol"]
    for c in required:
        if c not in df.columns:
            raise SystemExit(f"Missing required column: {c}")

    has_tax_fee = (not args.no_fee) and ("tax_and_fee" in df.columns)

    out_lines = []
    out_lines.append("START TRANSACTION;")

    for idx, row in df.iterrows():
        occurred_at = to_datetime_str(row["occurred_at"])
        biz = ("" if is_na(row["biz_type_code"]) else str(row["biz_type_code"]).strip())
        amount = to_decimal_str(row["amount"], scale=2)
        volume = "NULL" if is_na(row["volume"]) else to_int_volume(row["volume"])
        symbol = normalize_symbol(row["symbol"])

        # 跳过明显空行
        if not occurred_at or not biz or amount is None or not symbol:
            continue

        if has_tax_fee:
            fee_raw = to_decimal_str(row["tax_and_fee"], scale=2)
            fee_sql = "NULL"
            if fee_raw is not None:
                # fee 存正值：abs
                fee_sql = str(abs(Decimal(fee_raw))).rstrip("0").rstrip(".") if "." in fee_raw else str(abs(Decimal(fee_raw)))
                # 再标准化为两位
                fee_sql = format(abs(Decimal(fee_raw)).quantize(Decimal("1.00")), "f")

            out_lines.append(
                f"INSERT INTO {args.table} (occurred_at, biz_type_code, amount, tax_and_fee, volume, symbol) VALUES ("
                f"'{esc_sql(occurred_at)}', '{esc_sql(biz)}', {amount}, {fee_sql}, {volume}, '{esc_sql(symbol)}');"
            )
        else:
            out_lines.append(
                f"INSERT INTO {args.table} (occurred_at, biz_type_code, amount, symbol) VALUES ("
                f"'{esc_sql(occurred_at)}', '{esc_sql(biz)}', {amount}, '{esc_sql(symbol)}');"
            )

    out_lines.append("COMMIT;")

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines) + "\n")

    print(f"OK: wrote {len(out_lines)-2} INSERT statements to {args.out} (sheet={sheet})")


if __name__ == "__main__":
    main()
