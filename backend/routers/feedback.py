"""用户反馈路由 - 完整审查流程实现"""
from fastapi import APIRouter, Depends, HTTPException, Header, Request, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
import io
import hashlib
import json as json_lib
from datetime import datetime, timedelta
import asyncio
import logging

from auth.routes import get_current_user
from storage.crud import (
    create_feedback,
    update_feedback_bonus,
    get_feedbacks,
    get_feedback_count,
    get_user_bonus_credits,
    add_user_bonus_credits,
    get_today_bonus_count,
    check_contract_hash_exists,
    compute_contract_hash,
    add_bonus_log,
    get_feedback_by_id,
    update_feedback_status,
    update_feedback_score,
    create_reward_log,
    get_record,
    check_feedback_contract_uploaded,
)
from layers.input_layer import InputLayer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/feedback", tags=["feedback"])

# 初始化输入层（用于解析上传的合同文件）
_input_layer = InputLayer()


# ========== 文件包装器 - 用于适配InputLayer ==========

class _BytesFileWrapper:
    """将 bytes 内容包装成类文件对象，供 InputLayer.extract_text_from_file 使用"""
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self.file = io.BytesIO(content)


# ========== Pydantic模型 ==========

class SubmitFeedbackResponse(BaseModel):
    success: bool
    bonus_credits: int
    bonus_awarded: int
    message: str


class ReviewFeedbackRequest(BaseModel):
    feedback_id: int
    action: str  # "approve" 或 "reject"
    bonus_amount: Optional[int] = None  # 手动调整奖励额度
    reject_reason: Optional[str] = None


class FeedbacksResponse(BaseModel):
    success: bool
    feedbacks: List[dict]
    total: int
    page: int
    limit: int


# ========== 常量配置 ==========

# 基础规则
MIN_COMMENT_LENGTH = 20  # 最小描述长度（字符数）
MAX_COMMENT_LENGTH = 500  # 最大描述长度（字符数）
MIN_CONTRACT_LENGTH = 200  # 最小合同文本长度

# 频率限制
MAX_DAILY_FEEDBACK_PER_USER = 20  # 单用户每日最大反馈数
MAX_DAILY_FEEDBACK_PER_IP = 50  # 单IP每日最大反馈数
MIN_INTERVAL_BETWEEN_FEEDBACK = 10  # 两次反馈最小间隔（秒）- 测试期间临时降低

# 奖励规则
MAX_DAILY_BONUS_PER_USER = 10  # 单用户每日最大奖励额度
FEEDBACK_BONUS = 3  # 默认奖励额度

# 分类标签列表
VALID_CATEGORIES = [
    "风险遗漏",
    "误判",
    "建议不实用",
    "格式问题",
    "其他"
]


# ========== 内存存储频率限制计数器 ==========

# 存储结构: {user_id: {"count": int, "last_time": datetime}}
user_feedback_counter = {}
# 存储结构: {ip: {"count": int, "last_time": datetime}}
ip_feedback_counter = {}


def get_today_start() -> datetime:
    """获取今日开始时间"""
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def check_user_feedback_limit(user_id: int) -> tuple:
    """检查用户反馈频率限制"""
    now = datetime.now()
    today_start = get_today_start()
    
    user_data = user_feedback_counter.get(user_id, {"count": 0, "last_time": None})
    
    # 重置每日计数
    if user_data["last_time"] and user_data["last_time"] < today_start:
        user_data = {"count": 0, "last_time": None}
    
    # 检查每日上限
    if user_data["count"] >= MAX_DAILY_FEEDBACK_PER_USER:
        return False, "今日反馈次数已达上限"
    
    # 检查间隔限制
    if user_data["last_time"] and (now - user_data["last_time"]).seconds < MIN_INTERVAL_BETWEEN_FEEDBACK:
        remaining = MIN_INTERVAL_BETWEEN_FEEDBACK - (now - user_data["last_time"]).seconds
        return False, f"请等待{remaining}秒后再提交"
    
    return True, ""


