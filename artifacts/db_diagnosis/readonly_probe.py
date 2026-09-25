"""Read-only SQLite diagnostics. Never import application initialization code.

mode=ro&immutable=1 prevents journal/SHM writes. This inspects the main file
without replaying WAL; report WAL size and do not use this as live-WAL proof.
Only aggregate counts/schema/page metadata are reported, never row contents.
"""
import hashlib
import json
import sqlite3
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path


def metadata(path):
    if not path.exists():
        return {"exists": False}
    stat = path.stat()
    data = path.read_bytes()
    return {"exists": True, "bytes": stat.st_size,
            "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
            "sha256": hashlib.sha256(data).hexdigest()}


def inspect(path):
    path = path.resolve()
    sidecars = [path, *(Path(str(path) + suffix) for suffix in ("-wal", "-shm", "-journal"))]
    before = {str(p): metadata(p) for p in sidecars}
    result = {"path": str(path), "before": before, "sqlite_version": sqlite3.sqlite_version,
              "connection": "mode=ro&immutable=1; ignores WAL; no application imports"}
    raw = path.read_bytes()
    header = raw[:100]
    if len(header) < 100:
        result["error"] = "Short header"
        return result
    page_size = int.from_bytes(header[16:18], "big")
    page_size = 65536 if page_size == 1 else page_size
    result["header"] = {"sqlite_magic_valid": header[:16] == b"SQLite format 3\x00",
                        "page_size": page_size, "write_version": header[18], "read_version": header[19],
                        "change_counter": int.from_bytes(header[24:28], "big"),
                        "declared_pages": int.from_bytes(header[28:32], "big"),
                        "freelist_first": int.from_bytes(header[32:36], "big"),
                        "freelist_count": int.from_bytes(header[36:40], "big"),
                        "schema_cookie": int.from_bytes(header[40:44], "big"),
                        "version_valid_for": int.from_bytes(header[92:96], "big"),
                        "writer_sqlite_version": int.from_bytes(header[96:100], "big")}
    if page_size:
        result["physical_pages"] = len(raw) // page_size
        result["trailing_bytes"] = len(raw) % page_size
        result["zero_pages"] = [n + 1 for n in range(len(raw) // page_size)
                                if not any(raw[n * page_size:(n + 1) * page_size])]
    db = sqlite3.connect(path.as_uri() + "?mode=ro&immutable=1", uri=True)
    def query(sql):
        rows = []
        try:
            cursor = db.execute(sql)
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                rows.append(row)
            return {"rows": rows}
        except sqlite3.Error as exc:
            return {"partial_rows": rows, "error": str(exc), "error_code": getattr(exc, "sqlite_errorcode", None)}
    for pragma in ("integrity_check", "quick_check", "page_count", "freelist_count", "journal_mode", "schema_version", "user_version"):
        result[pragma] = query("PRAGMA " + pragma)
    result["schema"] = query("SELECT type,name,tbl_name,rootpage,sql FROM sqlite_schema ORDER BY type,name")
    result["table_scans"] = {}
    for typ, name, _, root, sql in result["schema"].get("rows", []):
        if typ != "table":
            continue
        quoted = '"' + name.replace('"', '""') + '"'
        entry = {"rootpage": root, "rows_read": 0}
        try:
            cursor = db.execute("SELECT * FROM " + quoted + " NOT INDEXED")
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                entry["rows_read"] += 1
            entry["status"] = "readable"
        except (sqlite3.Error, UnicodeError) as exc:
            entry.update(status="error", error=str(exc))
        result["table_scans"][name] = entry
    result["dbstat"] = query("SELECT name,path,pageno,pagetype,ncell,payload,unused,pgsize FROM dbstat ORDER BY name,path")
    result["foreign_key_check"] = query("PRAGMA foreign_key_check")
    db.close()
    result["after"] = {str(p): metadata(p) for p in sidecars}
    result["files_unchanged"] = before == result["after"]
    return result


if __name__ == "__main__":
    results = []
    for name in sys.argv[1:]:
        try:
            results.append(inspect(Path(name)))
        except Exception as exc:
            results.append({"path": name, "error": str(exc)})
    print(json.dumps(results, ensure_ascii=False, indent=2))
