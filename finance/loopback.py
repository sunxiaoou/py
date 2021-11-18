#! /usr/bin/python3
import sys
from datetime import date
from datetime import datetime

import matplotlib.pyplot as plt
import openpyxl
import pandas as pd
import akshare as ak
from openpyxl import load_workbook


def to_excel(xlsx: str, sheet: str, df: pd.DataFrame):
    try:
        wb = load_workbook(xlsx)
    except FileNotFoundError:
        wb = openpyxl.Workbook()

    writer = pd.ExcelWriter(xlsx, engine='openpyxl')
    writer.book = wb
    writer.sheets = {worksheet.title: worksheet for worksheet in wb.worksheets}
    df.to_excel(writer, sheet_name=sheet, index=False)
    writer.save()


def get_index_name(code: str) -> str:
    df = ak.stock_zh_index_spot()
    print(df)
    to_excel('loopback.xlsx', 'indexes', df)
    i = df.loc[df['代码'] == code].index[0]
    return df.at[i, '名称']


def xirr(df: pd.DataFrame, date_column: str, amount_column: str) -> float:
    residual = 1
    step = 0.05
    guess = 0.05
    epsilon = 0.0001
    limit = 10000

    df = df.sort_values(by=date_column).reset_index(drop=True)
    df['years'] = df.apply(lambda x: (x[date_column] - df[date_column][0]).days / 365, axis=1)
    while abs(residual) > epsilon and limit > 0:
        limit -= 1
        residual = df.apply(lambda x: x[amount_column] / pow(guess, x['years']), axis=1).sum()
        if abs(residual) > epsilon:
            if residual > 0:
                guess += step
            else:
                guess -= step
                step /= 2.0
    return guess - 1


def loop_back(code: str, begin: date):
    names = {
        "sz161039": "1000增强LOF",
        "sz164906": "中概互联网LOF",
        "sh501009": "生物科技LOF",
        "sh501050": "50AHLOF",
        "sh501090": "消费龙头LOF",
        "sh502000": "500增强LOF",
        "sh510310": "沪深300ETF易方达",
        "sh510580": "中证500ETF易方达",
        "sh510710": "上证50ETF博时",
        "sh512000": "券商ETF",
        "sh512170": "医疗ETF",
        "sh512260": "中证500低波ETF",
        "sh512800": "银行ETF",
        "sh513050": "中国互联网ETF",
        "sh515180": "红利ETF易方达"
    }
    name = names[code]
    df = ak.stock_zh_index_daily(symbol=code)[['date', 'close']]
    df = df[df['date'] > begin]
    df['index'] = df['date']
    df = df.set_index('index')
    df['每期金额'] = 100
    df['累计金额'] = df['每期金额'].cumsum()
    fee_rate = 0.001
    df['每期数量'] = df['每期金额'] / df['close'] * (1 - fee_rate)
    df['累计数量'] = df['每期数量'].cumsum()
    df['累计净值'] = df['close'] * df['累计数量']
    df['现金流'] = -100
    m = df.shape[0]     # number of row
    cumulative_amount = df.iloc[m - 1, df.columns.get_loc('累计金额')]
    cumulative_net = df.iloc[m - 1, df.columns.get_loc('累计净值')]
    hold_gain = cumulative_net - cumulative_amount
    df.iloc[m - 1, df.columns.get_loc('现金流')] += cumulative_net
    print(df)
    return_rate = xirr(df, 'date', '现金流')
    print(cumulative_amount, cumulative_net, hold_gain, return_rate)
    # to_excel('loopback.xlsx', symbol, df)
    df[['累计金额', '累计净值']].plot(figsize=(12, 6), grid=True, title=name + '定投曲线')


def main():
    if len(sys.argv) < 3:
        print('Usage: {} code YYYYmmdd'.format(sys.argv[0]))
        sys.exit(1)

    loop_back(sys.argv[1], datetime.strptime(sys.argv[2], '%Y%m%d').date())
    # loop_back('sh510310', date(2015, 6, 1))           # 沪深300ETF易方达
    # loop_back('sh501050', date(2015, 6, 1))           # 50AHLOF
    # loop_back('sh502000', date(2015, 6, 1))           # 500增强
    plt.show()


if __name__ == "__main__":
    main()
