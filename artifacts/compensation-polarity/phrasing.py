import sys,json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'backend')
from review_v2.deepseek_facts import extract
from review_v2.clause_parser import parse_contract_clauses
from review_v2.employment_fact_store import normalize
cases=[('终止时单位依法支付经济补偿。','economic_compensation.statutory','kind','STATUTORY_PAY'),('合同终止双方确认不支付任何经济补偿。','economic_compensation.statutory','kind','EXCLUDED'),('劳动者自愿放弃经济补偿。','economic_compensation.statutory','kind','WAIVED'),('未按期完成项目须支付5000元违约金。','penalties.obligations','scope','PROJECT_TASK_PERFORMANCE'),('迟到三次支付500元违约金。','penalties.obligations','scope','ATTENDANCE'),('离职未提前30日通知应支付1000元违约金。','penalties.obligations','scope','RESIGNATION_NOTICE'),('违反离职竞业限制应支付5万元违约金。','penalties.obligations','scope','NON_COMPETE')]
def test(case):
 text,concept,key,expected=case;cs=parse_contract_clauses('劳动合同\n第一条 约定\n'+text)
 raw=extract(cs,concept_keys=[concept]);facts=[f for p in raw for f in p['response']['facts']]
 assert facts,(text,raw)
 assert all(normalize(concept,f['value'])[key]==expected for f in facts),(text,facts)
 byid={c.clause_id:c.text for c in cs}
 assert all(e['quote'] in byid[e['clause_id']] for f in facts for e in f['evidence'])
 return {'source':text,'facts':facts,'status':'PASS'}
with ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(test,cases))
Path('artifacts/compensation-polarity/phrasing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
print('7 real DeepSeek extraction cases passed')
