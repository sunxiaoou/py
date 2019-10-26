#! /usr/local/bin/python3

# ! /opt/python/bin/python3

import re
import sys


def main():
    if len(sys.argv) < 2:
        lines = sys.stdin.readlines()
    else:
        log = open(sys.argv[1])
        lines = log.readlines()

    regex = re.compile(r'(\s+)PRINT\((\w+), "(\S+)"\)')
    i = 0
    cur_func = '1234'
    # out = 0
    while i < len(lines):
        mo = regex.search(lines[i])
        indent = mo.group(1)
        method = mo.group(2)
        func = mo.group(3)
        if not func.startswith(cur_func):
            assert method == 'log_in', print("{}: {} should begin with log_in()".format(i, func))
            assert indent == '  ', print("{}: {} first indent should be 2".format(i, func))
            if i > 0:
                # assert out > 0, print("{}: {} ends without log_out()".format(i, cur_func))
                mo = regex.search(lines[i - 1])
                indent = mo.group(1)
                method = mo.group(2)
                prev = mo.group(3)
                assert prev.startswith(cur_func), print("{}: {} should start with {}".format(i, prev, cur_func))
                assert method == 'log_out', print("{}: {} should begin with log_in()".format(i, prev))
                assert indent == '  ', print("{}: {} last indent should be 2".format(i, prev))
            cur_func = func
        i = i + 1
    print("Looks OK")


if __name__ == "__main__":
    main()
