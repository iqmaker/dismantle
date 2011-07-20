# -*- coding: utf-8 -*-
import sys
import MySQLdb
import os
sys.path.append( "../")
from settings import DATABASES
update_files = [ '01.sql', '05.sql' ]

DB = DATABASES[ 'default' ]['NAME']
DB_HOST = DATABASES[ 'default' ]['HOST']
DB_USER = DATABASES[ 'default' ]['USER']
DB_PASSWORD = DATABASES[ 'default' ]['PASSWORD']


def mysql_init():
    for i in update_files:
        command = "mysql -u%s"% DB_USER
        if DB_PASSWORD != '':
            command += ' -p%s'% DB_PASSWORD
        if DB_HOST != '':
            command += ' -h%s'% DB_HOST
        command += ' %s < %s' % ( DB, i )
        print command
        os.system( command )

        #command = "mysql -u%s -p%s -h%s %s < %s" % ( DB_USER, DB_PASSWORD, DB_HOST, DB, i )
def mysql_init2():
    conn = MySQLdb.Connection(db=DB, host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD)
    cursor = conn.cursor()
    for i in update_files:
        print i
        for line in open( i, "r").readlines():
            sql = line
            cursor.execute(sql)
            results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def main():
    mysql_init()

if __name__ == "__main__":
    main()
