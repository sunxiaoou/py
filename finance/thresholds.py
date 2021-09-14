#! /usr/bin/python3
import re
import sys
from pprint import pprint

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

columns = ['名称', '代码', '参考指标', '低估', '高估', '最高', '最低']
thresholds = [
    ('上证红利', '000015', '盈利收益率', 10, 6.40, 2.27, 17.50),
    ('50AH优选', '950090', '盈利收益率', 10, 6.40, 2.22, 16.60),
    ('基本面50', '000925', '盈利收益率', 10, 6.40, 2.22, 16.60),
    ('央视50', '399550', '盈利收益率', 10, 6.40, 2.50, 16.60),
    ('中证红利', '000922', '盈利收益率', 10, 6.40, 1.60, 16.60),
    ('300价值', '000919', '盈利收益率', 10, 6.40, 2.22, 16.60),
    ('上证50', '000016', '盈利收益率', 10, 6.40, 2.22, 14.50),
    ('上证180', '000010', '盈利收益率', 10, 6.40, 2.17, 13.90),
    ('H股指数', 'HSCEI', '盈利收益率', 10, 6.40, 3.45, 17.50),
    ('恒生指数', 'HSI', '盈利收益率', 10, 6.40, 4.76, 14.50),

    ('银行行业', '399986', '市净率', 0.9, 1.15, 1.4, 0.75),
    ('地产行业', '399393', '市净率', 1.6, 2.2, 4, 1.2),
    ('证券行业', '399975', '市净率', 1.6, 2.2, 4.8, 1.05),
    ('军工行业', '399967', '市净率', 2.6, 4, 9.2, 2.1),
    ('环保行业', '000827', '市净率', 2.3, 3, 5.9, 1.82),
    ('基建行业', '399995', '市净率', 1.1, 1.8, 3.6, 0.92),
    ('建筑材料', '931009', '市净率', 1.8, 2.1, 3.1, 1.4),

    # ('中证全指', '000985', '市盈率', 14, 21, 54, 11),
    ('红利机会', 'CSPSADRP', '市盈率', 13, 20, 30, 8),
    ('500低波动', '930782', '市盈率', 24, 30, 60, 17),
    ('500增强', '000905', '市盈率', 25, 40, 93, 17),
    ('沪深300', '000300', '市盈率', 11, 17, 49, 8),
    ('中证养老', '399812', '市盈率', 21, 27, 36, 17),
    ('创业板', '399006', '市盈率', 25, 45, 138, 27),
    ('深证100', '399330', '市盈率', 18, 24, 64, 12),
    ('医药100', '000978', '市盈率', 28, 36, 63, 23),
    ('中证医疗', '399989', '市盈率', 55, 75, 140, 32),
    ('生物科技', '930743', '市盈率', 57, 81, 135, 33),
    ('中证消费', '000932', '市盈率', 30, 40, 53, 17),
    ('中证白酒', '399997', '市盈率', 30, 40, 71, 15),
    ('食品饮料', '930653', '市盈率', 30, 40, 65, 18),
    ('可选消费', '000989', '市盈率', 18, 26, 45, 15),
    # ('可选消费', '686000', '市净率', 2.2, 4, 5.3, 1.7),
    ('消费红利', 'H30094', '市盈率', 25, 33, 45, 11),
    ('消费龙头', '931068', '市盈率', 24, 32, 45, 16),
    ('沪港深消费50', '931357', '市盈率', 33, 42, 56, 25),
    ('深证成指', '399001', '市盈率', 15, 30, 62, 11),
    ('基本面60', '399701', '市盈率', 17, 20, 60, 12),
    ('基本面120', '399702', '市盈率', 18, 22, 60, 13),
    ('深红利', '399324', '市盈率', 15, 22, 44, 11),
    ('纳斯达克100', 'NDX', '市盈率', 20, 30, 85, 15),
    ('标普500', 'SPX', '市盈率', 15, 25, 44, 5.8),
    ('标普科技', 'S5INFT', '市盈率', 21, 30, 90, 15),
    ('美股消费', 'IXY', '市盈率', 21, 30, 45, 15),
    ('全球医疗', 'SPG120035', '市盈率', 21, 30, 45, 15),
    ('香港中小', 'SPHCMSHP', '市盈率', 12, 17, 20, 8.4),
    ('中概互联', 'H30533', '市销率', 5.6, 8, 12.8, 3.47),
    ('A股龙头', 'HSCAIT', '市盈率', 11, 13, 15, 8),
    ('竞争力指数', '931142', '市盈率', 13, 18, 23, 10),
    ('MSCI质量', '707717', '市盈率', 26, 38, 55, 17),
    ('科创50', '000688', '市盈率', 50, 80, 100, 55),
    ('家用电器', '930697', '市盈率', 17, 20, 28, 12)]


