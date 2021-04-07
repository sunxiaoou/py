#! /usr/bin/python3
# To walk through a folder tree and searches for files with a certain file extension
# (such as .pdf or .jpg). Copy these files from whatever location they are in to a new folder.

import os, shutil, sys

def copyTypedFiles(ext, current, new):
    if os.path.exists(current)  == False:
        # print('Cannot find dir ' + current)
        print('Cannot find dir \'%s\'' % current)
        return
    if os.path.exists(new)  == False:
        os.makedirs(new)

    for foldername, subfolders, filenames in os.walk(current):
        if os.path.abspath(foldername) == os.path.abspath(new):
            continue
        for filename in filenames:
            if filename.endswith('.' + ext):
                print('cp %s %s' % (os.path.join(foldername, filename), new))
                shutil.copy(os.path.join(foldername, filename), new)

if len(sys.argv) < 4:
    print('Usage: ' + sys.argv[0] + ' extension currDir newDir')
    sys.exit(1)
copyTypedFiles(sys.argv[1], sys.argv[2], sys.argv[3])
