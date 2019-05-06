import os
import sys
import tarfile
import time
from pathlib import Path

import dotenv

from helpers import create

env_path = Path(os.getcwd()) / '.env'
dotenv.load_dotenv(dotenv_path=env_path)


def main():
    start = time.time()
    args = sys.argv
    # @todo If it's a create arg, go to create class, if it's a load, go to load class
    try:
        file = args[2]
    except IndexError:
        file = 'package.sspak'
    if args[1] == 'create':
        create.Create().create()
    if args[1] == 'createdb':
        create.Create().database()
    if args[1] == 'createassets':
        create.Create().assets()

    sspak(file)

    end = time.time()
    delta = end - start
    print("Finished creating sspak in %d seconds" % delta)


def sspak(file):
    basepath = os.getcwd()
    tar = tarfile.open(file, "w")
    if os.path.isfile(os.path.join(basepath, 'database.sql.gz')):
        tar.add('database.sql.gz')
    if os.path.isfile(os.path.join(basepath, 'assets.tar.gz')):
        tar.add('assets.tar.gz')
    tar.close()
    try:
        os.remove(os.path.join(basepath, 'assets.tar.gz'))
        os.remove(os.path.join(basepath, 'database.sql.gz'))
    except:
        print('Could not remove all source file(s)')


if __name__ == '__main__':
    main()
