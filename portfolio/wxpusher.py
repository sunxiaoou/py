#! /usr/bin/python3
import sys
from datetime import datetime

import requests

from market import Market

URL = 'https://wxpusher.zjiecode.com/api/send/message'


def get_volatile_stocks(volatility: float) -> dict:
    result = Market.get_cvtbones()
    return {x['name']: x['pc'] for x in result if x['pc'] >= volatility}


def post_pusher(summary: str, content: str):
    with open('auth/wxpusher.txt', 'r') as file:
        token = file.readline().strip()
        uid = file.readline().strip()

    data = {
        'appToken': token,
        'contentType': 1,
        # 'topicIds': [123],
        'uids': [uid],
        'verifyPay': False,
        'summary': summary,
        'content': content
    }
    response = requests.post(url=URL, json=data)
    # print(response.text)


def main():
    if len(sys.argv) < 2:
        print('Usage: {} volatility'.format(sys.argv[0]))
        sys.exit(1)

    stocks = get_volatile_stocks(float(sys.argv[1]))
    date = datetime.now().strftime('%y%m%d_%H%M%S')
    if len(stocks) == 0:
        print(date)
    else:
        keys = list(stocks.keys())
        print(date + ' - ' + str(stocks))
        # post_pusher(str(keys), str(stocks))


if __name__ == "__main__":
    main()
