"""Final regression comparison and current-contract positive/absence audit."""
import hashlib
import json
from pathlib import Path
from compare_review_regressions import read

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artifacts/technology_pass_semantics'


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    before = read(sorted(ART.glob('full29_batch*.xml')))
    paths = sorted(ART.glob('full30_batch*.xml'))
    assert len(paths) == 2, 'Final full suite is incomplete'
    after = read(paths)
    shared = before.keys() & after.keys()
    manifest = load(ART / 'round12_verified_live_manifest.json')
    report = load(ART / 'round12_verified_cooperative_live/report.json')
    original = load(ART / 'round12_before_cooperative_live/report.json')
    current_hash = hashlib.sha256((ROOT / 'backend/review_v2/engine.py').read_bytes()).hexdigest()
    samples = []
    for sample in manifest:
        if sample.get('status') == 'NOT_VERIFIED':
            samples.append(sample)
            continue
        r = load(Path(sample['report']))
        samples.append(dict(sample=sample['sample'], gate=r['release_quality_gate'],
            current_code=r['production_path_trace']['runtime_sources']['engine']['sha256'] == current_hash,
            process_id=r['production_path_trace']['process_id']))
    def selected(r):
        return {i['item_id']: i for i in r['items']}
    before_items, after_items = selected(original), selected(report)
    changes = []
    for rid, key in [('TC-11-02', 'confidentiality_period'), ('TC-05-04', 'development_delay_liability')]:
        old = next(e for e in before_items[rid]['coverage_elements'] if e['element_id'] == key)
        new = next(e for e in after_items[rid]['coverage_elements'] if e['element_id'] == key)
        changes.append(dict(rule_id=rid, element_id=key, before=old, after=new))
    audit = [dict(rule_id=i['item_id'], coverage=i['coverage_status'], elements=i['coverage_elements'],
                  evidence=i['evidence_clauses']) for i in report['items']
             if i['coverage_status'] in {'部分覆盖', '缺失'}]
    # These are unresolved diagnostic findings, not patched report decisions.
    remaining = [
        dict(rule_id='TC-05-01', elements=['development_schedule_and_milestones', 'funding_investment'],
             source_articles=['第三条', '第四条'], first_wrong_stage='COOPERATIVE_LOCAL_RECALL_AND_PROJECTION',
             reason='Stage dates and each party\'s contributions are present, but subtype-local labels discard them.'),
        dict(rule_id='TC-05-03', elements=['authorized_internal_users', 'independent_use_right', 'external_license_transfer_disclosure'],
             source_articles=['第六条'], first_wrong_stage='COOPERATIVE_DEFAULT_BRANCH',
             reason='Explicit internal-use permission and disposition consent must not become unconditional MISSING; complete transfer/sublicensing coverage still requires independent checking.'),
        dict(rule_id='TC-05-04', elements=['exit_research_material_handover'], source_articles=['第十四条'],
             first_wrong_stage='EXIT_OBJECT_MAPPING',
             reason='Project-data/material handover exists, but does not by itself prove source-code, sample or complete research-material handover.'),
        dict(rule_id='TC-11-01', elements=['confidential_use_restriction'], source_articles=['第五条', '第十条'],
             first_wrong_stage='COOPERATIVE_CONFIDENTIALITY_USE_MAPPING',
             reason='Project-data use is restricted; this is not complete coverage for every type of confidential information.'),
        dict(rule_id='TC-12-02', elements=['component_selection_control'], source_articles=['第七条'],
             first_wrong_stage='COMPONENT_CANDIDATE_TO_FINAL_COVERAGE',
             reason='A partial component arrangement survives in elements while the whole rule is MISSING. Platform-disruption remedies must not prove infringement-claim remedies.'),
        dict(rule_id='TC-13-01', elements=['deployment_and_operation_documentation'], source_articles=['第五条'],
             first_wrong_stage='COOPERATIVE_DOCUMENT_ALIAS_MAPPING',
             reason='Deployment instructions exist; operating documentation is a separate necessary component.'),
    ]
    result = dict(baseline={'PASS': 918, 'FAIL': 250}, engine_hash=current_hash,
        counts={s: sum(v['status'] == s for v in after.values()) for s in ('PASS', 'FAIL', 'SKIP')},
        recovered=sorted(k for k in shared if before[k]['status'] == 'FAIL' and after[k]['status'] == 'PASS'),
        newly_failing=sorted(k for k in shared if before[k]['status'] == 'PASS' and after[k]['status'] != 'PASS'),
        removed=sorted(before.keys()-after.keys()),
        added={k: after[k]['status'] for k in sorted(after.keys()-before.keys())},
        migrations=0, samples=samples, target_changes=changes,
        initial_raw_blockers=len(original['release_quality_gate']['failures']),
        final_raw_blockers=len(report['release_quality_gate']['failures']),
        remaining_confirmed_mapping_gaps=remaining, full_partial_missing_scan=audit,
        fixture_change=dict(path='test_data/122 测试2.docx',
            previous_sha256='e5463c90d88b68b07544d560894b0d0487b67aa4e163bb96e817c50206283ef5',
            current_sha256=hashlib.sha256((ROOT/'test_data/122 测试2.docx').read_bytes()).hexdigest(),
            affected_module='backend.tests.test_technology_exact_truth_pipeline',
            before_current_input=dict(
                engine_hash=original['production_path_trace']['runtime_sources']['engine']['sha256'],
                confidentiality_coverage=before_items['TC-11-02']['coverage_status'],
                gate=original['release_quality_gate']['status'],
                exit_findings=sum('TC-05-04' in f['source_review_ids'] for f in original['risk_findings'])),
            after_current_input=dict(
                confidentiality_coverage=after_items['TC-11-02']['coverage_status'],
                gate=report['release_quality_gate']['status'],
                exit_findings=sum('TC-05-04' in f['source_review_ids'] for f in report['risk_findings'])),
            note='Original entrusted source was replaced before this turn; no original test expectations were edited.'))
    (ART/'round12_final_summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps({k: result[k] for k in ['counts','recovered','newly_failing','removed','added','final_raw_blockers']}, ensure_ascii=False))
    print([(r['sample'], r.get('status') or r['gate']['status'], r.get('current_code')) for r in samples])


if __name__ == '__main__':
    main()
