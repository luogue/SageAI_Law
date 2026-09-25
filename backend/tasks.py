"""任务队列管理模块 - 内存缓存 + SQLite 持久化"""
import uuid
import asyncio
import logging
import contextvars
import json
import threading
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)

# 全局trace_id上下文变量
task_trace_id_context = contextvars.ContextVar('task_trace_id', default='unknown')

class TaskStatus(Enum):
    PENDING = "pending"
    UPLOADING = "uploading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    task_id: str
    filename: str
    file_size: int
    status: TaskStatus
    user_id: Optional[int] = None  # 添加用户ID字段
    remaining_bonus: Optional[int] = None  # 剩余额度（用于实时更新）
    record_id: Optional[int] = None  # 报告记录ID
    progress: int = 0
    result: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[Dict] = None
    validation: Optional[Dict] = None
    summary: Optional[Dict] = None
    trace_id: Optional[str] = None  # 链路追踪ID

# 内存缓存（快速查找）+ SQLite 持久化（容器重启恢复）
_tasks: Dict[str, Task] = {}
_task_lock = threading.RLock()
concurrent_semaphore = asyncio.Semaphore(3)  # 并发控制，同时处理不超过3个任务

# 进度同步阈值：每隔多少个百分点同步一次到 DB（避免过于频繁的 DB 写入）
_DB_SYNC_PROGRESS_STEP = 5

# SSE 事件通知：每个任务一个 asyncio.Event，update_task 时 set，SSE 端点 await
_task_events: Dict[str, asyncio.Event] = {}

def _get_db():
    """Compatibility helper: never share the returned session between threads."""
    from storage.database import SessionLocal
    return SessionLocal()

def _task_to_db(task: Task):
    """Persist before publishing success; every call owns its transaction/session."""
    from storage.database import session_scope
    from storage.models import TaskRecord
    with session_scope() as db:
        record = db.query(TaskRecord).filter(TaskRecord.task_id == task.task_id).first()
        if record is None:
            record = TaskRecord(task_id=task.task_id)
            db.add(record)
        for field in ('filename', 'file_size', 'user_id', 'remaining_bonus', 'record_id',
                      'progress', 'result', 'error', 'trace_id'):
            setattr(record, field, getattr(task, field))
        record.status = task.status.value if isinstance(task.status, TaskStatus) else str(task.status)
        for field in ('metadata', 'validation', 'summary'):
            value = getattr(task, field)
            setattr(record, field + '_json', json.dumps(value, ensure_ascii=False) if value is not None else None)
        db.commit()

def _db_record_to_task(record) -> Task:
    """将数据库记录转换为 Task 内存对象"""
    def _parse_json(val):
        if val is None:
            return None
        try:
            return json.loads(val)
        except (json.JSONDecodeError, TypeError):
            return None

    return Task(
        task_id=record.task_id,
        filename=record.filename,
        file_size=record.file_size or 0,
        status=TaskStatus(record.status) if record.status else TaskStatus.PENDING,
        user_id=record.user_id,
        remaining_bonus=record.remaining_bonus,
        record_id=record.record_id,
        progress=record.progress or 0,
        result=record.result,
        error=record.error,
        metadata=_parse_json(record.metadata_json),
        validation=_parse_json(record.validation_json),
        summary=_parse_json(record.summary_json),
        trace_id=record.trace_id,
    )

def _restore_tasks_from_db():
    """容器启动时从 SQLite 恢复未完成的任务到内存"""
    try:
        from storage.models import TaskRecord
        db = _get_db()
        try:
            # 恢复所有非终态任务（pending/uploading/processing）
            records = db.query(TaskRecord).filter(
                TaskRecord.status.in_(["pending", "uploading", "processing"])
            ).all()
            count = 0
            for record in records:
                task = _db_record_to_task(record)
                _tasks[task.task_id] = task
                count += 1
            logger.info(f"[TaskDB] 容器启动，从数据库恢复了 {count} 个未完成任务到内存")
        finally:
            db.close()
    except Exception as e:
        logger.warning(f"[TaskDB] 启动恢复任务时出错: {e}")

