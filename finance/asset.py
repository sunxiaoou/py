#! /usr/bin/python3
import csv
import getopt
import re
import sys
from datetime import datetime
from pprint import pprint
from typing import List

import requests

from save_to import save_to_spreadsheet, save_to_mongo


def usage_exit():
    print('Usage: {} --currency="rmb||hkd|usd" '
          '--exchange_rate=float '
          '--datafile=png|csv '
          '--balance=float '
          '--spreadsheet=xlsx '
          '"zsb|hsb|yh||hs|ft" %y%m%d'.format(sys.argv[0]))
    sys.exit(1)


def get_options(platforms: list) -> dict:
    opts = args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], '',
                                   ['currency=', 'exchange_rate=', 'datafile=', 'balance=', 'spreadsheet='])
    except getopt.GetoptError as err:
        print(err)
        usage_exit()
    if len(args) < 2:
        usage_exit()

    if args[0] not in platforms:
        usage_exit()
    dic = {'platform': args[0],
           'date': args[1],
           'currency': 'rmb',
           'exchange_rate': 1,
           'datafile': '',
           'balance': '',
           'spreadsheet': ''}
    for opt, var in opts:
        if opt == '--currency' and var in ['rmb', 'hkd', 'usd']:
            dic['currency'] = var
        elif opt == '--exchange_rate':
            dic['exchange_rate'] = float(var)
        elif opt == '--datafile':
            dic['datafile'] = var
        elif opt == '--balance':
            dic['balance'] = float(var)
        elif opt == '--spreadsheet':
            if not var.endswith('.xlsx'):
                var += '.xlsx'
            dic['spreadsheet'] = var
    return dic


def my_float(s: str, a: int) -> float:
    s = re.sub(',', '', s)
    if '.' not in s:
        s = s[: a] + '.' + s[a:]
    return float(s)


def print_grid(word1: str, word2: str, grid: List[List[int]]):
    row0 = ['\\', '\'\''] + [ch for ch in word1]
    print(', '.join(row0))
    w2 = ['\'\''] + list(word2)
    for i in range(len(w2)):
        print("{},  {}".format(w2[i], ', '.join([str(j) for j in grid[i]])))


def get_distance(source: str, target: str) -> int:
    n1, n2 = len(source), len(target)
    grid = [[0] * (n1 + 1) for _ in range(n2 + 1)]
    i = j = 0
    for i in range(1, n2 + 1):
        for j in range(1, n1 + 1):
            if target[i - 1] != source[j - 1]:
                grid[i][j] = max(grid[i - 1][j], grid[i][j - 1])
            else:
                grid[i][j] = grid[i - 1][j - 1] + 1
    # print_grid(source, target, grid)
    return grid[i][j]


def get_closest_code(code: str, codes: list) -> str:
    return max(codes, key=lambda x: get_distance(code, x))


def fill_values(platform: str, currency: str, exchange_rate: float, date: datetime, result: list):
    for dic in result:
        dic['platform'] = platform
        dic['currency'] = currency
        dic['exchange_rate'] = exchange_rate
        dic['date'] = date
        if currency == 'rmb':
            dic['mv_rmb'] = dic['market_value']
            dic['hg_rmb'] = dic['hold_gain']
        else:
            dic['mv_rmb'] = round(dic['market_value'] * exchange_rate, 2)
            dic['hg_rmb'] = round(dic['hold_gain'] * exchange_rate, 2)


def verify(result: list):
    for i in result:
        if i['code'] != 'cash':
            mv = round(i['nav'] * i['volume'])
            if round(i['market_value']) != mv:
                print('market_value failed {} {}'.format(i, mv))
            hg = round((i['nav'] - i['cost']) * i['volume'])
            if round(i['hold_gain']) != hg:
                print('hold_gain failed {} {}'.format(i, hg))


