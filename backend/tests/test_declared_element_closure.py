from dataclasses import replace
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.shared_fact_concepts import requirements, pool
from review_v2.element_resolution import resolve_declared_conditions
from review_v2.priority_contract_review import judge
from review_v2.safekeeping_contract_checklist import SAFEKEEPING_REVIEW_CHECKLIST
from review_v2.engine import review_contract_v2

UNAUTHORIZED='乙方未经甲方同意，将保管物转交第三人保管，造成损失的应承担赔偿责任。'
@pytest.mark.parametrize('permission,liability,state',[
 ('甲方不允许乙方将保管物转交第三人保管。','', '通过'),
 ('甲方☐是☑否允许乙方将保管物转交第三人保管。','', '通过'),
 ('甲方允许乙方将保管物转交第三人保管。','', '部分覆盖'),
 ('甲方允许乙方将保管物转交第三人保管。','经甲方同意转保管的，乙方仍应承担赔偿责任。', '通过'),
])
def test_declared_element_scenarios(permission,liability,state):
    checkpoint=next(c for c in SAFEKEEPING_REVIEW_CHECKLIST if c.node_id=='safekeeping_transfer_liability')
    checkpoint=replace(checkpoint,item_id='ARBITRARY-RULE')
    result=judge(checkpoint,parse_contract_clauses(permission+UNAUTHORIZED+liability))
    assert result.coverage_status==state

def test_inactive_atom_removed_from_denominator():
    elements= requirements(['unauthorized_delegation_liability','authorized_delegation_liability'])
    active,conditions=resolve_declared_conditions(elements,parse_contract_clauses('不允许转交第三人保管。'))
    assert len(active)==1
    assert conditions[0]['element_applicability']=='CONDITIONAL_NOT_TRIGGERED'
    assert conditions[0]['risk_relevant'] is False

def test_direct_return_obligation_wins_over_party_and_valuables():
    clauses=parse_contract_clauses('第一条\n甲方（寄存人）：某公司。\n第二条\n乙方应当将保管物归还甲方。\n第三条\n贵重物品未声明。')
    facts=pool(clauses,['return_entrusted_property'])['return_entrusted_property']
    assert len(facts)==1 and '应当将保管物归还' in facts[0]['quote']

def test_clear_default_does_not_invent_legal_uncertainty():
    r=review_contract_v2('保管合同\n第一条\n保管费每月100元。','deposit',use_llm=False)
    item=next(i for i in r['items'] if i['node_id']=='safekeeping_lien_condition')
    assert item['coverage_status']=='缺失'
    assert item['decision_trace']['default_law_assessment']['status']=='CLEAR_DEFAULT'
    assert '法定留置权' in item['risk_point_description']
    assert '能否留置' not in item['risk_point_description']
    assert '操作程序' in item['legal_consequence_if_missing']
