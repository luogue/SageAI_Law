from dataclasses import replace
import pytest
from review_v2.shared_fact_concepts import pool
from review_v2.clause_parser import parse_contract_clauses
from review_v2.safekeeping_contract_checklist import SAFEKEEPING_REVIEW_CHECKLIST
from review_v2.engine import _is_checkpoint_applicable, review_contract_v2

@pytest.mark.parametrize('text,applicable',[
 ('保管费按每月人民币2000元计算。',False),
 ('服务费为每天50元。',False),
 ('双方约定不收取报酬。',False),
 ('本合同为无偿保管。',False),
 ('保管费金额待协商确定。',True),
 ('合同仅约定保管期限。',True),
 ('保管费例如每月2000元，实际金额待定。',True),
 ('除退还保管费用外，每提前1日支付人民币200元违约金。',True),
 ('逾期领取时，按每日人民币300元支付额外费用。',True),
])
def test_unresolved_base_prerequisite_is_generic(text,applicable):
 source=next(c for c in SAFEKEEPING_REVIEW_CHECKLIST if c.unless_fact_concepts)
 arbitrary=replace(source,item_id='OTHER-DEFAULT',node_id='another_default')
 assert _is_checkpoint_applicable(text,arbitrary,'deposit')[0]==applicable

@pytest.mark.parametrize('text,unauthorized,authorized',[
 ('乙方未经甲方同意，将物品转交第三人保管，造成损失的应承担赔偿责任。',True,False),
 ('受托人未经委托人同意，委托第三人处理物品造成损失，应承担赔偿责任。',True,False),
 ('经寄存人同意转保管的，保管人仍应对第三人的行为承担赔偿责任。',False,True),
 ('未经同意转交第三人造成损失，不承担赔偿责任。',False,False),
])
def test_authorization_scenarios_remain_separate(text,unauthorized,authorized):
 facts=pool(parse_contract_clauses(text),['unauthorized_delegation_liability','authorized_delegation_liability'])
 assert bool(facts['unauthorized_delegation_liability'])==unauthorized
 assert bool(facts['authorized_delegation_liability'])==authorized

def test_same_transfer_source_reused_without_rule_exclusivity():
 text='乙方未经甲方同意，将物品转交第三人保管，造成损失的应承担赔偿责任。'
 facts=pool(parse_contract_clauses(text),['unauthorized_delegation_control','unauthorized_delegation_liability'])
 a,b=facts.values()
 assert a and b
 assert a[0]['clause_id']==b[0]['clause_id'] and a[0]['quote']==b[0]['quote']

def test_supporting_second_sentence_is_retained():
 text='因保管不善造成物品损失，应承担赔偿责任。无偿保管的，乙方证明自己没有故意或者重大过失的，不承担赔偿责任。'
 facts=pool(parse_contract_clauses(text),['gratuitous_fault_standard'])
 assert facts['gratuitous_fault_standard']
 assert all('无偿' in e['quote'] and '故意或者重大过失' in e['quote'] for e in facts['gratuitous_fault_standard'])

def test_general_negligence_sentence_cannot_prove_gratuitous_standard():
 facts=pool(parse_contract_clauses('因保管不善造成物品损失，应承担赔偿责任。'),['gratuitous_fault_standard'])
 assert not facts['gratuitous_fault_standard']

@pytest.mark.parametrize('body,expected',[
 ('乙方未经甲方同意，将物品转交第三人保管，造成损失的应承担赔偿责任。','部分覆盖'),
 ('正常领取物品。','缺失'),
])
def test_final_aggregation_and_audit(body,expected):
 result=review_contract_v2('保管合同\n第一条\n'+body,'deposit',use_llm=False)
 item=next(i for i in result['items'] if i['node_id']=='safekeeping_transfer_liability')
 assert item['coverage_status']==expected
 for e in item['coverage_elements']:
  if e['status']=='COVERED':
   assert e['evidence_ids']
   assert e['proposition'] not in item['risk_point_description']
   assert not any(a.get('element_id')==e['element_id'] and a.get('result')=='NOT_FOUND' for a in item['decision_trace'].get('element_absence_searches',[]))
 assert result['release_quality_gate']['status']=='REPORT_READY'
