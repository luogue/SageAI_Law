"""Shared factual prerequisites and exact evidence projection, not sample text."""
from copy import deepcopy

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.contract_facts import ContractFactGraph
from review_v2.engine import (
    _register_atomic_family_facts, _attach_contract_fact_registry_snapshot,
    _apply_technology_confidentiality_semantic_rules, _set_multi_element_state,
    _coverage_elements_for_item, _requirement_registry_key,
    ReviewItemResult,
)
from review_v2.technology_service_analysis import extract_claim_response_facts
from tests.test_technology_exact_truth_pipeline import make_item


@pytest.mark.parametrize('wording', [
    '双方的经营数据和非公开技术资料均属于保密信息。',
    '双方保密义务在合同终止后继续有效三年。',
    '保密信息包括客户信息及商业计划。',
])
def test_confidentiality_siblings_consume_shared_positive_prerequisites(wording):
    text = '技术委托开发合同\n第一条 保密\n' + wording
    clauses = parse_contract_clauses(text)
    graph = ContractFactGraph()
    _register_atomic_family_facts(graph, 'confidentiality_detail', clauses)
    graph.freeze('shared-test')
    items = []
    for rule in ('TC-11-01', 'TC-11-02', 'TC-11-03', 'TC-11-04'):
        item = make_item()
        item.item_id = rule
        items.append(item)
    _attach_contract_fact_registry_snapshot(items, graph, 'shared-test')
    _apply_technology_confidentiality_semantic_rules(items, text)
    for item in items[2:]:
        facts = item.decision_trace['confidentiality_applicability']
        assert facts['status'] == 'CONFIRMED'
        assert any(row.get('fact_ids') for row in facts['canonical_prerequisite_facts'].values())
        assert '尚不能确认' not in item.reasoning_summary


@pytest.mark.parametrize('provider,recipient', [('乙方', '甲方'), ('许可方', '被许可方'), ('卖方', '买方')])
def test_loss_allocation_proves_liability_actor_not_specific_cost_scope(provider, recipient):
    text = f'第一条 侵权\n第三方因{provider}开发内容向{recipient}主张侵权的，{provider}应负责处理并承担因此给{recipient}造成的合理损失。'
    facts = extract_claim_response_facts(parse_contract_clauses(text), provider, recipient)
    assert facts['liability_responsible_party']
    assert facts['claim_handling']
    assert not facts.get('defense_cost_scope')
    assert not facts.get('damages_scope')


def test_exact_source_adapter_projects_span_without_covering_neighbour():
    item = make_item()
    clause = {'clause_id': 'C1', 'text': '乙方负责处理第三方索赔。付款期限另行约定。', 'location': '第一条', 'source_type': 'BODY'}
    item.evidence_clauses = [deepcopy(clause)]
    elements = [
        {'element_id': 'handling', 'source_fact_key': 'claims.handling', 'status': 'COVERED',
         'proposition': '处理主体已明确', 'bound_evidence_ids': ['C1'],
         'supporting_evidence': [{'clause_id': 'C1', 'quote': '乙方负责处理第三方索赔。'}]},
        {'element_id': 'deadline', 'source_fact_key': 'claims.deadline', 'status': 'COVERED',
         'proposition': '应在三日内处理', 'bound_evidence_ids': ['C1'],
         'supporting_evidence': [{'clause_id': 'C1', 'quote': '应在三日内处理'}]},
    ]
    _set_multi_element_state(item, elements, [clause])
    good, bad = item.coverage_elements
    assert good['status'] == 'COVERED'
    assert good['source_spans'] == ['乙方负责处理第三方索赔。']
    assert bad['status'] == 'UNCERTAIN' and not bad['evidence_ids']
    assert any(row.get('quote') == good['source_spans'][0] and row['supporting_element_ids'] == ['handling']
               for row in item.evidence_clauses)


def test_requirement_label_is_not_a_registry_key_or_a_missing_fact():
    element = {'element_id': 'notice', 'required_fact': '第三方主张的书面通知',
               'proposition': '第三方主张的书面通知',
               'semantic_patterns': [r'应书面通知']}
    assert _requirement_registry_key(element) == ''
    assert _requirement_registry_key({**element, 'required_fact_key': 'claims.notice'}) == 'claims.notice'
    item = make_item()
    item.decision_trace['semantic_requirements'] = [element]
    item.evidence_clauses = [{'clause_id': 'C1', 'quote': '发生第三方索赔时，应书面通知对方。', 'location': '第一条'}]
    assert _coverage_elements_for_item(item)[0].status == 'COVERED'
    item.evidence_clauses[0]['quote'] = '发生第三方索赔时，由双方另行协商。'
    assert _coverage_elements_for_item(item)[0].status == 'MISSING'


