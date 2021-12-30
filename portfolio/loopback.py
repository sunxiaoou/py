#! /usr/bin/python3
import sys
from datetime import date
from datetime import datetime
from pprint import pprint

import matplotlib.pyplot as plt
import pandas as pd

from mongo import Mongo

# pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 6)


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


def increment(row: pd.Series, base: float, exp: int, thr=None, refer=None) -> float:
    if not exp:
        return 1000             # return constant amount
    if not thr:
        a = 1657.7              # threshold of 5 stars at 2011-01
        year, month = row['date'].year, row['date'].month
        star = 4                # use 4 star as underestimated level
        thr = a * 1.1 ** (year - 2011) * (1 + (month - 1) / 120) / 0.8 ** (5 - star)
    if refer == '盈利收益率':
        inc = 0 if row['valuation'] < thr else base * (row['valuation'] / thr) ** exp
    else:
        inc = 0 if row['valuation'] > thr else base * (thr / row['valuation']) ** exp
    return inc


def loop_back(code: str, begin: date, parameters=(1000, 0)) -> tuple:
    mongo = Mongo()
    dic = mongo.load_info(code)
    name, typ = dic['name'], dic['type']
    print(name, typ)
    name = '{}({})'.format(name if len(name) <= 10 else name[: 8] + '..', code[4:])
    if typ in ['指数型', 'QDII']:      # and parameters[1]:
        dic = mongo.get_threshold(code[4:])
        index, refer, thr = dic['_id'], dic['参考指标'], dic['低估']
        parameters += (thr, refer)
        print(parameters)
        df = mongo.load_valuation(index)
    else:
        df = mongo.load_close_price('sh000985')     # use '中证全指' as valuation
        df = df.rename({'close': 'valuation'}, axis=1)

    df['date'] = pd.to_datetime(df['date'])
    # print(df[(df['date'] > begin) & (df['date'].dt.dayofweek == 1)])
    df2 = mongo.load_close_price(code)
    # print(df2[(df2['date'] > begin) & (df2['date'].dt.dayofweek == 1)])
    df = pd.merge(df, df2, on='date', how='outer')
    df = df.sort_values('date')
    df.fillna(method='ffill', inplace=True)         # fill NaN with previous value
    df.fillna({'close': 1.0}, inplace=True)         # no previous value, fill with 1.0
    weekday = 1                                     # choose Tuesday, Mon: 0, Tue: 1, ... Sun: 6
    df = df[(df['date'] > begin) & (df['date'].dt.dayofweek == weekday)]
    # print(df)

    df['每期定投金额'] = df.apply(lambda x: increment(x, *parameters), axis=1)
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
    df = df.sort_index()
    df.index.name = None
    # print(df)
    return (name, cumulative_amount, cumulative_net, hold_gain, return_rate), df[['累计定投金额', name]]


def comparision(typ: str, codes: list, begin: date):
    results = [loop_back(i, begin, (1000, 0)) for i in codes]
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

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
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
    # df.to_excel('screw.xlsx', 'indexes', index=False)


def sort_indexes(begin: date):
    mongo = Mongo()
    lst = []
    for code in mongo.get_otc_indexes():
        r = loop_back(code, begin)
        name, rate = r[0][0], round(r[0][-1] * 100, 2)
        scale = get_scale(code, mongo)[1]
        manager, total_scale = get_manager(code, mongo)
        lst.append((name, manager, rate, scale, total_scale))
    df = pd.DataFrame(lst, columns=['名称(代码)', '基金经理', '年化(%)', '规模(亿元)', '总规模(亿元)'])
    df = df.sort_values('年化(%)', ascending=False).reset_index(drop=True)
    print(df)


FUNDS = {
    '深度价值': ['otc_001810', "otc_007130", "otc_006567", "otc_260112", 'otc_000480', 'otc_004350'],
    # otc_006551'
    '成长价值': ["otc_005827", 'otc_110011', "otc_005267", 'otc_169101', "otc_001712", "otc_519712", "otc_270002"],
    # 'otc_001112', 'otc_003396', 'otc_519697',
    '成长': ["otc_000595", 'otc_001975', 'otc_005354', "otc_110013", "otc_377240", 'otc_519035'],
    # "otc_007119", "otc_519068", "otc_260108", "otc_161005", "otc_260101"
    '均衡': ["otc_004868", "otc_163406", "otc_163415", "otc_163402", "otc_166002", 'otc_008276', "otc_519688"],
    # 'otc_519736',
    '主动医药': ['otc_006002', "otc_003095", "otc_004851", "otc_001766", "otc_001717"],
    # 'otc_000831',
    '主动消费': ["otc_000083", "otc_110022"],
    '新能源': ['otc_005669', "otc_540003"],
    # '医疗&消费': ["otc_001717", "otc_003095", "otc_001766", "otc_000083", "otc_110022", "otc_000248"],
    '其它': ["otc_001974", 'otc_005259', 'otc_001668', 'otc_001487', 'otc_001877']
}

INDEXES = {
    '大盘': ["otc_217027", "otc_110003", "otc_540012", 'otc_110020', 'otc_161227', 'otc_213010', 'otc_163109',
           'otc_530015', 'otc_070023', 'otc_040180'],
    '中小盘': ['otc_161039', 'otc_161022', 'otc_161017'],
    '策略': ["otc_519671", "otc_003318", "otc_007657", "otc_006341", 'otc_160716'],
    '红利': ['otc_501029', 'otc_481012', 'otc_090010'],
    '医药': ["otc_001550", "otc_162412", "otc_501009", "otc_000968"],
    '消费': ["otc_501090", "otc_001133", "otc_000248", 'otc_008928', 'otc_001631', 'otc_161725', 'otc_005063',
           'otc_008519'],
    '行业': ['otc_001064', 'otc_161024', 'otc_004856', 'otc_004069', 'otc_005223', 'otc_001594', 'otc_160218'],
    'QDII': ['otc_161128', 'otc_040046', 'otc_162415', 'otc_050025', 'otc_000369', 'otc_006327'],
    '港股': ["otc_501050", 'otc_000071', 'otc_110031', 'otc_501021', 'otc_012348'],
    '科技': ['otc_010202']
}


def test(code: str, begin: date):
    r0, r1 = loop_back(code, begin, (1000, 1))
    print(r0)
    print(r1)


def main():
    if len(sys.argv) < 2:
        print('Usage: {} YYYYmmdd'.format(sys.argv[0]))
        sys.exit(1)

    begin = datetime.strptime(sys.argv[1], '%Y%m%d')    # .date()
    # test('otc_110003', begin)
    # show_scales(FUNDS)
    key = '成长'
    comparision(key, FUNDS[key], begin)
    # key = '大盘指数'
    # comparision(key, INDEXES[key], begin)
    # indexes = ['otc_110003', 'otc_110020', 'otc_161017', 'otc_000071', 'otc_050025', 'otc_040046']
    # comparision('宽基', indexes, begin)

    # sort(INDEXES, begin)
    # sort(FUNDS, begin)
    # sort_indexes(begin)


if __name__ == "__main__":
    main()
