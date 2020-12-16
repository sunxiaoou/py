#! /usr/bin/python3

import os
import sys


def rename(dir: str):
    for count, f in enumerate(sorted(os.listdir(dir))):
        src = dir + f
        name, ext = os.path.splitext(f)
        # dst = '{}_{:02d}{}'.format(name.split(" ")[0], count + 1, ext)
        dst = '{}{}'.format(name.split(" ")[0], ext)
        dst = dir + dst
        if src != dst:
            print(src, dst)
            os.rename(src, dst)


def main():
    n = len(sys.argv)
    if n < 2:
        print('Usage: ' + sys.argv[0] + ' directory/')
        sys.exit(1)
    # sys.stdout.flush()
    rename(sys.argv[1])


if __name__ == "__main__":
    main()

