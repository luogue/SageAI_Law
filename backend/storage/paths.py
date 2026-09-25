"""Resolve auxiliary SQLite stores without opening them."""
import os
import sys
from pathlib import Path
import sqlite3
import tempfile
from contextlib import contextmanager


@contextmanager
def sqlite_connection(path):
    """Raw auxiliary-store operations own a connection, including failure paths."""
    if os.getenv('ENV') == 'test' or 'pytest' in sys.modules:
        if not Path(path).resolve().is_relative_to(Path(tempfile.gettempdir()).resolve()):
            raise RuntimeError('Raw test SQLite connection must use a temporary file')
    connection = sqlite3.connect(path, timeout=5)
    try:
        yield connection
    except BaseException:
        connection.rollback()
        raise
    finally:
        connection.close()


def auxiliary_db_path(name, legacy_path):
    base = os.getenv('SAGE_DATA_DIR')
    path = (Path(base) / name if base else Path(legacy_path)).resolve()
    if os.getenv('ENV') == 'test' or 'pytest' in sys.modules:
        root_value = os.getenv('SAGE_TEST_ROOT')
        if not root_value or not path.is_relative_to(Path(root_value).resolve()):
            raise RuntimeError('Auxiliary test database is not isolated')
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)
