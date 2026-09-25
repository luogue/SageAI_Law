import pytest
from backend.tests.test_employment_fact_pipeline import fact, packet, verified_packet
from review_v2.clause_parser import parse_contract_clauses


def review(monkeypatch, text, values):
    from review_v2 import employment_fact_pipeline as pipeline
    from review_v2.engine import review_contract_v2
    cs = parse_contract_clauses(text)
    monkeypatch.setattr(pipeline, 'extract', lambda *a, **k: packet(cs, [fact(cs, c, v, q) for c, v, q in values]))
    monkeypatch.setattr(pipeline, 'verify', verified_packet)
    result = review_contract_v2(text, 'labor')
    assert result['release_quality_gate']['status'] == 'REPORT_READY', result['release_quality_gate']
    return {r['item_id']: r for r in result['items']}


@pytest.mark.parametrize('concept,value,quote,status', [
 ('social_insurance.statutory_duties', True, '社会保险依法办理，单位应承担的法定义务不得免除。', '部分覆盖'),
 ('part_time.injury_insurance', True, '用人单位依法缴纳工伤保险。', '通过'),
 ('part_time.injury_insurance', False, '劳动者自行承担工伤风险，单位不缴工伤保险。', '风险条款'),
 ('social_insurance.cash_replacement', True, '由现金补贴替代单位社会保险缴纳义务。', '风险条款'),
 (None, None, '双方约定其他事项。', '缺失'),
])
def test_insurance_grading(monkeypatch, concept, value, quote, status):
    text = '非全日制劳动合同\n双方建立非全日制关系。\n' + quote
    values = [('contract.employment_form', 'PART_TIME', '双方建立非全日制关系。')]
    if concept: values.append((concept, value, quote))
    item = review(monkeypatch, text, values)['PT-04-01']
    assert item['coverage_status'] == status
    if status in {'部分覆盖', '缺失'}:
        assert item['risk_level'] == '低'
        assert item['action_priority'] == 'C_OPTIMIZATION'


@pytest.mark.parametrize('hazard,excluded,measures', [(False, False, True), (True, False, False), (False, True, True)])
def test_safety_training_scale(monkeypatch, hazard, excluded, measures):
    text = '劳动合同\n单位提供安全办公条件。\n岗位存在职业危害，需要专门安全培训。\n单位排除必要安全培训。\n岗位不存在职业危害。'
    values = [('labor_protection.hazard_exists', hazard, '岗位存在职业危害，需要专门安全培训。' if hazard else '岗位不存在职业危害。')]
    if measures: values.append(('labor_protection.measures', '安全办公条件', '单位提供安全办公条件。'))
    if excluded: values.append(('labor_protection.training_excluded', True, '单位排除必要安全培训。'))
    item = review(monkeypatch, text, values)['EMP-08-01']
    if excluded: assert item['coverage_status'] == '风险条款'
    elif hazard: assert item['coverage_status'] in {'缺失', '部分覆盖', '待核验'}
    else: assert item['coverage_status'] == '通过'
