#! /usr/local/bin/python3

from pymongo import MongoClient


class DBClient:
    def __init__(self, collection, db, host="localhost", port=27017):
        client = MongoClient(host, port)
        print("Connected successfully")
        self.collection = client.get_database(db).get_collection(collection)

    def find_one(self, filter):
        return self.collection.find_one(filter)

    def insert_one(self, document):
        return self.collection.insert_one(document)

    def update_one(self, filter, update):
        return self.collection.find_one_and_update(filter, {'$set': update})

    def count(self):
        return self.collection.count_documents({})

    def drop(self):
        self.collection.drop()


def main():
    pass


if __name__ == "__main__":
    main()
