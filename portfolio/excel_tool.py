#! /usr/bin/python3
import os

import pandas as pd
from openpyxl import load_workbook


def df_to_sheet(df: pd.DataFrame, xlsx: str, sheet: str, overlay=False, header=True):
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


def duplicate_last_sheet(xlsx: str, sheet: str, row_count: int):
    wb = load_workbook(xlsx)
    last_sheet = wb.worksheets[-1]
    new_sheet = wb.copy_worksheet(last_sheet)
    if row_count < new_sheet.max_row:
        new_sheet.delete_rows(row_count, new_sheet.max_row - 1)
    new_sheet.title = sheet
    wb.active = wb.index(new_sheet)
    wb.save(xlsx)


def main():
    pass


if __name__ == "__main__":
    main()
