#! /usr/bin/python3
import re
import sys
import time

import pandas as pd
from matplotlib import pyplot, ticker

from mysql import MySql
from xueqiu import Xueqiu

# pd.set_option('display.max_rows', 4000)
pd.set_option('display.max_columns', 10)


class Grid:
    def __init__(self, low: float, high: float, number: int, is_percent: bool):
        self.low = low
        self.high = high
        self.is_percent = is_percent
        self.number = number
        if not self.is_percent:
            self.change = round((high - low) / number, 2)
            self.change2 = - self.change
            self.array = [high - self.change * i for i in range(self.number + 1)]
        else:
            self.change = round((high / low) ** (1 / number) - 1, 4)
            self.change2 = round((low / high) ** (1 / number) - 1, 4)
            self.array = [round(high / (1 + self.change) ** i, 2) for i in range(self.number + 1)]

    def __str__(self):
        return str([self.change, self.change2]) + ' ' + str(self.array)

    def get_count(self, price: float, benchmark: float) -> tuple:
        index = self.array.index(benchmark)
        count = 0
        while index < self.number and self.array[index + 1] >= price:
            index += 1
            count += 1
        if count:
            return index, self.array[index], count

        while index > 0 and self.array[index - 1] <= price:
            index -= 1
            count -= 1
        return index, self.array[index], count

    def show_grid(self, quantity: int) -> pd.DataFrame:
        df = pd.DataFrame([self.array, [0] + [quantity] * self.number],
                          index=['price', 'quantity']).T
        df['quantity'] = df['quantity'].apply(lambda x: int(x))
        df['q_sum'] = df['quantity'].cumsum()
        df['amount'] = df['price'] * df['quantity']
        df['cost'] = df['amount'].cumsum()
        df['value'] = df['price'] * df['q_sum']
        df['loss'] = df['value'] - df['cost']
        df['loss(%)'] = round(df['loss'] / df['cost'] * 100, 2)
        return df


