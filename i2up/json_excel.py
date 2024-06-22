#! /usr/bin/python3
import json
import sys

import pandas as pd


def save_df(string: str, x: int, y: int, df: pd.DataFrame) -> pd.DataFrame:
    if y >= len(df):
        df = df.reindex(range(y + 5))
    if x >= len(df.columns):
        df = df.reindex(columns=range(x + 5))
    df.iat[y, x] = string
    # print("save %s at(%d,%d)" % (string, y, x))
    return df


def traverse_save(data, x: int, y: int, df: pd.DataFrame) -> (int, pd.DataFrame):
    if isinstance(data, dict):
        for key, value in data.items():
            df = save_df(key, x, y, df)
            y, df = traverse_save(value, x + 1, y, df)
    elif isinstance(data, list):
        # df = save_df("set", x, y, df)
        for index, item in enumerate(data):
            y, df = traverse_save(item, x, y, df)
    else:
        if isinstance(data, str):
            df = save_df('"' + data + '"', x, y, df)
        else:
            df = save_df(str(data), x, y, df)
        y += 1
    return y, df


def json2excel(json_data: dict, excel: str):
    count, df = traverse_save(json_data, 0, 0, pd.DataFrame(index=range(5), columns=range(5)))
    print("count(%d)" % count)
    print(df)
    df.to_excel(excel, index=False, header=False)


def main():
    if len(sys.argv) < 3:
        print('Usage: {} json_file excel'.format(sys.argv[0]))
        sys.exit(1)
    with open(sys.argv[1], 'r') as file:
        json_data = json.load(file)
    json2excel(json_data, sys.argv[2])


if __name__ == "__main__":
    main()
