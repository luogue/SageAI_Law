"""Preserve changed live sidecars; replay ONLY copies, compare against first evidence."""
import hashlib
import json
import sqlite3
import struct
from datetime import datetime, timezone
from pathlib import Path
import psutil

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'artifacts/db_recovery'
DEST = OUT/'evidence_followup'
WORK = OUT/'wal_replay'

def capture():
    result = {}
    for name in ('app.db','app.db-wal','app.db-shm'):
        path = ROOT/'backend'/name
        meta = path.stat()
        data = path.read_bytes()
        result[name] = (data, {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
                             'mtime_ns':meta.st_mtime_ns})
    return result

before, after = capture(), capture()
assert all(before[key][1] == after[key][1] for key in before), 'Live files changed during capture'
DEST.mkdir(exist_ok=False)
WORK.mkdir(exist_ok=False)
for name,(data,meta) in before.items():
    (DEST/name).write_bytes(data)
    if name != 'app.db-shm':
        (WORK/name).write_bytes(data)
manifest = {'captured_utc':datetime.now(timezone.utc).isoformat(), 'files':{k:v[1] for k,v in before.items()}}
(DEST/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
wal = before['app.db-wal'][0]
page_size = int.from_bytes(wal[8:12],'big')
frames=[]
for offset in range(32,len(wal),24+page_size):
    page, size = struct.unpack('>II',wal[offset:offset+8])
    frames.append({'page':page,'commit_db_pages':size})
report={'frames':frames,'page_size':page_size,'processes':[]}
for p in psutil.process_iter(['pid','name']):
    try:
        if 'python' in (p.info['name'] or '').lower() and any(f.path.lower()==str(ROOT/'backend/app.db').lower() for f in p.open_files()):
            report['processes'].append({'pid':p.pid,'cmd':p.cmdline(),'cwd':p.cwd(),
                'started_utc':datetime.fromtimestamp(p.create_time(),timezone.utc).isoformat()})
    except (psutil.NoSuchProcess,psutil.AccessDenied):
        pass
# Connections below refer exclusively to copied evidence. SQLite applies committed WAL there.
db=sqlite3.connect((WORK/'app.db').as_uri()+'?mode=ro',uri=True)
materialized=OUT/'latest_materialized'
materialized.mkdir(exist_ok=False)
target=sqlite3.connect(materialized/'app.db')
db.backup(target)
target.close()
old=sqlite3.connect((OUT/'evidence/app.db').as_uri()+'?mode=ro&immutable=1',uri=True)
old_schema=old.execute('SELECT type,name,tbl_name,sql FROM sqlite_schema ORDER BY type,name').fetchall()
new_schema=db.execute('SELECT type,name,tbl_name,sql FROM sqlite_schema ORDER BY type,name').fetchall()
report['added_schema']=[r for r in new_schema if r not in old_schema]
report['removed_schema']=[r for r in old_schema if r not in new_schema]
report['tables']={}
for (name,) in old.execute("SELECT name FROM sqlite_schema WHERE type='table' AND name!='task_record'"):
    sql='SELECT * FROM "'+name.replace('"','""')+'" ORDER BY rowid'
    a,b=old.execute(sql).fetchall(),db.execute(sql).fetchall()
    report['tables'][name]={'initial_count':len(a),'latest_count':len(b),'exact_equal':a==b}
report['tasks']={}
ids=[r[0] for r in db.execute('SELECT id FROM task_record INDEXED BY ix_task_record_id')]
for ident in ids:
    try:
        a=old.execute('SELECT * FROM task_record WHERE rowid=?',(ident,)).fetchone()
        b=db.execute('SELECT * FROM task_record WHERE rowid=?',(ident,)).fetchone()
        report['tasks'][str(ident)]={'exact_equal':a==b,'readable':True}
    except sqlite3.DatabaseError:
        report['tasks'][str(ident)]={'readable':False}
for name in ('integrity_check','quick_check'):
    try: report[name]=db.execute('PRAGMA '+name).fetchall()
    except sqlite3.DatabaseError as error: report[name]={'error':str(error)}
old.close();db.close()
(OUT/'live-wal-delta.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'processes':report['processes'],'wal_frames':len(frames),'commit_sizes':[f['commit_db_pages'] for f in frames if f['commit_db_pages']],
                  'added_schema_names':[r[1] for r in report['added_schema']], 'all_other_tables_equal':all(v['exact_equal'] for v in report['tables'].values()),
                  'readable_tasks':sum(v['readable'] for v in report['tasks'].values()),'all_readable_tasks_equal':all(v.get('exact_equal',True) for v in report['tasks'].values())},ensure_ascii=False,indent=2))
