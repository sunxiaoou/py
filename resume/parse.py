#! /usr/bin/python3
#or /opt/python/bin/python3

import json
import os
import shutil
import sys
import traceback

from bson import json_util
from htmlParser import HtmlParser
from htmlJL import HtmlJL
from resume import Keys


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
    base_folder = '/home/xixisun/suzy/shoulie/resumes'
    # base_folder = '/scratch/xixisun/shoulie/resumes'
    html_type = 'jl'
    html_folder = os.path.join(base_folder, html_type)
    err_folder = os.path.join(base_folder, html_type + 'err')
    if not os.path.exists(err_folder):
        os.makedirs(err_folder)

    output = open(os.path.join(base_folder, html_type + '.json'), 'w')
    i = 1
    for folderName, subfolders, fileNames in os.walk(html_folder):
        for fileName in fileNames:
            if os.path.splitext(fileName)[1] != '.html':
                continue
            fn = os.path.join(folderName, fileName)
            # parser = HtmlParser(fn, i)
            parser = HtmlJL(fn, i)
            try:
                resume = parser.new_resume()
                dictionary = resume.to_dictionary()
            except:
                print(traceback.format_exc())
                print(fn + ' failed')
                shutil.move(fn, os.path.join(err_folder, fileName))
                continue
            output.write(json.dumps(dictionary, default=json_util.default))
            output.write('\n')
            new_filename = dictionary.get(Keys.file)
            os.rename(fn, os.path.join(folderName, new_filename))
            print(fileName + ' to ' + new_filename)
            i += 1
            # if i == 1000:
            # break
    output.close()


# test_one()
parse()
sys.exit(0)
