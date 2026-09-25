import pytest
from review_v2.security_property_checklist import DEBT
from review_v2.priority_checklist_helpers import PROFILES
from review_v2.lease_semantics import corpus_facts
from review_v2.clause_parser import parse_contract_clauses
from review_v2.sale_evidence import PROFILES as SALE, supports

@pytest.mark.parametrize('text,expected', [
 ('主合同债务人：某设备有限公司。', [False,True]),
 ('主合同编号：LOAN-2026-01。债务人：某设备有限公司。',[True,True]),
 ('双方订立担保协议。',[False,False]),
 ('双方于2026年5月1日签订的2026年借字第123号《借款合同》。债务人：某贸易公司。',[True,True]),
])
def test_independent_debt_atoms(text,expected):
 specs=PROFILES['security_main_debt'][:2]
 facts=corpus_facts(parse_contract_clauses(text),specs)
 assert [bool(facts[s['element_id']]) for s in specs]==expected

@pytest.mark.parametrize('text,expected', [
 ('本合同生效后，甲乙双方不得擅自解除合同。',False),
 ('本合同自双方盖章之日起生效。',True),
 ('甲方盖章：乙方盖章：',False),
 ('本合同一经生效，双方应履行义务。',False),
 ('自合同生效之日起三日内交付。',False),
 ('本合同有效期内应妥善保管。',False),
 ('本合同经法定代表人签字并加盖公章后生效。',True),
 ('本合同自2026年10月1日起生效。',True),
 ('本合同经审批后生效。',True),
 ('本合同自质物移交完毕之日起生效。',True),
])
def test_actual_effectiveness_trigger(text,expected):
 assert supports(SALE['common_effective_clause'][0],text)==expected

@pytest.mark.parametrize('identity,expected', [
 ('主合同债务人：某设备有限公司。','部分覆盖'),
 ('主合同编号：LOAN-2026-01。主合同债务人：某设备有限公司。','通过'),
 ('','缺失'),
])
def test_production_atomic_aggregation_and_audit(identity,expected):
 from review_v2.engine import review_contract_v2
 financial='主债权金额：300000元。主债务履行期限：2027年9月8日。' if identity else ''
 r=review_contract_v2('动产质押合同。'+identity+financial+'本合同生效后，双方不得擅自解除合同。','movable_pledge',use_llm=False)
 by={i['item_id']:i for i in r['items']}
 assert by['SEC-01-01']['coverage_status']==expected
 assert by['S-00-01']['coverage_status']!='通过'
 for i in r['items']:
  found={e['element_id'] for e in i['coverage_elements'] if e['status']=='COVERED'}
  assert not found & {a['element_id'] for a in i['decision_trace'].get('element_absence_searches',[]) if a['result']=='NOT_FOUND'}
