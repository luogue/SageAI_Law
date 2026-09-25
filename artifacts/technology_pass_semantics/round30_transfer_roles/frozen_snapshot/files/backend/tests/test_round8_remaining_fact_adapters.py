from copy import deepcopy
import pytest
from review_v2 import engine
from review_v2.clause_parser import parse_contract_clauses
from review_v2.license_control_facts import elements
from review_v2.ancillary_fee_facts import elements as fee_elements
from tests.test_technology_exact_truth_pipeline import make_item


@pytest.mark.parametrize('family,text,key', [
    ('license_scope_remedies', '受让方超出许可范围，应停止使用并赔偿实际损失。', 'over_scope_breach_remedy'),
    ('license_mutual_confidentiality', '双方对算法和客户资料承担保密义务；未经提供方书面同意不得向第三方披露。双方保密义务在合同终止后五年持续有效。', 'mutual_confidentiality_responsibility'),
    ('license_secret_controls', '技术秘密为未公开的源代码。\n第二条 为生产合同产品之目的可以复制和编译。\n第三条 不得超出本合同目的使用。', 'purpose_scoped_copying_boundary'),
])
def test_license_typed_sources_retain_exact_parser_spans(family,text,key):
    clauses = parse_contract_clauses('第一条\n'+text)
    atom = next(r for r in elements(family,clauses) if r['element_id']==key)
    assert atom['status']=='COVERED'
    by_id={c.clause_id:c for c in clauses}
    for source in atom['supporting_evidence']:
        assert source['quote'] in by_id[source['clause_id']].text
    item=make_item();item.item_id='TC-07-03';item.coverage_status='通过'
    item.coverage_elements=[atom]
    engine._adapt_atomic_candidate_sources(item,family,clauses)
    engine._enrich_evidence_sources([item]);engine._attach_evidence_traceability([item],clauses)
    engine._verified_pass_sources([item],clauses,downgrade=True)
    assert item.decision_trace['verified_pass_source_gate']['status']=='PASS'


@pytest.mark.parametrize('family,text,key', [
    ('license_scope_remedies', '双方承担保密义务，甲方应支付许可费。', 'over_scope_breach_remedy'),
    ('license_mutual_confidentiality', '甲方对技术秘密承担保密义务。乙方支付服务费。', 'mutual_confidentiality_responsibility'),
    ('license_secret_controls', '甲方可以复制技术资料。', 'purpose_scoped_copying_boundary'),
])
def test_licence_other_obligations_are_not_control_or_remedy(family,text,key):
    assert next(r for r in elements(family,parse_contract_clauses(text)) if r['element_id']==key)['status']=='MISSING'


def test_licence_title_price_and_delivery_do_not_define_confidential_scope():
    clauses=parse_contract_clauses('技术秘密许可合同\n第一条 技术秘密许可费为20万元。\n第二条 乙方应交付完整技术资料。')
    scope=next(r for r in elements('license_mutual_confidentiality',clauses) if r['element_id']=='confidential_information_scope')
    assert scope['status']=='MISSING'
    assert scope['supporting_evidence']==[]


def test_named_confidential_category_with_an_obligation_is_scope_evidence():
    clauses=parse_contract_clauses('第七条 双方对履约中知悉的技术秘密承担保密义务。')
    scope=next(r for r in elements('license_secret_controls',clauses) if r['element_id']=='confidential_information_scope')
    assert scope['status']=='COVERED'
    assert scope['supporting_evidence'][0]['quote'] in clauses[0].text


def test_general_remedy_in_same_provision_keeps_its_separate_span():
    text='第一条 买方超出许可范围应停止使用并赔偿直接损失；一般违约赔偿总额不超过已付费用的30%，故意或重大过失不适用该上限。'
    clauses=parse_contract_clauses(text)
    atoms={r['element_id']:r for r in elements('license_scope_remedies',clauses)}
    assert atoms['over_scope_liability_cap']['status']=='COVERED'
    assert all('一般违约' in r['quote'] and r['quote'] in clauses[0].text
               for r in atoms['over_scope_liability_cap']['supporting_evidence'])
    unrelated=parse_contract_clauses('第一条 买方超出许可范围应赔偿损失。\n第二条 卖方泄密赔偿总额不超过10万元。')
    assert next(r for r in elements('license_scope_remedies',unrelated) if r['element_id']=='over_scope_liability_cap')['status']=='MISSING'


