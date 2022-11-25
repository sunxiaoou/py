#! /usr/bin/python3
import pandas as pd
from matplotlib import pyplot, ticker

import xueqiu


class Grid:
    def __init__(self, code: str, low: float, high: float, interval: float, unit: int):
        self.code = code
        self.interval = interval
        self.unit = unit
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
        # print(date)
        data.index.name = None

        buy = trans[trans['opt'] == 1][['date', 'price']]
        buy = buy.dropna().set_index('date', drop=True)
        buy.index.name = None
        sell = trans[trans['opt'] == -1][['date', 'price']]
        sell = sell.dropna().set_index('date', drop=True)
        sell.index.name = None

        pyplot.figure(figsize=(10, 6))
        pyplot.grid()
        pyplot.gca().xaxis.set_major_locator(ticker.MultipleLocator(40))
        pyplot.xticks(rotation=30)
        pyplot.plot(data.index, data[self.code])
        pyplot.plot(buy.index, buy['price'], 'or')
        pyplot.plot(sell.index, sell['price'], 'og')
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
    code = 'SH113504'
    df = xueqiu.get_data(code)
    start_date = '2021-07-01'
    if start_date:
        df = df[df['date'] >= start_date]
    grid = Grid('SH113504', 130, 170, 10, 50)
    grid.trade_daily(df)


if __name__ == "__main__":
    main()
