#! /usr/local/bin/python3

from excel_tool import df_to_sheet
from mysql import MySql

def ledger_to_df(db: MySql, xlsx: str, year: int, currency: str):
    sql = """
        SELECT
            l.id,
            l.occurred_at,
            l.biz_type_code,
            l.amount,
            l.symbol,
            l.direction,
            s.security_name,
            b.affect_position,
            b.taxable_flag
        FROM trade_ledger l
        JOIN security_master s ON l.symbol = s.symbol
        JOIN biz_type_dict b ON l.biz_type_code = b.biz_type_code
        WHERE
            l.occurred_at >= :start AND l.occurred_at < :end AND s.currency = :currency
        ORDER BY
            l.occurred_at, l.id;
    """
    start = f"{year}-01-01 00:00:00"
    end = f"{year+1}-01-01 00:00:00"
    df = db.to_frame_with_interval(sql, start, end, currency)
    df_to_sheet(df, xlsx, '%d_%s' % (year, currency) , header=True)


def main():
    tuples = [
        (2022, 'HKD'), (2022, 'USD'),
        (2023, 'HKD'), (2023, 'USD'),
        (2024, 'HKD'), (2024, 'USD')
    ]
    db = MySql(database='portfolio')
    for t in tuples:
        ledger_to_df(db, 'tradeLedger.xlsx', *t)


if __name__ == "__main__":
    main()
