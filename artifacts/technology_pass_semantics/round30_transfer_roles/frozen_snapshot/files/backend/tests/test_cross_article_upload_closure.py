"""Normal multipart upload of the original cross-article licence fixture."""
import json
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace

import pytest
from docx import Document
from fastapi.testclient import TestClient
from auth.utils import create_access_token
from main import app
from review_v2.clause_parser import parse_contract_clauses
from review_v2.verified_source import verify_binding
from review_v2.ancillary_fee_facts import elements as fee_elements
from review_v2.license_control_facts import elements as license_elements
from review_v2.engine import _review_evidence_element_gate

SOURCE = Path(__file__).resolve().parents[2] / 'artifacts/technology_pass_semantics/round8_close_input_cross_article/original.docx'


def upload():
    with TestClient(app) as client:
        response = client.post('/review-v2/file',
            headers={'Authorization': 'Bearer ' + create_access_token({'user_id': '1'})},
            data={'contract_type': 'technology', 'use_llm': 'false', 'include_low_risk': 'true',
                  'profile_json': json.dumps({'user_identity': '甲方/被许可方'})},
            files={'file': ('original.docx', SOURCE.read_bytes(),
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code == 200, response.text[:1000]
    return response.json()


@pytest.fixture(scope='module')
def cross_article_upload():
    return upload()


def item(report, key):
    return next(i for i in report['items'] if i['item_id'] == key)


def test_original_cross_article_upload_complete_gate(cross_article_upload):
    report = cross_article_upload
    assert report['production_path_trace']['entrypoint'] == 'routers.review_v2.review_v2_file'
    assert report['release_quality_gate']['status'] == 'REPORT_READY', report['release_quality_gate']['failures']
    assert not report['release_quality_gate']['failures']
    # A publishable review still reports genuine gaps; READY is not no risk.
    assert item(report, 'TC-11-04')['coverage_status'] == '部分覆盖'
    assert any(f['risk_group'] == 'confidentiality_period_and_scope' for f in report['risk_findings'])


def test_cross_article_sources_remain_separate_and_verbatim(cross_article_upload):
    original = '\n'.join(p.text for p in Document(SOURCE).paragraphs)
    clauses = parse_contract_clauses(original)
    for rule in ('TC-07-01', 'TC-11-01', 'TC-11-02', 'TC-11-04'):
        review = item(cross_article_upload, rule)
        for row in review['evidence_clauses']:
            if row.get('source_type') == 'SEARCH_AUDIT':
                continue
            assert row['quote'] in original
            assert verify_binding(row, clauses) == []
            assert row['supporting_element_ids']
        for element in review['coverage_elements']:
            for source in element.get('supporting_evidence', []):
                clause = next(c for c in clauses if c.clause_id == source['clause_id'])
                assert source['quote'] in clause.text
    controls = item(cross_article_upload, 'TC-11-01')
    copying = next(e for e in controls['coverage_elements'] if e['element_id'] == 'purpose_scoped_copying_boundary')
    assert len(set(copying['source_clause_ids'])) >= 2
    assert any('为生产合同产品之目的' in q for q in copying['source_spans'])
    assert any('超出本合同目的使用' in q for q in copying['source_spans'])


def test_each_confidentiality_duration_has_its_own_source(cross_article_upload):
    review = item(cross_article_upload, 'TC-11-02')
    period = next(e for e in review['coverage_elements'] if e['element_id'] == 'confidentiality_period')
    assert period['status'] == 'COVERED'
    sources = period['supporting_evidence']
    assert {s['obligated_party'] for s in sources} == {'买方', '卖方'}
    assert {('5年' in s['quote'], '3年' in s['quote']) for s in sources} == {(True, False), (False, True)}
    assert len({s['clause_id'] for s in sources}) == 2


def test_remedies_are_not_inferred_from_confidentiality_scope(cross_article_upload):
    review = item(cross_article_upload, 'TC-11-04')
    elements = {e['element_id']: e for e in review['coverage_elements']}
    assert elements['breach_damage_liability']['status'] == 'COVERED'
    assert elements['mitigation_obligation']['status'] == 'PARTIALLY_COVERED'
    assert elements['incident_notification']['status'] == 'MISSING'
    for e in elements.values():
        for s in e.get('supporting_evidence', []):
            assert '保密内容：' not in s['quote']


def test_price_component_has_explicit_total_and_instalment_sources(cross_article_upload):
    review = item(cross_article_upload, 'TC-09-04')
    elements = {e['element_id']: e for e in review['coverage_elements']}
    assert elements['service_fee_amount']['status'] == 'COVERED'
    assert elements['service_payment_schedule']['status'] == 'COVERED'
    assert any('200,000' in s['quote'] for s in elements['service_fee_amount']['supporting_evidence'])
    assert len(set(elements['service_payment_schedule']['source_clause_ids'])) >= 3


def test_product_metrics_do_not_prove_support_service_acceptance(cross_article_upload):
    review = item(cross_article_upload, 'TC-09-02')
    assert review['decision_trace']['atomic_requirement_family'] == 'service_acceptance'
    assert all(e['status'] == 'MISSING' for e in review['coverage_elements'])
    assert all(e.get('source_type') == 'SEARCH_AUDIT' for e in review['evidence_clauses'])


def test_removed_element_publication_is_still_blocked(cross_article_upload):
    review = SimpleNamespace(**deepcopy(item(cross_article_upload, 'TC-11-02')))
    assert _review_evidence_element_gate([review])['mismatch_count'] == 0
    review.evidence_clauses = [r for r in review.evidence_clauses if 'confidentiality_period' not in r.get('supporting_element_ids', [])]
    assert _review_evidence_element_gate([review])['mismatch_count'] > 0


def test_repeated_normal_upload_has_idempotent_states_and_spans(cross_article_upload):
    repeated = upload()
    def signature(report):
        return [(i['item_id'], i['coverage_status'],
                 [(e['element_id'], e['status'], e.get('source_fact_key'), e.get('source_clause_ids'), e.get('source_spans'))
                  for e in i['coverage_elements']],
                 [(r.get('evidence_id'), r.get('clause_id'), r.get('quote'), r.get('supporting_element_ids'))
                  for r in i['evidence_clauses']]) for i in report['items']]
    assert signature(repeated) == signature(cross_article_upload)
    assert repeated['release_quality_gate']['status'] == 'REPORT_READY'


@pytest.mark.parametrize('label', ['技术服务及指导费', '技术支持和培训费用', '技术指导费'])
def test_coordinated_fee_names_share_atomic_price_predicate(label):
    text = f'第一条 使用费\n技术秘密使用费总额：人民币90000元。其中{label}：人民币12000元。\n第二条 付款\n确认后10日内支付合同总额的50%；完成后支付剩余50%。'
    facts = {e['element_id']: e for e in fee_elements(parse_contract_clauses(text))}
    assert facts['service_fee_amount']['status'] == 'COVERED'
    assert facts['service_payment_schedule']['status'] == 'COVERED'
    assert all(s['quote'] in text for e in facts.values() for s in e['supporting_evidence'])


def test_service_promise_and_separate_price_do_not_imply_inclusion():
    text = '第一条 许可费\n许可费总额90000元。第二条 服务\n技术服务和指导由乙方提供。第三条 付款\n十日内支付合同总额的50%。'
    facts = {e['element_id']: e for e in fee_elements(parse_contract_clauses(text))}
    assert facts['service_fee_amount']['status'] == 'MISSING'
    assert facts['service_payment_schedule']['status'] == 'MISSING'


def test_historical_grant_does_not_supply_current_scope():
    text = '第一条 既有许可\n卖方曾向第三方授予独占许可，许可期限：十年。\n第二条 本次交易\n买方取得本技术秘密许可，实施方式另行协商。'
    facts = {e['element_id']: e for e in license_elements('secret_license_scope', parse_contract_clauses(text))}
    assert facts['license_type']['status'] == 'MISSING'
    assert facts['license_term']['status'] == 'MISSING'
