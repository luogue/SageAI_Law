"""Merge disjoint final-source test shards, never an incomplete/old run."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
out=root/'artifacts/technology_pass_semantics/round33_patent_transfer_projection'
hashes={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'backend/review_v2').glob('*.py')}
combined=ET.Element('testsuites');seen=set();logs=[]
for n in range(3):
 integrity=json.loads((out/f'patent{n}_source_integrity.json').read_text(encoding='utf8'))
 assert integrity['unchanged'] and integrity['before']==integrity['after']==hashes
 xml=ET.parse(out/f'patent{n}.xml')
 for case in xml.iter('testcase'):
  key=(case.attrib['classname'],case.attrib['name'])
  assert key not in seen
  seen.add(key)
 for suite in xml.getroot():combined.append(suite)
 logs.append((out/f'patent{n}.log').read_text(encoding='utf8'))
assert len(seen)==150
ET.ElementTree(combined).write(out/'patent.xml',encoding='utf-8',xml_declaration=True)
(out/'patent.log').write_text('\n'.join(logs),encoding='utf8')
(out/'patent_source_integrity.json').write_text(json.dumps({'before':hashes,'after':hashes,'unchanged':True,'validated_shards':3},indent=2),encoding='utf8')
print('Merged',len(seen),'final-source tests')
