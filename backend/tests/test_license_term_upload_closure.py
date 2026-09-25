"""License term evidence and whole-report authenticated upload regression."""
import io
import json

import pytest
from docx import Document
from fastapi.testclient import TestClient

from auth.utils import create_access_token
from main import app
from review_v2 import engine
from review_v2.clause_parser import parse_contract_clauses
from tests.test_technical_secret_license_contract_review import BASE_SECRET_LICENSE
from tests.test_technology_exact_truth_pipeline import make_item


@pytest.mark.parametrize('term,covered', [
    ('许可期限五年。', True),
    ('许可期限十二个月。', True),
    ('实施期限为两年。', True),
    ('合同有效期为2.5年。', True),
    ('许可期限自2026年1月1日起至2031年1月1日。', True),
    ('许可期限三十六个月。', True),
    ('许可期限____年。', False),
    ('双方保密期限为五年。', False),
])
def test_license_term_uses_shared_duration_grammar_and_own_evidence(term,covered):
    text='技术秘密许可合同\n第一条 '+term
    item=make_item();item.item_id='TC-07-01'
    engine._apply_technology_transaction_evidence_consistency([item],text,
        {'primary_subtype':'TECHNOLOGY_LICENSE','tertiary_subtype':'TECHNICAL_SECRET_LICENSE'})
    element=next(e for e in item.coverage_elements if e['element_id']=='license_term')
    assert element['status']==('COVERED' if covered else 'MISSING')
    if covered:
        assert element['evidence_ids']
        sources={c.clause_id:c.text for c in parse_contract_clauses(text)}
        assert all(span in sources[cid] for cid,span in zip(element['source_clause_ids'],element['source_spans']))
    else:
        assert element['evidence_ids']==[]


def test_balanced_secret_license_authenticated_upload_is_publishable_with_real_gaps():
    doc=Document()
    for line in BASE_SECRET_LICENSE.splitlines():
        doc.add_paragraph(line)
    data=io.BytesIO();doc.save(data)
    token=create_access_token({'user_id':'1'})
    # Real auth dependency and multipart upload route; no engine/gate overrides.
    with TestClient(app) as client:
        response=client.post('/review-v2/file',
            headers={'Authorization':'Bearer '+token},
            data={'contract_type':'technology','use_llm':'false','include_low_risk':'true',
                  'profile_json':json.dumps({'user_identity':'甲方/被许可方'})},
            files={'file':('secret-license.docx',data.getvalue(),
                          'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code==200,response.text[:1000]
    report=response.json()
    assert report['release_quality_gate']['status']=='REPORT_READY',report['release_quality_gate']['failures']
    assert report['release_quality_gate']['failures']==[]
    assert report['production_path_trace']['run_mode']=='review'
    assert report['production_path_trace']['entrypoint']=='routers.review_v2.review_v2_file'
    scope=next(i for i in report['items'] if i['item_id']=='TC-07-01')
    term=next(e for e in scope['coverage_elements'] if e['element_id']=='license_term')
    assert term['status']=='COVERED'
    assert any('许可期限五年' in s for s in term['source_spans'])
    assert next(i for i in report['items'] if i['item_id']=='TC-11-02')['coverage_status']=='通过'
    # A publishable report must retain actual missing safeguards, not erase risks.
    assert next(e for e in scope['coverage_elements'] if e['element_id']=='transfer_or_sublicense_boundary')['status']=='MISSING'
    assert {'license_over_scope_liability','license_infringement_responsibility',
            'third_party_claim_defense','technology_license_scope',
            'confidential_material_return_destroy','confidentiality_breach_liability'} <= {
                f['risk_group'] for f in report['risk_findings']}
    assert report['risk_findings']
