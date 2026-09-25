"""Audit current cross-article closure against the exact full28 test identities."""
import hashlib
import json
from pathlib import Path
from compare_review_regressions import read

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artifacts/technology_pass_semantics'


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--suite', default='full29')
    args = parser.parse_args()
    paths = sorted(ART.glob(args.suite + '_batch*.xml'))
    if len(paths) != 2:
        raise RuntimeError('Both final-code pytest batches must finish')
    before = read(sorted(ART.glob('full28_batch*.xml')))
    after = read(paths)
    base = load(ART / 'round10_final_summary.json')
    shared = before.keys() & after.keys()
    comparison = dict(
        recovered=sorted(k for k in shared if before[k]['status'] == 'FAIL' and after[k]['status'] == 'PASS'),
        newly_failing=sorted(k for k in shared if before[k]['status'] == 'PASS' and after[k]['status'] != 'PASS'),
        removed=sorted(before.keys() - after.keys()),
        added={k: after[k]['status'] for k in sorted(after.keys() - before.keys())})
    hashes = {name: hashlib.sha256((ROOT / 'backend/review_v2' / name).read_bytes()).hexdigest()
              for name in ('engine.py', 'ancillary_fee_facts.py', 'license_control_facts.py')}
    samples = []
    for name in ('cross_article', 'patent', 'guard', 'consulting', 'provider', 'balanced', 'ancillary'):
        prefix = 'round11_verified' if name == 'cross_article' else 'round11_final'
        path = ART / f'{prefix}_{name}_live/report.json'
        report = load(path)
        prior = load(ART / f'round10_final_{name}_live/report.json')
        runtime = report['production_path_trace']
        actual_hash = runtime['runtime_sources']['engine']['sha256']
        gate = report['release_quality_gate']
        samples.append(dict(sample=name, report=str(path), gate=gate['status'],
            raw_blockers=len(gate['failures']), failures=gate['failures'],
            process_id=runtime['process_id'], engine_hash=actual_hash,
            current_code=actual_hash == hashes['engine.py'],
            removed_risk_groups=sorted({f['risk_group'] for f in prior['risk_findings']} -
                                       {f['risk_group'] for f in report['risk_findings']})))
    baseline_blockers = load(ART / 'round9_final_cross_article_blockers.json')
    fresh_blockers = load(ART / 'round11_before_cross_article_blockers.json')
    causes = [
        dict(raw_index=1, code='REVIEW_EVIDENCE_ELEMENT_MISMATCH', rule_id='TC-09-02',
             element_id='PRIMARY_EVIDENCE', first_wrong_stage='SPECIALIZED_ACCEPTANCE_CANDIDATE',
             cause='Product-performance clauses were used as ancillary-service acceptance evidence without an object-domain relation.'),
        dict(raw_index=2, code='MISSING_WITH_POSITIVE_EVIDENCE', rule_id='TC-09-02', element_id=None,
             first_wrong_stage='SPECIALIZED_ACCEPTANCE_CANDIDATE',
             cause='An early missing decision and a later product-metric COVERED candidate diverged. Service-domain atoms now determine both evidence and coverage; actual service acceptance gaps remain.'),
        dict(raw_index=3, code='CROSS_RULE_CANONICAL_FACT_CONSISTENCY', rule_id=None, element_id=None,
             first_wrong_stage='FEE_ATOMIC_PREDICATE / SPECIALIZED_SCOPE_TO_CANONICAL',
             cause='Coordinated service-fee names and explicit component/total relations were not adapted; licence scope retained untyped, overly broad source candidates that exact verification rejected.'),
        dict(raw_index=4, code='NARRATIVE_EVIDENCE_GATE', rule_id='TC-11-02', element_id='confidentiality_period',
             first_wrong_stage='SPECIALIZED_FIELD_SOURCE_PROJECTION',
             cause='A synthesized label/value plus repeated sentence was not a verbatim source. Existing typed confidentiality facts now supply separate exact spans and actor provenance.'),
        dict(raw_index=5, code='POSITIVE_FACT_MONOTONICITY', rule_id='TC-09-02', element_id='objective_acceptance_standard',
             first_wrong_stage='SPECIALIZED_ACCEPTANCE_CANDIDATE', duplicate_root_of=1),
        dict(raw_index=6, code='NARRATIVE_EVIDENCE_GATE', rule_id='TC-11-02', element_id='confidentiality_period',
             duplicate_root_of=4),
        dict(raw_index=7, code='EXACT_ELEMENT_REPORT_INVARIANT', rule_id='TC-11-04', element_id=None,
             cause='Three consequence/unresolved-rendering refusals already absent in the freshly reproduced 904/251 baseline; preserved, not counted as this-round restoration.')]
    result = dict(baseline={'PASS': 904, 'FAIL': 251},
        counts={s: sum(v['status'] == s for v in after.values()) for s in ('PASS', 'FAIL', 'SKIP')},
        comparison=comparison, business_hashes=hashes, test_migrations=0,
        old_baseline_raw=baseline_blockers['raw_failure_count'], old_baseline_expanded=baseline_blockers['blocker_tuple_count'],
        fresh_raw=fresh_blockers['raw_failure_count'], fresh_expanded=fresh_blockers['blocker_tuple_count'],
        raw_blocker_causes=causes, samples=samples,
        protections={group: {k: after[k]['status'] if k in after else 'NOT_RUN' for k in values}
                     for group, values in base['protections'].items()})
    (ART / 'round11_final_summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps(dict(counts=result['counts'], recovered=comparison['recovered'],
        newly_failing=comparison['newly_failing'], added=len(comparison['added']),
        samples=[(s['sample'], s['gate'], s['raw_blockers'], s['current_code']) for s in samples]), ensure_ascii=False))


if __name__ == '__main__':
    main()
