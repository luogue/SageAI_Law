import pytest
from review_v2.engine import review_contract_v2
from review_v2.loan_facts import PROFILES,supports,consistency_gate,LoanFacts
from review_v2.clause_parser import parse_contract_clauses
from types import SimpleNamespace

@pytest.mark.parametrize('node,text',[
 ('loan_actual_disbursement_evidence','住址发生变化必须书面通知对方。'),
 ('loan_voucher_creditor_identification','甲乙双方住址可作为送达地址。'),
 ('loan_interest_calculation_base','诉讼期间无争议部分继续履行。'),
 ('loan_repayment_method_account','现住址发生变化应书面通知。'),
 ('loan_guarantee_attachment','评估、保险、登记、公证费用由乙方承担。'),
 ('loan_collection_record_attachment','附件或补充协议为合同组成部分。'),
])
def test_unrelated_text_cannot_support_element(node,text):
    assert not any(supports(e,text) for e in PROFILES[node])

def test_receipt_direct_evidence_and_missing_account():
    r=review_contract_v2('无抵押借款合同。贷款人：张三，身份证号123。借款人：李四，身份证号456。今收到贷款人张三现金150000元。住址变化应书面通知。附件为合同组成部分。','loan',use_llm=False)
    rows={i['item_id']:i for i in r['items']}
    for key in ['L-03-02','L-03-04','L-12-01','L-12-02']:
        assert rows[key]['coverage_status']=='通过'
        assert all('今收到' in e['quote'] for e in rows[key]['evidence_clauses'])
    assert rows['L-06-02']['coverage_status']=='缺失'
    assert rows['L-12-03']['coverage_status']=='不适用'
    assert rows['L-12-04']['coverage_status']=='缺失'

def test_natural_person_classification_and_existing_overdue_risk():
    text='贷款人：张三，身份证号123。借款人：李四，身份证号456。借款人逾期应每日按本金的0.5%支付违约金。'
    r=review_contract_v2(text,'loan',use_llm=False)
    rows={i['item_id']:i for i in r['items']}
    assert rows['L-01-02']['coverage_status']=='通过'
    assert rows['L-04-02']['coverage_status']=='待核验'
    assert rows['L-04-02']['decision_trace']['loan_cost_assessment']['components'][0]['annual_percent_estimate']==182.5
    assert 'loan_cost_assessment' not in rows['L-05-02']['decision_trace']
    assert not any({'L-04-02','L-05-02'}<=set(f['source_review_ids']) for f in r['risk_findings'])
    assert r['release_quality_gate']['status']=='REPORT_READY'

def test_invalid_pass_binding_is_blocked():
    facts=LoanFacts.from_clauses([])
    i=SimpleNamespace(node_id='loan_actual_disbursement_evidence',item_id='test',coverage_status='通过',evidence_clauses=[{'quote':'住址变化书面通知','supports_element_ids':['loan_disbursement_record']}],decision_trace={})
    assert consistency_gate([i],facts)['status']=='BLOCKED'


def test_service_address_is_partial_without_collection_channel():
    text='借款合同。甲乙双方提供的住址为现住址，如发生变化必须书面通知对方。如本合同发生争议，诉至法院双方提供的现住址可作为法院的送达地址。'
    result=review_contract_v2(text,'loan',use_llm=False)
    row=next(i for i in result['items'] if i['item_id']=='L-11-03')
    assert row['coverage_status']=='部分覆盖'
    assert '催收通知方式或渠道' in row['reasoning_summary']
    keys={k for e in row['evidence_clauses'] for k in e['supports_element_ids']}
    assert {'loan_service_address','loan_address_change_notice'} <= keys
    assert 'loan_collection_channel' not in keys


@pytest.mark.parametrize('base',['借款总额','本金','合同借款本金','借款金额'])
def test_unique_principal_cross_clause_reference(base):
    from review_v2.penalty_base import analyze
    text=f'1.2 借款金额：人民币壹拾伍万元整（￥150,000.00元）。\n2.4 每日按{base}的0.5%支付违约金。'
    rows=analyze(text)
    assert rows and all(r['status']=='DETERMINABLE' for r in rows)
    assert '150,000' in rows[0]['definitions'][0]


def test_ambiguous_principal_is_not_resolved():
    from review_v2.penalty_base import analyze
    rows=analyze('借款金额：100000元。借款本金：200000元。按本金的20%支付违约金。')
    assert rows[0]['status']=='UNDEFINED'


def test_resolved_principal_removes_false_theme_but_keeps_overdue_risk():
    result=review_contract_v2('贷款人：张三，身份证号123。借款人：李四，身份证号456。借款金额：150000元。每日按借款总额的0.5%支付逾期违约金。','loan',use_llm=False)
    assert not any(i['item_id']=='COMMON-20-01' and i['coverage_status']!='通过' for i in result['items'])
    assert next(i for i in result['items'] if i['item_id']=='L-04-02')['coverage_status']=='待核验'
    assert next(i for i in result['items'] if i['item_id']=='L-05-02')['coverage_status']=='缺失'


def test_actual_exposure_grading_preserves_coverage_and_evidence():
    text=('贷款人：张三，身份证号123。借款人：李四，身份证号456。借款金额：150000元。'
          '每日按借款总额的0.5%支付逾期违约金。'
          '双方住址变更应书面通知对方。双方现住址作为法院送达地址。'
          '收款收据：今收到贷款人张三现金150000元。')
    result=review_contract_v2(text,'loan',use_llm=False)
    rows={i['item_id']:i for i in result['items']}
    notice=rows['L-11-03']
    assert (notice['coverage_status'],notice['risk_severity'],notice['action_priority'])==('部分覆盖','LOW','C_OPTIMIZATION')
    assert (rows['L-04-02']['coverage_status'],rows['L-04-02']['risk_severity'],rows['L-04-02']['action_priority'])==('待核验','NONE','NONE')
    assert 'loan_cost_assessment' not in rows['L-05-02']['decision_trace']
    for key in ['L-12-01','L-12-02']:
        assert rows[key]['coverage_status']=='通过'
        assert all('今收到' in e['quote'] for e in rows[key]['evidence_clauses'])
    assert not any({'L-04-02','L-05-02'}<=set(f['source_review_ids']) for f in result['risk_findings'])
    assert result['release_quality_gate']['status']=='REPORT_READY'


def test_partial_alone_does_not_reduce_severity():
    from review_v2.engine import _actual_exposure_grade
    item=SimpleNamespace(node_id='generic',coverage_status='部分覆盖',economic_impact='none',
        decision_trace={'semantic_requirements':[
            {'element_id':'a','protective_mechanism':True},
            {'element_id':'b','residual_risk_kind':'core_obligation'}]},
        coverage_elements=[{'element_id':'a','status':'COVERED','evidence_ids':['e']},
                           {'element_id':'b','status':'MISSING'}])
    assert _actual_exposure_grade(item)=={}
    item.decision_trace['semantic_requirements'][1]['residual_risk_kind']='procedural_channel'
    assert _actual_exposure_grade(item)['severity']=='LOW'
    item.coverage_elements[0]['evidence_ids']=[]
    assert _actual_exposure_grade(item)=={}
