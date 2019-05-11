import getopt
import os
import shutil
import sys
import time

import dotenv

from sspy.create import Create
from sspy.files import Files
from sspy.load import Load


def main(arg, action, options):
    start = time.time()
    basepath = os.getcwd()
    file = None
    assets = False
    db = False
    for (ar, f) in options:
        if ar in ('-f', '--file'):
            file = f
        if ar in ('-d', '--db'):
            if f is not 'database.sql.gz':
                shutil.copy2(f, 'database.sql.gz')
                db = True
        if ar in ('-a', '--assets'):
            if f is not 'assets.tar.gz':
                shutil.copy2(f, 'assets.tar.gz')
                assets = True
    # Make sure the filename ends with `.sspak`
    if '.sspak' not in file:
        file += '.sspak'
    if arg == 'create':
        if action == 'db' and not db:
            Create().database()
        elif action == 'assets' and not assets:
            Create().assets()
        else:
            Create().create(db, assets)
        Create().sspak(file, basepath)
    if arg == 'load':
        Load().load(file, basepath)
    if arg == 'extract':
        Load().extract(file)

    if arg != 'extract':
        print('Cleaning up, if this takes a long time, feel free to CTRL-C this process')
        deleted = False
        while deleted is False:
            deleted = Files().delete_sources(basepath, db, assets)

    end = time.time()
    delta = end - start
    print('------------------------------------------------------------------------')
    print("Finished sspak operation in %d seconds" % delta)


def display_help():
    print("Usage:\n"
          "sspy [create|load|extract] (db|assets) --file=my.sspak --db=mydb.tar.gz --assets=myassets.tar.gz\n"
          "the db and assets commands are optional.\n"
          "This script should preferably be run from the webroot of the site\n"
          "---------------------------------------------------------------------------------------------------------"
          "-------------------------------------------\n"
          "Arguments:\n"
          "create\n"
          "       db     Only create a database snapshot\n"
          "       assets Only create an assets snapshot\n"
          "       none   Create a full snapshot\n"
          "load\n"
          "       No arguments required, it detects if there is a database or assets\n"
          "       Warning: No backup of database or assets will be created!\n"
          "extract\n"
          "       No arguments required. The SSPAK file will be extracted in to database.sql.gz and assets.tar.gz\n"
          "---------------------------------------------------------------------------------------------------------"
          "-------------------------------------------\n"
          "Parameters\n"
          "--file=|-f \n"
          "             Required, path to the sspak. E.g. --file=my.sspak or -f my.sspak\n"
          "             (note, no = sign for the shorthand!\n"
          "--db=|-d \n"
          "             Optional, path to existing database file, e.g. --db=mydatabase.sql.gz or -d mydatabase.sql.gz"
          " to create the sspak from existing sources\n"
          "             (note, no = sign for the shorthand!\n"
          "--assets=|-a \n"
          "             Optional, path to existing assets file, e.g. --assets=myassets.tar.gz or -a myassets.tar.gz"
          " to create the sspak from existing sources\n"
          "             (note, no = sign for the shorthand!\n"
          "---------------------------------------------------------------------------------------------------------"
          "-------------------------------------------\n"
          "--webroot=|-w \n"
          "              Optional, relative path from the current location to the webroot\n")
    exit(0)


if __name__ == '__main__':
    optargs = sys.argv[2:]
    action_type = None
    if len(sys.argv) < 2 or sys.argv[1] == 'help':
        if len(sys.argv) < 2:
            print("Not enough arguments given")
            display_help()
            exit(255)
        display_help()
    if sys.argv[2] in ['db', 'assets'] and sys.argv[1] == 'create':
        optargs = sys.argv[3:]
        action_type = sys.argv[2]
    opts, args = getopt.getopt(optargs, "d:a:f:w:", ['db=', 'assets=', 'file=', 'webroot='])

    for (opt, arg) in opts:
        if opt in ('-w', '--webroot='):
            os.chdir(os.path.join(os.getcwd(), arg))

    if os.path.isfile(os.path.join(os.getcwd(), '.env')):
        env_path = os.path.join(os.getcwd(), '.env')
        dotenv.load_dotenv(dotenv_path=env_path)

    main(sys.argv[1], action_type, opts)
