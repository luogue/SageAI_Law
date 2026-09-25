import pytest
from review_v2.security_property_checklist import TITLE
from review_v2.priority_checklist_helpers import PROFILES
from review_v2.lease_semantics import corpus_facts
from review_v2.clause_parser import parse_contract_clauses

@pytest.mark.parametrize('text,expected', [
 ('甲方合法所有并有权处分该财产。',[True,True,False]),
 ('该设备归甲方所有。',[True,False,False]),
 ('甲方有权处分该设备。',[False,True,False]),
 ('甲方系唯一合法所有权人，并具有完整处分权。',[True,True,False]),
 ('甲方确认：上述质物均为甲方合法所有并有权处分的财产，质物名称、型号、数量、设备编号及权属证明真实、完整。',[True,True,False]),
])
def test_shared_span_retains_all_supports(text,expected):
 specs=PROFILES['security_title_authority'];facts=corpus_facts(parse_contract_clauses(text),specs)
 assert [bool(facts[e['element_id']]) for e in specs]==expected
 if all(expected[:2]):
  a,b=[facts[e['element_id']][0] for e in specs[:2]]
  assert (a['text'],a['clause_id'],a['location'])==(b['text'],b['clause_id'],b['location'])
  assert a['supports_element_ids']!=b['supports_element_ids']

def test_completeness_declaration_is_not_asset_values():
 spec=PROFILES['pledge_movable_asset'][0]
 assert not corpus_facts(parse_contract_clauses('质物名称、型号、数量、设备编号及权属证明真实、完整。'),[spec])[spec['element_id']]

def test_final_gate_blocks_conflicting_audit():
 from review_v2.final_context_consistency import verify
 r={'items':[{'item_id':'GENERIC','coverage_elements':[{'element_id':'ownership','status':'COVERED','evidence_ids':['C1']}],
 'decision_trace':{'element_absence_searches':[{'element_id':'ownership','result':'NOT_FOUND'}]}}]}
 assert verify(r)['status']=='BLOCKED'
 r['items'][0]['decision_trace']['element_absence_searches'][0]['result']='FOUND'
 assert verify(r)['status']=='REPORT_READY'
