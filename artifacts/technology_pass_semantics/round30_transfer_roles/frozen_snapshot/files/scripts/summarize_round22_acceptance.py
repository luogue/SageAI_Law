"""Check final-source real uploads and compare complete regression runs."""
import hashlib
import json
import ast
from pathlib import Path
from compare_review_regressions import read

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT/'artifacts/technology_pass_semantics'
OUT = ART/'round22_routing'


def upload(path):
    r = json.loads(path.read_text(encoding='utf-8'))
    gate = r['release_quality_gate']
    def leaves(rows):
        return sum(leaves(children) if (children := next((row[k] for k in ('details', 'failures', 'mismatches') if isinstance(row.get(k), list) and row[k]), [])) else 1 for row in rows)
    runtime = r['production_path_trace']
    result = dict(report=str(path), gate=gate['status'], raw_blockers=len(gate['failures']),
                  expanded_blockers=leaves(gate['failures']),
                  evidence_mismatch=sum(gate['gate_results'][key] != 'PASS' for key in ('RISK_EVIDENCE_MISMATCH', 'REVIEW_EVIDENCE_ELEMENT_MISMATCH')),
                  contract_type=r['report_context']['contract_type_label'],
                  engine_hash_matches=runtime['runtime_sources']['engine']['sha256'] == hashlib.sha256((ROOT/'backend/review_v2/engine.py').read_bytes()).hexdigest(),
                  process_id=runtime['process_id'], cache=runtime.get('cache'), document_hash=runtime.get('document_hash'))
    assert result['gate'] == 'REPORT_READY'
    assert result['raw_blockers'] == result['expanded_blockers'] == result['evidence_mismatch'] == 0
    assert result['engine_hash_matches']
    return r, result


def comparison(baseline, current):
    before, after = read(baseline), read(current)
    changes = {k: [before[k]['status'], after[k]['status']] for k in before.keys() & after.keys() if before[k]['status'] != after[k]['status']}
    result = dict(total=len(after), passed=sum(v['status'] == 'PASS' for v in after.values()),
                  failed=sum(v['status'] == 'FAIL' for v in after.values()), changes=changes,
                  added=sorted(after.keys()-before.keys()), removed=sorted(before.keys()-after.keys()))
    assert not changes and not result['removed']
    return result


