#! /usr/bin/python3
import sys
from pprint import pprint

import pandas as pd
from snowball import Snowball


def find_monthly_corrections(df: pd.DataFrame) -> list:
    """
    根据月线级别下跌的定义，寻找修正的起止日期。
    定义：
      - 从当前新高 (peak) 开始，下跌达到15%或80个交易日内未再创新高，则认为进入修正阶段；
      - 修正结束定义为后续价格重新超过之前的最高点。

    参数：
      df: 包含 'Date' (datetime) 和 'Close' (float) 两列的 DataFrame，按日期升序排列。

    返回：
      corrections: 一个列表，每个元素为 (修正起始日期, 修正结束日期)。
      若最后一轮修正未结束，则不记录该事件。
    """
    # 按日期排序，确保数据顺序正确
    df = df.sort_values('date').reset_index(drop=True)
    corrections = []

    # 初始化：第一个交易日作为初始新高
    current_peak = df.loc[0, 'close']
    peak_date = df.loc[0, 'date']
    peak_index = 0  # 记录新高对应的交易日索引
    in_correction = False  # 是否处于修正阶段
    correction_start = None  # 修正起始日期

    # 遍历数据，从第二个交易日开始
    for i in range(1, len(df)):
        price = df.loc[i, 'close']
        current_date = df.loc[i, 'date']

        # 当出现新高时
        if price > current_peak:
            # 如果之前处于修正阶段，则此次新高代表修正结束
            if in_correction:
                corrections.append((correction_start, current_date))
                in_correction = False
            # 更新新高信息
            current_peak = price
            peak_date = current_date
            peak_index = i
        else:
            # 计算从新高下跌的比例
            decline_pct = (current_peak - price) / current_peak
            # 计算自新高以来经历的交易日数
            trading_days_since_peak = i - peak_index

            # 如果未处于修正中且任一条件触发，则启动修正
            if not in_correction and (decline_pct >= 0.15 or trading_days_since_peak >= 80):
                correction_start = peak_date
                in_correction = True
            # 若已经处于修正中，则继续等待新高来结束修正

    # 如果数据结束时仍处于修正中，可视需求决定是否记录，通常不记录未结束的修正事件
    return corrections


def check_correction_levels(df: pd.DataFrame) -> dict:
    """
    根据收盘价数据，找到标普500指数的历史最高点，
    求出从该点到最近一个交易日的下跌幅度和持续交易日数，
    并根据下列标准判断是否已达到日线/周线/月线级别的下跌：

      - 日线级别：下跌幅度>=5% 或 持续时间>=10个交易日
      - 周线级别：下跌幅度>=10% 或 持续时间>=20个交易日
      - 月线级别：下跌幅度>=15% 或 持续时间>=80个交易日

    参数：
      df: 包含 'Date' (datetime) 和 'Close' (float) 两列的 DataFrame，要求按日期升序排列。

    返回：
      一个字典，包含：
        - 'max_date': 历史最高点日期
        - 'max_close': 历史最高点价格
        - 'last_date': 最近交易日日期
        - 'last_close': 最近交易日价格
        - 'drop_percentage': 从历史最高点到最近交易日的下跌比例（小数表示，如0.08代表8%）
        - 'duration': 历史最高点至最近交易日的持续交易日数
        - 'daily_correction': 是否达到日线级别下跌（True/False）
        - 'weekly_correction': 是否达到周线级别下跌（True/False）
        - 'monthly_correction': 是否达到月线级别下跌（True/False）
    """
    # 确保数据按日期排序
    df = df.sort_values('date').reset_index(drop=True)

    # 找到历史最高点对应的行（最大收盘价）
    max_idx = df['close'].idxmax()
    max_date = df.loc[max_idx, 'date']
    max_close = df.loc[max_idx, 'close']

    # 获取最近交易日的数据（最后一行）
    last_idx = df.index[-1]
    last_date = df.loc[last_idx, 'date']
    last_close = df.loc[last_idx, 'close']

    # 计算下跌幅度：从历史最高点到最近交易日的跌幅比例
    drop_percentage = (max_close - last_close) / max_close if max_close > 0 else 0

    # 计算持续的交易日数：从最高点到最近交易日经历的交易日数量
    duration = last_idx - max_idx  # 或者使用 (len(df)-1 - max_idx)

    # 定义各级别的阈值
    daily_drop_threshold = 0.05   # 5%
    daily_duration_threshold = 10    # 10个交易日（约2周）
    weekly_drop_threshold = 0.10   # 10%
    weekly_duration_threshold = 20   # 20个交易日（约4周）
    monthly_drop_threshold = 0.15   # 15%
    monthly_duration_threshold = 80  # 80个交易日（约4个月）

    # 根据下跌幅度或持续交易日数，判断是否达到各级别下跌条件（只要满足其中一项即认为达标）
    daily_correction = (drop_percentage >= daily_drop_threshold) or (duration >= daily_duration_threshold)
    weekly_correction = (drop_percentage >= weekly_drop_threshold) or (duration >= weekly_duration_threshold)
    monthly_correction = (drop_percentage >= monthly_drop_threshold) or (duration >= monthly_duration_threshold)

    return {
        'max_date': max_date,
        'max_close': float(max_close),
        'last_date': last_date,
        'last_close': float(last_close),
        'drop_percentage': round(float(drop_percentage), 4),
        'duration': duration,
        'daily_correction': bool(daily_correction),
        'weekly_correction': bool(weekly_correction),
        'monthly_correction': bool(monthly_correction)
    }


def main():
    if len(sys.argv) < 2:
        print('Usage: %s check/find code' % sys.argv[0])
        sys.exit(1)
    action = sys.argv[1]
    if len(sys.argv) == 2:
        code = '.INX'
    else:
        code = sys.argv[2]
    snowball = Snowball()
    print(snowball.get_name(code))
    df = snowball.get_data(code)
    df = df[['date', 'close']]
    # print(df)
    if action == 'find':
        pprint(find_monthly_corrections(df))
    else:
        pprint(check_correction_levels(df))


if __name__ == "__main__":
    main()
