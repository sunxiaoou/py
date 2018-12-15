#! /usr/bin/python3

from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://book.douban.com/subject_search?search_text=python&cat=1001'

driver = webdriver.Chrome()     # needs chromedriver in $PATH
driver.get(url)
soup = BeautifulSoup(driver.page_source, "lxml")
driver.quit()
divs = soup.findAll('div', class_='detail')
for div in divs:
    title = div.find('div', class_='title').getText()
    rating_nums = div.find('span', class_='rating_nums').getText()
    pl = div.find('span', class_='pl').getText()
    print('title({}) rating_nums({}) rating_pl({})'.format(title, rating_nums, pl))
