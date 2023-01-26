#! /usr/bin/python3

import os
import sys


def rename(dir: str, file: str, ext: str):
    for i, filename in enumerate(sorted(os.listdir(dir))):
        if filename.endswith(ext):
            src = filename if dir == '.' else dir + filename
            dst = '{}_{:02d}.{}'.format(file, i + 1, ext)
            if dir != '.':
                dst = dir + dst
            print('mv "%s" %s' % (src, dst))
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

