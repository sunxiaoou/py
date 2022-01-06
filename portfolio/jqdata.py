#! /usr/bin/python3
import re
import time
from datetime import datetime, timedelta
from pprint import pprint

import jqdatasdk as jq
import numpy as np
import pandas as pd
from jqdatasdk import finance, query

from mongo import Mongo

jq.auth('13501071402', 'xuFengz2')
# pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100)


class JqData:
    @staticmethod
    def get_single_price(code: str, freq: str, start=None, end=None) -> pd.DataFrame:
        if start is None:
            start = jq.get_security_info(code).start_date
        if end is None:
            end = datetime.today()
        df = jq.get_price(code, start_date=start, end_date=end, frequency=freq, panel=False)
        print(df)
        return df

    @staticmethod
    def fund_nav_daily(code: str, start=None) -> pd.DataFrame:
        fields = (finance.FUND_NET_VALUE.day, finance.FUND_NET_VALUE.net_value,
                  finance.FUND_NET_VALUE.sum_value, finance.FUND_NET_VALUE.refactor_net_value)
        # q = query(*fields).filter(finance.FUND_NET_VALUE.code == code).\
        #     order_by(finance.FUND_NET_VALUE.day.desc()).limit(5)
        q = query(*fields).filter(finance.FUND_NET_VALUE.code == code)
        if start is not None:
            q = q.filter(finance.FUND_NET_VALUE.day > start)
        df = finance.run_query(q)
        df = df.rename({'day': '_id', 'net_value': 'nav', 'sum_value': 'cum_nav',
                        'refactor_net_value': 'refactor_nav'}, axis=1)
        df['_id'] = pd.to_datetime(df['_id'])
        if df.dtypes['nav'] != np.dtype('float64'):
            df['nav'] = df['nav'].apply(lambda x: None if x is None else float(x))
        if df.dtypes['cum_nav'] != np.dtype('float64'):
            df['cum_nav'] = df['cum_nav'].apply(lambda x: None if x is None else float(x))
        if df.dtypes['refactor_nav'] != np.dtype('float64'):
            df['refactor_nav'] = df['refactor_nav'].apply(lambda x: None if x is None else float(x))
        # print(df)
        return df

    @staticmethod
    def get_scale(code: str) -> tuple:
        fields = (finance.FUND_FIN_INDICATOR.period_end, finance.FUND_FIN_INDICATOR.total_tna)
        df = finance.run_query(query(*fields).filter(finance.FUND_FIN_INDICATOR.code == code).
                               order_by(finance.FUND_FIN_INDICATOR.pub_date.desc()).limit(1))
        return df.loc[0, 'period_end'], df.loc[0, 'total_tna']


def save_fund_nav(codes: list, mongo=None):
    if not mongo:
        mongo = Mongo()
    for code in codes:
        collection = 'otc_' + code
        if mongo.has_collection(collection):
            print(collection + ' is already in')
            continue
        print(collection)
        if re.match(r'\d{6}', code) is not None:
            df = JqData.fund_nav_daily(code)
            mongo.save(collection, df)
            time.sleep(1)


def update_fund_nav(prefix: str, mongo=None):
    if not mongo:
        mongo = Mongo()

    for code in mongo.get_list(prefix):
        ms = mongo.find_last(code)['_id']
        start = datetime.fromtimestamp(ms / 1000.0).strftime('%Y-%m-%d')
        print(code, start)
        df = JqData.fund_nav_daily(code.lstrip(prefix), start)
        if df.empty:
            print('empty')
            continue
        print(df)
        print()
        mongo.save(code, df)


def save_screw_otc():
    mongo = Mongo()
    dics = mongo.find('threshold', {}, {'场外代码': True})
    funds = [dic['场外代码'] for dic in dics if dic['场外代码']]
    save_fund_nav(funds, mongo)


def save_scales(prefix: str, codes=None, mongo=None):
    if not mongo:
        mongo = Mongo()
    result = []
    lst = codes if codes else mongo.get_list(prefix)
    for code in lst:
        code = code.lstrip(prefix)
        dic = {'_id': code}
        dic['period_end'], dic['total_tna'] = JqData.get_scale(code)
        result.append(dic)
    df = pd.DataFrame(result)
    df['_id'] = df['_id'].apply(lambda x: int(x))
    df['total_tna'] = df['total_tna'].apply(lambda x: round(float(x / 100000000), 2))
    df = df.sort_values('_id')
    print(df)
    mongo.save('funds_indicator', df)


def main():
    # codes = ['001487', '001877']
    # save_fund_nav(codes)
    # save_scales('otc_', codes)
    # for code in ['otc_' + code for code in codes]:
    #     print(code, Mongo().get_manager(code))

    # save_screw_otc()
    # df = JqData.fund_nav_daily('012348')
    # df = JqData.fund_nav_daily('377240', '2021-12-16')
    # print(df)
    update_fund_nav('otc_')


if __name__ == "__main__":
    main()
