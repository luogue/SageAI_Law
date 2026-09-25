import pytest
from review_v2.security_context import corporate_context,resolve
from review_v2.security_property_checklist import MOVABLE_ASSET
from review_v2.priority_checklist_helpers import PROFILES
from review_v2.lease_semantics import corpus_facts
from review_v2.clause_parser import parse_contract_clauses

@pytest.mark.parametrize('text,expected',[
 ('动产质押合同。',[False,False,False]),
 ('质物名称：工业控制柜。数量：5台。设备编号：DEV-123。',[True,True,True]),
 ('质物名称、数量、设备编号真实完整。',[False,False,False]),
 ('动产质押合同。\n附件一：质物清单\n质物名称：工业机器人\n数量：10台\n设备编号：RBT-2026-01。',[True,True,True]),
])
def test_actual_asset_values(text,expected):
 specs=PROFILES['pledge_movable_asset'][:3];facts=corpus_facts(parse_contract_clauses(text),specs)
 assert [bool(facts[s['element_id']]) for s in specs]==expected

@pytest.mark.parametrize('text,own,exception',[
 ('出质人：甲公司\n债务人：甲公司',True,False),
 ('出质人：甲公司\n债务人：乙公司',False,False),
 ('公司为自身债务提供担保。',True,False),
 ('非上市公司为其全资子公司开展经营活动提供担保。',False,True),
 ('上市公司为其全资子公司提供担保。',False,False),
])
def test_authority_context(text,own,exception):
 c=corporate_context(text);assert c['own_debt']==own;assert c['exception_claimed']==exception

@pytest.mark.parametrize('text,phrase,absent',[
 ('不动产抵押合同','抵押登记','交付质物前'),
 ('动产质押合同','现占有人','质押登记'),
 ('股权质押合同','对应权利质押登记','交付质物前'),
 ('应收账款质押合同','专项登记','交付质物前'),
])
def test_security_publicity_context(text,phrase,absent):
 rows=resolve('security_prior_encumbrances',PROFILES['security_prior_encumbrances'],text)
 instruction=rows[1]['verification_instruction'];assert phrase in instruction;assert absent not in instruction

@pytest.mark.parametrize('body,optional',[
 ('双方签订合同。',False),
 ('质物名称：工业控制柜。数量：5台。设备编号：DEV-123。',True),
])
def test_asset_priority_depends_on_actual_gap(body,optional):
 from review_v2.engine import review_contract_v2
 r=review_contract_v2('动产质押合同。'+body,'movable_pledge',use_llm=False)
 i=next(i for i in r['items'] if i['item_id']=='PLG-01-01')
 assert i['action_priority'] in ({'C_OPTIMIZATION'} if optional else {'B_PRACTICAL','A_CORE'})

@pytest.mark.parametrize('body,covered',[
 ('甲方已形成《董事会决议》。甲方应提供上述决议。法定代表人或授权的委托代理人签字。',True),
 ('甲方未提供任何授权信息。',False),
])
def test_company_authority_evidence_and_priority(body,covered):
 from review_v2.engine import review_contract_v2
 r=review_contract_v2('动产质押合同。\n出质人：甲有限公司\n主合同债务人：乙有限公司\n'+body,'movable_pledge',use_llm=False)
 i=next(i for i in r['items'] if i['item_id']=='SEC-10-01')
 if covered: assert all(e['status']=='COVERED' for e in i['coverage_elements'])
 else: assert i['action_priority']!='C_OPTIMIZATION'
 assert i['needs_manual_review']

def test_authority_exception_remains_verification():
 rows=resolve('security_company_authority',PROFILES['security_company_authority'], '非上市公司为其全资子公司开展经营活动提供担保。')
 assert all(e['requirement_kind']=='EXTERNAL_VERIFICATION' for e in rows[:2])
 assert all(e['verification_priority']=='MEDIUM' for e in rows[:2])

@pytest.mark.parametrize('text', ['甲方未形成董事会决议。','甲方无需提供授权材料。'])
def test_negative_authority_is_not_positive(text):
 specs=PROFILES['security_company_authority'][:2]
 facts=corpus_facts(parse_contract_clauses(text),specs)
 assert not any(facts.values())

def test_serial_numbers_are_not_clause_enumerations():
 text='附件一：质物清单\n质物名称：控制柜\n设备编号：ABC20260101、ABC20260102、ABC20260103\n数量：3台'
 clauses=parse_contract_clauses(text)
 assert any('ABC20260101、ABC20260102、ABC20260103' in c.text for c in clauses)
