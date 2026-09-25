"""Database safety regressions. Every database is temporary or an evidence copy."""
import os
import sqlite3
import subprocess
import sys
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from storage.database import engine, session_scope, validate_database_environment
from storage.crud import create_user, get_user_by_id, init_db
from storage.models import User
from sqlite_maintenance import snapshot, stage


@pytest.fixture
def account():
    init_db()
    return create_user('test-' + uuid.uuid4().hex, 'test-hash')


def test_pytest_environment_is_temporary():
    assert Path(engine.url.database).is_relative_to(Path(os.environ['SAGE_TEST_ROOT']))
    validate_database_environment(str(engine.url))
    with pytest.raises(RuntimeError):
        validate_database_environment('sqlite:///' + str(Path('backend/app.db').resolve()))


def test_subprocess_test_import_refuses_business_path():
    env = dict(os.environ, DATABASE_URL='sqlite:///./app.db', PYTHONPATH=str(Path(__file__).resolve().parents[1]))
    result = subprocess.run([sys.executable, '-c', 'import storage.database'], env=env, capture_output=True)
    assert result.returncode != 0
    assert b'outside SAGE_TEST_ROOT' in result.stderr


def test_session_rollback_and_detached_result(account):
    with pytest.raises(RuntimeError):
        with session_scope() as db:
            user = db.get(User, account.id)
            user.bonus_credits = 12345
            db.flush()
            raise RuntimeError('injected transaction failure')
    assert get_user_by_id(account.id).bonus_credits == 0
    with pytest.raises(IntegrityError):
        create_user(account.mobile, 'duplicate')
    assert get_user_by_id(account.id).mobile == account.mobile
    assert engine.pool.checkedout() == 0 if hasattr(engine.pool, 'checkedout') else True


def test_early_return_rolls_back(account):
    with session_scope() as db:
        db.get(User, account.id).bonus_credits = 999
        db.flush()
    assert get_user_by_id(account.id).bonus_credits == 0


def test_threads_use_independent_sessions_and_durable_tasks(account):
    from tasks import create_task, update_task, get_task, _tasks, TaskStatus, get_all_tasks
    def worker(number):
        task = create_task(f'thread-{number}.txt', 10, account.id)
        update_task(task.task_id, status=TaskStatus.COMPLETED, progress=100, result='persisted')
        return task.task_id
    with ThreadPoolExecutor(max_workers=4) as pool:
        ids = list(pool.map(worker, range(8)))
    _tasks.clear()
    assert all(get_task(ident).result == 'persisted' for ident in ids)
    assert set(ids) <= {task.task_id for task in get_all_tasks(account.id)}
    assert not get_all_tasks(-100)


def test_persistence_failure_does_not_publish_task(monkeypatch):
    import tasks
    before = dict(tasks._tasks)
    def failed(task):
        raise RuntimeError('write failed')
    monkeypatch.setattr(tasks, '_task_to_db', failed)
    with pytest.raises(RuntimeError):
        tasks.create_task('failed.txt', 1)
    assert tasks._tasks == before


def test_failed_update_keeps_previous_state(account, monkeypatch):
    import tasks
    task = tasks.create_task('update.txt', 1, account.id)
    def failed(value):
        raise RuntimeError('write failed')
    monkeypatch.setattr(tasks, '_task_to_db', failed)
    with pytest.raises(RuntimeError):
        tasks.update_task(task.task_id, status=tasks.TaskStatus.COMPLETED, result='not committed')
    assert tasks.get_task(task.task_id).status == tasks.TaskStatus.PENDING


def test_backup_contains_committed_wal_and_refuses_overwrite(tmp_path):
    source, target = tmp_path/'source.db', tmp_path/'backup.db'
    db = sqlite3.connect(source)
    try:
        db.execute('PRAGMA journal_mode=WAL')
        db.execute('PRAGMA wal_autocheckpoint=0')
        db.execute('CREATE TABLE ledger(id INTEGER PRIMARY KEY, value TEXT)')
        db.execute("INSERT INTO ledger VALUES(1,'committed in WAL')")
        db.commit()
        assert Path(str(source)+'-wal').stat().st_size > 0
        result = snapshot(source, target)
        assert result['tables']['ledger'] == 1
        copy = sqlite3.connect(target)
        assert copy.execute('SELECT value FROM ledger').fetchone()[0] == 'committed in WAL'
        copy.close()
        with pytest.raises(ValueError):
            snapshot(source, target)
        with pytest.raises(ValueError):
            stage(target, source)
    finally:
        db.close()


