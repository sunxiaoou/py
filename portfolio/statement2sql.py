#! /usr/local/bin/python3

import re
import calendar
from datetime import date
import pandas as pd

EXCEL_PATH = "valCapStatement.xlsx"
BROKER_NAME = "ValuableCapital"   # 未来可换成 IBKR / FUTU / etc


def parse_period(sheet_name: str) -> int:
    m = re.search(r"(\d{4})\D?(\d{2})", sheet_name)
    if not m:
        raise ValueError(f"无法从 sheet 名解析年月: {sheet_name}")
    return int(m.group(1)) * 100 + int(m.group(2))


def month_end(period_yyyymm: int) -> str:
    y = period_yyyymm // 100
    m = period_yyyymm % 100
    last_day = calendar.monthrange(y, m)[1]
    return date(y, m, last_day).isoformat()


def sql_value(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "NULL"
    if isinstance(v, str):
        return "'" + v.replace("'", "''") + "'"
    return str(v)


def main():
    xls = pd.ExcelFile(EXCEL_PATH, engine="openpyxl")

    for sheet in xls.sheet_names:
        period = parse_period(sheet)
        # stmt_date = month_end(period)

        df = pd.read_excel(xls, sheet_name=sheet)
        df.columns = [c.strip() for c in df.columns]

        # 清洗
        df = df[df["symbol"].notna()]
        df["symbol"] = df["symbol"].astype(str).str.strip()

        # 数值列
        for c in ["volume", "closing_price", "market_value", "exchange_rate", "HKD_equivalent"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")

        # 类型
        df["item_type"] = df["symbol"].apply(
            lambda s: "CASH" if s.upper().startswith("CASH_") else "POSITION"
        )

        total_hkd = df["HKD_equivalent"].fillna(0).sum()

        # ===== 头表 SQL =====
        print(f"\n-- ===== {sheet} / {BROKER_NAME} =====")
        print(
            f"""INSERT INTO broker_statement_monthly
(broker_name, period_yyyymm, base_ccy, exchange_rate, total_hkd_equiv)
VALUES
({sql_value(BROKER_NAME)}, {period}, 'HKD', {df['exchange_rate'][1]}, {total_hkd})
ON DUPLICATE KEY UPDATE
  total_hkd_equiv = VALUES(total_hkd_equiv);
"""
        )
# (broker_name, period_yyyymm, statement_date, base_ccy, total_hkd_equiv)
# ({sql_value(BROKER_NAME)}, {period}, {sql_value(stmt_date)}, 'HKD', {total_hkd})
#   statement_date = VALUES(statement_date);

        # ===== 明细表 SQL =====
        for idx, r in df.iterrows():
            print(
                f"""INSERT INTO broker_statement_monthly_item
(broker_name, period_yyyymm, item_type, symbol, volume, currency,
 closing_price, market_value, exchange_rate, hkd_equivalent, raw_row_no)
VALUES
({sql_value(BROKER_NAME)}, {period}, {sql_value(r.item_type)}, {sql_value(r.symbol)},
 {sql_value(r.get("volume"))}, {sql_value(r.get("currency"))},
 {sql_value(r.get("closing_price"))}, {sql_value(r.get("market_value"))},
 {sql_value(r.get("exchange_rate"))}, {sql_value(r.get("HKD_equivalent"))},
 {idx + 2})
ON DUPLICATE KEY UPDATE
  volume = VALUES(volume),
  closing_price = VALUES(closing_price),
  market_value = VALUES(market_value),
  exchange_rate = VALUES(exchange_rate),
  hkd_equivalent = VALUES(hkd_equivalent);
"""
            )


if __name__ == "__main__":
    main()