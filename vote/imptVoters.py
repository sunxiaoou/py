#! /usr/local/bin/python3

import sys
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from vote import Vote


def main():
    if len(sys.argv) < 2:
        print('Usage: {} file'.format(sys.argv[0]))
        sys.exit(1)

    try:
        client = MongoClient(host="localhost", port=27017)
        print("Connected successfully")
    except ConnectionFailure as e:
        sys.stderr.write("Could not connect to MongoDB: %s" % e)
        sys.exit(1)

    db = client.get_database("example")
    votes = db.votes
    votes.drop()

    file = open(sys.argv[1])
    for line in file.readlines():
        fields = [f.strip() for f in line.strip().split(',')]
        if not fields[-1]:
            continue
        vote = Vote(fields[0], fields[1], fields[2], fields[3], fields[4], '', '')
        pprint(vote.to_dictionary())
        votes.insert_one(vote.to_dictionary())

    print(votes.count_documents({}))


if __name__ == "__main__":
    main()
