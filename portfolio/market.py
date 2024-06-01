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

PID_ETF_A = 0
PID_HK = -7
PID_US = -6
PID_CVT = 8
PID_CVT_2 = 11
PID_CVT_3 = 12
PID_MISC = 4


class Market:
    fund_base = 'https://fund.xueqiu.com/dj/open/fund/deriveds?'

    URL_LIST = 'https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?'
    URL_STOCK = 'https://stock.xueqiu.com/v5/stock/batch/quote.json?'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.192 Safari/537.36',
    }
    with open('auth/xq_cookie.txt', 'r') as f:
        HEADERS['Cookie'] = f.read()[:-1]       # delete last '\n'

    @staticmethod
    def get_list(category: int, pid: int) -> list:
        params = {
            'size': 1000,
            'category': category,
            'pid': pid
        }
        url = Market.URL_LIST + urlencode(params)
        response = requests.request("GET", url, headers=Market.HEADERS)
        response.raise_for_status()
        stocks = json.loads(response.text)['data']['stocks']
        return [x['symbol'] for x in stocks]

    @staticmethod
    def get_stocks(pid: int) -> list:
        Market.HEADERS['Host'] = Market.URL_STOCK.split('/')[2]
        params = {
            'symbol': ','.join(Market.get_list(1, pid)),
            'extend': 'detail',
            'is_delay_hk': 'true'
        }
        url = Market.URL_STOCK + urlencode(params)
        # print(url)
        response = requests.get(url, headers=Market.HEADERS)
        response.raise_for_status()
        result = []
        items = response.json()['data']['items']
        for i in items:
            dic = {
                'code': i['quote']['symbol'],
                'ts': datetime.fromtimestamp(i['quote']['timestamp'] / 1000),
                'name': i['quote']['name'],
                'price': i['quote']['current'],
                'pct': i['quote']['percent']}
            result.append(dic.copy())
        return result

    @staticmethod
    def get_cvtbones(pid: int = None) -> list:
        Market.HEADERS['Host'] = Market.URL_STOCK.split('/')[2]
        if pid == PID_MISC:
            codes = Market.get_list(1, pid)
        else:
            codes = Market.get_list(1, PID_CVT)     # + Market.get_list(1, PID_CVT_2)
        params = {
            'symbol': ','.join(codes),
            'extend': 'detail',
            'is_delay_hk': 'true'
        }
        url = Market.URL_STOCK + urlencode(params)
        # print(url)
        response = requests.get(url, headers=Market.HEADERS)
        try:
            response.raise_for_status()
        except Exception as e:
            print(type(e))
            return []
        result = []
        items = response.json()['data']['items']
        for i in items:
            quote = i['quote']
            redeem = quote['conversion_price'] * 1.3                                # redeem trigger price
            share = quote['conversion_value'] / 100 * quote['conversion_price']     # share price
            dic = {
                # 'ts': datetime.fromtimestamp(quote['timestamp'] / 1000),
                'code': quote['symbol'],
                'name': quote['name'],
                'price': quote['current'],
                'premium': quote['premium_rate'],
                'remains': round(quote['outstanding_amt'] / quote['total_issue_scale'] * 100, 2),
                'days': (datetime.fromtimestamp(quote['maturity_date'] / 1000).date() - date.today()).days,
                'redeem': round((redeem - share) / share * 100, 2),
                'pct': quote['percent']
            }
            result.append(dic.copy())
        return result

    @staticmethod
    def get_funds(base_url: str, codes: list) -> list:
        Market.HEADERS['Host'] = base_url.split('/')[2]
        params = {
            'codes': ','.join(codes),
        }
        url = base_url + urlencode(params)
        # print(url)
        try:
            response = requests.get(url, headers=Market.HEADERS)
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

    if sys.argv[1] == 'a':
        result = Market.get_stocks(PID_ETF_A)
    elif sys.argv[1] == 'hk':
        result = Market.get_stocks(PID_HK)
    elif sys.argv[1] == 'us':
        result = Market.get_stocks(PID_US)
    elif sys.argv[1] == 'fund':
        funds = [
            '001556', '001594', '001810', '003318', '004069', '005259',
            '005827', '006327', '008138', '008407', '070023', '090010',
            '110003', '110011', '161005', '161128', '163402', '163407',
            '164906', '166002', '260108', '262001', '270002', '501021',
            '501050', '519671', '540003', '540006']
        result = Market.get_funds(Market.fund_base, funds)
    elif sys.argv[1] == 'cvtb':
        result = Market.get_cvtbones()
    elif sys.argv[1] == 'misc':
        result = Market.get_cvtbones(PID_MISC)
    # elif sys.argv[1] == 'grid':
    #     result = get_cvtbones(get_list(1, 12))
    else:
        print("Usage: {} a!cvtb|hk|us|fund".format(sys.argv[0]))
        sys.exit(1)

    # print(len(result))
    df = pd.DataFrame(result)
    if sys.argv[1] == 'cvtb':
        df = df.sort_values(by='pct', ascending=False)
    print(df)
    if sys.argv[1] != 'fund':
        print('mean({})'.format(round(df['pct'].mean(), 3)))

    # mysql = MySql()
    # mysql.from_frame('instant_price', df)

    mongo_host = '127.0.0.1'
    mongo_port = 27017
    mongo_db_name = 'finance'
    mongo_db_collection = 'xueqiu'

    # client = MongoClient(host=mongo_host, port=mongo_port)
    # db = client[mongo_db_name]
    # collection = db[mongo_db_collection]
    # collection.insert_many(result)


if __name__ == "__main__":
    main()
