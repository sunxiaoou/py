#! /usr/local/bin/python3

# ! /opt/python/bin/python3

import re
import sys


def main():
    if len(sys.argv) < 2:
        print('Usage: {} file'.format(sys.argv[0]))
        sys.exit(1)

    log = open(sys.argv[1])
    regex = re.compile(r'^(\w+ )?(\w+)\(.*\) {$')
    r2 = re.compile(r'^(\w+ )?(\w+)\(.*,$')
    r3 = re.compile(r'^(\s+)(return;|return \d;|return -\d;)')
    r4 = re.compile(r'^}$')
    lines = log.readlines()
    i = 0
    func = ''
    out = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if regex.search(line) is not None:
            mo = regex.search(line)
            func = mo.group(2)
            print(line)
            print('  PRINT(log_in, "{}")'.format(func))
        elif r2.search(line) is not None:
            mo = r2.search(line)
            func = mo.group(2)
            while True:
                print(line)
                line = lines[i + 1].rstrip()
                if not line.endswith(' {'):
                    break
                i += 1
            print('  PRINT(log_in, "{}")'.format(func))
        elif r3.search(line) is not None:
            mo = r3.search(line)
            s = mo.group(1)
            if out == 0:
                print('{}PRINT(log_out, "{}")'.format(s, func))
                out = 1
            else:
                print('{}PRINT(log_out, "{}{}")'.format(s, func, out))
            out += 1
            print(line)
        elif r4.search(line) is not None:
            prev_line = lines[i - 1].rstrip()
            if r3.search(prev_line) is None:
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
