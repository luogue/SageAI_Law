"""Independent phrasing/amount/date variants, plus production pipeline invariants."""
from functools import lru_cache
from types import SimpleNamespace
import json

import pytest

from review_v2.contract_registry import get_checklist
from review_v2.clause_parser import parse_contract_clauses
from review_v2.priority_contract_review import judge, probation_risk
# Retain the lexical evaluator baseline during migration. Public production
# entry/fact-store behavior is exercised in test_employment_fact_pipeline.
from review_v2.engine import _review_contract_v2_legacy as review_contract_v2, _enforce_applicability_status_invariant


def checkpoint(rule):
    return next(c for c in get_checklist('labor') if c.item_id == rule)


@lru_cache(maxsize=None)
def review(text):
    return review_contract_v2('劳动合同\n' + text, 'labor', use_llm=False)


def item(result, rule):
    return next(i for i in result['items'] if i['item_id'] == rule)


@pytest.mark.parametrize('amount', [7600, 12800, 19500])
def test_structured_wage_facts_pass_without_negative_amount_audit(amount):
    result = review(f'工资支付日：每月12日前\n月正常工作时间工资：{amount}元/月\n试用期月正常工作时间工资：6500元/月\n工资支付方式：银行转账')
    wage = item(result, 'EMP-06-01')
    assert wage['coverage_status'] == '通过'
    assert all(e['status'] == 'COVERED' for e in wage['coverage_elements'])
    audits = wage['decision_trace'].get('element_absence_searches', [])
    assert not any(a.get('element_id') == 'employment_wage_1' and a.get('result') == 'NOT_FOUND' for a in audits)
    assert '未找到工资金额' not in result['result']
    assert not any(e.get('source_type') == 'SEARCH_AUDIT' for e in wage['evidence_clauses'])
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


def test_trial_wage_cannot_substitute_for_normal_wage():
    wage = item(review('试用期月正常工作时间工资：6500元/月\n工资支付方式：银行转账'), 'EMP-06-01')
    assert wage['coverage_status'] == '部分覆盖'
    assert wage['coverage_elements'][0]['status'] == 'MISSING'


@pytest.mark.parametrize('employer,worker', [('青禾技术有限公司', '李思宁'), ('远川服务企业', '王安')])
def test_parenthesized_identity_with_intervening_fields(employer, worker):
    source = (f'甲方（劳务派遣单位）：{employer}\n统一社会信用代码：91310000123456789X\n'
              f'法定代表人：赵文\n注册地：杭州市西湖区文一路36号\n乙方（劳动者）：{worker}\n居民身份证号码：330100199507080019')
    assert item(review(source), 'EMP-01-01')['coverage_status'] == '通过'


def test_other_party_address_does_not_cover_employer_address():
    source = '甲方（劳务派遣单位）：青禾技术有限公司\n乙方（劳动者）：李思宁\n居民身份证号码：330100199507080019\n住所：杭州市西湖区文一路36号'
    assert item(review(source), 'EMP-01-01')['coverage_status'] == '部分覆盖'


@pytest.mark.parametrize('dates', [
    '自2027年4月1日起至2027年5月31日止',
    '自2028-01-01至2028-02-29',
])
def test_probation_dates_and_normal_worktime_wage_are_positive_evidence(dates):
    source = '试用期：\n' + dates + '\n试用期月正常工作时间工资：9100元/月'
    assert item(review(source), 'EMP-03-01')['coverage_status'] == '通过'


@pytest.mark.parametrize('term,trial,expected', [
    ('2027-04-01至2030-03-31', '2027-04-01至2027-09-30', False),
    ('2027-04-01至2030-03-31', '2027-04-01至2027-10-01', True),
    ('2027-04-01至2028-03-31', '2027-04-01至2027-06-01', True),
    ('2027-04-01至2028-03-31', '2027-04-01至2027-05-31', False),
    ('2027-04-01至2027-06-30', '2027-04-01至2027-04-30', False),
])
def test_calendar_probation_boundaries(term, trial, expected):
    assert probation_risk(f'劳动合同期限：自{term}\n试用期：自{trial}') is expected


def test_mixed_term_format_and_preventive_probation_text():
    assert probation_risk('劳动合同期限为一年。试用期：自2027年1月1日至2027年3月31日')
    assert not probation_risk('双方不得约定试用期为八个月。')


