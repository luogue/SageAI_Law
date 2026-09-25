"""Reproduce source/element acceptance and compare the complete prior baseline."""
import ast
import json
from pathlib import Path
from compare_review_regressions import read
from summarize_round22_acceptance import upload
from review_v2.technology_service_analysis import analyze_payment_schedule

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/technology_pass_semantics'
OUT=ART/'round24_patent_consistency'


def compare(before, after):
    changes={k:[before[k]['status'],after[k]['status']] for k in before.keys()&after.keys() if before[k]['status']!=after[k]['status']}
    newly_failing=[k for k in before.keys()&after.keys() if before[k]['status']=='PASS' and after[k]['status']!='PASS']
    added={k:after[k]['status'] for k in after.keys()-before.keys()}
    result=dict(total=len(after),passed=sum(v['status']=='PASS' for v in after.values()),
                failed=sum(v['status']=='FAIL' for v in after.values()),changes=changes,
                newly_failing=newly_failing,added=added,removed=sorted(before.keys()-after.keys()))
    assert not newly_failing and not result['removed'] and all(s=='PASS' for s in added.values()), result
    return result


def main():
    result={'current':{},'guards':{}}
    original=(OUT/'input/original.txt').read_text(encoding='utf-8')
    payment=analyze_payment_schedule(original)
    assert len(payment['nodes'])==3 and payment['amount_total']==payment['contract_total']==1200000
    assert payment['amount_delta']==0 and payment['percentage_total']==100
    result['payment']={k:payment[k] for k in ('nodes','amount_total','contract_total','amount_delta','percentage_total','payment_groups')}
    expected={'TC-07-01':['permitted_implementation_acts','license_territory'],
              'TC-07-03':['damage_compensation'],
              'TC-07-04':['on_demand_technical_service','patent_status_change_notice'],
              'TC-11-02':['confidentiality_exceptions'],'TC-12-02':['settlement_non_prejudice']}
    for party in ('licensor','licensee'):
        report,summary=upload(OUT/f'current_{party}/report.json')
        assert '专利实施许可' in summary['contract_type']
        items={i['item_id']:i for i in report['items']}
        assert 'GEN-PAY-01' not in items
        summary['rules']={}
        for key, ids in expected.items():
            atoms={e['element_id']:e for e in items[key]['coverage_elements']}
            for eid in ids:
                assert atoms[eid]['status']=='COVERED' and atoms[eid]['evidence_ids'], (key,eid)
            summary['rules'][key]=dict(coverage=items[key]['coverage_status'],
                elements={k:e['status'] for k,e in atoms.items()},
                narrative=items[key]['risk_point_description'],
                sources={k:e.get('supporting_evidence',[]) for k,e in atoms.items() if k in ids})
        exceptions=next(e for e in items['TC-11-02']['coverage_elements'] if e['element_id']=='confidentiality_exceptions')
        assert next(c for c in exceptions['component_coverage'] if c['element_id']=='confidentiality_exception_lawful_acquisition')['status']=='COVERED'
        for item in items.values():
            for e in item['coverage_elements']:
                if e['status']=='MISSING':
                    assert not e.get('supporting_evidence'), (item['item_id'], e['element_id'])
        for key in ('TC-07-01','TC-07-04','TC-12-01','TC-12-02'):
            facts=items[key]['decision_trace']['contract_fact_registry_consumption']['facts']
            for atom in items[key]['coverage_elements']:
                assert facts[atom['source_fact_key']]['status']==('MISSING' if atom['status']=='MISSING' else 'FOUND'), (key,atom)
        for key in ('TC-07-01','TC-11-02'):
            item=items[key]
            narrative=item['narrative_state']
            assert item['risk_point_description']==(narrative['issue'] or narrative['judgment'])
            assert '尚未覆盖' not in item['risk_point_description']
            assert item['applicability']['status']=='APPLICABLE'
        for item in items.values():
            registry=item['decision_trace'].get('contract_fact_registry_consumption',{}).get('facts',{})
            for atom in item['coverage_elements']:
                if atom['status']=='COVERED':
                    assert registry.get(atom.get('source_fact_key'),{}).get('status')!='MISSING'
        result['current'][party]=summary
    for path in sorted(ART.glob('round24_accepted_*/report.json')):
        report,summary=upload(path)
        name=path.parent.name.replace('round24_accepted_','')
        baseline=(ART/f'round23_boundaries/current_{name.removeprefix("recent_secret_")}/report.json'
                  if name.startswith('recent_secret_') else ART/f'round23_accepted_{name}/report.json')
        before=json.loads(baseline.read_text(encoding='utf-8'))
        old={f['risk_group'] for f in before['risk_findings']}
        new={f['risk_group'] for f in report['risk_findings']}
        summary.update(added_risk_groups=sorted(new-old),removed_risk_groups=sorted(old-new))
        assert old==new, (name,summary)
        result['guards'][name]=summary
    assert len(result['guards'])==15
    assert len({s['process_id'] for s in [*result['current'].values(),*result['guards'].values()]})==1
    baseline=read([ART/f'round23_boundaries/full69_batch{i}.xml' for i in (0,1)])
    result['full']=compare(baseline,read([OUT/f'full75_batch{i}.xml' for i in (0,1)]))
    result['supplemental']=compare(read([ART/'round22_routing/supplemental.xml']),read([OUT/'supplemental.xml']))
    focused=read([OUT/'focused.xml'])
    result['focused']=dict(total=len(focused),passed=sum(v['status']=='PASS' for v in focused.values()),
                           failed=sum(v['status']=='FAIL' for v in focused.values()),
                           changes={k:[baseline[k]['status'],v['status']] for k,v in focused.items() if k in baseline and baseline[k]['status']!=v['status']})
    assert not result['focused']['failed']
    def functions(path):
        return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(path.read_text(encoding='utf-8-sig')).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    old=functions(OUT/'baseline_source/engine.py');new=functions(ROOT/'backend/review_v2/engine.py')
    result['changed_engine_functions']=sorted(k for k in old.keys()&new.keys() if old[k]!=new[k])
    result['changed_gate_or_verifier_functions']=[k for k in result['changed_engine_functions'] if 'gate' in k or 'verif' in k or 'audit' in k]
    assert not result['changed_gate_or_verifier_functions']
    (OUT/'acceptance.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('focused','changed_gate_or_verifier_functions')},ensure_ascii=False))
    print('Current:',len(result['current']),'guards:',len(result['guards']),'full:',{k:v for k,v in result['full'].items() if k not in ('added','removed')},'added:',len(result['full']['added']))


if __name__=='__main__':main()
