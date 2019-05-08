import getopt
import os
import sys
import time
from pathlib import Path

import dotenv

from helpers.create import Create
from helpers.files import Files
from helpers.load import Load

env_path = Path(os.getcwd()) / '.env'
dotenv.load_dotenv(dotenv_path=env_path)


def main(arg, type, opts):
    print(arg)
    start = time.time()
    basepath = os.getcwd()
    # @todo use TarGZStream to stream directly in to the tarfile, omitting the need for removing the files
    file = 'package.sspak'
    for (ar, f) in opts:
        if ar in ('-f', '--file'):
            file = f
    # Make sure the filename ends with `.sspak`
    if '.sspak' not in file:
        file += '.sspak'
    if arg == 'create':
        if type == 'db':
            Create().database()
            Create().sspak(file, basepath)
        elif type == 'assets':
            Create().assets()
            Create().sspak(file, basepath)
        else:
            Create().create()
            Create().sspak(file, basepath)
    if arg == 'load':
        Load().load(file, basepath)
    if arg == 'extract':
        Load().extract(file)

    if arg != 'extract':
        print('Cleaning up, if this takes a long time, feel free to CTRL-C this process')
        deleted = False
        while deleted is False:
            deleted = Files().delete_sources(basepath)

    end = time.time()
    delta = end - start
    print('------------------------------------------------------------------------')
    print("Finished sspak operation in %d seconds" % delta)


if __name__ == '__main__':
    optargs = sys.argv[2:]
    type = None
    if sys.argv[2] in ['db', 'assets'] and sys.argv[1] == 'create':
        optargs = sys.argv[3:]
        type = sys.argv[2]
    opts, args = getopt.getopt(optargs, "d:a:f:", ['db=', 'assets=', 'file='])

    main(sys.argv[1], type, opts)
