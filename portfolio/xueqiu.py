#! /usr/bin/python3
import json
import sys
import time
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from requests import request

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
        url = 'https://stock.xueqiu.com/v5/stock/quote.json?symbol=%s' % code
        resp = request("GET", url, headers=self.headers, cookies=self.cookies)
        resp.raise_for_status()
        return resp.json()['data']['quote']['name']

    def get_data(self, code: str, period: str = 'day') -> pd.DataFrame:
        begin = int(time.time() * 1000)
        time_type = "before"
        count = 2000000000
        url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?" \
              "symbol=%s&begin=%d&period=%s&type=%s&count=%d&indicator=%s" % \
              (code, begin, period, time_type, -count, "kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance")
        # print(url)
        resp = request("GET", url, headers=self.headers, cookies=self.cookies)
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


def draw(df: pd.DataFrame, name: str, start_date: str):
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
    if len(sys.argv) > 2:
        start, code = sys.argv[2], sys.argv[1]
    elif len(sys.argv) == 2:
        start, code = '', sys.argv[1]
    else:
        print('Usage: %s code [yyyy-mm-dd]' % sys.argv[0])   # 'SZ128040' '2021-07-01'
        sys.exit(1)

    snowball = Xueqiu()
    print(snowball.get_name(code))
    df = snowball.get_data(code)
    print(df)
    # draw(df, code, start)


if __name__ == "__main__":
    main()