def check_ip_feedback_limit(ip: str) -> tuple:
    """检查IP反馈频率限制"""
    now = datetime.now()
    today_start = get_today_start()
    
    ip_data = ip_feedback_counter.get(ip, {"count": 0, "last_time": None})
    
    # 重置每日计数
    if ip_data["last_time"] and ip_data["last_time"] < today_start:
        ip_data = {"count": 0, "last_time": None}
    
    # 检查每日上限
    if ip_data["count"] >= MAX_DAILY_FEEDBACK_PER_IP:
        return False, "当前IP今日反馈次数已达上限"
    
    return True, ""


def update_feedback_counter(user_id: int, ip: str):
    """更新反馈计数器"""
    now = datetime.now()
    
    # 更新用户计数器
    if user_id in user_feedback_counter:
        user_feedback_counter[user_id]["count"] += 1
    else:
        user_feedback_counter[user_id] = {"count": 1}
    user_feedback_counter[user_id]["last_time"] = now
    
    # 更新IP计数器
    if ip in ip_feedback_counter:
        ip_feedback_counter[ip]["count"] += 1
    else:
        ip_feedback_counter[ip] = {"count": 1}
    ip_feedback_counter[ip]["last_time"] = now


def validate_captcha_token(token: Optional[str]) -> bool:
    """验证滑动验证码token（简化实现，实际应调用验证码服务）"""
    # 生产环境应调用真实的验证码验证服务
    # 这里简化处理：非空即有效
    return token is not None and token.strip() != ""


def check_invalid_content(comment: str) -> bool:
    """检查是否包含无效内容（辱骂、纯广告等）"""
    # 简单关键词过滤
    invalid_keywords = [
        "操", "草", "尼玛", "傻逼", "去死", "垃圾",
        "广告", "推广", "代理", "加盟", "兼职",
        "色情", "赌博", "毒品", "枪支"
    ]
    
    for keyword in invalid_keywords:
        if keyword in comment:
            return True
    return False


# ========== 管理员验证 ==========

def verify_admin(admin_token: Optional[str] = Header(None, alias="X-Admin-Token")):
    """验证管理员身份"""
    from security.middleware import ADMIN_TOKEN
    if not admin_token or admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="管理员认证失败")
    return True


# ========== AI评分异步任务 ==========

async def score_feedback_async(feedback_id: int, categories: list, comment: str, has_contract: bool):
    """异步执行AI评分"""
    try:
        # 延迟导入避免循环依赖
        from utils.feedback_scorer import score_feedback_async as scorer_func
        
        # 调用评分器
        result = await asyncio.to_thread(
            scorer_func, 
            categories=categories,
            comment=comment,
            has_contract=has_contract
        )
        
        # 使用CRUD函数更新反馈记录（避免直接使用数据库会话导致循环导入）
        update_feedback_score(
            feedback_id=feedback_id,
            quality_score=result['quality_score'],
            suggested_bonus=result['suggested_bonus'],
            ai_reason=result['reason']
        )
            
        logger.info(f"反馈 {feedback_id} AI评分完成: {result}")
        
    except Exception as e:
        logger.error(f"反馈 {feedback_id} AI评分失败: {e}")
        # 评分失败不影响反馈提交，保持默认值0


# ========== 接口实现 ==========

