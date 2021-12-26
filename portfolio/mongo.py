#! /usr/local/bin/python3

import json
import re
import time
from datetime import datetime
from pprint import pprint

import pandas as pd
from pymongo import MongoClient

pd.set_option('display.max_rows', 1000)
# pd.set_option('display.max_columns', 6)


class Mongo:
    def __init__(self, host='localhost', port=27017, database='portfolio'):
        client = MongoClient(host, port)
        self.db = client.get_database(database)

    def find(self, collection: str, conditions: dict, fields: dict) -> list:
        cursor = self.db.get_collection(collection).find(conditions, fields)
        num = cursor.count()
        print('Found {} documents'.format(num))
        return list(cursor)

    def find_last(self, collection: str) -> dict:
        return self.db.get_collection(collection).find_one({'$query': {}, '$orderby': {'_id': -1}})

    def get_list(self, prefix: str) -> list:
        return [name for name in self.db.list_collection_names() if name.startswith(prefix)]

    def save(self, collection: str, df: pd.DataFrame):
        dic = json.loads(df.T.to_json())        # use default date_format='epoch' instead of 'iso'
        collection = self.db[collection]
        collection.insert(dic.values())

    def save_securities(self, codes: list):
        for code in codes:
            if code in self.db.list_collection_names():
                print(code + ' is already in')
                continue
            print(code)
            df = pd.DataFrame()
            if re.match(r'(sh|sz)\d{6}', code) is not None:
                df = Mongo.index_price_daily(code)
            elif re.match(r'f\d{6}', code) is not None:
                df = Mongo.fund_nav_daily(code)
            else:
                assert True, print('code is not valid')
            self.save(code, df)
            time.sleep(1)

    def load_info(self, code: str) -> dict:
        dic = {}
        if re.match(r'(sh|sz)\d{6}', code) is not None:
            dic = self.db['indexes_info'].find_one({'_id': int(code[2:])})
            if dic is None:
                dic = self.db['on_market_info'].find_one({'_id': int(code[2:])})
        elif re.match(r'f\d{6}', code) is not None:
            dic = self.db['funds_info'].find_one({'_id': int(code[1:])})
        elif re.match(r'otc_\d{6}', code) is not None:
            dic = self.db['funds_info'].find_one({'_id': int(code[4:])})
        else:
            assert True, print('code is not valid')
        return dic

    def load_indicator(self, code: str) -> dict:
        dic = {}
        if re.match(r'otc_\d{6}', code):
            dic = self.db['funds_indicator'].find_one({'_id': int(code[4:])})
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
        elif re.match(r'otc_\d{6}', code) is not None:
            fields = {'refactor_nav': 1}
            names['refactor_nav'] = 'close'
        else:
            assert True, print('code is not valid')
        cursor = self.db[code].find({}, fields)
        df = pd.DataFrame(list(cursor))
        df['_id'] = pd.to_datetime(df['_id'], unit='ms')
        df = df.rename(names, axis=1)
        # print(df)
        return df

    def get_manager(self, code: str) -> list:
        assert re.match(r'otc_\d{6}', code)
        fund = self.load_info(code)['name']
        # print(fund)
        fields = {'_id': 0, 'name': 1, 'working_days': 1, 'total_scale': 1}
        cursor = self.db.get_collection('manager').find({'fund_name': fund}, fields)
        # return [x['name'] for x in list(cursor)]
        return list(cursor)

    def has_collection(self, code: str) -> bool:
        return code in self.db.list_collection_names()

    def drop(self, code: str):
        self.db.get_collection(code).drop()


def main():
    # otc_lst = Mongo().get_list('otc_')
    # pprint(otc_lst)
    # print(len(otc_lst))
    # ms = Mongo().find_last('otc_519688')['_id']
    # print(datetime.fromtimestamp(ms / 1000.0).strftime('%Y-%m-%d'))

    # code = 'sh000985'
    # print(mongo.load_info(code))
    # print(mongo.load_close_price(code))

    print(Mongo().get_manager('otc_166002'))


if __name__ == "__main__":
    main()
