#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import csv
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


TABLE = "broker_statement_monthly"


DEC_COLS = {
    "volume",
    "closing_price",
    "market_value",
    "usd_hkd_rate",
    "cny_rate",
}

STR_COLS = {
    "broker_name",
    "period_yyyymm",
    "symbol",
    "currency",
}


def esc_sql(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "''")


def to_decimal_or_none(s: str, scale=6):
    if s is None:
        return None
    s = s.strip()
    if s == "":
        return None
    s = s.replace(",", "")
    try:
        d = Decimal(s)
    except (InvalidOperation, ValueError):
        return None
    q = Decimal("1." + "0" * scale)
    return d.quantize(q, rounding=ROUND_HALF_UP)


def sql_val(v):
    """Render python value to SQL literal."""
    if v is None:
        return "NULL"
    if isinstance(v, Decimal):
        return format(v, "f")
    if isinstance(v, int):
        return str(v)
    # string
    return f"'{esc_sql(str(v))}'"


def main():
    if len(sys.argv) < 3:
        print('Usage: {} "csv_name" "sql_name"'.format(sys.argv[0]))
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames
        if not cols:
            raise SystemExit("CSV has no header")

        # 简单校验（可按需删）
        missing = [c for c in STR_COLS.union(DEC_COLS) if c not in cols]
        if missing:
            raise SystemExit(f"CSV missing columns: {missing}")

        rows = list(reader)

    with open(sys.argv[2], "w", encoding="utf-8") as out:
        out.write("START TRANSACTION;\n\n")

        for r in rows:
            # 字符列
            broker_name = (r.get("broker_name") or "").strip() or None
            period_yyyymm = (r.get("period_yyyymm") or "").strip() or None
            symbol = (r.get("symbol") or "").strip() or None
            currency = (r.get("currency") or "").strip() or None

            # period_yyyymm 转 int（若你表里是 INT）
            period_int = None
            if period_yyyymm and period_yyyymm.isdigit():
                period_int = int(period_yyyymm)

            # 数字列（空->NULL）
            volume = to_decimal_or_none(r.get("volume"))
            closing_price = to_decimal_or_none(r.get("closing_price"))
            market_value = to_decimal_or_none(r.get("market_value"))
            usd_hkd_rate = to_decimal_or_none(r.get("usd_hkd_rate"))
            cny_rate = to_decimal_or_none(r.get("cny_rate"))

            # 跳过明显空行
            if not broker_name or period_int is None or not symbol:
                continue

            # 生成 INSERT（字段名按 CSV）
            out.write(
                f"INSERT INTO {TABLE} "
                f"(broker_name, period_yyyymm, symbol, currency, volume, closing_price, market_value, usd_hkd_rate, cny_rate) "
                f"VALUES ("
                f"{sql_val(broker_name)}, "
                f"{sql_val(period_int)}, "
                f"{sql_val(symbol)}, "
                f"{sql_val(currency)}, "
                f"{sql_val(volume)}, "
                f"{sql_val(closing_price)}, "
                f"{sql_val(market_value)}, "
                f"{sql_val(usd_hkd_rate)}, "
                f"{sql_val(cny_rate)}"
                f");\n"
            )

        out.write("\nCOMMIT;\n")

    print(f"OK: wrote {len(rows)} rows to {sys.argv[2]}")


if __name__ == "__main__":
    main()