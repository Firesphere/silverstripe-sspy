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


if __name__ == '__main__':
    print(sys.argv)
    main()
