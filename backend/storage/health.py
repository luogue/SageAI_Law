"""Startup/periodic structural validation plus cheap critical-table probes."""
import threading
import time
from sqlalchemy import text
from .database import engine

_lock = threading.Lock()
_checked_at = 0.0
_structural_ok = False
_interval = 60.0


def database_health(force=False):
    global _checked_at, _structural_ok
    try:
        with _lock, engine.connect() as connection:
            if force or time.monotonic() - _checked_at >= _interval:
                _structural_ok = False
                _checked_at = time.monotonic()
                if engine.dialect.name == 'sqlite':
                    pragma = 'integrity_check' if force else 'quick_check'
                    rows = connection.exec_driver_sql('PRAGMA ' + pragma).fetchall()
                    if rows != [('ok',)]:
                        return {'status': 'unhealthy', 'reason': 'database_integrity_failed'}
                _structural_ok = True
            if not _structural_ok:
                return {'status': 'unhealthy', 'reason': 'database_integrity_failed'}
            # Selecting non-index columns requires actual table-page reads.
            for table, field in (('user', 'password_hash'), ('record', 'report_markdown'), ('task_record', 'status')):
                for direction in ('ASC', 'DESC'):
                    connection.execute(text(f'SELECT {field} FROM "{table}" ORDER BY id {direction} LIMIT 1')).fetchall()
        return {'status': 'ok', 'structural_check_interval_seconds': int(_interval)}
    except Exception:
        return {'status': 'unhealthy', 'reason': 'database_query_failed'}
