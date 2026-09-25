"""Audit exact current-service bindings and preserve the prior regression ledger."""
import ast
import difflib
import hashlib
import json
import re
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
from pathlib import Path
from compare_review_regressions import read
from summarize_round22_acceptance import upload

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artifacts/technology_pass_semantics'
OUT = ART / 'round27_consulting_binding'


def comparison(before, after):
    changes = {k: [before[k]['status'], after[k]['status']] for k in before.keys() & after.keys()
               if before[k]['status'] != after[k]['status']}
    return dict(total=len(after), passed=sum(v['status']=='PASS' for v in after.values()),
                failed=sum(v['status']=='FAIL' for v in after.values()), changes=changes,
                newly_failing=[k for k, v in changes.items() if v[0]=='PASS'],
                recovered=sorted(k for k,v in changes.items() if v==['FAIL','PASS']),
                changed_status=changes,
                newly_failing_count=sum(v[0]=='PASS' and v[1]=='FAIL' for v in changes.values()),
                recovered_count=sum(v==['FAIL','PASS'] for v in changes.values()),
                changed_status_count=len(changes),
                added_tests=len(after.keys()-before.keys()), removed_tests=len(before.keys()-after.keys()),
                added={k: after[k]['status'] for k in after.keys()-before.keys()},
                removed=sorted(before.keys()-after.keys()))


