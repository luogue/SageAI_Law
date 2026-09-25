import io

import pytest
from docx import Document
from fastapi import FastAPI
from fastapi.testclient import TestClient

from review_v2.final_snapshot import SnapshotStore
from routers.review_v2 import router, get_current_user


@pytest.fixture
def scenario(tmp_path, monkeypatch):
    path = tmp_path / 'snapshots.db'
    monkeypatch.setenv('REVIEW_V2_SNAPSHOT_DB', str(path))
    store = SnapshotStore(path)
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_current_user] = lambda: 17
    result = {'result': '# 最终审查报告\n当前版本的结论。', 'filename': 'example.docx',
              'release_quality_gate': {'status': 'REPORT_READY', 'failures': [], 'blocking_rules': []}}
    done = store.complete(store.begin(17), result)
    return TestClient(app), store, done


@pytest.mark.parametrize('format', ['docx','pdf'])
def test_export_uses_server_report_and_exact_binding(scenario, format):
    client, _, done = scenario
    response = client.post('/review-v2/export-' + format, json={'final_review_snapshot':done['final_review_snapshot']})
    assert response.status_code == 200, response.text
    assert response.headers['X-Review-Run-Id'] == done['review_run_id']
    assert response.headers['X-Report-Version'] == done['report_version']
    assert response.headers['X-Gate-Version'] == done['gate_version']
    assert response.headers['X-Snapshot-Hash'] == done['snapshot_hash']
    assert response.headers['X-Export-Version']
    if format == 'docx':
        assert '当前版本的结论。' in '\n'.join(p.text for p in Document(io.BytesIO(response.content)).paragraphs)
    else:
        assert response.content.startswith(b'%PDF')


@pytest.mark.parametrize('kind', ['unversioned','old_body','old_gate','old_run','old_version','new_blocked'])
def test_stale_or_mixed_export_is_rejected(scenario, kind):
    client, store, done = scenario
    payload = {'final_review_snapshot': dict(done['final_review_snapshot'])}
    if kind == 'unversioned':
        payload = {'result': 'old markdown', 'release_quality_gate': {'status':'REPORT_READY'}}
    elif kind == 'old_body':
        payload['result'] = 'old markdown'
    elif kind == 'old_gate':
        payload['release_quality_gate'] = {'status':'REPORT_READY','review_run_id':'old'}
    elif kind == 'old_run':
        payload['final_review_snapshot']['review_run_id'] = 'old'
    elif kind == 'old_version':
        payload['final_review_snapshot']['report_version'] = 'old'
    else:
        run = store.begin(17, done['review_task_id'])
        store.complete(run, {'result':'blocked', 'release_quality_gate':{'status':'BLOCKED'}})
    response = client.post('/review-v2/export-docx',json=payload)
    assert response.status_code == 409
    assert response.json()['detail']['code'] == 'EXPORT_BLOCKED_STALE_REPORT'
