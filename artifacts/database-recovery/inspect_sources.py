import pathlib,json,sqlite3,hashlib,zipfile,tarfile,shutil
b=pathlib.Path('artifacts/database-recovery/followup');inv=json.loads((b/'inventory.json').read_text(encoding='utf-8'));tmp=b/'isolated';tmp.mkdir(exist_ok=True);base=sqlite3.connect('file:'+str(pathlib.Path('artifacts/database-recovery/recovered.db').resolve())+'?mode=ro&immutable=1',uri=True);bc={t:[x[1] for x in base.execute('pragma table_info('+t+')')] for t in ['task_record','record']};br={t:{r[0]:r for r in base.execute('select * from '+t)} for t in bc};wanted=json.loads(pathlib.Path('artifacts/database-recovery/task-salvage.json').read_text(encoding='utf-8'));uuids={x['task_id'] for x in wanted['bad']};uuidall={r[1] for r in br['task_record'].values()}|uuids;results=[];archives=[]
def inspect(p,source):
 try:
  if p.read_bytes()[:16]!=b'SQLite format 3\x00':return
  folder=tmp/(__import__('uuid').uuid4().hex);folder.mkdir();q=folder/'app.db';shutil.copy2(p,q)
  for ext in ['-wal','-shm']:
   side=pathlib.Path(str(p)+ext)
   if side.exists():shutil.copy2(side,pathlib.Path(str(q)+ext))
  c=sqlite3.connect(q.resolve().as_uri()+'?mode=ro',uri=True);c.execute('pragma query_only=on');tables={r[0] for r in c.execute("select name from sqlite_schema where type='table'")}
  if not tables.intersection(bc):c.close();return
  x={'source':source,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'tables':{}};results.append(x)
  try:x['integrity']=c.execute('pragma integrity_check').fetchall()
  except Exception as e:x['integrity_error']=str(e)
  for t in tables.intersection(bc):
   z={};x['tables'][t]=z
   try:
    cols=[r[1] for r in c.execute('pragma table_info('+t+')')];rows=c.execute('select * from '+t).fetchall();z['count']=len(rows);z['columns']=cols;z['pk_conflicts']=[r[0] for r in rows if r[0] in br[t] and (cols!=bc[t] or tuple(r)!=tuple(br[t][r[0]]))]
    if t=='task_record':z['target_rows']=[dict(zip(cols,r)) for r in rows if dict(zip(cols,r)).get('task_id') in uuids];z['matching_known_task_uuids']=sum(dict(zip(cols,r)).get('task_id') in uuidall for r in rows)
    else:z['missing_report_candidates']=[dict(zip(cols,r)) for r in rows if r[0] in [1,3,4]]
   except Exception as e:z['error']=str(e)
  c.close()
 except Exception as e:results.append({'source':source,'error':str(e)})
for f in inv['files']:
 p=pathlib.Path(f['path']);lo=str(p).lower()
 if lo.endswith(('.db','.sqlite','.sqlite3','.bak','.backup')) or '.db.' in p.name.lower():
  if f['size']<100_000_000 and p.exists():inspect(p,str(p))
 if any(k in lo for k in ['sage','backup','备份']) and lo.endswith(('.zip','.tar.gz','.tgz')):
  a={'path':str(p),'members':[]};archives.append(a)
  try:
   if lo.endswith('.zip'):
    with zipfile.ZipFile(p) as z:
     for n in z.namelist():
      if n.lower().endswith(('.db','.sqlite','.sqlite3','.sql')):
       a['members'].append(n)
       if z.getinfo(n).file_size<100_000_000:
        q=tmp/('extract'+str(len(archives))+'-'+str(len(a['members']))+'.db');q.write_bytes(z.read(n));inspect(q,str(p)+'!'+n)
   else:
    with tarfile.open(p,'r:*') as z:
     for m in z:
      if m.isfile() and m.name.lower().endswith(('.db','.sqlite','.sqlite3','.sql')):
       a['members'].append(m.name)
       if m.size<100_000_000:
        q=tmp/('tar'+str(len(archives))+'-'+str(len(a['members']))+'.db');q.write_bytes(z.extractfile(m).read());inspect(q,str(p)+'!'+m.name)
  except Exception as e:a['error']=str(e)
(b/'candidate-checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');(b/'archive-checks.json').write_text(json.dumps(archives,ensure_ascii=False,indent=2),encoding='utf-8');print('business candidates',len(results),'archives',len(archives),'target hits',sum(len(x.get('tables',{}).get('task_record',{}).get('target_rows',[])) for x in results))

