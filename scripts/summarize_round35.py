"""Fail closed when any Round35 acceptance artifact is absent or inconsistent."""
import json,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[1]
out=root/'artifacts/technology_pass_semantics/round35_development_consumers'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cases(p):
 return {c.attrib['classname']+'::'+c.attrib['name']:('FAIL' if c.find('failure') is not None or c.find('error') is not None else 'SKIP' if c.find('skipped') is not None else 'PASS') for c in ET.parse(p).iter('testcase')}
hashes={str(p.relative_to(root)):sha(p) for p in (root/'backend/review_v2').glob('*.py')}
runtime=read(out/'runtime.json');assert runtime['source_hashes']==hashes
regression={}
for mode in ('targeted','technical','frozen'):
 integrity=read(out/f'{mode}_source_integrity.json')
 assert integrity['unchanged'] and integrity['after']==hashes,mode+' source mismatch'
 rows=cases(out/f'{mode}.xml')
 regression[mode]=dict(total=len(rows),passed=list(rows.values()).count('PASS'),failed=list(rows.values()).count('FAIL'))
 assert regression[mode]['failed']==0,mode
old=cases(out.parent/'round34_cooperative_routing/technical.xml')
new=cases(out/'technical.xml')
assert old==new,'technical states changed'
oldf={**cases(out.parent/'round34_cooperative_routing/targeted.xml'),**cases(out.parent/'round34_cooperative_routing/frozen.xml')}
assert oldf==cases(out/'frozen.xml'),'frozen states changed'
regression.update(newly_failing=0,old_status_changes=0,removed_tests=0,full_repository_suite='NOT_RUN')
def live(p):
 r=read(p);g=r['release_quality_gate']
 assert r['production_path_trace']['process_id']==runtime['process_id'],str(p)
 engine=[v for v in r['production_path_trace']['runtime_sources'].values() if str(v.get('file','')).replace('\\','/').endswith('/review_v2/engine.py')]
 assert engine and all(v['sha256']==sha(root/'backend/review_v2/engine.py') for v in engine),'live engine hash mismatch'
 assert g['status']=='REPORT_READY' and not g['failures'] and not g['blocking_rules'],str(p)
 assert g['gate_results']['REVIEW_EVIDENCE_ELEMENT_MISMATCH']=='PASS',str(p)
 return r,dict(path=str(p.relative_to(root)),gate=g['status'],raw_blockers=0,expanded_blockers=0,evidence_mismatch=0,
               contract_type=r['contract_type_name'],risk_groups=sorted(x['risk_group'] for x in r['risk_themes']),
               statuses={i['item_id']:i['coverage_status'] for i in r['items']})
current={}
for side in ('party_a','party_b'):
 r,row=live(out/f'final_{side}/report.json')
 assert r['contract_type_name']=='技术合同—技术开发合同—委托开发合同'
 items={i['item_id']:i for i in r['items']}
 assert 'TECH-SHARED-10' not in items or items['TECH-SHARED-10']['risk_status']!='ADVERSE'
 required={'TC-01-03':['project_identity','functional_scope','performance_scope'],
 'TC-04-01':['commissioned_project_and_objective','functional_and_technical_scope','schedule_and_milestones','acceptance'],
 'TC-04-04':['no_fault_technical_risk_allocation','failed_development_incurred_cost_settlement'],
 'TC-04-03':['inventor_authorship'],
 'TC-05-04':['payment_delay_liability'],
 'TC-11-01':['confidential_information_scope','during_contract_confidentiality'],
 'TC-11-02':['confidentiality_duration','confidentiality_exceptions'],
 'TC-13-03':['acceptance_metrics','acceptance_deadline','rectification_obligation','rectification_deadline','reinspection_procedure']}
 for rule,keys in required.items():
  states={e['element_id']:e['status'] for e in items[rule]['coverage_elements']}
  assert all(states.get(k)=='COVERED' for k in keys),(side,rule,states)
 assert items['TC-11-03']['coverage_status']=='通过'
 termination=next(e for e in items['TC-05-04']['coverage_elements'] if e['element_id']=='development_termination_mechanism')
 assert termination['status']=='PARTIALLY_COVERED' and '解除权' in termination['residual_gap']
 for rule in ('TC-03-04','TC-13-02'):
  assert items[rule]['coverage_status']=='部分覆盖'
 row['components']={k:items[k]['coverage_elements'] for k in [*required,'TC-11-03','TC-03-03','TC-03-04','TC-13-02']}
 before=read(out/f'before_{side}/report.json')
 row['status_changes']={i['item_id']:[i['coverage_status'],row['statuses'].get(i['item_id'])]
                        for i in before['items'] if row['statuses'].get(i['item_id'])!=i['coverage_status']}
 current[side]=row
