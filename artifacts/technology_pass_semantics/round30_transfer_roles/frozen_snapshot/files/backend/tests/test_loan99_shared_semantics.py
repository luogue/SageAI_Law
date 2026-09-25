import json
from pathlib import Path
from types import SimpleNamespace
import pytest
from review_v2.clause_parser import parse_contract_clauses as parse
from review_v2.loan_facts import LoanFacts, extract, financing_charge, negative_scan, PROFILES, consistency_gate
from review_v2.business_overlays import relevance, active
from review_v2.penalty_base import analyze

@pytest.mark.parametrize('prefix', ['', '第一条 合同主体\n', '附件一 主体信息\n'])
@pytest.mark.parametrize('lender,borrower,kinds', [
    ('甲方（出借人）：赵甲\n身份证号码：110101199001010019','乙方（借款人）：钱乙\n身份证号码：110101199002020021',('natural','natural')),
    ('出借人：甲有限公司','借款人：乙有限公司',('enterprise','enterprise')),
    ('贷款人：某商业银行','借款人：自然人赵甲',('financial','natural')),
])
def test_role_declaration_forms(prefix,lender,borrower,kinds):
    facts=LoanFacts.from_clauses(parse(prefix+lender+'\n'+borrower))
    assert (facts.values['lender_kind'],facts.values['borrower_kind']) == kinds
    assert facts.applicability('loan_enterprise_business_need')['applicable'] == (kinds == ('enterprise','enterprise'))
    assert facts.applicability('loan_financial_interest_compliance')['applicable'] == (kinds[0]=='financial')

@pytest.mark.parametrize('text,adverse',[
    ('收取2%手续费。',True),('不收取手续费。',False),
    ('除利息外，不另行收取手续费、管理费或其他融资费用。',False),
    ('不收取手续费，但收取管理费200元。',True),
    ('贷款人收取手续费2%。',True),('借款人承担诉讼律师费。',False),
])
def test_polarity_with_coordinated_objects(text,adverse):
    assert financing_charge(text) is adverse
    assert (negative_scan('loan_hidden_fee_over_cap',parse(text))['status']=='FOUND') is adverse

def supported(text):
    return {k for e in extract('loan_early_repayment_interest',parse(text)) for k in e['supports_element_ids']}

def test_joint_proof_requires_both_temporal_facts():
    stop='第一条 本金\n提前归还部分本金后，自到账日起已归还本金不再计算后续利息。'
    settle='第二条 清偿\n提前还款时结清截至实际还款日已经产生的利息。'
    expected={e['element_id'] for e in PROFILES['loan_early_repayment_interest']}
    assert supported(stop) < expected
    assert supported(settle) < expected
    assert supported(stop+'\n'+settle)==expected
    assert supported('提前还款利息按实际占用天数计算。')==expected
    assert not supported('借款人无需支付提前还款违约金。')

@pytest.mark.parametrize('text',[
    '任何一方联系方式发生变化，应于三个工作日内通知另一方。',
    '住所、联系电话变更，应在五个工作日内通知甲方。',
])
def test_notice_change_has_positive_evidence(text):
    assert any('loan_address_change_notice' in e['supports_element_ids'] for e in extract('loan_notice_service_method',parse(text)))

@pytest.mark.parametrize('text,level',[
    ('借款合同\n借款用于餐饮门店经营周转。','background_reference'),
    ('食品经营合同\n受托人负责食品经营。','direct_subject'),
    ('借款合同\n借款用于餐饮经营，放款必须以食品经营许可为前提。','performance_dependency'),
])
def test_regulatory_relevance(text,level):
    fact=relevance(text)['FOOD_OPERATION']
    assert fact['regulatory_relevance_level']==level
    assert ('FOOD_OPERATION' in active(text)) == (level != 'background_reference')

@pytest.mark.parametrize('period,expected',[
    ('利息自资金到账之日起计算至本金清偿之日止。','DETERMINABLE'),
    ('计息期间另行协商。','UNDEFINED'),
])
def test_formula_dependency(period,expected):
    rows=analyze('当期未付利息金额的1%支付违约金。利息以实际未偿还本金为基数。年利率为9%。'+period)
    assert rows[-1]['status']==expected

def test_supported_missing_conflict_blocks():
    node='loan_notice_service_method'
    clauses=parse('住所变更应通知甲方。')
    item=SimpleNamespace(node_id=node,item_id='test',coverage_status='部分覆盖',
        evidence_clauses=extract(node,clauses),decision_trace={'coverage_elements':[{'element_id':'loan_address_change_notice','status':'MISSING'}]})
    assert consistency_gate([item],LoanFacts.from_clauses(clauses))['status']=='BLOCKED'

def test_immutable_current_document():
    from layers.input_layer import InputLayer
    from review_v2.engine import review_contract_v2
    source=Path(__file__).resolve().parents[2]/'test_data'/'99 借款合同.docx'
    text=InputLayer()._extract_from_docx_content(source.read_bytes())
    r=review_contract_v2(text,'loan',use_llm=False)
    rows={i['item_id']:i for i in r['items']}
    for key in ('L-01-02','L-01-04','L-04-04','L-07-02','L-07-03','L-11-03','COMMON-20-01'):
        assert rows[key]['coverage_status']=='通过'
    for key in ('L-02-04','L-04-03'):
        assert rows[key]['coverage_status']=='不适用'
    assert rows['L-04-02']['applicability']['applicable'] is True
    assert '主体信息不足' not in rows['L-04-02']['reasoning_summary']
    assert 'REG-06-01' not in rows
    assert r['release_quality_gate']['status']=='REPORT_READY'
