#! /usr/bin/python3
import sys
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd

from mysql import MySql
from xueqiu import Xueqiu


class Plot:
    def __init__(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

    @staticmethod
    def draw_single(title: str, df: pd.DataFrame):
        df = df.dropna().set_index(df.columns[0])
        df.index.name = None
        plt.figure(figsize=(10, 6))
        plt.title(title)
        plt.grid()
        plt.figtext(0.82, 0.12, ' - 同光和尘')
        plt.plot(df.index, df.iloc[:, 0], label=df.columns[0])
        plt.legend()

    @staticmethod
    def draw_bilateral(title: str, df: pd.DataFrame):
        df = df.dropna().set_index(df.columns[0])
        df.index.name = None
        fig, ax1 = plt.subplots(figsize=(10, 6))
        plt.title(title)
        plt.grid()
        plt.figtext(0.82, 0.12, ' - 同光和尘')
        ax2 = ax1.twinx()
        ax1.plot(df.index, df.iloc[:, 0], 'g-', label=df.columns[0])
        ax1.legend(loc='upper left')
        ax2.plot(df.index, df.iloc[:, 1], 'b-', label=df.columns[1])
        ax2.legend(loc='upper right')

    @staticmethod
    def save(file: str):
        plt.savefig(file, dpi=400, bbox_inches='tight')

    @staticmethod
    def show():
        plt.show()


def plot_code(code: str, begin: str = ''):
    db = MySql()
    df = db.to_frame('etf_daily', ['date', 'name', 'close'], "code = '%s' and date >= '%s'" %
                     (code, begin))
    if df.empty:
        df = Xueqiu().get_data(code, begin)
        df = df[['date', 'name', 'close']]
    df = df.rename({'close': code}, axis=1)
    print(df)
    title = df['name'].iloc[-1]
    Plot.draw_single(title, df[['date', code]])
    # Plot.save('%s2.png' % code)
    Plot.show()


def date_to_cell(date: datetime) -> datetime:
    if date.hour or date.minute or date.second or date.microsecond:
        date = date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return date


def plot_code_valuation(code: str, begin: str = ''):
    title = ''
    db = MySql()
    if code == 'sh000985':
        df = db.to_frame('valuation', ['date', 'sh000985', 'star'], "date >= '%s'" % begin)
        title = '近年SH000985(中证全指)与螺丝钉星级走势对比'
    elif code == 'TLT':
        df = db.to_frame('etf_daily', ['date', 'name', 'close'], "code = '%s' and date >= '%s'"
                         % (code, begin))
        title = '近年%s(%s)与十年期国债利率走势对比' % (code, df['name'].iloc[-1])
        df.drop(columns=['name'], inplace=True)
        df['date'] = df['date'].apply(date_to_cell)
        df2 = db.to_frame('valuation', ['date', 'USBONE'], "date >= '%s'" % begin)
        df = df.merge(df2, on='date', how='inner')
        df = df.rename({'close': code, 'USBONE': '十年期国债利率%'}, axis=1)
    elif code == 'KWEB':    # or '03033'
        df = db.to_frame('etf_daily', ['date', 'name', 'close'], "code = '%s' and date >= '%s'"
                         % (code, begin))
        val_code = 'H30533'
        dic = db.last_row('threshold', 'name', "code = '%s'" % val_code)
        reference = dic['name'] + dic['reference']
        title = '近年%s(%s)与%s走势对比' % (code, df['name'].iloc[-1], reference)
        df.drop(columns=['name'], inplace=True)
        df['date'] = df['date'].apply(date_to_cell)
        df2 = db.to_frame('valuation', ['date', val_code], "date >= '%s'" % begin)
        df = df.merge(df2, on='date', how='inner')
        df = df.rename({'close': code, val_code: reference + '%'}, axis=1)
    else:
        df = db.to_frame('etf_daily', ['date', 'name', 'close'], "code = '%s' and date >= '%s'"
                         % (code, begin))
        dic = db.last_row('threshold', 'code', "onsite = '%s'" % code)
        val_code = dic['code']
        reference = dic['name'] + dic['reference']
        title = '近年%s(%s)与%s走势对比' % (code, df['name'].iloc[-1], reference)
        df.drop(columns=['name'], inplace=True)
        df2 = db.to_frame('valuation', ['date', val_code], "date >= '%s'" % begin)
        df = df.merge(df2, on='date', how='inner')
        df = df.rename({'close': code, val_code: reference + '%'}, axis=1)
    print(df)
    Plot.draw_bilateral(title, df)
    Plot.save('%s.png' % title)
    Plot.show()


def main():
    date = '2017-06-15'
    if len(sys.argv) > 2:
        date = sys.argv[2]
    elif len(sys.argv) < 2:
        print('Usage: %s code [yyyy-mm-dd]' % sys.argv[0])   # 'SH510310' '2021-07-01'
        sys.exit(1)

    # plot_code(sys.argv[1], date)
    plot_code_valuation(sys.argv[1], date)


if __name__ == "__main__":
    main()
