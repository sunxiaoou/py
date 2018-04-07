#! /usr/bin/python3

import openpyxl
wb = openpyxl.load_workbook('example.xlsx')
sheet = wb.get_sheet_by_name('Sheet1')
print(tuple(sheet['A1':'C3']))
