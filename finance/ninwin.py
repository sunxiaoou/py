#! /usr/bin/python3
import json
from urllib.parse import urlencode

from bs4 import BeautifulSoup
from requests import request
import pandas as pd

# pd.set_option('display.max_rows', 1000)
# pd.set_option('display.max_columns', 10)


def get_list(category: int, pid: int) -> list:
    url = 'https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?'
    params = {
        'size': 1000,
        'category': category,
        'pid': pid
    }
    url += urlencode(params)

    with open('auth/xq_cookie.txt', 'r') as f:
        cookie = f.read()
    headers = {
        'User-Agent': 'PostmanRuntime/7.29.2',      # to avoid response 500 error
        'Cookie': cookie
    }
    response = request("GET", url, headers=headers)
    response.raise_for_status()
    stocks = json.loads(response.text)['data']['stocks']
    return [x['symbol'] for x in stocks]


def ninwin(cbs: list) -> pd.DataFrame:
    # url = "https://www.ninwin.cn/index.php?m=cb&a=list&show_owned=1&show_owned_only=Y"
    url = "https://www.ninwin.cn/index.php?m=cb&show_cb_only=Y&show_listed_only=Y"

    with open('auth/nw_cookie.txt', 'r') as f:
        cookie = f.read()
    headers = {
        'User-Agent': 'PostmanRuntime/7.29.2',      # to avoid response 500 error
        'Cookie': cookie
    }
    response = request("GET", url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    tbody = soup.find('tbody')

    result = []
    for tr in tbody.find_all('tr'):
        code = tr['data-cb_code'].upper()
        if code in cbs:
            dic = {
                'code': code,
                'name': tr['data-cb_name'],
                'premium': round(float(tr['data-premium']) * 100, 2),
                'strike': tr.find('td', class_='cb_strike_id').text,
                'value': tr.find('td', class_='cb_value_id').text,
                'duration': tr.find('td', class_='cb_t_id bond_t bond_t1').text}
            result.append(dic.copy())
    return pd.DataFrame(result)


def main():
    print(ninwin(get_list(1, 8) + get_list(1, 11)))
    print(ninwin(get_list(1, 4)))


if __name__ == "__main__":
    main()
