#! /usr/local/bin/python3

from datetime import datetime

from vote import Keys
from dbClient import DBClient


def main():
    name = 'chun-yan.zhao'
    options = [1, 2, 4]

    client = DBClient('votes', 'example')
    origin = client.update_one({Keys.name: name}, {Keys.timestamp: datetime.now(), Keys.options: options})

    print('origin: ' + str(origin))
    new = client.find_one({Keys.name: name})
    print('new: ' + str(new))


if __name__ == "__main__":
    main()
