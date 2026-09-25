"""Two-way protection of the specialized -> canonical -> verifier contract."""
from copy import deepcopy

import pytest
from review_v2 import engine
from review_v2.clause_parser import parse_contract_clauses
from review_v2.consulting_element_facts import elements
from tests.test_technology_exact_truth_pipeline import make_item


@pytest.mark.parametrize('family,text,expected', [
    ('consulting_quality', '乙方对系统架构进行分析评估。咨询报告应包括风险分析。乙方提交纸质咨询报告。咨询报告应完整覆盖约定内容。', 4),
    ('consulting_inputs', '甲方提供系统架构图和性能数据，安排人员访谈及测试环境。甲方保证资料真实、完整，并通过加密电子文件方式提交。', 4),
    ('consulting_remedy', '咨询成果不符合约定的，乙方应在合理期限内免费修改。', 3),
])
def test_canonical_sources_survive_projection_and_independent_verification(family, text, expected):
    clauses = parse_contract_clauses('第一条 咨询\n' + text)
    item = make_item(); item.item_id = 'TC-08-01'
    item.applicability = {'status': 'APPLICABLE'}
    assert engine._project_atomic_requirement_state(item, family, clauses, allow_empty=True)
    assert sum(e['status'] == 'COVERED' for e in item.coverage_elements) == expected
    engine._enrich_evidence_sources([item])
    engine._attach_evidence_traceability([item], clauses)
    engine._verified_pass_sources([item], clauses, downgrade=True)
    assert item.decision_trace['verified_pass_source_gate']['status'] == 'PASS'
    assert item.coverage_status == '通过'
    before = deepcopy(item.coverage_elements)
    engine._protect_deterministic_semantic_evidence([item])
    assert item.coverage_elements == before
    graph = engine.extract_contract_fact_graph(clauses)
    engine._register_atomic_family_facts(graph, family, clauses)
    for atom in item.coverage_elements:
        if atom['status'] == 'COVERED':
            assert graph.matching([atom['source_fact_key']])
            assert atom['evidence_ids']


@pytest.mark.parametrize('family', ['consulting_quality', 'consulting_inputs', 'consulting_remedy'])
def test_related_heading_and_other_obligation_do_not_prove_consulting_elements(family):
    clauses = parse_contract_clauses('第一条 咨询报告\n乙方应在30日内支付违约金。地址变更须书面通知。')
    assert not any(e['status'] == 'COVERED' for e in elements(family, clauses))


def test_exact_report_id_does_not_get_shadowed_by_clause_id_in_advice():
    from types import SimpleNamespace
    item = SimpleNamespace(item_id='R', coverage_elements=[
        dict(element_id='post_termination_competition_restriction', status='ADVERSE', proposition='终止后限制', evidence_ids=['EV-1']),
        dict(element_id='independent_research_restriction', status='ADVERSE', proposition='限制研发', evidence_ids=['EV-2'])],
        evidence_clauses=[dict(evidence_id='EV-1', clause_id='C1', text='限制在合同终止后继续有效4年。')])
    # Use another real action-vocabulary element, not a test-only rule branch.
    keys = [key for key in engine.ADVERSE_ELEMENT_ACTIONS if key != 'post_termination_competition_restriction']
    item.coverage_elements[1]['element_id'] = keys[0]
    fragments = engine._adverse_element_recommendation_fragments(item)
    assert any('继续4年' in row['text'] for row in fragments)


def test_inline_article_payload_reaches_the_same_fact_predicate():
    clauses = engine._operative_technology_clauses(
        '第三条 甲方应在合同生效后4日内以电子文件方式向乙方提供设备图纸和技术资料，'
        '并提供测试环境和访问权限，保证资料真实、完整。')
    assert clauses
    assert all(e['status'] == 'COVERED' for e in elements('consulting_inputs', clauses))


