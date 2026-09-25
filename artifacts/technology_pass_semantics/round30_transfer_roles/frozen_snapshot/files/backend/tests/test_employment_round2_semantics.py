"""User-quoted clauses are test inputs, never silently appended to the DOCX."""
from copy import deepcopy
import json
import pytest

from test_employment_fact_semantics import review, item
from review_v2.report_state_consistency import report_state_consistency_failures
from review_v2.report_statistics import statistics_gate


@pytest.mark.parametrize('wage_clause', ['依法安排乙方补休或支付加班工资', '甲方依法安排劳动者调休或支付加班工资'])
def test_overtime_payment_alternative_is_covered(wage_clause):
    result = review('标准工时，每周至少休息一天。\n第六条 ' + wage_clause + '。')
    row = item(result, 'EMP-05-01')
    assert row['coverage_status'] == '通过'
    assert all(a['result'] == 'FOUND' for a in row['decision_trace'].get('element_absence_searches', []))
    assert not any(e.get('source_type') == 'SEARCH_AUDIT' for e in row['evidence_clauses'])
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


@pytest.mark.parametrize('dispute', ['进行协商、申请调解或仲裁', '双方依法申请仲裁'])
def test_labor_dispute_arbitration_alternative(dispute):
    result = review('第二十四条 劳动争议可' + dispute + '。')
    assert item(result, 'EMP-12-01')['coverage_status'] == '通过'
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


def test_exit_statutory_procedure_without_notice_date_passes_core_rule():
    source = '第二十条 劳动合同依法变更。\n第二十一条 解除或终止按照法律法规执行。\n第二十二条 甲方出具解除终止证明，15日内办理档案和社保关系转移。'
    result = review(source)
    row = item(result, 'EMP-10-01')
    assert row['coverage_status'] == '通过'
    assert row['coverage_elements'][0]['status'] == 'COVERED'
    optional = row['coverage_elements'][1]
    assert optional['status'] == 'MISSING'
    assert optional['risk_relevant'] is False
    assert not any('EMP-10-01' in f['source_review_ids'] for f in result['risk_findings'])
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


def test_compensation_lawful_basis_and_handover_settlement_are_sufficient():
    source = '第二十三条 甲方依法应向乙方支付经济补偿的，在办结工作交接时支付。'
    result = review(source)
    row = item(result, 'EMP-11-01')
    assert row['coverage_status'] == '通过'
    assert row['coverage_elements'][1]['status'] == 'COVERED'
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


def test_compensation_lawful_basis_without_settlement_deadline_passes_core_rule():
    result = review('解除终止符合法定经济补偿情形的，甲方依法向乙方支付经济补偿。')
    row = item(result, 'EMP-11-01')
    assert row['coverage_status'] == '通过'
    assert row['coverage_elements'][0]['status'] == 'COVERED'
    optional = row['coverage_elements'][1]
    assert optional['status'] == 'MISSING'
    assert optional['risk_relevant'] is False
    assert not any('EMP-11-01' in f['source_review_ids'] for f in result['risk_findings'])
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


@pytest.mark.parametrize('source,rule', [
    ('甲方可以随时解除本合同。', 'EMP-10-01'),
    ('甲方无需支付经济补偿。', 'EMP-11-01'),
])
def test_exit_and_compensation_direct_adverse_terms_still_hit_risk(source, rule):
    result = review(source)
    row = item(result, rule)
    assert row['coverage_status'] == '风险条款'
    assert row['evidence_clauses']
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


def test_negative_pass_cannot_pollute_positive_insurance_bundle():
    result = review('社会保险缴纳主体：川海技术有限公司。')
    negative = item(result, 'EMP-13-01')
    assert negative['coverage_status'] == '通过'
    assert negative['coverage_elements'] == [] and negative['related_risks'] == []
    assert negative['decision_trace']['negative_clause_check']['query_semantics'] == 'ADVERSE_CLAUSE_SEARCH'
    assert negative['decision_trace']['negative_clause_check']['description'] == '未发现对应禁止性/不利约定。'
    for finding in result['risk_findings']:
        assert 'EMP-13-01' not in finding['source_review_ids']
        assert '免除或放弃法定社会保险义务' not in json.dumps(finding, ensure_ascii=False)
    summary = result['result'].split('## 二、核心风险摘要', 1)[1].split('\n## ', 1)[0]
    assert '免除或放弃法定社会保险义务' not in summary
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


def test_gate_blocks_reintroduced_negative_pass_contamination():
    result = review('社会保险缴纳主体：川海技术有限公司。')
    findings = deepcopy(result['risk_findings'])
    findings[0]['source_review_ids'].append('EMP-13-01')
    failures = report_state_consistency_failures(result['items'], findings)
    assert any(f.get('reason') == 'NEGATIVE_PASS_AGGREGATION_CONTAMINATION' for f in failures)


def test_severity_and_action_counts_match_detail_and_explanation():
    result = review('社会保险缴纳主体：川海技术有限公司。')
    assert statistics_gate(result)['status'] == 'REPORT_READY'
    high = [d for d in result['final_dispositions'] if d['severity'] in {'HIGH', 'CRITICAL'}]
    for disposition in high:
        if disposition['final_action'] != 'MUST_CHANGE':
            assert disposition['downgrade_reason']
            assert '处理次序说明' in result['result']
    # This short input also lacks identities and wages; those may remain high.
    assert not any('EMP-07-01' in d['review_ids'] for d in high)
    assert '严重程度：中等风险' in result['result']
