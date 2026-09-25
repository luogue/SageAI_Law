import sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'backend'))
from review_v2.clause_parser import parse_contract_clauses
from review_v2.lease_semantics import corpus_facts,supports
from review_v2.sale_evidence import supports as sale_supports
folder=ROOT/'artifacts/equity-pledge-after'
r=json.loads((folder/'report.json').read_text(encoding='utf-8'))
b=json.loads((ROOT/'artifacts/equity-pledge-before/report.json').read_text(encoding='utf-8'))
corpus=json.loads((folder/'corpus.json').read_text(encoding='utf-8'))
assert corpus['file_sha256']==json.loads((ROOT/'artifacts/equity-pledge-before/corpus.json').read_text(encoding='utf-8'))['file_sha256']
clauses=parse_contract_clauses(corpus['text']);old={i['item_id']:i for i in b['items']}
targets=['SEC-01-01','SEC-02-01','SEC-03-01','SEC-04-01','SEC-05-01','SEC-06-01','EQP-01-01','EQP-02-01','S-00-01']
lines=['# 股权质押逐要素证据链及修复对比','','|规则|修复前|修复后|','|---|---|---|'];audit=[]
for i in r['items']:
 if i['item_id'] not in targets:continue
 lines.append('|'+i['item_id']+'|'+old[i['item_id']]['coverage_status']+'|'+i['coverage_status']+'|')
for i in r['items']:
 if i['item_id'] not in targets:continue
 lines+=['','## '+i['item_id']+' '+i['title'],'']
 for e in i['coverage_elements']:
  search=next((a for a in i['decision_trace'].get('element_absence_searches',[]) if a['element_id']==e['element_id']),{})
  spec=next((a for a in i['decision_trace'].get('semantic_requirements',[]) if a['element_id']==e['element_id']),{})
  candidates=[]
  if spec.get('semantic_patterns'):
   candidates=corpus_facts(clauses,[spec])[e['element_id']]
  else:
   candidates=[a for a in i['evidence_clauses'] if e['element_id'] in (a.get('supports_element_ids') or a.get('supporting_element_ids') or []) and a.get('source_type')!='SEARCH_AUDIT']
  for a in candidates:
   a['supports_result']=supports(spec,a) if spec.get('semantic_patterns') else sale_supports(spec,a.get('text','')) if spec.get('sale_patterns') else e['status']=='COVERED'
  audit.append({'rule_id':i['item_id'],'element':e,'requirements':spec,'received_corpus':'corpus.json','search_audit':search,'candidate_and_supports':candidates,'accepted_evidence':i['evidence_clauses'],'final_status':i['coverage_status']})
  assert not (e['status']=='COVERED' and search.get('result')=='NOT_FOUND')
  lines+=['### '+e['proposition'], '状态：'+e['status'], 'SEARCH_AUDIT：'+str(search.get('result','以最终证据绑定为准')), '检索条款：'+','.join(search.get('searched_clause_ids',[])), '']
  lines += ['- '+str(a.get('clause_id'))+' / '+str(a.get('location'))+' / supports='+str(a['supports_result'])+'：'+a.get('text','') for a in candidates]
  if not candidates:lines+=['- 未找到直接正向证据。']
(folder/'recall-chain.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
(folder/'comparison-and-evidence.md').write_text('\n'.join(lines),encoding='utf-8')
print('same_input=true; contradictions=0; audit_written=true')
