#! /usr/local/bin/python3

import re
import sys
from bs4 import BeautifulSoup
from selenium import webdriver


def usage():
    print('Usage: ' + sys.argv[0] + ' -b|m [-p num] [-t] subject')


def open_browser():
    return webdriver.Chrome()     # needs chromedriver in $PATH


# Prerequisites:
# A browser has opened in debug mode as, for example:
#   $ "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
#       --remote-debugging-port=9014 --user-data-dir=/tmp/chrome
# then login bugdb from SSO, that is why we need attach mode


def attach_browser():
    options = webdriver.ChromeOptions()
    options.debugger_address = 'localhost:9014'
    driver = webdriver.Chrome(chrome_options=options)
    return driver


def query_items(driver):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    trs = soup.find('table', id='SummaryTab').findAll('tr')
    for tr in trs:
        links = tr.findAll('a')
        if not links:
            continue
        bug = links[0].getText()
        print(bug)
        href = links[1].get('href')
        driver.get('https://bug.oraclecorp.com' + href)
        with open(bug + '.html', "w") as f:
            f.write(driver.page_source)


def main():
    url = 'https://bug.oraclecorp.com/pls/bug/WEBBUG_REPORTS.do_edit_report?' + \
          'rpt_title=&fcont_arr=CURRENT_USER&fid_arr=6&fcont_arr=&fid_arr=10&fcont_arr=off&fid_arr=157&' + \
          'fcont_arr=off&fid_arr=166&fcont_arr=2&fid_arr=100&cid_arr=2&cid_arr=3&cid_arr=9&cid_arr=8&cid_arr=7&' + \
          'cid_arr=30&cid_arr=11&cid_arr=6&cid_arr=5&cid_arr=51&cid_arr=13&f_count=5&c_count=11&query_type=1'
    # url = 'https://bug.oraclecorp.com/pls/bug/webbug_reports.my_open_bugs'

    driver = attach_browser()
    driver.get(url)
    tmp = driver.page_source
    query_items(driver)
    with open("buglist.html", "w") as f:
        regex = re.compile(r'/pls/bug/webbug_print.showbug\?c_rptno=(\d+)')
        tmp = regex.sub(r'\1.html', tmp)
        f.write(tmp)

    driver.quit()


if __name__ == "__main__":
    main()
