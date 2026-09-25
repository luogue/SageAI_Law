"""Source identity is necessary but not sufficient for a positive decision."""
from copy import deepcopy

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.contract_facts import extract_contract_fact_graph
from review_v2.engine import (
    _project_atomic_requirement_state, _verified_pass_sources,
    _attach_evidence_traceability, _protect_deterministic_semantic_evidence,
    _apply_review_evidence_ownership, _coverage_claim_for_item,
)
from review_v2.technology_transaction_evidence import extract_elements
from tests.test_technology_exact_truth_pipeline import make_item


@pytest.mark.parametrize('quote', [
    '乙方承担的赔偿责任以技术开发费用为最高限额。',
    '乙方研发迟延按合同总金额每日支付千分之一违约金。',
    '因未完成平台开发，甲方有权解除并要求退还研发费。',
])
def test_liability_topic_never_proves_transaction_classification(quote):
    clauses = parse_contract_clauses('第一条 违约\n' + quote)
    atoms = extract_elements('transaction_classification:ENTRUSTED_DEVELOPMENT', clauses)
    assert atoms and all(e['status'] == 'MISSING' for e in atoms)


@pytest.mark.parametrize('subtype,quote', [
    ('ENTRUSTED_DEVELOPMENT', '甲方委托乙方开发预测系统，乙方负责系统设计和开发。'),
    ('COOPERATIVE_DEVELOPMENT', '双方共同研发新的节能工艺。'),
    ('TECHNOLOGY_TRANSFER', '甲方将专利权转让给受让方。'),
    ('TECHNOLOGY_LICENSE', '许可方授予被许可方使用本软件的许可权。'),
    ('TECHNICAL_CONSULTING', '乙方应提交可行性论证及技术咨询报告。'),
    ('TECHNICAL_SERVICE', '乙方负责数据库分析、性能优化及故障处理。'),
])
def test_core_performance_fact_sources_survive_projection_and_verification(subtype, quote):
    clauses = parse_contract_clauses('第一条 核心给付\n' + quote + '\n第二条 违约\n赔偿最高限额为研发费。')
    item = make_item(); item.item_id = 'TC-01-02'
    item.decision_trace['review_nature'] = 'INTERNAL_CLASSIFICATION'
    assert _project_atomic_requirement_state(item, 'transaction_classification:' + subtype, clauses, allow_empty=True)
    assert item.coverage_status == '通过'
    for _ in range(2):
        _protect_deterministic_semantic_evidence([item])
        _apply_review_evidence_ownership([item])
        _attach_evidence_traceability([item], clauses)
        assert _verified_pass_sources([item], clauses)['status'] == 'REPORT_READY'
        assert all('赔偿' not in e['quote'] for e in item.evidence_clauses)
    assert {e['element_id'] for e in item.coverage_elements} == {e['element_id'] for e in _coverage_claim_for_item(item).required_elements}


def test_spoofed_classification_tag_and_valid_original_do_not_bypass_gate():
    clauses = parse_contract_clauses('第一条 责任\n赔偿最高限额为技术开发费。')
    item = make_item(); item.item_id = 'TC-01-02'; item.coverage_status = '通过'
    item.decision_trace['review_nature'] = 'INTERNAL_CLASSIFICATION'
    item.coverage_elements = [dict(element_id='classification', proposition='委托研发', status='COVERED')]
    clause = next(c for c in clauses if '最高限额' in c.text)
    item.evidence_clauses = [dict(clause_id=clause.clause_id, quote=clause.text,
                                supporting_element_ids=['classification'], entailment_status='SUPPORTS')]
    _attach_evidence_traceability([item], clauses)
    assert _verified_pass_sources([item], clauses)['status'] == 'BLOCKED'


def test_invoice_alone_does_not_cover_four_funding_elements():
    clauses = parse_contract_clauses('第一条 费用\n乙方应提供增值税发票。')
    elements = extract_elements('development_funding', clauses)
    assert [e['status'] for e in elements] == ['MISSING', 'MISSING', 'MISSING', 'PARTIALLY_COVERED']


def test_pass_gate_checks_every_reported_element_not_a_generic_topic():
    clauses = parse_contract_clauses('第一条 开发\n甲方委托乙方开发诊断软件。')
    item = make_item(); item.item_id = 'TC-01-02'
    _project_atomic_requirement_state(item, 'transaction_classification:ENTRUSTED_DEVELOPMENT', clauses, allow_empty=True)
    _attach_evidence_traceability([item], clauses)
    item.coverage_elements.append(dict(element_id='fabricated_fact', proposition='知识产权归甲方', status='COVERED', evidence_ids=[]))
    gate = _verified_pass_sources([item], clauses)
    assert any(f.get('element_id') == 'fabricated_fact' for f in gate['failures'])


def test_shared_registry_uses_exact_predicate_span_not_adjacent_liability():
    clauses = parse_contract_clauses('第一条\n乙方根据甲方需求完成平台开发。赔偿以开发费为限。')
    graph = extract_contract_fact_graph(clauses)
    facts = graph.matching(['technology.transaction.rd_performance'])
    assert facts and all('赔偿' not in span for f in facts for span in f.source_spans)


def test_mutated_quote_cannot_reuse_element_id_or_positive_tag():
    clauses = parse_contract_clauses('第一条\n甲方委托乙方开发检测平台。\n第二条\n乙方赔偿以开发费用为限。')
    item = make_item(); item.item_id = 'TC-01-01'
    _project_atomic_requirement_state(item, 'transaction_classification:ENTRUSTED_DEVELOPMENT', clauses, allow_empty=True)
    clause = next(c for c in clauses if '赔偿' in c.text)
    item.evidence_clauses = [dict(item.evidence_clauses[0], clause_id=clause.clause_id, quote=clause.text)]
    _attach_evidence_traceability([item], clauses)
    assert _verified_pass_sources([item], clauses)['status'] == 'BLOCKED'