def zhaoshang_bank(datafile: str, cash: float, currency: str, exchange_rate: float, date: datetime) -> list:
    result = [{'name': '现金', 'risk': 0, 'market_value': cash, 'hold_gain': 0}]
    with open(datafile) as f:
        text = f.read()
        # print(text)
    text = re.sub('[,‘]', '', text)
    amounts = re.findall(r'[-+]?\d*\.\d+', text)
    # print(amounts)
    amounts = [float(i) for i in amounts]
    result += [
        # {'name': '尊享日日盈', 'risk': 0, 'market_value': amounts[1], 'hold_gain': amounts[2]},
        # {'name': '尊享日日盈', 'risk': 0, 'market_value': amounts[3], 'hold_gain': amounts[4]},
        # {'name': '招赢日日盈', 'risk': 0, 'market_value': amounts[5], 'hold_gain': amounts[6]},
        {'name': '睿远平衡二十七期', 'risk': 1, 'market_value': amounts[1], 'hold_gain': amounts[2]},
        {'name': '卓远一年半定开8号', 'risk': 1, 'market_value': amounts[3], 'hold_gain': amounts[4]}]
    fill_values('招商银行', currency, exchange_rate, date, result)
    # verify result
    summary = round(sum([i['market_value'] for i in result[1:]]), 2)
    assert amounts[0] == summary, print("summary({}) != {}".format(summary, amounts[0]))
    return result


def hangseng_bank(datafile: str, cash: float, currency: str, exchange_rate: float, date: datetime) -> list:
    stocks = {
        '000595': ('嘉实泰和混合', 3),
        '001974': ('景顺长城量化新动力股票', 2),
        '002001': ('华夏回报混合', 3),
        '005267': ('嘉实价值精选股票', 2),
        '377240': ('上投摩根新兴动力混合', 3),
        '540003': ('汇丰晋信动态策略混合', 2)
    }
    result = [{'code': 'cash', 'name': '现金', 'risk': 0, 'market_value': cash, 'hold_gain': 0}]
    with open(datafile) as f:
        text = f.read()
        text = re.sub('[,‘]', '', text)
        nums = re.findall(r'[-+]?\d*\.?\d+', text)
        # print(nums)
        total_mv = float(nums.pop(0))
        total_hg = float(nums.pop(0))
        transit = float(nums.pop(0))
        qu, rem = divmod(len(nums), 5)
        assert(rem == 0), print('nums({}) % 5 !== 0'.format(len(nums)))
        for i in range(qu):
            code = nums[i * 5]
            dic = {
                'code': code,
                'name': stocks[code][0],
                'risk': stocks[code][1],
                'market_value': float(nums[i * 5 + 4]),
                'hold_gain': float(nums[i * 5 + 1])}
            """
            hg = round((dic['market_value'] - dic['hold_gain']) * float(nums[i * 5 + 2]) / 100)
            if hg != round(dic['hold_gain']):
               print('hold_gain failed {} {}'.format(hg, dic['hold_gain']))
            """
            result.append(dic.copy())
    fill_values('恒生银行', currency, exchange_rate, date, result)
    assert len(result) == len(stocks) + 1, print("result({}) != stocks({})".format(len(result), len(stocks) + 1))
    sum_mv = round(sum([i['market_value'] for i in result[1:]]), 2)
    assert sum_mv == total_mv, print("sum_mv({}) != total_mv({})".format(sum_mv, total_mv))
    sum_hg = round(sum([i['hold_gain'] for i in result[1:]]), 2)
    assert sum_hg == total_hg, print("sum_hg({}) != total_hg({})".format(sum_hg, total_hg))
    return result


