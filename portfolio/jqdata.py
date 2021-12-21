#! /usr/bin/python3
import re
import time
from datetime import datetime

import jqdatasdk as jq
import numpy as np
import pandas as pd
from jqdatasdk import finance, query

from mongo import Mongo

jq.auth('13501071402', 'xuFengz2')
# pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100)


otc_funds = [
    '000071',      # "华夏恒生ETF联接",
    '000248',      # "汇添富中证消费ETF联接",
    '001556',      # "天弘中证500A",
    '001594',      # "天弘中证银行A",
    '003318',      # "景顺500低波",
    '004069',      # "南方中证全指证券",
    '006327',      # "易方达中证海外50ETF联接",
    '006341',      # "中金MSCI中国质量指数A",
    '040046',      # "华安纳斯达克100指数",
    '050025',      # "博时标普50ETF联接",'
    '090010',      # "大成中证红利",
    '110003',      # "易方达上证50指数A",
    '162412',      # "华宝医疗ETF联接A",
    '163407',      # "兴全沪深300A",
    '164906',      # "交银中证海外中国互联网",
    '501009',      # "汇添富中证生物科技",
    '501050',      # "华夏上证50AH",
    '501090',      # "华宝中证消费龙头",
    '519671',      # "银河300价值",
    '540012',      # "汇丰晋信A股龙头",

    '001643',      # "汇丰晋信智造先锋",
    '001717',      # "工银前沿医疗",
    '004350',      # "汇丰晋信价值先锋",
    '004868',      # "交银股息优化",
    '000595',      # "嘉实泰和",
    '001766',      # "上投摩根医疗健康",
    '001810',      # "中欧潜力价值",
    '001974',      # "景顺长城量化新动力",
    '003095',      # "中欧医疗健康A",
    '005259',      # "建信龙头企业",
    '005267',      # "嘉实价值精选",
    '005354',      # "富国沪港深行业精选A",
    '006228',      # "中欧医疗创新A",
    '110011',      # "易方达优质精选",
    '161005',      # "富国天惠成长",
    '163402',      # "兴全趋势投资",
    '163406',      # "兴全合润",
    '163415',      # "兴全商业模式优选",
    '166002',      # "中欧新蓝筹A",
    '169101',      # "东方红睿丰",
    '270002',      # "广发稳健增长混合A",
    '377240',      # "上投摩根新兴动力",
    '519035',      # "富国天博创新",
    '519688',      # "交银精选",
    '540003',      # "汇丰晋信动态策略A"
]


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
    def fund_nav_daily(code: str) -> pd.DataFrame:
        fields = (finance.FUND_NET_VALUE.day, finance.FUND_NET_VALUE.net_value,
                  finance.FUND_NET_VALUE.sum_value, finance.FUND_NET_VALUE.refactor_net_value)
        # q = query(*fields).filter(finance.FUND_NET_VALUE.code == code).\
        #     order_by(finance.FUND_NET_VALUE.day.desc()).limit(5)
        q = query(*fields).filter(finance.FUND_NET_VALUE.code == code)
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
        print(df)
        return df

    @staticmethod
    def get_updated_navs(codes: list, info, start, end=None) -> pd.DataFrame:
        if end is None:
            end = datetime.today().strftime('%Y-%m-%d')
        securities = [s + '.OF' for s in codes]
        df = jq.get_extras(info, securities, start_date=start, end_date=end, df=True)
        print(df)
        return df


def save_fund_nav(codes: list):
    mongo = Mongo()
    for code in codes:
        collection = 'otc_' + code
        if collection in mongo.db.list_collection_names():
            print(collection + ' is already in')
            continue
        print(collection)
        if re.match(r'\d{6}', code) is not None:
            df = JqData.fund_nav_daily(code)
            mongo.save(collection, df)
            time.sleep(1)


def main():
    funds = ['000595', "001766", "001974", "005267", "377240", "540003"]
    save_fund_nav(otc_funds)
    # df = JqData.get_updated_navs(funds, 'adj_net_value', '2021-12-13')


if __name__ == "__main__":
    main()
