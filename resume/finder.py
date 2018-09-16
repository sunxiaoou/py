#! /usr/bin/python3

import datetime
import os
import shelve
import sys
import webbrowser
from pymongo import MongoClient

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
    def to_html(documents, base_folder, file):
        html = open(file, 'w')
        html.write(Reporter.to_html(documents, base_folder))
        html.close()
        webbrowser.open('file://{}/{}'.format(os.getcwd(), file))


def main():
    if len(sys.argv) < 3:
        print('Usage: {} condition_file base_folder'.format(sys.argv[0]))
        sys.exit(1)

    file = open(sys.argv[1])
    conditions = eval(file.read())
    documents = Finder.find(Finder.get_collection('localhost', 27017, 'shoulie', 'resumes'), conditions)
    if documents:
        # Finder.shelve(documents, 'finder_result.dat')
        Finder.to_html(documents, sys.argv[2], 'finder_result.html')


if __name__ == "__main__":
    main()
