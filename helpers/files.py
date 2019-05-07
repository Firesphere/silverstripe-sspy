import os

from pathlib import Path


class Files:
    def delete_sources(self, basepath):
        try:
            if os.path.isfile(os.path.join(basepath, 'assets.tar.gz')):
                Path(os.path.join(basepath, 'assets.tar.gz')).unlink()
            if os.path.isfile(os.path.join(basepath, 'database.sql.gz')):
                Path(os.path.join(basepath, 'database.sql.gz')).unlink()
            return True
        except PermissionError:
            return False