def test_atomic_projection_replay_keeps_distinct_spans_and_evidence_identity():
    from review_v2.engine import _project_atomic_requirement_state
    item = make_item()
    item.applicability = {'status': 'APPLICABLE'}
    clauses = parse_contract_clauses('第一条 后续改进\n甲方后续改进成果归甲方所有。'
        '乙方后续改进成果归乙方所有。甲方享有优先获得许可的权利，许可条件另行协商。')
    assert _project_atomic_requirement_state(item, 'improvement_license', clauses)
    before = {e['element_id']: list(e['evidence_ids']) for e in item.coverage_elements}
    rows = [dict(e, bound_evidence_ids=e['evidence_ids']) for e in item.coverage_elements]
    _set_multi_element_state(item, rows, item.evidence_clauses)
    after = {e['element_id']: list(e['evidence_ids']) for e in item.coverage_elements}
    assert before == after
    priority = next(e for e in item.coverage_elements if e['element_id'] == 'priority_license')
    assert priority['status'] == 'COVERED'
    assert priority['evidence_ids']
    assert all('优先' in span for span in priority['source_spans'])


def test_public_review_schema_roundtrip_preserves_gate_inputs():
    item = make_item()
    item.presentation = {'display_title': '审查项目'}
    restored = ReviewItemResult(**item.to_public_dict())
    assert restored.coverage_elements == item.coverage_elements
    assert restored.presentation == item.presentation


def test_source_verification_rekeys_exact_element_edges_without_clause_cross_binding():
    from review_v2.engine import _attach_evidence_traceability
    item = make_item()
    clauses = parse_contract_clauses('第一条\n乙方负责处理索赔。甲方承担费用。')
    clause = next(c for c in clauses if '乙方负责' in c.text)
    quotes = ['乙方负责处理索赔。', '甲方承担费用。']
    item.evidence_clauses = [{'clause_id': clause.clause_id, 'evidence_id': 'OLD',
        'quote': quote} for quote in quotes]
    item.coverage_elements = [{'element_id': key, 'evidence_ids': ['OLD'],
        'source_clause_ids': [clause.clause_id], 'source_spans': [quote]}
        for key, quote in zip(['handler', 'cost_actor'], quotes)]
    _attach_evidence_traceability([item], clauses)
    ids = [e['evidence_ids'][0] for e in item.coverage_elements]
    assert len(set(ids)) == 2 and all(e.startswith('SRC-') for e in ids)
    by_id = {e['evidence_id']: e['quote'] for e in item.evidence_clauses}
    assert [by_id[e] for e in ids] == quotes
    _attach_evidence_traceability([item], clauses)
    assert [e['evidence_ids'][0] for e in item.coverage_elements] == ids


def test_registry_projection_does_not_merge_different_elements_by_clause_id():
    from review_v2.engine import _apply_review_evidence_ownership
    item = make_item()
    item.coverage_elements = [{'element_id': key, 'required_fact_key': 'claims.' + key,
        'status': 'COVERED', 'source_clause_ids': ['C1'], 'source_spans': [quote],
        'source_locations': ['第一条']} for key, quote in [
            ('handler', '乙方负责处理索赔。'), ('cost_actor', '甲方承担费用。')]]
    _apply_review_evidence_ownership([item])
    assert len(item.evidence_clauses) == 2
    assert all(len(e['supporting_element_ids']) == 1 for e in item.evidence_clauses)


@pytest.mark.parametrize('quote,status', [
    ('乙方负责处理第三方索赔。', 'COVERED'),
    ('乙方应在三日内处理第三方索赔。', 'UNCERTAIN'),
])
def test_late_fact_registration_updates_snapshot_without_inventing_evidence(quote, status):
    from review_v2.engine import _synchronize_registered_element_bindings
    item = make_item()
    source = {'clause_id': 'C1', 'quote': '乙方负责处理第三方索赔。', 'location': '第一条'}
    item.evidence_clauses = [source]
    _set_multi_element_state(item, [{'element_id': 'handler', 'status': 'COVERED',
        'proposition': '索赔处理主体', 'bound_evidence_ids': ['C1']}], [source])
    item.decision_trace['specialized_evidence'] = [source]
    item.decision_trace['direct_element_fact_keys'] = {'handler': 'claims.handler'}
    item.decision_trace['direct_fact_bindings'] = {'claims.handler': [{'clause_id': 'C1', 'quote': quote}]}
    _synchronize_registered_element_bindings(item)
    element = item.decision_trace['specialized_elements'][0]
    assert element['status'] == status
    assert element['source_fact_key'] == 'claims.handler'
    assert bool(element['evidence_ids']) == (status == 'COVERED')


