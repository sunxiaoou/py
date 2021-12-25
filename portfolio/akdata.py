#! /usr/bin/python3

import akshare as ak
import numpy as np
import pandas as pd

from mongo import Mongo


class AkData:
    @staticmethod
    def indexes_info() -> pd.DataFrame:
        df = ak.index_stock_info()
        df = df.rename({'index_code': '_id', 'display_name': 'name'}, axis=1)
        df['_id'] = df['_id'].apply(lambda x: int(x))
        print(df)
        return df

    @staticmethod
    def on_market_info() -> pd.DataFrame:
        df = ak.fund_etf_category_sina(symbol='ETF基金')[['代码', '名称']]
        # print(df)
        df2 = ak.fund_etf_category_sina(symbol='LOF基金')[['代码', '名称']]
        df3 = ak.fund_etf_category_sina(symbol='封闭式基金')[['代码', '名称']]
        df = pd.concat([df, df2, df3], ignore_index=True, sort=False)
        df = df.rename({'代码': 'code', '名称': 'name'}, axis=1)
        df['_id'] = df['code'].apply(lambda x: int(x[2:]))
        print(df)
        return df

    @staticmethod
    def index_price_daily(code: str, source: str = None) -> pd.DataFrame:
        if source == 'tx':
            df = ak.stock_zh_index_daily_tx(symbol=code)
        elif source == 'em':
            df = ak.stock_zh_index_daily_em(symbol=code)
        else:
            df = ak.stock_zh_index_daily(symbol=code)
        df['date'] = pd.to_datetime(df['date'])
        df = df.rename({'date': '_id'}, axis=1)
        print(df)
        return df

    @staticmethod
    def funds_info() -> pd.DataFrame:
        df = ak.fund_em_fund_name()
        df = df.rename({'基金代码': '_id', '基金简称': 'name', '基金类型': 'type'}, axis=1)
        df['_id'] = df['_id'].apply(lambda x: int(x))
        df['typ2'] = df['type'].apply(lambda x: x.split('-')[1] if '-' in x else None)
        df['type'] = df['type'].apply(lambda x: x.split('-')[0])
        df = df[['_id', 'name', 'type', 'typ2']]
        print(df)
        return df

    @staticmethod
    def fund_nav_daily(code: str) -> pd.DataFrame:
        assert code[0] == 'f'
        code = code[1:]
        df = ak.fund_em_open_fund_info(code, indicator="单位净值走势")
        # print(df)
        df2 = ak.fund_em_open_fund_info(code, indicator="累计净值走势")
        df = pd.merge(df, df2, on='净值日期', how='outer')
        df2 = ak.fund_em_open_fund_info(code, indicator="同类排名百分比")
        # print(df2)
        df2 = df2.rename({'报告日期': '净值日期'}, axis=1)
        df = pd.merge(df, df2, on='净值日期', how='outer')
        df = df.rename({'净值日期': '_id', '单位净值': 'nav', '日增长率': 'growth_rate', '累计净值': 'cum_nav',
                        '同类型排名-每日近3月收益排名百分比': 'rank_3m'}, axis=1)
        if df.dtypes['nav'] != np.dtype('float64'):
            df['nav'] = df['nav'].apply(lambda x: None if x is None else float(x))
        if df.dtypes['cum_nav'] != np.dtype('float64'):
            df['cum_nav'] = df['cum_nav'].apply(lambda x: None if x is None else float(x))
        df['_id'] = pd.to_datetime(df['_id'])
        print(df)
        return df

    @staticmethod
    def managers() -> pd.DataFrame:
        df = ak.fund_manager(explode=True)[['姓名', '现任基金', '累计从业时间']]
        return df.rename({'姓名': 'name', '现任基金': 'fund_name', '累计从业时间': 'work_days'}, axis=1)


def main():
    df = AkData.managers()
    print(df)
    Mongo().save('manager', df)


if __name__ == "__main__":
    main()