def main():
    result = dict(current={}, protection={}, tests={}, modified_files=[])
    result['original_mismatches'] = json.loads((OUT/'before_diagnostics.json').read_text(encoding='utf-8'))
    for party in ('client', 'provider'):
        report, summary = upload(OUT / f'current_{party}/report.json')
        assert summary['contract_type'] == '技术合同—技术咨询合同'
        items = {i['item_id']: i for i in report['items']}
        summary['rules'] = {}
        summary['canonical_source_bindings'] = []
        for key in ('TC-01-03', 'TC-08-01', 'TC-08-02', 'TC-08-03', 'TC-08-04', 'TC-08-05', 'TC-11-01',
                    'TC-11-02', 'TC-11-03', 'TC-11-04', 'TC-12-02'):
            item = items[key]
            summary['rules'][key] = dict(status=item['coverage_status'],
                elements={e['element_id']: e['status'] for e in item['coverage_elements']},
                narrative=item['risk_point_description'])
            registry = item['decision_trace']['contract_fact_registry_consumption']['facts']
            for e in item['coverage_elements']:
                if e['status'] == 'COVERED':
                    assert e.get('source_fact_key'), (key, e)
                    assert registry[e['source_fact_key']]['status'] == 'FOUND', (key, e)
                    assert e.get('supporting_evidence'), (key, e)
                    # EV ids identify the earlier element proof; SRC ids identify
                    # the final verified parser span. The production ownership
                    # contract binds canonical key + element + exact clause/quote,
                    # not equality between these two identifier namespaces.
                    compact = lambda q: re.sub(r'\s+', '', q or '')
                    bound = [s for s in item['evidence_clauses']
                             if e['element_id'] in s.get('supports_element_ids', [])
                             and e['source_fact_key'] in s.get('canonical_fact_keys', [])
                             and any(s.get('clause_id') == f['clause_id'] and
                                     compact(s.get('quote')) == compact(f['quote'])
                                     for f in e['supporting_evidence'])]
                    assert bound and all(s['verified_original'] and s['support_type']=='DIRECT' for s in bound)
                    assert all(e['element_id'] in s['supports_element_ids'] for s in bound)
                    for f in e['supporting_evidence']:
                        assert any(s['clause_id']==f['clause_id'] and compact(s['quote'])==compact(f['quote']) for s in bound)
                    for s in bound:
                        ref, span = s['source_ref'], s['source_span']
                        assert s['raw_text'][ref['local_start']:ref['local_end']]==s['quote']
                        assert span['raw_text']==s['quote']
                        assert s['source_verification']['status']=='PASS'
                    summary['canonical_source_bindings'].append(dict(rule_id=key,
                        element_key=e['element_id'], canonical_fact_key=e['source_fact_key'],
                        element_evidence_ids=e['evidence_ids'], verified_evidence_ids=[s['evidence_id'] for s in bound],
                        sources=[dict(clause_id=s['clause_id'], quote=s['quote'], span=s['source_span']) for s in bound]))
                elif e['status'] == 'MISSING':
                    assert not e.get('supporting_evidence'), (key, e)
        assert summary['rules']['TC-01-03']['elements']['consulting_project']=='COVERED'
        for key in ('TC-08-01','TC-08-02','TC-08-05'):
            assert summary['rules'][key]['status']=='通过'
        for key in ('TC-08-03','TC-08-04','TC-11-01','TC-11-03','TC-11-04','TC-12-02'):
            assert summary['rules'][key]['status']=='部分覆盖'
        expected = {'TC-08-01':['consulting_scope','acceptance_standard'],
                    'TC-08-02':['qualified_consulting_decision_risk','consultant_fault_exception'],
                    'TC-08-04':['defect_trigger','correction_period','correction_remedy'],
                    'TC-08-05':['consulting_fee_total','payment_milestones'],
                    'TC-11-01':['need_to_know_personnel'],
                    'TC-11-02':['confidentiality_period','compelled_disclosure_exception','prior_notice_when_legally_permitted'],
                    'TC-12-02':['notification_requirement']}
        for rule, keys in expected.items():
            assert all(summary['rules'][rule]['elements'][key]=='COVERED' for key in keys)
        for key in ('termination_return_or_delete','processing_deadline','retained_backup_use_restriction'):
            assert summary['rules']['TC-11-03']['elements'][key]=='COVERED'
        for key in ('stop_disclosure','mitigation_obligation'):
            assert summary['rules']['TC-11-04']['elements'][key]=='COVERED'
        for key in ('defense_control','lawyer_selection','settlement_authority'):
            assert summary['rules']['TC-12-02']['elements'][key]=='MISSING'
        assert summary['rules']['TC-11-02']['status'] != '风险条款'
        assert '用于模型、产品优化或其他客户项目' not in summary['rules']['TC-11-02']['narrative']
        result['current'][party] = summary
    for path in sorted(ART.glob('round27_accepted_*/report.json')):
        report, summary = upload(path)
        name = path.parent.name.removeprefix('round27_accepted_')
        baseline = (ART / 'round26_service_binding' / ('current_' + name.removeprefix('service_')) / 'report.json'
                    if name.startswith('service_') else ART / ('round26_accepted_' + name) / 'report.json')
        prior = json.loads(baseline.read_text(encoding='utf-8'))
        old = {f['risk_group'] for f in prior['risk_findings']}
        new = {f['risk_group'] for f in report['risk_findings']}
        summary.update(added_risk_groups=sorted(new-old), removed_risk_groups=sorted(old-new))
        result['protection'][name] = summary
    for name, before, after in (
        ('full', [ART/f'round26_service_binding/full77_batch{i}.xml' for i in (0,1)], [OUT/f'full78_batch{i}.xml' for i in (0,1)]),
        ('supplemental', [ART/'round26_service_binding/supplemental.xml'], [OUT/'supplemental.xml']),
        ('focused', [ART/'round26_service_binding/focused.xml'], [OUT/'focused.xml']),
    ):
        if all(p.exists() for p in after):
            result['tests'][name] = comparison(read(before), read(after))
    baseline = OUT/'baseline_source'
    for source in (ROOT/'backend/review_v2').glob('*.py'):
        old = baseline/source.name
        if not old.exists() or old.read_bytes() != source.read_bytes():
            result['modified_files'].append(str(source))
    def functions(path):
        return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(path.read_text(encoding='utf-8-sig')).body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    old, new = functions(baseline/'engine.py'), functions(ROOT/'backend/review_v2/engine.py')
    result['modified_engine_functions'] = [k for k in old.keys() & new.keys() if old[k] != new[k]]
    result['modified_existing_gate_verifier_functions'] = [k for k in result['modified_engine_functions'] if 'gate' in k or 'verif' in k or 'audit' in k]
    result['source_hashes'] = {Path(p).name: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in result['modified_files']}
    frozen = json.loads((OUT/'full_start_source_hashes.json').read_text(encoding='utf-8-sig'))
    result['unchanged_since_full_test_start'] = all(
        hashlib.sha256((ROOT/'backend/review_v2'/name).read_bytes()).hexdigest() == digest
        for name, digest in frozen.items())
    result['core_files_modified_after_test_freeze'] = [name for name in frozen
        if (ROOT/'backend/review_v2'/name).stat().st_mtime > (OUT/'full_start_source_hashes.json').stat().st_mtime]
    result['partial_claim_verification'] = (
        'Basic claim-handling responsibility supports only the covered component of PARTIAL defense control; '
        'the same source remains insufficient for COVERED defense control. Exact source and actor checks remain active.')
    result['test_manifests'] = [str(OUT/name) for name in (
        'full78_batch0.modules.json', 'full78_batch1.modules.json',
        'focused.nodeids.json', 'supplemental.modules.json')]
    result['old_test_status_change_explanations'] = {}
    assert len(result['protection']) == 19
    assert result['unchanged_since_full_test_start']
    assert not result['core_files_modified_after_test_freeze']
    assert len({s['process_id'] for s in [*result['current'].values(), *result['protection'].values()]}) == 1
    # Cost audit rows now use their published canonical keys. The requirement
    # verifier receives the final PARTIAL status, but still rejects basic claim
    # handling as proof of complete defense control (covered by negative tests).
    assert not result['modified_existing_gate_verifier_functions']
    assert old['_review_evidence_element_gate'] == new['_review_evidence_element_gate']
    result['existing_gate_functions_changed'] = [k for k in old.keys() & new.keys() if 'gate' in k and old[k]!=new[k]]
    result['fallback_code_deltas'] = []
    for source in (ROOT/'backend/review_v2').glob('*.py'):
        prior = baseline/source.name
        diff = difflib.unified_diff(prior.read_text(encoding='utf-8-sig').splitlines() if prior.exists() else [],
                                   source.read_text(encoding='utf-8-sig').splitlines())
        result['fallback_code_deltas'].extend(dict(file=source.name,line=line) for line in diff
            if line.startswith(('+','-')) and not line.startswith(('+++','---')) and 'fallback' in line.lower())
    assert not result['existing_gate_functions_changed'] and not result['fallback_code_deltas']
    assert all(not x['added_risk_groups'] and not x['removed_risk_groups'] for x in result['protection'].values())
    assert set(result['tests']) == {'full','focused','supplemental'}
    assert all(not x['newly_failing'] and not x['removed'] and all(v=='PASS' for v in x['added'].values()) for x in result['tests'].values())
    assert all(set(x['changes']) <= set(result['old_test_status_change_explanations']) for x in result['tests'].values())
    assert len(result['tests']['full']['added']) == 73
    result['test_artifact_provenance'] = {}
    for name in ('full78_batch0','full78_batch1','focused','supplemental'):
        path = OUT/(name+'.xml')
        suite = ET.parse(path).getroot().find('testsuite')
        assert path.stat().st_mtime > (OUT/'full_start_source_hashes.json').stat().st_mtime
        result['test_artifact_provenance'][name] = dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            started_at=suite.get('timestamp'), duration_seconds=suite.get('time'), tests=suite.get('tests'),
            failures=suite.get('failures'), errors=suite.get('errors'),
            completed_at=datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat())
    replay = (OUT/'final_replay.out').read_text(encoding='utf-8-sig')
    last_test_completion = max((OUT/(n+'.xml')).stat().st_mtime for n in result['test_artifact_provenance'])
    for party, summary in result['current'].items():
        assert f'{party} HTTP=200 gate=REPORT_READY process={summary["process_id"]}' in replay
        path = OUT/f'current_{party}/report.json'
        assert path.stat().st_mtime > last_test_completion
        summary.update(http_status=200, replayed_after_all_tests=True,
            report_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    prior_acceptance = json.loads((ART/'round26_service_binding/acceptance.json').read_text(encoding='utf-8'))
    prior_tests = prior_acceptance['old_test_files']['sha256']
    assert all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest for name,digest in prior_tests.items())
    frozen_tests = json.loads((OUT/'full_start_test_hashes.json').read_text(encoding='utf-8'))
    assert all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest for name,digest in frozen_tests.items())
    # The Round26-added service test predates this round, but its filesystem
    # timestamp is not a reliable ordering proof. The frozen test hashes above
    # establish that no test expectation changed during final verification.
    result['old_test_files'] = dict(modified_during_round27=[], sha256=prior_tests)
    result['finalized_at'] = datetime.now(timezone.utc).isoformat()
    result['status'] = 'ACCEPTED'
    destination = OUT/'acceptance.json'
    temporary = OUT/'acceptance.tmp.json'
    temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(destination)
    (OUT/'acceptance.sha256').write_text(hashlib.sha256(destination.read_bytes()).hexdigest()+'  acceptance.json\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','finalized_at','tests')},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
