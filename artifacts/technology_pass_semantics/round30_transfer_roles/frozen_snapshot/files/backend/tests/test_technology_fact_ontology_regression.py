"""Equivalent source objects share facts without equating adjacent obligations."""
import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.contract_facts import canonical_fact_key, extract_contract_fact_graph
from review_v2.obligation_detail_elements import development_document_elements, development_acceptance_detail_elements
from review_v2.technology_fact_ontology import matches_action, license_scope_elements, registration_elements
from review_v2.technology_transaction_evidence import extract_elements
from review_v2.technology_adverse_evidence import prepare_negative_audits
from review_v2.engine import _verified_pass_sources
from tests.test_technology_exact_truth_pipeline import make_item


@pytest.mark.parametrize('name', ['部署说明', '安装说明', '安装部署文档', '部署指南'])
def test_installation_deployment_aliases_reuse_one_fact(name):
    clauses = parse_contract_clauses('第一条 系统交付\n乙方应提供' + name + '。')
    atoms = {a['element_id']: a for a in development_document_elements(clauses)}
    graph = extract_contract_fact_graph(clauses)
    keys = ['deployment_document_delivery', 'installation_document_delivery']
    assert all(atoms[key]['status'] == 'COVERED' for key in keys)
    assert len({atoms[key]['source_fact_key'] for key in keys}) == 1
    assert len(graph.matching([atoms[key]['source_fact_key'] for key in keys])) == 1
    assert name in graph.matching([atoms[keys[0]]['source_fact_key']])[0].source_spans[0]


@pytest.mark.parametrize('name', ['缺陷清单', 'bug 清单', '问题清单', '缺陷记录'])
def test_software_defect_aliases(name):
    clauses = parse_contract_clauses('第一条 软件测试交付\n乙方应提交系统' + name + '。')
    atom = next(a for a in development_document_elements(clauses) if a['element_id'] == 'defect_list_delivery')
    assert atom['status'] == 'COVERED'


@pytest.mark.parametrize('name', ['测试报告', '测试结果报告', '验收测试报告'])
def test_test_report_consumers_share_source_and_canonical_identity(name):
    clauses = parse_contract_clauses('第一条\n乙方应提交' + name + '。')
    documents = {a['element_id']: a for a in development_document_elements(clauses)}
    acceptance = {a['element_id']: a for a in development_acceptance_detail_elements(clauses)}
    a, b = documents['test_report_delivery'], acceptance['test_report_delivery']
    assert a['status'] == b['status'] == 'COVERED'
    assert a['source_fact_key'] == b['source_fact_key']
    assert a['supporting_evidence'] == b['supporting_evidence']


@pytest.mark.parametrize('name', ['源代码', '程序源码', 'source code'])
def test_code_aliases(name):
    clauses = parse_contract_clauses('第一条 交付\n乙方应交付' + name + '。')
    assert development_document_elements(clauses)[0]['status'] == 'COVERED'


@pytest.mark.parametrize('name', ['技术资料', '技术文档', '开发文档'])
def test_general_document_is_not_a_specific_test_report(name):
    atoms = {a['element_id']: a for a in development_document_elements(parse_contract_clauses('第一条\n乙方应提供' + name + '。'))}
    assert atoms['generic_technical_documentation']['status'] == 'COVERED'
    assert atoms['test_report_delivery']['status'] == 'MISSING'


@pytest.mark.parametrize('text', ['乙方未提供测试报告。', '部署说明的著作权归甲方。', '乙方应提供会议问题清单。'])
def test_mentions_negation_and_adjacent_domains_do_not_become_delivery(text):
    atoms = {a['element_id']: a for a in development_document_elements(parse_contract_clauses('第一条\n' + text))}
    assert all(atoms[key]['status'] == 'MISSING' for key in ('test_report_delivery', 'installation_document_delivery', 'defect_list_delivery'))


def test_refund_alias_and_claim_dimensions_are_not_collapsed():
    assert matches_action('payment_refund', '乙方应退款。')
    assert matches_action('payment_refund', '乙方应返还已付款。')
    assert not matches_action('payment_refund', '乙方应返还设备。')
    text = '乙方负责处理第三方索赔。'
    assert matches_action('third_party_claim_handling', text)
    assert not matches_action('third_party_liability_party', text)
    assert matches_action('third_party_liability_party', '乙方承担第三方权利主张责任。')


def test_licensing_facts_exclude_signing_place_and_incidental_validity_phrase():
    clauses = parse_contract_clauses('第一条\n双方在中国签字。合同有效期内应支付费用。')
    atoms = {a['element_id']: a for a in license_scope_elements(clauses)}
    assert atoms['license_territory']['status'] == atoms['license_term']['status'] == 'MISSING'


def test_registration_duty_and_cooperation_use_different_exact_sentences():
    clauses = parse_contract_clauses('第一条 专利申请权转让登记\n卖方应于10日内办理专利申请权转让登记。双方应提供申请人变更所需材料。')
    atoms = {a['element_id']: a for a in registration_elements(clauses)}
    assert all(a['status'] == 'COVERED' for a in atoms.values())
    assert '双方应提供' in atoms['registration_cooperation']['supporting_evidence'][0]['quote']
    assert '卖方应' in atoms['registration_deadline']['supporting_evidence'][0]['quote']


def test_functional_conformity_is_an_acceptance_criterion():
    atoms = {a['element_id']: a for a in extract_elements('development_scope', parse_contract_clauses(
        '第一条 验收\n系统应能够完成确认书列明的业务功能。乙方应交付源代码。'))}
    assert atoms['deliverables_and_acceptance']['status'] == 'COVERED'


def test_negative_search_is_prepared_before_positive_source_gate():
    item = make_item(); item.item_id = 'TC-02-02'; item.coverage_status = '通过'
    item.coverage_elements = [dict(element_id='affirmative_infringement_fact', status='NOT_APPLICABLE')]
    clauses = parse_contract_clauses('第一条\n第三方提出索赔时，乙方负责处理。')
    prepare_negative_audits([item], clauses)
    assert _verified_pass_sources([item], clauses)['status'] == 'REPORT_READY'
    clauses = parse_contract_clauses('第一条\n标的技术已经侵犯第三方专利。')
    prepare_negative_audits([item], clauses)
    assert _verified_pass_sources([item], clauses)['status'] == 'BLOCKED'
