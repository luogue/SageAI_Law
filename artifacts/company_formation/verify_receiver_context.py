from pathlib import Path
import json,hashlib
p=Path('artifacts/company_formation/receiver_context_final');r=json.loads((p/'result.json').read_text(encoding='utf-8'));d={i['item_id']:i for i in r['items']}
a=d['CF-02-01']['decision_trace']['contribution_deadline_assessment'];c=d['CF-04-01']['decision_trace']['fund_receiver_context']
assert a['contribution_deadline_present'] and a['contribution_deadline_compliant'] is False
assert d['CF-16-01']['coverage_status']=='风险条款' and d['CF-09-01']['coverage_status']=='风险条款'
assert c['personal_account_receiver_identified'] and all(x['protective_coverage'] is False and x['source_clause_ids'] for x in c['evidence'])
assert '【触发证据，不计入保护覆盖】' in r['result']
assert all(x in d['CF-01-01']['risk_point_description'] for x in ['110%','110万元','戊方','2034-09-30','2031-06-30'])
for key in ['CF-03-01','CF-04-01']:assert d[key]['applicability']['status']=='APPLICABLE'
for key in ['CF-05-01','CF-08-01','CF-12-01','COMMON-23-01','COMMON-24-01']:assert d[key]['coverage_status']=='风险条款'
for key,e in [('CF-02-01','formation_contributions_3'),('CF-10-01','formation_articles_alignment_2'),('COMMON-26-01','common_contract_termination_1')]:assert any(x['element_id']==e and x['result']=='FOUND' for x in d[key]['decision_trace']['element_absence_searches'])
assert not any(x['element_id']=='formation_transfer_exit_3' for x in d['CF-09-01']['coverage_elements'])
assert not any(x['node_id'].startswith('sale_') for x in r['items'])
assert r['release_quality_gate']['status']=='REPORT_READY'
sha=hashlib.sha256(Path('test_data/86 股东协议.docx').read_bytes()).hexdigest()
assert sha==json.loads(Path('artifacts/company_formation/round86_before/summary.json').read_text(encoding='utf-8'))['sha256']
out=dict(status='PASS',tests={'new_rule_cases':16,'regression_passed':326,'full_repository':False},deadline=a,account_context=c,context=r['report_context'],counts={'rules':len(r['items']),'themes':r['risk_theme_count'],'findings':len(r['risk_findings']),**r['final_overview_summary']},source_sha256=sha,all_preservation_assertions='PASS',browser={'review_id':'CR-20260909-110651-C906AA','pid':20908,'runtime':'CURRENT','release_quality_gate':'REPORT_READY'})
(p/'acceptance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out['counts'],ensure_ascii=False))
