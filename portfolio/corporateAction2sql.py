#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import argparse
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP

# 你的Excel列名（按截图）
COLS = [
    "registration_date",
    "ex_dividend_date",
    "bonus_shares_issued",
    "shares_per_unit",
    "ex_rights_per_share",
    "payment_date",
    "symbol",
    "registered_quantity",
    "dividend",
    "fee",
]

DATE_COLS = {"registration_date", "ex_dividend_date", "payment_date"}
DEC_COLS = {
    "bonus_shares_issued",
    "shares_per_unit",
    "ex_rights_per_share",
    "registered_quantity",
    "dividend",
    "fee",
}

def is_na(x) -> bool:
    try:
        return pd.isna(x)
    except Exception:
        return x is None

def esc_sql(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "''")

def to_date_sql(x):
    """Return 'YYYY-MM-DD' or NULL."""
    if is_na(x):
        return None
    # pandas读出来可能是 Timestamp / datetime / str
    try:
        dt = pd.to_datetime(x, errors="coerce")
        if pd.isna(dt):
            return None
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return None

def to_decimal_sql(x, scale=6):
    """Return Decimal or None."""
    if is_na(x):
        return None
    # 有些单元格可能是 '8,757.11'
    s = str(x).strip()
    if not s:
        return None
    s = s.replace(",", "")
    try:
        d = Decimal(s)
    except Exception:
        return None
    q = Decimal("1." + "0"*scale)
    return d.quantize(q, rounding=ROUND_HALF_UP)

def normalize_symbol(x):
    """Keep leading zeros like 00700. Return None if empty."""
    if is_na(x):
        return None
    s = str(x).strip()
    if not s:
        return None
    # 避免 700.0 这类
    if s.endswith(".0"):
        s = s[:-2]
    return s

def sheet_to_rows(df: pd.DataFrame, sheet_name: str):
    # 统一列名：去空格/小写
    rename_map = {c: str(c).strip() for c in df.columns}
    df = df.rename(columns=rename_map)

    # 保留我们关心的列（缺列就补空列）
    for c in COLS:
        if c not in df.columns:
            df[c] = None
    df = df[COLS]

    rows = []
    for idx0, row in df.iterrows():
        raw_row_no = int(idx0) + 2  # 假设第1行为表头；数据从第2行开始

        sym = normalize_symbol(row["symbol"])
        # symbol 为空的行直接跳过
        if not sym:
            continue

        out = {
            "source_sheet": sheet_name,
            "raw_row_no": raw_row_no,
            "registration_date": to_date_sql(row["registration_date"]),
            "ex_dividend_date": to_date_sql(row["ex_dividend_date"]),
            "payment_date": to_date_sql(row["payment_date"]),
            "symbol": sym,
        }

        for c in DEC_COLS:
            out[c] = to_decimal_sql(row[c], scale=6)

        rows.append(out)

    return rows

def infer_period_from_sheet(sheet_name: str):
    """sheet名通常是 2022/2023/...，取其中4位数字作为period_yyyy."""
    s = str(sheet_name).strip()
    digits = "".join(ch for ch in s if ch.isdigit())
    if len(digits) >= 4:
        return int(digits[:4])
    # 兜底：未知则用0
    return 0

def write_insert_sql(rows, out_sql_path: str, table="corporate_action"):
    with open(out_sql_path, "w", encoding="utf-8") as f:
        f.write("START TRANSACTION;\n\n")
        for r in rows:
            period_yyyy = infer_period_from_sheet(r["source_sheet"])

            def v_date(key):
                return "NULL" if r[key] is None else f"'{r[key]}'"

            def v_dec(key):
                return "NULL" if r[key] is None else str(r[key])

            stmt = (
                f"INSERT INTO {table} ("
                f"period_yyyy, "    # source_sheet, raw_row_no, "
                f"registration_date, ex_dividend_date, bonus_shares_issued, shares_per_unit, ex_rights_per_share, payment_date, "
                f"symbol, registered_quantity, dividend, fee"
                f") VALUES ("
                f"{period_yyyy}, "
                # f"'{esc_sql(r['source_sheet'])}', "
                # f"{r['raw_row_no']}, "
                f"{v_date('registration_date')}, "
                f"{v_date('ex_dividend_date')}, "
                f"{v_dec('bonus_shares_issued')}, "
                f"{v_dec('shares_per_unit')}, "
                f"{v_dec('ex_rights_per_share')}, "
                f"{v_date('payment_date')}, "
                f"'{esc_sql(r['symbol'])}', "
                f"{v_dec('registered_quantity')}, "
                f"{v_dec('dividend')}, "
                f"{v_dec('fee')}"
                f");\n"
            )
            f.write(stmt)

        f.write("\nCOMMIT;\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="corporate action excel file path")
    ap.add_argument("-o", "--out", default="corporate_action_insert.sql", help="output sql file")
    ap.add_argument("--table", default="corporate_action", help="target table name")
    args = ap.parse_args()

    xl = pd.ExcelFile(args.input)

    all_rows = []
    for sheet in xl.sheet_names:
        df = xl.parse(sheet_name=sheet, dtype={"symbol": str})  # 关键：保留前导0
        rows = sheet_to_rows(df, sheet)
        all_rows.extend(rows)

    write_insert_sql(all_rows, args.out, table=args.table)
    print(f"Generated {len(all_rows)} INSERT statements into: {args.out}")

if __name__ == "__main__":
    main()
