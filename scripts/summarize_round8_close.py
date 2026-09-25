"""Final ID comparisons and live-version audit, without synthesizing gate results."""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/technology_pass_semantics'
def suite(prefix):
    files=list(ART.glob(prefix+'_batch*.xml'))
    if len(files)!=6: raise RuntimeError(f'{prefix}: expected all six completed batches')
    return {c.get('classname')+'::'+c.get('name'):
            'FAIL' if c.find('failure') is not None or c.find('error') is not None else 'SKIP' if c.find('skipped') is not None else 'PASS'
            for path in files for c in ET.parse(path).iter('testcase')}
current=suite('full25')
baselines={r:suite(p) for r,p in [('Round6','full12'),('Round7','full16'),('Round8','full19')]}
comparisons={}
for name,before in baselines.items():
    comparisons[name]={'recovered':[k for k,v in before.items() if v=='FAIL' and current.get(k)=='PASS'],
                       'newly_failing':[k for k,v in before.items() if v=='PASS' and current.get(k)=='FAIL'],
                       'added':[k for k in current if k not in before],
                       'removed':[k for k in before if k not in current]}
previous=json.loads((ART/'round8_adjudication.json').read_text(encoding='utf8'))
targets={i['test_id']:current[i['test_id']] for i in previous['items'] if i['current']['status']=='FAIL'}
protected={i['test_id']:current[i['test_id']] for i in previous['items'] if i['current']['status']=='PASS'}
files=['engine.py','license_control_facts.py','ancillary_fee_facts.py','service_liability_sources.py']
hashes={f:hashlib.sha256((ROOT/'backend/review_v2'/f).read_bytes()).hexdigest() for f in files}
live=json.loads((ART/'round8_accept_live_manifest.json').read_text(encoding='utf8'))
live_result=[]
for sample in live:
    runtime=sample.get('runtime') or {}
    entry={'sample':sample['sample'],'gate':sample['gate']['status'],'raw_blockers':len(sample['gate'].get('failures',[])),
           'process_id':runtime.get('process_id'),'engine_hash_matches':runtime.get('runtime_sources',{}).get('engine',{}).get('sha256')==hashes['engine.py'],
           'entrypoint':runtime.get('entrypoint'),'run_mode':runtime.get('run_mode'),'report':sample.get('report')}
    blocker_file=ART/('round8_accept_'+sample['sample']+'_blockers.json')
    if blocker_file.exists(): entry['expanded_blockers']=json.loads(blocker_file.read_text(encoding='utf8'))['blocker_tuple_count']
    live_result.append(entry)
result={'counts':{s:sum(v==s for v in current.values()) for s in ('PASS','FAIL','SKIP')},
        'comparisons':comparisons,'remaining_five':targets,'protected_twenty_one':protected,
        'prior_eight':{k:current[k] for k in previous['prior_eight']},
        'prior_twenty_two':{k:current[k] for k in previous['round7_new_guards']},
        'prior_sixteen':{k:current[k] for k in previous['new_tests']},
        'code_hashes':hashes,'live':live_result,
        'migration_ids':['backend.tests.test_technical_secret_transfer_contract_review::test_ancillary_service_fee_keeps_covered_base_and_only_reports_excess_fee_gaps',
                         'backend.tests.test_technical_secret_transfer_contract_review::test_service_fee_and_confidentiality_use_only_direct_operational_clauses']}
(ART/'round8_close_final_summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'counts':result['counts'],'comparisons':{k:{metric:len(ids) for metric,ids in value.items()} for k,value in comparisons.items()},'remaining_five':targets,'live':live_result},ensure_ascii=False,indent=2))
