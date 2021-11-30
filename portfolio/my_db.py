#! /usr/bin/python3
import json
import re
import time
from datetime import datetime

import akshare as ak
import jqdatasdk as jq
import pandas as pd
from pymongo import MongoClient

mongo_host = '127.0.0.1'
mongo_port = 27017
mongo_db_name = 'portfolio'
# mongo_db_collection = 'daily'

# jq.auth('13501071402', 'xuFengz2')  # 账号是申请时所填写的手机号
# 设置行列不忽略
# pd.set_option('display.max_rows', 100000)
# pd.set_option('display.max_columns', 1000)

indexes = [
    "sz159928",     # "消费ETF",
    "sz161039",     # "1000增强",
    "sz164906",     # "中概互联网LOF",
    "sh501009",     # "生物科技LOF",
    "sh501050",     # "50AH",
    "sh501090",     # "消费龙头LOF",
    "sh502000",     # "500增强LOF",
    "sh510310",     # "沪深300",
    "sh510580",     # "中证500ETF易方达",
    "sh510710",     # "上证50",
    "sh512000",     # "券商ETF",
    "sh512170",     # "医疗ETF",
    "sh512260",     # "中证500低波ETF",
    "sh512800",     # "银行ETF",
    "sh513050",     # "中国互联网ETF",
    "sh515180",     # "红利ETF易方达",
    "sh515910",     # "质量ETF",
]

funds = [
    "f000071",      # "华夏恒生ETF联接",
    "f000248",      # "汇添富中证消费ETF联接",
    "f001556",      # "天弘中证500A",
    "f001594",      # "天弘中证银行A",
    "f003318",      # "景顺500低波",
    "f004069",      # "南方中证全指证券",
    "f006327",      # "易方达中证海外50ETF联接",
    "f006341",      # "中金MSCI中国质量指数A",
    "f040046",      # "华安纳斯达克100指数",
    "f050025",      # "博时标普500ETF联接",

    "f090010",      # "大成中证红利",
    "f110003",      # "易方达上证50指数A",
    "f162412",      # "华宝医疗ETF联接A",
    "f163407",      # "兴全沪深300A",
    "f164906",      # "交银中证海外中国互联网",
    "f501009",      # "汇添富中证生物科技",
    "f501050",      # "华夏上证50AH",
    "f501090",      # "华宝中证消费龙头",
    "f519671",      # "银河300价值",
    "f540012",      # "汇丰晋信恒生A股龙头",

    "f001643",      # "汇丰晋信智造先锋",
    "f001717",      # "工银前沿医疗",
    "f004868",      # "交银股息优化",
    "f000595",      # "嘉实泰和",
    "f001766",      # "上投摩根医疗健康",
    "f001810",      # "中欧潜力价值",
    "f001974",      # "景顺长城量化新动力",
    "f003095",      # "中欧医疗健康A",
    "f005259",      # "建信龙头企业",
    "f005267",      # "嘉实价值精选",
    "f005354",      # "富国沪港深行业精选A",
    "f006228",      # "中欧医疗创新A",
    "f110011",      # "易方达优质精选",
    "f161005",      # "富国天惠成长",
    "f163402",      # "兴全趋势投资",
    "f163406",      # "兴全合润",
    "f163415",      # "兴全商业模式优选",
    "f166002",      # "中欧新蓝筹A",
    "f169101",      # "东方红睿丰",
    "f270002",      # "广发稳健增长混合A",
    "f377240",      # "上投摩根新兴动力",
    "f519035",      # "富国天博创新",
    "f519688",      # "交银精选",
    "f540003",      # "汇丰晋信动态策略A"
]


def get_index_list() -> list:
    df = jq.get_all_securities(['index'])
    # print(df)
    return list(df.index)


def get_single_price(code: str, freq: str, start=None, end=None) -> pd.DataFrame:
    if start is None:
        start = jq.get_security_info(code).start_date
    if end is None:
        end = datetime.today()
    df = jq.get_price(code, start_date=start, end_date=end, frequency=freq, panel=False)
    print(df)
    return df


def indexes_info() -> dict:
    df = ak.index_stock_info()
    df = df.rename({'index_code': '_id', 'display_name': 'name'}, axis=1)
    df['_id'] = df['_id'].apply(lambda x: int(x))
    print(df)
    return json.loads(df.T.to_json())


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


def funds_info() -> dict:
    df = ak.fund_em_fund_name()
    df = df.rename({'基金代码': '_id', '基金简称': 'name', '基金类型': 'type'}, axis=1)
    df['_id'] = df['_id'].apply(lambda x: int(x))
    df['typ2'] = df['type'].apply(lambda x: x.split('-')[1] if '-' in x else None)
    df['type'] = df['type'].apply(lambda x: x.split('-')[0])
    df = df[['_id', 'name', 'type', 'typ2']]
    print(df)
    return json.loads(df.T.to_json())


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
    df['_id'] = pd.to_datetime(df['_id'])
    print(df)
    return json.loads(df.T.to_json())


def save_securities(codes: list, db: MongoClient):
    for code in codes:
        if code in db.list_collection_names():
            print(code + ' is already in')
            continue
        print(code)
        dic = {}
        if re.match(r'(sh|sz)\d{6}', code) is not None:
            dic = index_price_daily(code)
        elif re.match(r'f\d{6}', code) is not None:
            dic = fund_nav_daily(code)
        else:
            assert True, print('code is not valid')
        collection = db[code]
        collection.insert(dic.values())
        time.sleep(1)


def load_security(code: str, db: MongoClient) -> pd.DataFrame:
    cursor = db[code].find()
    df = pd.DataFrame(list(cursor))
    df['_id'] = pd.to_datetime(df['_id'], unit='ms')
    print(df)
    return df


def main():
    client = MongoClient(host=mongo_host, port=mongo_port)
    db = client[mongo_db_name]

    dic = indexes_info()
    collection = db['indexes_info']
    collection.insert(dic.values())

    # code = 'sh000985'
    # dic = index_price_daily(code, 'em')
    # collection = db[code]
    # collection.insert(dic.values())
    # save_securities(indexes, db)

    # dic = funds_info()
    # collection = db['funds_info']
    # collection.insert(dic.values())

    # fund_nav_daily('f163406')
    # save_securities(funds, db)

    # load_security('f540003', db)


if __name__ == "__main__":
    main()
