from copy import deepcopy
from types import SimpleNamespace

import pytest

from .test_lease_semantic_consistency import report
from review_v2.lease_semantics import PROFILES, supports, rule_evidence_package, evidence_identity


@pytest.mark.parametrize('text,expected', [
    ('属于甲方维修责任的合理维修费用由甲方承担。', False),
    ('乙方自行维修的合理维修费用由甲方承担。', False),
    ('乙方造成损坏，从押金中扣除的维修费用应当合理。', True),
    ('乙方造成损坏的维修费用从押金中扣除。属于甲方维修责任的合理维修费用由甲方承担。', False),
    ('甲方造成损坏，从押金中扣除的维修费用应当合理。', False),
])
def test_cost_proof_requires_same_party_and_scenario(text, expected):
    spec = PROFILES['reasonable_repair_cost'][1]
    assert supports(spec, {'text': text, 'clause_id': 'custom', 'location': '第九条'}) is expected


def test_rule_packages_have_exact_element_ownership(report):
    for raw in report['items']:
        item = SimpleNamespace(**raw)
        package = item.rule_evidence_package
        elements = {e['element_id']: e for e in item.coverage_elements}
        specs = {e['element_id']: e for e in item.decision_trace.get('semantic_requirements', [])}
        assert package == rule_evidence_package(item)
        for row in package['items']:
            assert row['evidence_id'] and row['evidence_id'] != 'None'
            assert row['supporting_review_ids'] == [item.item_id]
            assert set(row['supporting_element_ids']) <= elements.keys()
            for key in row['supporting_element_ids']:
                if row.get('source_type') == 'SEARCH_AUDIT':
                    assert elements[key]['status'] in {'MISSING', 'PARTIALLY_COVERED', 'UNCERTAIN'}
                elif key in specs:
                    assert supports(specs[key], row)
        assert package == rule_evidence_package(SimpleNamespace(**deepcopy(raw)))


def test_cost_scope_missing_does_not_borrow_landlord_proof(report):
    item = next(i for i in report['items'] if i['node_id'] == 'reasonable_repair_cost')
    assert item['coverage_status'] == '缺失'
    assert all(e['status'] == 'MISSING' for e in item['coverage_elements'])
    assert all(r['source_type'] == 'SEARCH_AUDIT' for r in item['rule_evidence_package']['items'])


def test_user_report_has_no_null_evidence_id(report):
    assert '[None]' not in report['result']
    assert '证据ID：None' not in report['result']
    for row in ({'text': '计算值', 'evidence_id': None}, {'quote': '真实原文', 'location': '第八条'}):
        assert evidence_identity(row) == evidence_identity(deepcopy(row))
        assert evidence_identity(row)['evidence_id'].startswith('SYN-')
