#! /usr/bin/python3
import sys
from datetime import date
from datetime import datetime
from pprint import pprint

import matplotlib.pyplot as plt
import pandas as pd

from mongo import Mongo

# pd.set_option('display.max_rows', 1000)
# pd.set_option('display.max_columns', 6)


def get_close_price(code: str, begin: date) -> tuple:
    mongo = Mongo()
    name = mongo.load_info(code)['name']
    # name = name if len(name) <= 10 else name[: 8] + '..'
    name = '{}({})'.format(name if len(name) <= 10 else name[: 8] + '..', code[4:])
    base = mongo.load_close_price('sh000985')               # use '中证全指' as base
    base['date'] = pd.to_datetime(base['date'])
    base = base.rename({'close': 'sh000985'}, axis=1)

    df = mongo.load_close_price(code)
    df = pd.merge(base, df, on='date', how='outer')
    df.fillna(method='ffill', inplace=True)                 # fill NaN with previous value
    df.fillna({'close': 1.0}, inplace=True)                 # no previous value, fill with 1.0
    weekday = 1                                             # choose Tuesday, Mon: 0, Tue: 1, ... Sun: 6
    df = df[(df['date'] > begin) & (df['date'].dt.dayofweek == weekday)]
    # print(df)
    return name, df


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


def loop_back(code: str, begin: date) -> tuple:
    name, df = get_close_price(code, begin)
    weekday = 1                                 # choose Tuesday, Mon: 0, Tue: 1, ... Sun: 6
    df = df[(df['date'] > begin) & (df['date'].dt.dayofweek == weekday)]

    star = 4
    base = 1000
    exp = 0

    def cal(row: pd.Series) -> float:
        if not exp:
            return base
        a = 1657.7                       # threshold of 5 stars at 2011-01
        year, month = row['date'].year, row['date'].month
        thr = a * 1.1 ** (year - 2011) * (1 + (month - 1) / 120) / 0.8 ** (5 - star)
        return base * (thr / row['sh000985']) ** exp

    df['每期定投金额'] = df.apply(cal, axis=1)
    # print(df)
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
    return_rate = xirr(df, 'date', '现金流')
    df = df.rename({'累计持仓净值': name}, axis=1).set_index('date')
    df.index.name = None
    # print(df)
    return (name, cumulative_amount, cumulative_net, hold_gain, return_rate), df[['累计定投金额', name]]


def comparision(typ: str, codes: list, begin: date):
    results = [loop_back(i, begin) for i in codes]
    columns = ['name', '累计定投金额(万)', '累计持仓净值(万)', '累计收益(万)', '内部收益率(%)']
    df = pd.DataFrame([r[0] for r in results], columns=columns)
    df[columns[1]] = df[columns[1]].apply(lambda x: round(x / 10000))
    df[columns[2]] = df[columns[2]].apply(lambda x: round(x / 10000))
    df[columns[3]] = df[columns[3]].apply(lambda x: round(x / 10000))
    df[columns[4]] = df[columns[4]].apply(lambda x: round(x * 100))
    df.set_index('name', inplace=True)
    df = df.sort_values('内部收益率(%)')
    df.index.name = None
    print(df)
    df2 = pd.concat([r[1] for r in results], axis=1)
    df2 = df2.loc[:, ~df2.columns.duplicated()]        # remove duplicated '累计定投金额'
    print(df2)

    _, axes = plt.subplots(nrows=2, ncols=1)
    title = typ + '定投回测：累计持仓曲线及收益率'
    df2.plot(ax=axes[0], figsize=(12, 8), grid=True, rot=0, title=title)
    ax = df.plot.bar(ax=axes[1], figsize=(12, 8), rot=20)
    for i in ax.containers:
        ax.bar_label(i)
    plt.figtext(.9, .1, '- 同光和尘')
    plt.show()


def get_scale(code: str, mongo=None) -> tuple:
    if not mongo:
        mongo = Mongo()
    name = mongo.load_info(code)['name']
    scale = mongo.load_indicator(code)['total_tna']
    return name, scale


