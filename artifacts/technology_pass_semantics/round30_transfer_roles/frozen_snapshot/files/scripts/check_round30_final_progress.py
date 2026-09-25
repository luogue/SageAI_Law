"""Progress only for duration-balanced final shards; acceptance uses complete JUnit."""
from pathlib import Path
import json,re,xml.etree.ElementTree as E
p=Path(__file__).resolve().parents[1]/'artifacts/technology_pass_semantics';o=p/'round30_transfer_roles'
by={}
for b in [0,1]:
 for c in E.parse(p/f'round29_secret_license_aggregation/full80_batch{b}.xml').iter('testcase'):
  m=c.get('classname').replace('.','/')+'.py';by.setdefault(m,[]).append((c.get('classname')+'::'+c.get('name'),'F' if c.find('failure') is not None or c.find('error') is not None else '.'))
by['backend/tests/test_secret_transfer_roles_projection.py']=[('added regression '+str(n),'.') for n in range(77)]
manifest=json.loads((o/'full83_manifest.json').read_text(encoding='utf8'))
for b,modules in enumerate(manifest['modules']):
 t=(o/f'full83_batch{b}.out').read_text(encoding='utf-8-sig');marks=''.join(re.findall(r'^([.FEsxX]+)\s+\[\s*\d+%\]',t,re.M));rows=[r for m in modules for r in by[m]]
 changes=[(rows[i][0],rows[i][1],v) for i,v in enumerate(marks) if i<len(rows) and rows[i][1]!=v]
 print(b,'completed markers',len(marks),'of',len(rows),'changes',changes)
