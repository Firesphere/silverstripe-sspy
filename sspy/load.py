import gzip
import os
import sys
import tarfile
import warnings

import pymysql


class Load:

    def load(self, sspak, basepath):
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
            queries = queries.split(";\n")
            i = 1
            sys.stdout.write("Running %s queries\n" % len(queries))
            with warnings.catch_warnings():
                # suppress warnings from the database about keys and such. They're not elephant
                warnings.simplefilter("ignore")
                # Put here your query raising a warning
                with conn.cursor() as cursor:
                    # split on ; and newline. We don't just want to split on ;
                    # because that'll cause content having ; in them to break catastrophically
                    # luckily, the content plus newline is outputted as a string `;\n` instead
                    # of an actual newline
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
        conn.close()
        print('------------------------------------------------------------------------')

    def assets(self, basedir):
        print('------------------------------------------------------------------------')
        print("Extracting assets")
        workingdir = basedir
        # If the public folder exist, use that one
        if os.path.isdir('public'):
            workingdir = os.path.join(workingdir, 'public')
        workingdir = os.path.join(workingdir, 'assets')
        # write gzip
        with tarfile.open("assets.tar.gz", "w:gz") as tar:
            tar.extractall(path=os.path.join(workingdir, "assets/"))

    def extract(self, file):
        print('------------------------------------------------------------------------')
        print("Extracting sspak")
        with tarfile.open(file, 'r') as tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar)
