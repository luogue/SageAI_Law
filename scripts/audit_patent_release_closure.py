"""Compare original release refusals against normal-upload report snapshots.

No synthesis of fact IDs: raw gate objects and the observed mutation timeline
are retained verbatim alongside the final element/evidence projection.
"""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--directory', type=Path, default=Path('artifacts/technology_pass_semantics'))
    p.add_argument('--round', default='round7')
    p.add_argument('--transitions', type=Path)
    args = p.parse_args()
    root = args.directory
    load = lambda path: json.loads(path.read_text(encoding='utf8'))
    baseline = load(root / 'round6_final_patent_blockers.json')
    old_transitions = load(root / 'round6_patent_stages/transitions.json')
    transitions = load(args.transitions) if args.transitions else []
    patent = load(root / f'{args.round}_final_patent_live/report.json')
    by_id = {i['item_id']: i for i in patent['items']}
    closures = []
    for index, row in enumerate(baseline['blockers'], 1):
        item = by_id.get(row['rule_id'], {})
        closures.append({
            'baseline_expanded_index': index, 'original_refusal': row,
            'fact_id': row['fact_id'], 'element_id': row['element_id'],
            'baseline_observed_transitions': [t for t in old_transitions if t['rule_id'] == row['rule_id']],
            'current_observed_transitions': [t for t in transitions if t['rule_id'] == row['rule_id']],
            'final_coverage': item.get('coverage_status'),
            'final_applicability': item.get('applicability'),
            'final_elements': item.get('coverage_elements'),
            'final_evidence': item.get('evidence_clauses'),
            'final_element_searches': item.get('decision_trace', {}).get('element_absence_searches'),
            'final_verification': item.get('decision_trace', {}).get('verified_pass_source_gate'),
            'publication_failures': patent['release_quality_gate']['failures'],
        })
    protections = {}
    for kind in ('patent', 'industrial', 'guard'):
        before = load(root / f'round6_final_{kind}_live/report.json')
        after = load(root / f'{args.round}_final_{kind}_live/report.json')
        a = {i['item_id']: i for i in before['items']}
        changes = [{'rule_id': i['item_id'], 'before': a[i['item_id']]['coverage_status'],
                    'after': i['coverage_status']}
                   for i in after['items'] if i['item_id'] in a
                   and a[i['item_id']]['coverage_status'] != i['coverage_status']]
        runtime = after['production_path_trace']
        protections[kind] = {
            'selected_type': after['selected_contract_type'], 'type': after['contract_type'],
            'before_gate': before['release_quality_gate']['status'],
            'gate': after['release_quality_gate']['status'],
            'before_raw_failures': len(before['release_quality_gate']['failures']),
            'raw_failures': len(after['release_quality_gate']['failures']),
            'remaining_failures': after['release_quality_gate']['failures'],
            'status_changes': changes, 'coverage_summary': after['coverage_summary'],
            'risk_theme_count': after['risk_theme_count'],
            'runtime': {k: runtime[k] for k in ('run_mode', 'entrypoint', 'engine_file', 'process_id')},
            'input_integrity': after.get('input_integrity'),
        }
    result = {
        'original_patent_sha256': hashlib.sha256((root / 'round6_patent/original.docx').read_bytes()).hexdigest(),
        'original_raw_failure_count': baseline['raw_failure_count'],
        'original_expanded_count': baseline['blocker_tuple_count'],
        'baseline_refusals': closures, 'protections': protections,
        'notes': 'Missing IDs remain null. Timelines record observed stages, not invented first-failure stages. '
                 'Publication status is taken only from the real upload response. Industrial timeline expectations '
                 'are not migrated: contract validity is not an independent performance deadline.',
    }
    target = root / f'{args.round}_release_closure.json'
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps({k: {'gate': v['gate'], 'raw_failures': v['raw_failures']}
                      for k, v in protections.items()}, ensure_ascii=False))


if __name__ == '__main__':
    main()
