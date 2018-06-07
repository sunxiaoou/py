#! /usr/bin/python3

import json
import os
import sys
import time
from htmlParser import HtmlParser
from htmlJL import HtmlJL
# from dbClient import DbClient


def test_one():
    # folder = '/home/xixisun/suzy/resumes/0001/2'
    # file = 'jm089638951r90250000000_2015-01-28_0.html'
    # file = 'jm090122773r90250000000_2015-03-08_0.html'
    # file = 'jm089867313r90250005000_2015-08-06_0.html'
    # file = 'jm170222194r90250000000.html'
    # file = 'jm337520048r90250001000.html'
    # file = 'jm328873785r90250000000.html'
    # parser = HtmlParser(folder + '/' + file)

    folder = '/home/xixisun/suzy/resumes/html/jl'
    file = '10052356-安敬辉.html'

    output = open('jl.out', 'w')
    parser = HtmlJL(folder + '/' + file)
    resume = parser.new_resume()
    # print(json.dumps(resume.to_dictionary()))
    output.write(json.dumps(resume.to_dictionary()))
    output.close()


def parse():
    folder = '/home/xixisun/suzy/resumes/html/jl'
    output = open('jl.out', 'w')
    # i = 0
    for folderName, subfolders, fileNames in os.walk(folder):
        for fileName in fileNames:
            if os.path.splitext(fileName)[1] != '.html':
                continue
            fn = folderName + '/' + fileName
            print(fn)
            parser = HtmlJL(fn)
            resume = parser.new_resume()
            output.write(json.dumps(resume.to_dictionary()))
            output.write('\n')
            # i += 1
            # if i == 1000:
                # break
    output.close()


# test_one()
parse()
sys.exit(0)
