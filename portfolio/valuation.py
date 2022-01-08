#! /usr/bin/python3
import os
import re
import sys
from datetime import datetime
from pprint import pprint

import pandas as pd
import pyperclip
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

from mongo import Mongo

INDEXES = [
    # PB
    '银行行业', '地产行业', '证券行业', '军工行业', '环保行业', '基建行业', '建筑材料',
    # EP
    '上证红利', '50AH优选', '基本面50', '央视50', '中证红利', '300价值', '上证50', '上证180', 'H股指数', '恒生指数',
    # PE
    '中证100', '沪深300', '中证500', '500增强', '500低波动', '中证1000', '红利机会', '中证养老',
    '创业板', '深证100', '医药100', '中证医疗', '生物科技', '科技100', '中证消费', '中证白酒', '食品饮料',
    '可选消费', '消费红利', '消费龙头', '消费50', '沪港深消费50', '深证成指', '基本面60', '基本面120', '深红利',
    '纳斯达克100', '标普500', '标普科技', '美股消费', '全球医疗', '香港中小', '中概互联', '恒生科技',
    'A股龙头', '竞争力指数', 'MSCI质量', '科创50', '家用电器',
    # other
    '美国房地产', '十年期国债', '10年期国债（A股）', '10年期国债（美股）'
]

COLUMNS = ['代码', '_id', '参考指标', '最低', '低估', '高估', '最高']
THRESHOLDS = [
    ('000015', '上证红利', '盈利收益率', 17.5, 10, 6.4, 2.27),
    ('950090', '50AH优选', '盈利收益率', 16.6, 10, 6.4, 2.22),
    ('000925', '基本面50', '盈利收益率', 16.6, 10, 6.4, 2.22),
    ('399550', '央视50', '盈利收益率', 16.6, 10, 6.4, 2.5),
    ('000922', '中证红利', '盈利收益率', 16.6, 10, 6.4, 1.6),
    ('000919', '300价值', '盈利收益率', 16.6, 10, 6.4, 2.22),
    ('000016', '上证50', '盈利收益率', 14.5, 10, 6.4, 2.22),
    ('000010', '上证180', '盈利收益率', 13.9, 10, 6.4, 2.17),
    ('HSCEI', 'H股指数', '盈利收益率', 17.5, 10, 6.4, 3.45),
    ('HSI', '恒生指数', '盈利收益率', 14.5, 10, 6.4, 4.76),

    ('399986', '银行行业', '市净率', 0.75, 0.9, 1.15, 1.4),
    ('399393', '地产行业', '市净率', 1.2, 1.6, 2.2, 4),
    ('399975', '证券行业', '市净率', 1.05, 1.6, 2.2, 4.8),
    ('399967', '军工行业', '市净率', 2.1, 2.6, 4, 9.2),
    ('000827', '环保行业', '市净率', 1.82, 2.3, 3, 5.9),
    ('399995', '基建行业', '市净率', 0.92, 1.1, 1.8, 3.6),
    ('931009', '建筑材料', '市净率', 1.4, 1.8, 2.1, 3.1),

    # ('000985', '中证全指', '市盈率', 11, 14, 21, 54),
    ('000903', '中证100', '市盈率', 7, 11, 15, 45),
    ('000300', '沪深300', '市盈率', 8, 11, 17, 49),
    ('930782', '500低波动', '市盈率', 17, 24, 30, 60),
    ('000905', '500增强', '市盈率', 17, 25, 40, 93),
    ('000852', '中证1000', '市盈率', 19, 35, 48, 145),
    ('CSPSADRP', '红利机会', '市盈率', 8, 13, 20, 30),
    ('399812', '中证养老', '市盈率', 17, 21, 27, 36),
    ('399006', '创业板', '市盈率', 27, 25, 45, 138),
    ('399330', '深证100', '市盈率', 12, 18, 24, 64),
    ('000978', '医药100', '市盈率', 23, 28, 36, 63),
    ('399989', '中证医疗', '市盈率', 32, 55, 75, 140),
    ('930743', '生物科技', '市盈率', 33, 57, 81, 135),
    # ('931152', '创新药', '市盈率', 29, 50, 70, 130),
    ('931187', '科技100', '市盈率', 18, 26, 40, 56),
    ('000932', '中证消费', '市盈率', 17, 30, 40, 53),
    ('399997', '中证白酒', '市盈率', 15, 30, 40, 71),
    ('930653', '食品饮料', '市盈率', 18, 30, 40, 65),
    ('000989', '可选消费', '市盈率', 15, 18, 26, 45),
    # ('686000', '可选消费', '市净率', 1.7, 2.2, 4, 5.3),
    ('H30094', '消费红利', '市盈率', 11, 25, 33, 45),
    ('931068', '消费龙头', '市盈率', 16, 24, 32, 45),
    ('931357', '沪港深消费50', '市盈率', 25, 33, 42, 56),
    ('399001', '深证成指', '市盈率', 11, 15, 30, 62),
    ('399701', '基本面60', '市盈率', 12, 17, 20, 60),
    ('399702', '基本面120', '市盈率', 13, 18, 22, 60),
    ('399324', '深红利', '市盈率', 11, 15, 22, 44),
    ('NDX', '纳斯达克100', '市盈率', 15, 20, 30, 85),
    ('SPX', '标普500', '市盈率', 5.8, 15, 25, 44),
    ('S5INFT', '标普科技', '市盈率', 15, 21, 30, 90),
    ('IXY', '美股消费', '市盈率', 15, 21, 30, 45),
    ('SPG120035', '全球医疗', '市盈率', 15, 21, 30, 45),
    ('SPHCMSHP', '香港中小', '市盈率', 8.4, 12, 17, 20),
    ('H30533', '中概互联', '市销率', 3.74, 5.6, 8, 12.8),
    ('HSTECH', '恒生科技', '市销率', 3.2, 4, 5.6, 9),
    ('HSCAIT', 'A股龙头', '市盈率', 8, 11, 13, 15),
    ('931142', '竞争力指数', '市盈率', 10, 13, 18, 23),
    ('707717', 'MSCI质量', '市盈率', 17, 26, 38, 55),
    ('000688', '科创50', '市盈率', 55, 50, 80, 100),
    ('930697', '家用电器', '市盈率', 12, 17, 20, 28)]


