"""任务队列管理模块 - 内存缓存 + SQLite 持久化"""
import uuid
import asyncio
import logging
import contextvars
import json
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
concurrent_semaphore = asyncio.Semaphore(3)  # 并发控制，同时处理不超过3个任务

# 进度同步阈值：每隔多少个百分点同步一次到 DB（避免过于频繁的 DB 写入）
_DB_SYNC_PROGRESS_STEP = 5

# SSE 事件通知：每个任务一个 asyncio.Event，update_task 时 set，SSE 端点 await
_task_events: Dict[str, asyncio.Event] = {}

def _get_db():
    """获取数据库会话（独立管理生命周期）"""
    from storage.database import SessionLocal
    db = SessionLocal()
    return db

def _task_to_db(task: Task, db=None):
    """将 Task 写入/更新到数据库"""
    from storage.models import TaskRecord
    should_close = db is None
    if db is None:
        db = _get_db()
    try:
        record = db.query(TaskRecord).filter(TaskRecord.task_id == task.task_id).first()
        if record is None:
            record = TaskRecord(task_id=task.task_id)
            db.add(record)
        record.filename = task.filename
        record.file_size = task.file_size
        record.status = task.status.value if isinstance(task.status, TaskStatus) else str(task.status)
        record.user_id = task.user_id
        record.remaining_bonus = task.remaining_bonus
        record.record_id = task.record_id
        record.progress = task.progress
        record.result = task.result
        record.error = task.error
        record.metadata_json = json.dumps(task.metadata, ensure_ascii=False) if task.metadata else None
        record.validation_json = json.dumps(task.validation, ensure_ascii=False) if task.validation else None
        record.summary_json = json.dumps(task.summary, ensure_ascii=False) if task.summary else None
        record.trace_id = task.trace_id
        db.commit()
    except Exception as e:
        logger.warning(f"[TaskDB] 任务 {task.task_id} 写入 DB 失败: {e}")
        if should_close:
            try:
                db.rollback()
            except:
                pass
    finally:
        if should_close:
            db.close()

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
        logger.warning(f"[TaskDB] 启动恢复任务时出错（可能表尚未创建）: {e}")

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
    _tasks[task_id] = task
    _task_events[task_id] = asyncio.Event()  # SSE 通知事件
    # 异步持久化到 DB（不阻塞创建流程）
    try:
        _task_to_db(task)
    except Exception as e:
        logger.warning(f"[TaskDB] 新建任务 {task_id} 持久化失败: {e}")
    return task

def get_task(task_id: str) -> Optional[Task]:
    """获取任务（内存优先，DB 兜底）"""
    task = _tasks.get(task_id)
    if task is not None:
        return task
    # 内存未命中 → 尝试从 DB 恢复（容器重启后场景）
    try:
        from storage.models import TaskRecord
        db = _get_db()
        try:
            record = db.query(TaskRecord).filter(TaskRecord.task_id == task_id).first()
            if record:
                task = _db_record_to_task(record)
                _tasks[task_id] = task  # 恢复到内存缓存
                # 初始化 SSE 通知事件（如果尚未存在）
                if task_id not in _task_events:
                    _task_events[task_id] = asyncio.Event()
                logger.info(f"[TaskDB] 从数据库恢复了任务 {task_id}（状态：{task.status.value}）")
                return task
        finally:
            db.close()
    except Exception as e:
        logger.warning(f"[TaskDB] 查询任务 {task_id} 失败：{e}")
    return None

def update_task(task_id: str, **kwargs):
    """更新任务状态（内存立即更新 + DB 选择性同步）"""
    task = _tasks.get(task_id)
    if not task:
        return

    old_status = task.status
    old_progress = task.progress

    for key, value in kwargs.items():
        if hasattr(task, key):
            setattr(task, key, value)

    # 判断是否需要同步到 DB
    new_status = task.status
    new_progress = task.progress

    # 满足以下任一条件时同步 DB：
    # 1. 状态变化（如 PENDING → PROCESSING → COMPLETED/FAILED）
    # 2. 进度跨越了阈值
    should_sync = (new_status != old_status) or \
                  (new_progress // _DB_SYNC_PROGRESS_STEP != old_progress // _DB_SYNC_PROGRESS_STEP)

    if should_sync:
        try:
            _task_to_db(task)
        except Exception as e:
            logger.warning(f"[TaskDB] 更新任务 {task_id} 到 DB 失败: {e}")

    # 通知 SSE 等待者：状态有变化
    event = _task_events.get(task_id)
    if event and not event.is_set():
        event.set()
        _task_events[task_id] = asyncio.Event()  # 替换为新 Event 供下次等待

def delete_task(task_id: str):
    """删除任务（内存 + DB 双删 + 清理事件）"""
    if task_id in _tasks:
        del _tasks[task_id]
    _task_events.pop(task_id, None)  # 清理 SSE 事件
    try:
        from storage.models import TaskRecord
        db = _get_db()
        try:
            record = db.query(TaskRecord).filter(TaskRecord.task_id == task_id).first()
            if record:
                db.delete(record)
                db.commit()
        finally:
            db.close()
    except Exception as e:
        logger.warning(f"[TaskDB] 删除任务 {task_id} 失败: {e}")

def get_all_tasks() -> List[Task]:
    """获取所有任务"""
    return list(_tasks.values())

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