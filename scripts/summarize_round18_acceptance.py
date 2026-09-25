"""Summarize final-code uploads and completed JUnit runs without hiding failures."""
import hashlib
import json
from pathlib import Path
from compare_review_regressions import read

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artifacts/technology_pass_semantics'


def report(name):
    return json.loads((ART / name / 'report.json').read_text(encoding='utf-8-sig'))


def main():
    current = report('round18_final6')
    items = {i['item_id']: i for i in current['items']}
    checks = {}
    for rule in ('TC-03-04', 'TC-13-02'):
        elements = {e['element_id']: e for e in items[rule]['coverage_elements']}
        date = elements['technology_patent_authorization_date']
        rights = elements['license_encumbrance_and_conflict_disclosure']
        checks[rule] = {
            'coverage': items[rule]['coverage_status'],
            'authorization_date': date['status'],
            'date_sources': date['source_spans'],
            'disclosure_sources': rights['source_spans'],
            'remaining_search_targets': rights['search_targets'],
        }
        assert date['status'] == 'COVERED'
        assert '既有许可披露' not in rights['search_targets']
        assert any('普通实施许可' in s for s in rights['source_spans'])
    for rule, forbidden in (('TC-11-01', '授予分许可'), ('TC-13-01', '第三方权利主张')):
        rows = items[rule]['evidence_clauses']
        direct = [e for e in rows if e.get('source_type') != 'SEARCH_AUDIT']
        assert all(forbidden not in (e.get('quote') or e.get('quoted_text') or '') for e in direct)
        assert all(e.get('element_ids') or e.get('supporting_element_ids') for e in direct)
        checks[rule] = {'coverage': items[rule]['coverage_status'], 'direct_evidence': direct}
    engine_hash = hashlib.sha256((ROOT / 'backend/review_v2/engine.py').read_bytes()).hexdigest()
    guards = {}
    for name in ('cooperative_live', 'cross_article_live', 'patent_live', 'consulting_live',
                 'provider_live', 'balanced_live', 'ancillary_live', 'entrusted', 'prior_patent', 'transfer'):
        r = report('round18_final6_' + name)
        old = report('round17_final4_' + name)
        added = sorted({f['risk_group'] for f in r['risk_findings']} - {f['risk_group'] for f in old['risk_findings']})
        removed = sorted({f['risk_group'] for f in old['risk_findings']} - {f['risk_group'] for f in r['risk_findings']})
        guards[name] = {'gate': r['release_quality_gate']['status'], 'risk_groups_added': added,
                        'risk_groups_removed': removed,
                        'engine_hash_matches': r['production_path_trace']['runtime_sources']['engine']['sha256'] == engine_hash}
        assert guards[name]['gate'] == 'REPORT_READY' and not removed
        assert guards[name]['engine_hash_matches']
    before = read([ART / f'full48_batch{i}.xml' for i in (0, 1)])
    after = read([ART / f'full54_batch{i}.xml' for i in (0, 1)])
    newly_failing = [k for k in before.keys() & after.keys() if before[k]['status'] == 'PASS' and after[k]['status'] == 'FAIL']
    recovered = [k for k in before.keys() & after.keys() if before[k]['status'] == 'FAIL' and after[k]['status'] == 'PASS']
    result = {'gate': current['release_quality_gate'], 'checks': checks, 'guards': guards,
              'engine_sha256': engine_hash,
              'pass': sum(v['status'] == 'PASS' for v in after.values()),
              'fail': sum(v['status'] == 'FAIL' for v in after.values()),
              'newly_failing': sorted(newly_failing), 'recovered': sorted(recovered),
              'added_tests': sorted(after.keys() - before.keys()),
              'removed_tests': sorted(before.keys() - after.keys()),
              'test_migrations': 0,
              'unavailable_original_entrusted_sha256': 'e5463c90d88b68b07544d560894b0d0487b67aa4e163bb96e817c50206283ef5',
              'unavailable_original_status': 'NOT_VERIFIED'}
    (ART / 'round18_final_acceptance.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('checks', 'guards', 'gate', 'added_tests')}, ensure_ascii=False))
    assert current['release_quality_gate']['status'] == 'REPORT_READY'
    assert not newly_failing and not result['removed_tests']


if __name__ == '__main__':
    main()
