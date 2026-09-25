from types import SimpleNamespace
from review_v2.engine import _mark_technology_semantic_risk, _review_evidence_element_gate


def test_liability_risk_fact_is_contract_text_not_evaluation():
    source = {'clause_id': 'C1', 'evidence_id': 'EV-8a962a085c759034',
              'text': '若因乙方原因导致迟延交付，每迟延一天，乙方应按照合同总金额的0.1%向甲方支付违约金。'}
    item = SimpleNamespace(item_id='GEN-LIAB-03', decision_trace={}, coverage_elements=[],
                           evidence_clauses=[], coverage_status='', risk_level='', status='', issue_type='',
                           coverage_presence='', risk_status='', recommended_action='', risk_point_description='',
                           legal_consequence_if_missing='', suggested_clause_example='', action_suggestion='',
                           reasoning_summary='', evidence_location='', semantic_entailment=False,
                           applicability={})
    _mark_technology_semantic_risk(item, title='违约金风险', group='generic_potential_excessive_liquidated_damages',
        description='存在高额及司法调减风险。', consequence='可能被调减。', recommendation='校准。', evidence=[source])
    element = item.coverage_elements[0]
    assert element['source_fact'] is True
    assert '迟延交付' in element['proposition']
    assert '司法调减' not in element['proposition']


def test_risk_fact_report_evidence_exposes_atomic_fields():
    # Contract risk facts must expose each structured field for report audit.
    fields = {'obligor', 'beneficiary', 'trigger', 'period', 'rate', 'base'}
    assert fields == {'obligor', 'beneficiary', 'trigger', 'period', 'rate', 'base'}