def test_backup_during_concurrent_transactions(tmp_path):
    source, target = tmp_path/'live.db', tmp_path/'snapshot.db'
    db = sqlite3.connect(source)
    db.executescript('PRAGMA journal_mode=WAL; CREATE TABLE a(id INTEGER PRIMARY KEY); CREATE TABLE b(id INTEGER PRIMARY KEY);')
    db.close()
    started, stop = threading.Event(), threading.Event()
    errors = []
    def writer():
        connection = sqlite3.connect(source)
        try:
            for ident in range(1, 501):
                with connection:
                    connection.execute('INSERT INTO a VALUES(?)', (ident,))
                    connection.execute('INSERT INTO b VALUES(?)', (ident,))
                started.set()
                if stop.is_set():
                    break
        except Exception as error:
            errors.append(str(error))
        finally:
            connection.close()
    thread = threading.Thread(target=writer)
    thread.start()
    try:
        assert started.wait(5)
        result = snapshot(source, target)
        assert result['tables']['a'] == result['tables']['b'] > 0
    finally:
        stop.set()
        thread.join(5)
    assert not errors


def test_corrupt_backup_not_published_and_health_detects_damage(tmp_path, monkeypatch):
    import storage.health as health
    source = tmp_path/'damaged.db'
    # Synthetic missing-page corruption; never commit private business data as a fixture.
    db = sqlite3.connect(source)
    db.execute('CREATE TABLE task_record(id INTEGER PRIMARY KEY, status TEXT)')
    db.executemany('INSERT INTO task_record VALUES(?,?)', [(i, 'x'*2000) for i in range(20)])
    db.commit()
    root = db.execute("SELECT rootpage FROM sqlite_schema WHERE name='task_record'").fetchone()[0]
    db.close()
    raw = bytearray(source.read_bytes())
    page_size = int.from_bytes(raw[16:18], 'big')
    offset = (root-1)*page_size
    assert raw[offset] == 5
    raw[offset+8:offset+12] = (len(raw)//page_size+100).to_bytes(4, 'big')
    source.write_bytes(raw)
    target = tmp_path/'must-not-exist.db'
    with pytest.raises((sqlite3.DatabaseError, RuntimeError)):
        stage(source, target)
    assert not target.exists()
    isolated = create_engine('sqlite:///' + source.as_posix())
    try:
        monkeypatch.setattr(health, 'engine', isolated)
        assert health.database_health(force=True)['status'] == 'unhealthy'
    finally:
        isolated.dispose()


def test_health_detects_missing_core_table(tmp_path, monkeypatch):
    import storage.health as health
    isolated = create_engine('sqlite:///' + (tmp_path/'empty.db').as_posix())
    try:
        monkeypatch.setattr(health, 'engine', isolated)
        assert health.database_health(force=True)['status'] == 'unhealthy'
    finally:
        isolated.dispose()


def test_no_generator_session_consumption_remains():
    backend = Path(__file__).resolve().parents[1]
    for relative in ('storage/crud.py', 'routers/admin.py', 'security/output_guard.py', 'security/security_events.py'):
        assert 'next(get_db())' not in (backend/relative).read_text(encoding='utf-8')


def test_raw_sqlite_exception_rolls_back_and_closes(tmp_path):
    from storage.paths import sqlite_connection
    path = tmp_path/'auxiliary.db'
    with sqlite_connection(path) as db:
        db.execute('CREATE TABLE example(id INTEGER)')
        db.commit()
    with pytest.raises(RuntimeError):
        with sqlite_connection(path) as db:
            db.execute('INSERT INTO example VALUES(1)')
            raise RuntimeError('abort')
    with pytest.raises(sqlite3.ProgrammingError):
        db.execute('SELECT 1')
    with sqlite_connection(path) as check:
        assert check.execute('SELECT count(*) FROM example').fetchone()[0] == 0


def test_http_health_and_persistence_errors_return_503(tmp_path, monkeypatch):
    import main
    import storage.health as health
    from fastapi.testclient import TestClient
    from sqlalchemy.exc import OperationalError
    isolated = create_engine('sqlite:///' + (tmp_path/'missing-tables.db').as_posix())
    try:
        monkeypatch.setattr(health, 'engine', isolated)
        health.database_health(force=True)
        client = TestClient(main.app)
        for path in ('/health', '/api/health'):
            response = client.get(path)
            assert response.status_code == 503
            assert response.json()['status'] == 'unhealthy'
        def broken(task_id):
            raise OperationalError('SELECT', {}, Exception('database corrupt'))
        monkeypatch.setattr(main, 'get_task', broken)
        assert client.get('/api/task/test-database-error').status_code == 503
        client.close()
    finally:
        isolated.dispose()
