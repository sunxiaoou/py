#! /usr/local/bin/python3

SECURITIES = {
    # 港股
    '00388': ('香港交易所', 'HKD', 'OTHER_EQ', 3),
    '00700': ('腾讯控股', 'HKD', 'OTHER_EQ', 3),
    '01024': ('快手-W', 'HKD', 'OTHER_EQ', 3),
    '01810': ('小米集团-W', 'HKD', 'OTHER_EQ', 3),
    '02015': ('理想汽车-W', 'HKD', 'OTHER_EQ', 3),
    '02127': ('汇森股份', 'HKD', 'OTHER_EQ', 3),
    '02135': ('瑞丽医美', 'HKD', 'OTHER_EQ', 3),
    '02150': ('奈雪的茶', 'HKD', 'OTHER_EQ', 3),
    '02158': ('医渡科技', 'HKD', 'OTHER_EQ', 3),
    '02618': ('京东物流', 'HKD', 'OTHER_EQ', 3),
    '02840': ('SPDR金', 'HKD', 'COMMODITY', 3),
    '03033': ('南方恒生科技', 'HKD', 'OTHER_EQ', 3),
    '03110': ('GX恒生高股息率', 'HKD', 'OTHER_EQ', 3),
    '03690': ('美团-W', 'HKD', 'OTHER_EQ', 3),
    '06127': ('昭衍新药', 'HKD', 'OTHER_EQ', 3),
    '06600': ('卧安机器人', 'HKD', 'OTHER_EQ', 3),
    '06606': ('诺辉健康', 'HKD', 'OTHER_EQ', 3),
    '06668': ('星盛商业', 'HKD', 'OTHER_EQ', 3),
    '06699': ('时代天使', 'HKD', 'OTHER_EQ', 3),
    '07200': ('FL二南方恒指', 'HKD', 'OTHER_EQ', 3),
    '09618': ('京东集团-W', 'HKD', 'OTHER_EQ', 3),
    '09626': ('哔哩哔哩-W', 'HKD', 'OTHER_EQ', 3),
    '09888': ('百度集团-SW', 'HKD', 'OTHER_EQ', 3),
    '09988': ('阿里巴巴-SW', 'HKD', 'OTHER_EQ', 3),
    '09961': ('携程集团-S', 'HKD', 'OTHER_EQ', 3),

    # 美股
    'AAPL': ('苹果', 'USD', 'US_EQ_TECH', 3),
    'AMZN': ('亚马逊', 'USD', 'US_EQ_TECH', 3),
    'ARKG': ('Ark基因', 'USD', 'US_EQ_TECH', 3),
    'ARKK': ('Ark创新', 'USD', 'US_EQ_TECH', 3),
    'ARKW': ('ArkWeb', 'USD', 'US_EQ_TECH', 3),
    'BABA': ('阿里巴巴', 'USD', 'OTHER_EQ', 3),
    'BILI': ('哔哩哔哩', 'USD', 'OTHER_EQ', 3),
    'BITB': ('BitwiseETF', 'USD', 'CRYPTOCURRENCY', 3),
    'BITW': ('Btws10CryptUnt', 'USD', 'CRYPTOCURRENCY', 3),
    'BRK': ('伯克希尔B', 'USD', 'US_EQ_VALUE', 2),
    'DVY': ('道琼斯股息ETF', 'USD', 'US_EQ_VALUE', 3),
    'EWJ': ('日本ETF', 'USD', 'OTHER_EQ', 3),
    'EWJV': ('日本价值ETF', 'USD', 'OTHER_EQ', 3),
    'EMXC': ('新兴市场ETF', 'USD', 'OTHER_EQ', 3),
    'FDN': ('道琼斯互联网', 'USD', 'OTHER_EQ', 3),
    'GBTC': ('GrayscaleBitcoin', 'USD', 'CRYPTOCURRENCY', 3),
    'GS': ('高盛', 'USD', 'US_EQ_VALUE', 3),
    'IBB': ('纳斯达克生物技术', 'USD', 'US_EQ_TECH', 3),
    'IBIT': ('iSharesBitcoin', 'USD', 'CRYPTOCURRENCY', 3),
    'IEF': ('美国7-10年期国债', 'USD', 'US_TREASURY_BOND', 2),
    'IGV': ('北美科技软件ETF', 'USD', 'US_EQ_TECH', 3),
    'INDA': ('印度ETF', 'USD', 'OTHER_EQ', 3),
    'IWM': ('罗素2000ETF', 'USD', 'US_EQ_INDEX', 3),
    'IWN': ('罗素2000价值ETF', 'USD', 'US_EQ_INDEX', 3),
    'KRE': ('区域银行ETF', 'USD', 'US_EQ_VALUE', 3),
    'KWEB': ('中国海外互联网ETF', 'USD', 'OTHER_EQ', 3),
    'MAGS': ('七姊妹', 'USD', 'US_EQ_TECH', 3),
    'MINT': ('美国增强型短债', 'USD', 'US_TREASURY_BOND', 1),
    'MSFT': ('微软', 'USD', 'US_EQ_TECH', 3),
    'NVDA': ('英伟达', 'USD', 'US_EQ_TECH', 3),
    'PDD': ('拼多多', 'USD', 'OTHER_EQ', 3),
    'QQQ': ('纳斯达克100', 'USD', 'US_EQ_INDEX', 2),
    'SHV': ('美国短期国债', 'USD', 'US_TREASURY_BOND', 1),
    'SPY': ('标普500', 'USD', 'US_EQ_INDEX', 2),
    'TLT': ('美国20年期国债', 'USD', 'US_TREASURY_BOND', 2),
    'UVXY': ('恐慌1.5X做多', 'USD', 'US_EQ_INDEX', 3),
    'XBI': ('生科ETF', 'USD', 'US_EQ_TECH', 3),
    'XLE': ('能源ETF', 'USD', 'US_EQ_VALUE', 3),
    'XLF': ('金融ETF', 'USD', 'US_EQ_VALUE', 3),
    'XLV': ('医疗ETF', 'USD', 'US_EQ_VALUE', 3),

    # 现金
    'CASH_HKD': ('港币现金', 'HKD', 'CASH', 0),
    'CASH_USD': ('美元现金', 'USD', 'CASH', 0)
}


def emit_security_master_insert(securities, table='security_master'):
    """
    输出纯 INSERT 语句（要求表中 symbol 尚不存在）
    """
    def esc(s):
        return s.replace("\\", "\\\\").replace("'", "''")

    for symbol, (name, currency, sec_type, risk) in sorted(securities.items()):
        print(
            f"INSERT INTO {table} "
            f"(symbol, security_name, currency, security_type, risk_level) VALUES ("
            f"'{esc(symbol)}', "
            f"'{esc(name)}', "
            f"'{currency}', "
            f"'{sec_type}', "
            f"{int(risk)}"
            f");"
        )


def main():
    emit_security_master_insert(SECURITIES)


if __name__ == "__main__":
    main()