def is_number(s: str) -> bool:
    if re.match("^\d+\.?\d+?$", s) is None:
        return s.isdigit()
    return True


def parse(l: list) -> list:
    date = l[3]
    valuations = []
    i = 0
    while l[i] != date:
        i += 1
    while True:
        while l[i] != "场外代码":
            i += 1
        i += 1
        while True:
            k = l[i]
            if k == '美股优秀行业进入绿色是进入到估值中枢以下':
                return valuations
            i += 1
            while not is_number(l[i]):
                k += l[i]
                i += 1
            if k.startswith('中概互联'):
                k = '中概互联'
            v = l[i]
            i += 1
            if v == date:
                break
            valuations.append((k, float(v)))
            while is_number(l[i]):
                i += 1


def to_lowest(row: pd.Series) -> float:
    val, lowest, low = row['当日'], row['最低'], row['低估']
    if row['参考指标'] == '盈利收益率':
        if val < low:
            return None
    elif val > low:
        return None
    return round((lowest - val) / (lowest - low), 4)


def to_low(row: pd.Series) -> float:
    val, low, high = row['当日'], row['低估'], row['高估']
    if row['参考指标'] == '盈利收益率':
        if val >= low or val <= high:
            return None
    elif val <= low or val >= high:
        return None
    return round((low - val) / (low - high), 4)


def to_high(row: pd.Series) -> float:
    val, high, highest = row['当日'], row['高估'], row['最高']
    if row['参考指标'] == '盈利收益率':
        if val > high:
            return None
    elif val < high:
        return None
    return round((high - val) / (high - highest), 4)


def calculate_thresholds(vals: list) -> pd.DataFrame:
    df = pd.DataFrame(thresholds, columns=columns)
    # print(df)
    df2 = pd.DataFrame(vals, columns=['名称', '当日'])
    # print(df2)
    df = pd.merge(df, df2, on='名称')
    df['距最低'] = df.apply(to_lowest, axis=1)
    df['距低估'] = df.apply(to_low, axis=1)
    df['距正常'] = df.apply(to_high, axis=1)
    df = df.sort_values(by=['距最低', '距低估', '距正常'])
    return df.reset_index(drop=True)


def to_excel(xlsx: str, sheet: str, df: pd.DataFrame):
    wb = load_workbook(xlsx)
    writer = pd.ExcelWriter(xlsx, engine='openpyxl')
    writer.book = wb
    writer.sheets = {worksheet.title: worksheet for worksheet in wb.worksheets}
    df.to_excel(writer, sheet_name=sheet, index=False)
    writer.save()

    wb = load_workbook(xlsx)
    ws = wb[sheet]
    last_row = ws.max_row
    last_col = ws.max_column
    for i in range(2, last_row + 1):
        for j in range(4, 9):
            ws.cell(row=i, column=j).number_format = '#,##,0.00'
        for j in range(9, last_col + 1):
            ws.cell(row=i, column=j).number_format = '0.00%'

    colors = ['99CC00', 'FFCC00', 'FF6600']
    i = 1
    for k in range(9, 12):
        fill = PatternFill(patternType='solid', fgColor=colors[k - 9])
        while ws.cell(row=i, column=k).value is not None:
            for j in range(1, last_col + 1):
                ws.cell(row=i, column=j).fill = fill
            i += 1

    wb.save(xlsx)


def main():
    if len(sys.argv) < 2:
        print('Usage: {} txt'.format(sys.argv[0]))
        print('       {} txt xlsx'.format(sys.argv[0]))
        sys.exit(1)

    with open(sys.argv[1]) as fp:
        lines = [line.rstrip('%\n') for line in fp.readlines()]

    date = lines[3]
    df = calculate_thresholds(parse(lines))
    df.rename(columns={'当日': date}, inplace=True)
    print(df)

    if len(sys.argv) > 2:
        to_excel(sys.argv[2], date, df)


if __name__ == "__main__":
    main()
