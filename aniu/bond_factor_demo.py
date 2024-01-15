#! /usr/bin/python3
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来在图中正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来在图中正常显示负号

data = pd.read_csv('data/bond_daily_20230101-20231222.csv')  # 导入数据，修改文件为本地目录和文件名
data['trade_date'] = pd.to_datetime(data['trade_date'])  # 字符转为日期格式
s_date = pd.to_datetime('20230101')  # 初始化开始日期
e_date = pd.to_datetime('20231231')  # 初始化结束日期
# stat_days=(e_date-s_date).days # 回测统计天数
data = data[data['trade_date'] >= s_date]  # 设置回测开始日期 大于上面的开始日期

# 价格表
pricedf = data[['bond_code', 'trade_date', 'close_price']]
pricedf = pricedf.set_index(['trade_date', 'bond_code']).unstack()['close_price']
pricedf = pricedf.fillna(method='pad')

# 每日收益率
day_return = pricedf.pct_change().shift(-1)
day_return = day_return.fillna(method='pad')

# 溢价率表
premdf = data[['bond_code', 'trade_date', 'bond_prem']]
premdf = premdf.set_index(['trade_date', 'bond_code']).unstack()['bond_prem']


# 取排名最小的N个标的 默认20 可以试试把复制代码问问chatGPT每个函数调用是什么意思
def filtTopN(factor: pd.DataFrame, N=20) -> pd.DataFrame:
    return factor.apply(lambda x: x.rank(method='first') <= N, axis=1)


# 计算每日盈亏，输入信号、日收益表、调仓频率天数freq、单向换仓成本cost_k 可以试试把复制代码问问chatGPT每行是什么意思
def calc_pnl(signal: pd.DataFrame, day_return: pd.DataFrame, freq=1, cost_k=0.001) -> pd.Series:
    signal_freq = pd.DataFrame(index=signal.index)
    var = signal.iloc[range(0, len(signal), freq)]
    signal_freq = signal_freq.join(var)
    signal_freq = signal_freq.fillna(method='pad')
    gross_pnl = day_return[signal_freq].sum(axis=1) / signal_freq.sum(axis=1)
    # print(gross_pnl)
    cost = abs(signal_freq.diff()).sum(axis=1) * cost_k / signal_freq.sum(axis=1)
    # print(cost)
    return gross_pnl - cost


# 设定因子 按低溢价率回测 也可改成按低价回测：factor=pricedf，或者按双低回测：factor=pricedf+premdf
factor = premdf
# 按10只轮动吧
signal = filtTopN(factor, 10)
# 计算每天盈亏数据
pnl = calc_pnl(signal, day_return, 10)
# stock_pnl=calc_pnl(signal, stock_day_return, 10)

# (1+pnl-stock_pnl).cumprod().plot(figsize=(8,4),grid=True);
# tp=(1+pnl-stock_pnl).cumprod()
# 画个收益曲线吧
(1 + pnl).cumprod().plot(figsize=(8, 4), grid=True)
# plt.show()

# 下面统计下总收益和回测
tp = (1 + pnl).cumprod()  # 计算每天累计收益
tp = pd.DataFrame({'date': tp.index, 'value': tp.values})  # 将日期和每天累计收益对应起来
# 计算当日前最高点
tp['max'] = tp['value'].expanding().max()
# 计算历史最高点到当日剩余
tp['d'] = tp['value'] / tp['max']
# 计算回撤完剩余量最小值，以及最大回撤结束时间
end_date, remains = tuple(tp.sort_values(by=['d']).iloc[0][['date', 'd']])
print('总收益:', round((100 * tp.value[len(tp) - 1] - 100), 2), '%')
print('最大回撤:', round((1 - remains) * 100, 2), '%')
