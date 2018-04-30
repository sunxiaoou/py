#! /usr/bin/python3

import sqlite3


class DbClient:
    def __init__(self, dbFile):
        self.conn = sqlite3.connect(dbFile)
        self.curs = self.conn.cursor()

    def execute(self, cmd):
        self.curs.execute(cmd)

    def close(self):
        self.conn.commit()
        self.conn.close()

