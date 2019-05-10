import gzip
import os
import tarfile
import warnings
import pymysql
import sys
from helpers import mysqldump

class Load:

    def load(self, sspak, basepath):
        mysqldump.print_message("Extracting sspak %s" % sspak)
        self.extract(sspak)
        self.database()
        self.assets(basepath)


    def database(self):
        print('------------------------------------------------------------------------')
        print("Importing database")
        conn = pymysql.connect(
            os.getenv('SS_DATABASE_SERVER'),
            db=os.getenv('SS_DATABASE_NAME'),
            user=os.getenv('SS_DATABASE_USERNAME'),
            password=os.getenv('SS_DATABASE_PASSWORD')
        )
        with gzip.open('database.sql.gz', 'r') as database:
            queries = database.read().decode()
            with warnings.catch_warnings():
                # suppress warnings from the database about keys and such. They're not elephant
                warnings.simplefilter("ignore")
                # Put here your query raising a warning
                with conn.cursor() as cursor:
                    # split on ; and newline. We don't just want to split on ;
                    # because that'll cause content having ; in them to break catastrophically
                    # luckily, the content plus newline is outputted as a string `;\n` instead
                    # of an actual newline
                    queries = queries.split(";\n")
                    i = 1
                    sys.stdout.write("Running %s queries\n" % len(queries))
                    for q in queries:
                        query_parts = q.split('`')
                        try:
                            if len(query_parts) >= 2:
                                msg = "\r[%s/%s] restoring database %s" % (i, len(queries), query_parts[1])
                                sys.stdout.write(msg)
                            cursor.execute(q)
                        except Exception as e:
                            print("Encountered an error, exiting import process\n")
                            print(e)
                            exit(255)
                        i += 1
                        sys.stdout.write("\r%s" % (80 * " "))
                    conn.commit()
                    # Create a newline at the end to not break other messages
                    sys.stdout.write("\nFinished %s queries" % i)
                    print('------------------------------------------------------------------------')

    def assets(self, basedir):
        workingdir = basedir
        # If the public folder exist, use that one
        if os.path.isdir('public'):
            workingdir = os.path.join(workingdir, 'public')
        workingdir = os.path.join(workingdir, 'assets')
        # write gzip
        with tarfile.open("assets.tar.gz", "w:gz") as tar:
            tar.extractall(path=os.path.join(workingdir, "assets/"))

    def extract(self, file):
        with tarfile.open(file, 'r') as tar:
            tar.extractall()
