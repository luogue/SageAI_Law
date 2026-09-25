import pytest
from review_v2.brokerage_facts import requirements
from review_v2.clause_parser import parse_contract_clauses
from review_v2.lease_semantics import corpus_facts

HEADER='中介合同\n甲方（委托人）：客户公司\n乙方（中介人）：中介公司\n'

@pytest.mark.parametrize('node,index,text,expected',[
 ('principal_no_obstruction',0,'甲方不得无故拒绝、拖延提供乙方履行中介服务所必需的协助与配合。',True),
 ('principal_no_obstruction',0,'甲方不得拖延中介服务履行。',True),
 ('principal_no_obstruction',0,'乙方不得拒绝甲方提供的协助。',False),
 ('principal_no_obstruction',0,'甲方不得拒绝提供运输服务。',False),
 ('principal_no_obstruction',0,'甲方应提供必要协助。',False),
 ('principal_no_obstruction',0,'甲方可以拒绝乙方要求的中介服务配合。',False),
 ('service_period_and_area',1,'乙方接受甲方委托，为该项目提供中介服务。',True),
 ('service_period_and_area',1,'中介服务仅限于指定公司的股权交易。',True),
 ('service_period_and_area',1,'甲方拥有本项目和标的公司。',False),
 ('service_period_and_area',1,'乙方为该项目不提供中介服务。',False),
 ('best_efforts_obligation',0,'乙方接受甲方委托，为该项目引荐客户，并促成双方签订合同。',True),
 ('best_efforts_obligation',0,'乙方负责促成双方签订合同。',True),
 ('best_efforts_obligation',0,'如果乙方最终促成双方签订合同，甲方应支付佣金。',False),
 ('best_efforts_obligation',0,'乙方接受甲方委托，如果引荐客户并最终促成双方签订合同，甲方支付报酬。',False),
 ('best_efforts_obligation',0,'乙方无需促成双方签订合同。',False),
])
def test_targeted_obligation_scope(node,index,text,expected):
    corpus=HEADER+text
    spec=requirements(corpus)[node][index]
    assert bool(corpus_facts(parse_contract_clauses(corpus),[spec])[spec['element_id']]) is expected
