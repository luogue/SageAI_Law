"""Record real upload outcomes and element bindings, independently of test totals."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/technology_pass_semantics'
manifest=json.loads((ART/'round8_accept_live_manifest.json').read_text(encoding='utf8'))
targets={'balanced':'TC-11-02','cross_article':'TC-11-01','over_scope':'TC-07-03',
         'ancillary':'TC-09-04','provider':'TECH-SHARED-08'}
before={}
for p in (ART/'round8_close_before').glob('*.json'):
    r=json.loads(p.read_text(encoding='utf8'))
    before[r['test_id']+'|'+hashlib.sha256(r['raw_input'].encode()).hexdigest()]=r
results=[]
for run in manifest:
    if not run.get('report'):
        results.append({'sample':run['sample'],'gate':'NOT_VERIFIED'})
        continue
    report=json.loads(Path(run['report']).read_text(encoding='utf8'))
    blocker_path=ART/('round8_accept_'+run['sample']+'_blockers.json')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'scripts/export_routing_gate_blockers.py'),
                    run['report'],str(blocker_path)],check=True,stdout=subprocess.DEVNULL)
    blockers=json.loads(blocker_path.read_text(encoding='utf8'))
    runtime=report['production_path_trace']
    engine_hash=hashlib.sha256((ROOT/'backend/review_v2/engine.py').read_bytes()).hexdigest()
    item=next((i for i in report['items'] if i['item_id']==targets.get(run['sample'])),{})
    results.append({'sample':run['sample'],'gate':report['release_quality_gate']['status'],
        'contract_type':report['contract_type'],'raw_blockers':blockers['raw_failure_count'],
        'expanded_blockers':blockers['blocker_tuple_count'],'process_id':runtime['process_id'],
        'engine_hash_matches':runtime['runtime_sources']['engine']['sha256']==engine_hash,
        'runtime_drift':runtime.get('runtime_source_drift',{}).get('status'),
        'target_rule':item.get('item_id'),'target_coverage':item.get('coverage_status'),
        'target_elements':item.get('coverage_elements',[]),
        'target_verification':item.get('decision_trace',{}).get('verified_pass_source_gate'),
        'remaining_blockers':[{'code':b['error_code'],'rule_id':b['rule_id'],
            'element_id':b['element_id'],'fact_id':b['fact_id'],'reason':b['reject_reason']}
            for b in blockers['blockers']]})
result={'samples':results,'code_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
    for p in [ROOT/'backend/review_v2'/f for f in ('engine.py','license_control_facts.py',
                                                 'ancillary_fee_facts.py','service_liability_sources.py')]}}
(ART/'round8_close_acceptance.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps([{k:r.get(k) for k in ('sample','gate','raw_blockers','expanded_blockers','target_rule',
                 'target_coverage','engine_hash_matches','runtime_drift')} for r in results],ensure_ascii=False,indent=2))
