import pytest
from review_v2.security_property_checklist import EQUITY_PLEDGE_CHECKLIST
from review_v2.priority_checklist_helpers import PROFILES
from review_v2.security_context import resolve
from review_v2.lease_semantics import corpus_facts
from review_v2.clause_parser import parse_contract_clauses
HEADER='股权质押合同\n甲方（质权人）：贷款公司\n乙方（出质人）：投资公司\n'

@pytest.mark.parametrize('node,index,body',[
 ('security_main_debt',0,'双方于本协议签署日签订《资产转让合同》。'),
 ('security_main_debt',2,'剩余股权转让价款为人民币1,500,000元。'),
 ('security_main_debt',2,'尚欠转让价款：280000元。'),
 ('security_title_authority',0,'乙方合法持有目标公司80%的股权。'),
 ('security_title_authority',1,'乙方具有合法的权利和能力将该股权质押给甲方。'),
 ('security_prior_encumbrances',0,'乙方未在该股权上设置其他质押和权利负担。'),
 ('security_prior_encumbrances',0,'不存在其他担保或者权利负担。'),
 ('security_realization',0,'发生债务人违约或者其他依法可以实现质权的情形。'),
 ('security_realization',0,'债务人违约时，债权人有权实现质权。'),
 ('security_exercise_period',1,'全部债权完全清偿后，质权人应配合办理股权出质注销登记。'),
 ('security_exercise_period',1,'债务清偿后应办理质押注销。'),
 ('pledge_equity_asset',0,'乙方将其合法持有的目标公司80%股权质押。'),
 ('pledge_equity_registration',0,'乙方应在条件具备后及时办理股权质押登记。'),
 ('pledge_equity_registration',0,'出质人负责办理股权出质登记。'),
])
def test_semantic_equivalence(node,index,body):
 text=HEADER+body;spec=resolve(node,PROFILES[node],text)[index]
 assert corpus_facts(parse_contract_clauses(text),[spec])[spec['element_id']]

@pytest.mark.parametrize('node,index,body',[
 ('security_title_authority',0,'乙方并非合法持有目标公司股权。'),
 ('security_title_authority',1,'乙方不具有将该股权质押的权限。'),
 ('pledge_equity_registration',0,'乙方无需办理股权质押登记。'),
 ('pledge_equity_registration',1,'乙方应及时办理股权质押登记。'),
 ('pledge_equity_registration',1,'乙方应在收到变更要求后五日内完成股权质押变更登记。'),
 ('security_main_debt',0,'当事人可能另行签订某个转让合同。'),
 ('security_main_debt',2,'股权估值为人民币100000元。'),
])
def test_related_words_do_not_entail_fact(node,index,body):
 text=HEADER+body;spec=resolve(node,PROFILES[node],text)[index]
 assert not corpus_facts(parse_contract_clauses(text),[spec])[spec['element_id']]

def test_scope_is_recalled_across_numbered_subclauses():
 text=HEADER+'第三条 被担保的主债权\n（一）《资产转让合同》项下尚未支付的价款；\n（二）前述债务产生的利息；\n（三）为实现债权所支付的律师费。'
 specs=resolve('security_scope',PROFILES['security_scope'],text)
 facts=corpus_facts(parse_contract_clauses(text),specs)
 assert all(facts[e['element_id']] for e in specs)

def test_protocol_effectiveness_is_not_post_effect_reference():
 from review_v2.sale_evidence import PROFILES as SALE,supports
 spec=SALE['common_effective_clause'][0]
 assert supports(spec,'本协议在双方盖章并完成股权出质登记后生效。')
 assert not supports(spec,'本协议生效后，双方应当办理登记。')

def test_party_labels_are_resolved_from_roles():
 text='甲方（出质人）：投资公司\n乙方（质权人）：债权公司\n甲方合法持有目标公司60%的股权，并具有合法权利和能力将该股权质押给乙方。'
 specs=resolve('security_title_authority',PROFILES['security_title_authority'],text)[:2]
 facts=corpus_facts(parse_contract_clauses(text),specs)
 assert all(facts[e['element_id']] for e in specs)

def test_fixed_contract_repeat_evidence_status_consistency():
 from pathlib import Path
 from docx import Document
 from review_v2.engine import review_contract_v2
 from review_v2.report_statistics import coverage_bucket
 from collections import Counter
 text='\n'.join(p.text for p in Document(Path(__file__).resolve().parents[2]/'test_data/73 股权质押.docx').paragraphs)
 reports=[review_contract_v2(text,'equity_pledge',use_llm=False) for _ in range(2)]
 core=lambda r:[(i['item_id'],i['coverage_status'],[(e['element_id'],e['status'],e.get('source_spans')) for e in i['coverage_elements']]) for i in r['items']]
 assert core(reports[0])==core(reports[1])
 for r in reports:
  for i in r['items']:
   found={e['element_id'] for e in i['coverage_elements'] if e['status']=='COVERED'}
   assert not found & {a['element_id'] for a in i['decision_trace'].get('element_absence_searches',[]) if a['result']=='NOT_FOUND'}
  assert dict(Counter(coverage_bucket(i['coverage_status']) for i in r['items']))==r['coverage_summary']
  assert r['release_quality_gate']['status']=='REPORT_READY'
