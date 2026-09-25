"""Inspect changed regression objects without replacing their assertions."""
import importlib
import json
from pathlib import Path
import sys
import inspect

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'backend'), str(ROOT)]
from backend.test_database_bootstrap import install
install()

CASES = [
    ('test_cooperative_development_latest_regressions', 'latest_cooperative_review', ['TC-02-02']),
    ('test_technical_service_latest_shared_fact_regressions', '_review', ['TC-09-03', 'TC-09-04']),
    ('test_patent_application_transfer_consistency', 'result', ['TC-06-04']),
    ('test_current_patent_license_evidence_recall', 'review', ['TC-07-01']),
    ('test_entrusted_development_consistency', 'gold_review', ['TC-04-01']),
    ('test_cooperative_development_evidence_fact_conclusion_consistency', 'cooperative_review', ['TC-01-01', 'TC-01-02']),
    ('test_technical_secret_transfer_contract_review', 'review', ['TC-02-02']),
]


def main():
    output = {}
    for name, function, keys in CASES:
        module = importlib.import_module('tests.' + name)
        fn = getattr(module, function)
        fn = getattr(fn, '__wrapped__', fn)
        kwargs = {}
        for key in inspect.signature(fn).parameters:
            dependency = getattr(module, key)
            kwargs[key] = getattr(dependency, '__wrapped__', dependency)()
        report = fn(**kwargs)
        output[name] = [dict(rule_id=i['item_id'], coverage=i['coverage_status'],
                            elements=i['coverage_elements'], evidence=[{k: r.get(k) for k in (
                                'clause_id', 'evidence_id', 'quote', 'location', 'supporting_element_ids')}
                                for r in i['evidence_clauses']],
                            gate=i['decision_trace'].get('verified_pass_source_gate'),
                            reason=i['reasoning_summary'],
                            predicate_metadata={k: i['decision_trace'].get(k) for k in (
                                'review_polarity','review_nature','atomic_requirement_family','negative_check_basis',
                                'original_source_review_required','specialized_coverage')},
                            negative={k: v for k, v in i['decision_trace'].items() if 'negative' in k or 'predicate' in k},
                            family=i['decision_trace'].get('atomic_requirement_family'))
                        for i in report['items'] if i['item_id'] in keys]
        path = ROOT / 'artifacts/technology_pass_semantics/changed_objects_round3.json'
        path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf8')
        print(name, 'written', flush=True)


if __name__ == '__main__':
    main()
