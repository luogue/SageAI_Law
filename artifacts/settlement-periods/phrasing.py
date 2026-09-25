import sys,json
from pathlib import Path
sys.path.insert(0,'backend')
from review_v2.deepseek_facts import extract
from review_v2.clause_parser import parse_contract_clauses
from review_v2.part_time_settlement import calendar_interval
text='非全日制用工协议\n第一条 工资\n当月一日至十日工资在当月十五日前支付；当月十一日至月末工资在次月五日前支付。'
raw=extract(parse_contract_clauses(text),concept_keys=['salary.settlement_period'])
facts=[f for p in raw for f in p['response']['facts']]
results=[calendar_interval(f['value']) for f in facts]
Path('artifacts/settlement-periods/phrasing.json').write_text(json.dumps({'facts':facts,'calculations':results},ensure_ascii=False,indent=2),encoding='utf8')
assert [r['status'] for r in results]==['PASS','RISK'],results
print('Live semantic extraction and calendar calculation passed')
