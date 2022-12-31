#! /usr/local/bin/python3

from sqlalchemy import create_engine
import pandas as pd
# import pymysql

pd.set_option('display.max_rows', 4000)
# pd.set_option('display.max_columns', 6)


class MySql:
    def __init__(self, host='localhost', port=3306, user='manga', password='manga', database='finance'):
        self.db = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database))

    # def close(self):
    #     self.db.close()

    def to_frame(self, table: str, fields: list = None) -> pd.DataFrame:
        s = ','.join(fields) if fields else '*'
        return pd.read_sql('select {} from {}'.format(s, table), self.db)

    def from_frame(self, table: str, frame: pd.DataFrame):
        frame.to_sql(table, con=self.db, if_exists='append', index=False)


def main():
    db = MySql()
    df = db.to_frame('instant_price')
    # df = db.to_frame('instant_price', ['code', 'price'])
    print(df)


if __name__ == "__main__":
    main()
