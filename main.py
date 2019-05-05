import os
import sys
import tarfile
from pathlib import Path

import dotenv

from helpers import create

env_path = Path(os.getcwd()) / '.env'
dotenv.load_dotenv(dotenv_path=env_path)


def main():
    args = sys.argv
    # @todo If it's a create arg, go to create class, if it's a load, go to load class
    # Currently, we only create
    file = (args[2] or 'package.sspak')
    if args[1] == 'create':
        create.Create().create(args)
        pak = tarfile.open(os.path.join(os.getcwd(), file))
        pak.add('database.sql.gz')
        pak.add('assets.tar.gz')
    if args[1] == 'createdb':
        create.Create().database(args)
    if args[1] == 'createassets':
        create.Create().assets()


if __name__ == '__main__':
    main()
