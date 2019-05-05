import os

from helpers import mysqldump


class Create:
    @staticmethod
    def create(args):
        Create.database(args)

    @staticmethod
    def database(args):
        filename = 'database.sql'
        if 3 < len(args):
            filename = args[2]
        mysqldump.dump(os.getenv('SS_DATABASE_NAME'), os.getenv('SS_DATABASE_SERVER'),
                       os.getenv('SS_DATABASE_USERNAME'), os.getenv('SS_DATABASE_PASSWORD'), filename)

    @staticmethod
    def assets(args):
        path = args[1]