def parse_fund_code(file: str) -> list:
    with open(file) as f:
        lines = []
        for l in f.readlines():
            lines += l.rstrip('\n').split()

    reg_date = re.compile(r'20\d{6}')
    result = []
    try:
        i = 0
        # while True:
        while reg_date.search(lines[i]) is None:
            i += 1
        date = reg_date.search(lines[i]).group()
        # print(date)
        i += 1
        while True:
            while lines[i] not in INDEXES and not lines[i].startswith('中概互联') \
                    and not lines[i].startswith('恒生科技'):
                if lines[i].startswith('永续A') or lines[i].startswith('注'):
                    i += 1
                    break
                i += 1
            else:
                if lines[i].startswith('中概互联'):
                    key = '中概互联'
                elif lines[i].startswith('恒生科技'):
                    key = '恒生科技'
                else:
                    key = lines[i]
                if key == '中概互联':
                    if lines[i + 1] == '513050':            # there is no value
                        i += 2
                        continue
                    if lines[i + 1].startswith('市销率'):
                        i += 1
                elif key == '十年期国债':
                    key = '10年期国债（A股）'
                i += 1
                while re.search(r'\d{6}', lines[i]) is None:
                    i += 1
                on, off = lines[i], None
                i += 1
                if re.search(r'\d{6}', lines[i]):
                    off = (lines[i])
                    i += 1
                elif key not in ['上证红利', '科创50']:
                    off, on = on, None
                # print(key, on, off)
                result.append((key, on, off))
    except IndexError:
        pass
    return result


def save_thresholds(file: str):
    df = pd.DataFrame(THRESHOLDS, columns=COLUMNS)
    df2 = pd.DataFrame(parse_fund_code(file), columns=['_id', '场内代码', '场外代码'])
    df = pd.merge(df, df2, on='_id')
    print(df)
    # Mongo().save('threshold', df)


