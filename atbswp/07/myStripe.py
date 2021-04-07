#! /usr/bin/python3

import re

def myStrip(string, *args):
    # print('first arg: ' + string)
    # if len(args) > 0:
    #    print('second arg: ' + args[0])
    if len(args) == 0:
        regex = re.compile(r'(^\s+)|(\s+$)')
    else:
        regex = re.compile(r'(^{0})|({0}$)'.format('[' + args[0] + ']+'))
    """
    mo = regex.search(string)
    if (mo == None):
        return False
    else:
        return True
    """
    return regex.sub('', string)

    
print(myStrip('One'))
print(myStrip('  One'))
print(myStrip('One  '))
print(myStrip('  One  '))

print(myStrip('zero one', 'two'))
print(myStrip('zero two', 'two'))
print(myStrip('two one', 'two'))
