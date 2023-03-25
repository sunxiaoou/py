#! /usr/bin/python3
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
from requests import request

# pd.set_option('display.max_columns', 6)
# pd.set_option('display.max_rows', 4000)

from mysql import MySql
from xueqiu import Xueqiu


class Plot:
    def __init__(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

    @staticmethod
    def draw_single(df: pd.DataFrame):
        df = df.dropna().set_index(df.columns[0])
        df.index.name = None
        plt.figure(figsize=(10, 6))
        plt.grid()
        plt.plot(df.index, df.iloc[:, 0])

    @staticmethod
    def draw_bilateral(title: str, df: pd.DataFrame):
        df = df.dropna().set_index(df.columns[0])
        df.index.name = None
        fig, ax1 = plt.subplots(figsize=(10, 6))
        plt.title(title)
        plt.grid()
        ax2 = ax1.twinx()
        ax1.plot(df.index, df.iloc[:, 0], 'g-', label=df.columns[0])
        ax1.legend(loc='upper left')
        ax2.plot(df.index, df.iloc[:, 1], 'b-', label=df.columns[1])
        ax2.legend()

    @staticmethod
    def save(file: str):
        plt.savefig(file, dpi=400, bbox_inches='tight')

    @staticmethod
    def show():
        plt.show()


def plot_code(code: str, begin: str = ''):
    df = pd.DataFrame()
    # df = MySql().to_frame('etf_daily', ['date, close'], "code = '%s' and date >= '%s'" % (code, begin))
    if df.empty:
        df = Xueqiu().get_data(code, begin)
        df = df[['date', 'close']]
    df = df.rename({'close': code}, axis=1)
    print(df)
    # Plot.draw_single(df)
    # # Plot.save('%s2.png' % code)
    # Plot.show()


def date_to_cell(date: datetime) -> datetime:
    if date.hour or date.minute or date.second or date.microsecond:
        date = date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return date


def plot_code_valuation(code: str, begin: str = ''):
    title = ''
    db = MySql()
    if code == 'sh000985':
        df = db.to_frame('valuation', ['date', 'sh000985', 'star'], "date >= '%s'" % begin)
    elif code == 'TLT':
        title = '近年TLT与美国十年期国债利率走势'
        df = db.to_frame('etf_daily', ['date, close'], "code = '%s' and date >= '%s'" % ('TLT', begin))
        df['date'] = df['date'].apply(date_to_cell)
        df2 = db.to_frame('valuation', ['date', 'USBONE'], "date >= '%s'" % begin)
        df = df.merge(df2, on='date', how='inner')
        df = df.rename({'close': code, 'USBONE': '十年期国债利率%'}, axis=1)
    else:
        df = pd.DataFrame()
    print(df)
    Plot.draw_bilateral(title, df)
    Plot.save('%s.png' % title)
    Plot.show()


def main():
    # plot_code('TLT', '2017-06-15')
    # plot_code('SH510310', '2017-06-15')
    plot_code_valuation('TLT', '2017-06-15')


if __name__ == "__main__":
    main()
