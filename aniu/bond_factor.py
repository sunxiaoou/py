#! /usr/bin/python3
from abc import ABC, abstractmethod

import pandas as pd
import matplotlib.pyplot as plt

# pd.set_option('display.max_rows', 200)
# pd.set_option('display.max_columns', 10)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来在图中正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来在图中正常显示负号


class Factor(ABC):
    PRICE = 'close_price'
    PREMIUM = 'bond_prem'

    def __init__(self, quantity: int, freq: int, cost: float, data: pd.DataFrame):
        self.quantity = quantity
        self.freq = freq
        self.cost = cost
        self.data = data
        self.prices = self.get_factor(self.PRICE, True)
        self.changes = self.prices.pct_change().shift(-1)
        self.changes = self.changes.fillna(method='pad')

    def get_factor(self, column_name: str, fill: bool = False) -> pd.DataFrame:
        df = self.data[['bond_code', 'trade_date', column_name]]
        df = df.set_index(['trade_date', 'bond_code']).unstack()[column_name]
        if fill:
            df = df.fillna(method='pad')
        return df

    @abstractmethod
    def get_signal(self) -> pd.DataFrame:
        pass

    # 取排名最小的N个标的
    def filter(self, factor: pd.DataFrame) -> pd.DataFrame:
        return factor.apply(lambda x: x.rank(method='first') <= self.quantity, axis=1)

    # 取标的的代码
    def get_codes(self, signal: pd.DataFrame) -> pd.DataFrame:
        df = signal.iloc[range(0, len(signal), self.freq)]
        return df.apply(lambda row: pd.Series(df.columns[row]), axis=1)

    def calc_pnl(self, signal: pd.DataFrame) -> pd.Series:
        df = signal.iloc[range(0, len(signal), self.freq)]
        signal_freq = pd.DataFrame(index=signal.index)
        signal_freq = signal_freq.join(df)
        signal_freq = signal_freq.fillna(method='pad')
        gross_pnl = self.changes[signal_freq].sum(axis=1) / signal_freq.sum(axis=1)
        # print(gross_pnl)
        cost = abs(signal_freq.diff()).sum(axis=1) * self.cost / signal_freq.sum(axis=1)
        # print(cost)
        return gross_pnl - cost

    def loop_back(self):
        signal = self.get_signal()
        print(self.get_codes(signal))
        pnl = self.calc_pnl(signal)
        tp = (1 + pnl).cumprod()  # 计算每天累计收益
        tp = pd.DataFrame({'date': tp.index, 'value': tp.values})  # 将日期和每天累计收益对应起来
        # 计算当日前最高点
        tp['max'] = tp['value'].expanding().max()
        # 计算历史最高点到当日剩余
        tp['d'] = tp['value'] / tp['max']
        end_date, remains = tuple(tp.sort_values(by=['d']).iloc[0][['date', 'd']])
        print('总收益:', round((100 * tp.value[len(tp) - 1] - 100), 2), '%')
        print('最大回撤:', round((1 - remains) * 100, 2), '%')


class LowPrice(Factor):
    def get_signal(self) -> pd.DataFrame:
        return self.filter(self.prices)


class LowPremium(Factor):
    def get_signal(self) -> pd.DataFrame:
        return self.filter(self.get_factor(self.PREMIUM))


class DoubleLow(Factor):
    def get_signal(self) -> pd.DataFrame:
        price_rank = self.prices.apply(lambda x: x.rank(), axis=1)
        premium_rank = self.get_factor(self.PREMIUM).apply(lambda x: x.rank(), axis=1)
        return self.filter(price_rank + premium_rank)


def main():
    data = pd.read_csv('data/bond_daily_20230101-20231222.csv')
    data['trade_date'] = pd.to_datetime(data['trade_date'])  # 字符转为日期格式
    s_date = pd.to_datetime('20230101')  # 初始化开始日期
    e_date = pd.to_datetime('20231231')  # 初始化结束日期
    # stat_days=(e_date-s_date).days # 回测统计天数
    data = data[data['trade_date'] >= s_date]  # 设置回测开始日期 大于上面的开始日期
    low_price = LowPrice(10, 10, 0.001, data)
    low_price.loop_back()
    low_premium = LowPremium(10, 10, 0.001, data)
    low_premium.loop_back()
    double_low = DoubleLow(10, 10, 0.001, data)
    double_low.loop_back()


if __name__ == "__main__":
    main()
