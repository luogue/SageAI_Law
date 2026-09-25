"""Document facts, disclosure audits and adjacent IP duties stay separate."""
import json
from pathlib import Path
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.contract_facts import extract_contract_fact_graph
from review_v2.license_control_facts import elements


@pytest.mark.parametrize('label', ['授权日', '授权日期', '授权公告日', '授权公告日期'])
def test_grant_date_alias_has_one_canonical_key_and_original_span(label):
    from review_v2.engine import _technology_registry_evidence
    text = f'第一条 专利信息\n{label}：2024年8月16日。'
    clauses = parse_contract_clauses(text)
    graph = extract_contract_fact_graph(clauses)
    rows = _technology_registry_evidence(graph, clauses, 'technology.patent.authorization_date')
    assert rows and all(label in r['quote'] and r['quote'] in text for r in rows)


@pytest.mark.parametrize('family', ['license_secret_controls', 'license_mutual_confidentiality'])
def test_sublicense_prohibition_is_not_information_disclosure(family):
    text = ('甲方不得再许可其他第三方实施专利。未经甲方书面同意，乙方不得向第三方授予分许可。'
            '未经信息提供方书面同意，接收方不得向第三方披露保密信息。')
    rows = elements(family, parse_contract_clauses(text))
    sources = next(e for e in rows if e['element_id'] in {
        'third_party_transfer_disclosure_restriction', 'third_party_disclosure_restriction'})['supporting_evidence']
    assert sources and all('披露保密信息' in s['quote'] for s in sources)


def test_delivery_heading_is_not_a_delivery_obligation():
    from review_v2.obligation_detail_elements import _delivery_sources
    text = '第四条 技术资料交付\n乙方应向甲方提供：\n安装说明书；\n操作手册。'
    rows = list(_delivery_sources(parse_contract_clauses(text)))
    assert rows and all('乙方应向甲方提供' in quote for _, _, quote in rows)


def test_inline_heading_metadata_does_not_erase_operative_delivery():
    from review_v2.obligation_detail_elements import _delivery_sources
    text = '第四条 技术资料：乙方应向甲方交付图纸、程序和操作手册。'
    rows = list(_delivery_sources(parse_contract_clauses(text)))
    assert rows and all('乙方应向甲方交付' in quote for _, _, quote in rows)


@pytest.fixture(scope='module')
def uploaded():
    from fastapi.testclient import TestClient
    from auth.utils import create_access_token
    from main import app
    source = Path(__file__).resolve().parents[2] / 'artifacts/technology_pass_semantics/round17_license_input/original.docx'
    with TestClient(app) as client:
        response = client.post('/review-v2/file',
            headers={'Authorization': 'Bearer ' + create_access_token({'user_id': '1'})},
            data={'contract_type': 'technology', 'use_llm': 'false',
                  'profile_json': json.dumps({'user_identity': '乙方'})},
            files={'file': ('original.docx', source.read_bytes(),
                           'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code == 200
    report = response.json()
    assert report['release_quality_gate']['status'] == 'REPORT_READY', json.dumps(report['release_quality_gate']['failures'], ensure_ascii=False)
    return {i['item_id']: i for i in report['items']}


@pytest.mark.parametrize('rule', ['TC-03-04', 'TC-13-02'])
def test_disclosed_facts_are_not_residual_audit_targets(uploaded, rule):
    item = uploaded[rule]
    assert next(e for e in item['coverage_elements'] if e['element_id'] ==
                'technology_patent_authorization_date')['status'] == 'COVERED'
    audit = item['decision_trace'].get('element_absence_searches', [])
    assert not any('既有许可披露' in e.get('search_targets', []) or
                   '专利授权日期' in e.get('search_targets', []) for e in audit)


@pytest.mark.parametrize('rule,forbidden', [('TC-11-01', '授予分许可'),
                                          ('TC-13-01', '第三方权利主张')])
def test_upload_does_not_publish_adjacent_topic_as_element_proof(uploaded, rule, forbidden):
    rows = uploaded[rule]['evidence_clauses']
    assert rows
    assert all(forbidden not in (r.get('quote') or r.get('quoted_text', '')) for r in rows)
    assert all((r.get('quote') or r.get('quoted_text')) != r.get('location')
               for r in rows if r.get('source_type') == 'BODY')
    if rule == 'TC-13-01':
        receipt = next(e for e in uploaded[rule]['coverage_elements'] if e['element_id'] == 'receipt_confirmation')
        assert receipt['source_spans']
        assert all('签署' in s or '签收' in s or '确认' in s for s in receipt['source_spans'])
