import sys,json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'backend')
from review_v2.deepseek_facts import extract
from review_v2.clause_parser import parse_contract_clauses
from review_v2.employment_conditions import normalize
cases=[('绩效低于80分可以退回。',{'ALLOWED_RETURN_REASON'}),('不得仅因绩效低于80分退回。',{'PROHIBITED_RETURN_REASON'}),('绩效低于80分不当然构成退回事由。',{'PROHIBITED_RETURN_REASON'}),('发生法律规定可以退回的情形时依法退回。',{'LEGAL_REFERENCE_ONLY'}),('岗位考核未达标可以退回，但不得仅因团队文化不匹配退回。',{'ALLOWED_RETURN_REASON','PROHIBITED_RETURN_REASON'})]
def test(case):
 text,expected=case;cs=parse_contract_clauses('劳务派遣劳动合同\n第一条 退回\n'+text)
 raw=extract(cs,concept_keys=['dispatch.return_terms']);facts=[f for p in raw for f in p['response']['facts']]
 vals=[normalize(f['concept'],f['value']) for f in facts]
 assert {v['disposition'] for v in vals}==expected,(text,vals)
 byid={c.clause_id:c.text for c in cs}
 assert all(e['quote'] in byid[e['clause_id']] for f in facts for e in f['evidence'])
 return {'source':text,'facts':facts,'status':'PASS'}
with ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(test,cases))
Path('artifacts/dispatch-return-polarity/deepseek-phrasing-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
print('5 real DeepSeek extraction cases passed')
