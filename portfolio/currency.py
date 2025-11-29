#! /usr/local/bin/python3
import requests
from bs4 import BeautifulSoup


def hkd_usd_rate() -> tuple:
    url = 'https://www.boc.cn/sourcedb/whpj/'
    i = 0
    dic = {}
    while '港币' not in dic or '美元' not in dic:
        if i > 0:
            url += "index_{}.html".format(i)
        res = requests.get(url)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, 'lxml')

        tab = soup.find_all("table")[1]
        trs = tab.find_all("tr")
        trs.pop(0)
        for tr in trs:
            tds = tr.find_all("td")
            if '港币' not in dic and tds[0].text == '港币':
                dic['港币'] = round(float(tds[4].text) / 100, 4)
            elif '美元' not in dic and tds[0].text == '美元':
                dic['美元'] = round(float(tds[4].text) / 100, 4)
        i += 1
    return dic['港币'], dic['美元']


def main():
    print(hkd_usd_rate())


if __name__ == "__main__":
    main()
