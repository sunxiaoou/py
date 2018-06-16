#! /usr/bin/python3

import datetime
import shelve
import webbrowser
from pymongo import MongoClient
from pprint import pprint

from condition import Condition


class Finder:

    def __init__(self, host, port, database, collection):
        client = MongoClient(host, port)
        self.collection = client.get_database(database).get_collection(collection)
        """
        self.conditions = {'$or': [{'技能.熟练': 'JAVA'}, {'技能.精通': 'JAVA'}],
                           # '专业': '计算机科学',
                           '出生日期': {'$gte': datetime.datetime(1978, 6, 16, 0, 0)},
                           '学历': {'$gte': 2},
                           '教育经历.学校类别': 1,
                           '工作经验': {'$gte': 5, '$lt': 10},
                           # '期望从事职业': {'$regex': '程序员'},
                           # '期望从事行业': {'$regex': 'IT'},
                           '期望工作地点': '北京'}
        """
        self.conditions = Condition.create_conditions()

    def find(self):
        key = 'file'
        cursor = self.collection.find(self.conditions, {'_id': 0, key: 1})
        num = cursor.count()
        print('Found {} documents'.format(num))
        files = []
        # for entry in cursor.limit(num if num < 10 else 10):
        for entry in cursor:
            files.append(entry.get(key))
        return files if files else None

    @staticmethod
    def shelve(result, fname):
        file = shelve.open(fname)
        file['result'] = result
        file.close()


if __name__ == "__main__":
    finder = Finder('localhost', 27017, 'shoulie', 'resumes')
    pprint(finder.conditions)
    print('\nInput any key to continue ...')
    input()
    print('Searching ...')
    # pprint(finder.find())
    r = finder.find()
    if r is not None:
        fn = 'result.dat'
        Finder.shelve(r, fn)
        print('Shelved to ' + fn)
        path = '/home/xixisun/suzy/resumes/html/jl'
        for i in range(min(5, len(r))):
            print(r[i])
            webbrowser.open(path + '/' + r[i])

