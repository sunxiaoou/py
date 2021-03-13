#! /usr/bin/python3
# $ cp ~/Desktop/"`ls -lrt ~/Desktop/*.png | tail -1 | awk -F/ '{print $NF}'`" us.png
# $ tesseract us.png us -l eng+chi_sim; cat us.txt

import re
import sys
from datetime import datetime
from pprint import pprint

import tesserocr
from PIL import Image
from pymongo import MongoClient


def yinhe(img: str) -> list:
    text = tesserocr.file_to_text(img, lang='chi_sim')
    lines = text.split('\n')
    result = []
    for i in range(len(lines)):
        if lines[i]:
            items = re.findall('^\D+|[-+]?\d+[.]?\d+', lines[i])
            if items[0].startswith('资金可用'):
                dic = {
                    'code': '000000',
                    'date': datetime.now(),
                    'name': '现金',
                    'nav': 1,
                    'hold_gain': 0,
                    'market_value': items[1],
                    'platform': '银河',
                    'risk': 0}
                result.append(dic.copy())
            elif len(items) == 5:
                lines[i + 1] = re.sub(':', '.', lines[i + 1])
                items.extend(re.findall('[-+]?\d+[.]?\d+', lines[i + 1]))
                dic = {
                    'code': items[1],
                    'date': datetime.now(),
                    'name': items[0].strip(),
                    'nav': float(items[8]),
                    'hold_gain': float(items[2]),
                    'market_value': float(items[5]),
                    'platform': '银河',
                    'risk': 2 if items[1][0] == '5' else 3}
                # print(items)
                result.append(dic.copy())
            else:
                pass
    return result


def huasheng(img: str, currency='hkd') -> list:
    hks = {
        '00388': ('香港交易所', 3),
        '00700': ('腾讯控股', 3),
        '02840': ('SPDR金ETF', 2),
        '03033': ('南方恒生科技', 2),
        '03690': ('美团-W', 3),
        '07200': ('FL二南方恒指', 2),
        '09988': ('阿里巴巴-SW', 3)
    }

    text = tesserocr.file_to_text(img, lang='eng+chi_sim')
    lines = text.split('\n')
    result = []
    for i in range(len(lines)):
        if lines[i].strip():
            lines[i] = re.sub('[,‘]', '', lines[i])
            items = re.findall('^\D+|[-+]?\d+\.?\d+', lines[i])
            print(items)

            if '现金' in items[0]:
                dic = {
                    'code': '00000',
                    'currency': currency,
                    'date': datetime.now(),
                    'hold_gain': 0,
                    'market_value': float(items[1]),
                    'name': '现金',
                    'nav': 1,
                    'platform': '华盛',
                    'risk': 0}
                result.append(dic.copy())
            elif re.search(r'\d{5}$', items[0]):
                dic = {
                    'code': items[0],
                    'currency': currency,
                    'date': datetime.now(),
                    'hold_gain': float(items[3]),
                    'market_value': float(items[7]),
                    'name': hks[items[0]][0],
                    'nav': float(items[6]),
                    'platform': '华盛',
                    'risk': hks[items[0]][1]}
                result.append(dic.copy())
    # pprint(result)
    return result


def my_float(s: str, a: int) -> float:
    if '.' not in s:
        s = s[: a] + '.' + s[a:]
    return float(s)


def huasheng2(pic: str, currency='hkd') -> list:
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
        'SPY': ('标普500指数ETF', 2)}

    image = Image.open(pic)
    image = image.convert('L')
    new_size = tuple(2 * x for x in image.size)             # enlarge the image size
    image = image.resize(new_size, Image.ANTIALIAS)
    text = tesserocr.image_to_text(image, lang='eng+chi_sim', psm=tesserocr.PSM.SINGLE_BLOCK)
    # print(text)

    lines = text.split('\n')
    result = []
    for line in lines:
        if line:
            line = re.sub('[,‘]', '', line)
            items = re.findall('^[A-Za-z]{2,4}|[-+]?\d*\.?\d+', line)
            # print(i, items)
            if items:
                if '现金' in line:
                    dic = {
                        'code': 'cash',
                        'currency': currency,
                        'date': datetime.now(),
                        'hold_gain': 0,
                        'market_value': float(items[0]),
                        'name': '现金',
                        'nav': 1,
                        'platform': '华盛',
                        'risk': 0}
                    result.append(dic.copy())
                elif re.search(r'\w{2,4}', items[0]):
                    items[0] = items[0].split()[0].upper()
                    if items[0] in us_stocks:
                        if len(items) == 9:         # remove digits in name
                           items.pop(1)
                        dic = {
                            'code': items[0],
                            'currency': currency,
                            'date': datetime.now(),
                            'hold_gain': my_float(items[3], -2),
                            'market_value': my_float(items[7], -2),
                            'name': us_stocks[items[0]][0],
                            'nav': my_float(items[6], -2),
                            'platform': '华盛',
                            'risk': us_stocks[items[0]][1]}
                        result.append(dic.copy())
    return result


def main():
    switch = {'yh': yinhe, 'hs': huasheng2}
    if len(sys.argv) < 3:
        print('Usage: {} "yh||hs|ft" img [rmb|hkd|usd]'.format(sys.argv[0]))
        sys.exit(1)

    if sys.argv[3]:
        result = switch[sys.argv[1]](sys.argv[2], currency=sys.argv[3])
    else:
        result = switch[sys.argv[1]](sys.argv[2])

    pprint(result)
    exit(1)

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
