#! /usr/bin/python3
from datetime import datetime

import openpyxl
from pymongo import MongoClient


def save_to_spreadsheet(filename: str, date: datetime, result: list):
    titles = ['platform', 'currency', 'code', 'name', 'risk', 'market_value', 'hold_gain',
              'mv_rmb', 'hg_rmb']
    sheet_name = date.strftime('%y-%m-%d')

    try:
        wb = openpyxl.load_workbook(filename)
        sheet = wb[sheet_name]
    except FileNotFoundError:
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = date.strftime('%y-%m-%d')
    except KeyError:
        wb.create_sheet(title=sheet_name)

    row = sheet.max_row
    if row == 1:
        for j in range(len(titles)):
            c = sheet.cell(row=1, column=j+1)
            c.value = titles[j]

    for i in range(len(result)):
        for key in result[i].keys():
            try:
                j = titles.index(key)
                c = sheet.cell(row=row+i+2, column=j+1)
                if key in ['market_value', 'hold_gain', 'mv_rmb', 'hg_rmb']:
                    c.number_format = "#,##,0.00"
                    c.value = result[i][key]
                else:
                    c.value = result[i][key]
            except ValueError:
                pass
        if 'currency' not in result[i].keys():
            j = titles.index('currency')
            sheet.cell(row=row+i+2, column=j+1).value = 'rmb'
        if 'mv_rmb' not in result[i].keys():
            j = titles.index('mv_rmb')
            c = sheet.cell(row=row+i+2, column=j+1)
            c.number_format = "#,##,0.00"
            c.value = result[i]['market_value']
        if 'hg_rmb' not in result[i].keys():
            j = titles.index('hg_rmb')
            c = sheet.cell(row=row+i+2, column=j+1)
            c.number_format = "#,##,0.00"
            c.value = result[i]['hold_gain']
    wb.save(filename)


def save_to_mongo(collection: str, result: list):
    mongo_host = '127.0.0.1'
    mongo_port = 27017
    mongo_db_name = 'finance'

    client = MongoClient(host=mongo_host, port=mongo_port)
    db = client[mongo_db_name]
    collection = db[collection]
    collection.insert_many(result)


def main():
    pass


if __name__ == "__main__":
    main()
