import pytest
from tests.test_employment_fact_semantics import review, item


@pytest.mark.parametrize('text,rule,index', [
    ('乙方（劳动者）：林川\n身份证号码：420***8632', 'EMP-01-01', 1),
    ('试用期为一个月。试用期工资为正式工资标准的85%，即人民币7,650元/月。', 'EMP-03-01', 1),
    ('甲方依法为员工办理社会保险及住房公积金。', 'EMP-07-01', 0),
    ('竞业限制地域限于江苏省。乙方不得为竞争企业从事同类的医疗器械、物流系统相关业务。', 'NC-01-01', 1),
    ('竞业限制地域限于江苏省。乙方不得为竞争企业从事同类的医疗器械、物流系统相关业务。', 'NC-01-01', 2),
    ('竞业限制：劳动合同解除或终止后一年内，乙方不得从事同类业务。', 'NC-02-01', 0),
])
def test_final_report_recalls_existing_elements(text, rule, index):
    if rule.startswith('NC-'):
        text = '双方约定乙方离职后承担竞业限制义务。\n' + text
    result = review(text)
    row = item(result, rule)
    element = row['coverage_elements'][index]
    assert element['status'] == 'COVERED'
    assert any(e.get('verified_original') for e in row['evidence_clauses'])
    audits = row['decision_trace'].get('element_absence_searches', [])
    assert not any(a['element_id'] == element['element_id'] and a['result'] == 'NOT_FOUND' for a in audits)
