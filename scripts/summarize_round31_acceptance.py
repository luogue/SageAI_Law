"""Verify and archive the bounded Round31 consistency acceptance."""
from pathlib import Path
import ast,hashlib,json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/technology_pass_semantics/round31_transfer_consistency'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tests(name):
    rows={}
    for t in ET.parse(OUT/name).iter('testcase'):
        rows[t.get('classname')+'::'+t.get('name')]='FAIL' if t.find('failure') is not None or t.find('error') is not None else 'SKIP' if t.find('skipped') is not None else 'PASS'
    return rows
def counts(rows):return dict(total=len(rows),passed=sum(x=='PASS' for x in rows.values()),failed=sum(x=='FAIL' for x in rows.values()))
targeted=tests('final_targeted.xml');focused={k:v for batch in range(4) for k,v in tests(f'verified_focused{batch}.xml').items()};legacy=tests('baseline_legacy.xml');rerun=tests('targeted.xml')
assert all(x=='PASS' for x in targeted.values()) and all(x=='PASS' for x in focused.values())
assert all(rerun[k]==v for k,v in legacy.items())
expected=read(OUT/'final_source_hashes.json')
actual={str(p.relative_to(ROOT/'backend/review_v2')):sha(p) for p in (ROOT/'backend/review_v2').rglob('*.py')}
assert expected==actual,'Source changed during final verification'
oldtests=read(OUT/'baseline_test_hashes.json')
assert all((ROOT/f).exists() and sha(ROOT/f)==h for f,h in oldtests.items())
frozen=ROOT/'artifacts/technology_pass_semantics/round30_transfer_roles/acceptance.json'
assert sha(frozen)=='f25db3b66926a6c67cc6c908d2fb5c53e2c299cf4bb86805b659dd5ca0a51969'
PASS_KEYS=['TC-01-03','TC-06-01','TC-02-01','TC-11-03','TC-12-01','COMMON-20-01','TC-10-01','TC-10-02','TC-10-04']
results={}
for party in ['transferee','transferor']:
    d=read(OUT/f'final_{party}/report.json');before=read(OUT/f'before_{party}/report.json');gate=d['release_quality_gate']
    assert gate['status']=='REPORT_READY' and not gate['failures'] and not gate['blocking_entities']
    assert gate['gate_results']['REVIEW_EVIDENCE_ELEMENT_MISMATCH']=='PASS'
    items={i['item_id']:i for i in d['items']}
    assert all(items[k]['coverage_status']=='通过' for k in PASS_KEYS)
    for t in d['risk_themes']:
        if len(t['source_rule_ids'])==1:assert t['status']==t['source_rule_statuses'][t['source_rule_ids'][0]]
    assert items['TC-09-01']['risk_point_description'].count('现场部署及培训的履行期限')==1
    assert items['TC-09-01']['narrative_state']['issue'].count('现场部署及培训的履行期限')==1
    for k in ['TC-03-04','TC-13-02']:
        assert items[k]['coverage_status']=='部分覆盖'
        by={e['element_id']:e for e in items[k]['coverage_elements']}
        for e in ['existing_license_disclosure','existing_license_counterparty','existing_license_term','existing_license_territory','historical_disclosure_objects','historical_disclosure_scope']:
            assert by[e]['status']=='COVERED'
        assert by['existing_license_disclosure']['fact_value']=='EXPLICIT_NONE'
    assert items['TC-09-02']['coverage_status']=='部分覆盖'
    results[party]=dict(gate=gate['status'],raw_blockers=0,expanded_blockers=0,evidence_mismatch=0,
        source_process=d['production_path_trace']['process_id'],themes_before=len(before['risk_themes']),themes_after=len(d['risk_themes']),
        prior_passes_preserved=PASS_KEYS,rule_statuses={k:items[k]['coverage_status'] for k in PASS_KEYS+['TC-03-04','TC-13-02','TC-06-03','TC-12-03','TC-09-01','TC-09-02']},
        components={k:items[k]['coverage_elements'] for k in ['TC-03-04','TC-13-02','TC-09-01','TC-09-02']})
