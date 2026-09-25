import pathlib,json,zipfile
b=pathlib.Path('artifacts/database-recovery/followup');inv=json.loads((b/'inventory.json').read_text(encoding='utf-8'));out=[]
for f in inv['files']:
 if not f['path'].lower().endswith('.zip'):continue
 try:
  with zipfile.ZipFile(f['path']) as z:
   hits=[n for n in z.namelist() if pathlib.PurePosixPath(n.replace('\\','/')).name.lower() in ['app.db','task_record.sql','record.sql'] or ('sage' in n.lower() and n.lower().endswith(('.db','.sqlite','.sql')))]
   if hits:out.append({'path':f['path'],'members':hits})
 except Exception as e:out.append({'path':f['path'],'error':str(e)})
(b/'all-zip-index.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print('zip_candidates_or_errors',len(out))
