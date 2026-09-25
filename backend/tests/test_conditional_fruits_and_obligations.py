import pytest
from dataclasses import replace
from review_v2.shared_fact_concepts import pool, requirements
from review_v2.clause_parser import parse_contract_clauses
from review_v2.element_resolution import resolve_declared_conditions
from review_v2.priority_contract_review import judge
from review_v2.safekeeping_contract_checklist import SAFEKEEPING_REVIEW_CHECKLIST

def decide(node,text):
    c=next(c for c in SAFEKEEPING_REVIEW_CHECKLIST if c.node_id==node)
    return judge(replace(c,item_id='UNRELATED-ID'),parse_contract_clauses(text))

@pytest.mark.parametrize('body,status',[
 ('保管物为普通机器设备。乙方应当将保管物归还甲方。','通过'),
 ('保管物为牲畜。乙方应当将保管物归还甲方。','部分覆盖'),
 ('保管期间产生的投资收益应予记录。乙方应当将保管物归还甲方。','部分覆盖'),
 ('保管物产生利息。乙方应当返还原物，并应当返还全部利息。','通过'),
 ('保管物为果树。','缺失'),
])
def test_fruits_only_in_triggered_scenario(body,status):
    assert decide('safekeeping_return_item_fruits',body).coverage_status==status

def test_no_fruits_scenario_excludes_atom_not_original_property():
    active,conditions=resolve_declared_conditions(requirements(['return_entrusted_property','return_property_fruits']),parse_contract_clauses('保管物为机器设备。'))
    assert [e['element_id'] for e in active]==['return_entrusted_property']
    assert conditions[0]['status']=='NOT_APPLICABLE'
    assert conditions[0]['risk_relevant'] is False

@pytest.mark.parametrize('text,pack,assist',[
 ('包装存在轻微挤压痕迹。',False,False),
 ('甲方向乙方移交保管物。',False,False),
 ('甲方应按照乙方合理要求完成必要包装并协助交付。',True,True),
 ('寄存人须提供适当包装。',True,False),
 ('交付方应配合入库清点。',False,True),
 ('甲方无需提供包装，也不必协助交付。',False,False),
 ('乙方应保持包装封闭。',False,False),
])
def test_description_and_behavior_are_not_duties(text,pack,assist):
    facts=pool(parse_contract_clauses(text),['depositor_packaging_duty','depositor_delivery_assistance'])
    assert bool(facts['depositor_packaging_duty'])==pack
    assert bool(facts['depositor_delivery_assistance'])==assist

def test_compound_duties_require_both_atoms():
    assert decide('safekeeping_depositor_packaging','寄存人须提供适当包装。').coverage_status=='部分覆盖'
    assert decide('safekeeping_depositor_packaging','包装挤压，甲方向乙方移交保管物。').coverage_status=='缺失'

def test_return_source_reused_by_separate_rules():
    text='乙方应当将保管物归还甲方。'
    a=decide('safekeeping_keep_return_purpose',text)
    b=decide('safekeeping_return_item_fruits',text)
    assert a.evidence_clauses[0]['quote']==b.evidence_clauses[0]['quote']

@pytest.mark.parametrize('attachment,expected',[
    ('\n附件\n接收清单：一台机器。','VALID'),('', 'UNVERIFIED'),
])
def test_unnumbered_reference_keeps_real_source(attachment,expected):
    from review_v2.contract_references import analyze, requirements as reference_requirements
    from review_v2.lease_semantics import corpus_facts
    clauses=parse_contract_clauses('第一条\n收到物品后出具接收清单（详见附件）。'+attachment)
    rows=analyze(clauses)['common_internal_references']
    assert rows and rows[0]['status']==expected
    if expected=='VALID':
        reqs=reference_requirements('common_internal_references',clauses)
        assert all(corpus_facts(clauses,reqs).values())

def test_final_nontriggered_atom_has_no_negative_audit():
    from review_v2.engine import review_contract_v2
    r=review_contract_v2('保管合同\n第一条\n保管物为机器设备。乙方应当将保管物归还甲方。','deposit',use_llm=False)
    item=next(i for i in r['items'] if i['node_id']=='safekeeping_return_item_fruits')
    assert item['coverage_status']=='通过'
    assert not any(a.get('element_id')=='return_property_fruits' for a in item['decision_trace'].get('element_absence_searches',[]))
    assert not item['related_risks']
