#! /usr/bin/python3

import tushare as ts


def close_prices(date: str) -> list:
    codes = ['600009.SH', '600104.SH', '600036.SH', '600276.SH', '600309.SH', '600519.SH',
             '600585.SH', '600660.SH', '600887.SH', '600900.SH', '601318.SH', '601901.SH',
             '603288.SH', '603886.SH',
             '000002.SZ', '000333.SZ', '000651.SZ', '000858.SZ', '000895.SZ', '002271.SZ',
             '002304.SZ', '002372.SZ', '002415.SZ', '002508.SZ', '002677.SZ']

    pro = ts.pro_api('c88f69544442a2b334556f33c12c502c3a9aa28c60cf8ecbcb1c3e56')
    prices = []
    for c in codes:
        df = pro.daily(ts_code=c, start_date=date, end_date=date)
        prices.append(float(df['close']))
    return prices


def main():
    prices = close_prices('20210305')
    for p in prices:
        print(p)


if __name__ == "__main__":
    main()
