#! /usr/bin/python3
import sys

import pandas as pd
from matplotlib import pyplot, ticker

import xueqiu


class Grid:
    def __init__(self, code: str, low: float, high: float, interval: float, unit: int):
        self.code = code
        self.interval = interval
        self.unit = unit
        self.high = high
        self.low = low
        self.number = (high - low) // interval
        self.index = 0
        self.benchmark = high
        self.cost = 0
        self.value = 0
        self.trans = []

    def __str__(self):
        return 'index(%d), benchmark(%.2f), value(%.2f), cost(%.2f), profit(%.2f)' %\
               (self.index, self.benchmark, self.value, self.cost, self.value - self.cost)

    def trade_open(self, day: str, price: float):
        count = 0
        while price <= self.benchmark - self.interval and self.index + count < self.number:
            self.benchmark -= self.interval
            count += 1
        if count:
            self.index += count
            self.benchmark = price
            quantity = self.unit * count
            self.cost += price * quantity
            self.value = price * self.unit * self.index
            # tran = Transaction(day, self.code, 1, price, quantity)
            dic = {'date': day,
                   'opt': 1,
                   'price': price,
                   'quantity': quantity,
                   'index': self.index,
                   'value': self.value,
                   'cost': self.cost,
                   'profit': self.value - self.cost}
            self.trans.append(dic.copy())
            return
        # count = 0
        while price >= self.benchmark + self.interval and self.index - count > 0:
            self.benchmark += self.interval
            count += 1
        if count:
            self.index -= count
            self.benchmark = price
            quantity = self.unit * count
            self.cost -= price * quantity
            self.value = price * self.unit * self.index
            # tran = Transaction(day, self.code, -1, price, quantity)
            dic = {'date': day,
                   'opt': -1,
                   'price': price,
                   'quantity': quantity,
                   'index': self.index,
                   'value': self.value,
                   'cost': self.cost,
                   'profit': self.value - self.cost}
            self.trans.append(dic.copy())
            return
        if self.index:
            self.value = price * self.unit * self.index

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
        pyplot.title('可转债网格回测 %s (%s ~ %s)' % (self.code, data.index[0], data.index[-1]))
        pyplot.ylabel('开盘价(元)')
        pyplot.grid()
        pyplot.gca().xaxis.set_major_locator(ticker.MultipleLocator(data.shape[0] // 8))
        pyplot.xticks(rotation=30)
        pyplot.plot(data.index, data[self.code])
        pyplot.plot(buy.index, buy['price'], 'og')
        pyplot.plot(sell.index, sell['price'], 'or')

        pyplot.figtext(0.9, 0.85, ' Grid')
        pyplot.figtext(0.9, 0.80, ' 格数 %d格' % (self.number + 1))
        pyplot.figtext(0.9, 0.75, ' 最高 %d元' % self.high)
        pyplot.figtext(0.9, 0.70, ' 最低 %d元' % self.low)
        pyplot.figtext(0.9, 0.65, ' 间隔 %d元' % self.interval)
        pyplot.figtext(0.9, 0.60, ' 单位 %d张' % self.unit)
        pyplot.figtext(0.9, 0.55, ' Trade')
        pyplot.figtext(0.9, 0.50, ' 开盘买(绿)')
        pyplot.figtext(0.9, 0.45, ' 开盘卖(红)')
        pyplot.figtext(0.9, 0.40, ' Result')
        pyplot.figtext(0.9, 0.35, ' 当前网格 %d' % self.index)
        pyplot.figtext(0.9, 0.30, ' 基准 %.2f' % self.benchmark)
        pyplot.figtext(0.9, 0.25, ' 市值 %.2f' % self.value)
        pyplot.figtext(0.9, 0.20, ' 成本 %.2f' % self.cost)
        pyplot.figtext(0.9, 0.15, ' 收益 %.2f' % (self.value - self.cost))
        pyplot.figtext(0.9, 0.05, '- 同光和尘')
        pyplot.show()

    def trade_daily(self, data: pd.DataFrame):
        for _, row in data.iterrows():
            # print(row['date'], row['open'])
            self.trade_open(row['date'], row['open'])

        trans = pd.DataFrame(self.trans)
        print(trans)
        print('%s - %s' % (data.iloc[0]['date'], data.iloc[-1]['date']))
        print(self)
        self.draw(data, trans)


def main():
    if len(sys.argv) < 2:
        print('Usage: {} stock_code [start_date(%Y-%m-%d)]'.format(sys.argv[0]))
        sys.exit(1)

    code = sys.argv[1]              # e.g.  code = 'SH113504'
    df = xueqiu.get_data(code)
    if len(sys.argv) > 2:
        start_date = sys.argv[2]    # start_date = '2021-07-01'
        df = df[df['date'] >= start_date]

    grid = Grid(code, 130, 170, 10, 50)
    grid.trade_daily(df)


if __name__ == "__main__":
    main()
