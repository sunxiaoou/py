#! /usr/bin/python3

from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver


def main():
    # url = 'https://book.douban.com/subject_search?search_text=python&cat=1001'
    url = 'https://book.douban.com/'

    driver = webdriver.Chrome()     # needs chromedriver in $PATH
    driver.get(url)
    element = driver.find_element_by_id('inp-query')
    element.send_keys('python')
    element.submit()

    items = []
    for i in range(2):
        soup = BeautifulSoup(driver.page_source, 'lxml')
        divs = soup.findAll('div', class_='detail')
        for div in divs:
            title = div.find('div', class_='title').getText()
            rating_nums = div.find('span', class_='rating_nums').getText()
            pl = div.find('span', class_='pl').getText()
            item = (title, rating_nums, pl)
            items.append(item)

        element = driver.find_element_by_link_text('后页>')
        element.click()

    pprint(items)
    # driver.quit()

if __name__ == "__main__":
    main()
