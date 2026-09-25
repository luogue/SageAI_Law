"""Direct evidence and final projections for confidentiality and acceptance."""
import pytest
from types import SimpleNamespace
from copy import deepcopy
from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routers import review_v2 as route
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import _atomic_requirement_family
from review_v2.engine import _review_evidence_element_gate


def test_exact_binding_rejects_theme_span_and_wrong_element():
    fact = {'clause_id': 'C1', 'quote': '双方应保密。'}
    element = {'element_id': 'duty', 'status': 'COVERED', 'source_fact_key': 'duty', 'supporting_evidence': [fact]}
    evidence = {'clause_id': 'C1', 'quote': fact['quote'], 'support_type': 'DIRECT', 'supporting_element_ids': ['duty']}
    item = SimpleNamespace(item_id='TEST', coverage_elements=[element], evidence_clauses=[evidence],
                           decision_trace={'direct_fact_bindings': {'duty': [fact]}, 'direct_element_fact_keys': {'duty': 'duty'}})
    assert _review_evidence_element_gate([item])['mismatch_count'] == 0
    for mutation in ({'quote': '双方应保密。其他义务另行协商。'}, {'supporting_element_ids': ['other']}, {'support_type': 'CONTEXTUAL'}):
        bad = deepcopy(item)
        bad.evidence_clauses[0].update(mutation)
        assert _review_evidence_element_gate([bad])['status'] == 'BLOCKED'


def rows(family, text):
    return {r['element_id']: r for r in _atomic_requirement_family(family, parse_contract_clauses(text))}


def test_confidentiality_list_and_disclosure_prohibition_are_positive():
    r = rows('confidentiality_detail', '第十二条 保密\n以下信息均属于保密信息：\n软件代码；\n经营数据。\n未经披露方同意，任何一方不得向第三方披露。\n合同终止后删除资料。')
    assert {k for k, v in r.items() if v['status'] == 'COVERED'} == {'confidential_information_scope', 'during_contract_confidentiality'}
    assert {k for k, v in r.items() if v['status'] == 'MISSING'} == {'post_termination_confidentiality', 'confidentiality_duration', 'confidentiality_exceptions'}
    assert all(v['supporting_evidence'] for v in r.values() if v['status'] == 'COVERED')


def test_acceptance_method_does_not_entail_documents_or_dispute_retest():
    r = rows('development_acceptance', '第五条 验收\n准确率不低于95%。\n双方进行功能测试、数据测试。\n未通过验收的重新申请验收。')
    assert {k for k, v in r.items() if v['status'] == 'COVERED'} == {'acceptance_metrics', 'acceptance_method'}
    assert all(not v['supporting_evidence'] for v in r.values() if v['status'] == 'MISSING')


@pytest.mark.parametrize('text,key', [
    ('乙方应提交测试报告。', 'test_report_delivery'),
    ('双方应签署验收记录。', 'acceptance_record_requirement'),
    ('乙方应编制测试用例。', 'test_case_requirement'),
    ('验收争议由第三方检测。', 'acceptance_dispute_verification'),
])
def test_acceptance_atoms_require_their_own_evidence(text, key):
    r = rows('development_acceptance', '第五条 验收\n' + text)
    assert {k for k, v in r.items() if v['status'] == 'COVERED'} == {key}
    assert r[key]['supporting_evidence'][0]['quote'] == text


def test_uploaded_development_contract_truth_projection():
    app = FastAPI()
    app.include_router(route.router)
    app.dependency_overrides[route.get_current_user] = lambda: {'id': 1}
    source = Path(__file__).resolve().parents[2] / 'test_data' / '88 委托开发合同.docx'
    with TestClient(app) as client:
        response = client.post('/review-v2/file', data={'contract_type': 'technology', 'use_llm': 'false'},
                               files={'file': (source.name, source.read_bytes())})
    assert response.status_code == 200
    report = response.json()
    for rule in ('TC-11-02', 'TC-13-03'):
        item = next(i for i in report['items'] if i['item_id'] == rule)
        assert item['coverage_status'] == '部分覆盖'
        covered = [e for e in item['coverage_elements'] if e['status'] == 'COVERED']
        assert covered and all(e['supporting_evidence'] for e in covered)
        bundle = next(f['evidence_bundle']['items'] for f in report['risk_findings'] if rule in f['source_review_ids'])
        for element in covered:
            expected = {e['evidence_id'] for e in bundle
                        if element['element_id'] in e.get('supporting_element_ids', [])
                        and any(f['clause_id'] == e.get('clause_id') and f['quote'] == e.get('quoted_text')
                                for f in element['supporting_evidence'])}
            assert expected and set(element['supporting_evidence_ids']) == expected
        for element in covered:
            for evidence in element['supporting_evidence']:
                assert any(evidence['quote'] in (e.get('quote') or e.get('text') or '') for e in item['evidence_clauses'])
        finding = next(f for f in report['risk_findings'] if rule in f['source_review_ids'])
        assert {e['element_id'] for e in finding['final_missing_elements']} == {
            e['element_id'] for e in item['coverage_elements'] if e['status'] == 'MISSING'}
    assert not any(f['requirement'] == 'NARRATIVE_TRUTH_GATE' for f in report['release_quality_gate']['failures'])
    assert not any(f['requirement'] == 'REVIEW_EVIDENCE_ELEMENT_MISMATCH' for f in report['release_quality_gate']['failures'])


def test_classification_pass_has_no_insufficient_narrative():
    app = FastAPI(); app.include_router(route.router)
    app.dependency_overrides[route.get_current_user] = lambda: {'id': 1}
    source = Path(__file__).resolve().parents[2] / 'test_data' / '88 委托开发合同.docx'
    with TestClient(app) as client:
        response = client.post('/review-v2/file', data={'contract_type': 'technology', 'use_llm': 'false'}, files={'file': (source.name, source.read_bytes())})
    report = response.json()
    item = next(i for i in report['items'] if i['item_id'] == 'TC-01-02')
    assert item['coverage_status'] == '通过'
    assert '不足' not in item['reasoning_summary']
    assert '委托开发合同' in item['reasoning_summary']
    assert '测试用例、测试报告和验收记录要求明确' not in report['result']
