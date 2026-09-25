"""Core statutory arrangements versus optional detail and actual overrides."""
import pytest
from test_employment_fact_semantics import review, item
from review_v2.report_statistics import statistics_gate


@pytest.mark.parametrize('source,rule', [
    ('甲乙双方按国家和浙江省的规定参加社会保险。', 'EMP-07-01'),
    ('甲方依法缴纳社会保险。', 'EMP-07-01'),
    ('如需支付经济补偿，则甲方在乙方工作交接结束后支付。', 'EMP-11-01'),
    ('经济补偿由甲方在办结工作交接时支付。', 'EMP-11-01'),
    ('甲方依法向乙方支付经济补偿。', 'EMP-11-01'),
])
def test_statutory_core_without_repeated_details_has_no_actual_risk(source, rule):
    result = review(source)
    row = item(result, rule)
    assert row['coverage_status'] == '通过'
    assert row['risk_severity'] == 'NONE'
    assert row['action_priority'] == 'NONE'
    assert not row['related_risks']
    assert not any(rule in f['source_review_ids'] for f in result['risk_findings'])
    assert result['release_quality_gate']['status'] == 'REPORT_READY'
    assert statistics_gate(result)['status'] == 'REPORT_READY'


@pytest.mark.parametrize('adverse', [
    '甲方不缴纳社会保险。',
    '甲方少缴社会保险。',
    '甲方应缴社会保险费用由乙方自行承担。',
    '社会保险单位应缴部分由劳动者全部承担。',
    '劳动者自愿放弃社会保险。',
])
def test_insurance_adverse_overrides_lawful_core(adverse):
    result = review('甲方依法缴纳社会保险。' + adverse)
    row = item(result, 'EMP-07-01')
    assert row['coverage_status'] == '风险条款'
    assert row['related_risks']
    assert any(adverse in e['text'] for e in row['evidence_clauses'])
    assert not row['narrative_state']['missing_elements']
    assert result['release_quality_gate']['status'] == 'REPORT_READY'
    findings = [f for f in result['risk_findings'] if {'EMP-07-01', 'EMP-13-01'} & set(f['source_review_ids'])]
    assert len(findings) == 1


@pytest.mark.parametrize('adverse', [
    '甲方不支付经济补偿。',
    '乙方放弃法定经济补偿。',
    '经济补偿低于法定标准。',
    '经济补偿按法定标准的50%支付。',
    '甲方仅支付法定经济补偿的一半。',
    '经济补偿在离职后六个月后支付。',
])
def test_compensation_adverse_overrides_normal_settlement(adverse):
    result = review('经济补偿由甲方在办结工作交接时支付。' + adverse)
    row = item(result, 'EMP-11-01')
    assert row['coverage_status'] == '风险条款'
    assert row['related_risks']
    assert all(e['status'] == 'ADVERSE' for e in row['coverage_elements'])
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


@pytest.mark.parametrize('protection,rule', [
    ('甲方不得少缴社会保险。', 'EMP-07-01'),
    ('甲方不得免除经济补偿。', 'EMP-11-01'),
    ('乙方不得放弃经济补偿。', 'EMP-11-01'),
    ('经济补偿不低于法定标准。', 'EMP-11-01'),
])
def test_prohibition_of_adverse_act_not_itself_adverse(protection, rule):
    row = item(review('甲方依法缴纳社会保险。甲方依法支付经济补偿。' + protection), rule)
    assert row['coverage_status'] == '通过'
    assert not row['related_risks']


@pytest.mark.parametrize('context', ['', '乙方从事办公室文书工作。', '本岗位不存在职业病危害因素。'])
def test_general_safety_absence_remains_actionable(context):
    result = review(context or '双方签订劳动合同。')
    row = item(result, 'EMP-08-01')
    assert row['coverage_status'] == '缺失'
    assert row['action_priority'] == 'B_PRACTICAL'
    assert row['decision_trace']['coverage_gap_type'] == 'MISSING_REQUIRED_CONTRACT_TERM'
    assert row['related_risks']
    assert result['release_quality_gate']['status'] == 'REPORT_READY'
    if '不存在' in context:
        assert row['coverage_elements'][1]['status'] == 'NOT_APPLICABLE'
        assert row['coverage_elements'][0]['status'] == 'MISSING'


def test_general_safety_present_without_occupational_hazard_passes():
    row = item(review('甲方提供劳动防护用品并开展安全培训。本岗位不存在职业病危害因素。'), 'EMP-08-01')
    assert row['coverage_status'] == '通过'
    assert row['action_priority'] == 'NONE'
