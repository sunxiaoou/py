#! /usr/bin/python3

import getopt
import re
import sys
from bs4 import BeautifulSoup
from pprint import pprint
from selenium import common
from selenium import webdriver


def usage():
    print('Usage: ' + sys.argv[0] + ' -b|m [-t] subject')


def open_browser():
    return webdriver.Chrome()     # needs chromedriver in $PATH


# Prerequisites:
# A browser has opened in debug mode as, for example:
#   $ google-chrome-stable --remote-debugging-port=9014 --user-data-dir=/tmp/chrome
def attach_browser():
    options = webdriver.ChromeOptions()
    options.debugger_address = 'localhost:9014'
    driver = webdriver.Chrome(chrome_options=options)
    return driver


def drive_by_name(subject, tag, driver):
    if not tag:
        # element.send_keys('perfect blue')
        element = driver.find_element_by_id('inp-query')
        element.send_keys(subject)
        element.submit()
    else:
        element = driver.find_element_by_link_text('所有热门标签»')
        element.click()
        elements = driver.find_elements_by_name('search_text')
        elements[1].send_keys(subject)
        elements[1].submit()


def get_sorted_items(tag, driver):
    items = []
    for i in range(10):
        soup = BeautifulSoup(driver.page_source, 'lxml')

        if not tag:
            elements = soup.findAll('div', class_='detail')
            for element in elements:
                try:
                    # title = div.find('div', class_=re.compile(r'^title')).getText()
                    title = element.find('div', class_='title').getText()
                    txt = element.find('span', class_='rating_nums').getText()
                    rating_nums = float(txt)
                    txt = element.find('span', class_='pl').getText()
                    mo = re.compile(r'(\d+)人评价').search(txt)
                    pl = int(mo.group(1))
                    item = (title, rating_nums, pl)
                    items.append(item)
                except AttributeError:
                    continue

        else:
            elements = soup.findAll('li', class_='subject-item')
            for element in elements:
                try:
                    element = element.find('div', class_='info')
                    txt = element.find('h2').getText()
                    mo = re.compile(r'(\w.*\w)').search(txt)
                    title = mo.group(1)
                    txt = element.find('span', class_='rating_nums').getText()
                    rating_nums = float(txt)
                    txt = element.find('span', class_='pl').getText()
                    mo = re.compile(r'(\d+)人评价').search(txt)
                    pl = int(mo.group(1))
                    item = (title, rating_nums, pl)
                    items.append(item)
                except (AttributeError, ValueError):
                    continue

        try:
            element = driver.find_element_by_link_text('后页>')
            element.click()
        except common.exceptions.NoSuchElementException:
            break

    items.sort(key=lambda e: [-e[1], -e[2]])
    return items


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "bmt")
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(1)

    type_name = None
    is_tag = False
    for o, a in opts:
        if o == '-b':
            type_name = 'book'
        elif o == '-m':
            type_name = 'movie'
        elif o == '-t':
            is_tag = True
        else:
            assert False, "unhandled option"

    if type_name is None:
        usage()
        sys.exit(1)

    url = 'https://' + type_name + '.douban.com/'
    print(url + ' ' + args[0])

    # driver = attach_browser()
    driver = open_browser()
    driver.get(url)

    drive_by_name(args[0], is_tag, driver)
    items = get_sorted_items(is_tag, driver)
    pprint(items)
    driver.quit()

if __name__ == "__main__":
    main()
