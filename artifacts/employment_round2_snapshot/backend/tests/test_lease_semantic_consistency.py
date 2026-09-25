from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from collections import Counter

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import review_contract_v2, _apply_coverage_gap_consistency_guard, _set_item_not_applicable
from review_v2.lease_semantics import PROFILES, apply, applicability, consistency_failures, corpus_facts, economic_exposure, party_types, requirement
from review_v2.report_statistics import statistics_gate


@pytest.fixture(scope='module')
def report():
    from docx import Document
    path = Path(__file__).resolve().parents[2] / 'test_data/53 租赁合同.docx'
    return review_contract_v2('\n'.join(p.text for p in Document(path).paragraphs if p.text.strip()), 'lease', use_llm=False)


def test_zero_positive_cannot_preserve_partial(report):
    row = deepcopy(next(r for r in report['items'] if r['node_id'] == 'indefinite_lease'))
    row['coverage_status'] = '部分覆盖'
    obj = SimpleNamespace(**row)
    _apply_coverage_gap_consistency_guard([obj])
    assert obj.coverage_status == '缺失'
    assert not obj.evidence_clauses


def test_partial_has_positive_and_missing_elements(report):
    for row in report['items']:
        if row['coverage_status'] != '部分覆盖':
            continue
        assert any(e['status'] == 'COVERED' and e['source_spans'] and e['source_locations'] for e in row['coverage_elements'])
        assert any(e['status'] in {'MISSING', 'PARTIALLY_COVERED', 'UNCERTAIN'} for e in row['coverage_elements'])


def test_shared_fact_has_identical_evidence(report):
    rows = [r for r in report['items'] if r['node_id'] in {'agreed_termination', 'termination_notice'}]
    elements = [next(e for e in r['coverage_elements'] if e['element_id'] == 'termination_trigger') for r in rows]
    assert len(elements) == 2
    assert all(e['status'] == 'COVERED' for e in elements)
    assert elements[0]['source_spans'] == elements[1]['source_spans']
    forged = deepcopy(rows)
    next(e for e in forged[1]['coverage_elements'] if e['element_id'] == 'termination_trigger')['status'] = 'MISSING'
    assert any(f['requirement'] == 'CROSS_RULE_FACT_STATUS_CONFLICT' for f in consistency_failures([SimpleNamespace(**r) for r in forged]))


def test_applicability_evaluator_accepts_arbitrary_fact_keys():
    assert applicability({'absent_fact': 'arbitrary.prerequisite'}, {'arbitrary.prerequisite': [{'text': 'direct source'}]}, {})[0] is False
    assert applicability({'absent_fact': 'arbitrary.prerequisite'}, {}, {})[0] is True


@pytest.mark.parametrize('tenant,kind', [('某某科技有限公司', 'LEGAL_PERSON'), ('某某合伙企业', 'UNINCORPORATED_ORGANIZATION'), ('张三', 'NATURAL_PERSON'), ('______', 'UNKNOWN')])
def test_party_types_are_role_specific(tenant, kind):
    types = party_types('甲方（出租人）：李四\n乙方（承租人）：' + tenant)
    assert types['landlord']['type'] == 'NATURAL_PERSON'
    assert types['tenant']['type'] == kind


def test_na_is_removed_from_risks_and_recommendations(report):
    nodes = {'tenant_death_successor', 'tenant_death_settlement', 'lessor_death', 'no_early_clause_fallback'}
    rows = [r for r in report['items'] if r['node_id'] in nodes]
    assert len(rows) == 4
    for r in rows:
        assert r['coverage_status'] == '不适用'
        assert r['risk_severity'] == 'NONE'
        assert not r['needs_manual_review']
        assert not any(r['item_id'] in f['source_review_ids'] for f in report['risk_findings'])


@pytest.mark.parametrize('text,expected', [
    ('乙方提前退租应通知甲方。合同没有调减机制。', 'LOW'),
    ('乙方提前退租的，违约方应按照两个月房屋租金向对方支付违约金。', 'MEDIUM'),
    ('乙方提前退租的，应按照12个月房屋租金支付违约金。', 'HIGH'),
    ('第一条 退出\n乙方提前退租应通知。\n第二条 迟延\n逾期付款按12个月租金支付违约金。', 'LOW'),
])
def test_economic_ceiling_requires_same_event_direct_amount(text, expected):
    assert economic_exposure(parse_contract_clauses(text))['ceiling'] == expected


def test_current_two_month_fee_is_not_major_risk(report):
    row = next(r for r in report['items'] if r['node_id'] == 'early_surrender')
    assert row['decision_trace']['economic_evidence_assessment']['monthly_multiple'] == 2
    assert row['risk_severity'] != 'HIGH'
    assert row['risk_level'] != '高'
    assert '改为固定月租倍数' not in report['result']
    forged = deepcopy(row)
    forged['risk_severity'] = 'HIGH'
    assert any(f['requirement'] == 'ECONOMIC_SEVERITY_EXCEEDS_EVIDENCE' for f in consistency_failures([SimpleNamespace(**forged)]))


def test_summary_detail_statistics_and_release(report):
    assert Counter(r['coverage_status'] for r in report['items']) == report['coverage_summary']
    assert sum(report['coverage_summary'].values()) == 50
    assert sum(report['summary'].values()) == 50 - report['coverage_summary']['不适用']
    assert statistics_gate(report)['status'] == 'REPORT_READY'
    assert not consistency_failures([SimpleNamespace(**r) for r in report['items']])
    assert report['release_quality_gate']['status'] == 'REPORT_READY'


def test_relationship_retrieval_is_not_keyword_or_section_number_based():
    requirements = PROFILES['indefinite_lease']
    unrelated = parse_contract_clauses('9.8 续租\n期满前提前60日通知，双方另行签订续租合同。')
    assert not any(corpus_facts(unrelated, requirements).values())
    moved = parse_contract_clauses('45.6 约定\n租期届满后继续使用房屋，出租人未提出异议。')
    facts = corpus_facts(moved, requirements)
    assert facts['post_expiry_continue_use'][0]['location'].endswith('45.6')
    assert facts['no_objection_or_rent_acceptance']


def test_evaluator_does_not_depend_on_review_number(report):
    row = deepcopy(next(r for r in report['items'] if r['node_id'] == 'termination_notice'))
    row['item_id'] = 'CUSTOM-RENUMBERED'
    obj = SimpleNamespace(**row)
    text = '99.8 解除\n乙方逾期不付款的，甲方有权解除本合同。'
    apply([obj], parse_contract_clauses(text), text, _set_item_not_applicable)
    assert obj.coverage_status == '部分覆盖'
    assert obj.evidence_clauses[0]['location'].endswith('99.8')


def test_natural_person_condition_does_not_exempt_unknown_parties():
    condition = {'party': 'tenant', 'types': ['NATURAL_PERSON']}
    assert applicability(condition, {}, {'tenant': {'type': 'UNKNOWN'}})[0]
    assert applicability(condition, {}, {'tenant': {'type': 'NATURAL_PERSON'}})[0]
    assert not applicability(condition, {}, {'tenant': {'type': 'LEGAL_PERSON'}})[0]
