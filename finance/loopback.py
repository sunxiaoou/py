#! /usr/bin/python3
from datetime import date

import matplotlib.pyplot as plt
import openpyxl
import pandas as pd
import akshare as ak    # 导入数据源
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


def hs300():
    # hs300_pe_df = ak.stock_a_pe(market="000300.XSHG").iloc[-1708:]    # 获取沪深300的PE和收盘价数据
    hs300_pe_df = ak.stock_a_pe(market="510310.XSHG").iloc[-1708:]    # 获取沪深300的PE和收盘价数据
    print(hs300_pe_df)
    hs300_pe_pct = hs300_pe_df[['middlePETTM','close']].rank(ascending=True, pct=True)*100    # 计算PE和收盘价的历史百分位
    hs300_pe_pct.plot(figsize=(16, 8), grid=True,title='沪深300估值和价格百分位')    # 画图


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


def loop_back(symbol: str, begin: date):
    commission_rate = 0.001

    df = ak.stock_zh_index_daily(symbol=symbol)
    df = df[df['date'] > begin]
    df = df[['date', 'close']]
    df['每期金额'] = 100
    df['累计金额'] = df['每期金额'].cumsum()
    df['每期数量'] = df.apply(lambda x: x['每期金额'] / x['close'] * (1 - commission_rate), axis=1)
    df['累计数量'] = df['每期数量'].cumsum()
    df['累计净值'] = df.apply(lambda x: x['close'] * x['累计数量'], axis=1)
    df['现金流'] = -100
    m = df.shape[0]     # number of row
    cumulative_amount = df.iloc[m - 1, df.columns.get_loc('累计金额')]
    cumulative_net = df.iloc[m - 1, df.columns.get_loc('累计净值')]
    hold_gain = cumulative_net - cumulative_amount
    df.iloc[m - 1, df.columns.get_loc('现金流')] += cumulative_net
    return_rate = xirr(df, 'date', '现金流')
    print(df)
    print(cumulative_amount, cumulative_net, hold_gain, return_rate)
    # to_excel('loopback.xlsx', symbol, df)


def main():
    # ttm_lyr()
    # hs300()
    # plt.show()
    loop_back('sh000300', date(2015, 6, 1))


if __name__ == "__main__":
    main()
