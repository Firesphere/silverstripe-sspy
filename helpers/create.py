import os
import tarfile
import time

from helpers import mysqldump


class Create:
    @staticmethod
    def create():
        Create.database()
        Create.assets()

    @staticmethod
    def database():
        mysqldump.dump(os.getenv('SS_DATABASE_NAME'), os.getenv('SS_DATABASE_SERVER'),
                       os.getenv('SS_DATABASE_USERNAME'), os.getenv('SS_DATABASE_PASSWORD'))

    @staticmethod
    def assets():
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
            mysqldump.print_message("Adding files from '%s' to assets tar" % workingdir)
            # Add all files in working dir
            tar.add('.')
            # Go back to base or things will break
            os.chdir(basedir)

        final = time.time()
        delta = final - initial
        mysqldump.print_message("Finished creating assets tar in %d seconds" % delta)
