#! /usr/bin/python3
# cp -p ~/Desktop/"`ls -lrt ~/Desktop/*.png | tail -1 | awk -F/ '{print $NF}'`" $name.png
# tesseract $name.png $name -l eng+chi_sim --psm 6; cat $name.txt
# mystocks.py --date=210312 yh yh_2323.88.png 2323.88
# mystocks.py --currency=hkd --exchange_rate=0.8384 --date=210312 hs hs_83088.38.png 83088.38
# mystocks.py --currency=usd --exchange_rate=6.5081 --date=210312 hs hs_17379.64.png 17379.64

import getopt
import re
import sys
from datetime import datetime
from pprint import pprint

import tesserocr
from PIL import Image
from pymongo import MongoClient


Stocks = {
    # A stocks
    '000858': ('五粮液', 3),
    '501046': ('财通福鑫', 3),
    '512170': ('医疗ETF', 2),
    '515170': ('食品饮料', 2),
    '600009': ('上海机场', 3),
    '600036': ('招商银行', 3),
    '600309': ('万华化学', 3),
    # HK stocks
    '00388': ('香港交易所', 3),
    '00700': ('腾讯控股', 3),
    '02840': ('SPDR金ETF', 2),
    '03033': ('南方恒生科技', 2),
    '03690': ('美团-W', 3),
    '07200': ('FL二南方恒指', 2),
    '09988': ('阿里巴巴-SW', 3),
    # US stocks
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


def usage_exit():
    print('Usage: {} --currency="rmb||hkd|usd" --exchange_rate=float --date=yyMMDD '
          '"yh||hs|ft" img cash'.format(sys.argv[0]))
    sys.exit(1)


def get_options() -> dict:
    opts = args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['currency=', 'exchange_rate=', 'date='])
    except getopt.GetoptError as err:
        print(err)
        usage_exit()
    if len(args) < 3:
        usage_exit()

    if args[0] not in ['yh', 'hs', 'ft']:
        usage_exit()
    dic = {'platform': args[0], 'image': args[1], 'cash': float(args[2]), 'currency': 'rmb', 'exchange_rate': 1,
           'date': datetime.now()}
    for opt, var in opts:
        if opt == '--currency' and var in ['rmb', 'hkd', 'usd']:
            dic['currency'] = var
        elif opt == '--exchange_rate':
            dic['exchange_rate'] = float(var)
        elif opt == '--date':
            dic['date'] = datetime.strptime(var, '%y%m%d')
    return dic


def recognize_image(image_name: str) -> str:
    image = Image.open(image_name)
    image = image.convert('L')
    new_size = tuple(2 * x for x in image.size)             # enlarge the image size
    image = image.resize(new_size, Image.ANTIALIAS)
    return tesserocr.image_to_text(image, lang='eng+chi_sim', psm=tesserocr.PSM.SINGLE_BLOCK)


def yinhe(text: str, cash: float, currency: str, exchange_rate: float, date: datetime) -> list:
    # print(text)
    dic = {
        'code': 'cash',
        'currency': currency,
        'date': date,
        'exchange_rate': exchange_rate,
        'hold_gain': 0,
        'market_value': cash,
        'name': '现金',
        'nav': 1,
        'platform': '银河',
        'risk': 0,
        'rmb_value': round(cash * exchange_rate, 2)}
    result = [dic.copy()]
    for line in text.split('\n'):
        if line:
            line = re.sub('[,‘]', '', line)
            items = re.findall('[-+]?\d*\.?\d+', line)
            if len(items) == 8:
                if items[0] in Stocks:
                    dic = {
                        'code': items[0],
                        'currency': currency,
                        'date': date,
                        'exchange_rate': exchange_rate,
                        'hold_gain': float(items[2]),
                        'market_value': float(items[5]),
                        'name': Stocks[items[0]][0],
                        'nav': float(items[6]),
                        'platform': '银河',
                        'risk': Stocks[items[0]][1],
                        'rmb_value': round(float(items[5]) * exchange_rate, 2)}
                    result.append(dic.copy())
    return result


def huasheng(text: str, cash: float, currency: str, exchange_rate: float, date: datetime) -> list:
    dic = {
        'code': 'cash',
        'currency': currency,
        'date': date,
        'exchange_rate': exchange_rate,
        'hold_gain': 0,
        'market_value': cash,
        'name': '现金',
        'nav': 1,
        'platform': '华盛',
        'risk': 0,
        'rmb_value': round(cash * exchange_rate, 2)}
    result = [dic.copy()]
    for line in text.split('\n'):
        if line:
            line = re.sub('[,‘]', '', line)
            items = re.findall('^[A-Za-z]{2,4}|[-+]?\d*\.?\d+', line)
            # print(items)
            if re.search(r'\w{2,4}', items[0]):
                items[0] = items[0].split()[0].upper()
                if items[0] in Stocks:
                    if len(items) == 9:         # remove digits in US stock's name
                        items.pop(1)
                    dic = {
                        'code': items[0],
                        'currency': currency,
                        'date': date,
                        'exchange_rate': exchange_rate,
                        'hold_gain': float(items[3]),
                        'market_value': float(items[7]),
                        'name': Stocks[items[0]][0],
                        'nav': float(items[6]),
                        'platform': '华盛',
                        'risk': Stocks[items[0]][1],
                        'rmb_value': round(float(items[7]) * exchange_rate, 2)}
                    result.append(dic.copy())
    return result


def main():
    platforms = {'yh': yinhe, 'hs': huasheng}
    options = get_options()
    text = recognize_image(options['image'])
    result = platforms[options['platform']](text, options['cash'], options['currency'], options['exchange_rate'],
                                            options['date'])
    pprint(result)
    exit(1)

    mongo_host = '127.0.0.1'
    mongo_port = 27017
    mongo_db_name = 'finance'
    mongo_db_collection = 'mystocks'

    client = MongoClient(host=mongo_host, port=mongo_port)
    db = client[mongo_db_name]
    collection = db[mongo_db_collection]
    collection.insert_many(result)


if __name__ == "__main__":
    main()
