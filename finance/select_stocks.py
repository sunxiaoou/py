#! /usr/bin/python3
import sys
import random


def get_stocks(quantity: int):
    list1 = ['AAPL', 'ADBE', 'AMZN', 'GOOGL', 'GS', 'KO', 'MSFT', 'NFLX', 'NVDA']
    # list2 = ['IEF', 'QQQ', 'SPY']
    # list2 = ['GS', 'KO', 'MSFT', 'SPY']
    list2 = ['00388', '03033', '07200']
    # print(sorted(the_list))
    print(random.sample(list1, quantity))
    print(random.choice(list2))


def main():
    n = len(sys.argv)
    if n < 2:
        print('Usage {} quantity'.format(sys.argv[0]))
        sys.exit(1)
    # sys.stdout.flush()
    get_stocks(int(sys.argv[1]))


if __name__ == "__main__":
    main()
