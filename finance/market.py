#! /usr/bin/python3
import json
import sys
from datetime import date, datetime
from pprint import pprint
from urllib.parse import urlencode

import pandas as pd
import requests
# from bson import Decimal128
from pymongo import MongoClient

from mysql import MySql

fund_base = 'https://fund.xueqiu.com/dj/open/fund/deriveds?'

URL_LIST = 'https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?'
URL_STOCK = 'https://stock.xueqiu.com/v5/stock/batch/quote.json?'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.192 Safari/537.36',
}

funds = [
    '001556', '001594', '001810', '003318', '004069', '005259',
    '005827', '006327', '008138', '008407', '070023', '090010',
    '110003', '110011', '161005', '161128', '163402', '163407',
    '164906', '166002', '260108', '262001', '270002', '501021',
    '501050', '519671', '540003', '540006']

mongo_host = '127.0.0.1'
mongo_port = 27017
mongo_db_name = 'finance'
mongo_db_collection = 'xueqiu'


def get_list(category: int, pid: int) -> list:
    params = {
        'size': 1000,
        'category': category,
        'pid': pid
    }
    url = URL_LIST + urlencode(params)
    response = requests.request("GET", url, headers=HEADERS)
    assert response.status_code == 200
    stocks = json.loads(response.text)['data']['stocks']
    return [x['symbol'] for x in stocks]


def get_stocks(codes: list) -> list:
    HEADERS['Host'] = URL_STOCK.split('/')[2]
    params = {
        'symbol': ','.join(codes),
        'extend': 'detail',
        'is_delay_hk': 'true'
    }
    url = URL_STOCK + urlencode(params)
    # print(url)
    response = requests.get(url, headers=HEADERS)
    assert response.status_code == 200
    result = []
    items = response.json()['data']['items']
    for i in items:
        dic = {
            'code': i['quote']['symbol'],
            'ts': datetime.fromtimestamp(i['quote']['timestamp'] / 1000),
            'name': i['quote']['name'],
            'price': i['quote']['current'],
            'pc': i['quote']['percent']}
        result.append(dic.copy())
    return result


def get_cvtbones(codes: list) -> list:
    HEADERS['Host'] = URL_STOCK.split('/')[2]
    params = {
        'symbol': ','.join(codes),
        'extend': 'detail',
        'is_delay_hk': 'true'
    }
    url = URL_STOCK + urlencode(params)
    # print(url)
    response = requests.get(url, headers=HEADERS)
    assert response.status_code == 200
    result = []
    items = response.json()['data']['items']
    for i in items:
        quote = i['quote']
        dic = {
            # 'ts': datetime.fromtimestamp(quote['timestamp'] / 1000),
            'code': quote['symbol'],
            'name': quote['name'],
            'price': quote['current'],
            'premium': quote['convert_bond_ratio'],
            'remains': round(quote['outstanding_amt'] / quote['total_issue_scale'] * 100, 2),
            'days': (datetime.fromtimestamp(quote['maturity_date'] / 1000).date() - date.today()).days,
            'pc': quote['percent']
        }
        result.append(dic.copy())
    return result


def get_funds(base_url: str, codes: list) -> list:
    HEADERS['Host'] = base_url.split('/')[2]
    params = {
        'codes': ','.join(codes),
    }
    url = base_url + urlencode(params)
    # print(url)
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            result = []
            items = response.json()['data']
            for i in items:
                dic = {
                    'code': i['fd_code'],
                    'date': datetime.strptime(i['end_date'], '%Y-%m-%d'),
                    'name': i['fd_name'],
                    # 'price': Decimal128(i['unit_nav'])}
                    'price': float(i['unit_nav'])}
                result.append(dic.copy())
            return result
    except requests.ConnectionError as e:
        print('Error', e.args)


def main():
    if len(sys.argv) < 2:
        print('Usage: {} "a|cvtb|hk|us|fund"'.format(sys.argv[0]))
        sys.exit(1)

    with open('auth/xq_cookie.txt', 'r') as f:
        HEADERS['Cookie'] = f.read()[:-1]       # delete last '\n'

    if sys.argv[1] == 'a':
        result = get_stocks(get_list(1, 0))
    elif sys.argv[1] == 'hk':
        result = get_stocks(get_list(1, -7))
    elif sys.argv[1] == 'us':
        result = get_stocks(get_list(1, -6))
    elif sys.argv[1] == 'fund':
        result = get_funds(fund_base, funds)
    elif sys.argv[1] == 'cvtb':
        result = get_cvtbones(get_list(1, 8) + get_list(1, 11))
    elif sys.argv[1] == 'misc':
        result = get_cvtbones(get_list(1, 4))
    elif sys.argv[1] == 'grid':
        result = get_cvtbones(get_list(1, 12))
    else:
        print("Usage: {} a!hk|us|fund".format(sys.argv[0]))
        sys.exit(1)

    # print(len(result))
    df = pd.DataFrame(result)
    print(df.sort_values(by='pc', ascending=False))
    print('mean({})'.format(round(df['pc'].mean(), 3)))

    # mysql = MySql()
    # mysql.from_frame('instant_price', df)

    # client = MongoClient(host=mongo_host, port=mongo_port)
    # db = client[mongo_db_name]
    # collection = db[mongo_db_collection]
    # collection.insert_many(result)


if __name__ == "__main__":
    main()
