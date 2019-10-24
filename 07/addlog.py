#! /usr/local/bin/python3

# ! /opt/python/bin/python3
# After running, please check with
# $ grep -n return shrpx.cc | grep -v "return.*;"

import re
import sys


def main():
    if len(sys.argv) < 2:
        print('Usage: {} file'.format(sys.argv[0]))
        sys.exit(1)

    log = open(sys.argv[1])
    rin = re.compile(r'^(\S+ )?(\S+)\(.*\) (\S+ )?{$')
    rin2 = re.compile(r'^(\S+ )?(\S+)\(.*,$')
    rout = re.compile(r'^(\s+)return ')
    rout2 = re.compile(r'^}$')

    lines = log.readlines()
    i = 0
    func = ''
    out = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if line == 'using namespace nghttp2;':
            print('#include "log.h"\n')
            print(line)
        elif rin.search(line) is not None:
            mo = rin.search(line)
            func = mo.group(2).lstrip('*')
            print(line)
            print('  PRINT(log_in, "{}")'.format(func))
        elif rin2.search(line) is not None:
            mo = rin2.search(line)
            func = mo.group(2).lstrip('*')
            while True:
                print(line)
                if line.endswith(' {'):
                    break
                i += 1
                line = lines[i].rstrip()
            print('  PRINT(log_in, "{}")'.format(func))
        elif rout.search(line) is not None:
            mo = rout.search(line)
            s = mo.group(1)
            if out == 0:
                print('{}PRINT(log_out, "{}")'.format(s, func))
                out = 1
            else:
                print('{}PRINT(log_out, "{}{}")'.format(s, func, out))
            out += 1
            print(line)
        elif rout2.search(line) is not None:
            prev_line = lines[i - 1].rstrip()
            if rout.search(prev_line) is None:
                if out == 0:
                    print('  PRINT(log_out, "{}")'.format(func))
                else:
                    print('  PRINT(log_out, "{}{}")'.format(func, out))
            out = 0
            print(line)
        else:
            print(line)
            # pass
        i = i + 1


if __name__ == "__main__":
    main()
