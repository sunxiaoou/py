#! /usr/local/bin/python3

import json
import re
import sys
import time

import akshare as ak
import numpy as np
import pandas as pd
from pymongo import MongoClient

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 6)


class Mongo:
    def __init__(self, host='localhost', port=27017, database='portfolio'):
        client = MongoClient(host, port)
        self.db = client.get_database(database)

    @staticmethod
    def indexes_info() -> dict:
        df = ak.index_stock_info()
        df = df.rename({'index_code': '_id', 'display_name': 'name'}, axis=1)
        df['_id'] = df['_id'].apply(lambda x: int(x))
        print(df)
        return json.loads(df.T.to_json())

    @staticmethod
    def index_price_daily(code: str, source: str = None) -> dict:
        if source == 'tx':
            df = ak.stock_zh_index_daily_tx(symbol=code)
        elif source == 'em':
            df = ak.stock_zh_index_daily_em(symbol=code)
        else:
            df = ak.stock_zh_index_daily(symbol=code)
        df['date'] = pd.to_datetime(df['date'])
        df = df.rename({'date': '_id'}, axis=1)
        print(df)
        return json.loads(df.T.to_json())      # use default date_format='epoch' instead of 'iso'

    @staticmethod
    def funds_info() -> dict:
        df = ak.fund_em_fund_name()
        df = df.rename({'基金代码': '_id', '基金简称': 'name', '基金类型': 'type'}, axis=1)
        df['_id'] = df['_id'].apply(lambda x: int(x))
        df['typ2'] = df['type'].apply(lambda x: x.split('-')[1] if '-' in x else None)
        df['type'] = df['type'].apply(lambda x: x.split('-')[0])
        df = df[['_id', 'name', 'type', 'typ2']]
        print(df)
        return json.loads(df.T.to_json())

    @staticmethod
    def fund_nav_daily(code: str) -> dict:
        assert code[0] == 'f'
        code = code[1:]
        df = ak.fund_em_open_fund_info(code, indicator="单位净值走势")
        # print(df)
        df2 = ak.fund_em_open_fund_info(code, indicator="累计净值走势")
        df = pd.merge(df, df2, on='净值日期', how='outer')
        df2 = ak.fund_em_open_fund_info(code, indicator="同类排名百分比")
        # print(df2)
        df2 = df2.rename({'报告日期': '净值日期'}, axis=1)
        df = pd.merge(df, df2, on='净值日期', how='outer')
        df = df.rename({'净值日期': '_id', '单位净值': 'nav', '日增长率': 'growth_rate', '累计净值': 'cum_nav',
                        '同类型排名-每日近3月收益排名百分比': 'rank_3m'}, axis=1)
        if df.dtypes['nav'] != np.dtype('float64'):
            df['nav'] = df['nav'].apply(lambda x: None if x is None else float(x))
        if df.dtypes['cum_nav'] != np.dtype('float64'):
            df['cum_nav'] = df['cum_nav'].apply(lambda x: None if x is None else float(x))
        df['_id'] = pd.to_datetime(df['_id'])
        print(df)
        return json.loads(df.T.to_json())

    def save_securities(self, codes: list):
        for code in codes:
            if code in self.db.list_collection_names():
                print(code + ' is already in')
                continue
            print(code)
            dic = {}
            if re.match(r'(sh|sz)\d{6}', code) is not None:
                dic = Mongo.index_price_daily(code)
            elif re.match(r'f\d{6}', code) is not None:
                dic = Mongo.fund_nav_daily(code)
            else:
                assert True, print('code is not valid')
            collection = self.db[code]
            collection.insert(dic.values())
            time.sleep(1)

    def load_info(self, code: str) -> dict:
        dic = {}
        if re.match(r'(sh|sz)\d{6}', code) is not None:
            dic = self.db['indexes_info'].find_one({'_id': int(code[2:])})
        elif re.match(r'f\d{6}', code) is not None:
            dic = self.db['funds_info'].find_one({'_id': int(code[1:])})
        else:
            assert True, print('code is not valid')
        return dic

    def load_close_price(self, code: str) -> pd.DataFrame:
        assert code in self.db.list_collection_names()
        fields = {}
        names = {'_id': 'date'}
        if re.match(r'(sh|sz)\d{6}', code) is not None:
            fields = {'close': 1}
        elif re.match(r'f\d{6}', code) is not None:
            fields = {'cum_nav': 1}
            names['cum_nav'] = 'close'
        else:
            assert True, print('code is not valid')
        cursor = self.db[code].find({}, fields)
        df = pd.DataFrame(list(cursor))
        df['_id'] = pd.to_datetime(df['_id'], unit='ms')
        df = df.rename(names, axis=1)
        # print(df)
        return df


def main():
    # if len(sys.argv) < 2:
    #     print('Usage: {} code'.format(sys.argv[0]))
    #     sys.exit(1)

    # Mongo.indexes_info()
    mongo = Mongo()
    code = 'sh000985'
    code = 'sh502000'
    # code = 'f540003'
    print(mongo.load_info(code))
    print(mongo.load_close_price(code))


if __name__ == "__main__":
    main()
