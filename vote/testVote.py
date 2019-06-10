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

    counter = {}
    for r in client.find({}, {Keys._id: False, Keys.options: True}):
        if r:
            print(r[Keys.options])
            for i in r[Keys.options]:
                if i not in counter.keys():
                    counter[i] = 1
                else:
                    counter[i] += 1
    print(counter)
    lst = []

    for i in range(int(max(counter, key=int))):
        if i + 1 in counter.keys():
            lst.append(counter[i + 1])
        else:
            lst.append(0)
    print(lst)


if __name__ == "__main__":
    main()
