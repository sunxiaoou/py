#! /usr/bin/python3


import openpyxl

wb = openpyxl.load_workbook('example.xlsx')
print(wb.get_sheet_names())
# ['Sheet1', 'Sheet2', 'Sheet3']
sheet = wb.get_sheet_by_name('Sheet3')
print(sheet)
# <Worksheet "Sheet3">
print(type(sheet))
# <class 'openpyxl.worksheet.worksheet.Worksheet'>
print(sheet.title)
# 'Sheet3'
anotherSheet = wb.active
print(anotherSheet)
# <Worksheet "Sheet1">
