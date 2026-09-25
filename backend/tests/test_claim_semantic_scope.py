"""Polarity and list scope at the fact producer and independent verifier."""
import pytest

from review_v2.technology_adverse_evidence import has_actual_infringement
from review_v2.technology_service_analysis import build_technology_fact_registry, claim_requirement_entailment


@pytest.mark.parametrize('text, expected', [
    ('如第三方主张本技术侵权，乙方应及时通知甲方。', False),
    ('若确认侵犯第三方专利，应停止使用。', False),
    ('如甲方在合同签署前已经明确知道有关技术侵犯第三方合法权利而未向乙方披露，甲方应赔偿损失。', False),
    ('甲方确认本技术目前侵犯第三方专利。', True),
    ('双方未发现本技术已经侵犯第三方专利。', False),
    ('双方未明确约定侵权处理方式。', False),
    ('双方未明确约定律师费、诉讼费承担。', False),
    ('甲方不允许乙方侵犯第三方技术成果。', False),
    ('甲方不得允许乙方侵犯第三方技术成果。', False),
    ('甲方确认本技术并未侵犯第三方专利。', False),
    ('甲方确认本技术未侵犯第三方专利。', False),
    ('甲方确认本技术不会侵犯第三方专利。', False),
    ('甲方确认本技术不再侵犯第三方专利。', False),
    ('甲方未确认本技术侵犯第三方专利。', False),
    ('双方无法确认本技术已经侵犯第三方专利。', False),
    ('假如本技术被确认侵犯第三方专利，甲方应赔偿损失。', False),
    ('当本技术被确认侵犯第三方专利时，甲方应赔偿损失。', False),
    ('在本技术被确认侵犯第三方专利的情况下，甲方应赔偿损失。', False),
    ('甲方允许乙方侵犯第三方技术成果。', True),
    ('若确认侵犯第三方专利，应当停止使用。甲方确认本技术目前侵犯第三方专利。', True),
    ('双方未明确约定侵权处理方式，但甲方确认本技术目前侵犯第三方专利。', True),
    ('双方未发现已经侵犯第三方专利，但甲方确认本技术目前侵犯第三方专利。', True),
    ('甲方确认本技术目前侵犯第三方专利，双方未明确约定侵权处理方式。', True),
])
def test_event_occurrence_polarity(text, expected):
    assert has_actual_infringement(text) is expected


@pytest.mark.parametrize('text, polarity', [
    ('甲方确认本技术目前侵犯第三方专利。', 'AFFIRMATIVE'),
    ('如第三方主张本技术侵权，乙方应通知甲方。', 'CONDITIONAL'),
    ('双方未发现第三方侵权。', 'NEGATED'),
    ('双方未明确约定侵权处理方式。', 'MISSING'),
    ('双方无法确认技术是否侵犯第三方专利。', 'MISSING'),
])
def test_shared_proposition_polarity(text, polarity):
    from review_v2.proposition_scope import scoped_propositions
    assert next(scoped_propositions(text))['polarity'] == polarity


BASE = '''技术秘密许可合同
甲方（许可方）许可乙方（被许可方）使用技术秘密。
第一条 第三方权利主张
如第三方主张乙方使用技术侵犯其知识产权，乙方应及时通知甲方。
如相关权利争议属于甲方签约前已经明确知悉而故意未披露的事项，由甲方承担因此给乙方造成的直接经济损失。
除此之外，双方未明确约定：
由哪一方负责诉讼、仲裁或者第三方交涉；
律师费、诉讼费、鉴定费等费用的承担；
是否可以未经另一方同意与第三方和解；
第三方权利主张发生后的具体通知期限。
'''


def test_absence_list_does_not_inherit_previous_actor_or_create_duties():
    claim = build_technology_fact_registry(BASE)['third_party_claim']
    facts = claim['response_element_evidence']
    for key in ('claim_handling', 'litigation_handling', 'attorney_fee', 'litigation_cost', 'claim_cost_allocation', 'notification_deadline', 'settlement_authority'):
        assert not facts.get(key), (key, facts.get(key))
    assert facts['notification_requirement']
    assert facts['damages_allocation'][0]['limited'] is True
    assert facts['damages_allocation'][0]['condition'].startswith('如相关权利争议')
    assert claim_requirement_entailment('claim_handling', '由哪一方负责诉讼、仲裁或者第三方交涉', BASE) is False


def test_affirmative_duty_after_absence_list_still_exists():
    claim = build_technology_fact_registry(BASE + '\n甲方应承担第三方侵权索赔的律师费及诉讼费。')['third_party_claim']
    facts = claim['response_element_evidence']
    assert facts['attorney_fee'] and facts['litigation_cost']
    assert all('甲方应承担' in row['quote'] for row in facts['attorney_fee'])


