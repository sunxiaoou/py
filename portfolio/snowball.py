#! /usr/bin/python3
import json
import os
import sys
import time
from datetime import datetime, date, timedelta
from urllib.parse import urlencode

import matplotlib.pyplot as plt
import pandas as pd
from requests import request

from mysql import MySql

# pd.set_option('display.max_columns', 6)
# pd.set_option('display.max_rows', 4000)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

PID_ETF_A = 0
PID_HK = -7
PID_US = -6
PID_CVT = 8
PID_CVT_2 = 11
PID_CVT_3 = 12
PID_MISC = 4


class Snowball:
    def __init__(self):
        url = 'https://xueqiu.com'
        self.headers = {'User-Agent': 'PostmanRuntime/7.29.2'}
        resp = request("GET", url, headers=self.headers)
        resp.raise_for_status()
        self.cookies = resp.cookies
        with open('auth/xq_cookie.txt', 'r') as f:
            self.my_cookies = f.read()

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
        if len(columns) == 0:
            return pd.DataFrame()
        columns[0] = 'date'
        items = []
        for i in data['data']['item']:
            item = i[: 8]
            item[0] = datetime.fromtimestamp(item[0] // 1000)
            items.append(item)
        return pd.DataFrame(items, columns=columns)

    def last_close(self, code: str) -> dict:
        name = self.get_name(code)
        df = self.get_data(code)
        df = df[['date', 'close']]
        dic = df.iloc[-1].to_dict()
        dic[name] = round(dic.pop('close'), 2)
        return dic

    def get_cvt_bones(self, codes: list) -> pd.DataFrame:
        params = {
            'symbol': ','.join(codes),
            'extend': 'detail',
            'is_delay_hk': 'true'
        }
        url = 'https://stock.xueqiu.com/v5/stock/batch/quote.json?' + urlencode(params)
        resp = request("GET", url, headers=self.headers, cookies=self.cookies)
        resp.raise_for_status()
        result = []
        items = resp.json()['data']['items']
        for i in items:
            quote = i['quote']
            redeem = quote['conversion_price'] * 1.3                                # redeem trigger price
            share = quote['conversion_value'] / 100 * quote['conversion_price']     # share price
            dic = {
                # 'ts': datetime.fromtimestamp(quote['timestamp'] / 1000),
                '代码': quote['symbol'][2:],
                '名称': quote['name'],
                '价格': quote['current'],
                '溢价率%': quote['premium_rate'],
                '剩余规模%': round(quote['outstanding_amt'] / quote['total_issue_scale'] * 100, 2),
                '剩余天数': (datetime.fromtimestamp(quote['maturity_date'] / 1000).date() - date.today()).days,
                '距强赎%': round((redeem - share) / share * 100, 2),
                '涨跌幅%': quote['percent']
            }
            result.append(dic.copy())
        return pd.DataFrame(result)

    def my_list(self, category: int, pid: int) -> list:
        params = {
            'size': 1000,
            'category': category,
            'pid': pid
        }
        url = 'https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?' + urlencode(params)
        header = self.headers.copy()
        header['Cookie'] = self.my_cookies
        resp = request("GET", url, headers=header)
        resp.raise_for_status()
        stocks = resp.json()['data']['stocks']
        return [x['symbol'] for x in stocks]

    def my_cvt_bones(self):
        return self.get_cvt_bones(self.my_list(1, PID_CVT))     # + self.my_list(1, 12)


def draw(df: pd.DataFrame, name: str):
    df = df[['date', 'close']]
    df = df.rename({'close': name}, axis=1)
    df = df.dropna().set_index('date')
    print(df)
    df.index.name = None
    df.plot(figsize=(12, 8), grid=True)
    plt.show()


def get_codes(file: str) -> list:
    with open(file) as f:
        text = f.read()
    blocks = text.split('代码')
    lines2 = blocks[2].split('\n')
    inner = [row.split()[1] for row in lines2[1: -2]]
    lines3 = blocks[3].split('\n')
    to_buy = [row.split()[1] for row in lines3[1: -2]]
    to_sell = []
    if len(blocks) > 4:
        lines4 = blocks[4].split('\n')
        to_sell = [row.split()[1] for row in lines4[1: -1]]
    lst = list(set(inner + to_buy + to_sell))
    lst = ['SH' + i if i.startswith('11') else 'SZ' + i for i in lst]
    return sorted(lst)


def get_data(code: str, db: MySql, snowball: Snowball) -> pd.DataFrame:
    dic = db.last_row('cvtbone_daily', 'date', 'code = "%s"' % code)
    if not dic:
        df = snowball.get_data(code)
        dic['name'] = snowball.get_name(code)
    else:
        begin_date = (dic['date'] + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        df = snowball.get_data(code, begin_date)
    # print(df)
    if not df.empty:
        df['code'] = code
        df['name'] = dic['name']
        df = df[['date', 'code', 'name', 'open', 'high', 'low', 'close', 'volume']]
    return df


def batch(file: str):
    codes = get_codes(file)
    print(codes)
    db = MySql(database='portfolio')
    snowball = Snowball()
    for code in codes:
        df = get_data(code, db, snowball)
        if not df.empty:
            print(df)
            db.from_frame('cvtbone_daily', df)
        time.sleep(0.2)


def get_etf_codes() -> list:
    db = MySql(database='portfolio')
    df = db.to_frame('threshold')
    # df['onsite'] = df['onsite'].apply(lambda x: None if x is None else 'SH' + x if x[0] == '5' else 'SZ' + x)
    # df['offsite'] = df['offsite'].apply(lambda x: None if x is None else 'F' + x)
    codes = df['onsite'].tolist()
    return [x for x in codes if x is not None]


def batch_etf():
    snowball = Snowball()
    db = MySql()
    for code in get_etf_codes() + ['KWEB', 'TLT', '03033']:
        df = snowball.get_data(code, '2017-06-15')
        if not df.empty:
            df['code'] = code
            df['name'] = snowball.get_name(code)
            df = df[['date', 'code', 'name', 'open', 'high', 'low', 'close', 'volume']]
            print(df)
            db.from_frame('etf_daily', df)
        time.sleep(0.2)


def main():
    batch_etf()
    sys.exit(0)
    # print(snowball.last_close('SZ127007'))
    # print(snowball.get_data('SZ127007', begin_date='2022-01-01', end_date='2023-01-06'))
    # print(snowball.get_data('SZ127007', end_date='2023-01-06'))

    if len(sys.argv) > 2:
        begin_date, code = sys.argv[2], sys.argv[1]
        snowball = Snowball()
        print(snowball.get_name(code))
        df = snowball.get_data(code, begin_date)
        print(df)
        draw(df, code)
    elif len(sys.argv) == 2:
        if not os.path.isfile(sys.argv[1]):
            db = MySql(database='portfolio')
            snowball = Snowball()
            print(get_data(sys.argv[1], db, snowball))
        else:
            batch(sys.argv[1])
    else:
        print('Usage: %s code [yyyy-mm-dd]' % sys.argv[0])   # 'SZ128040' '2021-07-01'
        print('       %s file' % sys.argv[0])   # '/tmp/cvt.txt'
        sys.exit(1)


if __name__ == "__main__":
    main()
