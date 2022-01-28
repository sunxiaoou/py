#! /usr/bin/python3
import sys
from datetime import datetime
from pprint import pprint
from urllib.parse import urlencode

import requests
import pandas as pd
from openpyxl import load_workbook

from mongo import Mongo

CODE = 'SH000985'


def from_xlsx() -> pd.DataFrame:
    xlsx = '历史数据查询.xlsx'
    wb = load_workbook(xlsx)
    ws_name = wb.active.title
    excel = pd.ExcelFile(xlsx)
    df = pd.read_excel(excel, ws_name)[['日期', '中证全指']]
    df = df.rename({'日期': '_id', '中证全指': 'close'}, axis=1).sort_values('_id').reset_index(drop=True)
    df['_id'] = pd.to_datetime(df['_id'])
    return df


def from_web() -> pd.DataFrame:
    stock_base = 'https://stock.xueqiu.com/v5/stock/batch/quote.json?'
    headers = {
        'Host': stock_base.split('/')[2],
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.192 Safari/537.36'}
    params = {
        'symbol': CODE,
        'extend': 'detail',
        'is_delay_hk': 'true'}

    with open('auth/xq_cookie.txt', 'r') as f:
        headers['Cookie'] = f.read()[:-1]

    url = stock_base + urlencode(params)
    result = []
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            items = response.json()['data']['items']
            for i in items:
                dic = {
                    # 'code': i['quote']['symbol'],
                    '_id': datetime.fromtimestamp(i['quote']['timestamp'] / 1000).date(),
                    'open': round(i['quote']['open'], 2),
                    'close': round(i['quote']['current'], 2),
                    'high': round(i['quote']['high'], 2),
                    'low': round(i['quote']['low'], 2),
                    'volume': i['quote']['volume'],
                    'amount': i['quote']['amount']}
                result.append(dic.copy())
    except requests.ConnectionError as e:
        print('Error', e.args)

    df = pd.DataFrame(result)
    df['_id'] = pd.to_datetime(df['_id'])
    return df


def update_mongo(df: pd.DataFrame):
    mongo = Mongo()
    code = CODE.lower()
    ms = mongo.find_last(code)['_id']
    start = datetime.fromtimestamp(ms / 1000.0)
    df = df[df['_id'] > start]
    print('{} row(s)'.format(df.shape[0]))
    mongo.save(code, df)


def main():
    # update_mongo(from_xlsx())
    update_mongo(from_web())


if __name__ == "__main__":
    main()