def parse_valuations(file: str) -> list:
    if not os.path.isfile(file):
        with open(file, 'w') as fp:
            fp.write(pyperclip.paste())

    with open(file) as f:
        lines = []
        for l in f.readlines():
            lines += l.rstrip('\n').split()

    reg_date = re.compile(r'20\d{6}')
    result = []
    try:
        i = 0
        while True:
            while reg_date.search(lines[i]) is None:
                i += 1
            date = reg_date.search(lines[i]).group()
            # print(date)
            dic = {'_id': date}
            i += 1
            while True:
                while lines[i] not in INDEXES and not lines[i].startswith('中概互联') \
                        and not lines[i].startswith('恒生科技'):
                    if lines[i].startswith('永续A') or lines[i].startswith('注'):
                        i += 1
                        break
                    i += 1
                else:
                    if lines[i].startswith('中概互联'):
                        key = '中概互联'
                    elif lines[i].startswith('恒生科技'):
                        key = '恒生科技'
                    else:
                        key = lines[i]
                    if key == '中概互联':
                        if lines[i + 1] == '513050':            # there is no value
                            i += 2
                            continue
                        if lines[i + 1].startswith('市销率'):
                            i += 1
                    elif key == '十年期国债':
                        key = '10年期国债（A股）'
                    i += 1
                    while lines[i] == '*':
                        i += 1
                    value = re.search(r'[\d.]+', lines[i]).group(0)
                    if key == '300价值' and value == lines[i]:
                        value = round(100 / float(value), 2)        # as 300价值 used PE before 20100225
                    else:
                        value = float(value)
                    i += 1
                    # print(key, value)
                    dic[key] = value
                    continue
                break               # break out of multiple loops as encountered '注：'
            result.append(dic)
    except IndexError:
        pass
    return result


def check(valuations: list):
    cur = {'_id'}
    for valuation in valuations:
        date = valuation['_id']
        s = set(valuation.keys())
        if cur == s:
            continue
        a = s - cur
        if a:
            print("{} add {}".format(date, a))
            cur |= a
        d = cur - s
        if d:
            print("{} missing {}".format(date, d))


def save_valuations(file: str):
    valuations = parse_valuations(file)
    check(valuations)
    # pprint(valuations)
    # for date, valuation in valuations:
    #     if '300价值' in valuation:
    #         print(date, valuation['300价值'])

    print(len(valuations))
    df = pd.DataFrame(valuations)
    df['_id'] = pd.to_datetime(df['_id'])
    print(df)
    # Mongo().save('valuation', df)


def update_valuations(xlsx: str):
    mongo = Mongo()
    ms = mongo.find_last('valuation')['_id']
    start = datetime.fromtimestamp(ms / 1000.0).strftime('%Y%m%d')

    wb = load_workbook(xlsx)
    wss = [ws.title for ws in wb.worksheets]
    excel = pd.ExcelFile(xlsx)
    valuations = []
    for ws in wss:
        if not re.search(r'20\d{6}$', ws) or ws <= start:
            continue
        df = pd.read_excel(excel, ws)
        dic = dict(zip(df['名称'].tolist(), df[ws].tolist()))
        dic['_id'] = ws
        valuations.append(dic)

    print(len(valuations))
    if not valuations:
        return
    # the valuation hasn't ('中证500', '美国房地产', '10年期国债（美股）', '10年期国债（A股）', '消费50')
    df = pd.DataFrame(valuations)
    df['_id'] = pd.to_datetime(df['_id'])
    print(df)
    mongo.save('valuation', df)


def to_lowest(row: pd.Series) -> float:
    val, lowest, low = row.iat[7], row['最低'], row['低估']
    if row['参考指标'] == '盈利收益率':
        if val < low:
            return None
    elif val > low:
        return None
    return round((lowest - val) / (lowest - low), 4)