@router.post("", response_model=SubmitFeedbackResponse)
async def submit_feedback(
    report_id: str = Form(...),
    feedback_type: str = Form(...),
    categories: str = Form("[]"),
    comment: str = Form(""),
    upload_consent: str = Form("false"),
    contract_file: Optional[UploadFile] = File(None),
    captcha_token: Optional[str] = Form(None),
    user_id: int = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Forwarded-For")
):
    """提交用户反馈 - 完整审查流程（支持multipart/form-data上传合同文件）"""
    # 获取真实IP
    if not client_ip:
        client_ip = "unknown"
    if "," in client_ip:
        client_ip = client_ip.split(",")[0].strip()
    
    # 解析 categories JSON 字符串
    try:
        categories_list = json_lib.loads(categories)
    except (json_lib.JSONDecodeError, TypeError):
        categories_list = []
    
    # 解析 upload_consent 布尔值
    upload_consent_bool = upload_consent.lower() in ("true", "1", "yes")
    
    # ========== 1. 验证验证码（开发环境可跳过）==========
    # if not validate_captcha_token(captcha_token):
    #     raise HTTPException(status_code=400, detail="验证码验证失败")
    
    # ========== 2. 频率限制检查 ==========
    # 用户级限制
    ok, msg = check_user_feedback_limit(user_id)
    if not ok:
        raise HTTPException(status_code=429, detail=msg)
    
    # IP级限制
    ok, msg = check_ip_feedback_limit(client_ip)
    if not ok:
        raise HTTPException(status_code=429, detail=msg)
    
    # ========== 3. 基础规则过滤 ==========
    # 检查分类标签
    if not categories_list or len(categories_list) == 0:
        raise HTTPException(status_code=400, detail="请至少选择一个反馈分类")
    
    # 验证分类有效性
    for cat in categories_list:
        if cat not in VALID_CATEGORIES:
            raise HTTPException(status_code=400, detail=f"无效的分类标签: {cat}")
    
    # 检查描述长度
    comment_length = len(comment.strip())
    if comment_length < MIN_COMMENT_LENGTH:
        raise HTTPException(status_code=400, detail=f"反馈描述至少需要{MIN_COMMENT_LENGTH}个字符")
    if comment_length > MAX_COMMENT_LENGTH:
        raise HTTPException(status_code=400, detail=f"反馈描述最多{MAX_COMMENT_LENGTH}个字符")
    
    # 检查无效内容
    if check_invalid_content(comment):
        logger.warning(f"用户 {user_id} 提交无效反馈内容")
        raise HTTPException(status_code=400, detail="反馈内容包含不当信息")
    
    # ========== 4. 处理合同文件上传 ==========
    contract_text = None
    has_valid_contract = False
    
    if upload_consent_bool and contract_file and contract_file.filename:
        # 4a. 读取文件内容并计算 MD5
        try:
            file_bytes = await contract_file.read()
        except Exception as e:
            logger.error(f"[反馈-合同上传] 读取文件失败: {e}")
            raise HTTPException(status_code=400, detail="合同文件读取失败，请重新上传")
        
        if not file_bytes or len(file_bytes) == 0:
            raise HTTPException(status_code=400, detail="合同文件为空，请重新上传")
        
        file_md5 = hashlib.md5(file_bytes).hexdigest()
        logger.info(f"[反馈-合同上传] 文件MD5: {file_md5}, 文件名: {contract_file.filename}")
        
        # 4b. 查询关联报告的 file_hash 进行 MD5 校验
        try:
            record_id_int = int(report_id)
            record = get_record(record_id_int, user_id)
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="无效的报告ID")
        
        if not record:
            raise HTTPException(status_code=400, detail="关联的报告不存在")
        
        expected_hash = record.get("metadata", {}).get("file_hash", "")
        if expected_hash:
            if file_md5 != expected_hash:
                logger.warning(
                    f"[反馈-合同上传] MD5不匹配! 期望: {expected_hash}, 实际: {file_md5}, "
                    f"用户: {user_id}, 报告: {report_id}"
                )
                raise HTTPException(status_code=400, detail="上传的合同文件与原始审查的合同不一致，请上传原始合同文件")
            logger.info(f"[反馈-合同上传] ✅ MD5校验通过")
        else:
            logger.warning(f"[反馈-合同上传] 报告 {report_id} 无 file_hash，跳过MD5校验")
        
        # 4c. 检查同一报告是否已上传过合同（最多一次）
        if check_feedback_contract_uploaded(report_id, user_id):
            raise HTTPException(status_code=400, detail="该报告的合同文件已上传，同一报告只能上传一次合同")
        
        # 4d. 解析文件内容为文本
        try:
            wrapper = _BytesFileWrapper(contract_file.filename, file_bytes)
            contract_text = _input_layer.extract_text_from_file(wrapper)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"[反馈-合同上传] 文件解析失败: {e}")
            raise HTTPException(status_code=400, detail=f"合同文件解析失败: {str(e)}")
        
        # 4e. 验证合同文本长度
        if contract_text and len(contract_text.strip()) >= MIN_CONTRACT_LENGTH:
            has_valid_contract = True
        else:
            # 文本不足则不视为有效上传
            logger.warning(f"[反馈-合同上传] 合同文本不足{MIN_CONTRACT_LENGTH}字符，不计入有效上传")
    
    # ========== 5. 更新计数器 ==========
    update_feedback_counter(user_id, client_ip)
    
    # ========== 6. 创建反馈记录（先不评分）==========
    feedback = create_feedback(
        user_id=user_id,
        report_id=report_id,
        feedback_type=feedback_type,
        categories=categories_list,
        comment=comment,
        upload_consent=upload_consent_bool,
        contract_text=contract_text if upload_consent_bool else None,
        quality_score=0,
        suggested_bonus=0,
        ai_reason=None
    )
    
    # ========== 7. 异步执行AI评分（不阻塞）==========
    asyncio.create_task(
        score_feedback_async(
            feedback.id,
            categories_list,
            comment,
            has_valid_contract
        )
    )
    
    # 获取当前用户额度
    current_credits = get_user_bonus_credits(user_id)
    
    return {
        "success": True,
        "bonus_credits": current_credits,
        "bonus_awarded": 0,
        "message": "感谢您的反馈！我们将尽快审核，审核通过后将赠送您免费审查额度。"
    }


