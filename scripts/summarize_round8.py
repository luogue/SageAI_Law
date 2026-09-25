"""Round8 adjudication, with original IDs and independent migration accounting."""
import json
import hashlib
import argparse
from pathlib import Path
from compare_review_regressions import read

ART = Path(__file__).resolve().parents[1] / 'artifacts/technology_pass_semantics'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-prefix', default='full19')
    args = parser.parse_args()
    r7 = json.loads((ART / 'round7_comparison_final.json').read_text(encoding='utf8'))
    r6 = read(sorted(ART.glob('full12_batch*.xml')))
    before = read(sorted(ART.glob('full16_batch*.xml')))
    current_files = sorted(ART.glob(args.run_prefix + '_batch*.xml'))
    if len(current_files) != 6:
        raise RuntimeError('Full run incomplete; do not publish partial counts')
    after = read(current_files)
    captured = {}
    for path in ART.joinpath('round8_original_outputs').glob('*.json'):
        obj = json.loads(path.read_text(encoding='utf8'))
        node = obj['test_id'].replace('/', '.').replace('.py::', '::')
        if node not in captured or path.stat().st_mtime > captured[node][0].stat().st_mtime:
            captured[node] = path, obj
    adjudication = []
    for key in r7['newly_failing']:
        name = key.split('::', 1)[1]
        kind, root, first = 'IMPLEMENTATION', '', ''
        migration = False
        if name.startswith(('test_tc_12_04_requires_same_loss', 'test_d_party_interest_check')):
            kind, root, first = 'TEST_CONTRACT', 'Same-loss qualifier order; applicability semantics unchanged', 'ASSERTION'
            migration = True
        elif name.startswith('test_negative_rule_requires_reproduced_complete'):
            kind, root, first = 'TEST_CONTRACT', 'Test omitted negative-search predicate producer required by production contract', 'TEST_AUDIT_CONSTRUCTION'
            migration = True
        elif 'consulting' in key:
            root, first = 'Specialized consulting candidates lacked predicate-bearing atomic adapter', 'SPECIALIZED_CANDIDATE_TO_CANONICAL'
            if 'signing_law' in name:
                root, first = 'Selected legal basis early return discarded independently resolved signing context', 'LEGAL_BASIS_DISPLAY'
            elif 'complete_data' in name:
                root, first = 'Inline article location equalled text and operative source was filtered as heading', 'OPERATIVE_CORPUS_FILTER'
        elif 'identity' in name:
            root, first = 'Second abbreviated identity matcher dropped valid resolver fields and source spans', 'EXACT_SOURCE_VERIFIER_IDENTITY_ADAPTER'
        elif 'theme_recommendation_economics' in key:
            root, first = 'clause_id shadowed exact evidence_id in recommendation metadata lookup', 'RECOMMENDATION_EVIDENCE_LOOKUP'
        elif 'patent_application_transfer_consistency' in key:
            root, first = 'Application-stage facts published status/source lists without predicate adapter', 'SPECIALIZED_CANDIDATE_TO_CANONICAL'
            if 'completed_core' in name:
                root, first = 'Explicit mutual undertaking treated as unidentified actor group', 'CONFIDENTIALITY_ACTOR_NORMALIZATION'
        elif 'latest_secret_license_compliant_use' in name:
            root, first = 'Reparsed filtered corpus changed clause IDs for the same claim-response quote', 'CLAIM_RESPONSE_SOURCE_PROJECTION'
        elif 'ancillary_service_fee_keeps' in name:
            kind = 'UNRESOLVED'
            root, first = 'Base-price inclusion inference and missing typed fee-source contract require separate verification', 'ANCILLARY_FEE_PROJECTION'
        elif 'service_fee_and_confidentiality_use_only' in name:
            root, first = 'Late confidentiality producer lacked core adapter; named duty object not recognized as scope', 'SPECIALIZED_CANDIDATE_TO_CANONICAL'
            migration = True
        elif 'service_provider_does_not_receive' in name:
            root, first = 'Beneficiary-oriented conclusion was checked as positive contractual core arrangement', 'ORIENTATION_TO_POSITIVE_VERIFICATION'
        elif 'party_direction_and_finding' in name:
            root, first = 'Service subject candidates lost predicate and list-context output sources', 'SPECIALIZED_CANDIDATE_TO_CANONICAL'
        else:
            root, first = 'License controls/remedies retain legacy untyped coverage rows; exact verifier rejects semantic support', 'SPECIALIZED_CANDIDATE_TO_CANONICAL'
        path, obj = captured[key] if key in captured else (None, None)
        rejects = []
        if obj:
            for item in obj['report']['items']:
                gate = item.get('decision_trace', {}).get('verified_pass_source_gate') or {}
                for failure in gate.get('failures', []):
                    element = next((e for e in item.get('coverage_elements', [])
                                    if e.get('element_id') == failure.get('element_id')), {})
                    rejects.append(dict(rule_id=item['item_id'], element_id=failure.get('element_id'),
                        fact_id=element.get('fact_id'), fact_ids=element.get('fact_ids'),
                        source_fact_key=element.get('source_fact_key'),
                        source_clause_ids=element.get('source_clause_ids'), source_spans=element.get('source_spans'),
                        reject=failure))
        adjudication.append(dict(test_id=key, classification=kind, root=root, first_stage=first,
            test_migration=migration, round6=r6[key], round7=before[key], current=after[key],
            diagnostic_capture=str(path) if path else None,
            diagnostic_capture_mtime=path.stat().st_mtime if path else None,
            captured_rejections_are_historical_diagnostics=True, captured_rejections=rejects))
    live = {}
    for name in ('patent','guard','consulting','industrial'):
        path = ART / f'round8_last_{name}_live' / 'report.json'
        if not path.exists():
            path = ART / f'round8_closure_{name}_live' / 'report.json'
        report = json.loads(path.read_text(encoding='utf8'))
        gate = report['release_quality_gate']
        runtime = report.get('production_path_trace') or {}
        loaded = runtime.get('runtime_sources', {}).get('engine', {}).get('sha256')
        actual = hashlib.sha256((ART.parents[1] / 'backend/review_v2/engine.py').read_bytes()).hexdigest()
        live[name] = dict(contract_type=report['contract_type'], status=gate['status'],
                         raw_failure_count=len(gate['failures']), failures=gate['failures'],
                         runtime=runtime, current_engine_sha256=actual,
                         final_revision_verified=loaded == actual, report_file=str(path))
    result = dict(items=adjudication,
        classification_counts={c: sum(x['classification'] == c for x in adjudication)
                               for c in ('IMPLEMENTATION','TEST_CONTRACT','UNRESOLVED')},
        targeted_pass=sum(x['current']['status']=='PASS' for x in adjudication),
        targeted_fail=sum(x['current']['status']=='FAIL' for x in adjudication),
        implementation_only_recovered=[x['test_id'] for x in adjudication
            if x['current']['status']=='PASS' and not x['test_migration']],
        migrated_targeted=[x['test_id'] for x in adjudication if x['test_migration']],
        prior_eight={k: after[k] for k in r7['recovered']},
        round7_new_guards={k: after[k] for k in r7['added']},
        new_tests={k: v for k,v in after.items() if k not in before},
        current={s:sum(x['status']==s for x in after.values()) for s in ('PASS','FAIL','SKIP')},
        api=live)
    (ART/'round8_adjudication.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps({k:result[k] for k in ('classification_counts','targeted_pass','targeted_fail','current')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
