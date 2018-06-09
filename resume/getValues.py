#! /usr/bin/python3

import re
from pymongo import MongoClient
from datetime import datetime
from pprint import pprint


def get_resumes():
    client = MongoClient('localhost', 27017)
    return client.get_database('shoulie').get_collection('resumes')

"""
def get_years():
    years = set()
    for entry in resumes.find({}, {'工作经验': 1}):
        years.add(entry.get('工作经验'))
    for year in years:
        print(year)


def get_births():
    births = set()
    # for entry in resumes.find({}, {'出生日期': 1}).limit(100):
    for entry in resumes.find({}, {'出生日期': 1}):
        births.add(entry.get('出生日期'))
    for birth in sorted(births):
        print(birth)


def get_field():
    fields = set()
    for entry in resumes.find({}, {'期望从事职业': 1}).limit(100):
        fields.add(entry.get('期望从事职业'))
    for field in sorted(fields):
        print(field)
"""


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
        regex = re.compile(r'\(.*\)')
        v = regex.sub('', entry.get(key))
        # for value in entry.get(key).split('、'):
        for value in re.split('，|、', v):
            values.add(value.upper())
    print('{}({})'.format(key, len(values)))
    for value in sorted(values):
        print(value)



resumes = get_resumes()

# get_values('工作经验')
# get_values('出生日期')
# get_values2('期望从事职业')
get_values2('期望从事行业')





# pprint(resumes.find_one({'姓名': '邹习骏'}))
# pprint(resumes.find_one({'出生日期': datetime(2013, 9, 15)}))
