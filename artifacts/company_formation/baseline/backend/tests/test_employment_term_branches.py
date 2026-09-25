from datetime import date
from pathlib import Path
import pytest
from test_employment_fact_semantics import review, item
from review_v2.employment_facts import probation_dates, operative_optional_arrangement
from review_v2.priority_contract_review import probation_risk


@pytest.mark.parametrize('kind', ['固定期限', '无固定期限'])
def test_effective_start_and_trial_end(kind):
    text = f'本合同为{kind}劳动合同。本合同于2027年2月12日生效，其中试用期至2027年5月11日止。试用期工资为人民币9000元。'
    if kind == '固定期限':
        text += '终止日期为2030年2月11日。'
    assert probation_dates(text)[1] == (date(2027,2,12), date(2027,5,11))
    result = review(text)
    for rule in ['EMP-02-01','EMP-03-01','EMP-15-01']:
        assert item(result, rule)['coverage_status'] == '通过'


def test_fixed_end_required_and_indefinite_start_required():
    assert item(review('本合同为固定期限劳动合同。本合同于2027年2月12日生效。'),'EMP-02-01')['coverage_status'] == '部分覆盖'
    assert item(review('本合同为无固定期限劳动合同。'),'EMP-02-01')['coverage_status'] == '部分覆盖'


def test_trial_dates_cannot_supply_missing_contract_end():
    result = review('本合同为固定期限劳动合同。本合同于2027年2月12日生效。试用期自2027年2月12日至2027年3月11日。')
    assert item(result,'EMP-02-01')['coverage_status'] == '部分覆盖'


def test_standalone_term_range_after_type():
    result = review('本合同为固定期限劳动合同。自2027年2月12日至2030年2月11日止。')
    assert item(result,'EMP-02-01')['coverage_status'] == '通过'


@pytest.mark.parametrize('end,risk', [('2027年8月11日',False),('2027年8月12日',True)])
def test_indefinite_six_month_calendar_boundary(end,risk):
    assert probation_risk(f'本合同为无固定期限劳动合同。本合同于2027年2月12日生效，其中试用期至{end}止。') is risk


def test_fixed_short_term_limit_still_applies():
    assert probation_risk('本合同为固定期限劳动合同。本合同于2027年2月12日生效。终止日期为2028年2月11日。其中试用期至2027年5月11日止。')


def test_task_completion_not_calendar_end():
    assert item(review('本合同为以完成软件迁移工作任务为期限的劳动合同，工作任务完成时本合同终止。本合同于2027年2月12日生效。'), 'EMP-02-01')['coverage_status'] == '通过'


@pytest.mark.parametrize('kind',['固定期限','无固定期限','以完成工程工作任务为期限'])
def test_future_agreements_independent_of_term_type(kind):
    result = review(f'本合同为{kind}劳动合同。第二条 如需专项培训并约定服务期，由双方另行订立专项培训及服务期协议。第三条 如有必要约定竞业限制，由双方另行签订竞业限制协议。')
    for rule in ['EMP-09-01','NC-01-01','NC-02-01','NC-03-01']:
        assert item(result,rule)['coverage_status'] == '不适用'


def test_present_duty_not_erased_by_future_reservation():
    assert operative_optional_arrangement('可以另行签订培训协议。乙方承诺服务期为3年。', '服务期')
    assert operative_optional_arrangement('另行签订竞业协议。竞业限制期限为2年。', '竞业限制')


@pytest.mark.parametrize('filename',['61 劳动合同.docx','64 无固定期限劳动合同.docx','63 劳动合同.docx'])
def test_three_actual_contracts(filename):
    from layers.input_layer import InputLayer
    from starlette.datastructures import UploadFile
    with (Path(__file__).resolve().parents[2]/'test_data'/filename).open('rb') as stream:
        text = InputLayer().extract_text_from_file(UploadFile(filename=filename,file=stream))
    result = review(text)
    assert result['release_quality_gate']['status'] == 'REPORT_READY'
    for rule in ['EMP-02-01','EMP-03-01','EMP-15-01']:
        assert item(result,rule)['coverage_status'] == '通过'
    for rule in ['EMP-09-01','NC-01-01','NC-02-01','NC-03-01']:
        assert item(result,rule)['coverage_status'] == '不适用'
    if filename.startswith('63'):
        for rule in ['EMP-10-01','EMP-13-01','EMP-IP-01']:
            assert item(result,rule)['coverage_status'] == '风险条款'
        assert len(result['risk_findings']) == 6
    elif filename.startswith('61'):
        assert result['final_disposition_summary']['actionable'] == 0
    else:
        assert item(result,'EMP-05-01')['coverage_status'] == '通过'
        assert result['final_disposition_summary']['actionable'] == 0
