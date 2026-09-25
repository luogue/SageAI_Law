"""Whole-upload closure and strict negative guards for typed risk evidence."""
import io
import json
from copy import deepcopy
from types import SimpleNamespace

import pytest
from docx import Document
from fastapi.testclient import TestClient

from auth.utils import create_access_token
from main import app
from review_v2.clause_parser import parse_contract_clauses
from review_v2.confidentiality_remedies import canonical_confidentiality_remedies
from review_v2.engine import _review_evidence_element_gate
from review_v2.narrative_evidence import narrative_evidence_gate
from tests.test_technical_secret_transfer_contract_review import _fixture_text


@pytest.fixture(scope='module')
def uploaded_transfer():
    document = Document()
    for line in _fixture_text().splitlines():
        document.add_paragraph(line)
    buffer = io.BytesIO(); document.save(buffer)
    with TestClient(app) as client:
        response = client.post('/review-v2/file',
            headers={'Authorization': 'Bearer ' + create_access_token({'user_id': '1'})},
            data={'contract_type': 'technology', 'use_llm': 'false', 'include_low_risk': 'true',
                  'profile_json': json.dumps({'user_identity': '甲方/技术秘密受让方'})},
            files={'file': ('transfer.docx', buffer.getvalue(),
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code == 200, response.text[:1000]
    return response.json()


def test_original_ancillary_upload_is_ready_and_retains_actual_risks(uploaded_transfer):
    report = uploaded_transfer
    assert report['release_quality_gate']['status'] == 'REPORT_READY', report['release_quality_gate']['failures']
    assert report['release_quality_gate']['failures'] == []
    assert report['production_path_trace']['entrypoint'] == 'routers.review_v2.review_v2_file'
    assert {'payment_formula_inconsistency', 'technical_timeline_conflict',
            'generic_liability_cap_validity', 'generic_potential_excessive_liquidated_damages',
            'confidential_material_return_destroy'} <= {f['risk_group'] for f in report['risk_findings']}
    assert report['release_quality_gate']['gate_results']['NARRATIVE_EVIDENCE_GATE'] == 'PASS'


def test_original_fee_does_not_infer_included_total_price(uploaded_transfer):
    item = next(i for i in uploaded_transfer['items'] if i['item_id'] == 'TC-09-04')
    elements = {e['element_id']: e for e in item['coverage_elements']}
    assert item['coverage_status'] == '部分覆盖'
    assert elements['service_fee_amount']['status'] == 'PARTIALLY_COVERED'
    assert elements['service_payment_schedule']['status'] == 'MISSING'
    assert elements['extra_service_pricing_standard']['status'] == 'MISSING'


@pytest.mark.parametrize('ordinary', [
    '乙方违约的赔偿总额以合同价款20%为限。',
    '甲方违反实施范围或者擅自转让技术秘密的，支付转让费50%的违约金。',
])
def test_mixed_liability_article_does_not_inherit_confidentiality_trigger(ordinary):
    text = '第一条 违约责任\n甲方违反保密义务，应赔偿乙方损失。\n' + ordinary
    elements = canonical_confidentiality_remedies(parse_contract_clauses(text))
    proofs = [f for e in elements for f in e['supporting_evidence']]
    assert proofs
    assert all(ordinary not in f['quote'] for f in proofs)
    assert {f['obligated_party'] for f in proofs} == {'甲方'}


def test_both_parties_explicit_confidentiality_remedies_remain_covered():
    elements = canonical_confidentiality_remedies(parse_contract_clauses(
        '第一条 保密责任\n甲方违反保密义务，应赔偿乙方损失。\n乙方违反保密义务，应赔偿甲方损失。'))
    damage = next(e for e in elements if e['element_id'] == 'breach_damage_liability')
    assert damage['status'] == 'COVERED'
    assert {r['obligated_party'] for r in damage['party_coverage']} == {'甲方', '乙方'}


@pytest.mark.parametrize('review_id', ['TC-06-02', 'GEN-LIAB-02', 'GEN-LIAB-03'])
def test_review_exact_mapping_rejects_removed_proof(uploaded_transfer, review_id):
    item = SimpleNamespace(**deepcopy(next(i for i in uploaded_transfer['items'] if i['item_id'] == review_id)))
    assert _review_evidence_element_gate([item])['mismatch_count'] == 0
    item.evidence_clauses = []
    assert _review_evidence_element_gate([item])['mismatch_count'] > 0


@pytest.mark.parametrize('group', ['payment_formula_inconsistency', 'technical_timeline_conflict'])
def test_derived_risk_must_publish_calculation_element_ownership(uploaded_transfer, group):
    findings = [SimpleNamespace(**deepcopy(f)) for f in uploaded_transfer['risk_findings']]
    items = [SimpleNamespace(**deepcopy(i)) for i in uploaded_transfer['items']]
    target = next(f for f in findings if f.risk_group == group)
    calculations = [row for row in target.evidence_bundle['items'] if row.get('source_type') == 'CALCULATION']
    assert calculations and all(row.get('supporting_element_ids') and row.get('supporting_review_ids') for row in calculations)
    assert all(row.get('derived_from_evidence_ids') for row in calculations)
    for row in target.evidence_bundle['items']:
        row['supporting_element_ids'] = []
        row['supporting_review_ids'] = []
    gate = narrative_evidence_gate(items, findings)
    assert gate['status'] == 'BLOCKED'
    assert any(f.get('risk_id') == target.finding_id
               for failure in gate['failures'] for f in failure['details'])
