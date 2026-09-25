"""管理员接口路由"""
from storage.database import session_scope
import os
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from fastapi.security import APIKeyHeader
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
import json

from auth.utils import verify_password
from storage.crud import verify_admin_password, get_admin_by_username, create_admin
from auth.utils import hash_password

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])

# 管理员认证
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "admin_secure_token_change_me")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
api_key_header = APIKeyHeader(name="X-Admin-Token", auto_error=False)


async def get_admin_token(token: str = Depends(api_key_header)):
    """验证管理员token"""
    if token != ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未授权的访问"
        )
    return token


# ========== 管理员登录接口 ==========

@router.post("/login", summary="管理员登录")
async def admin_login(request: Request) -> Dict[str, Any]:
    """管理员登录"""
    username = None
    password = None

    try:
        body = await request.json()
        username = body.get('username')
        password = body.get('password')
        logger.info(f"JSON格式: username={username}, password={password}")
    except Exception as e:
        logger.info(f"JSON解析失败: {e}")
        # 尝试表单格式
        form_data = await request.form()
        username = form_data.get('username')
        password = form_data.get('password')
        logger.info(f"表单格式: username={username}, password={password}")

    logger.info(f"最终参数: username={username}, password={password}")

    # 检查数据库中是否有管理员账号
    admin = get_admin_by_username(username)
    logger.info(f"查询管理员: {admin is not None}")
    if admin:
        logger.info(f"管理员用户名: {admin.username}")
        logger.info(f"密码哈希: {admin.password_hash}")
        # 数据库中有管理员，使用数据库验证
        password_valid = verify_password(password, admin.password_hash)
        logger.info(f"密码验证结果: {password_valid}")
        if password_valid:
            return {
                "success": True,
                "token": ADMIN_TOKEN,
                "username": username
            }
    else:
        logger.info("数据库中没有管理员，使用环境变量验证")
        # 数据库中没有管理员，使用环境变量验证（兼容旧版）
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return {
                "success": True,
                "token": ADMIN_TOKEN,
                "username": username
            }

    return {"success": False, "detail": "用户名或密码错误"}


# ========== 反馈审核接口 ==========

