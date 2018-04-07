#! /usr/bin/python3

import shelve

shelfFile = shelve.open('mydata')
cats = ['Zophie', 'Pooka', 'Simon']
shelfFile['cats'] = cats
shelfFile.close()

shelfFile = shelve.open('mydata')
type(shelfFile)
print(shelfFile['cats'])
shelfFile.close()