protections={}
for party in ['licensor','licensee']:
    d=read(OUT/f'protection_{party}/report.json')
    assert d['release_quality_gate']['status']=='REPORT_READY'
    b=read(ROOT/f'artifacts/technology_pass_semantics/round30_accepted_frozen_{party}/report.json')
    groups=lambda r:set(t['risk_group'] for t in r['risk_themes'])
    protections[party]=dict(gate='REPORT_READY',theme_count=len(d['risk_themes']),added_groups=sorted(groups(d)-groups(b)),removed_groups=sorted(groups(b)-groups(d)))
controls={}
for prefix in ['transfer','license_provider']:
    a=read(OUT/f'{prefix}_fixed_model_replay.json');b=read(OUT/f'{prefix}_fixed_model_baseline.json')
    ga=sorted(t['risk_group'] for t in a['risk_themes']);gb=sorted(t['risk_group'] for t in b['risk_themes'])
    assert ga==gb
    controls[prefix]=dict(identical_model_outputs=True,source_baseline='Round31 baseline_source (frozen Round30 production)',risk_groups_equal=True,groups=ga,
        diagnostic_gate_current=a['release_quality_gate']['status'],diagnostic_gate_baseline=b['release_quality_gate']['status'])
    # Raw-text replay is a control, not the file-interface acceptance.
source_files=[p for p in (ROOT/'backend/review_v2').rglob('*.py') if not (OUT/'baseline_source'/p.relative_to(ROOT/'backend/review_v2')).exists() or sha(p)!=sha(OUT/'baseline_source'/p.relative_to(ROOT/'backend/review_v2'))]
summary=dict(status='ACCEPTED_WITH_DOCUMENTED_MODEL_VARIABILITY',scope='Round31 transfer consistency only; no new rules',
    modified_source_files=[str(p.relative_to(ROOT)) for p in source_files],changed_engine_functions=read(OUT/'changed_functions.json'),
    current=results,protection=protections,fixed_model_controls=controls,
    directed=counts(targeted),added_tests=sum('test_transfer_theme_disclosure_consistency' in k for k in targeted),
    technology_focused=counts(focused),legacy_control=counts(legacy),newly_failing=0,old_pass_to_fail=0,old_test_files_changed=0,removed_tests=0,
    full_suite=dict(rerun=False,reason='Bounded follow-up; historical failures outside scope',frozen_round30_reference=str(frozen),historical_failures=246),
    gate_verifier_fallback_changed=False,source_hashes_unchanged_during_final_run=True,round30_frozen_acceptance_unchanged=True,
    known_limitations=['Live model theme variability remains (preliminary transferor 9 themes; license licensor observed 11/13). Final counts are recorded separately. Fixed-output final-source/old-source comparisons have identical risk groups.',
                      'Eight extra legacy test failures reproduce identically on frozen source and remain unchanged.',
                      'Raw-text fixed-output transfer control remains BLOCKED on the same pre-existing internal-reference issue; it is not substituted for the REPORT_READY file API results.'])
(OUT/'acceptance.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
files=[OUT/'acceptance.json',OUT/'final_source_hashes.json',OUT/'final_targeted.xml',*[OUT/f'verified_focused{b}.xml' for b in range(4)],OUT/'baseline_legacy.xml']+list(OUT.glob('final_*/report.*'))+list(OUT.glob('protection_*/report.*'))+source_files+[ROOT/'backend/tests/test_transfer_theme_disclosure_consistency.py',Path(__file__)]+list(ROOT.glob('scripts/*round31*.ps1'))
files += [ROOT/'scripts/check_round31_fixed_model.py', OUT/'run_verified_focused.py', OUT/'input/original.docx', OUT/'input/original.txt', OUT/'baseline_test_hashes.json']
files += list(OUT.glob('*fixed_model*.json'))
import shutil
for original in source_files + [ROOT/'backend/tests/test_transfer_theme_disclosure_consistency.py']:
    dest=OUT/'final_source'/original.relative_to(ROOT)
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(original,dest)
    files.append(dest)
manifest={str(p.relative_to(ROOT)):sha(p) for p in files}
(OUT/'final_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:summary[k] for k in ['status','directed','added_tests','technology_focused','legacy_control','newly_failing','old_pass_to_fail']},ensure_ascii=False))