def test_late_registration_preserves_other_explicit_element_edges():
    from review_v2.engine import _synchronize_registered_element_bindings
    item = make_item()
    sources = [{'clause_id': 'C1', 'quote': '乙方负责处理第三方索赔。', 'location': '第一条'},
               {'clause_id': 'C2', 'quote': '甲方承担律师费。', 'location': '第二条'}]
    item.evidence_clauses = sources
    _set_multi_element_state(item, [
        {'element_id': 'handler', 'status': 'COVERED', 'proposition': '索赔处理主体', 'bound_evidence_ids': ['C1']},
        {'element_id': 'cost', 'status': 'ADVERSE', 'proposition': '甲方承担律师费', 'bound_evidence_ids': ['C2']},
    ], sources)
    item.decision_trace['specialized_evidence'] = sources
    item.decision_trace['direct_element_fact_keys'] = {'handler': 'claims.handler'}
    item.decision_trace['direct_fact_bindings'] = {'claims.handler': [{'clause_id': 'C1', 'quote': sources[0]['quote']}]}
    _synchronize_registered_element_bindings(item)
    assert item.coverage_elements[1]['status'] == 'ADVERSE'
    assert item.coverage_elements[1]['evidence_ids'] == ['C2']


@pytest.mark.parametrize('prerequisite,status', [('UNKNOWN', 'CONDITION_UNRESOLVED'), ('FALSE', 'NOT_APPLICABLE')])
def test_unresolved_conditional_fact_survives_coverage_adapter(prerequisite, status):
    item = make_item()
    item.decision_trace['semantic_requirements'] = [{
        'element_id': 'authorization', 'required_fact': '上游授权证明',
        'proposition': '核验是否需要上游授权', 'conditional_element': True,
        'prerequisite_status': prerequisite,
    }]
    resolved = _coverage_elements_for_item(item)[0]
    assert resolved.status == status and not resolved.evidence_ids


def test_semantic_verification_does_not_borrow_unpublished_neighbouring_sentence():
    from review_v2.lease_semantics import supports
    element = {'element_id': 'notice', 'semantic_patterns': ['应书面通知']}
    row = {'clause_id': 'C1', 'location': '第一条',
           'text': '发生索赔应书面通知。费用另行协商。', 'quote': '费用另行协商。'}
    assert not supports(element, row)
    row['quote'] = '发生索赔应书面通知。'
    assert supports(element, row)


def test_evidence_package_projects_the_sentence_it_actually_verified():
    from review_v2.lease_semantics import rule_evidence_package
    item = make_item()
    item.decision_trace['semantic_requirements'] = [{'element_id': 'notice',
        'proposition': '书面通知', 'semantic_patterns': ['应书面通知']}]
    item.coverage_elements = [{'element_id': 'notice', 'status': 'COVERED'}]
    item.evidence_clauses = [{'clause_id': 'C1', 'location': '第一条',
        'text': '费用另行协商。发生索赔应书面通知。', 'quote': '发生索赔应书面通知。'}]
    bundle = rule_evidence_package(item)
    assert len(bundle['items']) == 1
    assert bundle['items'][0]['quote'] == '发生索赔应书面通知。'


def test_display_alias_gate_verifies_each_actual_alias_not_a_sibling_quote():
    from review_v2.lease_semantics import consistency_failures
    item = make_item()
    item.decision_trace['semantic_requirements'] = [{'element_id': 'notice',
        'proposition': '书面通知', 'semantic_patterns': ['应书面通知']}]
    item.coverage_elements = [{'element_id': 'notice', 'status': 'COVERED'}]
    item.evidence_clauses = [{'clause_id': 'C1', 'location': '第一条',
        'text': '发生索赔应书面通知。', 'quote': '发生索赔应书面通知。',
        'quoted_text': '费用另行协商。', 'supporting_element_ids': ['notice']}]
    assert any(row['requirement'] == 'DISPLAY_QUOTE_ELEMENT_CONFLICT' for row in consistency_failures([item]))


@pytest.mark.parametrize('status', ['ADVERSE', 'CONFLICTING'])
def test_direct_adverse_fact_does_not_turn_into_uncertain_entailment(status):
    item = make_item()
    quote = '乙方可以单方决定是否交付成果。'
    element = {'element_id': 'unilateral_delivery', 'source_fact_key': 'delivery.unilateral',
               'status': status, 'proposition': quote,
               'bound_evidence_ids': ['C1'], 'supporting_evidence': [{'clause_id': 'C1', 'quote': quote}]}
    item.evidence_clauses = [{'clause_id': 'C1', 'quote': quote, 'location': '第一条'}]
    _set_multi_element_state(item, [element], item.evidence_clauses)
    resolved = _coverage_elements_for_item(item)[0]
    assert resolved.status == status
    assert resolved.entailment == 'SUPPORTS'
