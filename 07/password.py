#! /usr/bin/python3

import re

def validate(password):
    regexs = ['[a-z]+', '[A-Z]+', '[0-9]+', '[a-zA-Z0-9]{8,}']
    for i in range(len(regexs)):
        regex = re.compile(r'{0}'.format(regexs[i])) 
        mo = regex.search(password)
        if (mo == None):
            return False
    return True

PASSWORDS = {'email': 'F7minlBDDuvMJuxESSKHFhTxFtjVB6',
             'blog': 'VmALvQyKAxiVH5G8v01if1MLZF3sdt',
             'luggage': 'Abc12345',
             'test1': 'ABC12345',
             'test2': 'abc12345',
             'test3': 'ABCabcab',
             'test4': 'Abc1234'
             }

# validate(PASSWORDS.get('email', None))
for k, v in PASSWORDS.items():
    print(k + ' ' + str(validate(v)))
