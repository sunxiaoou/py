#! /usr/bin/python3

import sqlite3


class DbClient:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.curs = self.conn.cursor()

    def execute(self, cmd):
        self.curs.execute(cmd)

    def close(self):
        self.conn.commit()
        self.conn.close()

