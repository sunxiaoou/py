#! /usr/bin/python3

import re

def lastName(names):
    regex = re.compile(r'(^[A-Z](\w)* Nakamoto$)') 

    for i in range(len(names)):
        mo = regex.search(names[i])
        if (mo != None):
            print(mo.group())

names = ['Satoshi Nakamoto', 'Alice Nakamoto', 'Robocop Nakamoto',
        'satoshi Nakamoto', 'Mr. Nakamoto', 'Nakamoto', 'Satoshi nakamoto' ]
lastName(names)
