#! /usr/local/bin/python3

import datetime
import os
import re
import shelve
import sys
import webbrowser
import zipfile
from pymongo import MongoClient

from reporter import Reporter
from resume import Keys


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

    @staticmethod
    def package(documents, base_folder, file):
        archive = zipfile.ZipFile(file, 'w')
        current_dir = os.getcwd()
        os.chdir(base_folder)
        num = min(100, len(documents))
        for i in range(num):
            html = documents[i].get(Keys.file)
            html_type = re.compile(r'^(\w+)_\d+').search(html).group(1)
            full_file_name = os.path.join(html_type, html)
            archive.write(full_file_name)
        os.chdir(current_dir)
        archive.close()
        print('{:d} htmls added to archive {}'.format(num, file))


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
        Finder.package(documents, sys.argv[2], 'finder_result.zip')


if __name__ == "__main__":
    main()
