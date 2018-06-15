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


def query_field(value):
    key = 'file'
    names = []
    for entry in resumes.find({'期望从事职业': {'$regex': value}}, {'_id': 0, key: 1}).limit(100):
        names.append(entry.get(key))
    return names if names else None


def query_skill(value):
    key = 'file'
    names = []
    for entry in resumes.find({'$or': [{'技能.熟练': value}, {'技能.精通': value}]}, {'_id': 0, key: 1}).limit(100):
        names.append(entry.get(key))
    return names if names else None


def query_years(num1, num2):
    if num1 is None and num2 is None:
        return None

    conditions = {}
    if num1 is not None:
        conditions['$gte'] = num1
    if num2 is not None:
        conditions['$lt'] = num2

    key = '姓名'
    names = []
    for entry in resumes.find({'工作经验': conditions}, {key: 1}).limit(100):
        names.append(entry.get(key))
    return names if names else None


def query_age(num1, num2):
    if num1 is None and num2 is None:
        return None

    today = datetime.today()
    date1 = datetime(today.year - num2, today.month, today.day)
    date2 = datetime(today.year - num1, today.month, today.day)

    conditions = {}
    if num1 is not None:
        conditions['$gte'] = date1
    if num2 is not None:
        conditions['$lt'] = date2

    key = '姓名'
    names = []
    for entry in resumes.find({'出生日期': conditions}, {key: 1}).limit(100):
        names.append(entry.get(key))
    return names if names else None


resumes = get_resumes()

# get_values('工作经验')
# get_values('出生日期')
# get_values2('期望从事职业')
# get_values2('期望从事行业')

# pprint(query_field('C\+\+'))
pprint(query_skill('PYTHON'))
# pprint(query_years(10, 12))
# pprint(query_age(35, 40))

# pprint(resumes.find_one({'姓名': '邹习骏'}))
# pprint(resumes.find_one({'出生日期': datetime(2013, 9, 15)}))
