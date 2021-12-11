#! /usr/bin/python3
import re
import sys
from pprint import pprint

indexes = [
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
    '十年期国债'
]


def parse(file: str) -> list:
    with open(file) as fp:
        lines = [line.rstrip('\n') for line in fp.readlines()]

    reg_date = re.compile(r'20\d{6}')
    result = []
    try:
        i = 0
        while True:
            while reg_date.search(lines[i]) is None:
                i += 1
            date = reg_date.search(lines[i]).group()
            # print(date)
            dic = {}
            i += 1
            while not lines[i].startswith('永续A收益'):
                l = lines[i]
                i += 1
                while ' ' not in l and re.search(r'[^\d%.\s]+', l):         # should not be digital str
                    l += lines[i]
                    i += 1
                if re.search(r'[^\d%.\s]+', l):
                    e = l.split()
                    key = e[0].strip('*')
                    value = ''
                    for j in range(1, len(e)):
                        if e[j] != '*':
                            value = e[j]
                            break
                    if key not in '盈利收益率 市盈率 市净率股息率 ROE 场内基金 场外基金':
                        # print(key, float(value.rstrip('%')))
                        assert(key in indexes), print('{} is not a index'.format(key))
                        dic[key] = float(value.rstrip('%'))
            result.append((date, dic))
    except IndexError:
        pass
    return result


def main():
    if len(sys.argv) < 2:
        print('Usage: {} txt'.format(sys.argv[0]))
        print('       {} txt xlsx'.format(sys.argv[0]))
        sys.exit(1)
    pprint(parse(sys.argv[1]))


if __name__ == "__main__":
    main()
