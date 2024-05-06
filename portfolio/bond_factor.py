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
        self.quantity = quantity                                # 策略组合中的标的数，10代表10只转债
        self.freq = freq                                        # 组合轮动的频率，比如10代表10个交易日
        self.cost = cost                                        # 交易佣金比率
        self.data = data                                        # 原始数据表
        self.prices = self.get_factor(self.PRICE, True)         # 全部标的的日收盘价表
        self.changes = self.prices.pct_change().shift(-1)       # 全部标的的日涨跌幅表
        self.changes = self.changes.fillna(method='pad')
        self.signal = self.get_signal()                         # bool表，标识轮动周期中加入组合的标的
        self.portfolio_codes = self.get_portfolio_codes()       # 轮动周期中加入组合的标的代码
        self.portfolio_prices = self.get_portfolio_prices()     # 轮动周期中加入组合的标的价格
        self.cum_prod = self.get_cum_prod()                     # 每日累计收益
        self.roi = self.get_return_on_investment()              # 总收益
        self.max_dd = self.get_max_draw_down()                  # 最大回撤

    # 生成不同因子的数值表
    def get_factor(self, column_name: str, fill: bool = False) -> pd.DataFrame:
        df = self.data[['bond_code', 'trade_date', column_name]]
        df = df.set_index(['trade_date', 'bond_code']).unstack()[column_name]
        if fill:
            df = df.fillna(method='pad')
        df.index.name = None
        return df

    # 取排名最小的N个标的，其中N为组合中的标的数，返回bool表，用于标识轮动周期中加入组合的标的
    def filter(self, factor: pd.DataFrame) -> pd.DataFrame:
        df = factor.apply(lambda x: x.rank(method='first') <= self.quantity, axis=1)
        signal = pd.DataFrame(index=df.index)
        df = df.iloc[range(0, len(df), self.freq)]      # 按轮动周期取样
        return signal.join(df).fillna(method='pad')     # 填充到本周期

    # 调用不同因子的filter
    @abstractmethod
    def get_signal(self) -> pd.DataFrame:
        pass

    def get_portfolio_codes(self) -> pd.DataFrame:
        df = self.signal.iloc[range(0, len(self.signal), self.freq)]
        return df.apply(lambda row: pd.Series(df.columns[row]), axis=1)

    def get_portfolio_prices(self) -> pd.DataFrame:
        df = self.prices[self.signal].apply(lambda row: row.dropna().values, axis=1)
        df = pd.DataFrame(df.to_list(), index=df.index)
        return df.iloc[range(0, len(df), self.freq)]

    # 通过本周期组合的涨跌幅表和首日价格序列，算出本周期完整价格表，逐日求和，再算出组合每日的涨跌幅
    def handle_change(self, change: pd.DataFrame) -> pd.DataFrame:
        first_price = self.portfolio_prices.loc[change.index[0]]    # 取得本周期组合的首日价格序列
        prices = (1 + change).cumprod() * first_price               # 计算后续价格表
        df = pd.DataFrame([first_price])
        prices = pd.concat([df, prices])                            # 加入首日价格到价格表
        prices['change'] = prices.sum(axis=1).pct_change()          # 计算组合涨跌幅
        return prices.iloc[1:]                                      # 去掉首日价格

    def get_cum_prod(self) -> pd.DataFrame:
        # gross_pnl = self.changes[self.signal].sum(axis=1) / self.signal.sum(axis=1)
        df = self.changes[self.signal].apply(lambda row: row.dropna().values, axis=1)
        portfolio_changes = pd.DataFrame(df.to_list(), index=df.index)
        portfolio_prices = None
        # 将组合涨跌幅按轮动周期分块，计算组合每日涨跌幅序列
        for i in range(0, len(portfolio_changes), self.freq):
            prices = self.handle_change(portfolio_changes.iloc[i: i + self.freq])
            if portfolio_prices is None:
                portfolio_prices = prices
            else:
                portfolio_prices = pd.concat([portfolio_prices, prices])
        gross_pnl = portfolio_prices.iloc[:, -1]
        # df2 = pd.DataFrame({'gross_pnl': gross_pnl, 'gross_pnl2': gross_pnl2})
        # df2['diff'] = df2['gross_pnl'] - df2['gross_pnl2']
        # print(df2)

        cost = abs(self.signal.diff()).sum(axis=1) * self.cost / self.signal.sum(axis=1)
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
        # print(self.get_portfolio_codes())
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