# ========== 管理员接口 ==========

@router.get("", response_model=FeedbacksResponse)
async def list_feedbacks(
    page: int = 1,
    limit: int = 20,
    status: Optional[str] = None,
    category: Optional[str] = None,
    sort_by: Optional[str] = None,  # quality_score, created_at
    _: bool = Depends(verify_admin)
):
    """获取反馈列表（管理员接口）"""
    if page < 1:
        page = 1
    if limit < 1 or limit > 100:
        limit = 20

    feedbacks = get_feedbacks(page=page, limit=limit, category=category, status=status, sort_by=sort_by)
    total = get_feedback_count(category=category, status=status)

    return {
        "success": True,
        "feedbacks": feedbacks,
        "total": total,
        "page": page,
        "limit": limit
    }


@router.get("/{feedback_id}")
async def get_feedback_detail(
    feedback_id: int,
    _: bool = Depends(verify_admin)
):
    """获取反馈详情（管理员接口）"""
    feedback = get_feedback_by_id(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="反馈不存在")
    
    return {
        "success": True,
        "feedback": {
            "id": feedback.id,
            "user_id": feedback.user_id,
            "report_id": feedback.report_id,
            "feedback_type": feedback.feedback_type,
            "categories": feedback.categories,
            "comment": feedback.comment,
            "upload_consent": feedback.upload_consent,
            "contract_text": feedback.contract_text,
            "quality_score": feedback.quality_score,
            "suggested_bonus": feedback.suggested_bonus,
            "ai_reason": feedback.ai_reason,
            "status": feedback.status,
            "bonus_awarded": feedback.bonus_awarded,
            "reviewed_at": feedback.reviewed_at,
            "reviewed_by": feedback.reviewed_by,
            "reject_reason": feedback.reject_reason,
            "created_at": feedback.created_at
        }
    }


