"""Real multipart production pipeline must not be hijacked by diagnostic state."""
import os
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routers import review_v2 as route

ROOT = Path(__file__).resolve().parents[2]


def client():
    app = FastAPI()
    app.include_router(route.router)
    app.dependency_overrides[route.get_current_user] = lambda: {"id": 1}
    return TestClient(app)


def upload(http, endpoint, filename, **data):
    path = ROOT / 'test_data' / filename
    return http.post(endpoint, data=data, files={
        'file': (path.name, path.read_bytes(),
                 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})


@pytest.mark.parametrize('kind,filename', [
    ('gift', '65 赠与合同.docx'),
    ('utility_supply', '62 供用水电气热力合同.docx'),
])
def test_normal_upload_generates_report_despite_legacy_diagnostic_env(monkeypatch, tmp_path, kind, filename):
    target = tmp_path / 'must-not-write.json'
    monkeypatch.setenv('REVIEW_V2_ONCE_INPUT_TRACE', str(target))
    with client() as http:
        response = upload(http, '/review-v2/file', filename,
                          contract_type=kind, use_llm='false')
    assert response.status_code == 200, response.text
    result = response.json()
    assert result['items'] and result['result']
    assert result['production_path_trace']['run_mode'] == 'review'
    assert result['release_quality_gate']['status'] == 'REPORT_READY'
    assert not result['release_quality_gate']['failures']
    assert '本次仅执行生产入口诊断' not in result['result']
    assert not target.exists()
    assert os.environ['REVIEW_V2_ONCE_INPUT_TRACE'] == str(target)


@pytest.mark.parametrize('persist', [False, True])
def test_explicit_diagnostic_never_calls_report_engine(monkeypatch, tmp_path, persist):
    if persist:
        monkeypatch.setenv('REVIEW_V2_ONCE_INPUT_TRACE', str(tmp_path / 'trace.json'))
    else:
        monkeypatch.delenv('REVIEW_V2_ONCE_INPUT_TRACE', raising=False)
    def forbidden(*args, **kwargs):
        raise AssertionError('Diagnostic request must not generate a report')
    monkeypatch.setattr(route, 'review_contract_v2', forbidden)
    with client() as http:
        response = upload(http, '/review-v2/diagnostics/input-trace', '65 赠与合同.docx')
    assert response.status_code == 200, response.text
    trace = response.json()
    assert trace['run_mode'] == 'diagnostic'
    assert trace['report_generated'] is False and trace['report_id'] is None
    assert 'result' not in trace
    assert (tmp_path / 'trace.json').exists() == persist
