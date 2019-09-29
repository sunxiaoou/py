#! /usr/local/bin/python3

import re
import sys
import time

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
# then login People Search from SSO, that is why we need attach mode

# After download, use following command to check location:
# $ grep "ADR;" *.vcf | awk -F\; '{printf("%s: %s\n", $1, $NF)}' | grep -v "CN"

def attach_browser():
    options = webdriver.ChromeOptions()
    options.debugger_address = 'localhost:9014'
    driver = webdriver.Chrome(options=options)
    return driver


def download_vcf(name, driver)
    # regex = re.compile(r'([a-zA-Z]+\.)?[a-zA-Z]+\.[a-zA-Z]+')
    regex = re.compile(r'([a-zA-Z]+(\.|-))?[a-zA-Z]+\.[a-zA-Z]{2,}')
    mo = regex.search(name)
    if mo is None:
        print('{}, Not a mail, ,'.format(name))
        return
    name = mo.group().lower()
    mail = name + '@oracle.com'
    print(mail)
    url = "https://people.oracle.com/apex/f?p=8000:1:101705649184588::::P1_SEARCH:"
    driver.get(url + mail)
    delay = 5   # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'P2_PERSON_EMAIL')))
        # print("Page is ready!")
    except TimeoutException:
        # print("{}, Retry, ,".format(name))
        links = driver.find_elements_by_tag_name('a')
        for link in links:
            href = link.get_attribute('href')
            if href.endswith(name.lower()):
                # print(href)
                driver.get(href)
                try:
                    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'P2_PERSON_EMAIL')))
                except TimeoutException:
                    print("{}, Timeout, ,".format(name))
                    return
                break

    try:
        button = driver.find_element_by_css_selector(
            ".t-Button.t-Button--icon.t-Button--small.t-Button--iconLeft.t-Button--hot")
        # print(type(button))
        button.click()
    except NoSuchElementException:
        print(name + ", Not found, ,")
        return


def main():
    if len(sys.argv) < 2:
        print('Usage: {} name_list'.format(sys.argv[0]))
        sys.exit(1)

    driver = attach_browser()
    file = open(sys.argv[1])
    try:
        for name in file.readlines():
            name = name.strip()
            if not name:
                continue
            download_vcf(name, driver)
            time.sleep(1)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')

    driver.quit()


if __name__ == "__main__":
    main()
