"""Search truth, applicability and coverage have independent evidence owners."""
from copy import deepcopy

import pytest

from review_v2 import engine
from review_v2.clause_parser import parse_contract_clauses
from review_v2.technology_adverse_evidence import prepare_negative_audits, verify_negative_search
from review_v2.technology_service_analysis import classify_technology_transaction
from tests.test_technology_exact_truth_pipeline import make_item


@pytest.mark.parametrize('rule_id', ['TC-02-02', 'TC-10-04'])
def test_negative_search_is_not_replaced_by_checkpoint_display_metadata(rule_id):
    item = make_item(); item.item_id = rule_id; item.coverage_status = '通过'
    clauses = parse_contract_clauses('第一条 改进\n双方独立改进成果各自所有，使用对方成果应协商许可。')
    prepare_negative_audits([item], clauses)
    audit = deepcopy(item.decision_trace['negative_clause_check'])
    checkpoint = next(c for c in engine.get_checklist('technology') if c.item_id == rule_id)
    engine._apply_checkpoint_metadata([item], [checkpoint], [c.clause_id for c in clauses])
    assert item.decision_trace['negative_clause_check'] == audit
    assert verify_negative_search(item, clauses)['status'] == 'PASS'


@pytest.mark.parametrize('mutation', ['incomplete_scope', 'contrary_clause', 'wrong_predicate'])
def test_negative_audit_requires_reproducible_predicate_and_full_corpus(mutation):
    item = make_item(); item.item_id = 'TC-10-04'
    clauses = parse_contract_clauses('第一条 改进\n双方独立改进成果各自所有。')
    prepare_negative_audits([item], clauses)
    if mutation == 'incomplete_scope':
        item.decision_trace['negative_clause_check']['searched_scope'] = []
    elif mutation == 'wrong_predicate':
        item.decision_trace['negative_clause_check']['predicate'] = 'ACTUAL_INFRINGEMENT'
    else:
        clauses = parse_contract_clauses('第一条 改进\n禁止被许可方自主改进许可技术。')
    assert verify_negative_search(item, clauses) is None


@pytest.mark.parametrize('clause', [
    '接受方按约实施遭遇第三方侵权主张时，许可方应负责应诉并承担相应侵权责任。',
    '买方遭到第三人索赔的，卖方应负责处理并承担合理损失。',
])
def test_trigger_party_does_not_own_later_provider_response(clause):
    text = '专利实施许可合同\n许可方授予接受方专利实施许可。\n第一条 权利主张\n' + clause
    facts = classify_technology_transaction(text)['fact_registry']['third_party_claim']
    assert facts['responsible_party'] == 'LICENSOR'
    assert not facts['licensee_litigation_handling']
    assert all(row['actor'] == 'LICENSOR' for row in facts['response_element_evidence']['liability_responsible_party'])


def test_confidentiality_undertaking_is_only_applicability_not_breach_liability():
    text = '专利实施许可合同\n许可方授予接受方专利实施许可。\n第一条 保密\n双方对履约中知悉的技术秘密承担保密义务。'
    item = make_item(); item.item_id = 'TC-11-04'
    engine._apply_technology_confidentiality_semantic_rules([item], text)
    assert item.applicability['status'] == 'APPLICABLE'
    assert item.applicability['evidence']
    assert item.coverage_status == '缺失'
    assert 'confidentiality_obligation_reference' not in {e['element_id'] for e in item.coverage_elements}
    assert not any(e['status'] == 'COVERED' for e in item.coverage_elements)


def test_replaying_completed_negative_search_is_idempotent():
    item = make_item(); item.item_id = 'TC-10-04'
    clauses = parse_contract_clauses('第一条 改进\n双方可以独立改进。')
    prepare_negative_audits([item], clauses)
    before = deepcopy(item.decision_trace)
    prepare_negative_audits([item], clauses)
    assert item.decision_trace == before


def test_rejected_positive_element_cannot_be_restored_from_specialized_snapshot():
    item = make_item(); item.item_id = 'TC-07-02'; item.coverage_status = '通过'
    clauses = parse_contract_clauses('第一条 通知\n地址变更应书面通知。')
    element = {'element_id': 'fee_calculation', 'status': 'PARTIALLY_COVERED',
               'proposition': '许可费计算方式', 'evidence_ids': ['old']}
    item.coverage_elements = [deepcopy(element)]
    item.evidence_clauses = []
    item.decision_trace.update(specialized_multi_element_state=True, specialized_elements=[deepcopy(element)])
    engine._verified_pass_sources([item], clauses, downgrade=True)
    assert item.coverage_elements[0]['status'] == 'UNCERTAIN'
    before = deepcopy(item.coverage_elements)
    engine._protect_deterministic_semantic_evidence([item])
    assert item.coverage_elements == before
    assert item.coverage_status not in {'通过', 'PASS'}
    assert item.decision_trace['element_verification_transitions'][0]['reject_reasons']
    assert engine._verified_element_revocation(item, 'fee_calculation')
    item.decision_trace['verified_pass_source_gate']['failures'] = []
    assert not engine._verified_element_revocation(item, 'fee_calculation')