@pytest.mark.parametrize('text,expected', [
    ('技术服务费用已包含在转让费中。', 'COVERED'),
    ('技术服务费为人民币5000元。', 'COVERED'),
    ('乙方应提供技术服务。', 'MISSING'),
    ('乙方提供现场技术服务不超过8个工作日。超过约定工作量的服务另行协商收费。', 'PARTIALLY_COVERED'),
])
def test_fee_inclusion_requires_a_price_relation_not_a_service_duty(text,expected):
    by_id={r['element_id']:r for r in fee_elements(parse_contract_clauses(text))}
    assert by_id['service_fee_amount']['status']==expected


def test_partial_price_arrangement_keeps_fact_presence_separate_from_completeness():
    clauses=parse_contract_clauses('第一条 乙方提供现场技术服务不超过8个工作日。超过约定工作量的服务另行协商收费。')
    atom=next(r for r in fee_elements(clauses) if r['element_id']=='service_fee_amount')
    item=make_item(); item.item_id='TC-09-04'; item.coverage_status='部分覆盖'
    item.coverage_elements=[atom]
    engine._adapt_atomic_candidate_sources(item,'ancillary_fee',clauses)
    engine._enrich_evidence_sources([item]);engine._attach_evidence_traceability([item],clauses)
    engine._verified_pass_sources([item],clauses,downgrade=True)
    element=item.coverage_elements[0]
    assert element['fact_status']=='FOUND'
    assert element['status']==element['requirement_status']=='PARTIALLY_COVERED'
    assert element['supporting_evidence_ids']
    assert element['residual_gap']
    original_sources=deepcopy(element['supporting_evidence'])
    engine._apply_technical_secret_transfer_semantic_rules([item],
        '第一条 乙方提供现场技术服务不超过8个工作日。超过约定工作量的服务另行协商收费。\n第二条 固定技术转让费100万元，分三期支付。',
        {'primary_subtype':'TECHNOLOGY_TRANSFER','tertiary_subtype':'TECHNICAL_SECRET_TRANSFER'})
    projected=next(e for e in item.coverage_elements if e['element_id']=='service_fee_amount')
    assert projected['supporting_evidence']==original_sources
    assert projected['source_clause_ids']==[s['clause_id'] for s in original_sources]
    assert projected['source_spans']==[s['quote'] for s in original_sources]
    assert projected['fact_status']=='FOUND'


@pytest.mark.parametrize('party,expected', [('甲方','PASS'),('乙方','BLOCKED')])
def test_cap_orientation_requires_verified_source_and_matching_review_context(party,expected):
    text='技术服务合同\n甲方（服务提供方）：技术公司\n乙方（服务接受方）：客户公司\n甲方承担的全部赔偿责任不超过乙方已经支付的服务费。'
    clauses=parse_contract_clauses(text)
    atom=engine._atomic_requirement_family('service_liability',clauses)[0]
    assert atom['status']=='COVERED'
    item=make_item();item.item_id='TECH-SHARED-08';item.coverage_status='通过'
    item.coverage_elements=[dict(atom,status='ADVERSE',risk_relevant=False)]
    engine._adapt_atomic_candidate_sources(item,'service_liability',clauses)
    item.decision_trace['orientation_provenance']={'review_context':{'canonical_role':'SERVICE_PROVIDER','party_label':party},'source_fact_key':atom['source_fact_key']}
    engine._enrich_evidence_sources([item]);engine._attach_evidence_traceability([item],clauses)
    engine._verified_pass_sources([item],clauses,downgrade=True)
    assert item.decision_trace['verified_pass_source_gate']['status']==expected
    if expected=='PASS':
        assert item.coverage_elements[0]['fact_status']=='FOUND'
        assert item.coverage_elements[0]['requirement_status']=='ADVERSE'
