"""Inspect copies of this application's IndexedDB stores, including old records."""
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'artifacts/db_recovery'/n) for n in ['forensic_reader','forensic_snappy','forensic_deps']]
from ccl_chromium_reader.storage_formats import ccl_leveldb
out=ROOT/'artifacts/db_recovery/browser_evidence';out.mkdir(exist_ok=True)
ids=['c6daf70a-ed9c-443a-9ad6-0b742f51ce76','7ea566e9-1f67-4d2e-bceb-a88c405081be','89ff9724-8eb3-43c5-8169-6071a0ba2bdc','e451edda-230a-49f9-8c23-7668892fb607']
needles=ids+['退休人员返聘协议','阴阳合同']
r=[]
for src in map(Path,json.loads((Path(__file__).parent/'browser-store-inventory.json').read_text())):
    dest=out/src.name;dest.mkdir(exist_ok=True);item={'source':str(src),'files':[],'errors':[],'records':0,'matches':[]}
    for f in src.rglob('*'):
        if not f.is_file() or f.name=='LOCK':continue
        try:
            data=f.read_bytes();t=dest/f.relative_to(src);t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(data)
            item['files'].append({'name':str(f.relative_to(src)),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
        except Exception as e:item['errors'].append({'file':f.name,'type':type(e).__name__})
    if src.name.endswith('.leveldb'):
        try:
            with ccl_leveldb.RawLevelDb(dest) as db:
                for rec in db.iterate_records_raw():
                    item['records']+=1
                    matches=[n for n in needles if n.encode('utf8') in rec.value or n.encode('utf-16-le') in rec.value]
                    if matches:
                        recordfile=out/f'{src.name}-match-{item["records"]}.bin';recordfile.write_bytes(rec.value)
                        item['matches'].append({'needles':matches,'file':str(recordfile),'bytes':len(rec.value)})
        except Exception as e:item['errors'].append({'type':type(e).__name__,'error':str(e)})
    r.append(item)
(out/'inspection.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps([{k:v for k,v in x.items() if k!='files'} for x in r],ensure_ascii=True))
