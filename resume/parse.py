#! /usr/bin/python3
#or /opt/python/bin/python3

import json
import os
import re
import shutil
import sys
import traceback

from bson import json_util
from htmlJL import HtmlJL
from htmlJxw import HtmlJxw
from htmlZljl import HtmlZljl
from resume import Keys


def test_one():
    folder = '/home/xixisun/suzy/shoulie/resumes/jl'
    # file = 'jl_0124952_安敬辉.html'
    file = 'jl_0085242_季文清.html'
    # file = 'jl_0000123_郝锐强.html'

    output = open('test.json', 'a')
    resume = HtmlJL.new_resume(os.path.join(folder, file), 1)
    # print(json.dumps(resume.to_dictionary()))
    output.write(json.dumps(resume.to_dictionary(), default=json_util.default))
    output.write('\n')
    output.close()


def parse():
    base_folder = '/home/xixisun/suzy/shoulie/resumes'
    # base_folder = '/scratch/xixisun/shoulie/resumes'
    parser = HtmlJL
    html_type = parser.get_type()
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
            try:
                mo = re.compile(re.escape(html_type) + r'_(\d{7})_\w+\.html').search(fileName)
                if mo is not None:      # no need to change file name
                    resume = parser.new_resume(fn, int(mo.group(1)))
                else:
                    resume = parser.new_resume(fn, i)
                dictionary = resume.to_dictionary()
            except:
                print(traceback.format_exc())
                print(fn + ' failed')
                shutil.move(fn, os.path.join(err_folder, fileName))
                continue
            output.write(json.dumps(dictionary, default=json_util.default))
            output.write('\n')
            new_filename = dictionary.get(Keys.file)
            if fileName != new_filename:
                os.rename(fn, os.path.join(folderName, new_filename))
                print(fileName + ' to ' + new_filename)
            i += 1
            # if i == 1000:
            # break
    output.close()


# test_one()
parse()
sys.exit(0)
