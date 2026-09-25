"""Canonical truth and exact published bindings through the real upload route."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from routers import review_v2 as route
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import (
    _atomic_requirement_family, _apply_development_exit_atomic_state,
    _review_evidence_element_gate, _technology_proposition_quote,
    ReviewItemResult,
)
from review_v2.development_exit import development_exit_elements
from review_v2.verified_source import bind_original, exact_span, verify_binding
from review_v2.contract_facts import extract_contract_fact_graph


def atoms(family, text):
    return {e['element_id']: e for e in _atomic_requirement_family(family, parse_contract_clauses(text))}


SECRECY = '''第十条 保密
任何一方知悉的对方非公开技术资料、经营数据、客户信息及商业计划均属于保密信息。
接受方不得向无权知悉的第三方披露或用于本合同以外的目的。
以下信息不属于保密信息：
1. 已经合法公开的信息；
2. 接受方从有权披露的第三方合法取得的信息；
3. 接受方未使用对方资料独立开发形成的信息。
法律法规或有权机关要求披露的，不视为违约。
保密义务在本合同终止后继续有效五年。'''


def test_scope_numbered_exceptions_and_survival_have_positive_sources():
    result = atoms('confidentiality_detail', SECRECY)
    assert all(e['status'] == 'COVERED' and e['supporting_evidence'] for e in result.values())
    exceptions = result['confidentiality_exceptions']
    quotes = [s['quote'] for s in exceptions['supporting_evidence']]
    assert any('以下信息不属于保密信息' in q and '独立开发' in q for q in quotes)
    assert any('有权机关' in q and '不视为违约' in q for q in quotes)


@pytest.mark.parametrize('text', [
    '第十条 保密\n经营数据不属于保密信息。',
    '第十条 保密\n保密范围尚未约定。',
])
def test_excluded_or_unresolved_scope_is_not_positive_scope(text):
    assert atoms('confidentiality_detail', text)['confidential_information_scope']['status'] == 'MISSING'


def test_exception_heading_does_not_leak_into_another_article():
    result = atoms('confidentiality_detail', '第一条 保密\n以下信息不属于保密信息：\n1. 已经合法公开的信息。\n第二条 开发\n乙方独立开发软件。')
    row = result['confidentiality_exceptions']
    assert row['status'] == 'PARTIALLY_COVERED'
    assert '独立开发信息例外' in row['search_targets']


@pytest.mark.parametrize('wording', [
    '未按约定时间完成最终交付', '未按期交付', '迟延交付',
])
def test_development_delivery_delay_is_not_discarded(wording):
    rows = {e['element_id']: e for e in development_exit_elements(parse_contract_clauses(
        f'技术委托开发合同\n第一条 违约\n乙方{wording}，每逾期一日按合同总价1%支付违约金。'))}
    assert rows['development_delay_liability']['status'] == 'COVERED'
    assert rows['development_delay_liability']['supporting_evidence']
    assert rows['exit_source_code_handover']['status'] == 'MISSING'
    assert rows['payment_delay_liability']['status'] == 'MISSING'


def test_goods_delay_is_not_research_delay():
    result = development_exit_elements(parse_contract_clauses('货物买卖合同\n第一条 违约\n乙方未按约定时间完成最终交付，每逾期一日支付违约金。'))
    assert next(e for e in result if e['element_id'] == 'development_delay_liability')['status'] == 'MISSING'


def test_survival_heading_and_post_exit_disposal_do_not_prove_a_termination_right():
    text = ('技术开发合同\n第一条 合同解除\n保密义务在本合同终止后继续有效五年。'
            '\n合同解除后，乙方应交付源代码。\n第二条 违约\n甲方有权解除合同并要求退还款项。')
    row = next(e for e in development_exit_elements(parse_contract_clauses(text))
               if e['element_id'] == 'development_termination_mechanism')
    assert row['status'] == 'COVERED'
    assert [s['quote'] for s in row['supporting_evidence']] == ['甲方有权解除合同并要求退还款项']


def test_exit_principles_retain_positive_sources_and_search_only_residuals():
    rows = {e['element_id']: e for e in development_exit_elements(parse_contract_clauses(
        '技术开发合同\n第一条 退出\n合同解除后，乙方应移交已经完成的项目成果和相关资料。'
        '\n合同解除后，开发费用的结算另行协商。'))}
    assert rows['exit_stage_result_handover']['status'] == 'COVERED'
    for key in ('exit_research_material_handover', 'exit_development_cost_settlement'):
        row = rows[key]
        assert row['status'] == 'PARTIALLY_COVERED' and row['supporting_evidence']
        assert row['search_targets'] == [row['residual_gap']]
        assert row['required_fact'] not in row['search_targets']
    assert rows['exit_source_code_handover']['status'] == 'MISSING'


def test_delayed_completion_resolves_to_a_canonical_penalty_not_an_evaluation():
    text = '第一条 违约\n乙方未按约定时间完成最终交付，每逾期一日，按合同总价的1%向甲方支付违约金。'
    facts = extract_contract_fact_graph(parse_contract_clauses(text)).matching(['liability.penalty'])
    assert len(facts) == 1
    value = facts[0].value
    assert value['trigger'] == '未按约定时间完成最终交付'
    assert value['rate'] == '1%' and value['base'] == '合同总价'
    assert value['trigger'] in value['raw_clause']
    assert '高额' not in value['raw_clause']


def make_item():
    return ReviewItemResult(item_id='TC-05-04', node_id='cooperation_breach_and_exit',
        title='技术开发违约和项目退出', risk_level='中', status='部分覆盖',
        coverage_status='部分覆盖', issue_type='PARTIAL', risk_point_description='',
        suggested_clause_example='', legal_basis_index='', legal_consequence_if_missing='',
        applicable_if='', matched_terms=[], evidence_clauses=[], evidence_location='',
        reasoning_summary='', applicability={'status': 'APPLICABLE'})


def test_exact_binding_survives_element_adapter_and_rejects_theme_binding():
    item = make_item()
    clauses = parse_contract_clauses('技术开发合同\n第一条 违约\n乙方未按期交付，应支付违约金。')
    _apply_development_exit_atomic_state(item, clauses)
    row = next(e for e in item.coverage_elements if e['element_id'] == 'development_delay_liability')
    assert row['source_spans'] and row['source_locations']
    assert row['source_clause_ids'] == [clauses[-1].clause_id]
    assert _review_evidence_element_gate([item])['mismatch_count'] == 0
    for mutation in ('wrong_target', 'context_only', 'whole_clause', 'missing_registry_binding'):
        bad = deepcopy(item)
        evidence = bad.evidence_clauses[0]
        if mutation == 'wrong_target': evidence['supporting_element_ids'] = ['payment_delay_liability']
        if mutation == 'context_only': evidence['support_type'] = 'CONTEXTUAL'
        if mutation == 'whole_clause': evidence['quote'] = clauses[-1].text
        if mutation == 'missing_registry_binding': bad.decision_trace['direct_fact_bindings'] = {}
        assert _review_evidence_element_gate([bad])['status'] == 'BLOCKED', mutation


def test_verification_keeps_selected_span_not_retrieval_context():
    clauses = parse_contract_clauses('第一条 保密\n双方应保密。第二项义务另行协商。')
    original = clauses[-1]
    row = bind_original({'clause_id': original.clause_id, 'text': original.text, 'quote': '双方应保密。'}, clauses)
    assert row['quote'] == '双方应保密。'
    assert verify_binding(row, clauses) == []


def test_multi_sentence_excerpt_is_contiguous_not_reassembled():
    text = '项目名称：甲系统。\n功能包括：\n1. 报表；\n2. 查询；\n3. 导出。\n交付时应提供文档。'
    quote = _technology_proposition_quote(text, ['项目名称', '交付'])
    assert exact_span(text, quote) is not None
    assert '2. 查询' in quote


def test_ownership_mentions_do_not_prove_document_delivery():
    result = atoms('development_documents', '第一条 成果\n软件源代码、技术文档和接口文档归甲方所有。')
    assert all(e['status'] == 'MISSING' for e in result.values())


def test_delivery_list_binds_verb_and_object_without_borrowing_siblings():
    text = '第一条 交付\n乙方应向甲方提交：\n1. 源代码；\n2. API接口文档；\n3. 用户操作手册。'
    result = atoms('development_documents', text)
    assert result['interface_document_delivery']['status'] == 'COVERED'
    assert '提交' in result['interface_document_delivery']['supporting_evidence'][0]['quote']
    assert result['architecture_document_delivery']['status'] == 'MISSING'
    assert result['test_report_delivery']['status'] == 'MISSING'


@pytest.fixture(scope='module')
def uploaded_report():
    app = FastAPI()
    app.include_router(route.router)
    app.dependency_overrides[route.get_current_user] = lambda: {'id': 1}
    # This development regression must retain the original development input.
    # The UI scratch file 122 is now a patent-right transfer, for which the
    # development-exit checkpoint is correctly not applicable. Assertions stay
    # unchanged; the patent upload has its own end-to-end regression.
    path = (Path(__file__).resolve().parents[2] /
            'artifacts/technology_pass_semantics/round14_entrusted_input/original.docx')
    with TestClient(app) as client:
        response = client.post('/review-v2/file', data={'contract_type': 'technology', 'use_llm': 'false'},
                               files={'file': (path.name, path.read_bytes())})
    assert response.status_code == 200
    return response.json()


def test_production_route_confidentiality_truth_is_covered(uploaded_report):
    item = next(i for i in uploaded_report['items'] if i['item_id'] == 'TC-11-02')
    assert item['coverage_status'] == '通过'
    assert all(e['status'] == 'COVERED' for e in item['coverage_elements'])
    assert all(e['supporting_evidence'] for e in item['coverage_elements'])


def test_production_route_exit_has_exact_positive_and_separate_absence(uploaded_report):
    item = next(i for i in uploaded_report['items'] if i['item_id'] == 'TC-05-04')
    assert item['coverage_status'] == '部分覆盖'
    delay = next(e for e in item['coverage_elements'] if e['element_id'] == 'development_delay_liability')
    assert delay['status'] == 'COVERED'
    finding = next(f for f in uploaded_report['risk_findings'] if 'TC-05-04' in f['source_review_ids'])
    assert delay['element_id'] not in {e['element_id'] for e in finding['final_missing_elements']}
    sources = finding['evidence_bundle']['items']
    assert any(delay['element_id'] in s.get('supporting_element_ids', [])
               and s.get('quoted_text') == delay['supporting_evidence'][0]['quote'] for s in sources)
    for gap in finding['final_missing_elements']:
        audits = [s for s in sources if s.get('source_type') == 'SEARCH_AUDIT'
                  and gap['element_id'] in s.get('searched_absent_element_ids', [])]
        assert audits, gap['element_id']
        assert all(s['searched_absent_element_ids'] == [gap['element_id']] for s in audits)


def test_production_release_gate_still_checks_all_layers(uploaded_report):
    gate = uploaded_report['release_quality_gate']
    assert gate['status'] == 'REPORT_READY', gate.get('failures')
    assert not gate['failures']
