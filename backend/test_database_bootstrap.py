"""Pytest setup before importing any application module (no application imports)."""
import atexit
import os
import sys
import tempfile
from pathlib import Path

_temporary = None


def install():
    global _temporary
    if _temporary is not None:
        return
    if 'storage.database' in sys.modules:
        raise RuntimeError('Database imported before pytest isolation was configured')
    _temporary = tempfile.TemporaryDirectory(prefix='sageai-test-')
    root = Path(_temporary.name)
    os.environ.update(ENV='test', SAGE_TEST_ROOT=str(root), SAGE_DATA_DIR=str(root),
                      DATABASE_URL='sqlite:///' + (root / 'app.db').as_posix(),
                      LOG_DIR=str(root / 'logs'), REDIS_URL='redis://127.0.0.1:1/0')
    (root / 'logs').mkdir()
    def cleanup():
        import logging
        database = sys.modules.get('storage.database')
        if database is not None:
            database.engine.dispose()
        logging.shutdown()
        _temporary.cleanup()
    atexit.register(cleanup)
