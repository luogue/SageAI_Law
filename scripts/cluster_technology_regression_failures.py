"""Auditable first-failing-assertion triage, not a claim of causal proof.

Each test is counted exactly once. Only documented obsolete assertions are
labelled genuinely outdated; heuristic buckets explicitly require follow-up.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

CATEGORIES = ('extraction miss', 'normalization / canonical mapping', 'applicability',
              'polarity', 'evidence binding', 'SEARCH_AUDIT conflict',
              'report rendering', 'genuinely outdated test expectation')
REVIEWED = {
    'test_cooperative_classification_uses_core_transaction_evidence':
        'Exact operative quotes need not repeat section headings or start with the funding section. '
        'Current source spans directly prove shared R&D; forcing quote order is not a semantic requirement.',
    'test_structural_pass_is_linked_to_higher_priority_substantive_risk':
        'TC-09-03 includes required service_result_use_boundary=MISSING with no direct source. '
        'The unchanged test still demands whole-rule PASS; ownership alone cannot prove that third element.',
}


def classify(name, assertion):
    if name in REVIEWED:
        return CATEGORIES[7], 'SOURCE_AND_ASSERTION_REVIEWED', REVIEWED[name]
    signals = assertion + '\n' + name
    checks = [
        (5, r'SEARCH_AUDIT|search_audit|absence_search|searched_absent|absence.*conflict|positive.*missing|conflict.*missing', 'absence/positive search disagreement'),
        (2, r'applicab|NOT_APPLICABLE|不适用|primary_subtype|primary_contract_type|transaction_structure|filters_unrelated|classification_prefers|subtype.*routing', 'applicability or transaction-route assertion'),
        (4, r'NO_VERIFIED|VERIFIED_PASS_ORIGINAL_GATE|IRRELEVANT_PASS|EVIDENCE_INSUFFICIENT|evidence_consistency_gate|direct_evidence|evidence_id|evidence_clauses|source_span|lineage|provenance', 'source/evidence verification assertion'),
        (1, r'KeyError|CROSS_REVIEW_FACT_CONFLICT|canonical|fact_id|fact_registry|shared_claim|shared_fact|normalized', 'canonical identity or projection field assertion'),
        (3, r'风险条款|ADVERSE|RISK_CLAUSE|polarity|favorable|unfavorable|direction|severity|priority|risk_level|risk_to_current_party|directly_burdened|不利|有利', 'risk polarity or orientation assertion'),
        (6, r'reasoning_summary|risk_point_description|action_suggestion|legal_consequence|suggested_clause|narrative|renderer|report\.split|report\[|in report|in rendered|统计|汇总|markdown|disposition', 'rendered state or presentation assertion'),
        (0, r'COVERED|MISSING|PARTIAL|缺失|部分覆盖|通过|scope_defined|found|extract|recall|识别|覆盖', 'coverage/extraction assertion'),
    ]
    for index, pattern, reason in checks:
        if re.search(pattern, signals, re.I):
            return CATEGORIES[index], 'ASSERTION_SIGNATURE_TRIAGE', reason
    return CATEGORIES[1], 'NEEDS_CAUSAL_REVIEW', 'Unresolved state/schema assertion; inspect per-test record before changing code.'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('xml', nargs='+', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    records, seen = [], set()
    for path in args.xml:
        for case in ET.parse(path).iter('testcase'):
            failure = case.find('failure')
            if failure is None:
                failure = case.find('error')
            if failure is None:
                continue
            key = case.get('classname') + '::' + case.get('name')
            if key in seen:
                raise ValueError('Duplicate test: ' + key)
            seen.add(key)
            assertion = (failure.text or failure.get('message', '')).split('Captured')[0][:6000]
            category, confidence, reason = classify(case.get('name'), assertion)
            records.append(dict(test_id=key, category=category, confidence=confidence,
                                reason=reason, assertion=assertion))
    counts = Counter(r['category'] for r in records)
    result = dict(method='FIRST_FAILING_ASSERTION_TRIAGE; not all buckets are confirmed causal diagnoses',
                  total_failures=len(records), counts={c: counts[c] for c in CATEGORIES},
                  confidence_counts=dict(Counter(r['confidence'] for r in records)), tests=records)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps({k: v for k, v in result.items() if k != 'tests'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
