from pathlib import Path
import pytest
from review_v2.clause_parser import parse_contract_clauses as parse
from review_v2.loan_facts import LoanFacts, extract, PROFILES
from review_v2.penalty_base import analyze

@pytest.mark.parametrize('body',[
 '甲方（出借方）：远星有限公司。乙方（借款方）：明川有限公司。',
 '甲方向乙方提供借款。第一条 期限\n借款一年。\n甲方：远星有限公司\n乙方：明川有限公司',
 '甲方（出借方）：\n乙方（借款方）：\n第一条 账户\n甲方指定还款账户如下：账户名称：远星有限公司。开户银行：某银行。\n第二条 签署\n乙方：明川有限公司。',
])
def test_roles_across_sections(body):
 f=LoanFacts.from_clauses(parse(body))
 assert (f.values['lender_kind'],f.values['borrower_kind'])==('enterprise','enterprise')
 assert f.applicability('loan_enterprise_business_need')['applicable'] is True
 assert f.applicability('loan_interest_lpr_cap')['applicable'] is True
 assert f.applicability('loan_financial_interest_compliance')['applicable'] is False

@pytest.mark.parametrize('body',[
 '借款人可提前还款，应提前7个工作日书面通知贷款人。',
 '乙方提前归还全部或部分本金，只需提前十日书面通知甲方。',
 '乙方拟提前还款的，须提前三日书面通知对方。',
])
def test_notification_right(body):
 found={k for e in extract('loan_early_repayment_notice',parse(body)) for k in e['supports_element_ids']}
 assert found=={e['element_id'] for e in PROFILES['loan_early_repayment_notice']}

@pytest.mark.parametrize('base',['应付未付利息','届期未付利息','到期未支付利息'])
@pytest.mark.parametrize('reverse',[False,True])
def test_formula_reordered(base,reverse):
 parts=['利息基数为实际占用且尚未归还的本金。','年利率为8.1%，日利率为年利率÷365。',
        '利息自实际到账之日起计算至相应本金归还之日止。', '每季度结息。',f'按{base}每日0.03%支付违约金。']
 text='\n'.join(reversed(parts) if reverse else parts)
 rows=analyze(text)
 assert rows and all(r['status']=='DETERMINABLE' for r in rows)

@pytest.mark.parametrize('body,expected',[
 ('借款合同\n贷款人：甲有限公司。借款人：乙有限公司。银行转账凭证作为到账证明。',False),
 ('借款人应另行出具借据，载明借款金额。',True),
 ('附件一 借据\n借款金额为30000元。',True),
])
def test_debt_instrument_scenario(body,expected):
 f=LoanFacts.from_clauses(parse(body))
 for n in ['loan_note_receipt_attachment','loan_voucher_creditor_identification']:
  assert f.applicability(n)['applicable'] is expected

def test_current_immutable_enterprise_document():
 from layers.input_layer import InputLayer
 from review_v2.engine import review_contract_v2
 source=Path(__file__).resolve().parents[2]/'test_data'/'101 企业之间借款合同.docx'
 result=review_contract_v2(InputLayer()._extract_from_docx_content(source.read_bytes()),'loan',use_llm=False)
 rows={i['item_id']:i for i in result['items']}
 for k in ['L-01-02','L-02-04','L-07-04','COMMON-20-01']:
  assert rows[k]['coverage_status']=='通过', (k,rows[k]['reasoning_summary'])
 for k in ['L-04-03','L-03-04','L-12-01']:
  assert rows[k]['coverage_status']=='不适用'
 assert rows['L-04-02']['applicability']['applicable'] is True
 assert result['release_quality_gate']['status']=='REPORT_READY'

@pytest.mark.parametrize('body,expected',[
 ('提前还款无需取得贷款人同意，但须提前六日书面通知贷款人。',True),
 ('提前还款应向贷款人申请并取得书面同意。',True),
 ('提前还款无需申请或取得贷款人同意。',False),
 ('借款人应提前六日通知贷款人变更地址。',False),
])
def test_repayment_procedure_boundaries(body,expected):
 from review_v2.loan_facts import supports
 assert supports(PROFILES['loan_early_repayment_notice'][0],body) is expected
