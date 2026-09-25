"""Safe SQLite snapshot/staging CLI. Never replaces an existing database.

Live backups use SQLite's backup API (including committed WAL content).
Restore staging validates first and creates a NEW file; switching is manual.
"""
import argparse
import gzip
import hashlib
import json
import os
import sqlite3
import tempfile
import time
from contextlib import closing
from pathlib import Path


def validate(connection):
    result = {name: connection.execute('PRAGMA ' + name).fetchall()
              for name in ('integrity_check', 'quick_check', 'foreign_key_check')}
    if result['integrity_check'] != [('ok',)] or result['quick_check'] != [('ok',)] or result['foreign_key_check']:
        raise RuntimeError('Database validation failed: ' + repr(result))
    result['tables'] = {}
    for (name,) in connection.execute("SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
        quoted = '"' + name.replace('"', '""') + '"'
        result['tables'][name] = connection.execute('SELECT count(*) FROM ' + quoted).fetchone()[0]
    return result


def snapshot(source, destination, timeout=60):
    source, destination = Path(source).resolve(strict=True), Path(destination).absolute()
    if destination.exists() or source == destination.resolve():
        raise ValueError('Destination must be a new file; replacement is forbidden')
    if any(Path(str(destination) + s).exists() for s in ('-wal', '-shm', '-journal')):
        raise ValueError('Destination has stale SQLite sidecars')
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=destination.name + '.', suffix='.partial', dir=destination.parent)
    os.close(fd)
    temporary = Path(temporary)
    started = time.monotonic()
    def progress(status, remaining, total):
        if time.monotonic() - started > timeout:
            raise TimeoutError('Snapshot timeout; no backup published')
    try:
        with closing(sqlite3.connect(source.as_uri() + '?mode=ro', uri=True, timeout=5)) as src:
            with closing(sqlite3.connect(temporary)) as dst:
                src.backup(dst, pages=256, progress=progress, sleep=0.05)
                # Self-contained backup: no WAL needed when the file is transferred.
                dst.execute('PRAGMA journal_mode=DELETE')
                result = validate(dst)
        with temporary.open('r+b') as stream:
            os.fsync(stream.fileno())
        # link is atomic and refuses a concurrently-created destination (unlike replace).
        os.link(temporary, destination)
        result.update(path=str(destination), source=str(source), bytes=destination.stat().st_size,
                      sha256=hashlib.sha256(destination.read_bytes()).hexdigest())
        return result
    finally:
        temporary.unlink(missing_ok=True)


def stage(source, destination):
    """Accept a plain or gzip backup; stage only, never stop services or switch paths."""
    source = Path(source).resolve(strict=True)
    if source.suffix != '.gz':
        return snapshot(source, destination)
    with tempfile.TemporaryDirectory(prefix='sageai-restore-') as directory:
        expanded = Path(directory) / 'backup.db'
        with gzip.open(source, 'rb') as compressed, expanded.open('xb') as output:
            import shutil
            shutil.copyfileobj(compressed, output)
        return snapshot(expanded, destination)


def configured_path():
    url = os.getenv('DATABASE_URL', '')
    prefix = 'sqlite:///'
    if not url.startswith(prefix) or not Path(url[len(prefix):]).is_absolute() or '?' in url:
        raise ValueError('Configured backup requires an absolute SQLite DATABASE_URL')
    return url[len(prefix):]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('backup', 'stage', 'validate'))
    parser.add_argument('--source')
    parser.add_argument('--configured', action='store_true')
    parser.add_argument('--output')
    args = parser.parse_args()
    if bool(args.source) == bool(args.configured):
        parser.error('Select exactly one of --source or --configured')
    source = configured_path() if args.configured else args.source
    if args.operation == 'validate':
        path = Path(source).resolve(strict=True)
        with closing(sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)) as connection:
            result = validate(connection)
    else:
        if not args.output:
            parser.error('--output is required')
        result = (snapshot if args.operation == 'backup' else stage)(source, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
