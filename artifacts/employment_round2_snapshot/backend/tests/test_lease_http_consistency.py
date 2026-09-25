"""Exercise the HTTP response contract, rather than only the engine return value."""
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from routers import review_v2 as route
from .test_lease_deadline_and_children import core_projection


def client():
    app = FastAPI()
    app.include_router(route.router)
    # Test-only authenticated principal; production auth is unchanged.
    app.dependency_overrides[route.get_current_user] = lambda: 1
    return TestClient(app)


def upload(http):
    path = Path(__file__).resolve().parents[2] / 'test_data/53 租赁合同.docx'
    return http.post('/review-v2/file', data={'contract_type': 'lease', 'use_llm': 'false'},
                     files={'file': (path.name, path.read_bytes(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})


def test_http_repeat_preserves_evidence_children_and_release_hold(monkeypatch):
    monkeypatch.setenv('REVIEW_V2_RELEASE_HOLD_DOMAINS', 'lease')
    with client() as http:
        first, second = upload(http), upload(http)
    assert first.status_code == second.status_code == 200
    a, b = first.json(), second.json()
    assert core_projection(a) == core_projection(b)
    assert a['coverage_summary'] == b['coverage_summary']
    assert b['release_quality_gate']['status'] == 'BLOCKED'
    assert b['release_hold']['active']
    assert b['technical_quality_gate']['status'] == 'REPORT_READY'
    assert b['recommendation_children_gate']['status'] == 'REPORT_READY'
    theme = next(r for r in b['recommendation_children_gate']['rows'] if r['risk_id'] == 'RF-PROPERTY-DAMAGE-001')
    assert theme['actionable_child_ids'] == theme['theme_child_ids'] == theme['formal_child_ids']
    assert not theme['missing_top_fragments']
    for item in b['items']:
        if item['node_id'] in {'deposit_return_deadline', 'sale_notice_preemption'}:
            assert item['coverage_status'] == '通过'
            assert all(s['result'] == 'FOUND' for s in item['decision_trace']['element_absence_searches'])


@pytest.mark.parametrize('dependency', ['lease_semantics', 'lease_recommendation_children', 'lease_fact_graph', 'clause_parser'])
def test_changed_lease_dependency_rejects_stale_worker(monkeypatch, dependency):
    original = route._runtime_source_identity
    target = route._RUNTIME_SOURCE_TARGETS[dependency]
    def changed(obj):
        value = original(obj)
        return {**value, 'sha256': 'modified-test-source'} if obj is target else value
    monkeypatch.setattr(route, '_runtime_source_identity', changed)
    assert dependency in route._runtime_source_drift_status()['changed_dependencies']
    with client() as http:
        response = upload(http)
    assert response.status_code == 503
    assert '旧代码' in response.json()['detail']
