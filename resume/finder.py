#! /usr/bin/python3

import datetime
import shelve
import webbrowser
from pymongo import MongoClient

from condition import Condition
from reporter import Reporter


class Finder:

    @staticmethod
    def get_collection(host, port, database, collection_name):
        client = MongoClient(host, port)
        return client.get_database(database).get_collection(collection_name)

    @staticmethod
    def get_conditions():
        """
        ex = {'$or': [{'技能.熟练': 'JAVA'}, {'技能.精通': 'JAVA'}],
              '出生日期': {'$gte': datetime.datetime(1978, 6, 16, 0, 0)},
              '学历': {'$gte': 2},
              '教育经历.学校类别': 1,
              '工作年限': {'$gte': 5, '$lt': 10},
              # '期望从事职业': {'$regex': '程序员'},
              # '期望从事行业': {'$regex': 'IT'},
              '期望工作地点': '北京'}
        """
        conditions = Condition.create_conditions()
        print('\nInput any key to continue ...')
        input()
        return conditions

    @staticmethod
    def find(resumes, conditions):
        cursor = resumes.find(conditions)
        num = cursor.count()
        print('Found {} documents'.format(num))
        return list(cursor)

    @staticmethod
    def shelve(documents, file):
        print('Shelved to ' + file)
        shelf = shelve.open(file)
        shelf['result'] = documents
        shelf.close()

    @staticmethod
    def to_html(documents, file):
        Reporter.output(documents, file)
        webbrowser.open(file)


if __name__ == "__main__":
    result = Finder.find(Finder.get_collection('localhost', 27017, 'shoulie', 'resumes'), Finder.get_conditions())
    if result is not None:
        Finder.shelve(result, 'result.dat')
        Finder.to_html(result, 'result.html')