def init_task_storage():
    """初始化任务存储：从数据库恢复未完成任务（需在 init_db() 之后调用）"""
    _restore_tasks_from_db()

def create_task(filename: str, file_size: int, user_id: Optional[int] = None) -> Task:
    """创建新任务（内存 + DB 双写）"""
    task_id = str(uuid.uuid4())
    # 获取当前请求的trace_id
    try:
        from security.logging_utils import trace_id_context
        current_trace_id = trace_id_context.get()
    except:
        current_trace_id = 'unknown'
    
    task = Task(
        task_id=task_id,
        filename=filename,
        file_size=file_size,
        user_id=user_id,
        status=TaskStatus.PENDING,
        progress=0,
        trace_id=current_trace_id
    )
    _task_to_db(task)
    with _task_lock:
        _tasks[task_id] = task
        _task_events[task_id] = asyncio.Event()
    return task

def get_task(task_id: str) -> Optional[Task]:
    """Read persisted state so other workers cannot leave a stale terminal status."""
    from storage.database import session_scope
    from storage.models import TaskRecord
    with session_scope() as db:
        record = db.query(TaskRecord).filter(TaskRecord.task_id == task_id).first()
        if record is None:
            return None
        persisted = _db_record_to_task(record)
    with _task_lock:
        cached = _tasks.get(task_id)
        if cached and cached.status == persisted.status and cached.progress > persisted.progress:
            return cached
        _tasks[task_id] = persisted
        _task_events.setdefault(task_id, asyncio.Event())
    return persisted

def update_task(task_id: str, **kwargs):
    """Use a new Task value and publish it only after required writes succeed."""
    from dataclasses import replace
    with _task_lock:
        task = get_task(task_id)
        if task is None:
            return
        candidate = replace(task, **{k: v for k, v in kwargs.items() if hasattr(task, k)})
        should_sync = (candidate.status != task.status or
                       candidate.progress // _DB_SYNC_PROGRESS_STEP != task.progress // _DB_SYNC_PROGRESS_STEP or
                       any(k != 'progress' and getattr(candidate, k) != getattr(task, k)
                           for k in kwargs if hasattr(task, k)))
        if should_sync:
            _task_to_db(candidate)
        _tasks[task_id] = candidate
        event = _task_events.get(task_id)
        if event and not event.is_set():
            event.set()
            _task_events[task_id] = asyncio.Event()

def delete_task(task_id: str):
    from storage.database import session_scope
    from storage.models import TaskRecord
    with _task_lock, session_scope() as db:
        record = db.query(TaskRecord).filter(TaskRecord.task_id == task_id).first()
        if record:
            db.delete(record)
            db.commit()
        _tasks.pop(task_id, None)
        _task_events.pop(task_id, None)

def get_all_tasks(user_id: Optional[int] = None) -> List[Task]:
    """History comes from persistence, including after restart, scoped by caller."""
    from storage.database import session_scope
    from storage.models import TaskRecord
    with session_scope() as db:
        query = db.query(TaskRecord)
        if user_id is not None:
            query = query.filter(TaskRecord.user_id == user_id)
        return [_db_record_to_task(record) for record in query.order_by(TaskRecord.id.desc()).all()]

async def run_with_concurrent_limit(coroutine):
    """带并发限制的任务执行"""
    async with concurrent_semaphore:
        try:
            return await coroutine
        except Exception as e:
            logger.error(f"任务执行失败: {e}")
            raise


async def wait_for_task_update(task_id: str, timeout: float = 30.0) -> bool:
    """等待任务状态变更（用于 SSE 端点）
    
    Args:
        task_id: 任务ID
        timeout: 最大等待秒数（超时后返回 False）
    
    Returns:
        True 如果事件被触发，False 如果超时
    """
    event = _task_events.get(task_id)
    if not event:
        return False
    try:
        await asyncio.wait_for(event.wait(), timeout=timeout)
        return True
    except asyncio.TimeoutError:
        return False
