#! /usr/bin/python3
import sys

import pandas as pd

pd.set_option('display.max_columns', 6)
# pd.set_option('display.max_rows', 4000)


def get_bones(file: str):
    with open(file) as f:
        text = f.read()
    blocks = text.split('代码')
    lines1 = blocks[1].split('\n')
    l1 = [row.split()[1] for row in lines1[1: -2]]
    lines5 = blocks[5].split('\n')
    l5 = [row.split()[1] for row in lines5[1: -2]]
    lines6 = blocks[6].split('\n')
    l6 = [row.split()[1] for row in lines6[1: -2]]
    l = sorted(list(set(l1 + l5 + l6)))
    print(l)


def get_result(csv: str):
    df = pd.read_csv(csv)
    # print(df)

    # select max value from last 3 columns
    df['max_col_name'] = df.iloc[:, -3:].idxmax(axis=1)
    df['max_value'] = df[df.columns[-4: -1]].max(axis=1)

    df = df.sort_values(by='max_value', ascending=False)
    df.reset_index(drop=True, inplace=True)
    print(df[['name', '115_5', '120_7.5', '125_10', 'max_value', 'max_col_name']])


def main():
    if len(sys.argv) < 2:
        print('Usage: %s file' % format(sys.argv[0]))
        sys.exit(1)

    get_bones(sys.argv[1])


if __name__ == "__main__":
    main()
