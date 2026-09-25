from datetime import date
from pathlib import Path
import pytest
from review_v2.engine import review_contract_v2
from review_v2.guarantee_scenarios import extract, applicable, attachment_inventory

PERSON='乙方（保证人）：周明\n身份证号码：123\n'


@pytest.mark.parametrize('node,body,expected',[
 ('state_org_guarantor_forbidden',PERSON,False),
 ('public_nonprofit_guarantor_forbidden',PERSON,False),
 ('state_org_guarantor_forbidden','乙方（保证人）：某财政局\n',True),
 ('public_nonprofit_guarantor_forbidden','乙方（保证人）：公益非营利基金会\n',True),
 ('single_written_guarantee','双方签署本保证合同。',False),
 ('single_written_guarantee','保证人已出具担保函。',True),
 ('single_written_guarantee','如果出具担保函，应另行约定。',False),
 ('assignment_transfer_attachment','债权人有权将债权转让第三方。',False),
 ('assignment_transfer_attachment','双方已签署债权转让协议。',True),
 ('guarantee_scope_exclusions','保证范围包括全部本金、利息、罚息和费用。',False),
 ('guarantee_scope_exclusions','保证人仅承担部分保证，保证比例为30%。',True),
 ('guarantee_scope_exclusions','保证人不承担罚息和其他费用。',True),
])
def test_factual_gates(node,body,expected):
    assert applicable(node,extract(body)) is expected


@pytest.mark.parametrize('text,status,active',[
 ('借款期限为2026年9月8日至2027年9月7日。','UNMATURED',False),
 ('借款期限为2020年9月8日至2021年9月7日。','HISTORICAL_OR_OVERDUE',True),
 ('本保证用于既有债务，债务已逾期。','HISTORICAL_OR_OVERDUE',True),
 ('如债务已到期则可以催收。','UNKNOWN',False),
])
def test_debt_age(text,status,active):
    f=extract(text,date(2026,9,8))
    assert f['main_contract_status']==status
    assert applicable('main_debt_limitation_disclosure',f) is active


@pytest.mark.parametrize('text,state',[
 ('本合同附件为组成部分，主合同编号为A1。','PENDING_VERIFICATION'),
 ('双方签署本保证合同。','NOT_APPLICABLE'),
 ('附件1：借款协议\n另行提供，正文略。','PENDING_VERIFICATION'),
 ('附件1：借款协议\n第一条 借款人及出借人约定借款本金为100万元，借款期限一年，按约定支付利息，双方同意依约办理借款资金交付。\n第二条 借款人应在借款期限届满时归还本金并支付利息，借款人未按约定还款的，应承担合同约定的违约责任，争议向人民法院起诉。','VERIFIED'),
])
def test_actual_annex_not_reference(text,state):
    assert attachment_inventory(text)['status']==state


@pytest.mark.parametrize('node,text,expected',[
 ('GUA-05-04','保证人承担一般保证责任。','法律提示'),
 ('GUA-05-04','保证期间因催收而中断。','风险条款'),
 ('GUA-05-04','保证期间不发生中止、中断和延长。','法律提示'),
 ('GUA-11-02','保证人承担责任后可以向债务人追偿。','法律提示'),
 ('GUA-11-02','保证人放弃代位权。','风险条款'),
 ('GUA-11-02','保证人不放弃代位权。','法律提示'),
 ('GUA-03-03','保证人承担一般保证责任。','法律提示'),
])
def test_statutory_default_and_actual_conflict(node,text,expected):
    r=review_contract_v2('保证合同\n'+PERSON+'第一条 保证责任\n'+text,'guarantee',use_llm=False)
    i=next(i for i in r['items'] if i['item_id']==node)
    assert i['coverage_status']==expected
    if expected=='法律提示':
        assert not i['related_risks']
        assert i['action_priority']=='NONE'
    else:assert i['evidence_clauses']


@pytest.mark.parametrize('clause',[
 '保证人追偿不得损害债权人利益。',
 '保证人追偿不影响债权人债权实现。',
 '保证人追偿劣后于债权人剩余债权。',
 '保证人追偿与债权人的支付要求同时存在时，债务人优先偿付其对债权人的债务。',
])
def test_recourse_priority_synonyms(clause):
    r=review_contract_v2('保证合同\n第一条 追偿\n'+clause,'guarantee',use_llm=False)
    i=next(i for i in r['items'] if i['item_id']=='GUA-11-04')
    assert i['coverage_status']=='通过'
    assert all(e['quote'] in clause or clause in e['quote'] for e in i['evidence_clauses'])


def test_credit_authorization_never_confirms_institution_qualification():
    text='保证合同\n'+PERSON+'第五条 征信\n保证人授权债权人查询人民银行征信信息并报送征信信息，用于本合同业务管理。'
    r=review_contract_v2(text,'guarantee',use_llm=False)
    i=next(i for i in r['items'] if i['item_id']=='GUA-13-01')
    f=i['decision_trace']['guarantee_shared_facts']['credit_reporting_eligibility']
    assert f['authorization_text']=='FOUND'
    assert f['query_access_qualification']==f['reporting_institution_qualification']=='UNVERIFIED'
    assert i['coverage_status']=='待核验'


def test_supplied_annex_binds_body_not_reference_heading():
    text=('保证合同\n'+PERSON+'主合同为《借款协议》。\n附件1：借款协议\n'
          '第一条 借款人及出借人约定借款本金为100万元，借款期限一年，按约定支付利息，双方同意依约办理借款资金交付。\n'
          '第二条 借款人应在借款期限届满时归还本金并支付利息，借款人未按约定还款的，应承担合同约定的违约责任，争议向人民法院起诉。')
    r=review_contract_v2(text,'guarantee',use_llm=False)
    i=next(i for i in r['items'] if i['item_id']=='GUA-12-04')
    assert i['coverage_status']=='通过'
    assert i['evidence_clauses']
    assert all(e['document_type']=='APPENDIX' and len(e['quote'])>20 for e in i['evidence_clauses'])
    assert r['release_quality_gate']['status']=='REPORT_READY'


def test_current_guarantee_closure():
    from layers.input_layer import InputLayer
    from fastapi import UploadFile
    p=next((Path(__file__).resolve().parents[2]/'test_data').glob('69 *.docx'))
    with p.open('rb') as file:text=InputLayer().extract_text_from_file(UploadFile(filename=p.name,file=file))
    r=review_contract_v2(text,'guarantee',use_llm=False)
    rows={i['item_id']:i for i in r['items']}
    for key in ('GUA-01-02','GUA-01-03','GUA-01-04','GUA-02-02','GUA-03-04','GUA-07-04','GUA-09-04','GUA-12-01',*[f'GUA-10-0{i}' for i in range(1,5)]):
        assert rows[key]['coverage_status']=='不适用'
    for key in ('GUA-07-02','GUA-08-01','GUA-08-02','GUA-08-03','GUA-11-04','GUA-09-03'):
        assert rows[key]['coverage_status']=='通过'
    assert rows['GUA-09-01']['coverage_status']=='法律提示'
    assert rows['GUA-01-01']['coverage_status']=='风险条款'
    assert rows['GUA-01-01']['action_priority']=='B_PRACTICAL'
    assert not rows['GUA-01-01']['needs_manual_review']
    assert r['overall_assessment']['signability']=='建议修改后签署'
    assert rows['GUA-12-04']['coverage_status']==rows['GUA-13-01']['coverage_status']=='待核验'
    assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']
    assert r['final_overview_summary']['recommended_action']>=1
