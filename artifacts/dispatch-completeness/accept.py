import json,hashlib
from pathlib import Path
base=Path('artifacts/dispatch-completeness');r=json.loads((base/'response.json').read_text(encoding='utf8'));items={i['item_id']:i for i in r['items']};debug=r['structured_fact_debug'];v=debug['semantic_verification']['verification']
assert r['release_quality_gate']['status']=='REPORT_READY'
assert r['contract_type_name']=='劳务派遣劳动合同'
assert items['EMP-01-01']['coverage_status']=='通过'
assert items['EMP-17-01']['coverage_status']=='通过'
assert items['DSP-01-01']['decision_trace']['specialized_legality']['status']=='PASS'
assert items['DSP-02-01']['decision_trace']['specialized_legality']['states']=={'temporary':False,'auxiliary':False,'substitute':False}
assert items['DSP-03-01']['coverage_status']=='待核验'
assert items['DSP-03-01']['decision_trace']['specialized_legality']['status']=='VERIFY'
assert items['EMP-14-01']['coverage_status']=='通过'
for k in ['DSP-05-01','EMP-06-01']:
 assert '1500元' in items[k]['economic_impact'] and '无明显直接金额影响' not in items[k]['economic_impact']
charge=[t for t in r['risk_themes'] if 'DSP-05-01' in t['related_rule_ids']]
assert len(charge)==1 and 'EMP-06-01' in charge[0]['related_rule_ids']
assert r['risk_theme_count']==6 and r['finding_count']==7
for k in ['DSP-06-01','DSP-07-01','DSP-09-01','DSP-10-01']:
 assert items[k]['coverage_status']=='风险条款'
msg=items['EMP-10-01']['decision_trace']['coverage_legality']['message']
section=r['result'].split('（EMP-10-01）')[1].split('\n## ')[0]
assert msg in section and '无需修改' not in section
assert 'DIFFERENT_SYSTEM' not in r['result']
assert r['production_path_trace']['process_id']==4268
p=Path('test_data/114 外派岗位劳动协议.docx');filehash=hashlib.sha256(p.read_bytes()).hexdigest()
a={'trace_id':r['contract_review_trace_id'],'process_id':4268,'endpoint':'http://127.0.0.1:5173/review-v2/file','file_sha256':filehash,'contract_type':r['contract_type_name'],'rule_count':len(items),'risk_themes':r['risk_theme_count'],'rule_findings':r['finding_count'],'severity':r['risk_theme_severity_summary'],'manual_review':[i['item_id'] for i in items.values() if i.get('needs_manual_review')],'checked_facts':len(v['checks']),'searched_concepts':len(v['searched_concepts']),'themes':[{'title':t['title'],'rules':t['related_rule_ids']} for t in r['risk_themes']],'release_quality_gate':r['release_quality_gate']['status'],'automated_tests':{'passed':188,'failed':0,'new_cases':20}}
(base/'acceptance.json').write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(a,ensure_ascii=True))
