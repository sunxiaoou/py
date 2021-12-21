#! /usr/local/bin/python3

import json
import re
import sys
import time
from datetime import datetime
from pprint import pprint

import akshare as ak
import numpy as np
import pandas as pd
from pymongo import MongoClient

pd.set_option('display.max_rows', 1000)
# pd.set_option('display.max_columns', 6)

columns = ['代码', '_id', '参考指标', '最低', '低估', '高估', '最高']
thresholds = [
    ('000015', '上证红利', '盈利收益率', 17.5, 10, 6.4, 2.27),
    ('950090', '50AH优选', '盈利收益率', 16.6, 10, 6.4, 2.22),
    ('000925', '基本面50', '盈利收益率', 16.6, 10, 6.4, 2.22),
    ('399550', '央视50', '盈利收益率', 16.6, 10, 6.4, 2.5),
    ('000922', '中证红利', '盈利收益率', 16.6, 10, 6.4, 1.6),
    ('000919', '300价值', '盈利收益率', 16.6, 10, 6.4, 2.22),
    ('000016', '上证50', '盈利收益率', 14.5, 10, 6.4, 2.22),
    ('000010', '上证180', '盈利收益率', 13.9, 10, 6.4, 2.17),
    ('HSCEI', 'H股指数', '盈利收益率', 17.5, 10, 6.4, 3.45),
    ('HSI', '恒生指数', '盈利收益率', 14.5, 10, 6.4, 4.76),

    ('399986', '银行行业', '市净率', 0.75, 0.9, 1.15, 1.4),
    ('399393', '地产行业', '市净率', 1.2, 1.6, 2.2, 4),
    ('399975', '证券行业', '市净率', 1.05, 1.6, 2.2, 4.8),
    ('399967', '军工行业', '市净率', 2.1, 2.6, 4, 9.2),
    ('000827', '环保行业', '市净率', 1.82, 2.3, 3, 5.9),
    ('399995', '基建行业', '市净率', 0.92, 1.1, 1.8, 3.6),
    ('931009', '建筑材料', '市净率', 1.4, 1.8, 2.1, 3.1),

    # ('000985', '中证全指', '市盈率', 11, 14, 21, 54),
    ('000903', '中证100', '市盈率', 7, 11, 15, 45),
    ('000300', '沪深300', '市盈率', 8, 11, 17, 49),
    ('930782', '500低波动', '市盈率', 17, 24, 30, 60),
    ('000905', '500增强', '市盈率', 17, 25, 40, 93),
    ('000852', '中证1000', '市盈率', 19, 35, 48, 145),
    ('CSPSADRP', '红利机会', '市盈率', 8, 13, 20, 30),
    ('399812', '中证养老', '市盈率', 17, 21, 27, 36),
    ('399006', '创业板', '市盈率', 27, 25, 45, 138),
    ('399330', '深证100', '市盈率', 12, 18, 24, 64),
    ('000978', '医药100', '市盈率', 23, 28, 36, 63),
    ('399989', '中证医疗', '市盈率', 32, 55, 75, 140),
    ('930743', '生物科技', '市盈率', 33, 57, 81, 135),
    # ('931152', '创新药', '市盈率', 29, 50, 70, 130),
    ('931187', '科技100', '市盈率', 18, 26, 40, 56),
    ('000932', '中证消费', '市盈率', 17, 30, 40, 53),
    ('399997', '中证白酒', '市盈率', 15, 30, 40, 71),
    ('930653', '食品饮料', '市盈率', 18, 30, 40, 65),
    ('000989', '可选消费', '市盈率', 15, 18, 26, 45),
    # ('686000', '可选消费', '市净率', 1.7, 2.2, 4, 5.3),
    ('H30094', '消费红利', '市盈率', 11, 25, 33, 45),
    ('931068', '消费龙头', '市盈率', 16, 24, 32, 45),
    ('931357', '沪港深消费50', '市盈率', 25, 33, 42, 56),
    ('399001', '深证成指', '市盈率', 11, 15, 30, 62),
    ('399701', '基本面60', '市盈率', 12, 17, 20, 60),
    ('399702', '基本面120', '市盈率', 13, 18, 22, 60),
    ('399324', '深红利', '市盈率', 11, 15, 22, 44),
    ('NDX', '纳斯达克100', '市盈率', 15, 20, 30, 85),
    ('SPX', '标普500', '市盈率', 5.8, 15, 25, 44),
    ('S5INFT', '标普科技', '市盈率', 15, 21, 30, 90),
    ('IXY', '美股消费', '市盈率', 15, 21, 30, 45),
    ('SPG120035', '全球医疗', '市盈率', 15, 21, 30, 45),
    ('SPHCMSHP', '香港中小', '市盈率', 8.4, 12, 17, 20),
    ('H30533', '中概互联', '市销率', 3.74, 5.6, 8, 12.8),
    ('HSTECH', '恒生科技', '市销率', 3.2, 4, 5.6, 9),
    ('HSCAIT', 'A股龙头', '市盈率', 8, 11, 13, 15),
    ('931142', '竞争力指数', '市盈率', 10, 13, 18, 23),
    ('707717', 'MSCI质量', '市盈率', 17, 26, 38, 55),
    ('000688', '科创50', '市盈率', 55, 50, 80, 100),
    ('930697', '家用电器', '市盈率', 12, 17, 20, 28)]


