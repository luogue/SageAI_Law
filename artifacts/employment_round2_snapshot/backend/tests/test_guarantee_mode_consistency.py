from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import json
import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import review_contract_v2
from review_v2.guarantee_mode import extract_mode, consistency_gate


@pytest.mark.parametrize('text, mode', [
    ('保证人承担一般保证责任。', 'GENERAL'),
    ('保证人提供连带责任保证。', 'JOINT'),
    ('保证人签字，负责担保。担保人代偿后有权追偿。', 'UNSPECIFIED'),
    ('原合同约定承担连带责任保证，本合同保证人承担一般保证责任。', 'GENERAL'),
    ('法律规定连带责任保证可以直接向保证人请求；本合同保证方式为一般保证。', 'GENERAL'),
    ('保证方式：□一般保证 □连带责任保证。', 'UNSPECIFIED'),
    ('保证方式为一般保证。保证人还承担连带责任保证。', 'CONFLICT'),
])
def test_operative_mode_not_mentions(text, mode):
    assert extract_mode(parse_contract_clauses(text))['mode'] == mode


@pytest.mark.parametrize('body, mode', [
    ('保证人承担一般保证责任。', 'GENERAL'),
    ('保证人承担连带责任保证。', 'JOINT'),
    ('保证人签字并负责担保。', 'UNSPECIFIED'),
    ('原合同约定承担连带责任保证，本合同约定承担一般保证责任。', 'GENERAL'),
])
def test_full_pipeline_exclusive_branches(body, mode):
    report = review_contract_v2('保证合同\n为借款合同的主债务提供保证。' + body + '保证人代偿后有权向债务人追偿。', 'guarantee', use_llm=False)
    rows = {r['item_id']:r for r in report['items']}
    assert rows['GUA-03-01']['coverage_status'] == '法律提示'
    assert rows['GUA-03-01']['risk_level'] == '低'
    if mode != 'UNSPECIFIED':
        assert rows['GUA-04-01']['coverage_status'] == '通过'
        assert rows['GUA-04-04']['coverage_status'] == '不适用'
        inactive = 'GUA-04-02' if mode == 'GENERAL' else 'GUA-04-03'
        assert rows[inactive]['coverage_status'] == '不适用'
        assert not any(inactive in f.get('source_review_ids',[]) or 'GUA-04-04' in f.get('source_review_ids',[]) for f in report['risk_findings'])
        assert all('追偿' not in e.get('quote', '') for e in rows['GUA-04-01']['evidence_clauses'])
    else:
        assert rows['GUA-04-04']['coverage_status'] == '缺失'
        assert rows['GUA-04-02']['coverage_status'] == rows['GUA-04-03']['coverage_status'] == '不适用'
        assert not any(e.get('source_type') == 'SOURCE_CLAUSE' and '追偿' in e.get('quote','') for e in rows['GUA-04-04']['evidence_clauses'])
    assert report['guarantee_mode_consistency_gate']['status'] == 'REPORT_READY'


def test_mutually_exclusive_status_mutation_is_blocked():
    item = SimpleNamespace(node_id='joint_guarantee_explicit_wording', item_id='GUA-04-02',
        coverage_status='缺失', decision_trace={'guarantee_mode_fact':{'mode':'GENERAL'}})
    assert consistency_gate([item])['status'] == 'BLOCKED'


def test_current_file_production_pipeline():
    from fastapi.testclient import TestClient
    from main import app
    from auth.routes import get_current_user
    path = next((Path(__file__).resolve().parents[2] / 'test_data').glob('51 *.docx'))
    old = app.dependency_overrides.get(get_current_user)
    app.dependency_overrides[get_current_user] = lambda: {'id':1,'phone':'test'}
    try:
        with TestClient(app) as client:
            response = client.post('/review-v2/file', files={'file':(path.name,path.read_bytes(),
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},
                data={'contract_type':'guarantee','use_llm':'false','include_low_risk':'true'})
        assert response.status_code == 200, response.text
        report = response.json()
        rows = {r['item_id']:r for r in report['items']}
        assert rows['GUA-04-01']['coverage_status'] == '通过'
        assert rows['GUA-04-02']['coverage_status'] == rows['GUA-04-04']['coverage_status'] == '不适用'
        assert rows['GUA-03-01']['coverage_status'] == '法律提示'
        assert rows['GUA-06-01']['coverage_status'] == rows['GUA-06-02']['coverage_status'] == '法律提示'
        assert rows['GUA-06-03']['coverage_status'] == rows['GUA-06-04']['coverage_status'] == '不适用'
        assert all(rows[f'GUA-10-0{n}']['coverage_status'] == '不适用' for n in range(1, 5))
        assert report['release_quality_gate']['status'] == 'REPORT_READY', report['release_quality_gate']
    finally:
        if old is None:
            app.dependency_overrides.pop(get_current_user, None)
        else:
            app.dependency_overrides[get_current_user] = old
