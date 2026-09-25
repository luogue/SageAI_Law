"""Audit a saved production object against the shared parser predicates.

Counts rule/source pairs (not repeated renderings of the same evidence).
Composite residual aliases are reported separately from unrelated sources.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'backend'), str(ROOT)]
from backend.test_database_bootstrap import install
install()
from layers.input_layer import InputLayer
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import _atomic_requirement_definitions, ReviewItemResult
from review_v2.element_evidence_projection import _key
from review_v2.technology_adverse_evidence import verify_negative_search


def scan(report, clauses):
    unrelated, partial = [], []
    scanned = 0
    for raw in report['items']:
        if not raw['item_id'].startswith('TC-'):
            continue
        item = ReviewItemResult(**raw)
        if (item.coverage_status in {'通过', 'PASS'} and not any(e['status'] in {'COVERED', 'PARTIALLY_COVERED', 'ADVERSE', 'CONFLICTING'} for e in item.coverage_elements)
                and verify_negative_search(item, clauses)):
            unrelated.extend(dict(rule_id=item.item_id, evidence_id=r.get('evidence_id'),
                clause_id=r.get('clause_id'), quote=r.get('quote'), reason='NEGATIVE_SEARCH_CONTEXT_NOT_ELEMENT_PROOF')
                for r in item.evidence_clauses)
        family = item.decision_trace.get('atomic_requirement_family')
        if not family:
            continue
        scanned += 1
        definitions = _atomic_requirement_definitions(family, clauses)
        definitions += [c for e in list(definitions) for c in e.get('child_elements', []) if isinstance(c, dict)]
        expected = {e['element_id']: e for e in definitions}
        valid_sources = set()
        for e in item.coverage_elements:
            definition = expected.get(e['element_id'])
            if not definition:
                continue
            proofs = definition.get('supporting_evidence', [])
            if e['status'] in {'COVERED', 'PARTIALLY_COVERED', 'ADVERSE', 'CONFLICTING'}:
                valid_sources.update(_key(p) for p in proofs)
            if e['status'] == 'PARTIALLY_COVERED':
                absent_children = [c for c in definition.get('child_elements', []) if c['status'] == 'MISSING']
                judgment = (item.narrative_state or {}).get('judgment', '')
                if not proofs or any(c['required_fact'] + '已有部分' in judgment for c in absent_children):
                    partial.append(dict(rule_id=item.item_id, element_id=e['element_id'],
                        reason='NO_POSITIVE_SOURCE' if not proofs else 'ABSENT_COMPONENT_RENDERED_AS_PARTIAL',
                        absent_components=[c['element_id'] for c in absent_children]))
        for row in item.evidence_clauses:
            if row.get('source_type') == 'SEARCH_AUDIT':
                continue
            if _key(row) not in valid_sources:
                unrelated.append(dict(rule_id=item.item_id, evidence_id=row.get('evidence_id'),
                    clause_id=row.get('clause_id'), quote=row.get('quote') or row.get('quoted_text')))
    return dict(scanned_modeled_rule_count=scanned, unrelated_evidence_count=len(unrelated),
                false_partial_count=len(partial), unrelated_evidence=unrelated, false_partials=partial)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('source', type=Path); p.add_argument('report', type=Path); p.add_argument('output', type=Path)
    args = p.parse_args()
    text = InputLayer()._extract_from_docx_content(args.source.read_bytes())
    if isinstance(text, dict): text = text['text']
    result = scan(json.loads(args.report.read_text(encoding='utf8')), parse_contract_clauses(text))
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps({k:v for k,v in result.items() if not isinstance(v, list)}, ensure_ascii=False))


if __name__ == '__main__': main()
