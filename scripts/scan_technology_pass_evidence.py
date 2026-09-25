"""Audit final technical PASS atoms against parser sources and their predicates.

Reports only inspected objects; zero failures is not an assertion that every
possible future legal proposition has a semantic model.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'backend'), str(ROOT)]
from backend.test_database_bootstrap import install
install()

from layers.input_layer import InputLayer
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import ReviewItemResult, _verified_pass_sources, _attach_evidence_traceability


def scan(report, clauses, include_covered=False):
    rows = [deepcopy(row) for row in report['items'] if row['item_id'].startswith('TC-')]
    selected = []
    for row in rows:
        if row['coverage_status'] in ('通过', 'PASS'):
            selected.append(row)
        elif include_covered:
            elements = [e for e in row.get('coverage_elements', []) if e['status'] == 'COVERED']
            if not elements:
                continue
            ids = {eid for e in elements for eid in e.get('evidence_ids', [])}
            sources = [s for e in elements for s in e.get('supporting_evidence', [])]
            row['evidence_clauses'] = [r for r in row['evidence_clauses']
                if r.get('source_type') != 'SEARCH_AUDIT' and (r.get('evidence_id') in ids
                    or any(s.get('clause_id') == r.get('clause_id') and s.get('quote') == r.get('quote') for s in sources))]
            row['coverage_elements'] = elements
            row['coverage_status'] = '通过'  # Audit only the positive projection, not its residuals.
            selected.append(row)
    items = [ReviewItemResult(**row) for row in selected]
    if include_covered:
        original_statuses = {row['item_id']: row['coverage_status'] for row in report['items']}
        # Partial findings publish EV records rather than the PASS-only SRC
        # representation. Verify those quoted spans against the original parser
        # before applying the same semantic predicates to this audit projection.
        _attach_evidence_traceability([i for i in items if original_statuses[i.item_id] not in ('通过', 'PASS')], clauses)
    check = _verified_pass_sources(items, clauses)
    return dict(pass_rule_count=len(items), covered_element_count=sum(len(i.coverage_elements) for i in items),
                mismatch_count=len(check['failures']), failures=check['failures'],
                rules=[dict(rule_id=i.item_id, status=i.coverage_status,
                            check=i.decision_trace['verified_pass_source_gate'],
                            elements=[dict(element_id=e['element_id'], status=e['status'],
                                           proposition=e['proposition'], evidence_ids=e.get('evidence_ids', []))
                                      for e in i.coverage_elements],
                            evidence=[dict(evidence_id=e.get('evidence_id'), clause_id=e.get('clause_id'),
                                           location=e.get('location'), quote=e.get('quote')) for e in i.evidence_clauses])
                       for i in items])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('report', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--include-covered', action='store_true')
    args = parser.parse_args()
    text = InputLayer()._extract_from_docx_content(args.source.read_bytes())
    if isinstance(text, dict):
        text = text['text']
    result = scan(json.loads(args.report.read_text(encoding='utf8')), parse_contract_clauses(text), args.include_covered)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps({k: v for k, v in result.items() if k != 'rules'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
