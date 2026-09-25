import json,hashlib,xml.etree.ElementTree as E
from pathlib import Path
root=Path.cwd();p=root/'artifacts/technology_pass_semantics/round33_patent_transfer_projection'
hashes={str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in (root/'backend/review_v2').glob('*.py')}
for n in ['targeted','existing','technical0','technical1','technical2','technical3','patent','patent0','patent1','patent2']:
 f=p/f'{n}_source_integrity.json'
 if not f.exists():print(n,'INCOMPLETE');continue
 i=json.loads(f.read_text());xs=list(E.parse(p/f'{n}.xml').iter('testcase'))
 print(n,'FINAL' if i['unchanged'] and i['after']==hashes else 'OLD_SOURCE',len(xs),'fails',sum(x.find('failure') is not None or x.find('error') is not None for x in xs))
for f in sorted(p.glob('*/report.json')):
 if f.parent.name.startswith(('final_','protection_')):
  r=json.loads(f.read_text(encoding='utf8'));print(f.parent.name,r['release_quality_gate']['status'],r.get('production_path_trace',{}).get('process_id'))
