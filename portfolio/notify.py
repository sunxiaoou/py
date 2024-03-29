#! /usr/bin/python3
import sys
from datetime import datetime

from icloud import ICloud
from market import Market
from wxpusher import WxPusher


def get_volatile_stocks(volatility: float) -> dict:
    result = Market.get_cvtbones()
    return {x['name'][:2] + str(x['pc']): x['pc'] for x in result if x['pc'] is not None and x['pc'] >= volatility}


def main():
    if len(sys.argv) < 3:
        print('Usage: {} volatility iCloud|wxPusher'.format(sys.argv[0]))
        sys.exit(1)

    date = datetime.now().strftime('%y%m%d_%H%M%S')
    stocks = get_volatile_stocks(float(sys.argv[1]))
    if len(stocks) == 0:
        print(date)
    elif 'iCloud' == sys.argv[2]:
        keys = list(stocks.keys())
        print(date + ' - ' + str(stocks))
        ic = ICloud()
        sender = ic.login()
        ic.send(sender, sender, str(keys), str(stocks))
    elif 'wxPusher' == sys.argv[2]:
        keys = list(stocks.keys())
        print(date + ' - ' + str(stocks))
        WxPusher.push(str(keys), str(stocks))
    else:
        print('Usage: {} volatility iCloud|wxPusher'.format(sys.argv[0]))
        sys.exit(1)


if __name__ == "__main__":
    main()
