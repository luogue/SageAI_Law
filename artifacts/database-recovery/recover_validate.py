import sqlite3,json,pathlib,hashlib,subprocess,shutil,tempfile,os,sys,concurrent.futures
base=pathlib.Path('artifacts/database-recovery').resolve(); src=pathlib.Path((base/'backup-path.txt').read_text().strip())/'app.db'; dst=base/'recovered.db'
assert not dst.exists()
c=sqlite3.connect(src.as_uri()+'?mode=ro&immutable=1',uri=True); schema=c.execute('select type,name,sql from sqlite_schema where sql is not null').fetchall(); salvage=json.loads((base/'task-salvage.json').read_text(encoding='utf-8')); rows={}
for typ,n,s in schema:
 if typ=='table':rows[n]=[r['row'] for r in salvage['good']] if n=='task_record' else c.execute('select * from "'+n+'" order by rowid').fetchall()
d=sqlite3.connect(dst)
for typ,n,s in schema:
 if typ=='table':d.execute(s)
for n,rs in rows.items():
 if rs:d.executemany('insert into "'+n+'" values('+','.join('?' for _ in rs[0])+')',rs)
for typ,n,s in schema:
 if typ!='table':d.execute(s)
d.commit(); d.execute('reindex');d.commit()
checks={k:d.execute('pragma '+k).fetchall() for k in ['integrity_check','quick_check','foreign_key_check']};comp={}
for n,rs in rows.items():
 actual=d.execute('select * from "'+n+'" order by rowid').fetchall();expected=sorted([tuple(r) for r in rs],key=lambda r:r[0]);assert actual==expected,n
 comp[n]={'recovered':len(actual),'field_differences':0}
old=sqlite3.connect((base.parent/'db_recovery/candidates_latest/logical.db').as_uri()+'?mode=ro',uri=True)
checks['prior_candidate_matches']=all(old.execute('select * from "'+n+'" order by rowid').fetchall()==d.execute('select * from "'+n+'" order by rowid').fetchall() for n in rows)
checks['dangling_report_links']=d.execute('select id,record_id from task_record where record_id is not null and record_id not in (select id from record)').fetchall();d.close()
cli=base.parent/'db_recovery/tools/sqlite3.exe';assert hashlib.sha256(cli.read_bytes()).hexdigest()=='5da2398d4913b893bd1ea578d85403b3a83a06fabf9d2303ca9f63ef0849fc6f'
sql=subprocess.run([str(cli),str(src),'.recover --ignore-freelist'],capture_output=True,check=True).stdout;(base/'recover.sql').write_bytes(sql)
recovery=base/'raw-recovered.db';p=subprocess.run([str(cli),str(recovery)],input=sql,capture_output=True);assert p.returncode==0,p.stderr
r=sqlite3.connect(recovery);checks['raw_recovery_integrity']=r.execute('pragma integrity_check').fetchall();checks['raw_recovery_tasks']=r.execute('select count(*) from task_record').fetchone()[0]
root=pathlib.Path(tempfile.mkdtemp(prefix='sageai-test-db-recovery-'));test=root/'app.db';shutil.copy2(dst,test);os.environ.update(ENV='test',SAGE_TEST_ROOT=str(root),DATABASE_URL='sqlite:///'+test.as_posix());sys.path.insert(0,str(pathlib.Path('backend').resolve()))
from tasks import create_task,update_task,get_task,get_all_tasks,delete_task,TaskStatus
assert len(get_all_tasks())==33
for t in get_all_tasks():assert get_task(t.task_id)
def worker(i):
 t=create_task('database-validation-'+str(i),12,user_id=1);update_task(t.task_id,status=TaskStatus.COMPLETED,progress=100);assert get_task(t.task_id).progress==100;delete_task(t.task_id);assert get_task(t.task_id) is None;return True
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:assert all(ex.map(worker,range(24)))
checks['business_task_crud_concurrent']='PASS: 24 tasks, 4 workers, create/update/read/delete';checks['history']='PASS: all 33 persisted tasks read';tc=sqlite3.connect(test);checks['post_crud_integrity']=tc.execute('pragma integrity_check').fetchall();assert tc.execute('select count(*) from task_record').fetchone()[0]==33
out={'source':str(src),'candidate':str(dst),'candidate_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'comparisons':comp,'checks':checks,'unrecoverable':salvage['bad'],'safe_to_switch':False,'reason':'4 incomplete task rows and preexisting missing report references'};(base/'validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out['checks'],ensure_ascii=False))
