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


def test_lease_before_sale_missing_uses_statutory_default_protection(report):
    row = next(r for r in report['items'] if r['item_id'] == 'HL-020')
    gap = row['decision_trace']['effective_gap']
    assessment = row['decision_trace']['default_law_assessment']
    priority = row['decision_trace']['priority_assessment']

    assert row['coverage_status'] == '缺失'
    assert row['decision_trace']['default_law_status'] == 'CLEAR_DEFAULT'
    assert assessment['status'] == 'CLEAR_DEFAULT'
    assert assessment['rule']['rule_id'] == 'LEASE-DEFAULT-SALE-NO-BREAK'
    assert gap['contract_coverage'] == '缺失'
    assert gap['statutory_default'] == 'CLEAR_DEFAULT'
    assert gap['default_strength'] == 'strong'
    assert gap['default_law_checked'] is True
    assert gap['affected_effective_gap'] is True
    assert gap['authority_ids'] == ['CN-CIVIL-CODE-725']
    assert '第725条' in gap['statutory_protection_scope']
    assert '不影响租赁合同效力' in gap['statutory_protection_scope']
    assert priority['input']['statutory_default_status'] == 'CLEAR_DEFAULT'
    assert priority['input']['default_protection_strength'] == 'strong'
    assert priority['input']['contract_override_risk'] == 'low'
    assert any(
        claim.get('authority_id') == 'CN-CIVIL-CODE-725'
        and claim.get('claim_type') == 'STATUTORY_DEFAULT'
        and claim.get('article') == '第725条'
        for claim in row['legal_references']
    )
    assert '未识别到足以补足该缺口的明确法定默认规则' not in row['legal_consequence_if_missing']
    section = report['result'].split('## 20. 房屋出售后的租赁承继（HL-020）', 1)[1].split('\n---', 1)[0]
    assert '合同层面未明确约定' in section
    assert '实际法律暴露受到法定规则补位' in section
    assert '未识别到足以补足该缺口的明确法定默认规则' not in section


def _review_section(report_text: str, item_id: str) -> str:
    marker = f"（{item_id}）"
    tail = report_text.split(marker, 1)[1]
    return tail.split('\n---', 1)[0]


def test_lease_statutory_fallback_is_global_four_layer_model(report):
    expected = {
        'HL-013': {
            'status': 'CLEAR_DEFAULT',
            'strength': 'strong',
            'authorities': {'CN-CIVIL-CODE-734', 'CN-CIVIL-CODE-730'},
            'tokens': ['第734条', '第730条', '不定期租赁'],
        },
        'HL-020': {
            'status': 'CLEAR_DEFAULT',
            'strength': 'strong',
            'authorities': {'CN-CIVIL-CODE-725'},
            'tokens': ['第725条', '买卖不破租赁', '不影响租赁合同效力'],
        },
        'HL-039': {
            'status': 'CLEAR_DEFAULT',
            'strength': 'strong',
            'authorities': {'CN-CIVIL-CODE-585'},
            'tokens': ['第585条', '司法调整', '不等于当然无法调整'],
        },
    }
    rows = {r['item_id']: r for r in report['items']}
    for item_id, spec in expected.items():
        row = rows[item_id]
        gap = row['decision_trace']['effective_gap']
        priority = row['decision_trace']['priority_assessment']
        assert row['coverage_status'] in {'缺失', '部分覆盖'}
        assert row['coverage_status'] != '通过'
        assert row['decision_trace']['default_law_status'] == spec['status']
        assert gap['contract_coverage'] == row['coverage_status']
        assert gap['statutory_default'] == spec['status']
        assert gap['default_strength'] == spec['strength']
        assert gap['default_law_checked'] is True
        assert gap['affected_effective_gap'] is True
        assert set(gap['authority_ids']) == spec['authorities']
        assert priority['input']['statutory_default_status'] == spec['status']
        assert priority['input']['default_protection_strength'] == spec['strength']
        assert priority['priority'] in {'B_PRACTICAL', 'C_OPTIMIZATION'}
        assert '未识别到足以补足该缺口的明确法定默认规则' not in row['legal_consequence_if_missing']
        section = _review_section(report['result'], item_id)
        assert '【实际法律暴露】' in section
        assert '实际法律暴露受到法定规则补位' in section
        assert '未识别到足以补足该缺口的明确法定默认规则' not in section
        for token in spec['tokens']:
            assert token in section or token in gap['statutory_protection_scope']


