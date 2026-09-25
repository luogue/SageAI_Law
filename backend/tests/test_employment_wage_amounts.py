"""Wage propositions survive extraction, binding and final coverage."""
import pytest
from review_v2.engine import review_contract_v2


@pytest.mark.parametrize('clause,covered', [
    ('月薪为人民币12,700元。', True),
    ('月正常工作时间工资为人民币21,500元，其中基本工资10,000元/月；岗位工资7,000元/月；绩效工资4,500元/月，绩效部分根据考核浮动。', True),
    ('基本工资为7200元/月；岗位工资为2300元/月；绩效工资按考核浮动。', True),
    ('计件工资按每件人民币16.50元计算，按实际合格件数结算。', True),
    ('计件单价：25元/套，按完成套数结算。', True),
    ('工资按公司制度执行。', False),
    ('计件工资按公司制度执行。', False),
    ('试用期月工资为人民币6,500元。', False),
])
def test_wage_amount_end_to_end(clause, covered):
    result = review_contract_v2('劳动合同\n第五条 ' + clause + '\n每月12日前通过银行转账支付工资。', 'labor', use_llm=False)
    row = next(i for i in result['items'] if i['item_id'] == 'EMP-06-01')
    amount = next(e for e in row['coverage_elements'] if e['element_id'] == 'employment_wage_1')
    assert amount['status'] == ('COVERED' if covered else 'MISSING')
    if covered:
        assert row['coverage_status'] == '通过'
        assert amount['evidence_refs'] and amount['supporting_evidence']
        assert all(e['quote'] in '劳动合同\n第五条 ' + clause + '\n每月12日前通过银行转账支付工资。' for e in amount['supporting_evidence'])
        assert not any(a.get('element_id') == 'employment_wage_1' and a.get('result') == 'NOT_FOUND' for a in row['decision_trace'].get('element_absence_searches', []))
