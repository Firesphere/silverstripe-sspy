import dotenv
import os
import sys
from pathlib import Path

from helpers import create

env_path = Path(os.getcwd()) / '.env'
dotenv.load_dotenv(dotenv_path=env_path)


def main():
    args = sys.argv
    if args[1] == 'create':
        create.Create().create(args)
    if args[1] == 'createdb':
        create.Create().database(args)


if __name__ == '__main__':
    main()
