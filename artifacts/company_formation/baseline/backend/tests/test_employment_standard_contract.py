"""Standard prose, independent values, adverse variants and gate mutation tests."""
from copy import deepcopy
from types import SimpleNamespace
from pathlib import Path
import pytest

from test_employment_fact_semantics import review, item, checkpoint
from review_v2.priority_contract_review import judge, probation_risk, applicability
from review_v2.clause_parser import parse_contract_clauses
from review_v2.lease_semantics import consistency_failures
from review_v2.priority_contract_types import classify_priority_contract


@pytest.mark.parametrize('salary', [6800, 8300, 12500])
def test_narrative_wage_and_payment_order(salary):
    result = review(f'第八条 乙方在试用期期间的工资标准为人民币{salary} 元/月。试用期为2个月。试用期满后，乙方月工资标准为人民币15000元/月。\n第九条 甲方于每月15日前，以银行转账方式足额支付乙方上一个自然月的工资。')
    for rule in ['EMP-03-01', 'EMP-06-01']:
        row = item(result, rule)
        assert row['coverage_status'] == '通过'
        assert not any(a['result'] == 'NOT_FOUND' for a in row['decision_trace'].get('element_absence_searches', []))


@pytest.mark.parametrize('source,rule', [
    ('甲方（用人单位）名称：云川设备有限公司\n注册登记地：江苏省南京市长江路18号\n乙方（劳动者）姓名：陈清\n性别：女\n居民身份证号码：320101199407050028', 'EMP-01-01'),
    ('甲方安排乙方在制造部设备检修岗位，从事设备维护、测试工作，工作地点为南京市长江路18号。', 'EMP-04-01'),
    ('甲乙双方按照国家及江苏省有关社会保险法律法规规定参加社会保险，依法缴纳养老保险、医疗保险、工伤保险等社会保险费用。其中依法应由乙方承担的社会保险费，由甲方从乙方工资中代扣代缴。', 'EMP-07-01'),
    ('甲方为乙方提供符合国家规定的劳动安全卫生条件以及与岗位相适应的工作设备和必要的劳动防护用品。本岗位不存在职业病危害因素。', 'EMP-08-01'),
])
def test_prose_facts_are_found(source, rule):
    row = item(review(source), rule)
    assert row['coverage_status'] == '通过'
    assert not any(a['result'] == 'NOT_FOUND' for a in row['decision_trace'].get('element_absence_searches', []))


@pytest.mark.parametrize('end,risk', [('2029年8月31日', False), ('2027年8月31日', True)])
def test_selected_fixed_term_not_inactive_task_option(end, risk):
    text = f'第一条 固定期限。自2026年9月1日起至{end}止。其中，试用期自2026年9月1日起至2026年11月30日止。\n（二）无固定期限。不适用。\n（三）以完成一定的工作任务为期限。不适用。'
    assert probation_risk(text) is risk
    row = item(review(text), 'EMP-15-01')
    assert row['coverage_status'] == ('风险条款' if risk else '通过')


@pytest.mark.parametrize('extra,active', [('', False), ('\n第二条 双方约定服务期为3年，竞业限制期限为1年。', True)])
def test_deferred_agreement_does_not_create_current_duty(extra, active):
    text = '第一条 甲方提供专项培训的，双方可以另行签订服务期协议。因工作需要，双方可以另行签订竞业限制协议。竞业限制期限和补偿依法执行。' + extra
    for rule in ['EMP-09-01', 'NC-01-01', 'NC-02-01']:
        assert applicability(text, checkpoint(rule), 'labor')[0] is active


def test_lawful_compensation_retains_only_real_residual():
    row = item(review('解除终止符合法定经济补偿情形的，甲方依法向乙方支付经济补偿。'), 'EMP-11-01')
    assert row['coverage_status'] == '通过'
    assert row['coverage_elements'][0]['status'] == 'COVERED'
    assert row['coverage_elements'][1]['status'] == 'MISSING'
    assert row['coverage_elements'][1]['risk_relevant'] is False


def test_trial_prose_salary_does_not_prove_regular_salary():
    row = item(review('乙方在试用期期间的工资标准为人民币8100元/月。'), 'EMP-06-01')
    assert row['coverage_elements'][0]['status'] == 'MISSING'


def test_training_expense_alone_does_not_impose_service_period():
    row = item(review('甲方提供专项培训费用6000元，不约定服务期。'), 'EMP-09-01')
    assert row['coverage_status'] == '不适用'


