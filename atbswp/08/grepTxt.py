#! /usr/bin/python3

import os, re, sys

if len(sys.argv) < 2:
    print('Usage: ' + sys.argv[0] + ' regex')
    sys.exit(1)

for fn in os.listdir():
    # if fn[-4:] == '.txt':
    if fn.endswith('.txt'):
        print(fn + ':')
        text = open(fn) 
        regex = re.compile(sys.argv[1])
        for line in text.readlines():
            if regex.search(line) != None:
                print(line, end = '')
        text.close()
