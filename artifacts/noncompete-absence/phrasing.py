import sys,json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'backend')
from review_v2.deepseek_facts import extract
from review_v2.clause_parser import parse_contract_clauses
from review_v2.employment_fact_store import normalize
cases=[('员工须妥善保护客户资料和企业商业秘密。',set()),('履行保密责任不得妨碍劳动者依法选择其他工作。',set()),('劳动关系结束后二十四个月内，不得从事与本企业竞争的业务。',{'EXISTS'}),('双方明确不设离职竞业限制。',{'EXPLICIT_NONE'}),('员工应当保守秘密。离职后两年内不得在竞争企业任职。',{'EXISTS'})]
def test(case):
 text,expected=case;cs=parse_contract_clauses('劳动合同\n第一条 约定\n'+text)
 raw=extract(cs,concept_keys=['non_compete.arrangement'])
 facts=[f for p in raw for f in p['response']['facts']]
 assert {normalize(f['concept'],f['value']) for f in facts}==expected,(text,facts)
 assert all('non_compete.arrangement' not in p['response'].get('unresolved_concepts',[]) for p in raw)
 byid={c.clause_id:c.text for c in cs}
 assert all(e['quote'] in byid[e['clause_id']] for f in facts for e in f['evidence'])
 return {'source':text,'facts':facts,'status':'PASS'}
with ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(test,cases))
Path('artifacts/noncompete-absence/phrasing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
print('5 real DeepSeek extraction cases passed')
