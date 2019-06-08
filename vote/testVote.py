#! /usr/local/bin/python3

from datetime import datetime

from vote import Keys
from dbClient import DBClient


def main():
    # name = 'chun-yan.zhao'
    # options = [1, 2, 4]
    name = 'susie.liu'
    options = [2, 3, 4, 6]

    client = DBClient('votes', 'example')
    origin = client.update_one({Keys.name: name}, {Keys.timestamp: datetime.now(), Keys.options: options})

    print('origin: ' + str(origin))
    new = client.find_one({Keys.name: name})
    print('new: ' + str(new))

    count = {}
    for r in client.find({}, {Keys._id: False, Keys.options: True}):
        if r:
            print(r[Keys.options])
            for i in r[Keys.options]:
                if i not in count.keys():
                    count[i] = 1
                else:
                    count[i] += 1
    print(count)


if __name__ == "__main__":
    main()
