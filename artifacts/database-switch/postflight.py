import os,sys,json,pathlib,sqlite3,concurrent.futures,datetime,hashlib,time
import requests
from dotenv import load_dotenv
root=pathlib.Path.cwd();out=root/'artifacts/database-switch';load_dotenv(root/'backend/.env',override=True);sys.path.insert(0,str(root/'backend'))
from auth.utils import create_access_token
from tasks import create_task,update_task,get_task,get_all_tasks,delete_task,TaskStatus
from storage.database import engine
from storage.crud import create_record,get_record,delete_record
new=pathlib.Path(json.loads((out/'preflight.json').read_text(encoding='utf-8'))['new_database']);assert pathlib.Path(engine.url.database).resolve()==new.resolve()
s=requests.Session();s.headers['Authorization']='Bearer '+create_access_token({'user_id':'1'},expires_delta=datetime.timedelta(minutes=20));base='http://127.0.0.1:8016';results={'actual_database':str(new),'checks':{}}
def check(name,value):results['checks'][name]=value;(out/'postflight.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
try:
 h=s.get(base+'/health',timeout=10);assert h.status_code==200,h.text;check('health',h.json())
 c=sqlite3.connect(new);assert c.execute('pragma integrity_check').fetchall()==[('ok',)];check('integrity','ok')
 history=s.get(base+'/api/tasks',timeout=10);assert history.status_code==200,history.text;assert len(history.json())==33;assert all(get_task(t.task_id) for t in get_all_tasks(1));check('history','33/33 tasks readable')
 for i in [1,3,4]:
  r=s.get(base+f'/api/records/{i}',timeout=10);assert r.status_code==404,r.text;assert '不存在' in r.text
 check('missing_reports','1/3/4 return explicit 404; no incorrect association')
 t=create_task('数据库切换验收任务',1,user_id=1);update_task(t.task_id,status=TaskStatus.COMPLETED,progress=100);r=s.get(base+'/api/task/'+t.task_id,timeout=10);assert r.status_code==200 and r.json()['progress']==100;r=s.delete(base+'/api/task/'+t.task_id,timeout=10);assert r.status_code==200;assert get_task(t.task_id) is None;check('task_crud','create/update through production repository; query/delete HTTP PASS')
 def worker(i):
  t=create_task('switch-concurrency-'+str(i),1,user_id=1);update_task(t.task_id,status=TaskStatus.COMPLETED,progress=100);assert get_task(t.task_id).progress==100;delete_task(t.task_id);return True
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:assert all(ex.map(worker,range(24)))
 check('concurrency','4 workers / 24 create-update-query-delete cycles PASS')
 p=root/'test_data/111 小时制用工协议.docx';r=s.post(base+'/review-v2/file',data={'contract_type':'labor','include_low_risk':'true','use_llm':'true'},files={'file':(p.name,p.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},timeout=600);(out/'new-review-response.json').write_text(r.text,encoding='utf-8');assert r.status_code==200,r.text[:300];d=r.json();assert d['release_quality_gate']['status']=='REPORT_READY',d['release_quality_gate'];md=d['result'];assert len(md)>100;check('new_report_generation','HTTP200 / DeepSeek / REPORT_READY')
 rid=create_record(1,'数据库切换验收—'+p.name,md,{'database_switch_acceptance':True,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest()});assert rid>4;rr=s.get(base+f'/api/records/{rid}',timeout=10);assert rr.status_code==200,rr.text;assert rr.json()['report_markdown']==md;assert get_record(rid,1)['report_markdown']==md;check('report_save_read',{'record_id':rid,'sha256':hashlib.sha256(md.encode()).hexdigest(),'repository_and_http':'PASS'})
 # Read again with a new connection and check old missing IDs remain absent.
 c.close();c=sqlite3.connect(new);assert c.execute('pragma integrity_check').fetchall()==[('ok',)];assert not c.execute('pragma foreign_key_check').fetchall();assert c.execute('select count(*) from task_record').fetchone()[0]==33;assert c.execute('select count(*) from record where id in (1,3,4)').fetchone()[0]==0
 check('final_integrity','ok');h=s.get(base+'/health',timeout=10);assert h.status_code==200,h.text;check('final_health',h.json());c.execute('pragma wal_checkpoint(TRUNCATE)');c.close();results.update(SAFE_TO_SWITCH='YES',PRODUCTION_DB_SWITCHED='YES',accepted_at=datetime.datetime.now().astimezone().isoformat(),database_sha256=hashlib.sha256(new.read_bytes()).hexdigest());(out/'postflight.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');print('ALL POST SWITCH CHECKS PASS',rid)
except Exception as e:
 results.update(SAFE_TO_SWITCH='NO',PRODUCTION_DB_SWITCHED='NO',error=str(e));(out/'postflight.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');print('ROLLBACK REQUIRED',type(e).__name__,str(e)[:400]);raise
