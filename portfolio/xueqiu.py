#! /usr/bin/python3
import json
import os
import sys
import time
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from requests import request

from mysql import MySql

# pd.set_option('display.max_columns', 6)
# pd.set_option('display.max_rows', 4000)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


class Xueqiu:
    def __init__(self):
        url = 'https://xueqiu.com'
        self.headers = {'User-Agent': 'PostmanRuntime/7.29.2'}
        resp = request("GET", url, headers=self.headers)
        resp.raise_for_status()
        self.cookies = resp.cookies

    def get_name(self, code: str) -> str:
        url = 'https://stock.xueqiu.com/v5/stock/quote.json?symbol=%s' % code.upper()
        resp = request("GET", url, headers=self.headers, cookies=self.cookies)
        resp.raise_for_status()
        return resp.json()['data']['quote']['name']

    def get_data(self, code: str, begin_date: str = '', end_date: str = '') -> pd.DataFrame:
        symbol = code.upper()
        period = 'day'
        typ = 'before'
        indicator = 'kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance'
        count = 2000000000

        if begin_date:
            begin = int(time.mktime(time.strptime(begin_date, "%Y-%m-%d"))) * 1000
            if end_date:
                end = int(time.mktime(time.strptime(end_date, "%Y-%m-%d"))) * 1000
                url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?" \
                      "symbol=%s&period=%s&type=%s&begin=%d&end=%d&indicator=%s" % \
                      (symbol, period, typ, begin, end, indicator)
            else:
                url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?" \
                      "symbol=%s&period=%s&type=%s&begin=%d&count=%d&indicator=%s" % \
                      (symbol, period, typ, begin, count, indicator)
        else:
            if end_date:
                begin = int(time.mktime(time.strptime(end_date, "%Y-%m-%d"))) * 1000
            else:
                begin = int(time.time() * 1000)
            url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?" \
                  "symbol=%s&period=%s&type=%s&begin=%d&count=%d&indicator=%s" % \
                  (symbol, period, typ, begin, -count, indicator)
        # print(url)
        resp = request("GET", url, headers=self.headers, cookies=self.cookies)
        resp.raise_for_status()
        resp.encoding = 'utf-8'
        data = json.loads(resp.text)
        columns = data['data']['column'][: 8]
        columns[0] = 'timestamp'
        items = []
        for i in data['data']['item']:
            item = i[: 8]
            item[0] //= 1000
            items.append(item)
        return pd.DataFrame(items, columns=columns)

    def get_full(self, code: str, period: str = 'day') -> pd.DataFrame:
        df = self.get_data(code, period)
        df = df.rename({'timestamp': 'date'}, axis=1)
        df['date'] = df['date'].apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d'))
        return df

    def last_close(self, code: str) -> dict:
        name = self.get_name(code)
        df = self.get_full(code)
        df = df[['date', 'close']]
        dic = df.iloc[-1].to_dict()
        dic[name] = round(dic.pop('close'), 2)
        return dic

    def full_to_mysql(self, code: str, db: MySql):
        df = self.get_data(code)
        df['code'] = code
        df['name'] = self.get_name(code)
        df = df[['timestamp', 'code', 'name', 'open', 'high', 'low', 'close', 'volume']]
        print(df)
        db.from_frame('cvtbone_daily', df)


def draw(df: pd.DataFrame, name: str, start_date: str = ''):
    df = df[['date', 'close']]
    df = df.rename({'close': name}, axis=1)
    if start_date:
        df = df[df['date'] >= start_date]
    df = df.dropna().set_index('date')
    print(df)
    df.index.name = None
    df.plot(figsize=(12, 8), grid=True)
    plt.show()


def get_codes(file: str) -> list:
    with open(file) as f:
        text = f.read()
    blocks = text.split('代码')
    lines1 = blocks[1].split('\n')
    l1 = [row.split()[1] for row in lines1[1: -2]]
    lines5 = blocks[5].split('\n')
    l5 = [row.split()[1] for row in lines5[1: -2]]
    lines6 = blocks[6].split('\n')
    l6 = [row.split()[1] for row in lines6[1: -2]]
    lst = list(set(l1 + l5 + l6))
    lst = ['SH' + i if i.startswith('11') else 'SZ' + i for i in lst]
    return sorted(lst)


def batch(file: str):
    codes = get_codes(file)
    print(codes)
    snowball = Xueqiu()
    db = MySql(database='portfolio')
    for code in codes:
        snowball.full_to_mysql(code, db)
        time.sleep(0.2)


def main():
    if len(sys.argv) > 2:
        start, code = sys.argv[2], sys.argv[1]
        snowball = Xueqiu()
        print(snowball.get_name(code))
        df = snowball.get_full(code)
        print(df)
        draw(df, code, start)
    elif len(sys.argv) == 2:
        if not os.path.isfile(sys.argv[1]):
            code = sys.argv[1]
            snowball = Xueqiu()
            print(snowball.get_name(code))
            df = snowball.get_full(code)
            print(df)
        else:
            batch(sys.argv[1])
    else:
        print('Usage: %s code|file [yyyy-mm-dd]' % sys.argv[0])   # 'SZ128040' '2021-07-01'
        print('       %s file' % sys.argv[0])   # '/tmp/cvt.txt'
        sys.exit(1)

    # snowball = Xueqiu()
    # print(snowball.last_close(code))
    # print(snowball.get_data('SZ127007', begin_date='2022-01-01', end_date='2023-01-06'))
    # print(snowball.get_data('SZ127007', end_date='2023-01-06'))
    # snowball = Xueqiu()
    # db = MySql(database='portfolio')
    # snowball.full_to_mysql('SZ127007', db)


if __name__ == "__main__":
    main()
