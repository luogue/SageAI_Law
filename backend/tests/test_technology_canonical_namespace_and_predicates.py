"""Fact addresses and operative event predicates survive every consumer."""
import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.contract_facts import ContractFactGraph, canonical_fact_key
from review_v2.requirement_keys import canonical_requirement_key, normalize_requirement_supports
from review_v2.technology_fact_ontology import has_confidentiality_remedy


@pytest.mark.parametrize('alias', ['major_decision_process', 'technology.governance.major_decision',
                                   'TECHNOLOGY_GOVERNANCE_MAJOR_DECISION'])
def test_fact_namespace_roundtrip_does_not_become_flat_requirement(alias):
    clause = parse_contract_clauses('第一条 治理\n重大研发事项须双方书面一致同意。')[0]
    graph = ContractFactGraph()
    graph.add(alias, True, clause, source_span='重大研发事项须双方书面一致同意。')
    graph.add('technology.governance.major_decision', True, clause,
              source_span='重大研发事项须双方书面一致同意。')
    payload = {'coverage_elements': [{'element_id': 'MajorDecisionProcess',
        'source_fact_key': alias, 'required_fact_key': alias}],
        'direct_element_fact_keys': {'MajorDecisionProcess': alias},
        'direct_fact_bindings': {alias: [{'clause_id': clause.clause_id, 'quote': clause.text}]}}
    output = normalize_requirement_supports(payload)
    address = output['coverage_elements'][0]['source_fact_key']
    assert address == 'technology.governance.major_decision'
    assert output['direct_element_fact_keys']['major_decision_process'] == address
    assert canonical_requirement_key(address) == address
    assert list(output['direct_fact_bindings']) == [address]
    facts = graph.matching([address])
    assert len(facts) == 1
    assert facts[0].value is True and facts[0].normalized_value is True
    assert facts[0].source_spans == ['重大研发事项须双方书面一致同意。']
    assert normalize_requirement_supports(output) == output


def test_registered_dotted_element_alias_is_not_a_fact_namespace():
    assert canonical_requirement_key('technical.secret.identity.and.delivery.scope') == (
        'technical_secret_identity_and_delivery_scope')
    assert canonical_requirement_key('technology.transaction.entrusted_direction') == (
        'technology.transaction.entrusted_direction')


def test_alias_chain_resolves_one_document_fact_without_rewriting_raw_text():
    assert canonical_fact_key('development_documents.deployment_document_delivery') == (
        'development_documents.installation_deployment_document')
    output = normalize_requirement_supports({'source_fact_key': 'development_documents.deployment_document_delivery',
        'quote': '乙方提交部署说明；不是测试报告。'})
    assert output['quote'] == '乙方提交部署说明；不是测试报告。'
    assert output['source_fact_key'] == 'development_documents.installation_deployment_document'


@pytest.mark.parametrize('text', [
    '乙方违反保密义务的，应向甲方支付人民币十万元违约金。',
    '买方泄露技术秘密的，应向卖方赔偿因此发生的损失。',
    '任何一方违背保密约定时，应立即停止披露并赔偿对方损失。',
    '受让方违反本合同保密条款，必须向让与方支付约定违约金。',
])
def test_recipient_between_modality_and_remedy_is_not_a_missing_obligation(text):
    assert has_confidentiality_remedy(text)


@pytest.mark.parametrize('text', [
    '违反保密义务的赔偿责任最高不超过合同总价。',
    '除违反保密义务外，赔偿责任以开发费为上限。',
    '乙方违反保密义务时无需向甲方支付违约金。',
    '乙方应向甲方支付服务费，并遵守保密义务。',
    '保密范围另行约定。乙方应承担逾期交付的赔偿责任。',
])
def test_liability_cap_topic_or_other_event_does_not_prove_breach_remedy(text):
    assert not has_confidentiality_remedy(text)


@pytest.mark.parametrize('obligor,recipient', [('乙方', '甲方'), ('买方', '卖方'),
                                             ('被许可方', '许可方'), ('许可方', '被许可方')])
def test_recipient_is_not_reclassified_as_obligor_in_registry_projection(obligor, recipient):
    from review_v2 import engine
    from review_v2.verified_source import bind_original
    text = f'{obligor}违反保密义务的，应向{recipient}赔偿因此发生的损失。'
    clauses = parse_contract_clauses('第一条 责任\n' + text)
    graph = ContractFactGraph()
    engine._register_atomic_family_facts(graph, 'confidentiality_remedies', clauses)
    graph.freeze('remedy-registry-test')
    elements = engine._atomic_requirement_family('confidentiality_remedies', clauses)
    damage = next(e for e in elements if e['element_id'] == 'breach_damage_liability')
    assert damage['status'] == 'COVERED'
    assert {p['obligated_party'] for p in damage['party_coverage']} == {obligor}
    facts = graph.matching([damage['source_fact_key']])
    assert len(facts) == 1
    assert facts[0].source_spans == [text]
    assert damage['supporting_evidence'][0]['quote'] == facts[0].source_spans[0]
    proof = bind_original(damage['supporting_evidence'][0], clauses)
    assert proof['verified_original']
    assert next(e for e in elements if e['element_id'] == 'stop_use')['status'] == 'MISSING'


def test_source_summary_survives_projection_without_copying_another_actors_fact():
    from review_v2 import engine
    from review_v2.element_evidence_projection import project, audit
    from tests.test_technology_exact_truth_pipeline import make_item
    clauses = parse_contract_clauses(
        '第一条 乙方责任\n乙方违反保密义务的，应停止使用并向甲方赔偿损失。\n'
        '第二条 甲方责任\n甲方违反保密义务的，应向乙方赔偿损失。')
    item = make_item(); item.item_id = 'TC-11-04'
    engine._project_atomic_requirement_state(item, 'confidentiality_remedies', clauses, allow_empty=True)
    project([item], [], clauses)
    originals = [r for r in item.evidence_clauses if r['source_type'] == 'BODY']
    by_actor = {r['obligated_party']: r for r in originals}
    assert '乙方泄密后停止使用' in by_actor['乙方']['support_summary']
    assert '停止使用' not in by_actor['甲方']['support_summary']
    assert '甲方泄密损失赔偿责任' in by_actor['甲方']['support_summary']
    assert not audit([item], [], clauses)
    summaries = [r['support_summary'] for r in originals]
    project([item], [], clauses)
    assert summaries == [r['support_summary'] for r in item.evidence_clauses if r['source_type'] == 'BODY']
