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

def sql_value(v) -> str:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "NULL"
    if isinstance(v, str):
        return "'" + v.replace("'", "''") + "'"
    return str(v)

def to_datetime_str(x) -> str:
    """Return 'YYYY-MM-DD HH:MM:SS' or None."""
    if is_na(x):
        return None
    dt = pd.to_datetime(x, errors="coerce")
    if pd.isna(dt):
        return None
    return dt.strftime("%Y-%m-%d %H:%M:%S")


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
    ap.add_argument("-o", "--out", default="stmtInsert.sql", help="Output SQL file")
    ap.add_argument("--sheet", default=None, help="Sheet name (default: first sheet)")
    ap.add_argument("--table", default="broker_statement_monthly_item", help="Target table name")
    ap.add_argument("--scale", type=int, default=6, help="Decimal scale for rates (default 6)")
    args = ap.parse_args()

    xl = pd.ExcelFile(args.input)
    sheet = args.sheet or xl.sheet_names[0]
    df = xl.parse(sheet_name=sheet)

    # 统一列名
    df.columns = [str(c).strip().lower() for c in df.columns]
    required = ["broker_name", "period_yyyymm", "symbol", "currency", "market_value", "volume", 'closing_price']
    for c in required:
        if c not in df.columns:
            raise SystemExit(f"Missing required column: {c}")

    lines = ["START TRANSACTION;"]
    inserted = 0
    for idx, row in df.iterrows():
        broker_name = None if is_na(row.get("broker_name")) else str(row.get("broker_name")).strip()
        period = None if is_na(row.get("period_yyyymm")) else int(row.get("period_yyyymm"))
        symbol = None if is_na(row.get("symbol")) else str(row.get("symbol")).strip()
        if broker_name is None or period is None or symbol is None:
            continue
        currency = row["currency"]
        if currency not in ("HKD", "USD"):
            raise SystemExit(f"[解析失败] currency : {currency} (idx={idx} + 2)")

        item_type = "CASH" if symbol.upper().startswith("CASH_") else "POSITION"
        market_value = to_dec_str(row.get("market_value"))
        volume = to_dec_str(row.get("volume"))
        closing_price = to_dec_str(row.get("closing_price"))

        lines.append(
            f"INSERT INTO {args.table} "
            f"(broker_name, period_yyyymm, item_type, symbol, currency, market_value, volume, closing_price, raw_row_no) "
            f"VALUES ({sql_value(broker_name)}, {period}, {sql_value(item_type)}, {sql_value(symbol)}, "
            f"{sql_value(currency)}, {market_value}, {sql_value(volume)}, {sql_value(closing_price)}, {idx + 2});"
        )
        inserted += 1

    lines.append("COMMIT;")

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"OK: wrote {inserted} INSERT statements to {args.out} (sheet={sheet})")


if __name__ == "__main__":
    main()
