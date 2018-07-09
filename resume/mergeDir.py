#! /usr/bin/python3
#or /opt/python/bin/python3

import os
import shutil


def walk_folder():
    i = 0
    for folderName, subfolders, fileNames in os.walk(src):
        for fileName in fileNames:
            fn = os.path.join(folderName, fileName)
            print('{:07d}, '.format(i + 1) + fn)
            shutil.move(fn, os.path.join(tgt, fileName))
            i += 1
    print(str(i) + ' files moved')


src = '/home/xixisun/suzy/shoulie/resumes/fail'
tgt = '/home/xixisun/suzy/shoulie/resumes/zljl'
walk_folder()
