#! /usr/local/bin/python3
import csv
import sys
from collections import namedtuple
from pprint import pprint

Stock = namedtuple('Stock', 'code name price change roe cash_rate profit_rate')


def row2stock(row):
    return Stock(row[0], row[1], row[2], row[3],
                 (row[4], row[5], row[6], row[7], row[8]),
                 (row[9], row[10], row[11], row[12], row[13]),
                 (row[14], row[15], row[16], row[17], row[18]))


def check_stock(stock):
    # For 5 consecutive years of ROE,
    # the average or the value of the most recent year is less than 20%
    average = sum(float(roe) for roe in stock.roe) / len(stock.roe)
    if average < 20 or float(stock.roe[0]) < 20:
        return False

    # For five consecutive years, the average net profit cash content is less than 100%
    average = sum(float(cash_rate) for cash_rate in stock.cash_rate) / len(stock.cash_rate)
    if average < 100:
        return False

    # For the 5 consecutive years of the gross profit margin,
    # the average or the value in the most recent year is less than 40%
    average = sum(float(profit_rate) for profit_rate in stock.profit_rate) / len(stock.profit_rate)
    if average < 40 or float(stock.profit_rate[0]) < 40:
        return False
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: {} file.csv".format(sys.argv[0]))
        sys.exit(1)
    
    with open(sys.argv[1]) as fp:
        reader = csv.reader(fp)
        stocks = [row2stock(row) for row in reader]

    # pprint(stocks[0])
    result = [stocks[i] for i in range(1, len(stocks)) if check_stock(stocks[i])]
    print(len(result))
    for stock in result:
        print(stock.code, stock.name)
        # print(stock.name, stock.roe, stock.cash_rate, stock.profit_rate)


if __name__ == "__main__":
    main()
