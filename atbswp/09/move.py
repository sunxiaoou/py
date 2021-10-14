#! /usr/bin/python3
import glob
import os
import re
import shutil


def main():
    home = os.path.expanduser('~')
    os.chdir(os.path.join(home, 'Downloads'))

    for dir in glob.glob('*鱿*'):
        source = os.path.join(dir, dir)
        new_name = '鱿鱼游戏_' + re.search('s\d\de\d\d', dir).group() + '.mp4'
        destination = os.path.join(home, 'Movies', '鱿鱼游戏', new_name)
        print(source, destination)
        shutil.copy(source, destination)


if __name__ == "__main__":
    main()
