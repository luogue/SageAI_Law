import pytest
from review_v2.brokerage_facts import requirements
from review_v2.clause_parser import parse_contract_clauses
from review_v2.lease_semantics import corpus_facts

HEADER='中介合同\n甲方（委托人）：甲公司\n乙方（中介人）：乙公司\n'

@pytest.mark.parametrize('node,text,expected',[
 ('remuneration_condition_concluded_contract','如果乙方的中介获得成功，则甲方应向乙方支付中介报酬。',True),
 ('remuneration_condition_concluded_contract','中介成功后，甲方支付佣金。',True),
 ('remuneration_condition_concluded_contract','中介成功后，甲方无需支付佣金。',False),
 ('media_service_both_parties_bear','甲方向乙方支付中介报酬。',True),
 ('media_service_both_parties_bear','中介费由甲方支付。',True),
 ('media_service_both_parties_bear','委托人向中介人支付佣金。',True),
 ('media_service_both_parties_bear','乙方有权向甲方收取中介服务费。',True),
 ('media_service_both_parties_bear','本合同涉及中介费。',False),
 ('media_service_both_parties_bear','乙方向甲方支付中介报酬。',False),
 ('media_service_both_parties_bear','甲方无需向乙方支付中介报酬。',False),
 ('brokerage_contract_nature','乙方接受委托引荐第三方，促成双方签订协议。',True),
 ('brokerage_not_agency_or_commission','乙方介绍交易对象，撮合双方签订合同。',True),
 ('media_brokerage_scope','乙方负责撮合交易。',True),
 ('media_brokerage_scope','本合同的第三方为客户。',False),
 ('media_brokerage_scope','乙方不负责撮合交易。',False),
 ('brokerage_contract_nature','乙方不负责引荐第三方。',False),
 ('bypass_remuneration_liability','甲方不得私下与第三方接触。',False),
 ('bypass_remuneration_liability','甲方不得私下与第三方接触规避应支付的中介费。',True),
 ('used_opportunity_evidence','甲方与乙方介绍的购买方签订合同。',True),
 ('accepted_service_evidence','乙方提交报备确认单，经甲方签字确认。',True),
 ('accepted_service_evidence','乙方提交报备确认单，无需甲方签字确认。',False),
])
def test_concept_positive_and_negative(node,text,expected):
    corpus=HEADER+text
    spec=requirements(corpus)[node][0]
    assert bool(corpus_facts(parse_contract_clauses(corpus),[spec])[spec['element_id']]) is expected


def test_no_contact_alone_does_not_complete_composite():
    text=HEADER+'甲方不得私下与第三方接触规避应支付的中介费。'
    specs=requirements(text)['bypass_order_three_elements']
    facts=corpus_facts(parse_contract_clauses(text),specs)
    assert facts['broker_bypass_contract']
    assert not facts['broker_service_received']
    assert not facts['broker_opportunity_used']


def test_role_swap_preserves_payment_direction():
    text='乙方（委托人）：客户\n甲方（中介人）：中介\n乙方向甲方支付中介费用。'
    spec=requirements(text)['media_service_both_parties_bear'][0]
    assert corpus_facts(parse_contract_clauses(text),[spec])[spec['element_id']]
