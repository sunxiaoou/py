#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import argparse
import pandas as pd
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


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

def to_int(x):
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

def to_dec_str(x, scale=6) -> str:
    """Return decimal string with fixed scale or None."""
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
    return format(d, "f")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="Excel file path")
    ap.add_argument("-o", "--out", default="fxRateInsert.sql", help="Output SQL file")
    ap.add_argument("--sheet", default=None, help="Sheet name (default: first sheet)")
    ap.add_argument("--table", default="fx_rate_snapshot", help="Target table name")
    ap.add_argument("--scale", type=int, default=6, help="Decimal scale for rates (default 6)")
    args = ap.parse_args()

    xl = pd.ExcelFile(args.input)
    sheet = args.sheet or xl.sheet_names[0]
    df = xl.parse(sheet_name=sheet)

    # 统一列名
    df.columns = [str(c).strip().lower() for c in df.columns]

    required = ["occurred_at", "currency", "spot_buying", "spot_selling", "average"]
    for c in required:
        if c not in df.columns:
            raise SystemExit(f"Missing required column: {c}")

    lines = ["START TRANSACTION;"]

    inserted = 0
    for _, row in df.iterrows():
        occurred_at = to_datetime_str(row["occurred_at"])
        period_yyyymm = to_int(row["period_yyyymm"])
        currency = None if is_na(row["currency"]) else str(row["currency"]).strip().upper()

        spot_buying = to_dec_str(row["spot_buying"], scale=args.scale)
        spot_selling = to_dec_str(row["spot_selling"], scale=args.scale)
        average = to_dec_str(row["average"], scale=args.scale)

        # 跳过空行/异常行
        if not occurred_at or not currency or spot_buying is None or spot_selling is None or average is None:
            continue

        # 简单币种校验（可选）
        if len(currency) != 3:
            raise SystemExit(f"[解析失败] currency 非3位: {currency} (occurred_at={occurred_at})")

        lines.append(
            f"INSERT INTO {args.table} (occurred_at, period_yyyymm, currency, spot_buying, spot_selling, average) VALUES ("
            f"'{esc_sql(occurred_at)}', {period_yyyymm}, '{esc_sql(currency)}', {spot_buying}, {spot_selling}, {average}"
            f");"
        )
        inserted += 1

    lines.append("COMMIT;")

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"OK: wrote {inserted} INSERT statements to {args.out} (sheet={sheet})")


if __name__ == "__main__":
    main()
