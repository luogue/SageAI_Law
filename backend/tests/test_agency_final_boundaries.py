"""Operative relation boundaries; no report text or status injection."""
import pytest
from review_v2.agency_facts import specs
from review_v2.clause_parser import parse_contract_clauses
from review_v2.lease_semantics import corpus_facts


@pytest.mark.parametrize('node,text,expected',[
 ('agency_expense_advance','委托人应预付处理事务所需必要费用。',True),
 ('agency_expense_advance','甲方按预算预拨备用金。',True),
 ('agency_expense_advance','解除后双方结算已支付委托费用及必要费用。',False),
 ('agency_expense_advance','受托人垫付必要费用，委托人事后报销。',False),
 ('agency_expense_advance','委托人无需预付必要费用。',False),
 ('agency_expense_advance','委托人提前支付服务报酬。',False),
 ('agency_emergency_sub_entrustment','情况紧急，为维护委托人利益，受托人可转委托第三人处理。',True),
 ('agency_emergency_sub_entrustment','终止时存在紧急事务，受托人应采取必要措施维护委托人利益。',False),
 ('agency_emergency_sub_entrustment','紧急情况下为维护利益也不得转委托第三人。',False),
 ('agency_sub_entrustment_liability','转委托经委托人同意，受托人就第三人的选任和指示承担责任。',True),
 ('agency_sub_entrustment_liability','经甲方追认的转委托，乙方对第三人的选任及指示承担责任。',True),
 ('agency_sub_entrustment_liability','在委托人明确指示范围内协助谈判。',False),
 ('agency_sub_entrustment_liability','经委托人同意可以转委托第三人。',False),
 ('agency_power_of_attorney_attachment','附件一：授权委托书',True),
 ('agency_power_of_attorney_attachment','附件2：代理授权书',True),
 ('agency_power_of_attorney_attachment','全权委托：不适用。',False),
 ('agency_power_of_attorney_attachment','应当提供授权委托书作为附件一。',False),
])
def test_separate_relations(node,text,expected):
    req=specs()[node]
    assert bool(corpus_facts(parse_contract_clauses(text),req)[req[0]['element_id']])==expected


@pytest.mark.parametrize('text,paid,expected',[
 ('解除时间不当造成对方损失的，解除方应按照法律规定承担赔偿责任。',True,True),
 ('终止合同导致损失的，终止方应依法承担赔偿责任。',True,True),
 ('解除时间不当造成对方损失的，解除方应按照法律规定承担赔偿责任。',False,False),
 ('解除合同造成损失的，解除方依法承担赔偿责任，但不赔偿可得利益。',True,False),
 ('解除合同造成损失的，解除方仅赔偿直接损失。',True,False),
 ('发生违约造成损失的，应依法承担赔偿责任。',True,False),
])
def test_statutory_incorporation(text,paid,expected):
    req=specs(paid)['agency_termination_compensation_scope'][1]
    assert bool(corpus_facts(parse_contract_clauses(text),[req])[req['element_id']])==expected


@pytest.mark.parametrize('node,valid,unrelated',[
 ('agency_expense_advance','委托人预付必要费用。','解除后双方结算费用。'),
 ('agency_emergency_sub_entrustment','情况紧急为维护甲方利益，乙方可以转委托第三人。','终止后乙方应处理紧急事务。'),
 ('agency_sub_entrustment_liability','经同意转委托，受托人对选任及指示承担责任。','按委托人指示协助谈判。'),
 ('agency_power_of_attorney_attachment','附件一：授权委托书','全权委托：不适用。'),
])
def test_publication_rejects_neighbor_as_core_proof(node,valid,unrelated):
    from types import SimpleNamespace
    from review_v2.semantic_consistency import validate
    req=specs()[node]
    clauses=parse_contract_clauses(valid+'\n'+unrelated)
    evidence=corpus_facts(clauses,req)[req[0]['element_id']]
    assert evidence
    evidence[0]=dict(evidence[0],quote=unrelated,text=unrelated)
    item=SimpleNamespace(item_id='boundary',node_id=node,coverage_status='通过',
        evidence_clauses=evidence,coverage_elements=[dict(element_id=req[0]['element_id'],status='COVERED')],
        decision_trace={'require_canonical_validation':True,'semantic_requirements':req})
    assert validate([item],clauses)['status']=='BLOCKED'
