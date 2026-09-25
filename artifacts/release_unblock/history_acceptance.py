"""Read historical endpoints in an isolated candidate copy, never the live DB."""
import hashlib, json, os, secrets, socket, sqlite3, subprocess, sys, tempfile, time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'artifacts/release_unblock'
candidate = ROOT/'artifacts/db_recovery/candidates_latest/logical.db'
work = Path(tempfile.mkdtemp(prefix='sageai-test-history-'))
database = work/'app.db'
database.write_bytes(candidate.read_bytes())
with sqlite3.connect(database) as db:
    tasks = db.execute('SELECT id,task_id,result FROM task_record WHERE record_id=1 ORDER BY id').fetchall()
with socket.socket() as sock:
    sock.bind(('127.0.0.1',0));port = sock.getsockname()[1]
env = dict(os.environ, ENV='test', SAGE_TEST_ROOT=str(work), SAGE_DATA_DIR=str(work),
           DATABASE_URL='sqlite:///'+database.as_posix(), LOG_DIR=str(work/'logs'),
           REDIS_URL='redis://127.0.0.1:1/0', PROBE_SECRET=secrets.token_hex(24),
           PROBE_PORT=str(port), ENABLE_RATE_LIMIT='false', PYTHONIOENCODING='utf-8')
s = requests.Session();s.trust_env=False;s.headers['X-Probe-Secret']=env['PROBE_SECRET']
base=f'http://127.0.0.1:{port}'
result={'database':str(database),'candidate_sha256':hashlib.sha256(candidate.read_bytes()).hexdigest(),'tasks':[]}
proc=None
log=(OUT/'history-instance.log').open('wb')
try:
    proc=subprocess.Popen([sys.executable,str(ROOT/'artifacts/db_diagnosis/isolated_server.py')],cwd=work,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
    for attempt in range(160):
        if proc.poll() is not None:raise RuntimeError('isolated instance exited')
        try:
            if s.get(base+'/health',timeout=2).status_code==200:break
        except requests.RequestException:pass
        time.sleep(.25)
    else:raise RuntimeError('startup timeout')
    seed=s.post(base+'/__probe/seed',timeout=20).json()
    s.headers['Authorization']='Bearer '+seed['existing_account_token']
    history=s.get(base+'/api/tasks',timeout=30);result['history_list_status']=history.status_code
    history_ids={x['task_id'] for x in history.json()}
    for ident,uid,expected in tasks:
        detail=s.get(base+'/api/task/'+uid,timeout=30)
        row={'id':ident,'task_id':uid,'in_history':uid in history_ids,'detail_status':detail.status_code,
             'result_matches':detail.status_code==200 and detail.json()['result']==expected,'exports':{}}
        for fmt in ['md','docx','pdf']:
            r=s.get(base+f'/api/task/{uid}/download?format={fmt}',timeout=60)
            row['exports'][fmt]={'status':r.status_code,'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest(),'error':r.text if r.status_code!=200 else None}
        result['tasks'].append(row)
    result['missing_report_endpoints']={p:s.get(base+p,timeout=30).status_code for p in ['/api/records/1','/api/download/1']}
    new_report=s.post(base+'/__probe/report',json={'user_id':1,'markdown':'# Report export verification'},timeout=20).json()['record_id']
    result['new_report_exports']={fmt:s.get(base+f'/api/download/{new_report}?format={fmt}',timeout=30).status_code for fmt in ['md','docx','pdf']}
    result['status']='PASS' if all(t['in_history'] and t['result_matches'] and all(e['status']==200 for e in t['exports'].values()) for t in result['tasks']) else 'FAILED'
except Exception as e:result.update(status='ERROR',error=str(e))
finally:
    if proc and proc.poll() is None:
        try:s.post(base+'/__probe/shutdown',timeout=5);proc.wait(timeout=20)
        except Exception:proc.terminate();proc.wait(timeout=10)
    log.close()
    result['candidate_unchanged']=hashlib.sha256(candidate.read_bytes()).hexdigest()==result['candidate_sha256']
    (OUT/'history-acceptance.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=True))
