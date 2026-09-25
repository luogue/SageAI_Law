"""Final-model regression for compositional positive evidence retrieval."""
import pytest

from tests.test_employment_fact_semantics import review, item


@pytest.mark.parametrize('amount', ['9,250', '11，640.50', '8700'])
def test_salary_modifiers_and_separate_payment_clause(amount):
    result = review(
        f'第一条 试用期\n试用期为一个月。乙方试用期税前固定工资为人民币{amount}元/月。\n'
        f'第二条 薪酬\n转正后固定工资为{amount}元/月。\n'
        '第三条 支付\n工资每月12日支付，通过银行转账。')
    for rule, index in [('EMP-03-01', 1), ('EMP-06-01', 0)]:
        row = item(result, rule)
        element = row['coverage_elements'][index]
        assert element['status'] == 'COVERED'
        assert any(e.get('verified_original') for e in row['evidence_clauses'])
        assert not any(a.get('element_id') == element['element_id'] and a.get('result') == 'NOT_FOUND'
                       for a in row['decision_trace'].get('element_absence_searches', []))


@pytest.mark.parametrize('insurance', [
    '用人单位为劳动者办理社会保险手续，并依法缴纳保险费用。',
    '甲方按当地规定办理养老保险、医疗保险、失业保险、工伤保险、生育保险等社会保险手续，并依法缴纳应由甲方承担的费用。',
])
def test_insurance_enrollment_and_employer_payment(insurance):
    assert item(review(insurance), 'EMP-07-01')['coverage_elements'][0]['status'] == 'COVERED'


def test_conditional_statutory_compensation_is_not_absent():
    result = review('第八条 解除及结算\n符合法律规定应当支付经济补偿或赔偿的，用人单位依法支付。')
    row = item(result, 'EMP-11-01')
    assert row['coverage_elements'][0]['status'] == 'COVERED'
    assert row['coverage_status'] == '部分覆盖'
    assert any(e.get('verified_original') for e in row['evidence_clauses'])


def test_protection_does_not_cover_training():
    row = item(review('甲方建立职业健康及劳动保护制度。'), 'EMP-08-01')
    assert row['coverage_status'] == '部分覆盖'
    assert row['coverage_elements'][0]['status'] == 'COVERED'
    assert next(e for e in row['coverage_elements'] if e['element_id'] == 'employment_safety_training')['status'] == 'MISSING'


def test_training_does_not_replace_protection():
    row = item(review('甲方定期开展安全培训。'), 'EMP-08-01')
    assert row['coverage_elements'][0]['status'] == 'MISSING'
    assert next(e for e in row['coverage_elements'] if e['element_id'] == 'employment_safety_training')['status'] == 'COVERED'
