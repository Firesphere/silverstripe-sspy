import os

import pymysql


class ListTables:
    def __init__(self):
        self.connection = pymysql.connect(
            host=os.getenv('SS_DATABASE_SERVER'),
            database=os.getenv('SS_DATABASE_NAME'),
            user=os.getenv('SS_DATABASE_USERNAME'),
            passwd=os.getenv('SS_DATABASE_PASSWORD')
        )

    def show_tables(self):
        with self.connection.cursor() as cursor:
            count = cursor.execute(
                "SELECT `table_name` FROM `information_schema`.`tables` WHERE `table_schema` = '%s'" % os.getenv('SS_DATABASE_NAME')
            )
            print("Table count: %s" % count)
            tables = cursor.fetchall()

            for table in tables:
                query = "SELECT COUNT(`ID`) FROM `%s`" % table
                cursor.execute(query)
                query = cursor.fetchall()
                print('%s : (%s)' % (table[0], query[0][0]))
        self.connection.close()
