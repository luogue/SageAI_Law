import json,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[1]
out=root/'artifacts/technology_pass_semantics/round34_cooperative_routing'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def testrows(p):
 return {c.attrib['classname']+'::'+c.attrib['name']:('FAIL' if c.find('failure') is not None or c.find('error') is not None else 'SKIP' if c.find('skipped') is not None else 'PASS') for c in ET.parse(p).iter('testcase')}
def summary(rows):return dict(total=len(rows),passed=list(rows.values()).count('PASS'),failed=list(rows.values()).count('FAIL'))
hashes={str(p.relative_to(root)):sha(p) for p in (root/'backend/review_v2').glob('*.py')}
regression={}
for mode in ['targeted','frozen','technical']:
 integrity=read(out/f'{mode}_source_integrity.json')
 assert integrity['unchanged'] and integrity['after']==hashes,mode+' final source mismatch'
 rows=testrows(out/f'{mode}.xml');regression[mode]=summary(rows)
 assert regression[mode]['failed']==0,mode
baseline={}
for n in range(4):baseline.update(testrows(out.parent/f'round33_patent_transfer_projection/technical{n}.xml'))
final=testrows(out/'technical.xml')
assert baseline==final,'Technical baseline changed'
assert testrows(out.parent/'round33_patent_transfer_projection/targeted.xml')==testrows(out/'frozen.xml')
regression.update(newly_failing=0,old_status_changes=0,removed_tests=0,full_suite='NOT_RUN')
runtime=read(out/'runtime.json');assert runtime['source_hashes']==hashes

def live(p):
 r=read(p);g=r['release_quality_gate']
 assert r['production_path_trace']['process_id']==runtime['process_id'],str(p)
 assert g['status']=='REPORT_READY' and not g['failures'] and not g['blocking_rules'],str(p)
 return dict(path=str(p.relative_to(root)),gate=g['status'],raw_blockers=len(g['failures']),expanded_blockers=len(g['blocking_rules']),
 evidence_mismatch=sum(len(x.get('mismatches',[])) for x in g['failures']),contract_type=r['contract_type_name'],
 risk_groups=sorted(x['risk_group'] for x in r['risk_themes']),statuses={i['item_id']:i['coverage_status'] for i in r['items']})
current={}
for side in ['party_a','party_b']:
 p=out/f'final_{side}/report.json';current[side]=live(p);r=read(p)
 assert r['contract_type_name']=='技术合同—技术开发合同—合作开发合同'
 assert not any(i['item_id'].startswith('S-') for i in r['items'])
 assert not any(t in r['result'] for t in ['买方','需方','商品买卖'])
 current[side]['components']={i['item_id']:i['coverage_elements'] for i in r['items'] if i['item_id'].startswith(('TC-05','TC-07','TC-10','TC-11','TC-12'))}
 current[side]['transaction_layers']=r['deterministic_analysis']['technology_classification']['transaction_layers']
protection={}
for name in ['granted_transferee','granted_transferor','application_transferee','application_transferor','secret_transferee','secret_transferor','secret_licensor','secret_licensee','patent_licensor','patent_licensee']:
 p=out/f'protection_{name}/report.json';row=live(p)
 before=read(out.parent/'round33_patent_transfer_projection'/(name.replace('granted_','final_') if name.startswith('granted_') else 'protection_'+name)/'report.json')
 groups={x['risk_group'] for x in before['risk_themes']};row['added_risk_groups']=sorted(set(row['risk_groups'])-groups);row['removed_risk_groups']=sorted(groups-set(row['risk_groups']))
 row['old_pass_changes']={i['item_id']:row['statuses'].get(i['item_id']) for i in before['items'] if i['coverage_status']=='通过' and row['statuses'].get(i['item_id'])!='通过'}
 protection[name]=row
controls={}
for name,row in protection.items():
 if row['added_risk_groups'] or row['removed_risk_groups'] or row['old_pass_changes']:
  b=read(out/f'{name}_fixed_baseline.json');f=read(out/f'{name}_fixed_final.json')
  statuses=lambda r:{i['item_id']:i['coverage_status'] for i in r['items']}
  groups=lambda r:sorted(i['risk_group'] for i in r['risk_themes'])
  controls[name]=dict(statuses_equal=statuses(b)==statuses(f),risk_groups_equal=groups(b)==groups(f),baseline_gate=b['release_quality_gate']['status'],final_gate=f['release_quality_gate']['status'])
  assert controls[name]['statuses_equal'] and controls[name]['risk_groups_equal'],name+' code drift'
audit=read(out/'source_audit.json');assert not audit['changed_gate_verifier_fallback_functions'] and not audit['modified_existing_tests'] and not audit['removed_existing_tests']
before=read(out/'before_party_a/report.json');after=read(out/'final_party_a/report.json')
data=dict(status='ACCEPTED',timestamp=datetime.now(timezone.utc).isoformat(),current=current,protection=protection,regression=regression,source_audit=audit,runtime=runtime,fixed_model_controls=controls,
 routing_before=before['domain_selection_resolution'],routing_after=after['domain_selection_resolution'],
 rules_before=[i['item_id'] for i in before['items']],rules_after=[i['item_id'] for i in after['items']],
 known_limitations=['No repository-wide full-suite run this round. Any live model variations are compared with fixed-output baseline/final controls; diagnostic controls are separate from real-interface acceptance.'])
(out/'acceptance.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
paths=[p for p in out.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='final_manifest.json']
paths += list((root/'scripts').glob('*round34*'))+[root/'backend/tests/test_cooperative_routing_consistency.py',root/'backend/tests/fixtures/round34_cooperative.txt']
(out/'final_manifest.json').write_text(json.dumps({str(p.relative_to(root)):sha(p) for p in paths},indent=2),encoding='utf8')
print(json.dumps(dict(regression=regression,current={k:{f:v[f] for f in ['gate','raw_blockers','expanded_blockers','evidence_mismatch']} for k,v in current.items()},controls=controls),ensure_ascii=False))
