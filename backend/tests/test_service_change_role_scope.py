"""Modal force, remedy direction and phase are separate evidence dimensions."""
from types import SimpleNamespace
import pytest
from review_v2.service_scenarios import PROFILES, profiles_for, extract_facts
from review_v2.clause_parser import parse_contract_clauses
from review_v2.utility_supply_evidence import _find_supports
from review_v2.lease_semantics import supports
from review_v2.prerequisite_resolution import prerequisite_status_failures

@pytest.mark.parametrize('node',['provider_change_requires_consent','change_record_and_confirmation'])
@pytest.mark.parametrize('text',[
    '合同未尽事宜，双方可以签订书面补充协议。',
    '尚未约定的事项，可另行书面补充。',
    '服务变更可以采用书面形式。',
])
def test_permissive_supplement_does_not_prove_mandatory_change(node,text):
    assert not _find_supports(parse_contract_clauses(text),node,PROFILES[node])[0]

@pytest.mark.parametrize('node,text',[
    ('provider_change_requires_consent','服务内容变更必须经双方协商一致。'),
    ('provider_change_requires_consent','经双方同意方可变更本合同。'),
    ('change_record_and_confirmation','本合同变更须采用书面形式。'),
    ('change_record_and_confirmation','双方应通过邮件确认服务变更。'),
])
def test_mandatory_existing_change_has_direct_evidence(node,text):
    assert _find_supports(parse_contract_clauses(text),node,PROFILES[node])[0]

@pytest.mark.parametrize('provider,customer',[('甲方','乙方'),('乙方','甲方')])
def test_quality_remedy_requires_provider_breach_and_customer_right(provider,customer):
    clauses=parse_contract_clauses(f'{provider}（服务提供方）：某公司\n第一条 {customer}严重违反合同，经书面催告仍不改正，{provider}有权解除合同。\n第二条 {provider}经{customer}书面催告仍不符合服务质量标准，{customer}有权解除合同。')
    node='service_quality_nonconform_remedy'
    found,rows=_find_supports(clauses,node,profiles_for(clauses)[node])
    assert found=={'failed_cure_remedy'}
    assert len(rows)==1 and rows[0]['location'].startswith('第二条')
    spec=profiles_for(clauses)[node][1]
    assert not supports({'element_id':spec[0],'semantic_patterns':[spec[2]]},
                        {'text':f'{customer}经催告仍不符合服务质量标准，{provider}有权解除合同。','clause_id':'wrong','location':'第一条'})

def test_generic_early_exit_does_not_prove_indefinite_stage_procedure():
    clauses=parse_contract_clauses('第一条 期满后期限转为不定期。\n第二条 甲方提前60日通知可以解除合同。')
    found,rows=_find_supports(clauses,'indefinite_service_termination',PROFILES['indefinite_service_termination'])
    assert found=={'indefinite_continuation'}
    assert extract_facts(clauses)['indefinite']['evidence'][0]['location'].startswith('第一条')

def test_explicit_indefinite_notice_is_supported():
    clauses=parse_contract_clauses('转为不定期服务后，任一方解除合同须提前60日通知对方。')
    assert 'termination_notice' in _find_supports(clauses,'indefinite_service_termination',PROFILES['indefinite_service_termination'])[0]

def test_applicability_without_direct_source_is_blocked():
    item=SimpleNamespace(item_id='SVC',coverage_status='部分覆盖',applicability={
        'depends_on':['indefinite'],'trigger_facts':[{'key':'indefinite','value':True,'requires_direct_evidence':True,'evidence':[]}]})
    assert prerequisite_status_failures([item])[0]['requirement']=='APPLICABILITY_EVIDENCE_MISSING'
