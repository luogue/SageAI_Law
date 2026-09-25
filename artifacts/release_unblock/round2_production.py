"""Current production verification: read-only file capture, no production SQL writes."""
import json,hashlib,sqlite3,datetime
from pathlib import Path
from production_probe import connect,remote_python,ROOT,OUT
result={'PRODUCTION_DB_STATUS':'UNKNOWN','started':datetime.datetime.now(datetime.timezone.utc).isoformat()}
c=connect();s=c.open_sftp()
try:
    code="""import subprocess,json,ast,hashlib
def run(cmd):
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=20);return {'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
r={'containers':{},'disk':run(['df','-h','/']),'git':run(['git','-C','/opt/sageai','rev-parse','HEAD'])}
for name in ['sageai-backend','sageai-frontend','sageai-redis']:
 p=run(['docker','inspect',name]);v=json.loads(p['stdout'])[0];env=dict(x.split('=',1) for x in v['Config']['Env'] if '=' in x)
 r['containers'][name]={'id':v['Id'],'image_id':v['Image'],'started':v['State']['StartedAt'],'status':v['State']['Status'],'health':v['State'].get('Health'),'mounts':v['Mounts'],'database_url':env.get('DATABASE_URL'),'labels':{k:x for k,x in v['Config'].get('Labels',{}).items() if k.startswith('com.docker.compose.')}}
r['backend_http']=run(['docker','exec','sageai-backend','python','-c',"import urllib.request; r=urllib.request.urlopen('http://127.0.0.1:8000/health'); print(r.status); print(r.read().decode())"])
r['frontend_http']=run(['docker','exec','sageai-frontend','wget','-S','--spider','http://127.0.0.1/'])
r['version']=run(['docker','exec','sageai-backend','python','-c',"import ast,json,hashlib; from pathlib import Path; p=Path('/app/main.py'); t=ast.parse(p.read_text()); print(json.dumps({'version':next(k.value.value for n in ast.walk(t) if isinstance(n,ast.Call) and getattr(n.func,'id','')=='FastAPI' for k in n.keywords if k.arg=='version'),'main_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))"])
print(json.dumps(r))
"""
    probe=remote_python(c,code);assert probe['exit']==0
    result['host']=json.loads(probe['stdout'])
    backend=result['host']['containers']['sageai-backend'];url=backend['database_url']
    assert url.startswith('sqlite:////'), 'Do not guess non-SQLite locations'
    container_path=url[len('sqlite:///'):]
    mount=max((m for m in backend['mounts'] if container_path.startswith(m['Destination']+'/')),key=lambda m:len(m['Destination']))
    source=mount['Source']+container_path[len(mount['Destination']):]
    result.update(database_type='SQLite',database_url=url,host_path=source,volume=mount.get('Name'))
    def capture():
        files={}
        for suffix in ['', '-wal', '-shm']:
            try:
                stat=s.stat(source+suffix)
                with s.open(source+suffix,'rb') as f:data=f.read()
                files['app.db'+suffix]=(data,{'size':len(data),'mtime':stat.st_mtime,'sha256':hashlib.sha256(data).hexdigest()})
            except FileNotFoundError:pass
        return files
    first,last=capture(),capture()
    assert first.keys()==last.keys() and all(first[k][1]==last[k][1] for k in first),'Unstable acquisition'
    result['files']={k:v[1] for k,v in last.items()};result['stable_acquisition']=True
    root=ROOT/'artifacts/db_recovery/production_readonly_round2';root.mkdir(exist_ok=False)
    evidence=root/'evidence';evidence.mkdir();work=root/'inspect';work.mkdir()
    for name,(data,meta) in last.items():
        (evidence/name).write_bytes(data)
        if name!='app.db-shm':(work/name).write_bytes(data)
    db=sqlite3.connect((work/'app.db').as_uri()+'?mode=ro',uri=True)
    result['checks']={name:db.execute('PRAGMA '+name).fetchall() for name in ['integrity_check','quick_check','foreign_key_check']}
    result['tables']={}
    for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        count=sum(1 for row in db.execute('SELECT * FROM "'+name.replace('"','""')+'"'))
        result['tables'][name]={'count':count,'fully_readable':True}
    result['missing_report_references']=db.execute('SELECT count(*) FROM task_record t LEFT JOIN record r ON t.record_id=r.id WHERE t.record_id IS NOT NULL AND r.id IS NULL').fetchone()[0]
    db.close()
    result['PRODUCTION_DB_STATUS']='HEALTHY' if all(result['checks'][p]==[('ok',)] for p in ['integrity_check','quick_check']) else 'BROKEN'
except Exception as e:result['error']=str(e)
finally:
    s.close();c.close();result['finished']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (OUT/'round2-production.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if k!='host'},ensure_ascii=True))
