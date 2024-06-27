#! /usr/bin/python3
import json

import pandas as pd


def save_to_df(string: str, x: int, y: int, df: pd.DataFrame) -> pd.DataFrame:
    if y >= len(df):
        df = df.reindex(range(y + 5))
    if x >= len(df.columns):
        df = df.reindex(columns=range(x + 5))
    df.iat[y, x] = string
    # print("save %s at(%d,%d)" % (string, y, x))
    return df


def traverse_save(data, x: int, y: int, df: pd.DataFrame, last=False) -> (int, pd.DataFrame):
    if isinstance(data, dict):
        if not data:
            df = save_to_df('{}', x, y, df)
            y += 1
        else:
            df = save_to_df('{', x, y, df)
            y += 1
            # for key, value in data.items():
            for index, (key, value) in enumerate(data.items()):
                df = save_to_df('"' + key + '":', x, y, df)
                if index < len(data) - 1:
                    y, df = traverse_save(value, x + 1, y, df)
                else:
                    y, df = traverse_save(value, x + 1, y, df, last=True)
                df = save_to_df('}' if last else '},', x, y, df)
            y += 1
    elif isinstance(data, list):
        if not data:
            df = save_to_df('[]', x, y, df)
            y += 1
        else:
            df = save_to_df('[', x, y, df)
            y += 1
            for index, item in enumerate(data):
                if index < len(data) - 1:
                    y, df = traverse_save(item, x, y, df)
                else:
                    y, df = traverse_save(item, x, y, df, last=True)
            df = save_to_df(']' if last else '],', x, y, df)
            y += 1
    else:
        if isinstance(data, str):
            df = save_to_df('"' + data + '"', x, y, df)
        else:
            s = str(data)
            if isinstance(data, bool):
                s = s.lower()
            df = save_to_df(s, x, y, df)
        if not last:
            df = save_to_df(',', x + 1, y, df)
        y += 1
    return y, df


def json_to_df(json_data: dict) -> pd.DataFrame:
    _, df = traverse_save(json_data, 0, 0, pd.DataFrame(index=range(8), columns=range(8)), True)
    return df


def df_to_json(df: pd.DataFrame) -> dict:
    json_str = ''
    for _, row in df.iterrows():
        row_str = " ".join([str(cell) for cell in row if pd.notna(cell)])
        json_str += row_str + "\n"
    return json.loads(json_str)


def main():
    pass


if __name__ == "__main__":
    main()
