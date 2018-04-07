#! /usr/bin/python3

import requests, bs4

res = requests.get('http://www.weather.gov')
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, "lxml")
print(type(soup))
# <class 'bs4.BeautifulSoup'>
