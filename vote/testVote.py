#! /usr/local/bin/python3

import sys

from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def main():
    record = {
        # '_id': 0,
        'name': 'xiao.ou.sun',
        # 'date': datetime.now(),
        'options': [1, 2, 4]
    }

    try:
        client = MongoClient(host="localhost", port=27017)
        print("Connected successfully")
    except ConnectionFailure as e:
        sys.stderr.write("Could not connect to MongoDB: %s" % e)
        sys.exit(1)

    db = client.get_database("example")
    records = db.records

    if records.count_documents({'name': record['name']}):
        records.delete_many({'name': record['name']})

    records.insert_one(record)
    record['options'] = [3, 4, 7, 8]
    # origin = records.find_one_and_replace({'name': record['name']}, record, upsert=True)
    origin = records.find_one_and_update(
        {'name': record['name']}, {'$set': {'date': datetime.now(), 'options': [3, 4, 7, 8]}})
    print('origin: ' + str(origin))
    for r in records.find({'name': record['name']}):
        print(r)


if __name__ == "__main__":
    main()
