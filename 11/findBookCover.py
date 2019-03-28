#! /usr/local/bin/python3

from selenium import webdriver

# http://selenium-python.readthedocs.org/

browser = webdriver.Firefox()
# type(browser)
# <class 'selenium.webdriver.firefox.webdriver.WebDriver'>

browser.get('http://inventwithpython.com')

try:
    # <a href="#automate">
    #   <img class="card-img-top cover-thumb" src="/images/cover_automate_thumb.png" alt="Cover of Automate the Boring Stuff with Python" />
    # </a>
    elem = browser.find_element_by_class_name('card-img-top.cover-thumb')
    type(elem)
    # <class 'selenium.webdriver.remote.webelement.WebElement'>
    print('Found <%s> element with that class name!' % (elem.tag_name))
    elem = browser.find_element_by_link_text('More Info')
    elem.click()
except:
    print('Was not able to find an element with that name.')
