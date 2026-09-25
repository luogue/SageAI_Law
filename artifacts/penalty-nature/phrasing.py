import sys,json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'backend')
from review_v2.deepseek_facts import extract
from review_v2.clause_parser import parse_contract_clauses
from review_v2.employment_fact_store import normalize
cases=[('设备损坏按实际损失赔偿。',{'worker.damage_liability'}),('损坏设备应赔偿800元。',{'penalties.obligations'}),('每逾期一日支付100元违约金。',{'penalties.obligations'}),('依法承担赔偿责任。',{'worker.damage_liability'}),('从工资中扣收800元设备保证金，归还后退还。设备因故意或重大过失损坏，按实际损失依法处理。',{'worker.security_payment','worker.damage_liability'})]
def test(case):
 text,expected=case;cs=parse_contract_clauses('劳动合同\n第一条 约定\n'+text)
 raw=extract(cs,concept_keys=['penalties.obligations','worker.damage_liability','worker.security_payment'])
 facts=[f for p in raw for f in p['response']['facts']]
 assert {f['concept'] for f in facts}==expected,(text,facts)
 for f in facts: normalize(f['concept'],f['value'])
 assert all(not p['response'].get('unresolved_concepts',[]) for p in raw)
 byid={c.clause_id:c.text for c in cs}
 assert all(e['quote'] in byid[e['clause_id']] for f in facts for e in f['evidence'])
 return {'source':text,'facts':facts,'status':'PASS'}
with ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(test,cases))
Path('artifacts/penalty-nature/phrasing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
print('5 real DeepSeek extraction cases passed')
