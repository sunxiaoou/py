#! /usr/bin/python3
import sys
from datetime import datetime

from icloud import ICloud
from market import Market
from wxpusher import WxPusher


def get_volatile_stocks(volatility: float) -> list:
    result = Market.get_cvtbonds()
    return ["{} {} {}%".format(x['name'][:2], x['price'], str(x['pct']))
            for x in result if x['pct'] is not None and x['pct'] >= volatility]


def main():
    if len(sys.argv) < 3:
        print('Usage: {} volatility iCloud|wxPusher'.format(sys.argv[0]))
        sys.exit(1)

    date = datetime.now().strftime('%y%m%d_%H%M%S')
    stocks = get_volatile_stocks(float(sys.argv[1]))
    if len(stocks) == 0:
        print(date)
    elif 'iCloud' == sys.argv[2]:
        print(date + ' - ' + str(stocks))
        ic = ICloud()
        sender = ic.login()
        ic.send(sender, sender, str(stocks), str(stocks))
    elif 'wxPusher' == sys.argv[2]:
        print(date + ' - ' + str(stocks))
        WxPusher.push(str(stocks), str(stocks))
    else:
        print('Usage: {} volatility iCloud|wxPusher'.format(sys.argv[0]))
        sys.exit(1)


if __name__ == "__main__":
    main()
