import os
import tarfile
from helpers import mysqldump
import time

class Create:
    @staticmethod
    def create(args):
        Create.database(args)
        Create.assets()

    @staticmethod
    def database(args):
        mysqldump.dump(os.getenv('SS_DATABASE_NAME'), os.getenv('SS_DATABASE_SERVER'),
                       os.getenv('SS_DATABASE_USERNAME'), os.getenv('SS_DATABASE_PASSWORD'), 'database.sql')

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
        tar = tarfile.open(os.path.join(basedir, "assets.tar.gz"), "w:gz")
        os.chdir(workingdir)
        mysqldump.print_message("Adding files from '%s' to assets tar" % workingdir)
        # Add all files in working dir
        tar.add('.')
        final = time.time()
        delta = final - initial
        mysqldump.print_message("Finished creating assets tar in %d seconds" % delta)

