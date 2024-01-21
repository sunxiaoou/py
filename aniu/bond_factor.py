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
    REMAIN = 'remain_size'

    def __init__(self, quantity: int, freq: int, cost: float, data: pd.DataFrame):
        self.quantity = quantity
        self.freq = freq
        self.cost = cost
        self.data = data
        self.prices = self.get_factor(self.PRICE, True)
        self.changes = self.prices.pct_change().shift(-1)
        self.changes = self.changes.fillna(method='pad')
        self.signal = self.get_signal()
        self.codes = self.get_codes()
        self.cum_prod = self.get_cum_prod()
        self.roi = self.get_return_on_investment()
        self.max_dd = self.get_max_draw_down()

    def get_factor(self, column_name: str, fill: bool = False) -> pd.DataFrame:
        df = self.data[['bond_code', 'trade_date', column_name]]
        df = df.set_index(['trade_date', 'bond_code']).unstack()[column_name]
        if fill:
            df = df.fillna(method='pad')
        df.index.name = None
        return df

    # 取排名最小的N个标的
    def filter(self, factor: pd.DataFrame) -> pd.DataFrame:
        return factor.apply(lambda x: x.rank(method='first') <= self.quantity, axis=1)

    @abstractmethod
    def get_signal(self) -> pd.DataFrame:
        pass

    # 取标的的代码
    def get_codes(self) -> pd.DataFrame:
        df = self.signal.iloc[range(0, len(self.signal), self.freq)]
        return df.apply(lambda row: pd.Series(df.columns[row]), axis=1)

    # 计算每天累计收益
    def get_cum_prod(self) -> pd.DataFrame:
        df = self.signal.iloc[range(0, len(self.signal), self.freq)]
        signal_freq = pd.DataFrame(index=self.signal.index)
        signal_freq = signal_freq.join(df)
        signal_freq = signal_freq.fillna(method='pad')
        gross_pnl = self.changes[signal_freq].sum(axis=1) / signal_freq.sum(axis=1)
        # print(gross_pnl)
        cost = abs(signal_freq.diff()).sum(axis=1) * self.cost / signal_freq.sum(axis=1)
        # print(cost)
        series = (gross_pnl - cost + 1).cumprod()
        return pd.DataFrame({'date': series.index, 'value': series.values})

    def get_return_on_investment(self) -> float:
        return round(self.cum_prod.value[len(self.cum_prod) - 1] * 100 - 100, 2)

    def get_max_draw_down(self) -> tuple:
        self.cum_prod['top'] = self.cum_prod['value'].expanding().max()  # 计算当日前最高点
        self.cum_prod['dd'] = self.cum_prod['value'] / self.cum_prod['top']  # 计算历史最高点到当日剩余
        date, remains = tuple(self.cum_prod.sort_values(by=['dd']).iloc[0][['date', 'dd']])
        return date, round((1 - remains) * 100, 2)

    def plot(self):
        df = self.cum_prod[['date', 'value']]
        df = df.dropna().set_index(df.columns[0])
        df.index.name = None
        df.plot(figsize=(8, 4), grid=True)

    def loop_back(self):
        # print(self.get_codes())
        print('总收益: {}%'.format(self.roi))
        print('最大回撤: {}% on {}'.format(self.max_dd[1], self.max_dd[0]))


class LowPrice(Factor):
    def get_signal(self) -> pd.DataFrame:
        return self.filter(self.prices)


class LowPremium(Factor):
    def get_signal(self) -> pd.DataFrame:
        return self.filter(self.get_factor(self.PREMIUM))


class LowRemain(Factor):
    def get_signal(self) -> pd.DataFrame:
        return self.filter(self.get_factor(self.REMAIN))


class TriangleLow(Factor):
    def get_signal(self) -> pd.DataFrame:
        price_rank = self.prices.apply(lambda x: x.rank(), axis=1)
        premium_rank = self.get_factor(self.PREMIUM).apply(lambda x: x.rank(), axis=1)
        remain_rank = self.get_factor(self.REMAIN).apply(lambda x: x.rank(), axis=1)
        return self.filter(price_rank + premium_rank + remain_rank)


def main():
    data = pd.read_csv('data/bond_daily_20230101-20231222.csv')
    data['trade_date'] = pd.to_datetime(data['trade_date'])  # 字符转为日期格式
    s_date = pd.to_datetime('20230101')  # 初始化开始日期
    e_date = pd.to_datetime('20231231')  # 初始化结束日期
    # stat_days=(e_date-s_date).days # 回测统计天数
    data = data[data['trade_date'] >= s_date]  # 设置回测开始日期 大于上面的开始日期
    print('================== 低价 ==================')
    factor = LowPrice(10, 10, 0.001, data)
    factor.loop_back()
    print('================== 低溢价 ==================')
    factor = LowPremium(10, 10, 0.001, data)
    factor.loop_back()
    print('================== 小盘 ==================')
    factor = LowRemain(10, 10, 0.001, data)
    factor.loop_back()
    print('================== 双低+小盘 ==================')
    factor = TriangleLow(10, 10, 0.001, data)
    factor.loop_back()
    factor.plot()
    plt.show()


if __name__ == "__main__":
    main()
