#! /usr/bin/python3
import sys

import pandas as pd
from openpyxl import load_workbook

from grid import Grid


def gridPlus(xlsx: str, sheet: str):
    wb = load_workbook(xlsx)
    if not sheet:
        sheet = wb.worksheets[-1].title
    df = pd.read_excel(xlsx, sheet_name=sheet)
    # df.iloc[:, 0] = df.iloc[:, 0].fillna(method='ffill')
    df.iloc[:, 0] = df.iloc[:, 0].ffill()
    df['网格'] = df['底格'].astype(str) + '_' + df['顶格'].astype(str) + '_5_1'
    df['名称'] = df.apply(lambda row: row['代码'] if row.iloc[0] == '海外' else row['标的'], axis=1)
    df = df[['网格', '名称']]
    # print(df)
    tuples = list(df.itertuples(index=False, name=None))
    for t in tuples:
        print(Grid.make(t[0], t[1]))

def usage():
    print('Usage: %s xlsx [sheet]' % sys.argv[0])
    sys.exit(1)

def main():
    if len(sys.argv) > 1:
        if not sys.argv[1].endswith('.xlsx'):
            usage()
        xlsx = sys.argv[1]
        if len(sys.argv) > 2:
            sheet = sys.argv[2]
        else:
            sheet = None
    else:
        usage()
    gridPlus(xlsx, sheet)


if __name__ == "__main__":
    main()
