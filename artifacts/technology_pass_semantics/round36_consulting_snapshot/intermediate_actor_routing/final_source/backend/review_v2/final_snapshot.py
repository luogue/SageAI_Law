"""Server-owned immutable review results and latest-run export authorization.

This layer does not decide quality. It binds the engine's completed Gate result
to the exact report it evaluated, and never substitutes an older passing run.
"""
import hashlib
import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path


FIELDS = ('review_task_id', 'review_run_id', 'fact_snapshot_id',
          'rule_result_version', 'report_version', 'gate_version', 'snapshot_hash')
GATE_BINDING_FIELDS = (*FIELDS, 'passed_report_version')


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(value):
    return hashlib.sha256(_json(value).encode()).hexdigest()


def report_digest(value):
    body = json.loads(_json(value))
    gate = body.get('release_quality_gate') or {}
    for key in GATE_BINDING_FIELDS:
        gate.pop(key, None)
    return digest(body)


def now():
    return datetime.now(timezone.utc).isoformat()


class SnapshotError(ValueError):
    def __init__(self, reason, *, expected=None, actual=None):
        self.detail = dict(code='EXPORT_BLOCKED_STALE_REPORT', message=reason,
                           expected=expected or {}, actual=actual or {})
        super().__init__(reason)


class SnapshotStore:
    def __init__(self, path=None):
        self.path = Path(path or os.getenv('REVIEW_V2_SNAPSHOT_DB') or
                         Path(__file__).resolve().parents[1] / 'data/review_snapshots.sqlite3')
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY, owner TEXT NOT NULL, latest_run TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY, task TEXT NOT NULL, created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL, state TEXT NOT NULL, payload TEXT,
                    payload_hash TEXT, binding TEXT);
                CREATE TABLE IF NOT EXISTS exports (
                    id TEXT PRIMARY KEY, run TEXT NOT NULL, report_version TEXT NOT NULL,
                    format TEXT NOT NULL, artifact_hash TEXT NOT NULL, created_at TEXT NOT NULL);
            ''')

    def connect(self):
        db = sqlite3.connect(self.path, timeout=30)
        db.row_factory = sqlite3.Row
        return db

    def begin(self, owner, task_id=None):
        task_id = str(uuid.UUID(task_id)) if task_id else str(uuid.uuid4())
        run_id, stamp = str(uuid.uuid4()), now()
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            task = db.execute('SELECT * FROM tasks WHERE id=?', (task_id,)).fetchone()
            if task and task['owner'] != str(owner):
                raise SnapshotError('当前审查任务不属于此用户。')
            db.execute('INSERT OR REPLACE INTO tasks VALUES (?,?,?)', (task_id, str(owner), run_id))
            db.execute('INSERT INTO runs (id,task,created_at,updated_at,state) VALUES (?,?,?,?,?)',
                       (run_id, task_id, stamp, stamp, 'RUNNING'))
        return dict(review_task_id=task_id, review_run_id=run_id, created_at=stamp)

    def complete(self, run, result):
        # Serialize once: subsequent mutations of caller-owned dictionaries cannot
        # change canonical facts, components, evidence, narratives or Gate in storage.
        copied = json.loads(_json(result))
        report_hash = report_digest(copied)
        gate = copied.get('release_quality_gate') or {}
        facts = {k: copied.get(k) for k in ('contract_facts', 'structured_facts',
                 'structured_fact_debug', 'fact_registry', 'fact_migration')}
        binding = {**run, 'updated_at': now(), 'snapshot_hash': report_hash,
                   'fact_snapshot_id': digest(facts),
                   'rule_result_version': digest(copied.get('items', [])),
                   'report_version': str(uuid.uuid4()), 'gate_version': str(uuid.uuid4()),
                   'export_version': None, 'gate_status': gate.get('status', 'BLOCKED')}
        binding['gate_binding'] = {k: binding[k] for k in FIELDS}
        binding['gate_binding']['passed_report_version'] = (
            binding['report_version'] if binding['gate_status'] == 'REPORT_READY' else None)
        copied['release_quality_gate'].update(binding['gate_binding'])
        payload = _json(copied)
        with self.connect() as db:
            changed = db.execute('UPDATE runs SET updated_at=?,state=?,payload=?,payload_hash=?,binding=? '
                'WHERE id=? AND state=?', (binding['updated_at'], binding['gate_status'], payload,
                 report_hash, _json(binding), run['review_run_id'], 'RUNNING')).rowcount
            if changed != 1:
                raise SnapshotError('最终审查快照已经封存或不存在，禁止覆盖。')
        return {**copied, **{k: binding[k] for k in (*FIELDS, 'created_at', 'updated_at', 'export_version')},
                'final_review_snapshot': binding}

    def _resolve(self, db, owner, supplied):
        task = db.execute('SELECT * FROM tasks WHERE id=? AND owner=?',
                          (supplied.get('review_task_id'), str(owner))).fetchone()
        if not task:
            raise SnapshotError('缺少有效的服务端审查快照，请重新审查。', actual=supplied)
        row = db.execute('SELECT * FROM runs WHERE id=?', (task['latest_run'],)).fetchone()
        expected = json.loads(row['binding']) if row['binding'] else dict(
            review_run_id=row['id'], gate_status=row['state'])
        if any(supplied.get(k) != expected.get(k) for k in FIELDS) or not row['payload']:
            raise SnapshotError('导出版本不是当前任务的最新最终报告。', expected=expected, actual=supplied)
        result = json.loads(row['payload'])
        gate_binding = expected['gate_binding']
        if (report_digest(result) != expected['snapshot_hash'] or
                any(gate_binding[k] != expected[k] for k in FIELDS)):
            raise SnapshotError('报告内容与 Gate 绑定的快照不一致。', expected=expected, actual=supplied)
        gate = result.get('release_quality_gate') or {}
        if any(gate.get(k) != gate_binding.get(k) for k in GATE_BINDING_FIELDS):
            raise SnapshotError('Gate 与报告版本不一致。', expected=expected, actual=supplied)
        if (row['state'] != 'REPORT_READY' or gate.get('status') != 'REPORT_READY' or
                gate.get('failures') or gate.get('blocking_rules') or
                gate_binding.get('passed_report_version') != expected['report_version']):
            raise SnapshotError('最新审查未通过质量门，禁止导出或回退旧报告。', expected=expected, actual=supplied)
        return result, expected

    def resolve_export(self, owner, supplied):
        with self.connect() as db:
            return self._resolve(db, owner, supplied)

    def record_export(self, owner, supplied, format, content):
        # Recheck after rendering: a review started while bytes were generated
        # must invalidate this export too. This transaction is its commit point.
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            _, binding = self._resolve(db, owner, supplied)
            export_id, stamp = str(uuid.uuid4()), now()
            artifact_hash = hashlib.sha256(content).hexdigest()
            db.execute('INSERT INTO exports VALUES (?,?,?,?,?,?)', (export_id,
                binding['review_run_id'], binding['report_version'], format, artifact_hash, stamp))
        return {**binding, 'export_version': export_id, 'export_created_at': stamp,
                'export_artifact_hash': artifact_hash}
