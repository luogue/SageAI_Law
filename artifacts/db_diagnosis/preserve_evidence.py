"""Byte-only evidence acquisition; no SQLite connection to the live source."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'backend' / 'app.db'
DEST = ROOT / 'artifacts' / 'db_recovery' / 'evidence'

def read(path):
    stat = path.stat()
    data = path.read_bytes()
    return data, {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                  'mtime_ns': stat.st_mtime_ns,
                  'modified_utc': datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()}

def main():
    DEST.mkdir(parents=True, exist_ok=False)
    paths = [Path(str(SOURCE) + suffix) for suffix in ('', '-wal', '-shm')]
    captured = {p.name: read(p) for p in paths}
    after = {p.name: read(p)[1] for p in paths}
    if any(meta != after[name] for name, (_, meta) in captured.items()):
        raise RuntimeError('Source changed during acquisition; no valid snapshot claimed')
    manifest = {'acquired_utc': datetime.now(timezone.utc).isoformat(), 'source': str(SOURCE),
                'method': 'read bytes only; stable two-pass acquisition; no source SQLite open',
                'files': {}, 'wal_empty': captured['app.db-wal'][1]['bytes'] == 0}
    for name, (data, meta) in captured.items():
        with (DEST / name).open('xb') as output:
            output.write(data)
        manifest['files'][name] = meta
    (DEST / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    if not manifest['wal_empty']:
        raise RuntimeError('Nonempty WAL: preserve evidence only; require consistent acquisition before recovery')

if __name__ == '__main__':
    main()
