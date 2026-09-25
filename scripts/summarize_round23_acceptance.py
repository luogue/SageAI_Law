"""Verify the two boundary mappings against real uploads and unchanged baselines."""
import ast
import json
from pathlib import Path
from compare_review_regressions import read
from summarize_round22_acceptance import upload, comparison

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artifacts/technology_pass_semantics'
OUT = ART / 'round23_boundaries'
KEYS = ('licensed_secret_subject', 'permitted_implementation_acts', 'license_territory',
        'license_term', 'license_type', 'transfer_or_sublicense_boundary', 'post_termination_use_boundary')


def main():
    result = {'current': {}, 'guards': {}}
    for party in ('licensor', 'licensee'):
        report, summary = upload(OUT / f'current_{party}/report.json')
        assert summary['contract_type'].endswith('技术秘密许可合同')
        item = next(i for i in report['items'] if i['item_id'] == 'TC-07-01')
        atoms = {e['element_id']: e for e in item['coverage_elements']}
        assert all(atoms[k]['status'] == 'COVERED' and atoms[k]['evidence_ids'] for k in KEYS)
        summary['elements'] = {k: atoms[k]['status'] for k in KEYS}
        summary['boundary_sources'] = {k: atoms[k]['supporting_evidence'] for k in KEYS[-2:]}
        baseline_report = json.loads((ART / f'round22_routing/current_{party}/report.json').read_text(encoding='utf-8'))
        previous = {i['item_id']: {e['element_id']: e['status'] for e in i['coverage_elements']} for i in baseline_report['items']}
        changes = []
        for current_item in report['items']:
            for e in current_item['coverage_elements']:
                old_status = previous[current_item['item_id']].get(e['element_id'])
                if old_status != e['status']:
                    changes.append([current_item['item_id'], e['element_id'], old_status, e['status']])
        assert sorted(changes) == sorted([['TC-07-01', k, 'UNCERTAIN', 'COVERED'] for k in KEYS[-2:]])
        summary['element_status_changes'] = changes
        result['current'][party] = summary
    for path in sorted(ART.glob('round23_accepted_*/report.json')):
        report, summary = upload(path)
        old = ART / path.parent.name.replace('round23_', 'round22_') / 'report.json'
        baseline = json.loads(old.read_text(encoding='utf-8'))
        before = {f['risk_group'] for f in baseline['risk_findings']}
        after = {f['risk_group'] for f in report['risk_findings']}
        summary['risk_groups_added'] = sorted(after - before)
        summary['risk_groups_removed'] = sorted(before - after)
        assert before == after, (path, summary)
        result['guards'][path.parent.name] = summary
    assert len(result['guards']) == 13
    assert len({s['process_id'] for s in [*result['current'].values(), *result['guards'].values()]}) == 1
    baseline = [ART / f'round22_routing/full68_batch{i}.xml' for i in (0, 1)]
    result['full'] = comparison(baseline, [OUT / f'full69_batch{i}.xml' for i in (0, 1)])
    focused, before = read([OUT / 'focused.xml']), read(baseline)
    result['focused'] = dict(total=len(focused), passed=sum(v['status'] == 'PASS' for v in focused.values()),
                             failed=sum(v['status'] == 'FAIL' for v in focused.values()),
                             changed=[k for k in focused.keys() & before.keys() if focused[k]['status'] != before[k]['status']])
    assert not result['focused']['failed'] and not result['focused']['changed']
    def functions(path):
        return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(path.read_text(encoding='utf-8-sig')).body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    old = functions(OUT / 'baseline_source/engine.py')
    new = functions(ROOT / 'backend/review_v2/engine.py')
    result['changed_engine_functions'] = [k for k in old.keys() & new.keys() if old[k] != new[k]]
    result['changed_gate_verifier_audit_functions'] = [k for k in result['changed_engine_functions'] if any(x in k for x in ('gate', 'verif', 'audit'))]
    assert not result['changed_gate_verifier_audit_functions']
    (OUT / 'acceptance.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('focused', 'changed_engine_functions', 'changed_gate_verifier_audit_functions')}, ensure_ascii=False))
    print('Current 2; protection 13; full', result['full']['total'], result['full']['passed'], result['full']['failed'], 'added', len(result['full']['added']))


if __name__ == '__main__':
    main()
