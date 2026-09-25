from copy import deepcopy
from types import SimpleNamespace
import pytest
from test_employment_fact_semantics import review, item
from review_v2.lease_semantics import consistency_failures

TASK = '1、固定期限劳动合同：不适用。\n2、无固定期限劳动合同：不适用。\n3、以完成一定工作任务为期限的劳动合同。\n本合同于2028年4月6日生效，以完成“仓库设备迁移项目”为工作任务。全部工作任务完成并经验收确认之日为本劳动合同终止时间。预计2028年12月完成仅作计划参考。本合同不约定试用期。'


def test_selected_task_and_no_probation():
    result = review(TASK)
    assert item(result,'EMP-02-01')['coverage_status'] == '通过'
    assert item(result,'EMP-03-01')['coverage_status'] == '不适用'
    assert item(result,'EMP-15-01')['coverage_status'] == '通过'
    assert not any('终止日期' in e['proposition'] for e in item(result,'EMP-02-01')['coverage_elements'])


@pytest.mark.parametrize('text', ['本合同不设试用期。', '本合同不约定试用期。'])
def test_explicit_none_not_missing(text):
    result = review(text)
    assert item(result,'EMP-03-01')['coverage_status'] == '不适用'


def test_task_trial_cannot_be_immunized_by_denial():
    result = review(TASK+'第四条 试用期为1个月，试用期工资为8000元。')
    assert item(result,'EMP-03-01')['coverage_status'] != '不适用'
    assert item(result,'EMP-15-01')['coverage_status'] == '风险条款'


@pytest.mark.parametrize('omitted', ['本合同于2028年4月6日生效，', '以完成“仓库设备迁移项目”为工作任务。', '全部工作任务完成并经验收确认之日为本劳动合同终止时间。'])
def test_task_required_elements_remain_required(omitted):
    assert item(review(TASK.replace(omitted,'')),'EMP-02-01')['coverage_status'] == '部分覆盖'


@pytest.mark.parametrize('rule,text', [
    ('EMP-01-01','甲方（公章）：东岭软件有限公司\n注册地址：杭州市西湖区文三路16号\n乙方（签名）：陈晓\n居民身份证号码：330106199005162315'),
    ('EMP-06-01','甲方于每月 8日 前通过 银行转账 方式支付乙方上一个自然月工资。乙方月工资标准为税前人民币 9300元/月。'),
    ('EMP-11-01','依法需要向劳动者支付经济补偿的，用人单位按照法律规定支付。'),
])
def test_prose_variants_bound_and_audit_gate(rule,text):
    row = item(review(text),rule)
    assert row['coverage_status'] == '通过'
    audits = row['decision_trace']['element_absence_searches']
    assert not any(a['result']=='NOT_FOUND' and a['element_id'] in {e['element_id'] for e in row['coverage_elements'] if e.get('risk_relevant') is not False} for a in audits)
    tampered = deepcopy(row)
    found = next(a for a in tampered['decision_trace']['element_absence_searches'] if a['result']=='FOUND')
    found['result'] = 'NOT_FOUND'
    assert any(f['requirement']=='SEARCH_AUDIT_ELEMENT_CONFLICT' for f in consistency_failures([SimpleNamespace(**tampered)]))


def test_worker_home_cannot_prove_employer_address():
    result = review('甲方（盖章）：东岭软件有限公司\n乙方（签字）：陈晓\n居民身份证号码：330106199005162315\n家庭住址：杭州市文三路16号')
    assert item(result,'EMP-01-01')['coverage_status'] == '部分覆盖'


def test_actual_task_contract_full_pipeline():
    from pathlib import Path
    from layers.input_layer import InputLayer
    from starlette.datastructures import UploadFile
    source = Path(__file__).resolve().parents[2]/'test_data/66 完成一定工作任务为期限的劳动合同.docx'
    with source.open('rb') as stream:
        text = InputLayer().extract_text_from_file(UploadFile(filename=source.name,file=stream))
    result = review(text)
    for rule in ['EMP-01-01','EMP-02-01','EMP-15-01','EMP-06-01','EMP-11-01']:
        assert item(result,rule)['coverage_status'] == '通过'
    for rule in ['EMP-03-01','EMP-09-01','NC-01-01','NC-02-01','NC-03-01']:
        assert item(result,rule)['coverage_status'] == '不适用'
    assert result['final_disposition_summary']['actionable'] == 0
    assert result['release_quality_gate']['status'] == 'REPORT_READY'