def to_lowest2(row: pd.Series) -> float:
    val, lowest, low = row.iat[7], row['最低'], row['低估']
    if row['参考指标'] == '盈利收益率':
        if val < low:
            return None
        return round((val - lowest) / val, 4)
    if val > low:
        return None
    return round((lowest - val) / val, 4)


def to_low(row: pd.Series) -> float:
    val, low, high = row.iat[7], row['低估'], row['高估']
    if row['参考指标'] == '盈利收益率':
        if val >= low or val <= high:
            return None
    elif val <= low or val >= high:
        return None
    return round((low - val) / (low - high), 4)


def to_low2(row: pd.Series) -> float:
    val, low, high = row.iat[7], row['低估'], row['高估']
    if row['参考指标'] == '盈利收益率':
        if val <= high:
            return None
        return round((val - low) / val, 4)
    if val >= high:
        return None
    return round((low - val) / val, 4)


def to_high(row: pd.Series) -> float:
    val, high, highest = row.iat[7], row['高估'], row['最高']
    if row['参考指标'] == '盈利收益率':
        if val > high:
            return None
    elif val < high:
        return None
    return round((high - val) / (high - highest), 4)


def to_high2(row: pd.Series) -> float:
    val, low, high = row.iat[7], row['低估'], row['高估']
    if row['参考指标'] == '盈利收益率':
        if val >= low:
            return None
        return round((val - high) / val, 4)
    if val <= low:
        return None
    return round((high - val) / val, 4)


def to_highest2(row: pd.Series) -> float:
    val, high, highest = row.iat[7], row['高估'], row['最高']
    if row['参考指标'] == '盈利收益率':
        if val >= high:
            return None
        return round((val - highest) / val, 4)
    if val <= high:
        return None
    return round((highest - val) / val, 4)


def calculate_threshold(lst: list) -> pd.DataFrame:
    columns = ['代码', '名称', '参考指标', '最低', '低估', '高估', '最高']
    df = pd.DataFrame(THRESHOLDS, columns=columns)
    dic = lst[0]
    date = dic['_id']

    df2 = pd.DataFrame(dic.items(), columns=['名称', date])
    # print(len(df), len(df2))
    # df = pd.merge(df, df2, on='名称', how='left', indicator=True)
    # print(df[df['_merge'] == 'left_only'])
    df = pd.merge(df, df2, on='名称', how='left')
    nan = df[df[date].isna()]
    assert len(nan) == 0, print(len(nan))

    df['距最低'] = df.apply(to_lowest, axis=1)     # to_lowest(), to_low(), to_high() are just for sort
    df['距低估'] = df.apply(to_low, axis=1)
    df['距高估'] = df.apply(to_high, axis=1)
    df = df.sort_values(by=['距最低', '距低估', '距高估'])
    df['距最低'] = df.apply(to_lowest2, axis=1)
    df['距低估'] = df.apply(to_low2, axis=1)
    df['距高估'] = df.apply(to_high2, axis=1)
    df['距最高'] = df.apply(to_highest2, axis=1)
    return df.reset_index(drop=True)


def to_excel(xlsx: str, sheet: str, df: pd.DataFrame):
    wb = load_workbook(xlsx)
    ws = wb.copy_worksheet(wb.worksheets[-1])       # copy a old sheet as template to avoid adjust size
    ws.title = sheet
    wb.active = len(wb.worksheets) - 1

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
        print('       {} txt xlsx'.format(sys.argv[0]))     # update spreadsheet from clipboard or file
        print('       {} xlsx'.format(sys.argv[0]))         # update db from spreadsheet
        sys.exit(1)

    # save_thresholds(sys.argv[1])
    # save_valuations(sys.argv[1])

    if len(sys.argv) == 3 and sys.argv[2].endswith('.xlsx'):
        df = calculate_threshold(parse_valuations(sys.argv[1]))
        print(df)
        date = list(df.keys())[7]
        to_excel(sys.argv[2], date, df)
    elif sys.argv[1].endswith('.xlsx'):
        update_valuations(sys.argv[1])


if __name__ == "__main__":
    main()