class LoopBack:
    def __init__(self, grid: Grid, code: str, quantity: int, start_date: str = ''):
        if len(code) == 8 and code[: 2] in ['sh', 'sz', 'SH', 'SZ'] and code[2:].isnumeric():
            code = code.upper()
        elif len(code) == 6 and code.isnumeric():
            if code.startswith('11'):
                code = 'SH' + code
            elif code.startswith('12'):
                code = 'SZ' + code

        # snowball = Xueqiu()
        # name = snowball.get_name(code)
        # data = snowball.get_full(code)

        db = MySql(database='portfolio')
        where = 'code = "%s"' % code
        if start_date:
            where += ' AND date >= "%s"' % start_date
        data = db.to_frame('cvtbone_daily', ['date', 'name', 'open'], where)
        name = data['name'].iloc[0]

        self.grid = grid
        self.code = code
        self.name = name
        self.data = data
        self.quantity = quantity
        self.benchmark = grid.high
        self.index = 0
        self.cost = 0
        self.value = 0
        self.trans = []

    def __str__(self):
        return 'index(%d), benchmark(%.2f), value(%.2f), cost(%.2f), profit(%.2f)' %\
               (self.index, self.benchmark, self.value, self.cost, self.value - self.cost)

    def trade_open(self, day: str, price: float):
        self.index, self.benchmark, count = self.grid.get_count(price, self.benchmark)
        self.value = price * self.quantity * self.index
        if count:
            volume = self.quantity * count
            self.cost += price * volume
            dic = {'date': day,
                   'opt': 1 if count > 0 else -1,
                   'price': price,
                   'volume': volume,
                   'index': self.index,
                   'value': self.value,
                   'cost': self.cost,
                   'profit': round(self.value - self.cost, 2)}
            self.trans.append(dic.copy())

    def draw(self, data: pd.DataFrame, trans: pd.DataFrame):
        data = data[['date', 'open']]
        data = data.rename({'open': self.code}, axis=1)
        data = data.dropna().set_index('date')
        data.index.name = None
        # print(date)

        buy = trans[trans['opt'] == 1][['date', 'price']]
        buy = buy.dropna().set_index('date', drop=True)
        buy.index.name = None
        sell = trans[trans['opt'] == -1][['date', 'price']]
        sell = sell.dropna().set_index('date', drop=True)
        sell.index.name = None

        pyplot.figure(figsize=(10, 6))
        pyplot.title('网格策略回测 %s(%s) (%s ~ %s)' %
                     (self.name, self.code, data.index[0], data.index[-1]))
        pyplot.ylabel('开盘价(元)')
        pyplot.grid()
        pyplot.gca().xaxis.set_major_locator(ticker.MultipleLocator(data.shape[0] // 8))
        pyplot.xticks(rotation=30)
        pyplot.plot(data.index, data[self.code])
        pyplot.plot(buy.index, buy['price'], 'og')
        pyplot.plot(sell.index, sell['price'], 'or')

        pyplot.figtext(0.9, 0.85, ' Grid')
        pyplot.figtext(0.9, 0.80, ' 格数 %d' % (self.grid.number + 1))
        pyplot.figtext(0.9, 0.75, ' 最高 %.2f' % self.grid.high)
        pyplot.figtext(0.9, 0.70, ' 最低 %.2f' % self.grid.low)
        if self.grid.change > 0.1:
            pyplot.figtext(0.9, 0.65, ' 涨跌幅 %.2f' % self.grid.change)
        else:
            pyplot.figtext(0.9, 0.65, ' 涨跌幅 %.2f' % (self.grid.change * 100) + '%')
        pyplot.figtext(0.9, 0.60, ' 数量 %d' % self.quantity)
        pyplot.figtext(0.9, 0.55, ' Trade')
        pyplot.figtext(0.9, 0.50, ' 开盘买(绿)')
        pyplot.figtext(0.9, 0.45, ' 开盘卖(红)')
        pyplot.figtext(0.9, 0.40, ' Result')
        pyplot.figtext(0.9, 0.35, ' 剩余网格 %d' % self.index)
        pyplot.figtext(0.9, 0.30, ' 基准 %.2f' % self.benchmark)
        pyplot.figtext(0.9, 0.25, ' 市值 %.2f' % self.value)
        pyplot.figtext(0.9, 0.20, ' 成本 %.2f' % self.cost)
        pyplot.figtext(0.9, 0.15, ' 盈亏 %.2f' % (self.value - self.cost))
        pyplot.figtext(0.9, 0.05, '- 同光和尘')
        pyplot.savefig('%s_%s.png' % (self.code, self.name), dpi=400, bbox_inches='tight')
        pyplot.show()

    def trade_daily(self) -> str:
        for _, row in self.data.iterrows():
            # print(row['date'], row['open'])
            self.trade_open(row['date'], row['open'])

        if 'pic' not in sys.argv:
            return '%s(%s) %s_%s %d %d %.2f %.2f %.2f %.2f' \
                   % (self.code, self.name, self.data.iloc[0]['date'], self.data.iloc[-1]['date'], len(self.trans),
                      self.index * self.quantity, self.benchmark, self.value, self.cost, self.value - self.cost)
        else:
            trans = pd.DataFrame(self.trans)
            print(trans)
            print('%s~%s' % (self.data.iloc[0]['date'], self.data.iloc[-1]['date']), self)
            self.draw(self.data, trans)
            return ''


def get_codes(file: str) -> list:
    with open(file) as f:
        text = f.read()
    blocks = text.split('代码')
    lines1 = blocks[1].split('\n')
    l1 = [row.split()[1] for row in lines1[1: -2]]
    lines5 = blocks[5].split('\n')
    l5 = [row.split()[1] for row in lines5[1: -2]]
    lines6 = blocks[6].split('\n')
    l6 = [row.split()[1] for row in lines6[1: -2]]
    return sorted(list(set(l1 + l5 + l6)))


def trade_codes(grid: Grid, codes: list, quantity: int, start_date: str) -> pd.DataFrame:
    result = []
    for code in codes:
        s = LoopBack(grid, code, quantity, start_date).trade_daily()
        s = s.split()
        result.append([s[0], float(s[-1])])
        time.sleep(0.1)
    change = round(grid.change * 100, 2) if grid.is_percent else grid.change
    return pd.DataFrame(result, columns=['code_name', '%d_%.2f' % (grid.low, change)])


def batch(file: str, quantity: int, start_date: str) -> pd.DataFrame:
    args_list = [
        (115, 135, 4, False), (120, 150, 4, False), (125, 165, 4, False),
        (115, 135, 4, True), (120, 150, 4, True), (125, 165, 4, True)
    ]

    codes = get_codes(file)
    result = pd.DataFrame()
    i = 0
    for i in range(len(args_list)):
        df = trade_codes(Grid(*args_list[i]), codes, quantity, start_date)
        result = result.merge(df, on=df.columns[0], how='inner') if i else df

    result['max_col_name'] = result.iloc[:, -i - 1:].idxmax(axis=1)
    result['max_value'] = result[result.columns[-i - 2: -1]].max(axis=1)
    result = result.sort_values(by='max_value', ascending=False)
    result.reset_index(drop=True, inplace=True)
    return result


def usage():
    print('Usage: {} grid low,high,number,is_percent price benchmark [quantity]'.
          format(sys.argv[0]))
    print('       {} loopback low,high,number,is_percent code quantity [pic start_date(%Y-%m-%d)]'.
          format(sys.argv[0]))
    print('       {} batch cvt_file quantity start_date(%Y-%m-%d)'.format(sys.argv[0]))


def main():
    if len(sys.argv) > 4:
        if sys.argv[1] == 'grid':
            a = sys.argv[2].split(',')
            grid = Grid(float(a[0]), float(a[1]), int(a[2]), True if int(a[3]) else False)
            print(grid)
            if len(sys.argv) > 5:
                print(grid.show_grid(int(sys.argv[5])))
            print(grid.get_count(float(sys.argv[3]), float(sys.argv[4])))
        elif sys.argv[1] == 'loopback':
            a = sys.argv[2].split(',')
            grid = Grid(float(a[0]), float(a[1]), int(a[2]), True if int(a[3]) else False)
            if re.match(r'\d\d\d\d-\d\d-\d\d', sys.argv[-1]):
                loopback = LoopBack(grid, sys.argv[3], int(sys.argv[4]), sys.argv[-1])
            else:
                loopback = LoopBack(grid, sys.argv[3], int(sys.argv[4]))
            print(loopback.trade_daily())
        elif sys.argv[1] == 'batch':
            print(batch(sys.argv[2], int(sys.argv[3]), sys.argv[4]))
        else:
            usage()
    else:
        usage()


if __name__ == "__main__":
    main()
