import pytest
from review_v2.engine import review_contract_v2


def row(text, rule):
    result = review_contract_v2('劳动合同\n' + text, 'labor', use_llm=False)
    return next(i for i in result['items'] if i['item_id'] == rule)


@pytest.mark.parametrize('text,status', [
    ('甲方依法支付加班工资。', 'COVERED'),
    ('实行标准工时制度。', 'MISSING'),
    ('乙方自愿放弃加班费。', 'ADVERSE'),
    ('加班时间原则上不再另行支付加班工资。', 'ADVERSE'),
    ('月工资已经包含加班费。', 'ADVERSE'),
])
def test_overtime_polarity(text, status):
    r = row(text, 'EMP-05-01')
    if status == 'ADVERSE':
        assert r['coverage_status'] == '风险条款'
        assert not any(e['element_id'] == 'employment_hours_3' and e['status'] == 'COVERED' for e in r['coverage_elements'])
    else:
        element = next(e for e in r['coverage_elements'] if e['element_id'] == 'employment_hours_3')
        assert element['status'] == status


@pytest.mark.parametrize('text', ['劳动争议可依法申请劳动争议仲裁。', '协商不成可以申请仲裁。', '争议向劳动仲裁委员会提交。', '双方可依法提起劳动仲裁。'])
def test_arbitration_synonyms(text):
    assert row(text, 'EMP-12-01')['coverage_status'] == '通过'


def test_exit_exists_even_with_restriction():
    r = row('乙方主动辞职，应提前45日通知。未经甲方批准，乙方不得自行离职。严重违反公司规章制度的，甲方可以解除劳动合同。', 'EMP-10-01')
    assert r['coverage_status'] == '风险条款'
    assert r['coverage_elements'][0]['status'] != 'MISSING'


def test_business_scope_independent_of_geography():
    r = row('乙方承诺履行竞业限制。离职后不得在与甲方存在竞争关系的企业任职，包括从事医疗器械、工业机器人业务的企业。', 'NC-01-01')
    statuses = {e['element_id']:e['status'] for e in r['coverage_elements']}
    assert statuses['employment_noncompete_scope_2'] == 'COVERED'
    assert statuses['employment_noncompete_scope_3'] == 'MISSING'


@pytest.mark.parametrize('verb', ['签署', '签订', '订立'])
def test_future_training_not_current_duty(verb):
    assert row(f'如提供专项培训，双方可以另行{verb}培训服务期协议。', 'EMP-09-01')['coverage_status'] == '不适用'


def test_actual_training_duty_still_applies():
    assert row('甲方承担专项培训费用，乙方承诺服务三年，服务期为三年。', 'EMP-09-01')['coverage_status'] != '不适用'


def test_earned_wage_withholding_reuses_existing_risk():
    r = row('月工资为12500元。每月10日前银行转账支付工资。乙方未完成交接时，甲方有权暂缓办理离职手续及支付尚未结算工资。', 'EMP-06-01')
    assert r['coverage_status'] == '风险条款'
    assert r['coverage_elements'][0]['status'] != 'MISSING'


def test_probation_evidence_excludes_other_topics():
    r = row('合同期限自2027年1月1日至2028年12月31日。试用期自2027年1月1日至2027年3月31日。\n试用期工资为9000元。\n试用期内依法缴纳社会保险。', 'EMP-15-01')
    assert r['coverage_status'] == '风险条款'
    quotes = [e.get('text','') for e in r['evidence_clauses']]
    assert quotes and not any('工资' in q or '社会保险' in q for q in quotes)
