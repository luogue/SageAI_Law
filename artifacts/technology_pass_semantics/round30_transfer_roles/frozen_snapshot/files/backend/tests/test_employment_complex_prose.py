"""Vary wording, actors, numbering and dates; bind risks to list predicates."""
import pytest
from pathlib import Path
from test_employment_fact_semantics import review, item, checkpoint
from review_v2.priority_contract_review import probation_risk, applicability, positive_rule_adverse_evidence
from review_v2.employment_exit import classify_exit_clauses
from review_v2.clause_parser import parse_contract_clauses


@pytest.mark.parametrize('day', ['五', '十五', '25'])
def test_money_payment_chinese_day(day):
    row = item(review(f'甲方每月{day}日前以货币形式支付乙方上月工资，基本工资为人民币13000元。'), 'EMP-06-01')
    assert row['coverage_status'] == '通过'
    assert all(a['result'] == 'FOUND' for a in row['decision_trace'].get('element_absence_searches', []))


@pytest.mark.parametrize('end,risk', [('2027年12月9日', False), ('2028年4月10日', True)])
def test_inherited_trial_start(end, risk):
    text = f'本合同自2027年9月10日起至2030年9月9日止，其中试用期至{end}止。乙方在试用期期间的基本工资为人民币8900元。'
    assert probation_risk(text) is risk
    assert item(review(text), 'EMP-03-01')['coverage_status'] == '通过'


def test_atomic_identity_with_employee_address_not_employer_address():
    row = item(review('甲方：清河研究院\n第二条 乙方陈清，性别女。\n居民身份证号码：320101199407050028。\n家庭住址：南京市长江路18号。'), 'EMP-01-01')
    assert row['coverage_status'] == '部分覆盖'
    assert row['coverage_elements'][0]['status'] == 'MISSING'
    assert row['coverage_elements'][1]['status'] == 'COVERED'
    assert row['risk_level'] != '高'


@pytest.mark.parametrize('text,rule,status', [
    ('实行的休假制度有国家法定节假日、公休日及带薪年假。', 'EMP-05-01', '部分覆盖'),
    ('甲乙双方按国家和广东省的规定参加社会保险。', 'EMP-07-01', '通过'),
    ('如需支付经济补偿，则甲方在乙方工作交接结束后支付。', 'EMP-11-01', '通过'),
])
def test_recognized_provisions_not_missing(text, rule, status):
    row = item(review(text), rule)
    assert row['coverage_status'] == status
    assert any(e['status'] == 'COVERED' for e in row['coverage_elements'])


def test_attachment_proves_actual_duties():
    row = item(review('工作地点为南京市。\n附件：岗位职责任务书\n负责系统模块的程序开发、测试和维护。'), 'EMP-04-01')
    assert row['coverage_status'] == '通过'
    assert any(e.get('section_type') == '附件' for e in row['evidence_clauses'])


def test_authorized_future_service_and_conditional_penalty_not_current_obligation():
    text = '第七条 甲方为乙方提供专项培训费用，对其进行培训的，可以与乙方订立协议，约定服务期。乙方违反服务期约定，应当按照约定向甲方支付违约金。'
    assert applicability(text, checkpoint('EMP-09-01'), 'labor')[0] is False
    assert applicability(text + '\n第八条 双方约定服务期为2年。', checkpoint('EMP-09-01'), 'labor')[0] is True


@pytest.mark.parametrize('text,category', [
    ('被依法追究刑事责任的', 'STATUTORY'),
    ('严重违反用人单位的规章制度的', 'DISCIPLINARY_VERIFICATION'),
    ('被行政拘留的', 'EXPANDED_RIGHT'),
    ('项目负责人调离的', 'EXPANDED_RIGHT'),
    ('经费来源终止的', 'EXPANDED_RIGHT'),
    ('不能胜任工作，经培训或调整工作岗位仍不能胜任工作的', 'STATUTORY'),
    ('相关社会行为严重违反公序良俗要求的', 'MANUAL_VERIFICATION'),
    ('不服从管理且构成严重违纪的', 'DISCIPLINARY_VERIFICATION'),
])
def test_parent_permission_classification(text, category):
    clauses = parse_contract_clauses('第八条 有下列情形之一的，甲方可以解除劳动合同：\n（一）' + text + '。')
    rows = classify_exit_clauses(clauses)
    assert len(rows) == 1
    assert rows[0]['classification'] == category


def test_protection_not_negative_but_sibling_expansion_is_bound():
    text = '第三条 乙方有下列情形之一的，甲方不得解除劳动合同：\n（一）女职工在孕期的。\n第四条 甲方可以随时解除劳动合同。'
    rows = positive_rule_adverse_evidence('employment_exit', parse_contract_clauses(text))
    assert rows and all('不得' not in r['text'] and '孕期' not in r['text'] for r in rows)
    result = review(text)
    row = item(result, 'EMP-10-01')
    assert row['coverage_status'] == '风险条款'
    assert all(e['status'] == 'ADVERSE' for e in row['coverage_elements'])
    assert row['related_risks']
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


def test_current_complex_contract_pipeline():
    from layers.input_layer import InputLayer
    from starlette.datastructures import UploadFile
    source = Path(__file__).resolve().parents[2] / 'test_data/63 劳动合同.docx'
    with source.open('rb') as f:
        text = InputLayer().extract_text_from_file(UploadFile(filename=source.name, file=f))
    result = review(text)
    for rule in ['EMP-03-01', 'EMP-04-01', 'EMP-06-01']:
        row = item(result, rule)
        assert row['coverage_status'] == '通过'
        assert not any(a['result'] == 'NOT_FOUND' for a in row['decision_trace'].get('element_absence_searches', []))
    for rule in ['EMP-01-01', 'EMP-05-01']:
        assert item(result, rule)['coverage_status'] == '部分覆盖'
    for rule in ['EMP-07-01', 'EMP-11-01']:
        assert item(result, rule)['coverage_status'] == '通过'
        assert item(result, rule)['risk_severity'] == 'NONE'
    assert item(result, 'EMP-11-01')['related_risks'] == []
    # A lawful basic insurance obligation may share its clause with an
    # independently adverse exemption; that link must originate from EMP-13.
    for risk_id in item(result, 'EMP-07-01')['related_risks']:
        finding = next(f for f in result['risk_findings'] if f['finding_id'] == risk_id)
        assert 'EMP-13-01' in finding['source_review_ids']
    safety = item(result, 'EMP-08-01')
    assert safety['coverage_status'] == '缺失'
    assert safety['action_priority'] == 'B_PRACTICAL'
    assert item(result, 'EMP-09-01')['coverage_status'] == '不适用'
    exit_row = item(result, 'EMP-10-01')
    assert exit_row['coverage_status'] == '风险条款'
    assert exit_row['related_risks']
    assert all('第二十二条' not in e['location'] for e in exit_row['evidence_clauses'])
    assert result['release_quality_gate']['status'] == 'REPORT_READY'
