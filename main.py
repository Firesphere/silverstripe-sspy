import os
import sys
import tarfile
import time
from pathlib import Path

import dotenv

from helpers.create import Create
from helpers.load import Load
from helpers.files import Files

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
        Create().create()
        Create().sspak(file, basepath)
    if args[1] == 'createdb':
        Create().database()
        Create().sspak(file, basepath)
    if args[1] == 'createassets':
        Create().assets()
        Create().sspak(file, basepath)
    if args[1] == 'load':
        Load().load(file, basepath)
    if args[1] == 'extract':
        Load().extract(file)

    print('Cleaning up, if this takes a long time, feel free to CTRL-C this process')
    deleted = False
    while deleted is False:
        deleted = Files().delete_sources(basepath)

    end = time.time()
    delta = end - start
    print('------------------------------------------------------------------------')
    print("Finished sspak operation in %d seconds" % delta)


if __name__ == '__main__':
    main()
