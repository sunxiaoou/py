#! /usr/bin/python3

import os
import sys
import time
from htmlParser import HtmlParser
from dbClient import DbClient


def test_one():
    folder = '/home/xixisun/suzy/resumes/0001/2'
    # file = 'jm089638951r90250000000_2015-01-28_0.html'
    # file = 'jm090122773r90250000000_2015-03-08_0.html'
    # file = 'jm089867313r90250005000_2015-08-06_0.html'
    file = 'jm170222194r90250000000.html'
    # file = 'jm337520048r90250001000.html'
    # file = 'jm328873785r90250000000.html'
    parser = HtmlParser(folder + '/' + file)
    resume = parser.new_resume()
    print(resume)
    for cmd in resume.insert_cmds():
        print(cmd)
        # dbClient.execute(cmd)


def parse():
    folder = '/home/xixisun/suzy/resumes/0001/2'
    for folderName, subfolders, fileNames in os.walk(folder):
        for fileName in fileNames:
            if os.path.splitext(fileName)[1] != '.html':
                continue
            fn = folderName + '/' + fileName
            print(fn)
            parser = HtmlParser(fn)
            resume = parser.new_resume()
            # print(resume)
            for cmd in resume.insert_cmds():
                # pass
                print(cmd)
                dbClient.execute(cmd)
                # print()
                # time.sleep(1)


dbFile = 'shoulie.sqlite'
dbClient = DbClient(dbFile)
test_one()
# parse()
dbClient.close()
sys.exit(0)
