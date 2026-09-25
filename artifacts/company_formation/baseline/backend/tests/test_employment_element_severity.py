"""Severity follows missing elements, not the insurance topic's maximum rating."""
import pytest
from test_employment_fact_semantics import review, item
from review_v2.report_statistics import statistics_gate


@pytest.mark.parametrize('core', [
    '用人单位依法按月缴纳社会保险。',
    '社会保险缴纳主体：远川技术有限公司。',
    '社会保险参保地：杭州市。社会保险缴纳主体：海舟服务有限公司。社会保险项目：养老、医疗、失业、工伤、生育。',
])
def test_withholding_only_gap_is_optional(core):
    result = review(core)
    row = item(result, 'EMP-07-01')
    assert row['coverage_status'] == '通过'
    assert row['risk_severity'] == 'NONE'
    assessment = row['decision_trace']['element_severity_assessment']
    assert assessment['theme_default_level'] == '高'
    assert assessment['selected_level'] == '低'
    assert assessment['elements'][0]['source_clause_ids']
    assert assessment['elements'][1]['status'] == 'MISSING'
    assert row['coverage_elements'][1]['risk_relevant'] is False
    assert not any('EMP-07-01' in f['source_review_ids'] for f in result['risk_findings'])
    assert result['release_quality_gate']['status'] == 'REPORT_READY'
    assert statistics_gate(result)['status'] == 'REPORT_READY'


@pytest.mark.parametrize('source', [
    '双方依法履行劳动合同。',
    '社会保险参保地：杭州市。社会保险项目：养老、医疗、失业、工伤、生育。',
    '劳动者个人应缴部分由甲方代扣代缴。',
])
def test_missing_employer_obligation_does_not_inherit_detail_downgrade(source):
    result = review(source)
    row = item(result, 'EMP-07-01')
    assert row['risk_level'] == '高' and row['risk_severity'] == 'HIGH'
    assert row['decision_trace']['element_severity_assessment']['elements'][0]['status'] == 'MISSING'
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


def test_express_illegal_waiver_remains_high_despite_positive_coverage():
    result = review('用人单位依法按月缴纳社会保险。劳动者自愿放弃社会保险。')
    assert item(result, 'EMP-07-01')['risk_severity'] == 'HIGH'
    assert item(result, 'EMP-13-01')['risk_severity'] == 'HIGH'
    finding = next(f for f in result['risk_findings'] if 'EMP-13-01' in f['source_review_ids'])
    assert finding['severity'] == 'HIGH'
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


def test_complete_insurance_pass_and_no_risk_finding():
    result = review('用人单位依法按月缴纳社会保险。劳动者个人应缴部分由用人单位代扣代缴。')
    assert item(result, 'EMP-07-01')['coverage_status'] == '通过'
    assert not any('EMP-07-01' in f['source_review_ids'] for f in result['risk_findings'])


def test_absent_submitted_clauses_remain_actual_gaps():
    result = review('标准工时，每周至少休息一天。派遣期限届满，甲方另行安排合法的劳务派遣岗位。')
    assert item(result, 'EMP-05-01')['coverage_status'] == '通过'
    assert item(result, 'EMP-05-01')['risk_severity'] == 'NONE'
    assert item(result, 'EMP-10-01')['coverage_status'] == '通过'
    assert item(result, 'EMP-10-01')['coverage_elements'][1]['risk_relevant'] is False
    assert item(result, 'EMP-11-01')['coverage_status'] == '缺失'
    assert result['release_quality_gate']['status'] == 'REPORT_READY'
