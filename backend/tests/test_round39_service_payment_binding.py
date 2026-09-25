from pathlib import Path

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.technology_service_elements import elements


def test_service_fee_heading_scopes_the_separate_amount_proposition():
    text = (
        '技术服务合同\n'
        '第六条 服务费用及支付\n'
        '本合同含税总价为人民币480,000元（大写：肆拾捌万元整）。\n'
        '上述费用包括现场实施、系统配置、人员培训和技术支持费用。'
    )
    row = elements('service_payment', parse_contract_clauses(text))[0]
    assert row['status'] == 'COVERED'
    assert row['source_fact_key'] == 'technology.service_payment.technical_service_remuneration'
    assert row['supporting_evidence'][0]['quote'].startswith('本合同含税总价为人民币480,000元')


@pytest.mark.parametrize('party', ['甲方', '乙方'])
def test_round39_payment_fact_has_exact_direct_final_binding(party):
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile

    text = (Path(__file__).parent / 'fixtures' / 'round39_service.txt').read_text(encoding='utf8')
    report = review_contract_v2(
        text, 'technology', use_llm=False,
        profile=UserRiskProfile(user_identity=party),
    )
    assert report['release_quality_gate']['status'] == 'REPORT_READY', report['release_quality_gate']['failures']
    item = next(row for row in report['items'] if row['item_id'] == 'TC-09-04')
    element = next(row for row in item['coverage_elements'] if row['element_id'] == 'technical_service_remuneration')
    assert item['coverage_status'] == '通过' and element['status'] == 'COVERED'
    assert element['source_fact_key'] == 'technology.service_payment.technical_service_remuneration'
    fact = item['decision_trace']['contract_fact_registry_consumption']['facts'][element['source_fact_key']]
    assert fact['status'] == 'FOUND'
    assert fact['source_clause_ids'] == ['C0016']
    evidence = next(row for row in item['evidence_clauses'] if row['evidence_id'] in element['evidence_ids'])
    assert evidence['support_type'] == 'DIRECT'
    assert evidence['verified_original'] is True
    assert evidence['source_span']['raw_text'] == element['source_spans'][0]
    gate = report['release_quality_gate']['gate_results']
    assert gate['REVIEW_EVIDENCE_ELEMENT_MISMATCH'] == 'PASS'
    assert gate['EXACT_ELEMENT_REPORT_INVARIANT'] == 'PASS'
