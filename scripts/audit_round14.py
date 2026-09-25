"""Frozen-input acceptance and per-test-ID comparison (no output rewriting)."""
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from compare_review_regressions import read

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/technology_pass_semantics'

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def risks(report):
    return {f['risk_group']:dict(rules=sorted(f['source_review_ids']),
        missing=sorted(e['element_id'] for e in f['final_missing_elements']),
        adverse=sorted(e['element_id'] for e in f['final_adverse_elements'])) for f in report['risk_findings']}

def main(prefix='full35'):
    before=load(ART/'round14_before/report.json')
    after=load(ART/'round14_final_entrusted_live/report.json')
    old={i['item_id']:i for i in before['items']}
    new={i['item_id']:i for i in after['items']}
    diff=[]
    for rid in new:
        a={e['element_id']:e for e in old[rid]['coverage_elements']}
        b={e['element_id']:e for e in new[rid]['coverage_elements']}
        changed=[dict(element_id=k,before=a.get(k,{}).get('status'),after=e['status'],
                      clauses=e.get('source_clause_ids'),spans=e.get('source_spans'),
                      residual=e.get('residual_gap'),fact_key=e.get('source_fact_key'))
                 for k,e in b.items() if a.get(k,{}).get('status')!=e['status']]
        if changed or old[rid]['coverage_status']!=new[rid]['coverage_status']:
            diff.append(dict(rule_id=rid,before=old[rid]['coverage_status'],after=new[rid]['coverage_status'],elements=changed))
    source_states=defaultdict(list)
    false_partial=[]
    for item in after['items']:
        for e in item['coverage_elements']:
            if e.get('source_fact_key'):
                source_states[e['source_fact_key']].append(dict(rule=item['item_id'],element=e['element_id'],status=e['status']))
            if e['status']=='PARTIALLY_COVERED' and not e.get('source_spans'):
                false_partial.append(dict(rule=item['item_id'],element=e['element_id']))
    conflicts={k:rows for k,rows in source_states.items() if any(r['status']=='COVERED' for r in rows)
               and any(r['status']=='MISSING' for r in rows)}
    engine=hashlib.sha256((ROOT/'backend/review_v2/engine.py').read_bytes()).hexdigest()
    guards=[]
    manifest=ART/'round14_final_live_manifest.json'
    if manifest.exists():
        for entry in load(manifest):
            if entry.get('status')=='NOT_VERIFIED':
                guards.append(entry);continue
            name=entry['sample']; r=load(Path(entry['report'])); prior=load(ART/f'round13_final_{name}_live/report.json')
            a,b=risks(prior),risks(r)
            guards.append(dict(sample=name,gate=r['release_quality_gate']['status'],
                blockers=r['release_quality_gate']['failures'],
                engine_hash_matches=r['production_path_trace']['runtime_sources']['engine']['sha256']==engine,
                lost_risk_groups=sorted(a.keys()-b.keys()),
                changed_risks={k:dict(before=a[k],after=b[k]) for k in a.keys()&b.keys() if a[k]!=b[k]}))
    out=dict(before_gate=before['release_quality_gate']['status'],original_blockers=before['release_quality_gate']['failures'],
        gate=after['release_quality_gate']['status'],raw_blockers=len(after['release_quality_gate']['failures']),
        expanded_blockers=sum(len(f.get('details') or f.get('mismatches') or [f]) for f in after['release_quality_gate']['failures']),
        engine_hash=engine,live_engine_hash=after['production_path_trace']['runtime_sources']['engine']['sha256'],
        process_id=after['production_path_trace']['process_id'],
        input_sha256=hashlib.sha256((ART/'round14_entrusted_input/original.docx').read_bytes()).hexdigest(),
        business_modules={name:hashlib.sha256((ROOT/'backend/review_v2'/name).read_bytes()).hexdigest()
            for name in ('engine.py','obligation_detail_elements.py','development_exit.py','domain_selection.py',
                         'technology_transaction_evidence.py','technical_component_facts.py','technology_fact_ontology.py',
                         'report_state_consistency.py','element_evidence_projection.py','entrusted_development_elements.py','material_disposition.py')},
        diff=diff,tc1202=new['TC-12-02']['coverage_elements'],false_partial=false_partial,
        canonical_conflicts=conflicts,guards=guards,test_migrations=0)
    paths=sorted(ART.glob(prefix+'_batch*.xml'))
    if len(paths)==2:
        baseline=read(sorted(ART.glob('full31_batch*.xml'))); current=read(paths); shared=baseline.keys()&current.keys()
        out['tests']=dict(pass_count=sum(v['status']=='PASS' for v in current.values()),
            fail_count=sum(v['status']=='FAIL' for v in current.values()),
            recovered=sorted(k for k in shared if baseline[k]['status']=='FAIL' and current[k]['status']=='PASS'),
            newly_failing={k:current[k]['message'] for k in sorted(shared) if baseline[k]['status']=='PASS' and current[k]['status']=='FAIL'},
            new_tests={k:current[k]['status'] for k in sorted(current.keys()-baseline.keys())},
            removed=sorted(baseline.keys()-current.keys()))
    (ART/'round14_final_summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:out[k] for k in ('gate','raw_blockers','expanded_blockers','false_partial','canonical_conflicts')},ensure_ascii=False))
    for guard in guards:
        print(guard['sample'],guard.get('gate') or guard.get('status'),guard.get('lost_risk_groups'),guard.get('changed_risks'))
    if 'tests' in out: print(json.dumps(out['tests'],ensure_ascii=False,indent=2))

if __name__=='__main__':
    import sys
    main(sys.argv[1] if len(sys.argv)>1 else 'full35')