def test_intellectual_property_warranty_is_not_development_delivery():
    clauses = parse_contract_clauses('第一条\n乙方保证其自行提供的技术成果不侵犯第三方合法知识产权。')
    atoms = extract_elements('development_scope', clauses)
    assert next(e for e in atoms if e['element_id'] == 'deliverables_and_acceptance')['status'] == 'MISSING'


def test_composite_losing_one_component_evidence_is_blocked():
    from review_v2.verified_source import check_pass, bind_original
    clauses = parse_contract_clauses('第一条\n乙方应提供发票。收款账户：工商银行123456789。')
    atom = extract_elements('development_funding', clauses)[-1]
    assert atom['status'] == 'COVERED'
    source = atom['supporting_evidence'][0]
    row = bind_original(source, clauses)
    check = check_pass([row], clauses, [atom], lambda requirement, evidence: True)
    assert any(f['reason'] == 'NO_VERIFIED_COMPONENT_SUPPORT' for f in check['failures'])


def test_unrelated_positive_tags_cannot_prove_unmodeled_technical_atom():
    item = make_item(); item.item_id = 'TC-04-01'; item.coverage_status = '通过'
    item.coverage_elements = [dict(element_id='specific_unmodeled_exit_procedure', status='COVERED', proposition='退出手续')]
    clauses = parse_contract_clauses('第一条\n乙方应保密。')
    clause = clauses[-1]
    item.evidence_clauses = [dict(clause_id=clause.clause_id, quote=clause.text, entailment_status='SUPPORTS')]
    _attach_evidence_traceability([item], clauses)
    assert _verified_pass_sources([item], clauses)['status'] == 'BLOCKED'


@pytest.mark.parametrize('family,quote,target', [
    ('development_result', '甲方应支付技术开发费用100万元。', 'technical_secret_result_ownership'),
    ('development_result', '合同终止后双方继续保密五年。', 'post_project_use_and_disposition'),
])
def test_neighbouring_payment_and_secrecy_domains_do_not_prove_unrelated_facts(family, quote, target):
    from review_v2.engine import _atomic_requirement_family
    atoms = _atomic_requirement_family(family, parse_contract_clauses('第一条\n' + quote))
    assert next(e for e in atoms if e['element_id'] == target)['status'] == 'MISSING'


def test_classification_facts_keep_registry_identity_in_report_elements():
    clauses = parse_contract_clauses('第一条\n甲方委托乙方开发传感系统。')
    graph = extract_contract_fact_graph(clauses)
    item = make_item(); item.item_id = 'TC-01-02'
    _project_atomic_requirement_state(item, 'transaction_classification:ENTRUSTED_DEVELOPMENT', clauses, allow_empty=True)
    for element in item.coverage_elements:
        assert set(element['fact_ids']) == {f.fact_id for f in graph.matching([element['source_fact_key']])}


def test_entrusted_role_aliases_are_core_performance_not_a_title_requirement():
    clauses = parse_contract_clauses('第一条\n委托人委托研究开发人研究开发智能检测系统的新技术成果。')
    assert all(e['status'] == 'COVERED' for e in extract_elements('transaction_classification:ENTRUSTED_DEVELOPMENT', clauses))


@pytest.mark.parametrize('quote', [
    '项目名称：智能平台合作研发项目',
    '利用共同研发经费购买的设备在项目结束后归甲方所有。',
    '因技术困难导致项目失败的，由乙方承担全部研发损失。',
])
def test_research_modifiers_and_risk_allocation_are_not_core_performance(quote):
    atoms = extract_elements('transaction_classification:COOPERATIVE_DEVELOPMENT', parse_contract_clauses('第一条\n' + quote))
    assert all(e['status'] == 'MISSING' for e in atoms)


def test_milestone_definition_and_delivered_result_ip_are_not_performance():
    clauses = parse_contract_clauses('第一条\n里程碑：乙方阶段性完成的独立软件模块。\n第二条\n乙方提交的开发成果如涉及背景知识产权，乙方授予甲方使用许可。')
    atoms = {e['element_id']: e for e in extract_elements('development_scope', clauses)}
    assert atoms['schedule_and_milestones']['status'] == 'MISSING'
    assert atoms['deliverables_and_acceptance']['status'] == 'MISSING'


@pytest.mark.parametrize('text,complete,expected', [
    ('第三方提出侵权主张时，乙方应处理纠纷。', True, 'REPORT_READY'),
    ('第三方提出侵权主张时，乙方应处理纠纷。', False, 'BLOCKED'),
    ('本项技术已经侵犯第三方专利。', True, 'BLOCKED'),
])
def test_negative_rule_requires_reproduced_complete_adverse_search(text, complete, expected):
    from review_v2.technology_adverse_evidence import prepare_negative_audits
    clauses = parse_contract_clauses('第一条\n' + text)
    item = make_item(); item.item_id = 'TC-02-02'; item.coverage_status = '通过'
    item.coverage_elements = [dict(element_id='affirmative_infringement_fact', status='NOT_APPLICABLE')]
    # Exercise the production search producer, not a display-only boolean
    # snapshot lacking the target predicate and search execution contract.
    prepare_negative_audits([item], clauses)
    if not complete:
        item.decision_trace['negative_clause_check']['searched_scope'] = []
    assert _verified_pass_sources([item], clauses)['status'] == expected
