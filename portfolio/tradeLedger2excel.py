#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import pandas as pd
from sqlalchemy import create_engine, text
from openpyxl.utils import get_column_letter


def autosize_and_freeze(writer, sheet_name: str, df: pd.DataFrame):
    """Auto column width + freeze header row."""
    ws = writer.sheets[sheet_name]
    ws.freeze_panes = "A2"

    # Auto width (simple heuristic)
    for i, col in enumerate(df.columns, start=1):
        series = df[col].astype(str)
        max_len = max([len(col)] + series.map(len).tolist()) if len(series) else len(col)
        max_len = min(max_len + 2, 60)  # cap
        ws.column_dimensions[get_column_letter(i)].width = max_len


def export_year_to_excel(
    mysql_url: str,
    year: int,
    out_xlsx: str,
    sheet_name: str = None,
    timezone: str = None,
):
    """
    Export trade_ledger records of a given year into one Excel sheet.
    - mysql_url example: mysql+pymysql://user:pass@host:3306/db?charset=utf8mb4
    """
    engine = create_engine(mysql_url, pool_pre_ping=True)

    # 用 [year-01-01, year+1-01-01) 做范围过滤，走 occurred_at 索引更友好
    start = f"{year}-01-01 00:00:00"
    end = f"{year+1}-01-01 00:00:00"

    sql = text("""
        SELECT
            id,
            occurred_at,
            biz_type_code,
            amount,
            symbol,
            direction,
            account_id,
            broker_txn_id,
            note,
            raw_text
        FROM trade_ledger
        WHERE occurred_at >= :start AND occurred_at < :end
        ORDER BY occurred_at, id
    """)

    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params={"start": start, "end": end})

    # 可选：如果你希望把 occurred_at 视为某个时区（通常 MySQL DATETIME 是“无时区”的）
    # 这里默认不做转换，只原样导出。
    # 如果你想转换，可再告诉我你库里存的是哪个时区、想导出哪个时区。

    if sheet_name is None:
        sheet_name = f"trade_ledger_{year}"

    # 写 Excel
    with pd.ExcelWriter(out_xlsx, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        autosize_and_freeze(writer, sheet_name, df)

    return len(df)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, required=True, help="year to export, e.g. 2022")
    ap.add_argument("--out", required=True, help="output xlsx path, e.g. trade_ledger_2022.xlsx")
    ap.add_argument("--sheet", default=None, help="excel sheet name (optional)")
    ap.add_argument("--mysql-url", default=None, help="SQLAlchemy MySQL URL (optional, can use env MYSQL_URL)")
    args = ap.parse_args()

    mysql_url = args.mysql_url or os.getenv("MYSQL_URL")
    if not mysql_url:
        raise SystemExit(
            "Missing MySQL URL. Provide --mysql-url or env MYSQL_URL.\n"
            "Example:\n"
            "  export MYSQL_URL='mysql+pymysql://user:pass@127.0.0.1:3306/yourdb?charset=utf8mb4'"
        )

    rows = export_year_to_excel(
        mysql_url=mysql_url,
        year=args.year,
        out_xlsx=args.out,
        sheet_name=args.sheet,
    )
    print(f"Exported {rows} rows to {args.out}")


if __name__ == "__main__":
    main()
