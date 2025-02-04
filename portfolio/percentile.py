#! /usr/bin/python3
import re
import sys
from datetime import datetime, timedelta

import pandas as pd

from snowball import Snowball


def get_data_from_snowball(code: str, begin: str) -> pd.DataFrame:
    df = Snowball().get_data(code, begin)
    df = df[['date', 'close']]
    df = df.rename({'close': code}, axis=1)
    print(df)
    return df


def get_bounds(df: pd.DataFrame) -> tuple:
    # df['date'] = pd.to_datetime(df['date'])
    code = df.columns[1]
    df[code] = pd.to_numeric(df[code])
    # 计算 5% 和 95% 分位数
    return float(df[code].quantile(0.1)), float(df[code].quantile(0.9))


def main():
    # df = pd.read_csv("tlt.csv")
    if len(sys.argv) > 2:
        if re.match(r'\d\d\d\d-\d\d-\d\d', sys.argv[2]):
            date = sys.argv[2]
        else:
            date = (datetime.today() + timedelta(days=int(sys.argv[2]))).strftime('%Y-%m-%d')
    elif len(sys.argv) == 2:
        date = '2017-06-15'
    else:
        print('Usage: %s code [yyyy-mm-dd]' % sys.argv[0])   # 'SH510310' '2021-07-01'
        print('       %s code -365' % sys.argv[0])   # 'SH510310' '2021-07-01'
        sys.exit(1)
    df = get_data_from_snowball(sys.argv[1], date)
    print(get_bounds(df))


if __name__ == "__main__":
    main()
