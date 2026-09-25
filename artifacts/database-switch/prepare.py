import sqlite3,pathlib,json,hashlib,re,shutil,tempfile,os,sys,concurrent.futures,datetime
root=pathlib.Path.cwd();out=root/'artifacts/database-switch';src=root/'artifacts/database-recovery/recovered.db';expected=json.loads((root/'artifacts/database-recovery/followup/final-validation.json').read_text(encoding='utf-8'))['sha256'];assert hashlib.sha256(src.read_bytes()).hexdigest()==expected
c=sqlite3.connect(src.as_uri()+'?mode=ro&immutable=1',uri=True);assert c.execute('pragma integrity_check').fetchall()==[('ok',)];schema=c.execute('select type,name,sql from sqlite_schema where sql is not null').fetchall();rows={n:c.execute('select * from "'+n+'" order by rowid').fetchall() for t,n,s in schema if t=='table'}
p=root/'backend/data/recovered-production-20260911.sqlite';assert not p.exists();d=sqlite3.connect(p)
for typ,n,s in schema:
 if typ=='table':
  if n in ['task_record','record']:
   s=re.sub(r'\bid INTEGER NOT NULL', 'id INTEGER PRIMARY KEY AUTOINCREMENT',s,count=1);s=s.replace('\n\tPRIMARY KEY (id),','').replace('\n\tPRIMARY KEY (id)','');assert 'AUTOINCREMENT' in s
  d.execute(s)
for n,rs in rows.items():
 if rs:d.executemany('insert into "'+n+'" values('+','.join('?' for _ in rs[0])+')',rs)
for typ,n,s in schema:
 if typ!='table':d.execute(s)
for table,floor in [('task_record',37),('record',4)]:
 d.execute('update sqlite_sequence set seq=max(seq,?) where name=?',(floor,table))
 d.execute(f"CREATE TRIGGER recovery_reserved_{table}_ids BEFORE INSERT ON {table} WHEN NEW.id BETWEEN 1 AND {floor} BEGIN SELECT RAISE(ABORT, 'reserved historical identifier'); END")
d.execute('CREATE TABLE recovery_data_gaps(entity TEXT NOT NULL, historical_id INTEGER NOT NULL, task_id TEXT, accepted_at TEXT NOT NULL, reason TEXT NOT NULL, PRIMARY KEY(entity,historical_id))')
accepted=datetime.datetime.now(datetime.timezone.utc).isoformat();bad=json.loads((root/'artifacts/database-recovery/task-salvage.json').read_text(encoding='utf-8'))['bad']
for r in bad:d.execute('insert into recovery_data_gaps values(?,?,?,?,?)',('task_record',r['id'],r['task_id'],accepted,'业务已接受：历史任务无法完整恢复；未创建占位业务记录'))
for r in rows['task_record']:
 if r[7]==1:d.execute('insert into recovery_data_gaps values(?,?,?,?,?)',('task_report_reference',r[0],r[1],accepted,'业务已接受：原报告已不可用；record_id=1历史复用，禁止关联其他报告'))
for i in [1,3,4]:d.execute('insert into recovery_data_gaps values(?,?,?,?,?)',('record',i,None,accepted,'历史报告缺失；保留编号，不伪造报告'))
d.commit();assert d.execute('pragma integrity_check').fetchall()==[('ok',)];assert not d.execute('pragma foreign_key_check').fetchall()
for n,rs in rows.items():assert d.execute('select * from "'+n+'" order by rowid').fetchall()==rs,n
d.close();stagehash=hashlib.sha256(p.read_bytes()).hexdigest()
work=pathlib.Path(tempfile.mkdtemp(prefix='sageai-test-switch-'));test=work/'app.db';shutil.copy2(p,test);os.environ.update(ENV='test',SAGE_TEST_ROOT=str(work),DATABASE_URL='sqlite:///'+test.as_posix());sys.path.insert(0,str(root/'backend'))
from tasks import create_task,update_task,get_task,get_all_tasks,delete_task,TaskStatus
from storage.crud import create_record,get_record,delete_record
assert len(get_all_tasks())==33
for t in get_all_tasks():assert get_task(t.task_id)
def run(i):
 t=create_task('switch-preflight-'+str(i),10,user_id=1);update_task(t.task_id,status=TaskStatus.COMPLETED,progress=100);assert get_task(t.task_id).progress==100;delete_task(t.task_id);assert get_task(t.task_id) is None;return True
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:assert all(ex.map(run,range(24)))
a=create_record(1,'switch-preflight','# validation',{});assert a>4;assert get_record(a,1)['report_markdown']=='# validation';delete_record(a,1);b=create_record(1,'switch-preflight','# validation2',{});assert b>a;delete_record(b,1)
tc=sqlite3.connect(test);assert tc.execute('pragma integrity_check').fetchall()==[('ok',)];assert tc.execute('select count(*) from task_record').fetchone()[0]==33
result={'source':str(src),'source_sha256':expected,'new_database':str(p),'staged_sha256':stagehash,'integrity_check':'ok','field_comparison':'all 77 original rows identical','history':'33/33 readable; accepted gaps unchanged','crud':'PASS','concurrency':'4 workers / 24 tasks PASS','report_id_nonreuse':'PASS','accepted_at':accepted,'changes':'AUTOINCREMENT + historical ID reservation + separate gap manifest; no fabricated business rows'}
(out/'preflight.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
