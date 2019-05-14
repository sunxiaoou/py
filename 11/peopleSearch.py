#! /usr/local/bin/python3

import re
import sys
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def open_browser():
    return webdriver.Chrome()     # needs chromedriver in $PATH


# Prerequisites:
# A browser has opened in debug mode as, for example:
#   $ "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
#       --remote-debugging-port=9014 --user-data-dir=/tmp/chrome
# then login bugDB from SSO, that is why we need attach mode


def attach_browser():
    options = webdriver.ChromeOptions()
    options.debugger_address = 'localhost:9014'
    driver = webdriver.Chrome(options=options)
    return driver


def people_search(name, driver):
    url = "https://people.oracle.com/apex/f?p=8000:1:101705649184588::::P1_SEARCH:"
    driver.get(url + name + "@oracle.com")
    delay = 5   # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'profile_main')))
        # print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
        return

    soup = BeautifulSoup(driver.page_source, 'lxml')
    try:
        ul = soup.find('ul', class_='p-UserBlocks p-UserBlocks--horizontal p-UserBlocks--managers')
        manager = ul.find('span', class_='p-UserBlock-name').getText()
        dt = soup.find('dt')
        cost_center = ''
        if dt.getText().strip() == 'Cost Center':
            sibling = dt.find_next_sibling()
            while sibling is not None and sibling.name != 'dd':
                sibling = sibling.find_next_sibling()
            cost_center = sibling.getText().strip()
        ul = soup.find('ul', class_='p-DetailList p-DetailList--stacked')
        city = ul.find('a').getText()
    except NoSuchElementException:
        return
    people = (name, manager, cost_center, city)
    print(people)

    # with open(name + '.html', "w") as f:
    #    f.write(driver.page_source)


def main():
    # people_search("xiao.ou.sun", driver)
    # people_search("junger.he", driver)

    if len(sys.argv) < 2:
        print('Usage: %s file'.format(sys.argv[0]))
        sys.exit(1)

    driver = attach_browser()
    file = open(sys.argv[1])
    for name in file.readlines():
        name = name.strip()
        people_search(name, driver)
        time.sleep(1)
    driver.quit()


if __name__ == "__main__":
    main()
