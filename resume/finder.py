#! /usr/bin/python3

import os
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
    def find(resumes, conditions):
        cursor = resumes.find(conditions, {'_id': False})
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
        html = open(file, 'w')
        html.write(Reporter.to_html(documents))
        html.close()
        webbrowser.open('file://{}/{}'.format(os.getcwd(), file))


def main():
    entries = Condition.input()
    conditions = Condition.create_conditions(entries)
    print('\nInput any key to continue ...')
    input()
    result = Finder.find(Finder.get_collection('localhost', 27017, 'shoulie', 'resumes'), conditions)
    if result:
        Finder.shelve(result, 'result.dat')
        Finder.to_html(result, 'result.html')


if __name__ == "__main__":
    main()
