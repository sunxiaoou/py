#! /usr/bin/python3

from selenium import webdriver

browser = webdriver.Firefox()
browser.get('file:///home/xixisun/student/hfhtmlcss/chapter14/contest/form.html')

elem = browser.find_element_by_name('firstname')
# elem.clear()
elem.send_keys('Scott')

elem = browser.find_element_by_name('lastname')
elem.send_keys('Tiger')

elem.submit()
