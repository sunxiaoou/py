#! /usr/bin/python3

import os
import shutil
from datetime import datetime
from pprint import pprint


# def get_year(file):
#    return datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y')


def walk_folder(path):
    years = {}
    # outputs = {}
    os.chdir(path)
    i = 0
    # print("Counting ...")
    for folderName, subfolders, fileNames in os.walk(folder):
        for fileName in fileNames:
            fn = folderName + '/' + fileName
            year = datetime.fromtimestamp(os.path.getmtime(fn)).strftime('%Y')
            print('{:07d}, '.format(i + 1) + fn + ', ' + year)
            if year not in years.keys():
                years[year] = 1
                # output = open(year + '.out', 'w')
                # outputs[year] = output
            else:
                years[year] += 1
                # output = outputs.get(year)
            if int(year) <= 2010:
                try:
                    shutil.move(fn, old)
                except shutil.Error:
                    pass
            # output.write(fn)
            # output.write('\n')
            i += 1
    # for output in outputs.values():
        # output.close()
    pprint(years)


folder = '/home/xixisun/suzy/resumes/dirs'
old = '/home/xixisun/suzy/resumes/old'
walk_folder(folder)
