#! /opt/python/bin/python3
#or /usr/bin/python3

import os
import shutil
from pprint import pprint


def walk_folder():
    i = 0
    for folderName, subfolders, fileNames in os.walk(new2):
        for fileName in fileNames:
            fn = folderName + '/' + fileName
            print('{:07d}, '.format(i + 1) + fn)
            shutil.move(fn, os.path.join(new, fileName))
            i += 1
    print(str(i) + ' files moved')


new = '/scratch/xixisun/shoulie/new/zljl'
new2 = '/scratch/xixisun/shoulie/new.2/zljl'
walk_folder()