def show_scales(funds: dict):
    mongo = Mongo()
    for key in funds.keys():
        print(key)
        for code in funds[key]:
            print(code[4:], get_scale(code, mongo))


def get_manager(code: str, mongo=None) -> tuple:
    if not Mongo:
        mongo = Mongo()
    managers = mongo.get_manager(code)
    if len(managers) == 1:
        name = managers[0]['name']
        total_scale = managers[0]['total_scale']
    else:
        name = ', '.join([x['name'] for x in managers])
        total_scale = ', '.join([str(x['total_scale']) for x in managers])
    return name, total_scale


def sort(funds: dict, begin: date):
    mongo = Mongo()
    lst = []
    for key in funds.keys():
        for code in funds[key]:
            r = loop_back(code, begin)
            name, rate = r[0][0], round(r[0][-1] * 100, 2)
            scale = get_scale(code, mongo)[1]
            manager, total_scale = get_manager(code, mongo)
            lst.append((name, manager, key, rate, scale, total_scale))
    df = pd.DataFrame(lst, columns=['名称(代码)', '基金经理', '类型', '年化(%)', '规模(亿元)', '总规模(亿元)'])
    df = df.sort_values('年化(%)', ascending=False).reset_index(drop=True)
    print(df)
    df.to_excel('screw_funds.xlsx', index=False)


FUNDS = {
    '深度价值': ["otc_001810", "otc_007130", "otc_006567", 'otc_004350', "otc_260112"],
    '成长价值': ["otc_005827", "otc_005267", "otc_169101", "otc_001712", "otc_519712", "otc_270002", 'otc_110011'],
    '成长': ["otc_260108", "otc_001975", "otc_161005", 'otc_519035', "otc_110013", 'otc_005354', "otc_007119",
           "otc_519068", "otc_377240", "otc_000595"],
    # "otc_007119", "otc_519068"
    '均衡': ["otc_004868", "otc_519688", "otc_163406", "otc_163415", "otc_163402", "otc_166002", 'otc_008276'],
    # 'otc_008276'
    '主动医药': ["otc_001717", 'otc_006002', "otc_003095", "otc_004851", "otc_001766"],
    '主动消费': ["otc_000083", "otc_110022"],
    # '医疗&消费': ["otc_001717", "otc_003095", "otc_001766", "otc_000083", "otc_110022", "otc_000248"],
    '其它': ["otc_001974", 'otc_005259', "otc_540003"]
}

INDEXES = {
    '大盘指数': ["otc_501050", "otc_160716", "otc_217027", "otc_110003", "otc_540012", 'otc_110020'],
    '策略指数': ["otc_519671", "otc_003318", "otc_090010", "otc_501029", "otc_007657", "otc_006341"],
    '医药指数': ["otc_001550", "otc_162412", "otc_501009", "otc_000369", "otc_000968", "otc_001717"],
    '消费指数': ["otc_501090", "otc_001133", "otc_008928", "otc_000248", 'otc_001631', 'otc_161725']
}


def main():
    if len(sys.argv) < 2:
        print('Usage: {} YYYYmmdd'.format(sys.argv[0]))
        sys.exit(1)

    begin = datetime.strptime(sys.argv[1], '%Y%m%d')    # .date()
    # comparision('宽基指数', ["sh502000", "sh510310", "sh510710", "f050025", "f040046", "f000071"], begin)
    # comparision('宽基指数', ["sz161039", "sh501050", "f006341", "f003318", "f090010", "f519671"], begin)
    # comparision('行业指数', ["f000248", "f162412", "f501009", "sz164906", "sh512000", "sh512800"], begin)
    # comparision('主动基金', ["otc_001643", "otc_001717", "otc_001810", "otc_005267", "otc_161005", "otc_163402"], begin)
    # comparision('主动基金', ["f000595", "f001766", "f001974", "f005267", "f377240", "f540003"], begin)

    # show_scales(FUNDS)
    # key = '均衡风格'
    # comparision(key, FUNDS[key], begin)
    sort(FUNDS, begin)


if __name__ == "__main__":
    main()
