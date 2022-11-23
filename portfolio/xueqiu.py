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


def get_cookies(stock_code: str) -> RequestsCookieJar:
    # https://xueqiu.com/S/%s
    # 需要先请求页面获取cookie
    url_str = "https://xueqiu.com/S/%s" % stock_code
    headers = {
        'User-Agent': 'PostmanRuntime/7.29.2'
    }
    resp = request("GET", url_str, headers=headers)
    if resp.status_code == 200:
        return resp.cookies
    else:
        print(resp, resp.text)


def get_data(stock_code: str, period: str) -> pd.DataFrame:
    begin = int(time.time() * 1000)
    time_type = "before"
    count = 2000000000
    url_string = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=%s&begin=%d&period=%s&type=%s&count=%d" \
                 "&indicator=%s" % (
                     stock_code, begin, period, time_type, -count, "kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance")
    # print(url_string)
    headers = {
        'User-Agent': 'PostmanRuntime/7.29.2'
    }
    resp = request("GET", url_string, headers=headers, cookies=get_cookies(stock_code))
    resp.raise_for_status()
    resp.encoding = 'utf-8'
    data = json.loads(resp.text)
    columns = data['data']['column'][: 8]
    columns[0] = 'date'
    items = []
    for i in data['data']['item']:
        item = i[: 8]
        item[0] = datetime.fromtimestamp(item[0] / 1000).date()
        items.append(item)
    return pd.DataFrame(items, columns=columns)


def draw(df: pd.DataFrame, name: str, start_date: str = ''):
    df = df[['date', 'close']]
    df = df.rename({'close': name}, axis=1)
    if start_date:
        df = df[df['date'] >= datetime.strptime(start_date, "%Y-%m-%d").date()]
    df = df.dropna().set_index('date')
    print(df)
    df.index.name = None
    df.plot(figsize=(12, 8), grid=True)
    plt.show()


def main():
    # df = get_data('SZ128040', 'day')
    # draw(df, 'SZ128040', '2022-01-01')
    df = get_data("KWEB", 'day')
    draw(df, 'KWEB', '2022-01-01')


if __name__ == "__main__":
    main()
