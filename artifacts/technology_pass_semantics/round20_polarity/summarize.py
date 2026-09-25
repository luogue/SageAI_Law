"""Reproducible acceptance summary; never waives release or test failures."""
import hashlib
import json
from pathlib import Path

ROOT = Path('F:/ai/Sage')
ART = ROOT / 'artifacts/technology_pass_semantics'
OUT = ART / 'round20_polarity'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def summarize(report):
    assert report['production_path_trace']['runtime_sources']['engine']['sha256'] == hashlib.sha256(
        (ROOT / 'backend/review_v2/engine.py').read_bytes()).hexdigest(), 'Stale backend engine'
    gate = report['release_quality_gate']
    failures = gate['failures']
    checks = {k: v for k, v in gate['gate_results'].items() if 'EVIDENCE' in k and 'MISMATCH' in k}
    return dict(gate=gate['status'], raw_blockers=len(failures),
                expanded_blockers=sum(len(f.get('details') or [f]) for f in failures),
                evidence_mismatch_checks=checks,
                evidence_mismatch_count=sum(v == 'FAIL' for v in checks.values()),
                failures=failures, process_id=report['production_path_trace']['process_id'])


def main():
    frozen = read(OUT / 'manifest.json')
    assert all(hashlib.sha256((ROOT / row['path']).read_bytes()).hexdigest() == row['sha256']
               for row in frozen['sources']), 'Source changed after test freeze'
    result = dict(source_manifest='manifest.json', current_contract={}, protections={})
    for party in ('licensee', 'licensor'):
        report = read(ART / f'round20_complete_current_{party}/report.json')
        row = summarize(report)
        selected = {i['item_id']: i for i in report['items'] if i['item_id'] in {'TC-02-02', 'TC-12-01', 'TC-12-02', 'TC-11-04'}}
        row['review_states'] = {key: value['coverage_status'] for key, value in selected.items()}
        row['tc0202_audit'] = selected['TC-02-02']['decision_trace']['negative_clause_check']
        row['tc0202_elements'] = selected['TC-02-02']['coverage_elements']
        row['tc1202_elements'] = selected['TC-12-02']['coverage_elements']
        for key in ('litigation_handling', 'attorney_fee', 'litigation_cost'):
            assert next(e for e in row['tc1202_elements'] if e['element_id'] == key)['status'] == 'MISSING', key
        assert selected['TC-02-02']['coverage_status'] == '通过'
        assert not row['tc0202_audit']['adverse_clause_exists']
        assert not any(e['status'] == 'ADVERSE' for e in row['tc0202_elements'])
        assert not any(f['risk_group'] == selected['TC-02-02']['risk_group'] for f in report['risk_findings'])
        assert row['gate'] == 'REPORT_READY' and row['expanded_blockers'] == row['evidence_mismatch_count'] == 0
        result['current_contract'][party] = row
    names = ['patent_closed', 'cooperative_live', 'cross_article_live', 'patent_live',
             'consulting_live', 'provider_live', 'balanced_live', 'ancillary_live',
             'entrusted', 'prior_patent', 'transfer']
    for name in names:
        report = read(ART / f'round20_complete_{name}/report.json')
        before = read(ART / ('round18_final6' if name == 'patent_closed' else f'round18_final6_{name}') / 'report.json')
        row = summarize(report)
        old = {f['risk_group'] for f in before['risk_findings']}
        new = {f['risk_group'] for f in report['risk_findings']}
        row.update(risk_groups_added=sorted(new-old), risk_groups_removed=sorted(old-new))
        assert row['gate'] == 'REPORT_READY' and not row['failures']
        assert not row['risk_groups_added'] and not row['risk_groups_removed'], name
        result['protections'][name] = row
    comparison = OUT / 'full61_comparison.json'
    if comparison.exists():
        result['full_regression'] = read(comparison)
        assert not result['full_regression']['newly_failing']
        assert not result['full_regression']['removed']
        assert all(r['status'] == 'PASS' for r in result['full_regression']['added'].values())
    (OUT / 'acceptance.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps({k: {n: {f: r[f] for f in ('gate', 'raw_blockers', 'expanded_blockers', 'evidence_mismatch_count')}
                          for n, r in result[k].items()} for k in ('current_contract', 'protections')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
