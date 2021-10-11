#! /usr/bin/python3
import re
import sys
from time import sleep

import pandas as pd
from selenium import webdriver


def parse() -> list:
    url = 'https://www.zhaobiaoziyuan.com/zhaobiao/24-0-0-0-0/steam.html'

    driver = webdriver.Chrome()
    driver.get(url)
    bids = []

    # for i in range(3):
    while True:
        span = driver.find_element_by_class_name('layui-laypage-curr')
        ems = span.find_elements_by_tag_name('em')
        print(ems[1].text)

        links = driver.find_elements_by_class_name('search_center5')
        for a in links:
            href = a.get_attribute('href')
            title, date, comment, others = a.text.split('\n')
            city, amount = re.sub(' ', '', others).split('中标信息')
            bids.append((title, date, city, amount, href))

        next = driver.find_element_by_class_name('layui-laypage-next')
        if 'layui-disabled' in next.get_attribute('class'):
            break
        next.click()
        sleep(2)

    driver.quit()
    return bids


def main():
    columns = ['title', 'date', 'city', 'amount', 'link']
    bids = pd.DataFrame(parse(), columns=columns)
    print(bids)

    if len(sys.argv) > 1:
        bids.to_excel(sys.argv[1])


if __name__ == "__main__":
    main()