def yinhe(datafile: str, cash: float, currency: str, exchange_rate: float, date: datetime) -> list:
    stocks = {
        '000858': ('五粮液', 3),
        '110033': ('国贸转债', 2),
        '110070': ('凌钢转债', 2),
        '113009': ('广汽转债', 2),
        '113027': ('华钰转债', 2),
        '113033': ('利群转债', 2),
        '113504': ('艾华转债', 2),
        '113525': ('台华转债', 2),
        '113536': ('三星转债', 2),
        '113541': ('荣晟转债', 2),
        '113561': ('正裕转债', 2),
        '113565': ('宏辉转债', 2),
        '113567': ('君禾转债', 2),
        '113570': ('百达转债', 2),
        '113577': ('春秋转债', 2),
        '113585': ('寿仙转债', 2),
        '113610': ('灵康转债', 2),
        '123012': ('万顺转债', 2),
        '123024': ('岱勒转债', 2),
        '123052': ('飞鹿转债', 2),
        '123062': ('三超转债', 2),
        '123080': ('海波转债', 2),
        '128013': ('洪涛转债', 2),
        '128040': ('华通转债', 2),
        '128057': ('博彦转债', 2),
        '128066': ('亚泰转债', 2),
        '128085': ('鸿达转债', 2),
        '128087': ('孚日转债', 2),
        '128094': ('星帅转债', 2),
        '128100': ('搜特转债', 2),
        '128127': ('文科转债', 2),
        '501046': ('财通福鑫', 2),
        '512170': ('医疗ETF', 3),
        '600009': ('上海机场', 3),
    }

    result = [{'code': 'cash', 'name': '现金', 'risk': 0, 'market_value': cash, 'hold_gain': 0}]
    with open(datafile) as f:
        text = f.read()
        text = re.sub('[,‘]', '', text)
        nums = re.findall(r'[-+]?\d*\.?\d+', text)
        # print(nums)
        nums.pop(0)
        total_mv = float(nums.pop(0))
        total_hg = float(nums.pop(0))
        nums.pop(0)
        nums.pop(0)
        qu, rem = divmod(len(nums), 8)
        assert(rem == 0), print('nums({}) % 8 !== 0'.format(len(nums)))
        for i in range(qu):
            code = nums[i * 8]
            dic = {
                'code': code,
                'name': stocks[code][0],
                'risk': stocks[code][1],
                'market_value': float(nums[i * 8 + 4]),
                'hold_gain': float(nums[i * 8 + 1]),
                'volume': int(nums[i * 8 + 2]),
                'nav': float(nums[i * 8 + 7]),
                'cost': float(nums[i * 8 + 3])}
            """
            hg = round((dic['market_value'] - dic['hold_gain']) * float(nums[i * 5 + 2]) / 100)
            if hg != round(dic['hold_gain']):
               print('hold_gain failed {} {}'.format(hg, dic['hold_gain']))
            """
            result.append(dic.copy())

    fill_values('银河', currency, exchange_rate, date, result)
    # assert len(result) == len(stocks) + 1, print("result({}) != stocks({})".format(len(result), len(stocks) + 1))
    sum_mv = round(sum([i['market_value'] for i in result[1:]]), 2)
    assert sum_mv == total_mv, print("sum_mv({}) != total_mv({})".format(sum_mv, total_mv))
    sum_hg = round(sum([i['hold_gain'] for i in result[1:]]), 2)
    assert sum_hg == total_hg, print("sum_hg({}) != total_hg({})".format(sum_hg, total_hg))
    verify(result)
    return result


def huasheng(datafile: str, cash: float, currency: str, exchange_rate: float, date: datetime) -> list:
    hk_stocks = {
        '00388': ('香港交易所', 3),
        '00700': ('腾讯控股', 3),
        '02015': ('理想汽车', 3),
        '03033': ('南方恒生科技', 3),
        '03690': ('美团-W', 3),
        '07200': ('FL二南方恒指', 3),
        '09988': ('阿里巴巴-SW', 3),
    }
    us_stocks = {
        'AAPL': ('苹果', 3),
        'ARKW': ('ARK Web x.0 ETF', 3),
        'BABA': ('阿里巴巴', 3),
        'BILI': ('哔哩哔哩', 3),
        'GS':  ('高盛', 3),
        'MSFT': ('微软', 3),
        'PDD': ('拼多多', 3),
    }
    stocks = hk_stocks if currency == 'hkd' else us_stocks

    dic = {
        'code': 'cash',
        'name': '现金',
        'risk': 0,
        'hold_gain': 0,
        'market_value': cash,
        'nav': 1}
    result = [dic.copy()]

    with open(datafile) as f:
        for line in f.readlines():
            # print(line)
            line = re.sub('[,‘]', '', line)
            items = re.findall('^[A-Za-z]{2,4}|[-+]?\d*\.?\d+', line)
            # print(items)
            if items and re.search(r'\w{2,4}', items[0]):
                items[0] = items[0].split()[0].upper()
                if items[0] in stocks:
                    if len(items) == 9:         # remove digits in US stock's name
                        items.pop(1)
                    dic = {
                        'code': items[0],
                        'name': stocks[items[0]][0],
                        'risk': stocks[items[0]][1],
                        'volume': int(items[1]),
                        'market_value': my_float(items[7], -2),
                        'hold_gain': my_float(items[3], -3 if currency == 'hkd' else -2),
                        'cost': my_float(items[5], -3 if currency == 'hkd' else -2),
                        'nav': my_float(items[6], -3 if currency == 'hkd' else -2)}
                    result.append(dic.copy())
    fill_values('华盛' + currency.upper(), currency, exchange_rate, date, result)
    assert len(result) == len(stocks) + 1, print("result({}) != stocks({})".format(len(result), len(stocks) + 1))
    verify(result)
    return result


