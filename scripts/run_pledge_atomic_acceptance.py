import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'backend'))
from docx import Document
from review_v2.engine import review_contract_v2
source=ROOT/'test_data/68 动产质押合同.docx'
text='\n'.join(p.text for p in Document(source).paragraphs)
r=review_contract_v2(text,'movable_pledge',use_llm=False)
out=ROOT/'artifacts/pledge_atomic_acceptance';out.mkdir(parents=True,exist_ok=True)
(out/'report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'report.md').write_text(r['result'],encoding='utf-8')
conflicts=[]
for i in r['items']:
 found={e['element_id'] for e in i.get('coverage_elements',[]) if e['status']=='COVERED'}
 for a in i['decision_trace'].get('element_absence_searches',[]):
  if a['result']=='NOT_FOUND' and a['element_id'] in found: conflicts.append((i['item_id'],a['element_id']))
 if i['item_id'] in ['SEC-01-01','S-00-01']:
  print(json.dumps({k:i.get(k) for k in ['item_id','coverage_status','coverage_elements','evidence_clauses','risk_point_description']},ensure_ascii=False))
print(json.dumps(dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),conflicts=conflicts,coverage=r['coverage_summary'],gate=r['release_quality_gate']),ensure_ascii=False))
assert not conflicts
