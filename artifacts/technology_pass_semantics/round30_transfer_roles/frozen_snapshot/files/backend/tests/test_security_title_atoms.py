import pytest
from review_v2.security_property_checklist import TITLE
from review_v2.priority_checklist_helpers import PROFILES
from review_v2.lease_semantics import corpus_facts
from review_v2.clause_parser import parse_contract_clauses

@pytest.mark.parametrize('text,expected', [
 ('甲方以其有权处分的财产作质押。',[False,True,False]),
 ('甲方系质物唯一合法所有权人，并有权处分。',[True,True,False]),
 ('质物为甲方与第三人共有，第三人已书面同意质押。',[False,False,True]),
 ('双方签订合同。',[False,False,False]),
 ('出质人对质物享有处分权。',[False,True,False]),
 ('甲方有权将该财产设定质押。',[False,True,False]),
 ('担保人有权以该财产提供担保。',[False,True,False]),
 ('出质人对质押财产具有合法处分权限。',[False,True,False]),
 ('质物归甲方所有。',[True,False,False]),
 ('甲方无权处分该财产。',[False,False,False]),
 ('甲方是否有权处分的财产尚待核实。',[False,False,False]),
 ('质物为共有，第三人尚未书面同意质押。',[False,False,False]),
])
def test_independent_title_authority_atoms(text,expected):
 specs=PROFILES['security_title_authority']
 facts=corpus_facts(parse_contract_clauses(text),specs)
 assert [bool(facts[e['element_id']]) for e in specs]==expected

@pytest.mark.parametrize('text,expected', [
 ('甲方以其有权处分的财产作质押。','部分覆盖'),
 ('双方约定办理财产交接。','缺失'),
])
def test_final_aggregation_and_search_audit(text,expected):
 from review_v2.engine import review_contract_v2
 r=review_contract_v2('动产质押合同。'+text,'movable_pledge',use_llm=False)
 item=next(i for i in r['items'] if i['item_id']=='SEC-03-01')
 assert item['coverage_status']==expected
 found={e['element_id'] for e in item['coverage_elements'] if e['status']=='COVERED'}
 assert not found & {a['element_id'] for a in item['decision_trace'].get('element_absence_searches',[]) if a['result']=='NOT_FOUND'}
 if found:
  assert found=={'security_title_authority_2'}
  assert any('有权处分' in e.get('text','') for e in item['evidence_clauses'])
