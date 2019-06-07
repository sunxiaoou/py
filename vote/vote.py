#! /usr/local/bin/python3

import hashlib


class Keys:
    _id = '_id'
    name = 'name'
    phone = 'phone'
    center = 'center'
    location = 'location'
    manager = 'manager'
    options = 'options'
    timestamp = 'timestamp'


class Vote:
    def __init__(self, name, phone, center, location, manager, options, timestamp):
        self.name = name
        self.phone = phone
        self.center = center
        self.location = location
        self.manager = manager
        self.options = options
        self.timestamp = timestamp

    def to_dictionary(self):
        vote = {Keys.name: self.name,
                Keys._id: int(hashlib.sha1(self.name.encode('utf-8')).hexdigest(), 16) % (10 ** 9)}

        if self.phone:
            vote[Keys.phone] = self.phone
        if self.center:
            vote[Keys.center] = self.center
        if self.location:
            vote[Keys.location] = self.location
        if self.manager:
            vote[Keys.manager] = self.manager
        if self.options:
            vote[Keys.options] = self.options
        if self.timestamp:
            vote[Keys.timestamp] = self.timestamp
        return vote


def main():
    pass


if __name__ == "__main__":
    main()
