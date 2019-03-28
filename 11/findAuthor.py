#! /usr/local/bin/python3

import bs4

exampleFile = open('example.html')
exampleSoup = bs4.BeautifulSoup(exampleFile.read(), "lxml")

print(type(exampleSoup))
# <class 'bs4.BeautifulSoup'>

elems = exampleSoup.select('#author')

print(type(elems))
# <class 'list'>

print(len(elems))
# 1

print(type(elems[0]))
# <class 'bs4.element.Tag'>

print(str(elems[0]))
# '<span id="author">Al Sweigart</span>'

print(elems[0].getText())
# 'Al Sweigart'

print(elems[0].attrs)
# {'id': 'author'}

print()

for elem in exampleSoup.select('p'):
    print(str(elem))
    print(str(elem.getText()))

print()

soup = bs4.BeautifulSoup(open('example.html'), "lxml")
spanElem = soup.select('span')[0]

print(str(spanElem))
# '<span id="author">Al Sweigart</span>'

print(spanElem.get('id'))
# 'author'

print(spanElem.get('some_nonexistent_addr') == None)
# True

print(spanElem.attrs)
# {'id': 'author'}
