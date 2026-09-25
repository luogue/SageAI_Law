import os,pathlib,json,time
out=pathlib.Path('artifacts/database-recovery/followup');out.mkdir(exist_ok=True)
roots=['F:/','D:/','E:/','G:/','H:/','M:/','N:/','C:/Users/Administrator','C:/ProgramData']
skip={'node_modules','.git','.pnpm-store','site-packages','__pycache__','windowsapps','wpsystem','$recycle.bin','system volume information','steamapps','cache','code cache','gpucache'};found=[];errors=[];dirs=0
for root in roots:
 for r,ds,fs in os.walk(root,onerror=lambda e:errors.append(str(e))):
  dirs+=1;ds[:]=[d for d in ds if d.lower() not in skip]
  for f in fs:
   lo=f.lower();p=pathlib.Path(r)/f
   if lo.endswith(('.db','.sqlite','.sqlite3','.sql','.dump','.bak','.backup','.zip','.7z','.rar','.tar','.gz')) or '.db.' in lo:
    try:found.append({'path':str(p),'size':p.stat().st_size,'mtime':p.stat().st_mtime})
    except OSError:pass
(out/'inventory.json').write_text(json.dumps({'roots':roots,'skipped_names':sorted(skip),'directories':dirs,'files':found,'errors':errors},ensure_ascii=False,indent=2),encoding='utf-8');print('directories',dirs,'candidates',len(found),'errors',len(errors))
