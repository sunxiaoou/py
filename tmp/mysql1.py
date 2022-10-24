#! /usr/bin/python3

import pymysql


def main():
    db_host = 'localhost'
    # db_user = 'root'
    # db_pass = 'abc123'
    # db_database = 'mysql'
    db_user = 'manga'
    db_pass = 'manga'
    db_database = 'manga'
    db_port = 3306

    conn = pymysql.connect(host=db_host, port=db_port, user=db_user,
                           password=db_pass, db=db_database)
    # sqlstr = """
    #     select user, host from user
    # """
    sqlstr = 'select name, price from fruit'
    cursor = conn.cursor()
    cursor.execute(sqlstr)
    result = cursor.fetchall()
    for i in result:
        print("user:%s host:%s" %(i[0], i[1]))
    conn.close()


if __name__ == "__main__":
    main()
