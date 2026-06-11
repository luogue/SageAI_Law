"""管理员接口路由"""
import os
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from fastapi.security import APIKeyHeader
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
import json

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
    try:
        body = await request.json()
        username = body.get('username')
        password = body.get('password')
    except:
        # 尝试表单格式
        form_data = await request.form()
        username = form_data.get('username')
        password = form_data.get('password')
    
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
        db = next(__import__('storage.database', fromlist=['get_db']).get_db())
        
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
        db = next(__import__('storage.database', fromlist=['get_db']).get_db())
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
        db = next(__import__('storage.database', fromlist=['get_db']).get_db())
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
    """获取所有黑名单记录"""
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


@router.delete("/blacklist", summary="移除黑名单记录")
async def remove_from_blacklist(
    type: str,
    value: str,
    token: str = Depends(get_admin_token)
) -> Dict[str, Any]:
    """移除黑名单记录"""
    from security.blacklist import blacklist_manager
    
    if type not in ["ip", "user_id"]:
        return {"success": False, "detail": "无效的类型，必须是 'ip' 或 'user_id'"}
    
    try:
        success = blacklist_manager.remove(type, value)
        if success:
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
        success = blacklist_manager.add(type, value, reason, expires_datetime)
        if success:
            return {"success": True, "detail": f"已添加到黑名单: {type}={value}"}
        else:
            return {"success": False, "detail": "该记录已存在"}
    except Exception as e:
        logger.error(f"添加黑名单失败: {e}")
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
        from storage.database import get_db
        from storage.models import Record, User
        from sqlalchemy import desc

        db = next(get_db())

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
        from storage.database import get_db
        from storage.models import Record, User

        db = next(get_db())

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
        from storage.database import get_db
        from storage.models import Record, User

        db = next(get_db())

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