def main():
    result = {'current': {}, 'guards': {}, 'files': {}}
    for party in ('licensor', 'licensee'):
        r, summary = upload(OUT/f'current_{party}/report.json')
        assert summary['contract_type'].endswith('技术秘密许可合同')
        items = {i['item_id']: i for i in r['items']}
        summary['rules'] = {key: dict(coverage=items[key]['coverage_status'],
            elements={e['element_id']: e['status'] for e in items[key]['coverage_elements']},
            sources=[e.get('quote') or e.get('text') for e in items[key]['evidence_clauses'] if e.get('source_type') != 'SEARCH_AUDIT'])
            for key in ('TC-07-01', 'TC-07-02', 'TC-11-02', 'TC-11-04', 'TC-12-03')}
        scope = summary['rules']['TC-07-01']['elements']
        assert all(scope[key] == 'COVERED' for key in ('licensed_secret_subject', 'permitted_implementation_acts', 'license_territory', 'license_term', 'license_type'))
        assert summary['rules']['TC-07-02']['elements']['main_license_fee_arrangement'] == 'COVERED'
        assert any('80万元' in q for q in summary['rules']['TC-07-02']['sources'])
        assert not any('改进' in q for q in summary['rules']['TC-07-02']['sources'])
        assert summary['rules']['TC-11-02']['elements']['confidentiality_exceptions'] == 'COVERED'
        assert all(summary['rules']['TC-11-04']['elements'][key] == 'COVERED' for key in ('stop_disclosure', 'stop_use', 'mitigation_obligation', 'incident_notification'))
        assert summary['rules']['TC-12-03']['elements']['future_fee_after_secret_loss'] == 'ADVERSE'
        assert summary['rules']['TC-12-03']['elements']['termination_after_secret_loss'] == 'COVERED'
        assert summary['rules']['TC-12-03']['elements']['technical_secret_consideration'] == 'COVERED'
        assert '未履行服务对应价款' not in items['TC-12-03']['risk_point_description']
        forbidden = ('patent_name', 'patent_number', 'patent_owner', 'patent_authorization_date', 'patent_application_date', 'annual_fee')
        summary['active_patent_exclusive_elements'] = [e['element_id'] for i in r['items'] if i.get('applicability', {}).get('applicable') for e in i['coverage_elements'] if any(key in e['element_id'] for key in forbidden)]
        assert not summary['active_patent_exclusive_elements']
        result['current'][party] = summary
    for path in sorted(ART.glob('round22_accepted_*/report.json')):
        current, summary = upload(path)
        old_name = path.parent.name.replace('round22_accepted_', 'round21_accepted_').replace('prior_secret_', 'current_')
        baseline = json.loads((ART/old_name/'report.json').read_text(encoding='utf-8'))
        old_groups = {f['risk_group'] for f in baseline['risk_findings']}
        groups = {f['risk_group'] for f in current['risk_findings']}
        summary['risk_groups_added'] = sorted(groups-old_groups)
        summary['risk_groups_removed'] = sorted(old_groups-groups)
        assert not summary['risk_groups_added'] and not summary['risk_groups_removed'], (path, summary)
        result['guards'][path.parent.name] = summary
    assert len(result['guards']) == 13
    assert len({r['process_id'] for r in [*result['current'].values(), *result['guards'].values()]}) == 1
    result['full'] = comparison([ART/f'round21_semantics/full64_batch{i}.xml' for i in (0,1)], [OUT/f'full68_batch{i}.xml' for i in (0,1)])
    result['supplemental'] = comparison([ART/'round21_semantics/supplemental_after4.xml'], [OUT/'supplemental.xml'])
    focused = read([OUT/'focused7.xml', OUT/'focused_final.xml'])
    focused_before = {**read([ART/f'round21_semantics/full64_batch{i}.xml' for i in (0,1)]),
                      **read([ART/'round21_semantics/focused8.xml'])}
    focused_changes = {k: [focused_before[k]['status'], focused[k]['status']] for k in focused.keys() & focused_before.keys() if focused_before[k]['status'] != focused[k]['status']}
    result['focused'] = dict(total=len(focused), passed=sum(v['status'] == 'PASS' for v in focused.values()),
                             failed=sum(v['status'] == 'FAIL' for v in focused.values()), changes=focused_changes)
    assert not focused_changes
    for name in ('technology_service_analysis.py', 'license_control_facts.py', 'obligation_detail_elements.py', 'confidentiality_remedies.py', 'technology_fact_ontology.py', 'engine.py'):
        result['files'][name] = hashlib.sha256((ROOT/'backend/review_v2'/name).read_bytes()).hexdigest()
    def functions(path):
        return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(path.read_text(encoding='utf-8-sig')).body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    before = functions(OUT/'baseline_source/engine.py')
    after = functions(ROOT/'backend/review_v2/engine.py')
    result['changed_engine_functions'] = sorted(k for k in before.keys() & after.keys() if before[k] != after[k])
    result['changed_gate_or_verifier_functions'] = [k for k in result['changed_engine_functions'] if 'gate' in k or 'verif' in k or 'audit' in k]
    assert not result['changed_gate_or_verifier_functions']
    (OUT/'acceptance.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(dict(current=len(result['current']), guards=len(result['guards']),
        tests={key: {k: v for k, v in result[key].items() if k in ('total', 'passed', 'failed', 'changes')} for key in ('full', 'focused', 'supplemental')},
        added_tests=len(result['full']['added']), changed_gate_or_verifier_functions=result['changed_gate_or_verifier_functions']), ensure_ascii=False))


if __name__ == '__main__':
    main()
