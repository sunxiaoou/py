#! /usr/bin/python3
import argparse
import json
import os

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
            if not last:
                df = save_to_df(',', x + 1, y, df)
        else:
            df = save_to_df('{', x, y, df)
            y += 1
            for index, (key, value) in enumerate(data.items()):
                df = save_to_df('"' + key + '":', x, y, df)
                if index < len(data) - 1:
                    y, df = traverse_save(value, x + 1, y, df)
                else:
                    y, df = traverse_save(value, x + 1, y, df, last=True)
                df = save_to_df('}' if last else '},', x, y, df)
    elif isinstance(data, list):
        if not data:
            df = save_to_df('[]', x, y, df)
            if not last:
                df = save_to_df(',', x + 1, y, df)
        else:
            df = save_to_df('[', x, y, df)
            y += 1
            for index, item in enumerate(data):
                if index < len(data) - 1:
                    y, df = traverse_save(item, x, y, df)
                else:
                    y, df = traverse_save(item, x, y, df, last=True)
            df = save_to_df(']' if last else '],', x, y, df)
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
    return y + 1, df


def json_to_df(json_data: dict) -> pd.DataFrame:
    _, df = traverse_save(json_data, 0, 0, pd.DataFrame(index=range(8), columns=range(8)), True)
    return df


def df_to_json(df: pd.DataFrame) -> dict:
    json_str = ''
    for _, row in df.iterrows():
        row_str = " ".join(['null' if str(cell) == 'None' else str(cell) for cell in row if pd.notna(cell)])
        json_str += row_str + "\n"
    return json.loads(json_str)


def df_to_excel(df: pd.DataFrame, xlsx: str, sheet: str, overwrite=False):
    if not os.path.exists(xlsx):
        with pd.ExcelWriter(xlsx, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet, index=False, header=False)
        print(f"Created new Excel file with sheet({sheet})")
    else:
        with pd.ExcelWriter(xlsx, engine='openpyxl', mode='a') as writer:
            if sheet in writer.book.sheetnames:
                if not overwrite:
                    print(f"Sheet({sheet}) already exists in {xlsx}")
                    return
                del writer.book[sheet]
                print(f"Deleted original sheet({sheet}) in {xlsx}")
            df.to_excel(writer, sheet_name=sheet, index=False, header=False)
            print(f"Added new sheet({sheet}) to file: {xlsx}")


def excel_to_df(xlsx: str, sheet: str) -> pd.DataFrame:
    return pd.read_excel(xlsx, sheet_name=sheet, header=None)


def json_to_excel(json_file: str, xlsx: str, sheet: str):
    with open(json_file, 'r') as f:
        json_data = json.load(f)
    df_to_excel(json_to_df(json_data), xlsx, sheet, True)
    print(f"Converted {json_file} to sheet({sheet}) in {xlsx}")


def excel_to_json(xlsx: str, sheet: str, json_file: str):
    json_data = df_to_json(excel_to_df(xlsx, sheet))
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=4)
    print(f"Converted sheet({sheet}) in {xlsx} to {json_file}")


def main():
    parser = argparse.ArgumentParser(description='Convert JSON to Excel or Excel to JSON')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--json-to-excel', action='store_true', help='Convert JSON to Excel')
    group.add_argument('--excel-to-json', action='store_true', help='Convert Excel to JSON')
    parser.add_argument('--json-file', required=True, help='JSON filename')
    parser.add_argument('--excel-file', required=True, help='Excel filename')
    parser.add_argument('--excel-sheet', required=True, help='Excel sheet')
    args = parser.parse_args()
    if args.json_to_excel:
        json_to_excel(args.json_file, args.excel_file, args.excel_sheet)
    elif args.excel_to_json:
        excel_to_json(args.excel_file, args.excel_sheet, args.json_file)


if __name__ == "__main__":
    main()
