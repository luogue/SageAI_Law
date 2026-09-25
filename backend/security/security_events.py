"""安全事件日志模块 - 记录封禁、解封、攻击拦截等安全事件"""
from storage.database import session_scope
import logging
from typing import Optional, List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


def record_security_event(
    event_type: str,
    severity: str = "warning",
    source: str = "system",
    detail: str = "",
    user_id: Optional[int] = None,
    ip: Optional[str] = None,
    meta: Optional[Dict] = None,
):
    """
    记录安全事件到 security_events 表

    Args:
        event_type: 事件类型 (prompt_injection, output_leak, auto_ban, manual_ban, unban, rate_limit 等)
        severity: 严重程度 (info, warning, critical)
        source: 来源 (middleware, injection_detector, output_guard, admin)
        detail: 事件详情
        user_id: 关联用户ID
        ip: 来源IP
        meta: 额外的元数据 (JSON)
    """
    import json

    from storage.models import SecurityEvent

    try:
        with session_scope() as db:
            event = SecurityEvent(
                event_type=event_type,
                severity=severity,
                source=source,
                detail=detail,
                user_id=str(user_id) if user_id else None,
                ip=ip or "unknown",
                meta_json=json.dumps(meta, ensure_ascii=False) if meta else None,
            )
            db.add(event)
            db.commit()
            logger.info(
                f"[SEC_EVENT] type={event_type}, severity={severity}, "
                f"user_id={user_id}, ip={ip}"
            )
    except Exception as e:
        logger.error(f"[SEC_EVENT] 记录安全事件失败: {e}")


def record_admin_log(
    admin_user: str,
    action: str,
    target_type: str,
    target_value: str,
    detail: str = "",
):
    """
    记录管理员操作日志到 admin_logs 表

    Args:
        admin_user: 管理员用户名
        action: 操作类型 (ban, unban, approve, reject 等)
        target_type: 目标类型 (user_id, ip, feedback 等)
        target_value: 目标值
        detail: 操作详情/理由
    """

    from storage.models import AdminLog

    try:
        with session_scope() as db:
            log_entry = AdminLog(
                admin_user=admin_user,
                action=action,
                target_type=target_type,
                target_value=target_value,
                detail=detail,
            )
            db.add(log_entry)
            db.commit()
            logger.info(
                f"[ADMIN_LOG] admin={admin_user}, action={action}, "
                f"target={target_type}:{target_value}"
            )
    except Exception as e:
        logger.error(f"[ADMIN_LOG] 记录管理员操作失败: {e}")
