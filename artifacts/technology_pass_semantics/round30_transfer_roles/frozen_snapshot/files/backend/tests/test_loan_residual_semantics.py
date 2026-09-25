import pytest
from review_v2.loan_facts import extract,negative_scan
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import review_contract_v2

@pytest.mark.parametrize('text,found',[
 ('保险扣款顺序：保费、复利、罚息、利息、本金。',False),
 ('还款不足清偿全部债务时，依次抵充费用、利息、本金。',True),
 ('部分还款先清偿利息，再偿还本金。',True),
])
def test_offset_boundary(text,found):
 assert bool(extract('loan_repayment_offset_order',parse_contract_clauses(text)))==found

@pytest.mark.parametrize('node,text,found',[
 ('loan_overdue_interest','逾期罚息在执行利率基础上加收50%。',True),
 ('loan_overdue_interest','逾期罚息年利率6.30%。',True),
 ('loan_overdue_interest','贷款年利率4%。',False),
 ('loan_early_repayment_interest','提前还款利息按照实际贷款占用天数计算。',True),
 ('loan_early_repayment_interest','提前还款手续费另议。',False),
])
def test_interest_relations(node,text,found):
 assert bool(extract(node,parse_contract_clauses(text)))==found

@pytest.mark.parametrize('node,text,status',[
 ('loan_hidden_fee_over_cap','仅支付律师费、诉讼费和保全费。','NOT_FOUND'),
 ('loan_hidden_fee_over_cap','借款人另支付融资服务费100元。','FOUND'),
 ('loan_deducted_interest_forbidden','贷款人预扣利息100元。','FOUND'),
 ('loan_deducted_interest_forbidden','贷款人不得预扣利息。','NOT_FOUND'),
 ('loan_unreasonable_early_repayment_penalty','提前还款应支付违约金100元。','FOUND'),
 ('loan_unreasonable_early_repayment_penalty','提前还款不收取手续费。','NOT_FOUND'),
])
def test_negative_scan(node,text,status):
 assert negative_scan(node,parse_contract_clauses(text))['status']==status

def test_fixed_runtime_and_aggregation():
 from pathlib import Path
 from docx import Document
 p=next((Path(__file__).resolve().parents[2]/'test_data').glob('98 *.docx'))
 result=review_contract_v2('\n'.join(x.text for x in Document(p).paragraphs),'loan',use_llm=False)
 rows={r['item_id']:r for r in result['items']}
 assert rows['L-06-03']['coverage_status']=='缺失'
 assert rows['L-05-02']['coverage_status']=='部分覆盖'
 assert '逾期利息起止期间' in rows['L-05-02']['reasoning_summary']
 for key in ['L-07-02','L-07-03','L-03-03','L-04-04']:
  assert rows[key]['coverage_status']=='通过', (key,rows[key]['reasoning_summary'])
  assert not rows[key]['needs_manual_review']
 themes=[r for r in result['risk_findings'] if set(r['source_review_ids'])&{'L-03-02','L-12-02'}]
 assert len(themes)==1
 assert {'L-03-02','L-12-02'} <= set(themes[0]['source_review_ids'])
 assert result['release_quality_gate']['status']=='REPORT_READY'
