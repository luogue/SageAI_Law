"""Acceptance must be justified by exact final-code results, never old artifacts."""
import hashlib
import json
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone

root=Path(__file__).resolve().parents[1]
out=root/'artifacts/technology_pass_semantics/round36_consulting_snapshot'
read=lambda p:json.loads(p.read_text(encoding='utf8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def tests(path):
    return {r.attrib['classname']+'::'+r.attrib['name']: 'FAIL' if r.find('failure') is not None or r.find('error') is not None
            else 'SKIP' if r.find('skipped') is not None else 'PASS' for r in ET.parse(path).iter('testcase')}

audit=read(out/'source_audit.json')
assert all(sha(root/p)==h for p,h in audit['source_hashes'].items())
runtime=read(out/'runtime.json')
assert all(sha(root/p)==h for p,h in runtime['source_hashes'].items())
regression={}
for mode in ('targeted','technical','frozen','adjacent'):
    rows=tests(out/f'{mode}.xml')
    integrity=read(out/f'{mode}_source_integrity.json')
    assert integrity['unchanged'] and all(sha(root/p)==h for p,h in integrity['after'].items())
    regression[mode]={'total':len(rows),'passed':list(rows.values()).count('PASS'),'failed':list(rows.values()).count('FAIL')}
    if mode != 'adjacent':
        assert regression[mode]['failed']==0
baseline_adjacent=tests(out/'adjacent_baseline.xml')
final_adjacent=tests(out/'adjacent.xml')
assert baseline_adjacent.keys()==final_adjacent.keys()
new_failures=[key for key,value in final_adjacent.items() if value=='FAIL' and baseline_adjacent[key]!='FAIL']
recoveries=[key for key,value in final_adjacent.items() if value=='PASS' and baseline_adjacent[key]=='FAIL']
assert not new_failures,new_failures
regression['adjacent'].update(baseline_failed=list(baseline_adjacent.values()).count('FAIL'),
    newly_failing=new_failures,recovered=recoveries,
    changed_status={k:[baseline_adjacent[k],v] for k,v in final_adjacent.items() if baseline_adjacent[k]!=v})
oldtechnical=tests(out.parent/'round35_development_consumers/technical.xml')
assert oldtechnical==tests(out/'technical.xml')
oldfrozen={**tests(out.parent/'round35_development_consumers/frozen.xml'),**tests(out.parent/'round35_development_consumers/targeted.xml')}
assert oldfrozen==tests(out/'frozen.xml')
regression.update(newly_failing=0,
    existing_selected_test_status_changes=len(regression['adjacent']['changed_status']),
    removed_tests=0,full_repository_suite='NOT_RUN')
assert 'built in' in (out/'frontend_build.log').read_text(encoding='utf8')
front=(out/'frontend_tests.log').read_text(encoding='utf8')
assert '# fail 0' in front
regression['frontend_tests_log']='frontend_tests.log'
frontend_build_sources={k.replace('\\','/'):v for k,v in read(out/'intermediate_actor_routing/source_audit.json')['source_hashes'].items()}
for path in ('frontend/src/views/ContractReviewV2.vue','frontend/src/utils/api.js'):
    assert sha(root/path)==frontend_build_sources[path], 'Frontend changed after build: '+path

current={}
receipts=read(out/'export_receipts.json')
for side in ('party_a','party_b'):
    r=read(out/f'final_{side}/report.json')
    binding=r['final_review_snapshot']; gate=r['release_quality_gate']
    assert r['production_path_trace']['process_id']==runtime['process_id']
    assert gate['status']=='REPORT_READY' and not gate['failures'] and not gate['blocking_rules']
    assert not gate['blocking_entities'] and not gate['blocking_reasons']
    assert gate['gate_results']['REVIEW_EVIDENCE_ELEMENT_MISMATCH']=='PASS'
    for key in ('review_run_id','report_version','fact_snapshot_id','snapshot_hash','gate_version'):
        assert r[key]==binding[key]==gate[key]
    assert gate['passed_report_version']==binding['report_version']
    items={i['item_id']:i for i in r['items']}
    for rule in ('TC-01-03','TC-01-04','TC-08-01','TC-08-02','TC-08-05'):
        assert items[rule]['coverage_status']=='通过'
    assert items['TC-12-02']['coverage_status']=='部分覆盖'
    assert items['TC-12-02']['applicability']['triggered']
    claims={e['element_id']:e for e in items['TC-12-02']['coverage_elements']}
    assert all(claims[k]['status']=='COVERED' for k in ('notification_requirement','necessary_assistance','provider_infringement_liability'))
    assert all(s['actor']=='LICENSOR' for s in claims['provider_infringement_liability']['supporting_evidence'])
    covered={e['element_id']:e['status'] for e in items['TC-11-02']['coverage_elements']}
    assert all(covered[key]=='COVERED' for key in ('confidentiality_period','public_information_exception',
        'lawful_third_party_source_exception','independent_development_exception','compelled_disclosure_exception'))
    for format in ('docx','pdf'):
        export=receipts[side][format]
        lowered={k.lower():v for k,v in export.items()}
        assert lowered['x-review-run-id']==binding['review_run_id']
        assert lowered['x-report-version']==binding['report_version']
        assert lowered['x-snapshot-hash']==binding['snapshot_hash']
        assert lowered['x-export-artifact-hash']==sha(out/f'final_{side}/export.{format}')
    current[side]={'binding':binding,'gate':'REPORT_READY','raw_blockers':0,'expanded_blockers':0,'evidence_mismatch':0,
        'contract_type':r['contract_type_name'], 'rules':{i:items[i]['coverage_status'] for i in items if i.startswith(('TC-01','TC-08','TC-11','TC-12'))},
        'exports':receipts[side]}

protection={}
for p in sorted(out.glob('protection_*/report.json')):
    r=read(p);g=r['release_quality_gate']
    assert r['production_path_trace']['process_id']==runtime['process_id']
    assert g['status']=='REPORT_READY' and not g['failures'] and not g['blocking_rules'],str(p)
    base=read(out.parent/'round35_development_consumers'/p.parent.name/'report.json')
    groups=lambda data:sorted(t['risk_group'] for t in data['risk_themes'])
    name=p.parent.name.removeprefix('protection_')
    a,b=set(groups(base)),set(groups(r))
    oldstates={i['item_id']:i['coverage_status'] for i in base['items']}
    newstates={i['item_id']:i['coverage_status'] for i in r['items']}
    state_changes={key:[value,newstates.get(key)] for key,value in oldstates.items() if value!=newstates.get(key)}
    protection[name]={'gate':'REPORT_READY','added_risk_groups':sorted(b-a),'removed_risk_groups':sorted(a-b)}
    protection[name]['state_changes']=state_changes
    if a!=b or state_changes:
        before=read(out/f'{name}_fixed_baseline.json');after=read(out/f'{name}_fixed_final.json')
        states=lambda data:{i['item_id']:i['coverage_status'] for i in data['items']}
        before_states,after_states=states(before),states(after)
        corrections={k:[v,after_states.get(k)] for k,v in before_states.items() if v!=after_states.get(k)}
        assert before_states.keys()==after_states.keys()
        assert groups(before)==groups(after), name+' fixed-output risk-group drift'
        if corrections:
            # The user explicitly requested this existing consumer to recognize
            # excluded construction/procurement/software work. Record the
            # source-backed correction, rather than claim zero state drift.
            assert corrections=={'TC-01-04':['待核验','通过']}, (name,corrections)
            corrected=next(i for i in after['items'] if i['item_id']=='TC-01-04')
            assert all(e['status']=='COVERED' and e['supporting_evidence'] for e in corrected['coverage_elements'])
            protection[name]['verified_projection_correction']=corrections
            protection[name]['correction_reason']='Explicit parallel exclusions now bind all construction, procurement and software components; prior REVIEW_NEEDED did not consume these facts.'
        protection[name]['fixed_output_states_and_groups_equal']=not corrections
        protection[name]['control_gates']=[before['release_quality_gate']['status'],after['release_quality_gate']['status']]
assert len(protection)==17

data={'status':'ACCEPTED','timestamp':datetime.now(timezone.utc).isoformat(),
      'original':read(out/'original_version_diagnostics.json'),'current':current,'regression':regression,
      'protection':protection,'source_audit':audit,
      'limitations':['Whole repository suite not run; regression claims apply to recorded selections.',
                     'Real model risk-group differences, if present, are recorded separately from identical-output code controls.']}
(out/'acceptance.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
paths=[p for p in out.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='final_manifest.json']
paths+=list(root.glob('scripts/*round36*'))+list(root.glob('backend/tests/test*final*snapshot*.py'))
paths+=[root/'backend/tests/test_consulting_final_projection.py',root/'backend/tests/test_snapshot_export_routes.py',
        root/'frontend/tests/finalSnapshotExport.test.mjs',root/'backend/tests/fixtures/round36_consulting.txt']
(out/'final_manifest.json').write_text(json.dumps({str(p.relative_to(root)):sha(p) for p in paths},indent=2),encoding='utf8')
print(json.dumps({'status':data['status'],'regression':regression,'protection':len(protection)},ensure_ascii=False))
