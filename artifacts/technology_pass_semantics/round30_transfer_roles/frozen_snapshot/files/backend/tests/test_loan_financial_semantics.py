from pathlib import Path
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.loan_facts import LoanFacts,extract,PROFILES,supports

@pytest.mark.parametrize('text,active',[
 ('本贷款不得办理展期。',False),
 ('本借款不允许展期。',False),
 ('借款人可申请展期，经贷款人批准后办理。',True),
])
def test_extension_polarity(text,active):
 f=LoanFacts.from_clauses(parse_contract_clauses(text))
 for node in ['loan_extension_request','loan_extension_interest_rate','loan_extension_original_due_no_consent']:
  assert f.applicability(node)['applicable']==active

@pytest.mark.parametrize('node,text,found',[
 ('loan_repayment_method_account','还款方式：按月等额本息还款。',True),
 ('loan_repayment_method_account','借款人授权贷款人从还款账户自动扣收应偿还的本息。',True),
 ('loan_repayment_method_account','转账给装修公司支付装修款。',False),
 ('loan_compound_interest_limit','扣款顺序：保费、复利、罚息、利息、本金。',False),
 ('loan_compound_interest_limit','对未付利息按罚息利率计收复利。',True),
 ('loan_compound_interest_limit','不计收复利。',True),
 ('loan_early_repayment_notice','提前还款应事先向贷款人申请并取得同意。',True),
 ('loan_early_repayment_notice','提前还款无需申请或取得贷款人同意。',False),
 ('loan_notice_service_method','借款人的住所发生重大变化，应及时通知贷款人。',True),
 ('loan_actual_disbursement_evidence','电子借据记载贷款金额，作为放款证明。',True),
])
def test_positive_negative_relations(node,text,found):
 assert bool(extract(node,parse_contract_clauses(text)))==found

def test_cross_clause_repayment():
 c=parse_contract_clauses('第一条 还款方式\n按月等额本息还款。\n第二条 还款账户\n还款账户：账号1234。')
 hits=extract('loan_repayment_method_account',c)
 assert {e for h in hits for e in h['supports_element_ids']}=={'loan_repayment_method','loan_repayment_account'}
 assert len({h['clause_id'] for h in hits})==2

@pytest.mark.parametrize('lender,borrower,expected',[
 ('某银行','自然人甲',False),('某银行','待补充',False),('甲有限公司','乙有限公司',True)])
def test_enterprise_gate(lender,borrower,expected):
 f=LoanFacts.from_clauses(parse_contract_clauses(f'贷款人：{lender}。借款人：{borrower}。'))
 assert f.applicability('loan_enterprise_business_need')['applicable']==expected

def test_fixed_file():
 from docx import Document
 from review_v2.engine import review_contract_v2
 p=next((Path(__file__).resolve().parents[2]/'test_data').glob('98 *.docx'))
 text='\n'.join(x.text for x in Document(p).paragraphs)
 r=review_contract_v2(text,'loan',use_llm=False)
 rows={i['item_id']:i for i in r['items']}
 for key in ['L-02-01','L-02-02','L-02-04','L-08-01','L-08-02','L-08-04','L-12-01']:
  assert rows[key]['coverage_status']=='不适用'
 assert rows['L-06-02']['coverage_status']=='通过'
 assert rows['L-07-04']['coverage_status']=='部分覆盖'
 assert rows['L-05-03']['coverage_status']!='通过'
 assert '已覆盖' not in rows['L-05-03']['risk_point_description']
 assert '未约定提前还款通知程序' not in rows['L-07-04']['risk_point_description']
 assert r['release_quality_gate']['status']=='REPORT_READY'
