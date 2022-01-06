#! /usr/bin/python3

import sys
from pprint import pprint

import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string

pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', 100)


def get_bones(xlsx: str) -> pd.DataFrame:
    wb = load_workbook(xlsx, data_only=True)
    # ws = wb['激进轮动可转债']
    ws = wb['可转债排名']
    # col = column_index_from_string('J')
    for col in range(1, 20):
        c = ws.cell(row=1, column=col)
        if c.value == '转债代码':
            break
    lst = []
    for i in range(2, ws.max_row):
        c = ws.cell(row=i, column=col)
        if c.value is None:
            break
        code = str(c.value)
        name = ws.cell(row=i, column=col + 1).value
        rank = ws.cell(row=i, column=col + 2).value
        rank_170 = ws.cell(row=i, column=col + 3).value
        rank_130 = ws.cell(row=i, column=col + 4).value
        nav = ws.cell(row=i, column=col + 5).value
        quote_change = '{0:.2%}'.format(ws.cell(row=i, column=col + 6).value)
        comment = ws.cell(row=i, column=col + 7).value
        lst.append((code, name, rank, rank_170, rank_130, nav, quote_change, comment))
    columns = ['code', 'name', 'rank', 'rank_170', 'rank_130', 'nav', 'quote_change', 'comment']
    df = pd.DataFrame(lst, columns=columns)
    # df['rank_130'] = df['rank_130'].apply(lambda x: int(x) if pd.notna(x) else x)
    # df = df.set_index('rank')
    # df.index.name = None
    return df


def get_my_list(xlsx: str) -> pd.DataFrame:
    wb = load_workbook(xlsx, data_only=True)
    ws = wb.worksheets[-1]
    lst = []
    for i in range(1, ws.max_row):
        if ws.cell(row=i, column=1).value == '银河' and ws.cell(row=i, column=4).value.endswith('转债'):
            lst.append((ws.cell(row=i, column=3).value, ws.cell(row=i, column=4).value))
    return pd.DataFrame(lst, columns=['code', 'name'])


def main():
    if len(sys.argv) < 2:
        print('Usage: {} xlsx'.format(sys.argv[0]))
        sys.exit(1)

    mine = get_my_list('asset.xlsx')

    xlsx = sys.argv[1]
    bones = get_bones(xlsx)
    print('无阈值排名(截止到<170的第20名)')
    df = bones.loc[bones['rank_170'] == 20]
    r = df.iloc[0, df.columns.get_loc('rank')]
    radical = bones[bones['rank'] <= r]
    print(radical)

    inner = pd.merge(radical, mine, on=['code', 'name'])
    print('已持有的激进转债({})'.format(len(inner)))
    print(inner)

    to_buy = radical.append(inner).drop_duplicates(keep=False)
    to_buy = to_buy[to_buy['nav'] < 170]
    print('未持有的<170的激进转债({})'.format(len(to_buy)))
    print(to_buy)

    to_sell = mine.append(inner[['code', 'name']]).drop_duplicates(keep=False)
    print('持有的非激进转债({})'.format(len(to_sell)))
    print(to_sell)


if __name__ == "__main__":
    main()
