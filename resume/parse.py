#! /usr/bin/python3
#or /opt/python/bin/python3

import json
import os
import re
import shutil
import sys
import traceback

from bson import json_util
from htmlJ51 import HtmlJ51
from htmlJL import HtmlJL
from htmlJxw import HtmlJxw
from htmlZljl import HtmlZljl
from resume import Keys


def get_parser(name):
    if name == 'j51':
        parser = HtmlJ51
    elif name == 'jl':
        parser = HtmlJL
    elif name == 'jxw':
        parser = HtmlJxw
    elif name == 'zljl':
        parser = HtmlZljl
    else:
        raise TypeError

    assert parser.get_type() == name
    return parser


def parse_one(file):
    # folder = '/home/xixisun/suzy/shoulie/resumes/j51'
    # file = 'jl_0124952_安敬辉.html'
    # file = 'j51_0079223_李智惠.html'

    base = os.path.basename(file)
    parser_name = base.split('_')[0]
    parser = get_parser(parser_name)
    resume = parser.new_resume(file, 1)
    output = open('test.json', 'a')
    # print(json.dumps(resume.to_dictionary()))
    output.write(json.dumps(resume.to_dictionary(True), default=json_util.default))
    output.write('\n')
    output.close()


def parse(folder):
    # base_folder = '/home/xixisun/suzy/shoulie/resumes'
    # base_folder = '/scratch/xixisun/shoulie/resumes'

    parser_name = os.path.basename(folder)
    parser = get_parser(parser_name)

    parent_folder = os.path.dirname(folder)
    err_folder = os.path.join(parent_folder, parser_name + 'err')
    if not os.path.exists(err_folder):
        os.makedirs(err_folder)

    output = open(os.path.join(parent_folder, parser_name + '.json'), 'w')
    i = 1
    for folderName, subfolders, fileNames in os.walk(folder):
        for fileName in fileNames:
            if os.path.splitext(fileName)[1] != '.html':
                continue
            fn = os.path.join(folderName, fileName)
            try:
                mo = re.compile(re.escape(parser_name) + r'_(\d{7})_\w+\.html').search(fileName)
                if mo is not None:      # no need to change file name
                    resume = parser.new_resume(fn, int(mo.group(1)))
                else:
                    resume = parser.new_resume(fn, i)
                dictionary = resume.to_dictionary(True)
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


def main():
    if len(sys.argv) < 2:
        print('Usage: ' + sys.argv[0] + ' file|dir')
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        parse_one(sys.argv[1])
    elif os.path.isdir(sys.argv[1]):
        parse(sys.argv[1])
    else:
        raise TypeError


if __name__ == "__main__":
    main()
