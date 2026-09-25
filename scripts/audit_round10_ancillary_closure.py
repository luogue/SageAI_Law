"""Reconcile the final upload version, raw refusals and original test identities."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from compare_review_regressions import read
from audit_round9_release_closure import blocker_identity

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artifacts/technology_pass_semantics'


def load(path):
    return json.loads(path.read_text(encoding='utf8'))


def main():
    paths = sorted(ART.glob('full28_batch*.xml'))
    if len(paths) != 6:
        raise RuntimeError('Full final-code suite has not completed')
    before = read(sorted(ART.glob('full26_batch*.xml')))
    after = read(paths)
    baseline = load(ART / 'round9_final_summary.json')
    engine_hash = hashlib.sha256((ROOT / 'backend/review_v2/engine.py').read_bytes()).hexdigest()
    common = before.keys() & after.keys()
    comparison = {
        'recovered': sorted(k for k in common if before[k]['status'] == 'FAIL' and after[k]['status'] == 'PASS'),
        'newly_failing': sorted(k for k in common if before[k]['status'] == 'PASS' and after[k]['status'] == 'FAIL'),
        'removed': sorted(before.keys() - after.keys()),
        'added': {k: after[k]['status'] for k in sorted(after.keys() - before.keys())},
    }
    runs = load(ART / 'round10_final_live_manifest.json')
    if len(runs) != 9:
        raise RuntimeError('Original upload matrix has not completed')
    samples = []
    for run in runs:
        name = run['sample']
        if not run.get('report'):
            samples.append({'sample': name, 'gate': 'NOT_VERIFIED'})
            continue
        report = load(Path(run['report']))
        old_report = load(ART / f'round9_final_{name}_live/report.json')
        exported = ART / f'round10_final_{name}_blockers.json'
        subprocess.run([sys.executable, '-X', 'utf8',
            str(ROOT / 'scripts/export_routing_gate_blockers.py'), run['report'], str(exported)],
            check=True, stdout=subprocess.DEVNULL)
        current = load(exported)
        previous = load(ART / f'round9_final_{name}_blockers.json')
        previous_set = {blocker_identity(b) for b in previous['blockers']}
        current_set = {blocker_identity(b) for b in current['blockers']}
        runtime = report['production_path_trace']
        runtime_engine = next(value for value in runtime['runtime_sources'].values()
                              if value.get('file', '').replace('\\', '/').endswith('/review_v2/engine.py'))
        groups = {f['risk_group'] for f in report['risk_findings']}
        old_groups = {f['risk_group'] for f in old_report['risk_findings']}
        samples.append({
            'sample': name, 'gate': current['status'],
            'raw_before': previous['raw_failure_count'], 'raw_after': current['raw_failure_count'],
            'expanded_before': previous['blocker_tuple_count'], 'expanded_after': current['blocker_tuple_count'],
            'closed_tuples': [json.loads(b) for b in sorted(previous_set - current_set)],
            'new_tuples': [json.loads(b) for b in sorted(current_set - previous_set)],
            'runtime_process_id': runtime['process_id'],
            'engine_sha256': runtime_engine['sha256'],
            'runtime_matches_final_code': runtime_engine['sha256'] == engine_hash,
            'removed_risk_groups': sorted(old_groups - groups),
            'added_risk_groups': sorted(groups - old_groups),
            'report': run['report'],
        })
    result = {
        'baseline': {'PASS': 893, 'FAIL': 252},
        'counts': {s: sum(row['status'] == s for row in after.values()) for s in ('PASS', 'FAIL', 'SKIP')},
        'comparison': comparison, 'test_migrations': 0,
        'business_modules': {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in ('backend/review_v2/engine.py', 'backend/review_v2/confidentiality_remedies.py')},
        'protections': {group: {k: after[k]['status'] if k in after else 'NOT_RUN' for k in values}
                        for group, values in baseline['protections'].items()},
        'samples': samples,
        'raw_blocker_causes': [
            {'raw_index': 1, 'code': 'REVIEW_EVIDENCE_ELEMENT_MISMATCH', 'rule_id': 'TC-06-02',
             'element_id': 'core_contract_arrangement', 'fact_id': None,
             'first_wrong_stage': 'EXACT_SOURCE_VERIFIER accepted evidence projection',
             'cause': 'Verified evidence IDs were replaced while source clause/span arrays retained the old paragraph snapshot.'},
            {'raw_index': 2, 'code': 'NARRATIVE_EVIDENCE_GATE',
             'first_wrong_stage': 'SPECIALIZED_CANDIDATE_TO_REPORT_ELEMENT',
             'cause': 'Exact risk source segments and selected penalty obligations did not populate Review bindings; typed calculation derivation inputs lost element/review ownership in final bundles.'},
            {'raw_index': 3, 'code': 'NARRATIVE_EVIDENCE_GATE', 'duplicate_of_raw_index': 2,
             'cause': 'The same 11 narrative refusal tuples were also emitted by the final narrative audit.'},
            {'raw_index': 4, 'code': 'EXACT_ELEMENT_REPORT_INVARIANT', 'rule_id': 'TC-11-04',
             'first_wrong_stage': 'confidentiality_remedy_elements event-context extraction',
             'cause': 'A confidentiality sentence promoted an entire mixed liability article to confidentiality context. General liability of the other party was incorrectly covered; the residual party requirements and consequence projection also diverged.'},
        ],
    }
    output = ART / 'round10_final_summary.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps({'counts': result['counts'],
        'recovered': len(comparison['recovered']), 'newly_failing': len(comparison['newly_failing']),
        'added': len(comparison['added']),
        'samples': [(s['sample'], s['gate'], s.get('raw_after'), s.get('runtime_matches_final_code')) for s in samples]}, ensure_ascii=False))


if __name__ == '__main__':
    main()
