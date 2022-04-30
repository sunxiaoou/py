#! /usr/bin/python3


on_market = {
    '501046': ('财通福鑫', '主动', 2),
    '512170': ('医疗ETF', '医药', 3),
    '515910': ('质量ETF', '指数', 2),
    '600009': ('上海机场', '股票', 3),
    'BABA': ('阿里巴巴', '中概股', 3),
    'ARKW': ('ARK Web', '股票', 3),
    'SPY': ('标普500', '指数', 2),
    'AAPL': ('苹果', '股票', 3),
    'MSFT': ('微软', '股票', 3),
    'GS': ('高盛', '股票', 3),
    'BILI': ('哔哩哔哩', '中概股', 3),
    'PDD': ('拼多多', '中概股', 3),
    '00388': ('香港交易所', '股票', 3),
    '00700': ('腾讯控股', '中概股', 3),
    '07200': ('FL二南方恒指', '股票', 3),
    '01810': ('小米集团-W', '中概股', 3),
    '03690': ('美团-W', '中概股', 3),
    '09618': ('京东集团-W', '中概股', 3),
    '09988': ('阿里巴巴-SW', '中概股', 3),
    '03033': ('南方恒生科技', '中概股', 3),
    'GBTC': ('Grayscale Bitcoin', '股票', 3),
    'KWEB': ('中国海外互联网ETF', '中概股', 3)
}


off_market = {
    # 宽基指数
    "000311": ("景顺长城沪深300", "指数", 2),
    "001556": ("天弘中证500A", "指数", 2),
    "110003": ("易方达上证50指数A", "指数", 2),
    "161039": ("富国中证1000", "指数", 2),
    "163407": ("兴全沪深300A", "指数", 2),

    # 策略指数
    "003318": ("景顺长城中证500低波动", "指数", 2),
    "006341": ("中金MSCI中国A股国际质量A", "指数", 2),
    "090010": ("大成中证红利指数A", "指数", 2),
    "501050": ("华夏上证50AH", "指数", 2),
    "519671": ("银河沪深300价值", "指数", 2),
    "540012": ("汇丰晋信恒生股票龙头", "指数", 2),

    # 行业指数
    "001594": ("天弘中证银行A", "指数", 2),
    "004069": ("南方中证全指证券", "指数", 2),
    "006327": ("易方达中证海外50ETF联接", "中概股", 3),
    "010202": ("天弘中证科技100", "指数", 3),
    "012348": ("天弘恒生科技", "中概股", 3),
    "164906": ("交银中证海外中国互联网", "中概股", 3),
    "501009": ("汇添富中证生物科技", "医药", 3),
    "501090": ("华宝中证消费龙头", "指数", 2),

    # 货币
    "003474": ("南方天天利B", "货币", 0),
    "000642": ("汇添富货币市场C", "货币", 0),
    "000730": ("博时现金宝", "货币", 0),
    "000773": ("万家现金宝", "货币", 0),

    # 深度价值
    "000480": ("东方红新动力", "主动", 2),
    "001810": ("中欧潜力价值", "主动", 2),
    "004350": ("汇丰晋信价值先锋", "主动", 2),
    "006567": ("中泰星元灵活配置A", "主动", 2),
    "006624": ("中泰玉衡价值优选", "主动", 2),
    "260112": ("景顺长城能源基建", "主动", 2),

    # 成长价值
    "001112": ("东方红中国优势", "主动", 2),
    "001487": ("宝盈优势产业", "主动", 3),
    "005267": ("嘉实价值精选", "主动", 2),
    "005827": ("易方达蓝筹精选", "主动", 2),
    "100020": ("富国天益价值", "主动", 2),
    "169101": ("东方红睿丰", "主动", 2),
    "519712": ("交银阿尔法核心", "主动", 2),

    # 成长
    "001538": ("上投摩根科技前沿", "主动", 3),
    "005354": ("富国沪港深行业精选A", "主动", 2),
    "110013": ("易方达科翔", "主动", 2),
    "377240": ("上投摩根新兴动力", "主动", 3),
    "519035": ("富国天博创新", "主动", 2),

    # 医药
    "001717": ("工银前沿医疗", "医药", 3),
    "001766": ("上投摩根医疗健康", "医药", 3),
    "003095": ("中欧医疗健康A", "医药", 3),
    "004851": ("广发医疗保健", "医药", 3),
    "006002": ("工银医药健康行业", "医药", 3),

    # 均衡
    "002340": ("富国价值优势", "主动", 2),
    "004674": ("富国新机遇灵活配置", "主动", 2),
    "004868": ("交银股息优化", "主动", 2),
    "005587": ("安信比较优势", "主动", 2),
    "163406": ("兴全合润", "主动", 2),
    "163415": ("兴全商业模式优选", "主动", 2),
    "166002": ("中欧新蓝筹A", "主动", 2),
    "519688": ("交银精选", "主动", 2),

    "001974": ("景顺长城量化新动力", "主动", 2),
    "540003": ("汇丰晋信动态策略A", "主动", 2)
}


def main():
    pass


if __name__ == "__main__":
    main()
