#! /usr/bin/python3
#or /opt/python/bin/python3


import json
import os
from pprint import pprint

base_folder = '/home/xixisun/suzy/shoulie/resumes'
# base_folder = '/scratch/xixisun/shoulie/resumes'
filename = 'j51.json'

json_file = open(os.path.join(base_folder, filename))

len_count = {}
len_sum = 0
while True:
    a = json_file.readline()
    if not a:
        break

    dict = json.loads(a)
    file = dict.get('file')
    length = len(a)
    len_sum += length
    len_count[file] = length

num = len(len_count)
print('Total {:d} files, average {:d}'.format(num, len_sum // num))     # return integer instead of float
len_count_sorted = sorted(len_count.items(), key=lambda kv: kv[1], reverse=True)
pprint(len_count_sorted)
