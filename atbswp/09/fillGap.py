#! /usr/bin/python3
# Write a program that finds all files with a given prefix, such as
# spam001.txt, spam002.txt, and so on, in a single folder and locates any gaps in the numbering
# (such as if there is a spam001.txt and spam003.txt but no spam002.txt).
# Have the program rename all the later files to close this gap.

import re, os, shutil, sys

def fillGap(prefix, folder):
    if os.path.exists(folder)  == False:
        print('Cannot find dir \'%s\'' % folder)
        return

    regex = re.compile(r'^({0})(\d\d\d)(.*)$'.format(prefix))
    os.chdir(folder)
    files = []
    for filename in os.listdir():
        if regex.search(filename) != None:
            files.append(filename)

    files.sort()
    for i in range(len(files)):
        mo = regex.search(files[i])
        if int(mo.group(2)) != i:
            new = mo.group(1) + '%03d' % i + mo.group(3)   
            print('Rename "%s" to "%s"...' % (files[i], new))
            shutil.move(files[i], new)

if len(sys.argv) < 3:
    print('Usage: ' + sys.argv[0] + 'prefix folder')
    sys.exit(1)
fillGap(sys.argv[1], sys.argv[2])
