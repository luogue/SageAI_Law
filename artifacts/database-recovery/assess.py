import sqlite3,json,pathlib,re
p=pathlib.Path('backend/app.db').resolve()
c=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True);c.execute('PRAGMA query_only=ON')
report={'database':str(p),'sqlite_version':sqlite3.sqlite_version,'integrity':[],'tables':[]}
try:report['integrity']=[r[0] for r in c.execute('PRAGMA integrity_check')]
except Exception as e:report['integrity']=[str(e)]
for kind,name,sql in c.execute("SELECT type,name,sql FROM sqlite_master WHERE type IN ('table','index') ORDER BY type,name"):
 if kind=='table':
  q='"'+name.replace('"','""')+'"';entry={'name':name}
  try:entry['count']=c.execute('SELECT count(*) FROM '+q+' NOT INDEXED').fetchone()[0];entry['read_count']=sum(1 for _ in c.execute('SELECT * FROM '+q+' NOT INDEXED'))
  except Exception as e:entry['error']=str(e)
  report['tables'].append(entry)
report['schema']=[dict(zip(['type','name','tbl_name','rootpage','sql'],r)) for r in c.execute('SELECT type,name,tbl_name,rootpage,sql FROM sqlite_master')]
pathlib.Path('artifacts/database-recovery/readonly-assessment.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in report.items() if k!='schema'},ensure_ascii=False))
logs=[]
for base in (pathlib.Path('.runtime-logs'),pathlib.Path('backend/logs')):
 for f in base.glob('*.log'):
  for line in f.read_text(encoding='utf8',errors='replace').splitlines():
   if any(x in line.lower() for x in ('database disk image is malformed','database_integrity_failed','rowid','btree','b-tree')) and re.match(r'\d{4}-\d\d-\d\d',line):logs.append((line[:23],str(f),line[:700]))
print('EARLIEST',sorted(logs)[:4])
pathlib.Path('artifacts/database-recovery/earliest-errors.json').write_text(json.dumps(sorted(logs)[:20],ensure_ascii=False,indent=2),encoding='utf8')
