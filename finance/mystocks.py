#! /usr/bin/python3
import csv
import getopt
import re
import sys
from datetime import datetime
from pprint import pprint
from typing import List

import tesserocr
from PIL import Image

from save_to import save_to_spreadsheet, save_to_mongo


def usage_exit():
    print('Usage: {} --currency="rmb||hkd|usd" --exchange_rate=float --date=%y%m%d '
          '"zsb|yh||hs|ft" png|csv balance'.format(sys.argv[0]))
    sys.exit(1)


def get_options(platforms: list) -> dict:
    opts = args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['currency=', 'exchange_rate=', 'date='])
    except getopt.GetoptError as err:
        print(err)
        usage_exit()
    if len(args) < 3:
        usage_exit()

    if args[0] not in platforms:
        usage_exit()
    dic = {'platform': args[0],
           'datafile': args[1],
           'cash': float(args[2]),
           'currency': 'rmb',
           'exchange_rate': 1,
           'date': datetime.now().strftime('%y%m%d')}
    for opt, var in opts:
        if opt == '--currency' and var in ['rmb', 'hkd', 'usd']:
            dic['currency'] = var
        elif opt == '--exchange_rate':
            dic['exchange_rate'] = float(var)
        elif opt == '--date':
            dic['date'] = var
    return dic


def recognize_image(image_name: str) -> str:
    image = Image.open(image_name)
    """
    image = image.convert('L')
    new_size = tuple(2 * x for x in image.size)             # enlarge the image size
    image = image.resize(new_size, Image.ANTIALIAS)
    """
    # image.show()
    return tesserocr.image_to_text(image, lang='eng+chi_sim', psm=tesserocr.PSM.SINGLE_BLOCK)


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
            if i['nav'] * i['volume'] != i['market_value']:
                print('market_value failed {} {}'.format(i, i['nav'] * i['volume']))
            if round((i['nav'] - i['cost']) * i['volume']) != round(i['hold_gain']):
                print('hold_gain failed {} {}'.format(i, (i['nav'] - i['cost']) * i['volume']))


def zhaoshang_bank(image_file: str, cash: float, currency: str, exchange_rate: float, date: datetime) -> list:
    result = [{'name': '现金', 'risk': 0, 'market_value': cash, 'hold_gain': 0}]
    text = recognize_image(image_file)
    text = re.sub('[,‘]', '', text)
    amounts = re.findall(r'[-+]?\d*\.\d+', text)
    # print(amounts)
    amounts = [float(i) for i in amounts]
    result += [
        {'name': '招赢尊享日日盈', 'risk': 0, 'market_value': amounts[1], 'hold_gain': amounts[2]},
        {'name': '招赢尊享日日盈', 'risk': 0, 'market_value': amounts[3], 'hold_gain': amounts[4]},
        {'name': '睿远平衡二十七期', 'risk': 1, 'market_value': amounts[5], 'hold_gain': amounts[6]},
        {'name': '卓远一年半定开8号', 'risk': 1, 'market_value': amounts[7], 'hold_gain': amounts[8]}]
    fill_values('招商银行', currency, exchange_rate, date, result)
    # verify result
    summary = sum([i['market_value'] for i in result[1:]])
    assert amounts[0] == summary, print("summary({}) != {}".format(summary, amounts[0]))
    return result


def yinhe(image_file: str, cash: float, currency: str, exchange_rate: float, date: datetime) -> list:
    stocks = {
        '000858': ('五粮液', 3),
        '501046': ('财通福鑫', 3),
        '512170': ('医疗ETF', 2),
        '515170': ('食品饮料', 2),
        '600009': ('上海机场', 3),
        '600036': ('招商银行', 3),
        '600309': ('万华化学', 3)
    }

    dic = {
        'code': 'cash',
        'name': '现金',
        'risk': 0,
        'market_value': cash,
        'hold_gain': 0,
        'nav': 1}
    result = [dic.copy()]

    text = recognize_image(image_file)
    # print(text)
    for line in text.split('\n'):
        if line:
            line = re.sub('[,‘]', '', line)
            items = re.findall('[-+]?\d*\.?\d+', line)
            # print(items)
            if len(items) == 8:
                if items[0] not in stocks:
                    items[0] = get_closest_code(items[0], list(stocks.keys()))
                dic = {
                    'code': items[0],
                    'name': stocks[items[0]][0],
                    'risk': stocks[items[0]][1],
                    'volume': int(items[1]),
                    'market_value': my_float(items[5], -2),
                    'hold_gain': my_float(items[2], -2),
                    'nav': my_float(items[6], -3),
                    'cost': my_float(items[7], -3)}
                result.append(dic.copy())
    fill_values('银河', currency, exchange_rate, date, result)
    assert len(result) == len(stocks) + 1, print("result({}) != stocks({})".format(len(result), len(stocks) + 1))
    verify(result)
    return result


def huasheng(image_file: str, cash: float, currency: str, exchange_rate: float, date: datetime) -> list:
    hk_stocks = {
        '00388': ('香港交易所', 3),
        '00700': ('腾讯控股', 3),
        '02840': ('SPDR金ETF', 2),
        '03033': ('南方恒生科技', 2),
        '03690': ('美团-W', 3),
        '07200': ('FL二南方恒指', 2),
        '09988': ('阿里巴巴-SW', 3),
    }
    us_stocks = {
        'AAPL': ('苹果', 3),
        'AMZN': ('亚马逊', 3),
        'ARKG': ('ARK Genomic ETF', 3),
        'ARKK': ('ARK Innovation ETF', 3),
        'ARKW': ('ARK Web x.0 ETF', 3),
        'BABA': ('阿里巴巴', 3),
        'BILI': ('哔哩哔哩', 3),
        'GS':  ('高盛', 3),
        'MSFT': ('微软', 3),
        'PDD': ('拼多多', 3),
        'SPY': ('标普500指数ETF', 2)
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

    text = recognize_image(image_file)
    # print(text)
    for line in text.split('\n'):
        if line:
            line = re.sub('[,‘]', '', line)
            items = re.findall('^[A-Za-z]{2,4}|[-+]?\d*\.?\d+', line)
            # print(items)
            if re.search(r'\w{2,4}', items[0]):
                items[0] = items[0].split()[0].upper()
                if items[0] in stocks:
                    if len(items) == 9:         # remove digits in US stock's name
                        items.pop(1)
                    dic = {
                        'code': items[0],
                        'name': stocks[items[0]][0],
                        'risk': stocks[items[0]][1],
                        'volume': int(items[1]),
                        'market_value': float(items[7]),
                        'hold_gain': float(items[3]),
                        'cost': float(items[5]),
                        'nav': float(items[6])}
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
    try:
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
    except FileNotFoundError as e:
        print(e)

    fill_values('富途' + currency.upper(), currency, exchange_rate, date, result)
    verify(result)
    return result


def main():
    platforms = {'zsb': zhaoshang_bank, 'yh': yinhe, 'hs': huasheng, 'ft': futu}
    options = get_options(list(platforms.keys()))

    result = platforms[options['platform']](options['datafile'],
                                            options['cash'],
                                            options['currency'],
                                            options['exchange_rate'],
                                            datetime.strptime(options['date'], '%y%m%d'))
    # verify(result)
    # pprint(result)
    print(len(result))

    # save_to_spreadsheet('finance.xlsx', options['date'], result)
    # save_to_mongo('mystocks', result)


if __name__ == "__main__":
    main()
