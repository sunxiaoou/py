#! /usr/bin/python3
import argparse
import json
import os

import pandas as pd


import re
import json

uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)


def process_uuid(obj):
    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            if isinstance(value, str) and uuid_pattern.match(value):
                new_dict[key] = None  # 将值设为null
            else:
                new_dict[key] = process_uuid(value)
        return new_dict
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, str) and uuid_pattern.match(item):
                return []  # 将整个列表设为空列表
        return [process_uuid(item) for item in obj]
    else:
        return obj  # 非列表或字典的其他值保持不变


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
        if data is None:
            df = save_to_df('Null', x, y, df)
        elif isinstance(data, str):
            escaped = data.replace('\\', '\\\\').replace('"', '\\"')
            df = save_to_df('"' + escaped + '"', x, y, df)
        else:
            s = str(data)
            if isinstance(data, bool):
                s = s.lower()
            df = save_to_df(s, x, y, df)
        if not last:
            df = save_to_df(',', x + 1, y, df)
    return y + 1, df


def merge_dict(default_dict: dict, subset_dict: dict):
    for key, value in subset_dict.items():
        if isinstance(value, dict) and isinstance(default_dict.get(key), dict):
            merge_dict(default_dict[key], value)
        else:
            default_dict[key] = value


def merge_json(template: str, subset: str, output: str):
    with open(template, 'r') as f:
        default_dict = json.load(f)
        with open(subset, 'r') as f2:
            subset_dict = json.load(f2)
            merge_dict(default_dict, subset_dict)
            with open(output, 'w') as f:
                json.dump(default_dict, f, indent=4)


def json_to_df(json_data: dict) -> pd.DataFrame:
    _, df = traverse_save(json_data, 0, 0, pd.DataFrame(index=range(8), columns=range(8)), True)
    return df


def df_to_json(df: pd.DataFrame) -> dict:
    json_str = ''
    for _, row in df.iterrows():
        row_str = " ".join(['null' if str(cell) == 'Null' else str(cell) for cell in row if pd.notna(cell)])
        json_str += row_str + "\n"
    return json.loads(json_str)


def df_to_excel(df: pd.DataFrame, xlsx: str, sheet: str, overlay=False, header=False):
    if not os.path.exists(xlsx):
        with pd.ExcelWriter(xlsx, engine='openpyxl') as w:
            df.to_excel(w, sheet_name=sheet, index=False, header=header)
        print(f"Created new Excel file with sheet({sheet})")
    elif not overlay:
        with pd.ExcelWriter(xlsx, engine='openpyxl', mode='a') as w:
            if sheet in w.book.sheetnames:
                print(f"Sheet({sheet}) already exists in {xlsx}")
                return
            df.to_excel(w, sheet_name=sheet, index=False, header=header)
            print(f"Added new sheet({sheet}) to file {xlsx}")
    else:
        with pd.ExcelWriter(xlsx, engine='openpyxl', mode='a', if_sheet_exists='overlay') as w:
            df.to_excel(w, sheet_name=sheet, index=False, header=header, startrow=0, startcol=0)
            print(f"Overlap sheet({sheet}) in file {xlsx}")


def excel_to_df(xlsx: str, sheet: str) -> pd.DataFrame:
    return pd.read_excel(xlsx, sheet_name=sheet, header=None)


def json_to_excel(json_file: str, xlsx: str, sheet: str):
    with open(json_file, 'r') as f:
        json_data = json.load(f)
    df_to_excel(json_to_df(json_data), xlsx, sheet, True)
    print(f"Converted {json_file} to sheet({sheet}) in {xlsx}")


def excel_to_json(xlsx: str, sheet: str, template: str, temp_sheet: str, json_file: str):
    json_data = df_to_json(excel_to_df(template, temp_sheet))
    subset = df_to_json(excel_to_df(xlsx, sheet))
    merge_dict(json_data, subset)
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=4)
    print(f"Converted sheet({sheet}) in {xlsx} to {json_file}")


def sort_json(json_file: str, output_file:str):
    with open(json_file, 'r') as f:
        data = json.load(f)
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)


def main():
    parser = argparse.ArgumentParser(description='Convert JSON to Excel or Excel to JSON')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--json2excel', action='store_true', help='Convert JSON to Excel')
    group.add_argument('--excel2json', action='store_true', help='Convert Excel to JSON')
    parser.add_argument('--json', required=True, help='JSON filename')
    parser.add_argument('--excel', required=True, help='Excel filename')
    parser.add_argument('--sheet', required=True, help='Excel sheet name')
    parser.add_argument('--template', required=False, help='Template excel filename')
    parser.add_argument('--t_sheet', required=False, help='Template sheet name')
    args = parser.parse_args()
    if args.json2excel:
        json_to_excel(args.json, args.excel, args.sheet)
    elif args.excel2json:
        excel_to_json(args.excel, args.sheet, args.template, args.t_sheet, args.json)


if __name__ == "__main__":
    main()
