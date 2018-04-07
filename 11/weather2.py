#! /usr/bin/python3

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.formfill.enable', False)
browser = webdriver.Firefox(firefox_profile=profile)
browser.get('http://www.weather.gov')

elem = browser.find_element_by_id('inputstring')
elem.clear()
elem.send_keys('94105, San Francisco, CA, USA')
elem.submit()
