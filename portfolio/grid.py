#! /usr/bin/python3
import sys

import pandas as pd
from matplotlib import pyplot, ticker

from xueqiu import Xueqiu


class Grid:
    def __init__(self, code: str, name: str, low: float, high: float, change: float, quantity: int):
        self.code = code
        self.name = name
        self.change = change
        self.quantity = quantity
        self.high = high
        self.low = low
        self.number = (high - low) // change if self.change > 0.1 else 4
        self.index = 0
        self.benchmark = high
        self.cost = 0
        self.value = 0
        self.trans = []

    def __str__(self):
        return 'index(%d), benchmark(%.2f), value(%.2f), cost(%.2f), profit(%.2f)' %\
               (self.index, self.benchmark, self.value, self.cost, self.value - self.cost)

    def trade(self, day: str, price: float, opt: int, count: int):
        self.index += count * opt
        if self.change > 0.1:
            assert self.benchmark == self.high - self.change * self.index
        else:
            self.benchmark = price
        volume = self.quantity * count
        self.cost += price * volume * opt
        self.value = price * self.quantity * self.index
        dic = {'date': day,
               'opt': opt,
               'price': price,
               'volume': volume,
               'index': self.index,
               'value': self.value,
               'cost': self.cost,
               'profit': self.value - self.cost}
        self.trans.append(dic.copy())

    def trade_open(self, day: str, price: float):
        count = 0
        change = self.change if self.change > 0.1 else self.benchmark * self.change

        while price <= self.benchmark - change and self.index + count < self.number:
            self.benchmark -= change
            change = self.change if self.change > 0.1 else self.benchmark * self.change
            count += 1
        if count:
            self.trade(day, price, 1, count)
            return

        while price >= self.benchmark + change and self.index - count > 0:
            self.benchmark += change
            change = self.change if self.change > 0.1 else self.benchmark * self.change
            count += 1
        if count:
            self.trade(day, price, -1, count)
            return

        if self.index:
            self.value = price * self.quantity * self.index

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
        pyplot.figtext(0.9, 0.80, ' 格数 %d' % (self.number + 1))
        pyplot.figtext(0.9, 0.75, ' 最高 %.2f' % self.high)
        pyplot.figtext(0.9, 0.70, ' 最低 %.2f' % self.low)
        if self.change > 0.1:
            pyplot.figtext(0.9, 0.65, ' 涨跌幅 %.2f' % self.change)
        else:
            pyplot.figtext(0.9, 0.65, ' 涨跌幅 %.2f' % (self.change * 100) + '%')
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

    def trade_daily(self, data: pd.DataFrame):
        for _, row in data.iterrows():
            # print(row['date'], row['open'])
            self.trade_open(row['date'], row['open'])

        if len(sys.argv) < 8:
            print('%s(%s) %s_%s %d %d %.2f %.2f %.2f %.2f' %
                  (self.code, self.name, data.iloc[0]['date'], data.iloc[-1]['date'], len(self.trans),
                   self.index * self.quantity, self.benchmark, self.value, self.cost, self.value - self.cost))
        else:
            trans = pd.DataFrame(self.trans)
            print(trans)
            print('%s~%s' % (data.iloc[0]['date'], data.iloc[-1]['date']), self)
            self.draw(data, trans)


def main():
    if len(sys.argv) < 6:
        print('Usage: {} code low high change quantity [start_date(%Y-%m-%d)] [1]'.format(sys.argv[0]))
        sys.exit(1)

    code = sys.argv[1]              # e.g.  code = 'SH113504'
    if len(code) == 8 and code[: 2] in ['sh', 'sz', 'SH', 'SZ'] and code[2:].isnumeric():
        code = code.upper()
    elif len(code) == 6 and code.isnumeric():
        if code.startswith('11'):
            code = 'SH' + code
        elif code.startswith('12'):
            code = 'SZ' + code
    # else:
    #     assert False

    snowball = Xueqiu()
    name = snowball.get_name(code)
    df = snowball.get_data(code)
    if len(sys.argv) > 6:
        start_date = sys.argv[6]    # start_date = '2021-07-01'
        df = df[df['date'] >= start_date]

    grid = Grid(code, name, float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]))
    grid.trade_daily(df)


if __name__ == "__main__":
    main()
