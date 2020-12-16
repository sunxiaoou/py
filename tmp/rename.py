#! /usr/bin/python3

import os
import sys


def rename(dir: str, file: str, ext: str):
    for count, filename in enumerate(sorted(os.listdir(dir))):
        src = dir + filename
        dst = '{}_{:02d}.{}'.format(file, count, ext)
        dst = dir + dst
        print(src, dst)
        os.rename(src, dst)


def main():
    n = len(sys.argv)
    if n < 4:
        print('Usage: ' + sys.argv[0] + ' directory/' + ' file' + ' extension')
        sys.exit(1)
    # sys.stdout.flush()
    rename(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()

