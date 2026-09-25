"""Loopback-only acceptance harness around the real application and persistence APIs.

Probe endpoints exist ONLY in this artifact, guarded by a random per-run secret.
No application behavior or LLM implementation is mocked.
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'backend'))
if os.environ.get('ENV') != 'test' or not os.environ.get('SAGE_TEST_ROOT'):
    raise RuntimeError('Only isolated test environments are permitted')
from storage.database import engine, session_scope
from storage.models import User
from storage.crud import create_user, create_record, get_user_by_id
from auth.utils import hash_password, create_access_token
from tasks import create_task, update_task, TaskStatus
from fastapi import Header, HTTPException, Body
import main
import uvicorn

def authorize(secret):
    if secret != os.environ['PROBE_SECRET']:
        raise HTTPException(403)


@main.app.post('/__probe/seed')
def seed(x_probe_secret: str = Header()):
    authorize(x_probe_secret)
    user = create_user('19900000001', hash_password('Isolated-acceptance-2026!'))
    with session_scope() as db:
        db.get(User, user.id).status = 'normal'
        db.commit()
    return {'new_user_id': user.id, 'existing_account_token': create_access_token(data={'user_id': 1})}


@main.app.post('/__probe/task')
def task(payload: dict = Body(), x_probe_secret: str = Header()):
    authorize(x_probe_secret)
    if not payload.get('task_id'):
        value = create_task('isolated-acceptance.txt', 100, payload['user_id'])
        return {'task_id': value.task_id}
    changes = dict(payload['changes'])
    if 'status' in changes:
        changes['status'] = TaskStatus(changes['status'])
    update_task(payload['task_id'], **changes)
    return {'saved': True}


@main.app.post('/__probe/report')
def report(payload: dict = Body(), x_probe_secret: str = Header()):
    authorize(x_probe_secret)
    ident = create_record(payload['user_id'], 'isolated-report.txt', payload['markdown'], {'model_version': 'acceptance'})
    return {'record_id': ident}


@main.app.post('/__probe/rollback')
def rollback(payload: dict = Body(), x_probe_secret: str = Header()):
    authorize(x_probe_secret)
    before = get_user_by_id(payload['user_id']).bonus_credits
    try:
        with session_scope() as db:
            db.get(User, payload['user_id']).bonus_credits = before + 999
            db.flush()
            raise RuntimeError('acceptance transaction abort')
    except RuntimeError:
        pass
    return {'rolled_back': get_user_by_id(payload['user_id']).bonus_credits == before}


@main.app.post('/__probe/shutdown')
def shutdown(x_probe_secret: str = Header()):
    authorize(x_probe_secret)
    server.should_exit = True
    return {'stopping': True}


server = uvicorn.Server(uvicorn.Config(main.app, host='127.0.0.1', port=int(os.environ['PROBE_PORT']), log_level='warning'))
try:
    server.run()
finally:
    engine.dispose()
