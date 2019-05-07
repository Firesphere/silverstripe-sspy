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
    basepath = os.getcwd()
    args = sys.argv
    # @todo If it's a create arg, go to create class, if it's a load, go to load class
    # @todo use TarGZStream to stream directly in to the tarfile, omitting the need for
    # removing the files, as that is proving troublesome
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

    sspak(file, basepath)

    print('Cleaning up, if this takes a long time, feel free to CTRL-C this process')
    deleted = False
    while deleted is False:
        deleted = delete_sources(basepath)

    end = time.time()
    delta = end - start
    print('------------------------------------------------------------------------')
    print("Finished creating sspak in %d seconds" % delta)


def sspak(file, basepath):
    print("------------------------------------------------------------------------")
    with tarfile.open(file, "w") as tar:
        if os.path.isfile(os.path.join(basepath, 'database.sql.gz')):
            tar.add('database.sql.gz')
        if os.path.isfile(os.path.join(basepath, 'assets.tar.gz')):
            tar.add('assets.tar.gz')


def delete_sources(basepath):
    try:
        Path(os.path.join(basepath, 'assets.tar.gz')).unlink()
        Path(os.path.join(basepath, 'database.sql.gz')).unlink()
        return True
    except PermissionError:
        return False


if __name__ == '__main__':
    main()