@pytest.mark.parametrize('rule,adverse,protective', [
    ('EMP-13-01', '劳动者自愿放弃社会保险。', '不得要求劳动者自愿放弃社会保险。'),
    ('EMP-14-01', '劳动者辞职须支付违约金5000元。', '不得约定劳动者辞职须支付违约金5000元。'),
    ('EMP-15-01', '双方再次约定试用期。', '双方不得再次约定试用期。'),
    ('EMP-16-01', '甲方可以随时解除劳动合同且无需支付经济补偿。', '不得约定甲方可以随时解除劳动合同且无需支付经济补偿。'),
])
def test_all_employment_prohibitions_share_negative_semantics(rule, adverse, protective):
    cp = checkpoint(rule)
    assert cp.kind == 'forbidden' and cp.polarity == 'NEGATIVE_CLAUSE_CHECK'
    for text, status in [('双方依法履行劳动合同。', '通过'), (protective, '通过'), (adverse, '风险条款')]:
        judgment = judge(cp, parse_contract_clauses(text))
        assert judgment.coverage_status == status
        result = review(text)
        row = item(result, rule)
        assert row['coverage_status'] == status
        assert row['decision_trace']['review_polarity'] == 'NEGATIVE_CLAUSE_CHECK'
        if status == '风险条款':
            assert row['related_risks']
            assert set(row['related_risks']) <= {f['finding_id'] for f in result['risk_findings']}
        assert result['release_quality_gate']['status'] == 'REPORT_READY', result['release_quality_gate']['failures']


def test_insurance_core_passes_with_or_without_withholding_detail():
    source = '社会保险参保地：杭州市\n社会保险缴纳主体：青禾技术有限公司\n社会保险项目：养老、医疗、失业、工伤、生育'
    assert item(review(source), 'EMP-07-01')['coverage_status'] == '通过'
    assert item(review(source + '\n劳动者个人应缴部分由甲方代扣代缴。'), 'EMP-07-01')['coverage_status'] == '通过'


@pytest.mark.parametrize('absence', ['本岗位不属于存在职业病危害因素的岗位', '本岗位不存在职业病危害因素', '无职业危害'])
def test_hazard_absence_is_element_na_not_missing(absence):
    result = review('提供必要防护用品，开展安全培训。\n' + absence)
    safety = item(result, 'EMP-08-01')
    assert safety['coverage_status'] == '通过'
    health = next(e for e in safety['coverage_elements'] if e['element_id'] == 'employment_safety_2')
    assert health['status'] == 'NOT_APPLICABLE'
    assert health['prerequisite_status'] == 'FALSE' and health['prerequisite_evidence']
    assert result['release_quality_gate']['status'] == 'REPORT_READY'
    assert not any(a.get('element_id') == health['element_id'] for a in safety['decision_trace'].get('element_absence_searches', []))


def test_hazard_trigger_preserves_general_safety_and_required_health_review():
    result = review('提供必要防护用品，开展安全培训。\n本岗位存在职业病危害因素。')
    safety = item(result, 'EMP-08-01')
    assert safety['coverage_status'] == '部分覆盖'
    health = next(e for e in safety['coverage_elements'] if e['element_id'] == 'employment_safety_2')
    assert health['status'] == 'MISSING' and health['prerequisite_status'] == 'TRUE'
    no_general = item(review('本岗位不存在职业病危害因素。'), 'EMP-08-01')
    assert no_general['coverage_status'] == '缺失'


@pytest.mark.parametrize('rule', ['EMP-13-01', 'EMP-14-01', 'EMP-15-01', 'EMP-16-01'])
def test_applicable_negative_search_cannot_be_repaired_as_positive_absence(rule):
    # Exercise the actual invariant with a late stale N/A projection.
    row = SimpleNamespace(**item(review('双方依法履行劳动合同。'), rule))
    row.coverage_status = '不适用'
    _enforce_applicability_status_invariant([row])
    assert row.coverage_status == '通过'
    assert '未发现' in row.reasoning_summary and '缺失' not in row.reasoning_summary


def test_gate_preserves_exact_failed_review_diagnostics():
    from review_v2.engine import _applicability_polarity_gates
    rows = []
    for rule in ['EMP-15-01', 'EMP-16-01']:
        row = SimpleNamespace(**item(review('双方依法履行劳动合同。'), rule))
        row.coverage_status = '不适用'
        rows.append(row)
    gate = _applicability_polarity_gates(rows, [], [])
    failure = next(f for f in gate['failures'] if f['requirement'] == 'NOT_APPLICABLE_NARRATIVE_GATE')
    assert len(failure['reviews']) == 2
    for diagnostic, row in zip(failure['reviews'], rows):
        assert diagnostic['rule_id'] == row.item_id
        assert diagnostic['polarity'] == 'NEGATIVE_CLAUSE_CHECK'
        assert diagnostic['applicability'] == 'APPLICABLE'
        assert diagnostic['expected_status'] == 'PASS'
        assert diagnostic['actual_status'] == '不适用'
        assert diagnostic['violation_reason'] == 'ALWAYS_APPLICABLE_RULE_MARKED_NOT_APPLICABLE'
