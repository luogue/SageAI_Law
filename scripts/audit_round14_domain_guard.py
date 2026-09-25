"""Isolated counterfactual for the additional domain guard; never used by API.

Compare the new signal-source checks with the pre-change collector while
leaving every downstream verifier and gate intact. No production file changes.
"""
import ast
import inspect
import json
import runpy
from pathlib import Path
from review_v2 import domain_selection as domain


def main():
    test = runpy.run_path('backend/tests/test_domain_selection_consistency.py')
    original = domain._collect_family_evidence
    tree = ast.parse(inspect.getsource(original))
    loop = next(n for n in tree.body[0].body if isinstance(n, ast.For))
    loop.body = [n for n in loop.body if not (
        isinstance(n, ast.If) and 'signal_type.endswith' in ast.unparse(n.test))]
    for node in loop.body:
        if isinstance(node, ast.If) and 'lease_parties' in ast.unparse(node.test):
            node.body = [n for n in node.body if not (
                isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
                and n.targets[0].id == 'hits')]
    scope = dict(original.__globals__)
    exec(compile(ast.fix_missing_locations(tree), '<pre-change-collector-diagnostic>', 'exec'), scope)
    results = {}
    try:
        for name, collector in [('current', original), ('without_new_signal_filters', scope[original.__name__])]:
            domain._collect_family_evidence = collector
            report = test['review_contract_v2'](test['FRAMEWORK_SUPPLY'], 'house_lease', use_llm=False)
            results[name] = dict(domain_gate=report['domain_selection_consistency_gate'],
                                 failures=report['release_quality_gate']['failures'])
    finally:
        domain._collect_family_evidence = original
    results['same_blockers'] = results['current']['failures'] == results['without_new_signal_filters']['failures']
    Path('artifacts/technology_pass_semantics/round14_domain_guard_audit.json').write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding='utf8')
    print('same_blockers', results['same_blockers'])
    print(json.dumps(results['current']['failures'], ensure_ascii=False))


if __name__ == '__main__':
    main()