def futu(csv_file: str, cash: float, currency: str, exchange_rate: float, date: datetime) -> list:
    dic = {
        'code': 'cash',
        'name': '现金',
        'risk': 0,
        'hold_gain': 0,
        'market_value': cash,
        'nav': 1}
    result = [dic.copy()]
    if csv_file:
        with open(csv_file) as f:
            reader = csv.reader(f, delimiter='\t')
            rows = list(reader)
            rows.pop(0)
            for row in rows:
                dic = {
                    'code': row[1],
                    'name': row[2],
                    'risk': 3,
                    'volume': int(row[3].split('@')[0]),
                    'market_value': my_float(row[5], -2),
                    'hold_gain': my_float(row[7], -2),
                    'cost': my_float(row[6], -4),
                    'nav': my_float(row[3].split('@')[1], -4)}
                result.append(dic.copy())

    fill_values('富途' + currency.upper(), currency, exchange_rate, date, result)
    verify(result)
    return result


def danjuan(plan='') -> list:
    risks = {
        '000730': 0,    # 现金宝
        '004069': 3,    # 南方中证全指证券联接A
        '005259': 2,    # 建信龙头企业股票
        '006228': 3,    # 中欧医疗创新股票A
        '006327': 3,    # 易方达中概互联50ETF联接人民币A
        '110011': 3,    # 易方达中小盘混合
        '501050': 2,    # 华夏上证50AH优选指数（LOF）A
        'CSI1014': 1,   # 我要稳稳的幸福
        'CSI1019': 1    # 钉钉宝365天组合
    }

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
                        # 'risk': 2 if plan_code == 'CSI666' else 3
                        'risk': 2
                    }
                    if dic['market_value']:
                        result.append(dic.copy())
            # if not plan:
            #    pprint(result)
            return result
    except requests.ConnectionError as e:
        print('Error', e.args)


def danjuan_wrap(file: str, cash: float, currency: str, exchange_rate: float, date: datetime) -> list:
    return danjuan()


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

            # pprint(result)
            return result
    except requests.ConnectionError as e:
        print('Error', e.args)


def tonghs_wrap(file: str, cash: float, currency: str, exchange_rate: float, date: datetime) -> list:
    return tonghs()


def main():
    platforms = {'zsb': zhaoshang_bank,
                 'hsb': hangseng_bank,
                 'yh': yinhe,
                 'hs': huasheng,
                 'ft': futu,
                 'dj': danjuan_wrap,
                 'ths': tonghs_wrap}

    options = get_options(list(platforms.keys()))
    result = platforms[options['platform']](options['datafile'],
                                            options['balance'],
                                            options['currency'],
                                            options['exchange_rate'],
                                            datetime.strptime(options['date'], '%y%m%d'))
    # pprint(result)
    print('{}: {} record(s)'.format(options['platform'], len(result)))

    if options['spreadsheet']:
        save_to_spreadsheet(options['spreadsheet'], options['date'], result)
    # save_to_mongo('mystocks', result)


if __name__ == "__main__":
    main()
