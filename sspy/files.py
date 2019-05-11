import os

from pathlib import Path


class Files:
    def delete_sources(self, basepath, db, assets):
        try:
            if not assets and os.path.isfile(os.path.join(basepath, 'assets.tar.gz')):
                Path(os.path.join(basepath, 'assets.tar.gz')).unlink()
            if not db and os.path.isfile(os.path.join(basepath, 'database.sql.gz')):
                Path(os.path.join(basepath, 'database.sql.gz')).unlink()
            return True
        except PermissionError:
            return False