class Mongo:
    def __init__(self, host='localhost', port=27017, database='portfolio'):
        client = MongoClient(host, port)
        self.db = client.get_database(database)

    def find(self, collection: str, conditions: dict, fields: dict) -> list:
        cursor = self.db.get_collection(collection).find(conditions, fields)
        num = cursor.count()
        print('Found {} documents'.format(num))
        return list(cursor)

    def get_list(self, prefix: str) -> list:
        return [name for name in self.db.list_collection_names() if name.startswith(prefix)]

    def get_min_last_id(self, prefix: str) -> int:
        return min([
            self.db.get_collection(name).find_one({'$query': {}, '$orderby': {'_id': -1}})['_id']
            for name in self.get_list(prefix)
        ])

    @staticmethod
    def indexes_info() -> pd.DataFrame:
        df = ak.index_stock_info()
        df = df.rename({'index_code': '_id', 'display_name': 'name'}, axis=1)
        df['_id'] = df['_id'].apply(lambda x: int(x))
        print(df)
        return df

    @staticmethod
    def on_market_info() -> pd.DataFrame:
        df = ak.fund_etf_category_sina(symbol='ETF基金')[['代码', '名称']]
        # print(df)
        df2 = ak.fund_etf_category_sina(symbol='LOF基金')[['代码', '名称']]
        df3 = ak.fund_etf_category_sina(symbol='封闭式基金')[['代码', '名称']]
        df = pd.concat([df, df2, df3], ignore_index=True, sort=False)
        df = df.rename({'代码': 'code', '名称': 'name'}, axis=1)
        df['_id'] = df['code'].apply(lambda x: int(x[2:]))
        print(df)
        return df

    @staticmethod
    def index_price_daily(code: str, source: str = None) -> pd.DataFrame:
        if source == 'tx':
            df = ak.stock_zh_index_daily_tx(symbol=code)
        elif source == 'em':
            df = ak.stock_zh_index_daily_em(symbol=code)
        else:
            df = ak.stock_zh_index_daily(symbol=code)
        df['date'] = pd.to_datetime(df['date'])
        df = df.rename({'date': '_id'}, axis=1)
        print(df)
        return df

    @staticmethod
    def funds_info() -> pd.DataFrame:
        df = ak.fund_em_fund_name()
        df = df.rename({'基金代码': '_id', '基金简称': 'name', '基金类型': 'type'}, axis=1)
        df['_id'] = df['_id'].apply(lambda x: int(x))
        df['typ2'] = df['type'].apply(lambda x: x.split('-')[1] if '-' in x else None)
        df['type'] = df['type'].apply(lambda x: x.split('-')[0])
        df = df[['_id', 'name', 'type', 'typ2']]
        print(df)
        return df

    @staticmethod
    def index_pe_daily(name: str):
        # df = ak.index_value_name_funddb()

        df = ak.index_value_hist_funddb(symbol=name, indicator="市盈率")
        print(df)

    @staticmethod
    def fund_nav_daily(code: str) -> pd.DataFrame:
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
        return df

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


def main():
    # if len(sys.argv) < 2:
    #     print('Usage: {} code'.format(sys.argv[0]))
    #     sys.exit(1)

    # Mongo.index_pe_daily('上证50')
    # Mongo.indexes_info()
    # Mongo.on_market_info()

    # mongo = Mongo()
    # df = pd.DataFrame(thresholds, columns=columns)
    # print(df)
    # mongo.save('thresholds', df)

    # otc_lst = Mongo().get_list('otc_')
    # pprint(otc_lst)
    # print(len(otc_lst))

    ms = Mongo().get_min_last_id('otc_')
    print(datetime.fromtimestamp(ms/1000.0))

    # mongo.save('on_market_info', Mongo.on_market_info())
    # code = 'sh000985'
    # code = 'sh502000'
    # # code = 'f540003'
    # print(mongo.load_info(code))
    # print(mongo.load_close_price(code))


if __name__ == "__main__":
    main()
