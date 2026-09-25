import copy
import json
import sqlite3

import pytest

from review_v2.final_snapshot import SnapshotStore, SnapshotError, FIELDS


@pytest.fixture
def store(tmp_path):
    return SnapshotStore(tmp_path / 'snapshots.db')


def report(status='REPORT_READY'):
    return {'result': '# 最终报告\n事实已有直接证据。', 'items': [{'item_id': 'X', 'coverage_status': '通过'}],
            'contract_facts': {'identity': 'current'}, 'release_quality_gate': {
                'status': status, 'failures': [] if status == 'REPORT_READY' else [{'requirement': 'FACT'}],
                'blocking_rules': []}}


def ready(store, owner='a', task=None):
    return store.complete(store.begin(owner, task), report())['final_review_snapshot']


def test_immutable_report_and_restart(store):
    original = report()
    done = store.complete(store.begin('a'), original)
    binding = done['final_review_snapshot']
    original['result'] = 'changed'
    done['items'][0]['coverage_status'] = '缺失'
    stored, _ = SnapshotStore(store.path).resolve_export('a', binding)
    assert stored['result'] == report()['result'] and stored['items'] == report()['items']
    assert stored['release_quality_gate']['review_run_id'] == binding['review_run_id']


@pytest.mark.parametrize('field', FIELDS)
def test_every_binding_field_is_enforced(store, field):
    binding = ready(store)
    bad = {**binding, field: 'previous'}
    with pytest.raises(SnapshotError) as caught:
        store.resolve_export('a', bad)
    assert caught.value.detail['code'] == 'EXPORT_BLOCKED_STALE_REPORT'


@pytest.mark.parametrize('state', ['RUNNING', 'BLOCKED', 'REPORT_READY'])
def test_new_run_invalidates_old_pass_even_if_new_run_fails(store, state):
    old = ready(store)
    run = store.begin('a', old['review_task_id'])
    if state != 'RUNNING':
        store.complete(run, report(state))
    with pytest.raises(SnapshotError):
        store.resolve_export('a', old)


def test_out_of_order_completion_does_not_replace_latest(store):
    older = store.begin('a')
    newer = store.begin('a', older['review_task_id'])
    latest = store.complete(newer, report())['final_review_snapshot']
    late = store.complete(older, report())['final_review_snapshot']
    assert store.resolve_export('a', latest)[1]['review_run_id'] == newer['review_run_id']
    with pytest.raises(SnapshotError):
        store.resolve_export('a', late)


def test_owner_isolation(store):
    binding = ready(store)
    with pytest.raises(SnapshotError):
        store.resolve_export('b', binding)
    with pytest.raises(SnapshotError):
        store.begin('b', binding['review_task_id'])


def test_no_unversioned_export_or_fallback(store):
    ready(store)
    with pytest.raises(SnapshotError):
        store.resolve_export('a', {})


def test_sealed_run_cannot_be_overwritten(store):
    run = store.begin('a')
    store.complete(run, report())
    with pytest.raises(SnapshotError):
        store.complete(run, report('BLOCKED'))


def test_report_tampering_is_detected(store):
    binding = ready(store)
    with store.connect() as db:
        db.execute('UPDATE runs SET payload=? WHERE id=?', (json.dumps(report('BLOCKED')), binding['review_run_id']))
    with pytest.raises(SnapshotError):
        store.resolve_export('a', binding)


@pytest.mark.parametrize('field', ['review_run_id', 'snapshot_hash', 'passed_report_version'])
def test_stored_gate_binding_is_verified(store, field):
    binding = ready(store)
    tampered = copy.deepcopy(binding)
    tampered['gate_binding'][field] = 'old'
    with store.connect() as db:
        db.execute('UPDATE runs SET binding=? WHERE id=?', (json.dumps(tampered), binding['review_run_id']))
    with pytest.raises(SnapshotError):
        store.resolve_export('a', binding)


def test_review_started_during_render_blocks_export_commit(store):
    binding = ready(store)
    store.resolve_export('a', binding)
    store.begin('a', binding['review_task_id'])
    with pytest.raises(SnapshotError):
        store.record_export('a', binding, 'docx', b'old bytes')


def test_export_receipt_binds_exact_version_and_artifact(store):
    import hashlib
    binding = ready(store)
    exported = store.record_export('a', binding, 'docx', b'final bytes')
    assert all(exported[k] == binding[k] for k in FIELDS)
    assert exported['export_version']
    assert exported['export_artifact_hash'] == hashlib.sha256(b'final bytes').hexdigest()
    assert binding['export_version'] is None  # export cannot mutate the sealed review


def test_blocked_report_cannot_export(store):
    binding = store.complete(store.begin('a'), report('BLOCKED'))['final_review_snapshot']
    with pytest.raises(SnapshotError):
        store.resolve_export('a', binding)
