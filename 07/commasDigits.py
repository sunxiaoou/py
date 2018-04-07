#! /usr/bin/python3

import re

def commasDigits(numbers):
    # regex = re.compile(r'(^\d{1,3}(,\d\d\d)*)$') 
    regex = re.compile(r'(^\d{1,3}(,\d{3})*)$') 

    for i in range(len(numbers)):
        mo = regex.search(numbers[i])
        if (mo != None):
            print(mo.group())

numbers = ['42', '1,234', '6,368,745', '12,34,567', '1234']
commasDigits(numbers)
