#! /usr/local/bin/python3

# ! /opt/python/bin/python3

import re


def main():
    log = open('error_log')
    regex = re.compile(r'{|}')
    r2 = re.compile(r'\[.*\] ')
    r3 = re.compile(r'(\w+)')
    r4 = re.compile(r'\\n')
    for line in log.readlines():
        line = line.rstrip()
        if regex.search(line) is not None:
            line = r2.sub('', line)
            words = line.split(': ')
            line = r3.sub(r'{0}:\1'.format(words[0]), words[1])
            print(line)
        elif r4.search(line) is not None:
            for i in line.split('\\n'):
                print(i)
        else:
            print(line)


if __name__ == "__main__":
    main()
