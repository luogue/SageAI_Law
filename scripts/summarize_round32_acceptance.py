"""Summarize completed outputs; fail closed on incomplete test or live artifacts."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[1]
out=root/'artifacts/technology_pass_semantics/round32_patent_application_transfer'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tests(p):
 return {c.attrib['classname']+'::'+c.attrib['name']:('FAIL' if c.find('failure') is not None or c.find('error') is not None else 'SKIP' if c.find('skipped') is not None else 'PASS') for c in ET.parse(p).iter('testcase')}
def counts(rows):return dict(total=len(rows),passed=list(rows.values()).count('PASS'),failed=list(rows.values()).count('FAIL'),skipped=list(rows.values()).count('SKIP'))
def live(p):
 r=read(p);gate=r['release_quality_gate'];items={i['item_id']:i for i in r['items']}
 return dict(path=str(p.relative_to(root)),sha256=sha(p),gate=gate['status'],raw_blockers=len(gate['failures']),
 expanded_blockers=len(gate.get('blocking_rules',[])),evidence_mismatch=sum(len(f.get('mismatches',[])) for f in gate['failures'] if f.get('requirement')=='REVIEW_EVIDENCE_ELEMENT_MISMATCH'),
 contract_type=r['report_context']['contract_type_label'],subtype=r['deterministic_analysis']['technology_classification']['tertiary_subtype'],
 process=r.get('production_path_trace',{}).get('process_id'),risk_groups=sorted(i['risk_group'] for i in r['risk_themes']),
 rule_statuses={k:i['coverage_status'] for k,i in items.items()},
 components={k:i['coverage_elements'] for k,i in items.items() if k in ('TC-01-03','TC-03-03','TC-03-04','TC-06-01','TC-06-04','TC-12-01','TC-12-02','TC-13-02','TECH-SHARED-APP-REJECTION-01','COMMON-20-01')})
baseline=tests(out/'baseline_tests.xml');existing=tests(out/'existing.xml');targeted=tests(out/'targeted.xml')
technical={}
for n in range(4):technical.update(tests(out/f'technical{n}.xml'))
changes=[dict(test=k,before=baseline[k],after=existing[k]) for k in baseline.keys()&existing.keys() if baseline[k]!=existing[k]]
new_fail=[r for r in changes if r['after']=='FAIL']
recovered=[r for r in changes if r['before']=='FAIL' and r['after']=='PASS']
integrity={mode:read(out/(mode+'_source_integrity.json')) for mode in ('existing','targeted','technical0','technical1','technical2','technical3')}
assert all(i['unchanged'] for i in integrity.values()),'Source changed during test run'
current_hashes={str(p.relative_to(root)):sha(p) for p in (root/'backend/review_v2').glob('*.py')}
assert all(i['after']==current_hashes for i in integrity.values()),'Tests do not cover final source'
current={name:live(out/f'final_{name}/report.json') for name in ('transferee','transferor')}
protection={}
comparators={
 'secret_transferee':'round31_transfer_consistency/final_transferee',
 'secret_transferor':'round31_transfer_consistency/final_transferor',
 'secret_licensor':'round31_transfer_consistency/protection_licensor',
 'secret_licensee':'round31_transfer_consistency/protection_licensee',
 'patent_licensor':'round30_accepted_current_patent_licensor',
 'patent_licensee':'round30_accepted_current_patent_licensee'}
for name,prior in comparators.items():
 after=live(out/f'protection_{name}/report.json');before=live(out.parent/prior/'report.json')
 after['risk_groups_added']=sorted(set(after['risk_groups'])-set(before['risk_groups']))
 after['risk_groups_removed']=sorted(set(before['risk_groups'])-set(after['risk_groups']))
 after['prior_pass_changes']={k:after['rule_statuses'].get(k) for k,v in before['rule_statuses'].items() if v=='通过' and after['rule_statuses'].get(k)!='通过'}
 protection[name]=after
audit=read(out/'source_audit.json')
assert not audit['changed_gate_verifier_fallback_functions']
assert not audit['modified_existing_tests'] and not audit['removed_existing_tests']
assert not new_fail and not (baseline.keys()-existing.keys())
assert counts(targeted)['failed']==0 and counts(technical)['failed']==0
assert all(r['gate']=='REPORT_READY' and r['raw_blockers']==r['expanded_blockers']==r['evidence_mismatch']==0 for r in current.values())
assert all(r['gate']=='REPORT_READY' for r in protection.values())
data=dict(status='ACCEPTED_CURRENT_CONTRACT_WITH_EXISTING_BASELINE_FAILURES',timestamp=datetime.now(timezone.utc).isoformat(),
 scope='Round32 patent application right transfer; no gate/verifier/fallback changes',
 source_audit=audit,current=current,protection=protection,
 regression={'targeted':counts(targeted),'technology':counts(technical),'existing':counts(existing),'baseline':counts(baseline),
 'newly_failing':new_fail,'recovered':recovered,'changed_status':changes,'added_tests':len(targeted),
 'removed_tests':sorted(baseline.keys()-existing.keys()),'full_suite':'NOT_RERUN_THIS_ROUND'},
 original_diagnostic='original_mismatch_diagnostic.json',
 known_limitations=['12 existing failures in the 155-test application/penalty baseline remain outside this repair; see baseline_tests.xml.',
 'Live model output can vary; protection risk-group/status differences are recorded per sample, not asserted zero without a fixed-output comparison.'])
fixed_before=live(out/'fixed_model_baseline.json');fixed_after=live(out/'fixed_model_final.json')
data['fixed_model_control']={
 'recorded_responses':'round31_transfer_consistency/transfer_fixed_model_outputs.json',
 'baseline_gate':fixed_before['gate'],'final_gate':fixed_after['gate'],
 'baseline_blockers':read(out/'fixed_model_baseline.json')['release_quality_gate']['failures'],
 'final_blockers':read(out/'fixed_model_final.json')['release_quality_gate']['failures'],
 'rule_statuses_equal':fixed_before['rule_statuses']==fixed_after['rule_statuses'],
 'risk_groups_equal':fixed_before['risk_groups']==fixed_after['risk_groups'],
 'gate_equal':read(out/'fixed_model_baseline.json')['release_quality_gate']==read(out/'fixed_model_final.json')['release_quality_gate']}
assert all(data['fixed_model_control'][k] for k in ('rule_statuses_equal','risk_groups_equal','gate_equal'))
data['known_limitations'].append('Archived-model-output replay has the same three COMMON-21-01 consistency blockers on baseline and final code; this diagnostic replay is not counted as a live REPORT_READY protection sample.')
(out/'acceptance.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
paths=[p for p in out.rglob('*') if p.is_file() and 'baseline_source' not in p.parts and '__pycache__' not in p.parts and p.suffix in ('.json','.xml','.py','.ps1','.txt','.docx','.md') and p.name!='final_manifest.json']
paths.extend(root/p for p in audit['changed_source_functions'])
paths.extend([root/'backend/tests/test_application_transfer_exact_projection.py',root/'backend/tests/fixtures/round32_patent_application_transfer.txt'])
paths.extend(root/'scripts'/n for n in ('run_round32_current.ps1','run_round32_protection.ps1','run_round32_tests.py','audit_round32_artifacts.py','summarize_round32_acceptance.py','check_round32_fixed_model.py'))
(out/'final_manifest.json').write_text(json.dumps({str(p.relative_to(root)):sha(p) for p in paths},indent=2),encoding='utf8')
print(json.dumps({'current':{k:{f:v[f] for f in ('gate','raw_blockers','expanded_blockers','evidence_mismatch','subtype')} for k,v in current.items()},'regression':data['regression'],'protection':{k:{f:v[f] for f in ('gate','risk_groups_added','risk_groups_removed','prior_pass_changes')} for k,v in protection.items()}},ensure_ascii=False))