def test_declared_lease_default_law_nodes_have_effective_gap_entities(report):
    declared = {
        'indefinite_lease',
        'lease_before_sale',
        'force_majeure',
        'changed_circumstances',
        'pre_delivery_defect',
        'third_party_tort',
        'third_party_defect',
        'housing_safety_emergency',
        'excessive_deduction',
        'deposit_offset_order',
        'property_damage_deposit_evidence',
    }
    rows = [
        r for r in report['items']
        if r['coverage_status'] in {'缺失', '部分覆盖'}
        and (r['node_id'] in declared or r['risk_group'] in declared)
    ]
    assert rows
    for row in rows:
        assessment = row['decision_trace']['default_law_assessment']
        gap = row['decision_trace']['effective_gap']
        assert assessment['executed'] is True
        assert assessment['rule']['rule_id']
        assert gap['default_law_checked'] is True
        assert gap['statutory_default'] in {'CLEAR_DEFAULT', 'PARTIAL_DEFAULT', 'NONE'}
        assert gap['affected_effective_gap'] is (gap['statutory_default'] in {'CLEAR_DEFAULT', 'PARTIAL_DEFAULT'})
        assert gap['authority_ids']
        assert gap['contract_coverage'] == row['coverage_status']
        assert row['coverage_status'] != '通过'


def test_lease_default_law_direct_semantic_gate_reaches_production_and_renderer(report):
    rows = {r['item_id']: r for r in report['items']}
    for item_id in {'HL-035', 'HL-037', 'HL-040', 'HL-041', 'HL-042'}:
        row = rows[item_id]
        assessment = row['decision_trace']['default_law_assessment']
        gap = row['decision_trace']['effective_gap']
        assert row['legal_basis_index']
        assert assessment['direct_match'] is False
        assert assessment['fallback_match'] is False
        assert assessment['status'] == 'NONE'
        assert gap['statutory_default'] == 'NONE'
        assert gap['default_strength'] == 'none'
        assert gap['affected_effective_gap'] is False
        assert not gap['statutory_protection_scope']
        assert '现行法律提供部分默认处理规则' not in _review_section(report['result'], item_id)

    assert rows['HL-037']['decision_trace']['default_law_assessment']['rule']['authority_ids'] == ['CN-CIVIL-CODE-585']
    assert rows['HL-035']['decision_trace']['default_law_assessment']['rule']['authority_ids'] == ['CN-CIVIL-CODE-710', 'CN-CIVIL-CODE-714']


def test_lease_default_law_positive_controls_pass_all_semantic_dimensions(report):
    rows = {r['item_id']: r for r in report['items']}
    for item_id in {'HL-013', 'HL-020', 'HL-039'}:
        assessment = rows[item_id]['decision_trace']['default_law_assessment']
        assert assessment['direct_match'] is True
        assert assessment['role_match'] is True
        assert assessment['scenario_match'] is True
        assert assessment['legal_effect_match'] is True
        assert assessment['fallback_match'] is True
        assert assessment['status'] == 'CLEAR_DEFAULT'


def test_default_law_audit_covers_every_lease_gap_with_legal_basis(report):
    expected = {
        row['item_id'] for row in report['items']
        if row['coverage_status'] in {'缺失', '部分覆盖'} and row['legal_basis_index']
    }
    audit = report['observability']['default_law_debug_table']
    assert {row['review_id'] for row in audit} == expected
    required = {
        'review_id', 'target_element', 'legal_basis', 'direct_match', 'role_match',
        'scenario_match', 'legal_effect_match', 'statutory_fallback', 'actual_legal_exposure',
    }
    assert all(required <= set(row) for row in audit)
    assert not [
        row for row in audit
        if not row['direct_match'] and row['statutory_fallback'] in {'CLEAR_DEFAULT', 'PARTIAL_DEFAULT'}
    ]


def test_general_contract_renegotiation_default_reaches_renderer_without_changing_coverage(report):
    from review_v2.engine import _default_law_assessment
    row = next(r for r in report['items'] if r['node_id'] == 'changed_circumstances')
    assessment = row['decision_trace']['default_law_assessment']
    assert all(assessment[key] for key in (
        'direct_match', 'role_match', 'scenario_match', 'legal_effect_match', 'fallback_match'))
    assert assessment['status'] == 'PARTIAL_DEFAULT'
    assert assessment['rule']['authority_ids'] == ['CN-CIVIL-CODE-533']
    assert '重新协商' in assessment['authority_validation'][0]['authority']['text']
    assert row['coverage_status'] == '缺失'
    gap = row['decision_trace']['effective_gap']
    assert gap['contract_coverage'] == '缺失'
    assert gap['statutory_default'] == 'PARTIAL_DEFAULT'
    assert gap['affected_effective_gap'] is True
    section = _review_section(report['result'], row['item_id'])
    assert '【实际法律暴露】' in section
    assert '实际法律暴露受到法定规则补位' in section
    assert '重新协商' in section and '仲裁机构' in section
    renamed = SimpleNamespace(**deepcopy(row))
    renamed.item_id = 'RENAMED-GENERAL-CONTRACT-REMEDY'
    assert _default_law_assessment(renamed, 'lease')['status'] == 'PARTIAL_DEFAULT'
    renamed.coverage_elements[0]['element_id'] = 'damage_proof_burden'
    assert _default_law_assessment(renamed, 'lease')['status'] == 'NONE'


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
    assert report['release_quality_gate']['status'] in {'REPORT_READY', 'BLOCKED'}
    if report['release_quality_gate']['status'] == 'BLOCKED':
        assert any(failure.get('requirement') == 'RELEASE_HOLD' for failure in report['release_quality_gate']['failures'])


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
