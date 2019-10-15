#! /usr/local/bin/python3

# ! /opt/python/bin/python3

import re
import sys


def main():
    if len(sys.argv) < 2:
        print('Usage: {} file'.format(sys.argv[0]))
        sys.exit(1)
    
    log = open(sys.argv[1])
    regex = re.compile(r'\w{2}')
    r2 = re.compile(r'[\[\]]')
    for line in log.readlines():
        line = line.split('|')[1].strip()
        nums = []
        for num in regex.findall(line):
            nums.append('0X' + num)
        print(r2.sub('', str(nums)))


if __name__ == "__main__":
    main()