def test_patent_identity_absence_query_is_field_specific():
    item = make_item(); item.item_id = 'TC-03-04'
    clauses = parse_contract_clauses('第一条 专利\n专利号为ZL201910876543.2。')
    number = engine._search_final_element(item, {'element_id': 'technology.patent.number'}, clauses)
    date = engine._search_final_element(item, {'element_id': 'technology.patent.application_date'}, clauses)
    assert number['result'] == 'FOUND'
    assert date['result'] == 'NOT_FOUND'
    assert date['search_targets'] == ['专利申请日期']
    assert date['searched_clause_ids'] == [c.clause_id for c in clauses]


def test_canonical_penalty_rekey_preserves_exact_binding_contract():
    from review_v2.penalty_fact_binding import bind
    clauses = parse_contract_clauses('第一条 违约\n乙方迟延交付，每逾期一日按合同总价的1%向甲方支付违约金。')
    graph = engine.extract_contract_fact_graph(clauses)
    fact = graph.matching(['liability.penalty'])[0]
    source = {'clause_id': fact.source_clause_ids[0], 'quote': fact.value['raw_clause']}
    item = make_item(); item.item_id = 'TC-05-04'
    item.coverage_elements = [{'element_id': 'development_delay_liability', 'status': 'COVERED',
                              'required_fact': '开发迟延的违约后果', 'source_fact_key': 'old_local_key',
                              'supporting_evidence': [source]}]
    item.decision_trace.update(direct_fact_bindings={'old_local_key': [source]},
                               direct_element_fact_keys={'development_delay_liability': 'old_local_key'})
    bind([item], graph)
    element = item.coverage_elements[0]
    assert element['source_fact_key'] == fact.fact_id
    assert item.decision_trace['direct_element_fact_keys'][element['element_id']] == fact.fact_id
    assert item.decision_trace['direct_fact_bindings'][fact.fact_id] == [source]


def test_generic_confidentiality_claim_reuses_scope_and_obligation_sources():
    clauses = parse_contract_clauses('第一条 权属\n开发形成的源代码和技术文档归甲方所有。\n第二条 保密\n技术资料、经营信息均属于保密信息。双方在履行期间承担保密义务。')
    atoms = engine._atomic_requirement_family('confidentiality_core', clauses)
    assert {a['status'] for a in atoms} == {'COVERED'}
    assert all('权属' not in source['quote'] and '归甲方所有' not in source['quote']
               for a in atoms for source in a['supporting_evidence'])


@pytest.mark.parametrize('declaration,found', [
    ('许可方确认其为许可标的的合法专利权人。', True),
    ('甲方声明是该项技术的专利权人。', True),
    ('甲方不是该项技术的专利权人。', False),
    ('甲方如为专利权人，应提供证书。', False),
])
def test_owner_declaration_is_identity_not_document_availability(declaration, found):
    graph = engine.extract_contract_fact_graph(parse_contract_clauses('第一条 权属\n' + declaration))
    assert bool(graph.matching(['technology.patent.owner'])) == found
    assert not graph.matching(['technology.patent.certificate'])


@pytest.mark.parametrize('clause,covered', [
    ('许可方应交付设计图纸和操作手册。', True),
    ('许可方应提交电气原理图和维修手册。', True),
    ('许可方提供的操作手册发生错误时应承担赔偿责任。', False),
])
def test_material_delivery_uses_same_document_taxonomy_as_scope(clause, covered):
    text = '专利实施许可合同\n第一条 许可\n许可方向接受方授予专利实施许可。\n第二条 资料\n' + clause
    item = make_item(); item.item_id = 'TC-13-01'
    engine._apply_technology_common_semantic_rules([item], text, classify_technology_transaction(text))
    elements = item.decision_trace['specialized_elements']
    delivery = next(e for e in elements if e['element_id'] == 'delivery_obligation')
    assert (delivery['status'] == 'COVERED') == covered


def test_liability_cap_does_not_replace_explicit_claim_handler():
    text = ('专利实施许可合同\n第一条 许可\n许可方向被许可方授予专利实施许可。\n第二条 侵权\n'
            '第三方指控被许可方实施技术侵权时，由被许可方负责处理相关争议；'
            '许可方仅提供必要协助；许可方承担的全部赔偿责任不超过许可费的20%。')
    facts = classify_technology_transaction(text)['fact_registry']['third_party_claim']
    assert facts['responsible_party'] == 'LICENSEE'
    assert not facts['response_element_evidence'].get('liability_responsible_party')


def test_general_liability_allocation_does_not_establish_concrete_damage_items():
    item = make_item(); item.item_id = 'TC-12-04'
    clauses = parse_contract_clauses('第一条 索赔\n许可方负责处理第三方侵权并承担相应责任。')
    item.decision_trace['fact_registry'] = {'third_party_claim': {'response_element_evidence': {
        'third_party_compensation_allocation': [{'clause_id': clauses[0].clause_id, 'quote': clauses[0].text}]
    }}}
    engine._restore_tc1204_shared_claim_audit_elements([item], clauses)
    assert not any(e['element_id'] == 'infringement_damage_items' for e in item.coverage_elements)
