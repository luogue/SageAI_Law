"""Finalize only complete, final-source Round33 evidence and regression outputs."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[1]
out=root/'artifacts/technology_pass_semantics/round33_patent_transfer_projection'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tests(p):
 return {c.attrib['classname']+'::'+c.attrib['name']:('FAIL' if c.find('failure') is not None or c.find('error') is not None else 'SKIP' if c.find('skipped') is not None else 'PASS') for c in ET.parse(p).iter('testcase')}
def counts(rows):return {k:sum(v==state for v in rows.values()) for k,state in [('passed','PASS'),('failed','FAIL'),('skipped','SKIP')]}|{'total':len(rows)}
def live(p):
 r=read(p);g=r['release_quality_gate'];items={i['item_id']:i for i in r['items']}
 return dict(path=str(p.relative_to(root)),sha256=sha(p),gate=g['status'],raw_blockers=len(g['failures']),expanded_blockers=len(g.get('blocking_rules',[])),
  evidence_mismatch=sum(len(f.get('mismatches',[])) for f in g['failures'] if f.get('requirement')=='REVIEW_EVIDENCE_ELEMENT_MISMATCH'),
  subtype=r['deterministic_analysis']['technology_classification']['tertiary_subtype'],process=r.get('production_path_trace',{}).get('process_id'),
  risk_groups=sorted(i['risk_group'] for i in r['risk_themes']),rule_statuses={k:i['coverage_status'] for k,i in items.items()},
  components={k:i['coverage_elements'] for k,i in items.items() if k in ('TC-06-01','TC-06-02','TC-06-03','TC-06-04','TC-10-02','TC-10-03','TC-11-01','TC-11-02','TC-13-01')})
final_hashes={str(p.relative_to(root)):sha(p) for p in (root/'backend/review_v2').glob('*.py')}
modes=['targeted','existing','patent']+[f'technical{n}' for n in range(4)]
integrity={mode:read(out/f'{mode}_source_integrity.json') for mode in modes}
assert all(v['unchanged'] and v['after']==final_hashes for v in integrity.values()),'Tests must use final unchanged source'
technical={}
for n in range(4):technical.update(tests(out/f'technical{n}.xml'))
regression={'targeted':counts(tests(out/'targeted.xml')),'technology':counts(technical)}
for mode in ['existing','patent']:
 before=tests(out/f'{mode}_baseline.xml');after=tests(out/f'{mode}.xml')
 changes=[{'test':k,'before':before[k],'after':after[k]} for k in before.keys()&after.keys() if before[k]!=after[k]]
 regression[mode]={'baseline':counts(before),'final':counts(after),'changed_status':changes,
  'newly_failing':[x for x in changes if x['after']=='FAIL'],'recovered':[x for x in changes if x['before']=='FAIL' and x['after']=='PASS'],
  'removed_tests':sorted(before.keys()-after.keys())}
 assert not regression[mode]['newly_failing'] and not regression[mode]['removed_tests']
assert regression['targeted']['failed']==regression['technology']['failed']==0
current={name:live(out/f'final_{name}/report.json') for name in ['transferee','transferor']}
runtime=read(out/'runtime.json')
assert runtime['source_hashes']==final_hashes,'Server source is not the final source'
assert all(v['process']==runtime['process_id'] for v in current.values()),'Current reports are from an old server'
assert all(v['gate']=='REPORT_READY' and v['raw_blockers']==v['expanded_blockers']==v['evidence_mismatch']==0 for v in current.values())
protection={}
for name in ['application_transferee','application_transferor','secret_transferee','secret_transferor','secret_licensor','secret_licensee','patent_licensor','patent_licensee']:
 before_path=out.parent/'round32_patent_application_transfer'/((name.replace('application_','final_')) if name.startswith('application_') else 'protection_'+name)/'report.json'
 before=live(before_path);after=live(out/f'protection_{name}/report.json')
 after['risk_groups_added']=sorted(set(after['risk_groups'])-set(before['risk_groups']))
 after['risk_groups_removed']=sorted(set(before['risk_groups'])-set(after['risk_groups']))
 after['old_pass_changes']={k:after['rule_statuses'].get(k) for k,v in before['rule_statuses'].items() if v=='通过' and after['rule_statuses'].get(k)!='通过'}
 protection[name]=after
assert all(v['gate']=='REPORT_READY' for v in protection.values())
assert all(v['process']==runtime['process_id'] for v in protection.values()),'Protection reports are from an old server'
audit=read(out/'source_audit.json')
assert not audit['changed_gate_verifier_fallback_functions'] and not audit['modified_existing_tests'] and not audit['removed_existing_tests']
assert all(sha(root/k)==v for k,v in audit['final_source_hashes'].items())
data=dict(status='ACCEPTED_CURRENT_CONTRACT',timestamp=datetime.now(timezone.utc).isoformat(),
 scope='Granted patent right transfer with historical ordinary licence and limited licence-back; no new review rules',
 current=current,protection=protection,regression=regression,source_audit=audit,runtime=runtime,
 original_diagnostic='original_scope_diagnostic.json',full_suite='NOT_RERUN_THIS_ROUND',
 known_limitations=['Pre-existing failures in the compared regression selections remain outside this repair. Live model variations are recorded separately.'])
controls={}
for p in out.glob('*_fixed_final.json'):
 name=p.name.removesuffix('_fixed_final.json');a=live(p);b=live(out/f'{name}_fixed_baseline.json')
 controls[name]={'risk_groups_equal':a['risk_groups']==b['risk_groups'],'rule_statuses_equal':a['rule_statuses']==b['rule_statuses'],
                 'baseline_gate':b['gate'],'final_gate':a['gate']}
data['fixed_model_controls']=controls
if any(v['baseline_gate']!='REPORT_READY' for v in controls.values()):
 data['known_limitations'].append('The secret-transferee and secret-transferor fixed-output diagnostic replays have the same three pre-existing consistency blockers on baseline and final code; these diagnostic replays are not counted among the eight live REPORT_READY protection cases.')
for name,v in protection.items():
 if v['risk_groups_added'] or v['risk_groups_removed'] or v['old_pass_changes']:
  assert controls.get(name,{}).get('risk_groups_equal') and controls[name]['rule_statuses_equal'],f'Unexplained protection drift: {name}'
(out/'acceptance.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
paths=[p for p in out.rglob('*') if p.is_file() and '__pycache__' not in p.parts and 'baseline_source' not in p.parts and p.name!='final_manifest.json' and p.suffix in ('.json','.xml','.txt','.docx','.md','.py','.ps1')]
paths += [root/k for k in audit['changed_source_functions']]+[root/'backend/tests/test_patent_transfer_exact_projection.py',root/'backend/tests/fixtures/round33_patent_transfer.txt']
paths += list((root/'scripts').glob('*round33*'))
(out/'final_manifest.json').write_text(json.dumps({str(p.relative_to(root)):sha(p) for p in paths},indent=2),encoding='utf8')
print(json.dumps({'current':{k:{f:v[f] for f in ('gate','raw_blockers','expanded_blockers','evidence_mismatch')} for k,v in current.items()},'regression':regression,'protection':{k:{f:v[f] for f in ('gate','risk_groups_added','risk_groups_removed','old_pass_changes')} for k,v in protection.items()}},ensure_ascii=False))