def test_ancillary_secrecy_topics_do_not_become_an_independent_agreement():
    text = '项目名称：设备能耗技术咨询项目。甲方向乙方支付咨询报酬。双方保护保密信息、商业秘密，承担保密义务。'
    assert classify_priority_contract(text, parse_contract_clauses(text)) is None
    independent = '披露方：青河公司。接收方：白云公司。保密信息包括商业秘密，接收方承担保密义务。'
    assert classify_priority_contract(independent, parse_contract_clauses(independent))[0] == 'confidentiality'


def test_employment_gap_consequence_cannot_use_packaging_template():
    row = item(review('劳动保护与职业危害防护。'), 'EMP-08-01')
    assert '运输损坏' not in str(row)


def test_labor_runtime_drift_gate_ignores_unrelated_utility_supply_dependency(monkeypatch):
    from routers import review_v2 as route

    loaded = deepcopy(route._LOADED_DEPENDENCY_SOURCES)
    loaded['utility_supply_evidence'] = {
        **loaded['utility_supply_evidence'],
        'sha256': 'stale-unrelated-utility-supply',
    }
    monkeypatch.setattr(route, '_LOADED_DEPENDENCY_SOURCES', loaded)

    labor = route._runtime_source_drift_status('labor')
    utility = route._runtime_source_drift_status('utility_supply')

    assert labor['status'] == 'CURRENT'
    assert 'utility_supply_evidence' not in labor['changed_dependencies']
    assert utility['status'] == 'STALE_RUNTIME'
    assert utility['changed_dependencies'] == ['utility_supply_evidence']


def test_gate_rejects_untriggered_conditional_missing():
    row = deepcopy(item(review('甲方提供劳动保护用品，安排安全培训。本岗位不存在职业病危害因素。'), 'EMP-08-01'))
    conditional = next(e for e in row['coverage_elements'] if e.get('conditional_element'))
    conditional.update(status='MISSING', risk_relevant=True)
    assert any(f['requirement'] == 'UNTRIGGERED_CONDITIONAL_ELEMENT_RISK' for f in consistency_failures([SimpleNamespace(**row)]))


def test_gate_rejects_positive_evidence_and_not_found_same_element():
    row = deepcopy(item(review('月工资：18000元。每月12日支付工资，工资通过银行转账。'), 'EMP-06-01'))
    row['decision_trace']['element_absence_searches'][0]['result'] = 'NOT_FOUND'
    assert any(f['requirement'] == 'SEARCH_AUDIT_ELEMENT_CONFLICT' for f in consistency_failures([SimpleNamespace(**row)]))


def test_gate_rejects_risk_without_direct_fact():
    row = deepcopy(item(review('甲方有权随时解除劳动合同且无需支付经济补偿。'), 'EMP-16-01'))
    assert row['coverage_status'] == '风险条款'
    row['evidence_clauses'] = []
    assert any(f['requirement'] == 'ADVERSE_RULE_WITHOUT_DIRECT_FACT' for f in consistency_failures([SimpleNamespace(**row)]))


def test_standard_docx_full_pipeline():
    from layers.input_layer import InputLayer
    from starlette.datastructures import UploadFile
    source = Path(__file__).resolve().parents[2] / 'test_data/61 劳动合同.docx'
    with source.open('rb') as stream:
        text = InputLayer().extract_text_from_file(UploadFile(filename=source.name, file=stream))
    result = review(text)
    assert len(result['items']) == 20
    assert result['release_quality_gate']['status'] == 'REPORT_READY'
    assert not result['release_quality_gate']['failures']
    for rule in ['EMP-01-01', 'EMP-03-01', 'EMP-04-01', 'EMP-05-01', 'EMP-06-01', 'EMP-07-01', 'EMP-13-01', 'EMP-14-01', 'EMP-15-01', 'EMP-16-01']:
        assert item(result, rule)['coverage_status'] == '通过'
    safety = item(result, 'EMP-08-01')
    assert safety['coverage_status'] == '待核验'
    assert safety['needs_manual_review']
    assert {e['status'] for e in safety['coverage_elements']} == {'COVERED', 'CONDITION_UNRESOLVED'}
    for rule in ['EMP-09-01', 'NC-01-01', 'NC-02-01', 'NC-03-01']:
        assert item(result, rule)['coverage_status'] == '不适用'
    assert item(result, 'EMP-10-01')['coverage_status'] == '通过'
    assert item(result, 'EMP-11-01')['coverage_status'] == '通过'
    assert not any(f['severity'] in {'HIGH', 'CRITICAL', 'MEDIUM'} for f in result['final_dispositions'])
    assert result['final_disposition_summary']['must_change'] == 0
    assert '运输损坏' not in result['result']
    assert not any(f['severity'] in {'HIGH', 'CRITICAL'} for f in result['final_dispositions'])
