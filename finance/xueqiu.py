#! /usr/bin/python3
import sys
from datetime import datetime
from pprint import pprint
from urllib.parse import urlencode

import pandas as pd
import requests
# from bson import Decimal128
from pymongo import MongoClient

from mysql import MySql

stock_base = 'https://stock.xueqiu.com/v5/stock/batch/quote.json?'
fund_base = 'https://fund.xueqiu.com/dj/open/fund/deriveds?'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.192 Safari/537.36'}

a_stocks = [
    'SH600009', 'SH600036', 'SH600104', 'SH600276', 'SH600309', 'SH600519',
    'SH600585', 'SH600660', 'SH600887', 'SH600900', 'SH601318', 'SH601901',
    'SH603288', 'SH603886',
    'SZ000002', 'SZ000333', 'SZ000651', 'SZ000858', 'SZ000895', 'SZ002271',
    'SZ002304', 'SZ002372', 'SZ002415', 'SZ002508', 'SZ002677', 'SZ300015']
cvtbones = [
    'SH113570', 'SH113591', 'SZ123023', 'SZ123110', 'SZ123127', 'SZ128021',
    'SZ128022', 'SZ128025', 'SZ128042', 'SZ128066', 'SZ128073', 'SZ128085',
    'SZ128100', 'SZ128119', 'SZ128130',
    'SH110070', 'SH113027', 'SH113039', 'SH113502', 'SH113504', 'SH113525',
    'SH113567', 'SH113598', 'SZ123080', 'SZ127007', 'SZ128029', 'SZ128034',
    'SZ128040', 'SZ128076', 'SZ128087', 'SZ128128']
a_etfs = [
    'SH501021', 'SH501050', 'SH510310', 'SH510580', 'SH510710', 'SH512000',
    'SH512170', 'SH512260', 'SH512800', 'SH515170', 'SH515180',
    'SZ159910', 'SZ159915', 'SZ159916', 'SZ159928']
hk_stocks = [
    '00345', '00388', '00405', '00700', '00778', '01928',
    '02020', '02840', '03033', '03690', '07200', '09988']
us_stocks = [
    'AAPL', 'ADBE', 'AMZN', 'ARKG', 'ARKK', 'ARKW', 'BABA', 'BILI', 'FB',
    'GBTC', 'GOOGL', 'GS', 'MSFT', 'PDD', 'QQQ', 'SPY', 'TSM', 'VTV', 'VXX']

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


def get_stocks(base_url: str, codes: list) -> list:
    headers['Host'] = base_url.split('/')[2]
    params = {
        'symbol': ','.join(codes),
        'extend': 'detail',
        'is_delay_hk': 'true'
    }
    url = base_url + urlencode(params)
    # print(url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = []
            items = response.json()['data']['items']
            for i in items:
                dic = {
                    'code': i['quote']['symbol'],
                    'timestamp': datetime.fromtimestamp(i['quote']['timestamp'] / 1000),
                    'name': i['quote']['name'],
                    'price': i['quote']['current'],
                    'percent': i['quote']['percent']}
                result.append(dic.copy())
            return result
    except requests.ConnectionError as e:
        print('Error', e.args)


def get_funds(base_url: str, codes: list) -> list:
    headers['Host'] = base_url.split('/')[2]
    params = {
        'codes': ','.join(codes),
    }
    url = base_url + urlencode(params)
    # print(url)
    try:
        response = requests.get(url, headers=headers)
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
        print('Usage: {} "a|hk|us|fund"'.format(sys.argv[0]))
        sys.exit(1)

    with open('auth/xq_cookie.txt', 'r') as f:
        headers['Cookie'] = f.read()[:-1]       # delete last '\n'

    if sys.argv[1] == 'a':
        result = get_stocks(stock_base, a_stocks) + get_stocks(stock_base, a_etfs)
    elif sys.argv[1] == 'hk':
        result = get_stocks(stock_base, hk_stocks)
    elif sys.argv[1] == 'us':
        result = get_stocks(stock_base, us_stocks)
    elif sys.argv[1] == 'fund':
        result = get_funds(fund_base, funds)
    elif sys.argv[1] == 'cvtb':
        result = get_stocks(stock_base, cvtbones)
    else:
        print("Usage: {} a!hk|us|fund".format(sys.argv[0]))
        sys.exit(1)

    # for i in result:
    #     i['type'] = sys.argv[1]
    # pprint(result)
    print(len(result))

    df = pd.DataFrame(result)
    print(df)

    mysql = MySql()
    mysql.from_frame('instant_price', df)

    # client = MongoClient(host=mongo_host, port=mongo_port)
    # db = client[mongo_db_name]
    # collection = db[mongo_db_collection]
    # collection.insert_many(result)


if __name__ == "__main__":
    main()
