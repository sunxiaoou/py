#! /usr/bin/python3
import sys
from datetime import datetime
from pprint import pprint

import requests
from pymongo import MongoClient

risks = {
    '000730': 0,    # 现金宝
    '001810': 3,    # 中欧潜力价值混合
    '004069': 2,    # 南方中证全指证券联接A
    '005259': 3,    # 建信龙头企业股票
    '006327': 2,    # 易方达中概互联50ETF联接人民币A
    '110011': 3,    # 易方达中小盘混合
    '161128': 2,    # 易方达标普信息科技
    '501050': 2,    # 华夏上证50AH优选指数（LOF）A
    'CSI1014': 1,   # 我要稳稳的幸福
    'CSI1019': 1    # 钉钉宝365天组合
}


def danjuan(plan='') -> list:
    with open('auth/dj_cookie.txt', 'r') as f:
        cookie = f.read()[:-1]      # delete last '\n'
    url = 'https://danjuanapp.com/djapi/holding/'
    headers = {
        'Cookie': cookie,
        'Host': url.split('/')[2],
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.192 Safari/537.36'}

    if not plan:
        url += 'summary'
    else:
        url += 'plan/' + plan
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = []
            ts = response.json()['data']['ts']
            year = datetime.fromtimestamp(ts / 1000).strftime("%Y")
            items = response.json()['data']['items']
            for i in items:
                if not plan:
                    code = i['fd_code']
                    dic = {
                        'code': code,
                        'date': datetime.fromtimestamp(i['ts'] / 1000),
                        'name': i['fd_name'],
                        'nav': i['nav'],
                        'hold_gain': i['hold_gain'],
                        'market_value': i['market_value'],
                        'platform': '蛋卷'}
                    if code not in ['CSI666', 'CSI1033']:
                        dic['risk'] = risks[code]
                        result.append(dic.copy())
                    else:
                        result.extend(danjuan(plan=dic['code']))
                else:
                    plan_code = i['plan_code']
                    dic = {
                        'code': i['fd_code'],
                        'date': datetime.strptime(year + '-' + i['nav_date'], '%Y-%m-%d'),
                        'name': i['fd_name'],
                        'nav': i['nav'],
                        'hold_gain': i['hold_gain'],
                        'market_value': i['market_value'],
                        'platform': '蛋卷' + plan_code,
                        'risk': 2 if plan_code == 'CSI666' else 3
                    }
                    if dic['market_value']:
                        result.append(dic.copy())
            if not plan:
                pprint(result)
            return result
    except requests.ConnectionError as e:
        print('Error', e.args)


def tonghs() -> list:
    with open('auth/ths_cookie.txt', 'r') as f:
        cookie = f.read()[:-1]      # delete last '\n'
    url = 'https://trade.5ifund.com/pc_query/trade_queryIncomeWjZeroList.action?_=1615356614458'
    url2 = 'https://trade.5ifund.com/pc_query/trade_currentShareList.action?_=1615344156640'
    headers = {
        'Cookie': cookie,
        'Host': url.split('/')[2],
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.192 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'}

    try:
        result = []
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            items = response.json()['singleData']['IncomeShareListResult']
            for i in items:
                dic = {
                    'code': i['fundCode'],
                    'date': datetime.strptime(i['fundDate'], '%Y-%m-%d'),
                    'hold_gain': float(i['sumIncome']),
                    'market_value': float(i['totalVol']),
                    'name': i['fundName'],
                    'nav': 1,
                    'platform': '同花顺',
                    'risk': 0}
                result.append(dic.copy())

        response = requests.get(url2, headers=headers)
        if response.status_code == 200:
            items = response.json()['singleData']['currentShareList']
            for i in items:
                dic = {
                    'code': i['fundCode'],
                    'date': datetime.strptime(i['alternationdate'], '%Y%m%d'),
                    'hold_gain': float(i['totalprofitlossText']),
                    'market_value': float(i['currentValueText']),
                    'name': i['fundName'],
                    'nav': float(i['navText']),
                    'platform': '同花顺',
                    'risk': 5 - int(i['fundType'])}
                result.append(dic.copy())

            pprint(result)
            return result
    except requests.ConnectionError as e:
        print('Error', e.args)


def main():
    if len(sys.argv) < 2:
        print('Usage: {} "dj|ths"'.format(sys.argv[0]))
        sys.exit(1)

    if sys.argv[1] == 'dj':
        result = danjuan()
    elif sys.argv[1] == 'ths':
        result = tonghs()
    else:
        print('Usage: {} "dj|ths"'.format(sys.argv[0]))
        sys.exit(1)

    mongo_host = '127.0.0.1'
    mongo_port = 27017
    mongo_db_name = 'finance'
    mongo_db_collection = 'myfunds'

    client = MongoClient(host=mongo_host, port=mongo_port)
    db = client[mongo_db_name]
    collection = db[mongo_db_collection]
    collection.insert_many(result)


if __name__ == "__main__":
    main()
