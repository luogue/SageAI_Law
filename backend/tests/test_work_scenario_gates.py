import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.work_evidence import applicability
from review_v2.settlement_formula import applicability as shortfall

@pytest.mark.parametrize('text,active',[
 ('变卖所得不足以支付费用的，应补足差额。',False),
 ('赔偿不足部分应补足。',False),
 ('工资不足应补齐。',False),
 ('年度基数1000万元，未完成部分按8%补足。',True),
 ('最低采购额不足的，应补足差额。',True),
])
def test_shortfall_scope(text,active):
 assert shortfall(text)['applicable']==active

@pytest.mark.parametrize('text,active',[
 ('定作方未提供资料或者完成必要辅助工作，应承担责任。',False),
 ('承揽方可将辅助工作交由第三人完成。',True),
 ('承揽人将辅助工作外协。',True),
 ('承揽人负责辅助工作，不向第三方披露资料。',False),
])
def test_auxiliary_role(text,active):
 assert applicability('work_auxiliary_subcontract_liability',parse_contract_clauses(text))['applicable']==active

def test_shared_transfer():
 clauses=parse_contract_clauses('未经定作方同意，承揽方不得将主要加工工作转交第三方完成。')
 assert applicability('work_main_subcontract_consent',clauses)['applicable']
 assert applicability('work_illegal_total_subcontract',clauses)['applicable']

@pytest.mark.parametrize('text,expected',[
 ('合同未付报酬。',(True,True,False)),
 ('承揽人有权留置成果。',(True,True,False)),
 ('承揽人不得留置成果。',(False,False,True)),
])
def test_lien_exclusion(text,expected):
 clauses=parse_contract_clauses(text)
 assert tuple(applicability('work_'+n,clauses)['applicable'] for n in ['contractor_lien_condition','lien_notice_scope','lien_exclusion'])==expected


def test_fixed_work_contract_final_scenarios():
 from pathlib import Path
 from review_v2.engine import review_contract_v2
 text=(Path(__file__).resolve().parents[2]/'artifacts/work85/source.txt').read_text(encoding='utf8')
 result=review_contract_v2(text,'work',use_llm=False)
 rows={r['item_id']:r for r in result['items']}
 for key in ['COMMON-23-01','W-03-03','W-10-03']:
  assert rows[key]['coverage_status']=='不适用'
 assert rows['W-03-04']['applicability']['applicable']
 for key in ['W-04-03','W-04-04']:
  assert rows[key]['coverage_status']=='部分覆盖'
 assert result['release_quality_gate']['status']=='REPORT_READY'
