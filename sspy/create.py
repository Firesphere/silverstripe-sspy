import os
import sys
import tarfile
import time

from sspy import mysqldump


class Create:

    def create(self, db, assets):
        if not db:
            self.database()
        if not assets:
            self.assets()

    def database(self):
        mysqldump.dump(os.getenv('SS_DATABASE_NAME'), os.getenv('SS_DATABASE_SERVER'),
                       os.getenv('SS_DATABASE_USERNAME'), os.getenv('SS_DATABASE_PASSWORD'), 'database.sql.gz', 'gz')

    def assets(self):
        initial = time.time()
        mysqldump.print_message("------------------------------------------------------------------------")
        basedir = os.getcwd()
        workingdir = basedir
        # If the public folder exist, use that one
        if os.path.isdir('public'):
            workingdir = os.path.join(workingdir, 'public')
        workingdir = os.path.join(workingdir, 'assets')
        # write gzip
        with tarfile.open(os.path.join(basedir, "assets.tar.gz"), "w:gz") as tar:
            os.chdir(workingdir)
            mysqldump.print_message("Adding files from '%s' to assets tar. This might take a while" % workingdir)
            # Add all files in working dir
            tar.add('.', filter=filter_output)
            # Go back to base or things will break
            os.chdir(basedir)

        final = time.time()
        delta = final - initial
        print("\nFinished creating assets tar in %d seconds" % delta)

    def sspak(self, file, basepath):
        initial = time.time()
        print("------------------------------------------------------------------------")
        print("Generating %s" % file)
        with tarfile.open(file, "w") as tar:
            if os.path.isfile(os.path.join(basepath, 'database.sql.gz')):
                print("Adding database.sql.gz")
                tar.add('database.sql.gz')
                final = time.time()
                delta = final - initial
                print("Finished adding database in %d seconds" % delta)
            if os.path.isfile(os.path.join(basepath, 'assets.tar.gz')):
                print("adding assets.tar.gz")
                tar.add('assets.tar.gz')
                final = time.time()
                delta = final - initial
                print("Finished adding assets in %d seconds" % delta)
        print("------------------------------------------------------------------------")


def filter_output(output):
    sys.stdout.write("\r%s" % (100 * " "))
    sys.stdout.write("\radding %s" % output.name)
    return output
