#! /usr/bin/python3

import sys
from pprint import pprint

import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string

columns = ['rank', 'code', 'name']


def get_radical_bones(xlsx: str) -> pd.DataFrame:
    wb = load_workbook(xlsx, data_only=True)
    ws = wb['激进轮动可转债']
    col = column_index_from_string('J')
    lst = []
    for i in range(2, ws.max_row):
        c = ws.cell(row=i, column=col + 2)
        if c.value is None:
            break
        if float(ws.cell(row=i, column=col + 3).value) < 170:
            lst.append((c.value, str(ws.cell(row=i, column=col).value), ws.cell(row=i, column=col + 1).value))
    return pd.DataFrame(lst, columns=columns)


def get_low2_bones(xlsx: str) -> pd.DataFrame:
    wb = load_workbook(xlsx, data_only=True)
    ws = wb['轮动可转债']
    col = column_index_from_string('K')
    lst = []
    for i in range(2, ws.max_row):
        c = ws.cell(row=i, column=col + 2)
        if c.value is None:
            break
        lst.append((c.value, str(ws.cell(row=i, column=col).value), ws.cell(row=i, column=col + 1).value))
    return pd.DataFrame(lst, columns=columns)


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

    xlsx = sys.argv[1]
    low2 = get_low2_bones(xlsx)
    print('轮动可转债')
    print(low2)
    print('激进轮动可转债')
    radical = get_radical_bones(xlsx)
    print(radical)

    mine = get_my_list('asset.xlsx')

    inner = pd.merge(radical, mine, on=['code', 'name'])
    print('已持有的激进转债({})'.format(len(inner)))
    print(inner)

    diff = radical.append(inner).drop_duplicates(keep=False)
    print('未持有的激进转债({})'.format(len(diff)))
    print(diff)

    diff2 = mine.append(inner[['code', 'name']]).drop_duplicates(keep=False)
    print('持有的非激进转债({})'.format(len(diff2)))
    print(diff2)

    inner2 = pd.merge(low2, diff2, on=['code', 'name'])
    diff3 = diff2.append(inner2[['code', 'name']]).drop_duplicates(keep=False)
    print('持有的非激进或双低转债({})'.format(len(diff2)))
    print(diff3)

if __name__ == "__main__":
    main()
