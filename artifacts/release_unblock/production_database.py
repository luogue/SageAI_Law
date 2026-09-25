"""Acquire a stable read-only production snapshot; inspect only local copies."""
import hashlib
import json
import sqlite3
from pathlib import Path
from production_probe import connect, remote_python, ROOT, OUT

LOCAL = ROOT/'artifacts/db_recovery/production_readonly'
SOURCE = '/var/lib/docker/volumes/sageai-db-data/_data/app.db'

def main():
    result = {'PRODUCTION_DB_STATUS':'UNKNOWN','actual_host_path':SOURCE,'actual_container_path':'/app/data/app.db',
              'acquisition':'SFTP read only; two full byte/metadata passes; SQLite checks on local copies including WAL'}
    client=connect()
    sftp=client.open_sftp()
    def capture():
        captured={}
        for suffix in ('','-wal','-shm'):
            path=SOURCE+suffix
            try:
                stat=sftp.stat(path)
                with sftp.open(path,'rb') as stream:data=stream.read()
                captured['app.db'+suffix]=(data,{'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'mtime':stat.st_mtime})
            except FileNotFoundError:pass
        return captured
    try:
        before,after=capture(),capture()
        stable=before.keys()==after.keys() and all(before[k][1]==after[k][1] for k in before)
        result['stable_acquisition']=stable
        result['files']={k:v[1] for k,v in before.items()}
        if not stable:raise RuntimeError('Production bytes changed during acquisition; no integrity conclusion')
        LOCAL.mkdir(parents=True,exist_ok=False)
        evidence=LOCAL/'evidence';evidence.mkdir()
        work=LOCAL/'inspect';work.mkdir()
        for name,(data,meta) in before.items():
            (evidence/name).write_bytes(data)
            if name!='app.db-shm':(work/name).write_bytes(data)
        db=sqlite3.connect((work/'app.db').as_uri()+'?mode=ro',uri=True)
        result['sqlite_header_valid']=before['app.db'][0][:16]==b'SQLite format 3\0'
        result['checks']={}
        for name in ('integrity_check','quick_check','foreign_key_check'):
            try:result['checks'][name]=db.execute('PRAGMA '+name).fetchall()
            except sqlite3.Error as error:result['checks'][name]={'error':str(error)}
        result['tables']={}
        for (table,) in db.execute("SELECT name FROM sqlite_schema WHERE type='table'"):
            try:
                cursor=db.execute('SELECT * FROM "'+table.replace('"','""')+'"')
                count=sum(1 for _ in cursor)
                result['tables'][table]={'fully_readable':True,'count':count}
            except sqlite3.Error as error:result['tables'][table]={'fully_readable':False,'error':str(error)}
        try:
            result['task_report_orphan_count']=db.execute('SELECT count(*) FROM task_record t LEFT JOIN record r ON t.record_id=r.id WHERE t.record_id IS NOT NULL AND r.id IS NULL').fetchone()[0]
        except sqlite3.Error as error:result['task_report_reference_error']=str(error)
        salvage=json.loads((ROOT/'artifacts/db_recovery/candidates_latest/task-salvage.json').read_text(encoding='utf-8'))
        result['damaged_local_tasks_in_production']={}
        for ident, fields in salvage['partial'].items():
            try:
                cursor=db.execute('SELECT * FROM task_record WHERE task_id=?',(fields['task_id'],));row=cursor.fetchone()
                result['damaged_local_tasks_in_production'][ident]={'exists':row is not None,'columns':[v[0] for v in cursor.description] if row else []}
                if row:
                    (LOCAL/f'recovered-task-{ident}.json').write_text(json.dumps(dict(zip([v[0] for v in cursor.description],row)),ensure_ascii=False,indent=2),encoding='utf-8')
            except sqlite3.Error as error:result['damaged_local_tasks_in_production'][ident]={'error':str(error)}
        db.close()
        result['PRODUCTION_DB_STATUS']='VERIFIED_HEALTHY' if result['checks']['integrity_check']==[('ok',)] and result['checks']['quick_check']==[('ok',)] and all(v['fully_readable'] for v in result['tables'].values()) else 'VERIFIED_UNHEALTHY'
        version_code='''import json,subprocess
code="""import hashlib,json,re,os
from pathlib import Path
p=Path('/app/main.py');s=p.read_text(encoding='utf-8')
r={'main_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'app_version':re.search(r'FastAPI\\([^\\n]*version=[\\\"\\\']([^\\\"\\\']+)',s).group(1),'packaged_databases':[]}
for p in Path('/app').rglob('*.db'):
 if str(p).startswith('/app/data/'):continue
 r['packaged_databases'].append({'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
print(json.dumps(r))
"""
p=subprocess.run(['docker','exec','sageai-backend','python','-c',code],capture_output=True,text=True)
print(json.dumps({'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}))
'''
        result['version_and_packaged_db_probe']=remote_python(client,version_code)
    except Exception as error:
        result['error']=str(error)
    finally:
        sftp.close();client.close()
        (OUT/'production-database.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
