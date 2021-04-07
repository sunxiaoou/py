#! /usr/bin/python3
# To walk through a folder tree and searches for exceptionally large files or folders—say,
# ones that have a file size of more than 100MB. 

import os, sys

def findBigFiles(folder):
    if os.path.exists(folder)  == False:
        print('Cannot find dir \'%s\'' % folder)
        return

    for foldername, subfolders, filenames in os.walk(folder):
        for filename in filenames:
            filename = os.path.join(foldername, filename)
            size = os.path.getsize(filename)
            if size > 1024 * 1024 * 100:
                print('%s - %d' % (filename, size))

if len(sys.argv) < 2:
    print('Usage: ' + sys.argv[0] + ' folder')
    sys.exit(1)
findBigFiles(sys.argv[1])
