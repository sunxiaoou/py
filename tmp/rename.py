#! /usr/bin/python3

import os
import re
import sys


def rename(path: str, src: str, tgt: str, start_no: int):
    os.chdir(path)
    todo = []
    done = []
    for name in os.listdir('.'):
        if re.match(src, name):
            todo.append(name)
        elif re.match(tgt, name):
            done.append(name)
    # print(todo)
    # print(done)

    for i, src_name in enumerate(sorted(todo)):
        serial_no = '_%02d' % (i + start_no + len(done))
        tgt_name = tgt.replace('_??', serial_no)
        if not os.path.isfile(tgt_name):
            print('mv "%s" %s' % (src_name, tgt_name))
            if sys.argv[-1] == 'fire':
                os.rename(src_name, tgt_name)


def main():
    n = len(sys.argv)
    if n < 4:
        print('Usage:   %s path src tgt [start_no] [fire]' % sys.argv[0])
        print('example: %s summertime.*\\.mp4 summerTimeRender_??.mp4 6' % sys.argv[0])
        sys.exit(1)
    start_no = 1 if n < 5 else int(sys.argv[4])
    rename(sys.argv[1], sys.argv[2], sys.argv[3], start_no)


if __name__ == "__main__":
    main()
