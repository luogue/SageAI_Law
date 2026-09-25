"""Compare original upload blockers and complete per-test identities, without altering gates."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from compare_review_regressions import read

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artifacts/technology_pass_semantics'


def load(path):
    return json.loads(path.read_text(encoding='utf8'))


def blocker_identity(blocker):
    # Preserve the actual nullable IDs and source records, not just counts.
    fields = {k: blocker.get(k) for k in (
        'error_code', 'rule_id', 'element_id', 'fact_id', 'reject_reason')}
    # Evidence packages are unordered sets; keep every source, but compare
    # membership rather than incidental hash/set traversal order.
    fields['source_spans'] = sorted(blocker.get('source_spans', []),
                                   key=lambda s: json.dumps(s, ensure_ascii=False, sort_keys=True))
    fields['gate_reasons'] = blocker.get('gate_tuple', {}).get('reasons')
    return json.dumps(fields, ensure_ascii=False, sort_keys=True)


def main():
    baseline = read(sorted(ART.glob('full25_batch*.xml')))
    current_paths = sorted(ART.glob('full26_batch*.xml'))
    if len(current_paths) != 6:
        raise RuntimeError('Complete final regression results are required')
    current = read(current_paths)
    old_summary = load(ART / 'round8_close_final_summary.json')
    comparisons = {
        'recovered': sorted(k for k in baseline.keys() & current.keys()
                            if baseline[k]['status'] == 'FAIL' and current[k]['status'] == 'PASS'),
        'newly_failing': sorted(k for k in baseline.keys() & current.keys()
                                if baseline[k]['status'] == 'PASS' and current[k]['status'] == 'FAIL'),
        'removed': sorted(baseline.keys() - current.keys()),
        'added': {k: current[k]['status'] for k in sorted(current.keys() - baseline.keys())},
    }
    protections = {group: {k: current[k]['status'] if k in current else 'NOT_RUN'
                           for k in old_summary[group]}
                   for group in ('remaining_five', 'protected_twenty_one', 'prior_eight',
                                 'prior_twenty_two', 'prior_sixteen')}
    samples = []
    for run in load(ART / 'round9_final_live_manifest.json'):
        name = run['sample']
        if not run.get('report'):
            samples.append({'sample': name, 'gate': 'NOT_VERIFIED'})
            continue
        report = load(Path(run['report']))
        before = load(ART / f'round8_accept_{name}_live/report.json')
        path = ART / f'round9_final_{name}_blockers.json'
        subprocess.run([sys.executable, '-X', 'utf8',
                        str(ROOT / 'scripts/export_routing_gate_blockers.py'),
                        run['report'], str(path)], check=True, stdout=subprocess.DEVNULL)
        old_blocks = load(ART / f'round8_accept_{name}_blockers.json')
        blocks = load(path)
        old_map = {blocker_identity(b): b for b in old_blocks['blockers']}
        new_map = {blocker_identity(b): b for b in blocks['blockers']}
        runtime = report['production_path_trace']
        old_groups = {f['risk_group'] for f in before['risk_findings']}
        new_groups = {f['risk_group'] for f in report['risk_findings']}
        items = {i['item_id']: i for i in report['items']}
        samples.append({
            'sample': name, 'gate': report['release_quality_gate']['status'],
            'raw_blockers_before': old_blocks['raw_failure_count'],
            'expanded_blockers_before': old_blocks['blocker_tuple_count'],
            'raw_blockers': blocks['raw_failure_count'],
            'expanded_blockers': blocks['blocker_tuple_count'],
            'remaining_blockers': blocks['blockers'],
            'added_blockers': [new_map[k] for k in sorted(new_map.keys() - old_map.keys())],
            'removed_blockers': [old_map[k] for k in sorted(old_map.keys() - new_map.keys())],
            'evidence_order_only_changes': [{k: new_map[key].get(k) for k in
                ('error_code', 'rule_id', 'element_id', 'fact_id')} for key in new_map.keys() & old_map.keys()
                if new_map[key]['source_spans'] != old_map[key]['source_spans']],
            'risk_groups_removed': sorted(old_groups - new_groups),
            'risk_groups_added': sorted(new_groups - old_groups),
            'process_id': runtime['process_id'],
            'runtime_engine_hash': runtime['runtime_sources']['engine']['sha256'],
            'engine_hash_matches': runtime['runtime_sources']['engine']['sha256'] ==
                hashlib.sha256((ROOT / 'backend/review_v2/engine.py').read_bytes()).hexdigest(),
            'runtime_drift': runtime['runtime_source_drift']['status'],
            'entrypoint': runtime['entrypoint'], 'run_mode': runtime['run_mode'],
            'target_elements': items['TC-07-01']['coverage_elements'] if name == 'balanced' else None,
            'confidentiality_coverage': items['TC-11-02']['coverage_status'] if name == 'balanced' else None,
            'gate_checks': report['release_quality_gate']['gate_results'],
        })
    result = {
        'counts': {s: sum(r['status'] == s for r in current.values()) for s in ('PASS', 'FAIL', 'SKIP')},
        'comparisons': comparisons, 'protections': protections, 'test_migrations': [],
        'samples': samples,
        'root_cause': {
            'rule_id': 'TC-07-01', 'element_id': 'license_term', 'fact_id': None,
            'error_code': 'EXACT_ELEMENT_REPORT_INVARIANT',
            'reject_reason': 'FINAL_MISSING_WITHOUT_ELEMENT_ABSENCE_SEARCH',
            'first_wrong_stage': '_apply_technology_transaction_evidence_consistency -> _set_multi_element_state',
            'detected_stage': 'Final Evidence Projection',
            'source_clause_id': 'C0005',
            'source_span': '第三条 许可期限五年，许可地域为中国境内，仅限生产合同产品。',
            'cause': 'Rule-local Arabic-year-only grammar rejected a valid Chinese-number licence duration; full search found it and correctly refused a false absence audit.',
            'same_as_restored_confidentiality_test': False,
            'test_gap': 'Original directional confidentiality assertions cover TC-11-02, not TC-07-01 or whole-report release.',
        },
    }
    (ART / 'round9_final_summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps({
        'counts': result['counts'],
        'comparisons': {k: len(v) for k, v in comparisons.items()},
        'protections': {g: {s: list(v.values()).count(s) for s in set(v.values())} for g, v in protections.items()},
        'samples': [{k: r.get(k) for k in ('sample', 'gate', 'raw_blockers', 'expanded_blockers',
                    'engine_hash_matches', 'risk_groups_removed')} for r in samples],
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
