#! /usr/bin/python3
import re
import sys
from datetime import date
from datetime import datetime

import matplotlib.pyplot as plt
import numpy
import openpyxl
import pandas as pd
import akshare as ak
from openpyxl import load_workbook

# pd.set_option('display.max_rows', 100)
# pd.set_option('display.max_columns', 6)

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
    "sh515180": "红利ETF易方达",

    "004868": "交银股息优化",
    "000595": "嘉实泰和",
    "001766": "上投摩根医疗健康",
    "001810": "中欧潜力价值",
    "001974": "景顺长城量化新动力",
    "003095": "中欧医疗健康A",
    "005259": "建信龙头企业",
    "005267": "嘉实价值精选",
    "005354": "富国沪港深行业精选A",
    "006228": "中欧医疗创新A",
    "110011": "易方达优质精选",
    "161005": "富国天惠成长",
    "163402": "兴全趋势投资",
    "163406": "兴全合润",
    "163415": "兴全商业模式优选",
    "166002": "中欧新蓝筹A",
    "169101": "东方红睿丰",
    "377240": "上投摩根新兴动力",
    "519035": "富国天博创新",
    "519688": "交银精选",
    "540003": "汇丰晋信动态策略A",

    "000248": "汇添富中证消费ETF联接",
    "001556": "天弘中证500A",
    "001594": "天弘中证银行A",
    "003318": "景顺长城中证500低波动",
    "004069": "南方中证全指证券",
    "006327": "易方达中证海外50ETF联接",
    "090010": "大成中证红利指数A",
    "110003": "易方达上证50指数A",
    "163407": "兴全沪深300A",
    "164906": "交银中证海外中国互联网",
    "501009": "汇添富中证生物科技",
    "501050": "华夏上证50AH",
    "501090": "华宝中证消费龙头",
    "519671": "银河沪深300价值",
    "540012": "汇丰晋信恒生A股龙头"
}


def get_weekly(code: str, begin: date) -> pd.DataFrame:
    df = pd.DataFrame()
    if re.match(r'(sh|sz)\d{6}', code) is not None:
        # df = ak.stock_zh_index_daily_tx(symbol=code)[['date', 'close']]
        df = ak.stock_zh_index_daily(symbol=code)[['date', 'close']]
    elif re.match(r'\d{6}', code) is not None:
        df = ak.fund_em_open_fund_info(fund=code, indicator='累计净值走势')   # [['净值日期', '单位净值']]
        df = df.rename({'净值日期': 'date', '累计净值': 'close'}, axis=1)
        if df.dtypes['close'] != numpy.dtype('float64'):
            df['close'] = df['close'].apply(lambda x: float(x))
    else:
        assert True
    df['date'] = pd.to_datetime(df['date'])
    weekday = 1             # Mon: 0, Tue: 1, ... Sun: 6
    df = df[(df['date'] > begin) & (df['date'].dt.dayofweek == weekday)]
    print(df)
    return df


def get_index_name(code: str) -> str:
    df = ak.stock_zh_index_spot()
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


def loop_back(code: str, begin: date):
    df = get_weekly(code, begin)
    df['每期定投金额'] = 1000
    df['累计定投金额'] = df['每期定投金额'].cumsum()
    fee_rate = 0.001
    df['每期持仓数量'] = df['每期定投金额'] / df['close'] * (1 - fee_rate)
    df['累计持仓数量'] = df['每期持仓数量'].cumsum()
    df['累计持仓净值'] = df['close'] * df['累计持仓数量']
    df['现金流'] = - df['每期定投金额']
    m = df.shape[0]     # number of row
    cumulative_amount = df.iloc[m - 1, df.columns.get_loc('累计定投金额')]
    cumulative_net = df.iloc[m - 1, df.columns.get_loc('累计持仓净值')]
    hold_gain = cumulative_net - cumulative_amount
    df.iloc[m - 1, df.columns.get_loc('现金流')] += cumulative_net
    print(df)
    return_rate = xirr(df, 'date', '现金流')
    print(cumulative_amount, cumulative_net, hold_gain, return_rate)
    # to_excel('loopback.xlsx', symbol, df)
    try:
        title = '{}({})-定投曲线'.format(names[code], code)
    except KeyError:
        title = '{}-定投曲线'.format(code)
    df[['累计定投金额', '累计持仓净值']].plot(figsize=(12, 6), grid=True, title=title)


def main():
    if len(sys.argv) < 3:
        print('Usage: {} code YYYYmmdd'.format(sys.argv[0]))
        sys.exit(1)

    begin = datetime.strptime(sys.argv[2], '%Y%m%d')    # .date()
    loop_back(sys.argv[1], begin)
    # plt.show()


if __name__ == "__main__":
    main()
