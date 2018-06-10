#! /usr/bin/python3

import re
from pymongo import MongoClient
from datetime import datetime
from pprint import pprint


def get_resumes():
    client = MongoClient('localhost', 27017)
    return client.get_database('shoulie').get_collection('resumes')


def get_values(key):
    values = set()
    # for entry in resumes.find({}, {key: 1}).limit(100):
    for entry in resumes.find({}, {key: 1}):
        values.add(entry.get(key))
    print('{}({})'.format(key, len(values)))
    for value in sorted(values):
        print(value)


def get_values2(key):
    values = set()
    # for entry in resumes.find({}, {key: 1}).limit(100):
    for entry in resumes.find({}, {key: 1}):
        for value in entry.get(key):
            # values.add(value.upper())
            values.add(value)
    print('{}({})'.format(key, len(values)))
    for value in sorted(values):
        print(value)



resumes = get_resumes()

# get_values('工作经验')
# get_values('出生日期')
get_values2('期望从事职业')
# get_values2('期望从事行业')





# pprint(resumes.find_one({'姓名': '邹习骏'}))
# pprint(resumes.find_one({'出生日期': datetime(2013, 9, 15)}))
