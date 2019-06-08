#! /usr/local/bin/python3

import sys
from pprint import pprint

from vote import Vote
from dbClient import DBClient


def main():
    if len(sys.argv) < 2:
        print('Usage: {} file'.format(sys.argv[0]))
        sys.exit(1)

    client = DBClient('votes', 'example')
    client.drop()

    file = open(sys.argv[1])
    for line in file.readlines():
        fields = [f.strip() for f in line.strip().split(',')]
        if not fields[-1]:
            continue
        vote = Vote(fields[0], fields[1], fields[2], fields[3], fields[4], '', '')
        pprint(vote.to_dictionary())
        client.insert_one(vote.to_dictionary())

    print(client.count())


if __name__ == "__main__":
    main()
