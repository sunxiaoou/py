#! /usr/bin/python3
import json

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
import pandas as pd
# import pymysql

pd.set_option('display.max_rows', 4000)
# pd.set_option('display.max_columns', 6)


class MySql:
    def __init__(self, host='localhost', port=3306, user='manga', password='manga', database='portfolio'):
        self.db = create_engine('mysql+pymysql://%s:%s@%s:%s/%s' % (user, password, host, port, database))

    # def close(self):
    #     self.db.close()

    def last_row(self, table: str, column: str) -> dict:
        metadata = MetaData(self.db)
        tab = Table(table, metadata, autoload=True)
        columns = [c.name for c in tab.columns]
        # print(columns)
        query = 'SELECT * FROM %s ORDER BY %s DESC LIMIT 1' % (table, column)
        values = self.db.execute(query).fetchone()
        # print(values)
        return dict(zip(columns, values))

    def insert(self, table: str, row: dict):
        session = sessionmaker(bind=self.db)()
        val_str = ', '.join(["'{}'".format(x) if isinstance(x, str) else str(x) for x in row.values()])
        stmt = 'INSERT INTO %s (%s) VALUES (%s)' % (table, ', '.join(row.keys()), val_str)
        print(stmt)
        session.execute(stmt)
        session.commit()

    def to_frame(self, table: str, fields: list = None) -> pd.DataFrame:
        s = ','.join(fields) if fields else '*'
        return pd.read_sql('select %s from %s' % (s, table), self.db)

    def from_frame(self, table: str, frame: pd.DataFrame):
        frame.to_sql(table, con=self.db, if_exists='append', index=False)


def threshold() -> pd.DataFrame:
    with open('threshold.json') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['代码'] = df['代码'].apply(lambda x: 'C' + x if x.isnumeric() else x)
    df = df.rename({'_id': 'name', '代码': 'code', '参考指标': 'reference', '最低': 'lowest', '低估': 'low',
                    '高估': 'high', '最高': 'highest', '场内代码': 'onsite', '场外代码': 'offsite'}, axis=1)
    # print(df.columns)
    return df


def valuation() -> pd.DataFrame:
    dic = {
        '_id': 'timestamp',
        '上证180': 'C000010',
        '上证红利': 'C000015',
        '上证50': 'C000016',
        '沪深300': 'C000300',
        '科创50': 'C000688',
        '环保行业': 'C000827',
        '中证1000': 'C000852',
        '中证100': 'C000903',
        '500增强': 'C000905',
        '中证800': 'C000906',
        '300价值': 'C000919',
        '中证红利': 'C000922',
        '基本面50': 'C000925',
        '中证消费': 'C000932',
        '医药100': 'C000978',
        '可选消费': 'C000989',
        '深证成指': 'C399001',
        '创业板': 'C399006',
        '深红利': 'C399324',
        '深证100': 'C399330',
        '地产行业': 'C399393',
        '央视50': 'C399550',
        '基本面60': 'C399701',
        '基本面120': 'C399702',
        '中证养老': 'C399812',
        '军工行业': 'C399967',
        '证券行业': 'C399975',
        '银行行业': 'C399986',
        '中证医疗': 'C399989',
        '基建行业': 'C399995',
        '中证白酒': 'C399997',
        'MSCI质量': 'C707717',
        '食品饮料': 'C930653',
        '家用电器': 'C930697',
        '生物科技': 'C930743',
        '500低波动': 'C930782',
        '建筑材料': 'C931009',
        '消费龙头': 'C931068',
        '竞争力指数': 'C931142',
        '科技100': 'C931187',
        '沪港深消费50': 'C931357',
        '50AH优选': 'C950090',
        '红利机会': 'CSPSADRP',
        '消费红利': 'H30094',
        '中概互联': 'H30533',
        'A股龙头': 'HSCAIT',
        'H股指数': 'HSCEI',
        '恒生指数': 'HSI',
        '恒生科技': 'HSTECH',
        '美股消费': 'IXY',
        '纳斯达克100': 'NDX',
        '标普科技': 'S5INFT',
        '全球医疗': 'SPG120035',
        '香港中小': 'SPHCMSHP',
        '标普500': 'SPX',
    }

    with open('valuation.json') as f:
        data = json.load(f)
    val = pd.DataFrame(data)
    val = val[dic.keys()]
    val = val.rename(dic, axis=1)

    with open('sh000985.json') as f:
        data = json.load(f)
    sh = pd.DataFrame(data)
    sh = sh[['_id', 'close', 'star']]
    sh = sh.rename({'_id': 'timestamp', 'close': 'sh000985'}, axis=1)

    df = pd.merge(val, sh, on='timestamp')
    df['timestamp'] //= 1000
    df['timestamp'] -= 3600 * 8
    return df


def main():
    # df = threshold()
    # print(df['code'])
    # df = valuation()
    # print(df.columns)
    # print(df)
    # db = MySql(database='portfolio')
    # db.from_frame('valuation', df)
    # # df = db.to_frame('instant_price')
    # df = db.to_frame('instant_price', ['code', 'price'])
    db = MySql(database='portfolio')
    print(db.last_row('valuation', 'timestamp'))
    # db = MySql(database='manga')
    # db.insert('export', {'export_id': 27, 'name': '费沙自治领'})


if __name__ == "__main__":
    main()
