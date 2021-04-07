#! /usr/local/bin/python3

# ! /opt/python/bin/python3

import re
import sys


def main():
    if len(sys.argv) < 2:
        print('Usage: {} file'.format(sys.argv[0]))
        sys.exit(1)

    log = open(sys.argv[1])
    regex = re.compile(r'^(\s+)fprintf\(stderr, "%\*c{ (~?\w+)')
    r2 = re.compile(r'^(\s+)fprintf\(stderr, "%\*c} (~?\w+)')
    r3 = re.compile(r'^(\s+)fprintf\(stderr, "%\*c (\w+)')
    for line in log.readlines():
        line = line.rstrip()
        if regex.search(line) is not None:
            # print(line)
            mo = regex.search(line)
            print('{0}PRINT(log_in, "{1}")'.format(mo.group(1), mo.group(2)))
        elif r2.search(line) is not None:
            # print(line)
            mo = r2.search(line)
            print('{0}PRINT(log_out, "{1}")'.format(mo.group(1), mo.group(2)))
        elif r3.search(line) is not None:
            # print(line)
            mo = r3.search(line)
            print('{0}PRINT(log_still, "{1}")'.format(mo.group(1), mo.group(2)))
        else:
            print(line)
            pass


if __name__ == "__main__":
    main()
