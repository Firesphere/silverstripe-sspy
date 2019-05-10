import gzip
import os
import tarfile
import warnings
import pymysql


class Load:

    def load(self, sspak, basepath):
        self.extract(sspak)
        self.database()
        self.assets(basepath)


    def database(self):
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
                    for q in queries.split(';\n'):
                        try:
                            cursor.execute(q)
                        except:
                            print()
                            # do nothing, continue
                    conn.commit()

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
