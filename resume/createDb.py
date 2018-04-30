#! /usr/bin/python3

import sqlite3


def create_tabs():
    cmd = 'CREATE TABLE person ' +\
          '(file TEXT, name TEXT, gender TEXT, birth TEXT, email TEXT, phone INTEGER PRIMARY KEY)'
    print(cmd)
    curs.execute(cmd)

    cmd = 'CREATE TABLE objective ' +\
          '(spot TEXT, salary INTEGER, field TEXT, industry TEXT, phone INTEGER, ' +\
          'FOREIGN KEY(phone) REFERENCES person(phone))'
    print(cmd)
    curs.execute(cmd)

    cmd = 'CREATE TABLE experience ' +\
          '(start_date TEXT, end_date TEXT, company TEXT, job TEXT, phone INTEGER, ' +\
          'FOREIGN KEY(phone) REFERENCES person(phone))'
    print(cmd)
    curs.execute(cmd)

    cmd = 'CREATE TABLE education ' +\
          '(start_date TEXT, end_date TEXT, school TEXT, major TEXT, degree TEXT, phone INTEGER, ' +\
          'FOREIGN KEY(phone) REFERENCES person(phone))'
    print(cmd)
    curs.execute(cmd)


def drop_tabs():
    cmd = 'DROP TABLE IF EXISTS person'
    print(cmd)
    curs.execute(cmd)
    cmd = 'DROP TABLE IF EXISTS objective'
    print(cmd)
    curs.execute(cmd)
    cmd = 'DROP TABLE IF EXISTS experience'
    print(cmd)
    curs.execute(cmd)
    cmd = 'DROP TABLE IF EXISTS education'
    print(cmd)
    curs.execute(cmd)


dbFile = 'shoulie.sqlite'
conn = sqlite3.connect(dbFile)
curs = conn.cursor()

# drop_tabs()
create_tabs()

conn.commit()
conn.close()