protection={}
for p in sorted(out.glob('protection_*/report.json')):
 name=p.parent.name.replace('protection_','')
 _,row=live(p)
 base=(out.parent/'round34_cooperative_routing'/('final_party_'+name[-1] if name.startswith('cooperative_') else p.parent.name)/'report.json')
 if name in ('service_client','service_provider','consulting_client','consulting_provider','entrusted'):
  base=out.parent/('round30_accepted_'+name)/'report.json'
 b=read(base)
 oldgroups={x['risk_group'] for x in b['risk_themes']}
 row['added_risk_groups']=sorted(set(row['risk_groups'])-oldgroups)
 row['removed_risk_groups']=sorted(oldgroups-set(row['risk_groups']))
 row['old_pass_changes']={i['item_id']:row['statuses'].get(i['item_id']) for i in b['items']
                          if i['coverage_status']=='通过' and row['statuses'].get(i['item_id'])!='通过'}
 if row['added_risk_groups'] or row['removed_risk_groups'] or row['old_pass_changes']:
  a=read(out/f'{name}_fixed_baseline.json');z=read(out/f'{name}_fixed_final.json')
  statuses=lambda r:{i['item_id']:i['coverage_status'] for i in r['items']}
  groups=lambda r:sorted(i['risk_group'] for i in r['risk_themes'])
  row['fixed_output_control']=dict(statuses_equal=statuses(a)==statuses(z),risk_groups_equal=groups(a)==groups(z))
  assert row['fixed_output_control']==dict(statuses_equal=True,risk_groups_equal=True),name+' code drift'
  row['fixed_output_control']['diagnostic_gate_status']={
   'baseline':a['release_quality_gate']['status'],'final':z['release_quality_gate']['status']}
  row['fixed_output_control']['purpose']='Identical model output comparison; not a substitute for real HTTP acceptance.'
 protection[name]=row
assert len(protection)==17
audit=read(out/'source_audit.json')
assert not audit['changed_gate_verifier_fallback_functions'] and not audit['modified_existing_tests'] and not audit['removed_existing_tests']
data=dict(status='ACCEPTED',timestamp=datetime.now(timezone.utc).isoformat(),original_conflicts=read(out/'original_conflicts.json'),
 current=current,protection=protection,regression=regression,source_audit=audit,runtime=runtime,
 known_limitations=['Repository-wide full suite not run; regression claims apply to the recorded selections.',
 'Live risk-group differences were observed for cooperative_a, secret_licensor and secret_transferee. Identical model-output baseline/final controls reproduced equal rule states and risk groups; live outputs are not claimed to have zero drift.'])
(out/'acceptance.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
paths=[p for p in out.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='final_manifest.json']
paths+=list((root/'scripts').glob('*round35*'))+[root/'backend/tests/test_development_consumer_snapshot.py',root/'backend/tests/fixtures/round35_entrusted_development.txt']
(out/'final_manifest.json').write_text(json.dumps({str(p.relative_to(root)):sha(p) for p in paths},indent=2),encoding='utf8')
print(json.dumps(dict(status=data['status'],regression=regression,protection=len(protection)),ensure_ascii=False))