def test_actor_named_inside_absence_list_does_not_create_duty():
    text = ('技术秘密许可合同\n甲方许可乙方使用技术秘密。\n第一条 第三方索赔\n'
            '如第三方主张技术侵权，乙方应通知甲方。\n双方未明确约定：\n'
            '甲方承担第三方侵权索赔律师费；\n甲方负责第三方诉讼。')
    facts = build_technology_fact_registry(text)['third_party_claim']['response_element_evidence']
    assert not facts.get('attorney_fee')
    assert not facts.get('claim_handling')


def test_conditional_notification_is_not_fault_limited_liability():
    facts = build_technology_fact_registry(BASE)['third_party_claim']['response_element_evidence']
    row = facts['notification_requirement'][0]
    assert row['condition'].startswith('如第三方主张')
    assert row['limited'] is False


def test_report_element_preserves_fault_condition():
    from review_v2.engine import ReviewItemResult, _apply_exact_claim_response
    from review_v2.clause_parser import parse_contract_clauses
    item = ReviewItemResult(
        item_id='TC-12-02', node_id='test', title='第三方权利主张', risk_level='中',
        status='部分覆盖', coverage_status='部分覆盖', issue_type='PARTIAL',
        risk_point_description='', suggested_clause_example='', legal_basis_index='',
        legal_consequence_if_missing='', applicable_if='', matched_terms=[],
        evidence_clauses=[], evidence_location='', reasoning_summary='',
    )
    _apply_exact_claim_response(item, parse_contract_clauses(BASE), build_technology_fact_registry(BASE)['third_party_claim'])
    element = next(e for e in item.coverage_elements if e['element_id'] == 'damages_allocation')
    assert '如相关权利争议属于甲方签约前已经明确知悉而故意未披露的事项' in element['proposition']
    assert element['supporting_evidence'][0]['limited'] is True


def test_conditional_assistance_retains_its_own_limit():
    text = '技术秘密许可合同。许可方许可被许可方使用技术秘密。\n第一条 第三方索赔\n如第三方主张被许可方使用技术侵权，许可方仅提供必要技术协助。'
    facts = build_technology_fact_registry(text)['third_party_claim']['response_element_evidence']
    assert facts['claim_assistance'][0]['limited'] is True


@pytest.mark.parametrize('statement, adverse', [
    ('如第三方主张本技术侵权，乙方应及时通知甲方。', False),
    ('甲方确认该技术目前侵犯第三方专利。', True),
    ('甲方确认该技术目前侵犯第三方专利，双方未明确约定侵权处理方式。', True),
    ('甲方确认该技术未侵犯第三方专利。', False),
    ('甲方确认该技术不会侵犯第三方专利。', False),
    ('双方未发现第三方侵权。', False),
    ('双方未明确约定侵权处理方式。', False),
])
def test_infringement_polarity_through_final_report(statement, adverse):
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile
    text = BASE + '\n第二条 技术权利现状\n' + statement
    report = review_contract_v2(text, 'technology', use_llm=False,
                               profile=UserRiskProfile(user_identity='乙方/被许可方'))
    item = next(row for row in report['items'] if row['item_id'] == 'TC-02-02')
    assert item['coverage_status'] == ('风险条款' if adverse else '通过')
    assert item['decision_trace']['negative_clause_check']['adverse_clause_exists'] is adverse
    assert any(e['status'] == 'ADVERSE' for e in item['coverage_elements']) is adverse
    if adverse:
        proofs = [e for e in item['evidence_clauses'] if e.get('support_type') == 'DIRECT']
        assert proofs and all(has_actual_infringement(e.get('quote') or e.get('text', '')) for e in proofs)
        assert any(f['risk_group'] == item['risk_group'] for f in report['risk_findings'])
    assert not any(f.get('entity_id') == 'TC-02-02' or
                   any(d.get('review_id') == 'TC-02-02' for d in f.get('details', []))
                   for f in report['release_quality_gate']['failures'])


def test_non_actionable_party_gap_remains_visible_without_risk_recommendation():
    from review_v2.engine import ReviewItemResult, _build_narrative_state
    from review_v2.confidentiality_remedies import confidentiality_remedy_elements, party_narrative_failures
    item = ReviewItemResult(
        item_id='TC-11-04', node_id='test', title='泄密救济', risk_level='中',
        status='缺失', coverage_status='缺失', issue_type='MISSING',
        risk_point_description='', suggested_clause_example='', legal_basis_index='',
        legal_consequence_if_missing='', applicable_if='', matched_terms=[],
        evidence_clauses=[], evidence_location='', reasoning_summary='',
    )
    item.coverage_elements = confidentiality_remedy_elements([])
    state = _build_narrative_state(item)
    assert '责任方泄密损失赔偿责任' in state['missing_elements']
    assert '文本完整性记录' in state['judgment']
    assert '责任方泄密损失赔偿责任' not in state['recommendation']
    assert not party_narrative_failures(item.coverage_elements, state, state['recommendation'])
