#! /usr/bin/python3


import re
import requests
from bs4 import BeautifulSoup
# from pprint import pprint
from selenium import webdriver


def get_animes():
    url = 'http://ww1.animeland.tv/anime-list'
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')
    div = soup.find('div', id='ddmcc_container')
    animes = []
    for a in div.find_all('a'):
        animes.append(a.getText())
    return animes


def search_rating(animes):
    url = 'https://movie.douban.com/'
    driver = webdriver.Chrome()     # needs chromedriver in $PATH
    driver.get(url)
    items = []
    for i in range(len(animes)):
        try:
            element = driver.find_element_by_id('inp-query')
            # element.send_keys('perfect blue')
            element.send_keys(animes[i])
            element.submit()
            soup = BeautifulSoup(driver.page_source, 'lxml')

            divs = soup.findAll('div', class_='detail')
            for div in divs:
                try:
                    txt = div.find('div', class_='meta abstract').getText()
                    mo = re.compile(r'动画').search(txt)
                    if mo is None:
                        continue
                    title = div.find('div', class_='title').getText()
                    txt = div.find('span', class_='rating_nums').getText()
                    rating_nums = float(txt)
                    txt = div.find('span', class_='pl').getText()
                    mo = re.compile(r'(\d+)人评价').search(txt)
                    pl = int(mo.group(1))
                    item = (animes[i], title, rating_nums, pl)
                    items.append(item)
                    break
                except AttributeError:
                    continue
            driver.back()
        except Exception as err:
            print('{} happened at {}'.format(str(err), i))
            break

    driver.quit()
    items.sort(key=lambda e: [-e[2], -e[3]])
    # pprint(items)
    for item in items:
        print("'{}', '{}', {}, {}".format(item[0], item[1], item[2], item[3]))


def main():
    animes = get_animes()
    # pprint(animes)
    # search_rating(['Amnesia'])
    search_rating(animes)


if __name__ == "__main__":
    main()
