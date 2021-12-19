#! /usr/bin/python3
import re
import sys
from pprint import pprint

import pandas as pd
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


def parse(file: str) -> list:
    with open(file) as f:
        lines = []
        for l in f.readlines():
            lines += l.rstrip('\n').split()

    # with open('tmp.txt', 'w') as f:
    #     for l in lines:
    #         f.write(l + '\n')

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


def main():
    if len(sys.argv) < 2:
        print('Usage: {} txt'.format(sys.argv[0]))
        print('       {} txt xlsx'.format(sys.argv[0]))
        sys.exit(1)
    valuations = parse(sys.argv[1])
    # pprint(valuations)
    print(len(valuations))
    df = pd.DataFrame(valuations)
    df['_id'] = pd.to_datetime(df['_id'])
    print(df)

    mongo = Mongo()
    mongo.save('screw', df)
    # check(valuations)
    # for date, valuation in valuations:
    #     if '300价值' in valuation:
    #         print(date, valuation['300价值'])


if __name__ == "__main__":
    main()
