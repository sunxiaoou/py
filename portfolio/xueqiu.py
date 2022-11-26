#! /usr/bin/python3
import json
import time
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from requests import request
from requests.cookies import RequestsCookieJar

# pd.set_option('display.max_columns', 6)
# pd.set_option('display.max_rows', 4000)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def get_cookies(code: str) -> RequestsCookieJar:
    url = "https://xueqiu.com/S/%s" % code
    headers = {
        'User-Agent': 'PostmanRuntime/7.29.2'
    }
    resp = request("GET", url, headers=headers)
    resp.raise_for_status()
    return resp.cookies


def get_name(code: str) -> str:
    url = 'https://stock.xueqiu.com/v5/stock/quote.json?symbol=%s' % code
    headers = {
        'User-Agent': 'PostmanRuntime/7.29.2'
    }
    resp = request("GET", url, headers=headers, cookies=get_cookies(code))
    resp.raise_for_status()
    return resp.json()['data']['quote']['name']


def get_data(code: str, period: str = 'day') -> pd.DataFrame:
    begin = int(time.time() * 1000)
    time_type = "before"
    count = 2000000000
    url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?" \
          "symbol=%s&begin=%d&period=%s&type=%s&count=%d&indicator=%s" % \
          (code, begin, period, time_type, -count, "kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance")
    # print(url)
    headers = {
        'User-Agent': 'PostmanRuntime/7.29.2'
    }
    resp = request("GET", url, headers=headers, cookies=get_cookies(code))
    resp.raise_for_status()
    resp.encoding = 'utf-8'
    data = json.loads(resp.text)
    columns = data['data']['column'][: 8]
    columns[0] = 'date'
    items = []
    for i in data['data']['item']:
        item = i[: 8]
        # item[0] = datetime.fromtimestamp(item[0] / 1000).date()
        item[0] = datetime.fromtimestamp(item[0] / 1000).strftime('%Y-%m-%d')
        items.append(item)
    return pd.DataFrame(items, columns=columns)


def draw(df: pd.DataFrame, name: str, start_date: str = ''):
    df = df[['date', 'close']]
    df = df.rename({'close': name}, axis=1)
    if start_date:
        # df = df[df['date'] >= datetime.strptime(start_date, "%Y-%m-%d").date()]
        df = df[df['date'] >= start_date]
    df = df.dropna().set_index('date')
    print(df)
    df.index.name = None
    df.plot(figsize=(12, 8), grid=True)
    plt.show()


def main():
    code = 'SZ128040'
    # code = 'KWEB'
    print(get_name(code))
    df = get_data(code)
    draw(df, code, '2022-01-01')


if __name__ == "__main__":
    main()