@router.get("/feedbacks", summary="获取反馈列表")
async def get_feedbacks(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    feedback_type: Optional[str] = None,
    category: Optional[str] = None,
    sort_by: Optional[str] = None,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """获取反馈列表（分页）"""
    from storage.crud import get_feedbacks, get_feedback_count

    try:
        # 获取反馈列表
        feedbacks = get_feedbacks(
            page=page,
            limit=size,
            category=category,
            status=status,
            sort_by=sort_by
        )

        # 获取总数
        total = get_feedback_count(category=category, status=status)

        # 获取用户手机号用于显示
        from storage.crud import get_user_by_id
        for f in feedbacks:
            user = get_user_by_id(f["user_id"])
            if user:
                # 脱敏手机号
                mobile = user.mobile
                if mobile and len(mobile) >= 7:
                    f["mobile"] = mobile[:3] + "****" + mobile[-4:]
                else:
                    f["mobile"] = "未知"
            else:
                f["mobile"] = "未知"

        return {
            "success": True,
            "data": feedbacks,
            "total": total,
            "page": page,
            "size": size
        }
    except Exception as e:
        logger.error(f"获取反馈列表失败: {e}")
        return {"success": False, "detail": str(e)}


@router.get("/feedbacks/{feedback_id}", summary="获取反馈详情")
async def get_feedback_detail(
    feedback_id: int,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """获取单条反馈详情"""
    from storage.crud import get_feedback_by_id, get_user_by_id

    try:
        feedback = get_feedback_by_id(feedback_id)
        if not feedback:
            return {"success": False, "detail": "反馈不存在"}

        # 获取用户信息
        user = get_user_by_id(feedback.user_id)
        mobile = "未知"
        if user:
            mobile = user.mobile
            if mobile and len(mobile) >= 7:
                mobile = mobile[:3] + "****" + mobile[-4:]

        # 解析分类
        categories = json.loads(feedback.categories) if feedback.categories else []

        # 脱敏合同文本
        contract_text = None
        if feedback.contract_text:
            # 脱敏处理：替换手机号、邮箱等
            text = feedback.contract_text
            # 可以添加更多脱敏规则
            contract_text = text[:500] + "..." if len(text) > 500 else text

        return {
            "success": True,
            "data": {
                "id": feedback.id,
                "user_id": feedback.user_id,
                "mobile": mobile,
                "report_id": feedback.report_id,
                "feedback_type": feedback.feedback_type,
                "categories": categories,
                "comment": feedback.comment,
                "upload_consent": feedback.upload_consent,
                "contract_text": contract_text,
                "quality_score": feedback.quality_score,
                "suggested_bonus": feedback.suggested_bonus,
                "ai_reason": feedback.ai_reason,
                "bonus_awarded": feedback.bonus_awarded,
                "status": feedback.status,
                "reviewed_at": feedback.reviewed_at,
                "reviewed_by": feedback.reviewed_by,
                "reject_reason": feedback.reject_reason,
                "created_at": feedback.created_at
            }
        }
    except Exception as e:
        logger.error(f"获取反馈详情失败: {e}")
        return {"success": False, "detail": str(e)}


@router.post("/feedbacks/{feedback_id}/approve", summary="通过审核")
async def approve_feedback(
    feedback_id: int,
    bonus_credits: int = 3,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """通过审核并发放奖励"""
    from storage.crud import get_feedback_by_id, update_feedback_status, add_user_bonus_credits, create_reward_log

    try:
        feedback = get_feedback_by_id(feedback_id)
        if not feedback:
            return {"success": False, "detail": "反馈不存在"}

        if feedback.status != "pending":
            return {"success": False, "detail": "只能审核待审核状态的反馈"}

        # 发放奖励
        new_bonus = add_user_bonus_credits(feedback.user_id, bonus_credits)

        # 更新反馈状态
        update_feedback_status(
            feedback_id=feedback_id,
            status="approved",
            reviewed_at=datetime.now(),
            bonus_awarded=bonus_credits,
            reviewed_by=ADMIN_USERNAME
        )

        # 创建奖励发放记录
        create_reward_log(
            user_id=feedback.user_id,
            amount=bonus_credits,
            reason="feedback_approve",
            related_feedback_id=feedback_id,
            operator=ADMIN_USERNAME
        )

        logger.info(f"反馈 {feedback_id} 审核通过，发放奖励 {bonus_credits} 次，用户 {feedback.user_id} 剩余额度: {new_bonus}")

        return {
            "success": True,
            "detail": f"审核通过，已发放 {bonus_credits} 次免费审查额度",
            "remaining_bonus": new_bonus
        }
    except Exception as e:
        logger.error(f"审核通过失败: {e}")
        return {"success": False, "detail": str(e)}


@router.post("/feedbacks/{feedback_id}/reject", summary="驳回审核")
async def reject_feedback(
    feedback_id: int,
    reason: Optional[str] = "",
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """驳回审核"""
    from storage.crud import get_feedback_by_id, update_feedback_status

    try:
        feedback = get_feedback_by_id(feedback_id)
        if not feedback:
            return {"success": False, "detail": "反馈不存在"}

        if feedback.status != "pending":
            return {"success": False, "detail": "只能审核待审核状态的反馈"}

        # 更新反馈状态
        update_feedback_status(
            feedback_id=feedback_id,
            status="rejected",
            reviewed_at=datetime.now(),
            reject_reason=reason,
            reviewed_by=ADMIN_USERNAME
        )

        logger.info(f"反馈 {feedback_id} 审核驳回，原因: {reason}")

        return {
            "success": True,
            "detail": "已驳回该反馈"
        }
    except Exception as e:
        logger.error(f"驳回审核失败: {e}")
        return {"success": False, "detail": str(e)}


@router.post("/feedbacks/batch-approve", summary="批量通过审核")
async def batch_approve_feedbacks(
    feedback_ids: List[int],
    bonus_credits: int = 3,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """批量通过审核"""
    from storage.crud import get_feedback_by_id, update_feedback_status, add_user_bonus_credits, create_reward_log

    success_count = 0
    failed_list = []

    try:
        for feedback_id in feedback_ids:
            try:
                feedback = get_feedback_by_id(feedback_id)
                if not feedback:
                    failed_list.append({"id": feedback_id, "reason": "反馈不存在"})
                    continue

                if feedback.status != "pending":
                    failed_list.append({"id": feedback_id, "reason": "非待审核状态"})
                    continue

                # 发放奖励
                add_user_bonus_credits(feedback.user_id, bonus_credits)

                # 更新反馈状态
                update_feedback_status(
                    feedback_id=feedback_id,
                    status="approved",
                    reviewed_at=datetime.now(),
                    bonus_awarded=bonus_credits,
                    reviewed_by=ADMIN_USERNAME
                )

                # 创建奖励发放记录
                create_reward_log(
                    user_id=feedback.user_id,
                    amount=bonus_credits,
                    reason="feedback_approve",
                    related_feedback_id=feedback_id,
                    operator=ADMIN_USERNAME
                )

                success_count += 1
            except Exception as e:
                failed_list.append({"id": feedback_id, "reason": str(e)})

        logger.info(f"批量审核完成: 成功 {success_count} 条，失败 {len(failed_list)} 条")

        return {
            "success": True,
            "success_count": success_count,
            "failed_count": len(failed_list),
            "failed_list": failed_list,
            "detail": f"批量审核完成：成功 {success_count} 条，失败 {len(failed_list)} 条"
        }
    except Exception as e:
        logger.error(f"批量审核失败: {e}")
        return {"success": False, "detail": str(e)}


# ========== 数据统计接口 ==========

@router.get("/stats/overview", summary="获取统计概览")
async def get_stats_overview(token: str = Depends(get_admin_token)) -> Dict[str, Any]:
    """获取统计概览数据"""
    from storage.crud import get_feedback_count

    try:
        with session_scope() as db:

            # 总用户数
            total_users = db.query(__import__('storage.models', fromlist=['User']).User).count()

            # 今日新增用户
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_users = db.query(__import__('storage.models', fromlist=['User']).User).filter(
                __import__('storage.models', fromlist=['User']).User.created_at >= today_start
            ).count()

            # 总反馈数
            total_feedbacks = get_feedback_count()

            # 待审核反馈数
            pending_feedbacks = get_feedback_count(status="pending")

            # 已发放奖励总额度
            total_bonus_awarded = db.query(__import__('storage.models', fromlist=['BonusLog']).BonusLog).with_entities(
                __import__('storage.models', fromlist=['BonusLog']).BonusLog.awarded_amount
            ).all()
            total_bonus = sum([row[0] for row in total_bonus_awarded])

            return {
                "success": True,
                "data": {
                    "total_users": total_users,
                    "today_users": today_users,
                    "total_feedbacks": total_feedbacks,
                    "pending_feedbacks": pending_feedbacks,
                    "total_bonus_awarded": total_bonus
                }
            }
    except Exception as e:
        logger.error(f"获取统计概览失败: {e}")
        return {"success": False, "detail": str(e)}


@router.get("/stats/trend", summary="获取趋势数据")
async def get_stats_trend(
    days: int = 7,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """获取近N天的趋势数据"""
    try:
        with session_scope() as db:
            Feedback = __import__('storage.models', fromlist=['Feedback']).Feedback

            result = []
            for i in range(days):
                date = (datetime.now() - timedelta(days=i)).date()
                start_time = datetime.combine(date, datetime.min.time())
                end_time = datetime.combine(date, datetime.max.time())

                count = db.query(Feedback).filter(
                    Feedback.created_at >= start_time,
                    Feedback.created_at <= end_time
                ).count()

                result.append({
                    "date": date.isoformat(),
                    "count": count
                })

            # 按日期升序排列
            result.reverse()

            return {
                "success": True,
                "data": result,
                "days": days
            }
    except Exception as e:
        logger.error(f"获取趋势数据失败: {e}")
        return {"success": False, "detail": str(e)}


@router.get("/stats/categories", summary="获取反馈分类统计")
async def get_category_stats(token: str = Depends(get_admin_token)) -> Dict[str, Any]:
    """获取反馈分类占比统计"""
    try:
        with session_scope() as db:
            Feedback = __import__('storage.models', fromlist=['Feedback']).Feedback

            feedbacks = db.query(Feedback).all()

            category_counts = {}
            for f in feedbacks:
                if f.categories:
                    try:
                        categories = json.loads(f.categories)
                        for cat in categories:
                            category_counts[cat] = category_counts.get(cat, 0) + 1
                    except:
                        pass

            total = sum(category_counts.values())

            result = [{
                "category": cat,
                "count": count,
                "percentage": round(count / total * 100, 2) if total > 0 else 0
            } for cat, count in category_counts.items()]

            # 按数量降序排列
            result.sort(key=lambda x: x["count"], reverse=True)

            return {
                "success": True,
                "data": result,
                "total": total
            }
    except Exception as e:
        logger.error(f"获取分类统计失败: {e}")
        return {"success": False, "detail": str(e)}


# ========== 黑名单管理接口 ==========

@router.get("/blacklist", summary="获取所有黑名单记录")
async def get_blacklist(token: str = Depends(get_admin_token)) -> Dict[str, Any]:
    """获取所有黑名单记录（含封禁类型、解封状态）"""
    from security.blacklist import blacklist_manager

    try:
        records = blacklist_manager.get_all()
        return {
            "success": True,
            "data": records,
            "count": len(records)
        }
    except Exception as e:
        logger.error(f"获取黑名单失败: {e}")
        return {"success": False, "detail": str(e)}


@router.post("/blacklist/unban", summary="解封黑名单记录")
async def unban_from_blacklist(
    type: str,
    value: str,
    unban_reason: str = "",
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """解封黑名单记录（标记为已解封，需填写解封理由）"""
    from security.blacklist import unban as do_unban
    from security.security_events import record_admin_log

    if type not in ["ip", "user_id"]:
        return {"success": False, "detail": "无效的类型，必须是 'ip' 或 'user_id'"}

    if not unban_reason.strip():
        return {"success": False, "detail": "解封必须填写理由"}

    try:
        success = do_unban(type, value, ADMIN_USERNAME, unban_reason)
        if success:
            # 记录审计日志
            record_admin_log(
                admin_user=ADMIN_USERNAME,
                action="unban",
                target_type=type,
                target_value=value,
                detail=unban_reason
            )
            return {"success": True, "detail": f"已解封 {type}: {value}"}
        else:
            return {"success": False, "detail": "未找到该记录或解封失败"}
    except Exception as e:
        logger.error(f"解封失败: {e}")
        return {"success": False, "detail": str(e)}


@router.delete("/blacklist", summary="移除黑名单记录")
async def remove_from_blacklist(
    type: str,
    value: str,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """移除黑名单记录（物理删除）"""
    from security.blacklist import blacklist_manager
    from security.security_events import record_admin_log

    if type not in ["ip", "user_id"]:
        return {"success": False, "detail": "无效的类型，必须是 'ip' 或 'user_id'"}

    try:
        success = blacklist_manager.remove(type, value)
        if success:
            record_admin_log(
                admin_user=ADMIN_USERNAME,
                action="delete_ban",
                target_type=type,
                target_value=value,
                detail="物理删除黑名单记录"
            )
            return {"success": True, "detail": f"已从黑名单移除 {type}: {value}"}
        else:
            return {"success": False, "detail": "未找到该记录"}
    except Exception as e:
        logger.error(f"移除黑名单失败: {e}")
        return {"success": False, "detail": str(e)}


@router.post("/blacklist", summary="添加黑名单记录")
async def add_to_blacklist(
    type: str,
    value: str,
    reason: str = "",
    expires_at: Optional[str] = None,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """添加黑名单记录"""
    from security.blacklist import blacklist_manager
    from security.security_events import record_admin_log

    if type not in ["ip", "user_id"]:
        return {"success": False, "detail": "无效的类型，必须是 'ip' 或 'user_id'"}

    # 解析过期时间
    expires_datetime = None
    if expires_at:
        try:
            expires_datetime = datetime.fromisoformat(expires_at)
        except:
            return {"success": False, "detail": "无效的过期时间格式，应为 ISO 格式（如 2024-01-01T12:00:00）"}

    try:
        success = blacklist_manager.add(type, value, reason, expires_datetime, ban_type="manual")
        if success:
            record_admin_log(
                admin_user=ADMIN_USERNAME,
                action="ban",
                target_type=type,
                target_value=value,
                detail=reason or "管理员手动封禁"
            )
            return {"success": True, "detail": f"已添加到黑名单: {type}={value}"}
        else:
            return {"success": False, "detail": "该记录已存在"}
    except Exception as e:
        logger.error(f"添加黑名单失败: {e}")
        return {"success": False, "detail": str(e)}


# ========== 安全事件接口 ==========

@router.get("/security-events", summary="获取安全事件列表")
async def get_security_events(
    event_type: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    page: int = Query(1, ge=1),
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """获取安全事件列表"""
    try:

        from storage.models import SecurityEvent
        from sqlalchemy import desc

        with session_scope() as db:
            query = db.query(SecurityEvent)

            if event_type:
                query = query.filter(SecurityEvent.event_type == event_type)
            if severity:
                query = query.filter(SecurityEvent.severity == severity)

            total = query.count()
            events = query.order_by(desc(SecurityEvent.created_at)) \
                          .offset((page - 1) * limit) \
                          .limit(limit) \
                          .all()

            return {
                "success": True,
                "data": [
                    {
                        "id": e.id,
                        "event_type": e.event_type,
                        "severity": e.severity,
                        "source": e.source,
                        "detail": e.detail,
                        "user_id": e.user_id,
                        "ip": e.ip,
                        "meta_json": e.meta_json,
                        "created_at": e.created_at.isoformat() if e.created_at else None
                    }
                    for e in events
                ],
                "total": total,
                "page": page,
                "limit": limit
            }
    except Exception as e:
        logger.error(f"获取安全事件失败: {e}")
        return {"success": False, "detail": str(e)}


@router.get("/security-events/stats", summary="获取安全事件统计")
async def get_security_event_stats(
    days: int = 7,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """获取按事件类型统计的安全事件数据"""
    try:

        from storage.models import SecurityEvent
        from sqlalchemy import func

        with session_scope() as db:
            cutoff = datetime.now() - timedelta(days=days)

            stats = db.query(
                SecurityEvent.event_type,
                func.count(SecurityEvent.id).label('count')
            ).filter(
                SecurityEvent.created_at >= cutoff
            ).group_by(
                SecurityEvent.event_type
            ).all()

            return {
                "success": True,
                "data": [
                    {"event_type": s[0], "count": s[1]}
                    for s in stats
                ],
                "days": days
            }
    except Exception as e:
        logger.error(f"获取安全事件统计失败: {e}")
        return {"success": False, "detail": str(e)}


# ========== 管理员操作日志接口 ==========

@router.get("/admin-logs", summary="获取管理员操作日志")
async def get_admin_logs(
    action: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    page: int = Query(1, ge=1),
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """获取管理员操作审计日志"""
    try:

        from storage.models import AdminLog
        from sqlalchemy import desc

        with session_scope() as db:
            query = db.query(AdminLog)

            if action:
                query = query.filter(AdminLog.action == action)

            total = query.count()
            logs = query.order_by(desc(AdminLog.created_at)) \
                        .offset((page - 1) * limit) \
                        .limit(limit) \
                        .all()

            return {
                "success": True,
                "data": [
                    {
                        "id": l.id,
                        "admin_user": l.admin_user,
                        "action": l.action,
                        "target_type": l.target_type,
                        "target_value": l.target_value,
                        "detail": l.detail,
                        "created_at": l.created_at.isoformat() if l.created_at else None
                    }
                    for l in logs
                ],
                "total": total,
                "page": page,
                "limit": limit
            }
    except Exception as e:
        logger.error(f"获取管理员日志失败: {e}")
        return {"success": False, "detail": str(e)}


@router.get("/blacklist/auto-ban-stats", summary="获取自动封禁统计数据")
async def get_auto_ban_stats(
    hours: int = 24,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """获取自动封禁统计数据"""
    from security.blacklist import get_blacklist_stats

    try:
        stats = get_blacklist_stats(hours)
        return {
            "success": True,
            "data": stats,
            "query_hours": hours,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"获取自动封禁统计失败: {e}")
        return {"success": False, "detail": str(e)}


# ========== 拦截日志接口 ==========

@router.get("/intercept-logs", summary="获取拦截日志")
async def get_intercept_logs(
    trigger_word: Optional[str] = None,
    limit: int = 20,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """获取最近的拦截日志"""
    from security.sensitive_filter import get_recent_intercept_logs

    try:
        logs = get_recent_intercept_logs(trigger_word, limit)
        return {
            "success": True,
            "data": logs,
            "count": len(logs)
        }
    except Exception as e:
        logger.error(f"获取拦截日志失败: {e}")
        return {"success": False, "detail": str(e)}


@router.get("/intercept-logs/frequent-triggers", summary="获取高频触发词统计")
async def get_frequent_triggers(
    days: int = 7,
    limit: int = 50,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """获取高频触发词统计"""
    from security.sensitive_filter import get_frequent_triggers

    try:
        triggers = get_frequent_triggers(days, limit)
        return {
            "success": True,
            "data": triggers,
            "days": days,
            "count": len(triggers)
        }
    except Exception as e:
        logger.error(f"获取高频触发词失败: {e}")
        return {"success": False, "detail": str(e)}


# ========== 白名单管理接口 ==========

@router.get("/whitelist", summary="获取白名单")
async def get_whitelist(token: str = Depends(get_admin_token)) -> Dict[str, Any]:
    """获取当前白名单列表"""
    from security.sensitive_filter import WHITELIST

    return {
        "success": True,
        "data": sorted(list(WHITELIST)),
        "count": len(WHITELIST)
    }


@router.post("/whitelist", summary="添加白名单词")
async def add_whitelist_word(
    word: str,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """添加词到白名单"""
    from security.sensitive_filter import add_to_whitelist

    try:
        success = add_to_whitelist(word)
        if success:
            return {"success": True, "detail": f"已添加 '{word}' 到白名单"}
        else:
            return {"success": False, "detail": "添加失败"}
    except Exception as e:
        logger.error(f"添加白名单失败: {e}")
        return {"success": False, "detail": str(e)}


@router.delete("/whitelist/{word}", summary="移除白名单词")
async def remove_whitelist_word(
    word: str,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """从白名单移除词"""
    from security.sensitive_filter import remove_from_whitelist

    try:
        success = remove_from_whitelist(word)
        if success:
            return {"success": True, "detail": f"已从白名单移除 '{word}'"}
        else:
            return {"success": False, "detail": "未找到该词"}
    except Exception as e:
        logger.error(f"移除白名单失败: {e}")
        return {"success": False, "detail": str(e)}


# ========== 系统设置接口 ==========

@router.get("/settings", summary="获取系统设置")
async def get_settings(token: str = Depends(get_admin_token)) -> Dict[str, Any]:
    """获取系统设置"""
    return {
        "success": True,
        "data": {
            "admin_username": ADMIN_USERNAME,
            "auto_ban_enable": os.getenv("AUTO_BAN_ENABLE", "false").lower() == "true",
            "aliyun_green_enable": os.getenv("ALIYUN_GREEN_ENABLE", "false").lower() == "true",
            "default_bonus_credits": int(os.getenv("DEFAULT_BONUS_CREDITS", "3"))
        }
    }


# ========== 使用记录接口 ==========

def _mask_phone(mobile: str) -> str:
    """脱敏手机号：138****0000"""
    if not mobile or len(mobile) < 7:
        return mobile or "未知"
    return mobile[:3] + "****" + mobile[-4:]


def _parse_status(metadata: dict) -> str:
    """从metadata中解析审查状态"""
    if not metadata:
        return "success"
    m = metadata
    if isinstance(m, str):
        try:
            m = json.loads(m)
        except Exception:
            return "success"
    if m.get("error"):
        return "failed"
    if m.get("validation", {}).get("is_contract") is False:
        return "failed"
    return "success"


def _count_risks(report_md: str) -> int:
    """统计报告中的风险条目数量（正则匹配风险等级）"""
    if not report_md:
        return 0
    import re
    risk_indicators = re.findall(r'风险等级[：:]\\s*(高|中|低|严重|重大)', report_md)
    if risk_indicators:
        return len(risk_indicators)
    count = len(re.findall(r'^[#]{1,4}\\s+.*风险', report_md, re.MULTILINE))
    return count


@router.get("/usage", summary="获取使用记录列表")
async def get_usage_records(
    user_id: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """获取使用记录列表，支持按用户筛选和分页"""
    try:

        from storage.models import Record, User
        from sqlalchemy import desc

        with session_scope() as db:

            query = db.query(
                Record.id,
                Record.user_id,
                Record.filename,
                Record.report_markdown,
                Record.metadata_json,
                Record.created_at,
                User.mobile
            ).outerjoin(User, Record.user_id == User.id)

            if user_id:
                query = query.filter(Record.user_id == user_id)

            total = query.count()
            rows = query.order_by(desc(Record.created_at)) \
                        .offset((page - 1) * page_size) \
                        .limit(page_size) \
                        .all()

            records = []
            for row in rows:
                rid, uid, filename, report_md, meta_json, created_at, mobile = row
                metadata = {}
                if meta_json:
                    try:
                        metadata = json.loads(meta_json)
                    except Exception:
                        pass

                status_val = _parse_status(metadata)
                risk_count = _count_risks(report_md or "")

                duration_ms = 0
                if metadata.get("start_time") and metadata.get("end_time"):
                    try:
                        duration_ms = int((metadata["end_time"] - metadata["start_time"]) * 1000)
                    except Exception:
                        pass

                records.append({
                    "id": rid,
                    "user_id": uid,
                    "user_phone": _mask_phone(mobile) if mobile else "未知",
                    "filename": filename or "未知",
                    "created_at": created_at.isoformat() if created_at else "",
                    "duration_ms": duration_ms,
                    "status": status_val,
                    "risk_count": risk_count
                })

            return {
                "success": True,
                "total": total,
                "page": page,
                "page_size": page_size,
                "records": records
            }
    except Exception as e:
        logger.error(f"获取使用记录失败: {e}")
        return {"success": False, "detail": str(e)}


@router.get("/usage/users", summary="获取有记录的用户列表")
async def get_usage_users(token: str = Depends(get_admin_token)) -> Dict[str, Any]:
    """获取有审查记录的用户列表，用于筛选下拉框"""
    try:

        from storage.models import Record, User

        with session_scope() as db:

            rows = db.query(
                Record.user_id,
                User.mobile
            ).outerjoin(User, Record.user_id == User.id) \
             .group_by(Record.user_id, User.mobile) \
             .order_by(Record.user_id) \
             .all()

            users = []
            for uid, mobile in rows:
                if uid:
                    users.append({
                        "user_id": uid,
                        "user_phone": _mask_phone(mobile) if mobile else "未知"
                    })

            return {"success": True, "data": users}
    except Exception as e:
        logger.error(f"获取用户列表失败: {e}")
        return {"success": False, "detail": str(e)}


@router.get("/report/{record_id}", summary="查看审查报告")
async def get_admin_report(
    record_id: int,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """查看某次审查的完整报告（Markdown原文）"""
    try:

        from storage.models import Record, User

        with session_scope() as db:

            row = db.query(
                Record.id,
                Record.filename,
                Record.report_markdown,
                Record.created_at,
                User.mobile
            ).outerjoin(User, Record.user_id == User.id) \
             .filter(Record.id == record_id) \
             .first()

            if not row:
                return {"success": False, "detail": "记录不存在"}

            rid, filename, report_md, created_at, mobile = row

            return {
                "success": True,
                "data": {
                    "id": rid,
                    "filename": filename or "未知",
                    "user_phone": _mask_phone(mobile) if mobile else "未知",
                    "created_at": created_at.isoformat() if created_at else "",
                    "report_markdown": report_md or ""
                }
            }
    except Exception as e:
        logger.error(f"获取报告详情失败: {e}")
        return {"success": False, "detail": str(e)}


# ========== 用户管理接口 ==========

@router.get("/users", summary="获取用户列表")
async def get_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    mobile: Optional[str] = None,
    status: Optional[str] = None,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """获取用户列表（分页），支持按手机号搜索和状态筛选"""
    from storage.crud import get_users

    try:
        result = get_users(page=page, limit=size, mobile=mobile, status=status)

        # 脱敏手机号
        for user in result["data"]:
            user["mobile"] = _mask_phone(user["mobile"])

        return {
            "success": True,
            "data": result["data"],
            "total": result["total"],
            "page": result["page"],
            "size": result["limit"]
        }
    except Exception as e:
        logger.error(f"获取用户列表失败: {e}")
        return {"success": False, "detail": str(e)}


@router.get("/users/{user_id}", summary="获取用户详情")
async def get_user_detail(
    user_id: int,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """获取用户详情（含额度变动流水）"""
    from storage.crud import get_user_detail, get_admin_logs_by_target

    try:
        user = get_user_detail(user_id)
        if not user:
            return {"success": False, "detail": "用户不存在"}

        # 脱敏手机号
        user["mobile"] = _mask_phone(user["mobile"])

        # 获取额度变动流水（从admin_logs中提取）
        logs = get_admin_logs_by_target("user_id", str(user_id))

        return {
            "success": True,
            "data": {
                "user": user,
                "credit_logs": logs["data"]
            }
        }
    except Exception as e:
        logger.error(f"获取用户详情失败: {e}")
        return {"success": False, "detail": str(e)}


@router.post("/users/{user_id}/ban", summary="封禁用户")
async def ban_user(
    user_id: int,
    reason: Optional[str] = "",
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """封禁用户账号"""
    from storage.crud import update_user_status, create_admin_log

    try:
        success = update_user_status(user_id, "blocked")
        if not success:
            return {"success": False, "detail": "用户不存在"}

        # 记录操作日志
        create_admin_log(
            admin_user=ADMIN_USERNAME,
            action="ban_user",
            target_type="user_id",
            target_value=str(user_id),
            detail=reason or "管理员手动封禁"
        )

        logger.info(f"用户 {user_id} 已被封禁")
        return {"success": True, "detail": "已封禁用户"}
    except Exception as e:
        logger.error(f"封禁用户失败: {e}")
        return {"success": False, "detail": str(e)}


@router.post("/users/{user_id}/unban", summary="解封用户")
async def unban_user(
    user_id: int,
    reason: Optional[str] = "",
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """解封用户账号"""
    from storage.crud import update_user_status, create_admin_log

    try:
        success = update_user_status(user_id, "normal")
        if not success:
            return {"success": False, "detail": "用户不存在"}

        # 记录操作日志
        create_admin_log(
            admin_user=ADMIN_USERNAME,
            action="unban_user",
            target_type="user_id",
            target_value=str(user_id),
            detail=reason or "管理员手动解封"
        )

        logger.info(f"用户 {user_id} 已被解封")
        return {"success": True, "detail": "已解封用户"}
    except Exception as e:
        logger.error(f"解封用户失败: {e}")
        return {"success": False, "detail": str(e)}


@router.post("/users/create", summary="管理员创建用户")
async def create_user(
    mobile: str,
    password: str,
    country_code: str = "+86",
    bonus_credits: int = 3,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """管理员手动创建用户账号（默认状态为normal已审核）"""
    from storage.crud import create_user_by_admin, create_admin_log
    from auth.utils import hash_password

    try:
        if not mobile or not password:
            return {"success": False, "detail": "手机号和密码不能为空"}

        user = create_user_by_admin(
            mobile=mobile,
            password_hash=hash_password(password),
            country_code=country_code,
            bonus_credits=bonus_credits
        )

        create_admin_log(
            admin_user=ADMIN_USERNAME,
            action="create_user",
            target_type="user_id",
            target_value=str(user.id),
            detail=f"创建用户 {mobile}，赠送 {bonus_credits} 次额度"
        )

        logger.info(f"管理员创建用户: {mobile} (ID: {user.id})")
        return {
            "success": True,
            "detail": f"用户创建成功",
            "user_id": user.id,
            "mobile": _mask_phone(user.mobile)
        }
    except ValueError as e:
        return {"success": False, "detail": str(e)}
    except Exception as e:
        logger.error(f"创建用户失败: {e}")
        return {"success": False, "detail": str(e)}


@router.post("/users/{user_id}/approve", summary="审核通过用户")
async def approve_user(
    user_id: int,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """审核通过待审核用户（pending -> normal）"""
    from storage.crud import approve_user, create_admin_log

    try:
        success = approve_user(user_id)
        if not success:
            return {"success": False, "detail": "用户不存在或不是待审核状态"}

        create_admin_log(
            admin_user=ADMIN_USERNAME,
            action="approve_user",
            target_type="user_id",
            target_value=str(user_id),
            detail="管理员审核通过"
        )

        logger.info(f"用户 {user_id} 审核通过")
        return {"success": True, "detail": "已审核通过"}
    except Exception as e:
        logger.error(f"审核用户失败: {e}")
        return {"success": False, "detail": str(e)}


@router.post("/users/{user_id}/add-credits", summary="增加额度")
async def add_credits(
    user_id: int,
    amount: int = Query(1, ge=1),
    reason: Optional[str] = "",
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """增加用户免费审查额度"""
    from storage.crud import add_user_credits, create_admin_log

    try:
        new_credits = add_user_credits(user_id, amount)
        if new_credits == 0:
            return {"success": False, "detail": "用户不存在"}

        # 记录操作日志
        create_admin_log(
            admin_user=ADMIN_USERNAME,
            action="add_credits",
            target_type="user_id",
            target_value=str(user_id),
            detail=f"增加额度 +{amount}，理由: {reason}" if reason else f"增加额度 +{amount}"
        )

        logger.info(f"用户 {user_id} 额度增加 {amount}，当前额度: {new_credits}")
        return {
            "success": True,
            "detail": f"已增加 {amount} 次免费审查额度",
            "remaining_credits": new_credits
        }
    except Exception as e:
        logger.error(f"增加额度失败: {e}")
        return {"success": False, "detail": str(e)}


@router.post("/users/{user_id}/reduce-credits", summary="减少额度")
async def reduce_credits(
    user_id: int,
    amount: int = Query(1, ge=1),
    reason: Optional[str] = "",
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """减少用户免费审查额度"""
    from storage.crud import reduce_user_credits, create_admin_log

    try:
        new_credits = reduce_user_credits(user_id, amount)
        if new_credits == 0:
            # 需要检查是用户不存在还是额度已为0
            from storage.crud import get_user_detail
            user = get_user_detail(user_id)
            if not user:
                return {"success": False, "detail": "用户不存在"}

        # 记录操作日志
        create_admin_log(
            admin_user=ADMIN_USERNAME,
            action="reduce_credits",
            target_type="user_id",
            target_value=str(user_id),
            detail=f"减少额度 -{amount}，理由: {reason}" if reason else f"减少额度 -{amount}"
        )

        logger.info(f"用户 {user_id} 额度减少 {amount}，当前额度: {new_credits}")
        return {
            "success": True,
            "detail": f"已减少 {amount} 次免费审查额度",
            "remaining_credits": new_credits
        }
    except Exception as e:
        logger.error(f"减少额度失败: {e}")
        return {"success": False, "detail": str(e)}


@router.get("/users/{user_id}/records", summary="获取用户审查记录")
async def get_user_records(
    user_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """获取用户审查记录（分页）"""
    from storage.crud import get_user_records

    try:
        result = get_user_records(user_id, page=page, limit=size)

        # 处理每条记录
        records = []
        for record in result["data"]:
            # 计算风险数量
            risk_count = _count_risks(record["report_markdown"] or "")

            # 解析状态
            status_val = _parse_status(record["metadata"])

            records.append({
                "id": record["id"],
                "filename": record["filename"],
                "created_at": record["created_at"].isoformat() if record["created_at"] else "",
                "status": status_val,
                "risk_count": risk_count
            })

        return {
            "success": True,
            "data": records,
            "total": result["total"],
            "page": result["page"],
            "size": result["limit"]
        }
    except Exception as e:
        logger.error(f"获取用户审查记录失败: {e}")
        return {"success": False, "detail": str(e)}


@router.get("/users/{user_id}/records/{record_id}/final-report", summary="获取最终报告")
async def get_final_report(
    user_id: int,
    record_id: int,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """获取审查记录的最终报告（用户可见版本）"""
    try:

        from storage.models import Record

        with session_scope() as db:
            record = db.query(Record).filter(
                Record.id == record_id,
                Record.user_id == user_id
            ).first()

            if not record:
                return {"success": False, "detail": "记录不存在"}

            return {
                "success": True,
                "data": {
                    "id": record.id,
                    "filename": record.filename,
                    "report_markdown": record.report_markdown or "",
                    "created_at": record.created_at.isoformat() if record.created_at else ""
                }
            }
    except Exception as e:
        logger.error(f"获取最终报告失败: {e}")
        return {"success": False, "detail": str(e)}


@router.get("/users/{user_id}/records/{record_id}/raw-report", summary="获取原始报告")
async def get_raw_report(
    user_id: int,
    record_id: int,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """获取审查记录的原始报告（大模型返回的完整内容）"""
    try:

        from storage.models import Record

        with session_scope() as db:
            record = db.query(Record).filter(
                Record.id == record_id,
                Record.user_id == user_id
            ).first()

            if not record:
                return {"success": False, "detail": "记录不存在"}

            return {
                "success": True,
                "data": {
                    "id": record.id,
                    "filename": record.filename,
                    "raw_output": record.raw_output or "",
                    "created_at": record.created_at.isoformat() if record.created_at else ""
                }
            }
    except Exception as e:
        logger.error(f"获取原始报告失败: {e}")
        return {"success": False, "detail": str(e)}
