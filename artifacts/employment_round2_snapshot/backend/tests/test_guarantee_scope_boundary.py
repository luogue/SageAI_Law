import pytest
from review_v2.engine import review_contract_v2
from review_v2.clause_parser import parse_contract_clauses
from review_v2.guarantee_scope import scope_evidence


@pytest.mark.parametrize('body, covered', [
    ('保证本金人民币800000元，利息最高人民币40000元，最高保证金额人民币840000元。超出保证金额及保证期限的款项，保证人不承担责任。', True),
    ('保证本金人民币2000000元，利息最高人民币120000元，最高保证额人民币2120000元。', True),
    ('保证范围为本金、利息、违约金及实现债权费用，保证人全部承担。', True),
    ('保证人承担担保责任。', False),
    ('保证人代偿后有权向借款人追偿本金、利息、违约金及实现债权费用，借款人全部承担。', False),
])
def test_scope_boundary_production(body, covered):
    report = review_contract_v2('保证合同\n保证人承担一般保证责任。' + body, 'guarantee', use_llm=False)
    row = next(r for r in report['items'] if r['item_id'] == 'GUA-07-04')
    assert (row['coverage_status'] == '通过') == covered
    if covered:
        assert row['evidence_clauses']
        assert all(e['source_type'] == 'SOURCE_CLAUSE' for e in row['evidence_clauses'])
        assert not row['suggested_clause_example']


def test_recoursing_costs_cannot_support_scope():
    assert not scope_evidence(parse_contract_clauses('保证人承担保证责任后，有权追偿律师费、诉讼费及实现债权费用。'))
