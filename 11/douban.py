#! /usr/bin/python3

import re
import sys
from bs4 import BeautifulSoup
from pprint import pprint
from selenium import common
from selenium import webdriver


def open_browser():
    return webdriver.Chrome()     # needs chromedriver in $PATH


def attach_browser():
    # A browser has opened as, for example:
    #   $ google-chrome-stable --remote-debugging-port=9014 --user-data-dir=/tmp/chrome
    options = webdriver.ChromeOptions()
    options.debugger_address = 'localhost:9014'
    driver = webdriver.Chrome(chrome_options=options)
    return driver


def main():
    if len(sys.argv) < 3:
        print('Usage: ' + sys.argv[0] + ' book|movie subject')
        sys.exit(1)

    url = 'https://' + sys.argv[1] + '.douban.com/'
    print(url + ' ' + sys.argv[2])

    # driver = attach_browser()
    driver = open_browser()

    driver.get(url)
    element = driver.find_element_by_id('inp-query')
    # element.send_keys('perfect blue')
    element.send_keys(sys.argv[2])
    element.submit()

    items = []
    for i in range(10):
        soup = BeautifulSoup(driver.page_source, 'lxml')
        divs = soup.findAll('div', class_='detail')

        for div in divs:
            try:
                # title = div.find('div', class_=re.compile(r'^title')).getText()
                title = div.find('div', class_='title').getText()
                txt = div.find('span', class_='rating_nums').getText()
                rating_nums = float(txt)
                txt = div.find('span', class_='pl').getText()
                mo = re.compile(r'(\d+)人评价').search(txt)
                pl = int(mo.group(1))
                item = (title, rating_nums, pl)
                items.append(item)
            except AttributeError:
                continue

        try:
            element = driver.find_element_by_link_text('后页>')
            element.click()
        except common.exceptions.NoSuchElementException:
            break

    items.sort(key=lambda e: [-e[1], -e[2]])
    pprint(items)
    driver.quit()

if __name__ == "__main__":
    main()