def test_explicit_mutual_undertaking_is_not_an_unidentified_party_group():
    clauses = parse_contract_clauses('第十条 保密\n双方对未公开信息承担保密义务。\n买方\n保密内容：源代码。\n卖方\n保密内容：研发数据。')
    rows = engine._atomic_requirement_family('confidentiality_core', clauses)
    duty = next(e for e in rows if e['element_id'] == 'during_contract_confidentiality')
    assert duty['status'] == 'COVERED'
    assert all(e['status'] == 'COVERED' for e in duty['party_coverage'])


def test_response_projection_uses_original_not_reparsed_clause_identity():
    text = ('专利许可合同\n许可方授予被许可方专利实施许可。\n第一条 定义\n第二条 通知\n'
            '第三方对被许可方提出侵权主张时，许可方负责处理并承担赔偿责任。')
    clauses = parse_contract_clauses(text)
    # Deliberately drop a topic-only header, exactly as candidate filtering may.
    selected = [c for c in clauses if c.text.strip() != '第一条 定义']
    atoms = engine._atomic_requirement_family('license_liability_direction', selected)
    originals = {c.clause_id: c.text for c in clauses}
    assert all(e['status'] == 'COVERED' for e in atoms)
    for atom in atoms:
        for source in atom['supporting_evidence']:
            assert source['quote'] in originals[source['clause_id']]


@pytest.mark.parametrize('text,covered', [
    ('卖方保证已经取得全部研发人员职务成果归属的内部文件。', True),
    ('卖方应当今后提供研发人员身份材料。', False),
])
def test_application_representations_are_not_inferred_from_future_materials(text, covered):
    clauses = parse_contract_clauses('第十九条 其他约定\n' + text)
    atom = next(e for e in engine._atomic_requirement_family('application_transfer', clauses)
                if e['element_id'] == 'employee_result_assignment')
    assert (atom['status'] == 'COVERED') is covered
    if covered:
        assert all(s['quote'] in next(c.text for c in clauses if c.clause_id == s['clause_id'])
                   for s in atom['supporting_evidence'])


@pytest.mark.parametrize('text,covered', [
    ('乙方通过系统分析和参数调试提供技术服务，并提交技术优化报告。', True),
    ('甲方支付技术服务费用。乙方违约赔偿以技术服务费用为上限。', False),
])
def test_service_subject_candidates_retain_performance_not_remedy_sources(text, covered):
    clauses = parse_contract_clauses('第一条 合同安排\n' + text)
    atoms = engine._atomic_requirement_family('technical_service_subject', clauses)
    assert all(e['status'] == 'COVERED' for e in atoms) is covered
    if not covered:
        assert all(e['status'] == 'MISSING' for e in atoms)


def test_named_object_of_confidentiality_duty_is_scope_not_remedy():
    clauses = parse_contract_clauses('第八条 保密\n甲方对乙方提供的程序代码和销售数据承担保密义务。')
    scope = next(e for e in engine._atomic_requirement_family('confidentiality_core', clauses)
                 if e['element_id'] == 'confidential_information_scope')
    assert scope['status'] == 'COVERED'
    counter = parse_contract_clauses('第八条 责任\n甲方违反保密义务，应赔偿数据泄露损失。')
    scope = next(e for e in engine._atomic_requirement_family('confidentiality_core', counter)
                 if e['element_id'] == 'confidential_information_scope')
    assert scope['status'] == 'MISSING'


def test_multiple_sources_for_one_element_do_not_expand_verified_quotes():
    item = make_item()
    item.coverage_elements = [dict(element_id='public_exception', status='COVERED',
        proposition='合法公开信息例外', evidence_ids=['SRC-a', 'SRC-b'],
        source_clause_ids=['C1', 'C1'], source_spans=['已经合法公开。', '非因违约被公开。'])]
    item.evidence_clauses = [dict(evidence_id='SRC-a', clause_id='C1',
        quote='已经合法公开。', text='已经合法公开。',
        raw_text='已经合法公开。非因违约被公开。', verified_original=True,
        supporting_element_ids=['public_exception'])]
    engine._synchronize_evidence_support_to_final_elements(item)
    assert item.evidence_clauses[0]['quote'] == '已经合法公开。'
    assert item.evidence_clauses[0]['evidence_id'] == 'SRC-a'
