#! /usr/bin/python3
import math
import re
import sys
from datetime import datetime, timedelta

import pandas as pd

from grid import Grid
from snowball import Snowball


def get_data_from_snowball(code: str, begin: str) -> pd.DataFrame:
    df = Snowball().get_data(code, begin)
    df = df[['date', 'close']]
    df = df.rename({'close': code}, axis=1)
    print(df)
    return df


def get_grid(percent: float, df: pd.DataFrame) -> Grid:
    # df['date'] = pd.to_datetime(df['date'])
    code = df.columns[1]
    df[code] = pd.to_numeric(df[code])
    # 计算 5% 和 95% 分位数
    low = round(float(df[code].quantile(0.1)), 2)
    high = round(float(df[code].quantile(0.9)), 2)
    num = int(round(math.log(high / low, 1 + percent)))
    return Grid(low, high, num, True)


def main():
    # df = pd.read_csv("tlt.csv")
    if len(sys.argv) > 3:
        if re.match(r'\d\d\d\d-\d\d-\d\d', sys.argv[3]):
            date = sys.argv[3]
        else:
            date = (datetime.today() + timedelta(days=int(sys.argv[3]))).strftime('%Y-%m-%d')
    elif len(sys.argv) == 3:
        date = '2017-06-15'
    else:
        print('Usage: %s code estimate_step [yyyy-mm-dd]' % sys.argv[0])   # 'SH510310' '2021-07-01'
        print('       %s code estimate_step -365' % sys.argv[0])   # 'SH510310' '2021-07-01'
        sys.exit(1)
    df = get_data_from_snowball(sys.argv[1], date)
    print(get_grid(float(sys.argv[2]), df))


if __name__ == "__main__":
    main()