@router.post("/review")
async def review_feedback(
    request: ReviewFeedbackRequest,
    admin_token: str = Header(None, alias="X-Admin-Token")
):
    """审核反馈（管理员接口）"""
    from security.middleware import ADMIN_TOKEN
    
    # 验证管理员身份
    if not admin_token or admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="管理员认证失败")
    
    # 获取管理员用户名（从环境变量获取）
    admin_username = "admin"  # 实际应从token解析或配置获取
    
    # 验证 action
    if request.action not in ["approve", "reject"]:
        raise HTTPException(status_code=400, detail="无效的审核操作")

    # 获取反馈
    feedback = get_feedback_by_id(request.feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="反馈不存在")

    if feedback.status != "pending":
        raise HTTPException(status_code=400, detail="该反馈已被审核过")

    # 更新反馈状态
    now = datetime.utcnow()
    bonus_amount = 0

    if request.action == "approve":
        # 审核通过
        # 使用建议奖励或手动调整的奖励
        bonus_amount = request.bonus_amount if request.bonus_amount else feedback.suggested_bonus
        
        # 验证奖励范围
        if bonus_amount < 1 or bonus_amount > 5:
            raise HTTPException(status_code=400, detail="奖励额度必须在1-5之间")
        
        # 检查用户每日奖励上限
        today_bonus = get_today_bonus_count(feedback.user_id)
        if today_bonus + bonus_amount > MAX_DAILY_BONUS_PER_USER:
            raise HTTPException(status_code=400, detail=f"用户今日已达奖励上限（{MAX_DAILY_BONUS_PER_USER}次）")
        
        update_feedback_status(
            feedback_id=request.feedback_id,
            status="approved",
            reviewed_at=now,
            bonus_awarded=bonus_amount,
            reject_reason=None,
            reviewed_by=admin_username
        )

        # 增加用户额度
        current_credits = add_user_bonus_credits(feedback.user_id, bonus_amount)

        # 记录赠送日志
        add_bonus_log(
            user_id=feedback.user_id,
            bonus_type="feedback_approve",
            awarded_amount=bonus_amount,
            contract_hash=feedback.contract_hash
        )

        return {
            "success": True,
            "message": f"审核通过！已向用户赠送 {bonus_amount} 次免费审查额度",
            "bonus_awarded": bonus_amount,
            "current_credits": current_credits
        }
    else:
        # 审核驳回
        update_feedback_status(
            feedback_id=request.feedback_id,
            status="rejected",
            reviewed_at=now,
            bonus_awarded=0,
            reject_reason=request.reject_reason,
            reviewed_by=admin_username
        )

        return {
            "success": True,
            "message": "审核驳回，不赠送额度",
            "bonus_awarded": 0
        }


@router.post("/batch-review")
async def batch_review_feedback(
    feedback_ids: List[int],
    action: str,
    bonus_amount: Optional[int] = None,
    reject_reason: Optional[str] = None,
    admin_token: str = Header(None, alias="X-Admin-Token")
):
    """批量审核反馈（管理员接口）"""
    from security.middleware import ADMIN_TOKEN
    
    if not admin_token or admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="管理员认证失败")
    
    if action not in ["approve", "reject"]:
        raise HTTPException(status_code=400, detail="无效的审核操作")
    
    if action == "approve" and (bonus_amount is None or bonus_amount < 1 or bonus_amount > 5):
        raise HTTPException(status_code=400, detail="批量通过时奖励额度必须在1-5之间")
    
    results = []
    success_count = 0
    fail_count = 0
    
    for feedback_id in feedback_ids:
        try:
            feedback = get_feedback_by_id(feedback_id)
            if not feedback:
                results.append({"feedback_id": feedback_id, "success": False, "message": "反馈不存在"})
                fail_count += 1
                continue
            
            if feedback.status != "pending":
                results.append({"feedback_id": feedback_id, "success": False, "message": "反馈已被审核"})
                fail_count += 1
                continue
            
            now = datetime.utcnow()
            
            if action == "approve":
                # 检查用户每日奖励上限
                today_bonus = get_today_bonus_count(feedback.user_id)
                if today_bonus + bonus_amount > MAX_DAILY_BONUS_PER_USER:
                    results.append({"feedback_id": feedback_id, "success": False, "message": "用户今日奖励已达上限"})
                    fail_count += 1
                    continue
                
                update_feedback_status(
                    feedback_id=feedback_id,
                    status="approved",
                    reviewed_at=now,
                    bonus_awarded=bonus_amount,
                    reviewed_by="admin"
                )
                
                add_user_bonus_credits(feedback.user_id, bonus_amount)
                add_bonus_log(
                    user_id=feedback.user_id,
                    bonus_type="feedback_approve",
                    awarded_amount=bonus_amount,
                    contract_hash=feedback.contract_hash
                )
                
                results.append({"feedback_id": feedback_id, "success": True, "message": "审核通过"})
                success_count += 1
            else:
                update_feedback_status(
                    feedback_id=feedback_id,
                    status="rejected",
                    reviewed_at=now,
                    reject_reason=reject_reason,
                    reviewed_by="admin"
                )
                results.append({"feedback_id": feedback_id, "success": True, "message": "审核驳回"})
                success_count += 1
                
        except Exception as e:
            results.append({"feedback_id": feedback_id, "success": False, "message": str(e)})
            fail_count += 1
    
    return {
        "success": True,
        "total_count": len(feedback_ids),
        "success_count": success_count,
        "fail_count": fail_count,
        "results": results
    }
