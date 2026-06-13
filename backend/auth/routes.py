"""认证路由 - 短信验证码仅用于注册，登录使用手机号+密码"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional, Any, Dict

from .utils import create_access_token, verify_token, hash_password, verify_password
from storage.crud import (
    get_user_by_mobile, 
    create_user_with_invite, 
    add_user_bonus_credits,
    create_invite_reward,
    check_phone_has_been_invited,
    get_invitee_count_by_ip,
    get_user_by_id,
    parse_phone_number
)
from security.registration_rate_limiter import (
    check_registration_allowed,
    validate_phone_number
)
from utils.sms_client import sms_client
from utils.redis_client import redis_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 常量配置
INVITE_REWARD_CREDITS = 3  # 邀请奖励额度
NEW_USER_DEFAULT_CREDITS = 3  # 新用户默认赠送额度
MAX_INVITEES_PER_IP_24H = 3  # 24小时内同一IP最多被邀请注册次数
MAX_LOGIN_ATTEMPTS = 5  # 最大登录失败次数
LOGIN_LOCK_DURATION = 15 * 60  # 登录锁定时长（秒）
CAPTCHA_THRESHOLD = 3  # 登录失败几次后需要验证码

# 短信限流配置
SMS_RATE_LIMIT_PHONE_MINUTE = 1  # 同一手机号每分钟最多1次
SMS_RATE_LIMIT_PHONE_HOUR = 3  # 同一手机号每小时最多3次
SMS_RATE_LIMIT_PHONE_DAY = 10  # 同一手机号每天最多10次
SMS_RATE_LIMIT_IP_HOUR = 10  # 同一IP每小时最多10次


class RegisterRequest(BaseModel):
    phone: str
    sms_code: str
    password: str
    confirm_password: str
    captcha_token: Optional[str] = None
    inviter_id: Optional[int] = None  # 邀请人ID


class LoginRequest(BaseModel):
    phone: str
    password: str
    captcha_token: Optional[str] = None


class SendCodeRequest(BaseModel):
    phone: str
    captcha_token: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    mobile: str


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """获取当前用户依赖"""
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return int(user_id)


def check_sms_rate_limit(phone: str, client_ip: str) -> Optional[str]:
    """
    检查短信发送频率限制
    :return: 如果受限返回错误消息，否则返回None
    """
    # 检查手机号限流 - 每分钟
    phone_minute_key = f"sms:limit:phone:minute:{phone}"
    phone_minute_count = redis_client.incr(phone_minute_key)
    if phone_minute_count == 1:
        redis_client.expire(phone_minute_key, 60)
    if phone_minute_count > SMS_RATE_LIMIT_PHONE_MINUTE:
        return "请稍后再试，每分钟最多发送1次验证码"
    
    # 检查手机号限流 - 每小时
    phone_hour_key = f"sms:limit:phone:hour:{phone}"
    phone_hour_count = redis_client.incr(phone_hour_key)
    if phone_hour_count == 1:
        redis_client.expire(phone_hour_key, 3600)
    if phone_hour_count > SMS_RATE_LIMIT_PHONE_HOUR:
        return "请稍后再试，每小时最多发送3次验证码"
    
    # 检查手机号限流 - 每天
    phone_day_key = f"sms:limit:phone:day:{phone}"
    phone_day_count = redis_client.incr(phone_day_key)
    if phone_day_count == 1:
        redis_client.expire(phone_day_key, 86400)
    if phone_day_count > SMS_RATE_LIMIT_PHONE_DAY:
        return "今日发送次数已达上限，请明天再试"
    
    # 检查IP限流 - 每小时
    ip_hour_key = f"sms:limit:ip:hour:{client_ip}"
    ip_hour_count = redis_client.incr(ip_hour_key)
    if ip_hour_count == 1:
        redis_client.expire(ip_hour_key, 3600)
    if ip_hour_count > SMS_RATE_LIMIT_IP_HOUR:
        return "当前IP发送过于频繁，请稍后再试"
    
    return None


def check_login_lock(phone: str, client_ip: str) -> Optional[str]:
    """
    检查登录锁定状态
    :return: 如果锁定返回错误消息，否则返回None
    """
    # 检查手机号登录失败次数
    phone_fail_key = f"login:fail:phone:{phone}"
    phone_fail_count = redis_client.get(phone_fail_key)
    if phone_fail_count and int(phone_fail_count) >= MAX_LOGIN_ATTEMPTS:
        return "该账号已被锁定，请15分钟后再试"
    
    # 检查IP登录失败次数
    ip_fail_key = f"login:fail:ip:{client_ip}"
    ip_fail_count = redis_client.get(ip_fail_key)
    if ip_fail_count and int(ip_fail_count) >= MAX_LOGIN_ATTEMPTS:
        return "当前IP登录失败次数过多，请15分钟后再试"
    
    return None


def record_login_failure(phone: str, client_ip: str):
    """记录登录失败"""
    # 记录手机号失败次数
    phone_fail_key = f"login:fail:phone:{phone}"
    phone_fail_count = redis_client.incr(phone_fail_key)
    if phone_fail_count == 1:
        redis_client.expire(phone_fail_key, LOGIN_LOCK_DURATION)
    
    # 记录IP失败次数
    ip_fail_key = f"login:fail:ip:{client_ip}"
    ip_fail_count = redis_client.incr(ip_fail_key)
    if ip_fail_count == 1:
        redis_client.expire(ip_fail_key, LOGIN_LOCK_DURATION)


def clear_login_failure(phone: str, client_ip: str):
    """清除登录失败记录"""
    redis_client.delete(f"login:fail:phone:{phone}")
    redis_client.delete(f"login:fail:ip:{client_ip}")


@router.post("/send-code")
async def send_sms_code(request: SendCodeRequest, req: Request) -> Dict[str, Any]:
    """发送短信验证码接口（仅用于注册）"""
    client_ip = req.client.host if req.client else "unknown"
    
    # 验证手机号格式
    valid, phone_msg = validate_phone_number(request.phone)
    if not valid:
        return {"success": False, "detail": phone_msg}
    
    # 检查手机号是否已注册
    existing_user = get_user_by_mobile(request.phone)
    if existing_user:
        return {"success": False, "detail": "该手机号已被注册"}
    
    # 检查频率限制
    rate_limit_msg = check_sms_rate_limit(request.phone, client_ip)
    if rate_limit_msg:
        return {"success": False, "detail": rate_limit_msg}
    
    # 验证滑动验证码（如果提供了）
    if request.captcha_token:
        # TODO: 实际实现滑动验证码验证
        pass
    
    # 发送验证码
    success = sms_client.send_sms_code(request.phone)
    if not success:
        return {"success": False, "detail": "发送失败，请稍后再试"}
    
    logger.info(f"短信验证码发送成功: {request.phone}")
    return {"success": True, "message": "验证码已发送，请注意查收"}


def check_need_captcha(phone: str, client_ip: str) -> bool:
    """检查是否需要验证码（登录失败3次后需要）"""
    # 检查手机号登录失败次数
    phone_fail_key = f"login:fail:phone:{phone}"
    phone_fail_count = redis_client.get(phone_fail_key)
    if phone_fail_count and int(phone_fail_count) >= CAPTCHA_THRESHOLD:
        return True
    
    # 检查IP登录失败次数
    ip_fail_key = f"login:fail:ip:{client_ip}"
    ip_fail_count = redis_client.get(ip_fail_key)
    if ip_fail_count and int(ip_fail_count) >= CAPTCHA_THRESHOLD:
        return True
    
    return False


@router.post("/login")
async def login(request: LoginRequest, req: Request) -> Dict[str, Any]:
    """登录接口 - 仅支持手机号+密码登录"""
    client_ip = req.client.host if req.client else "unknown"
    
    # 验证手机号格式
    valid, phone_msg = validate_phone_number(request.phone)
    if not valid:
        return {"success": False, "code": 4001, "detail": phone_msg}
    
    # 检查登录锁定
    lock_msg = check_login_lock(request.phone, client_ip)
    if lock_msg:
        return {"success": False, "code": 4002, "detail": lock_msg}
    
    # 检查是否需要验证码
    need_captcha = check_need_captcha(request.phone, client_ip)
    if need_captcha and not request.captcha_token:
        return {"success": False, "code": 4004, "detail": "请先完成图形验证码验证"}
    
    # 解析手机号，分离区号和手机号
    country_code, mobile = parse_phone_number(request.phone)
    
    # 获取用户
    user = get_user_by_mobile(mobile, country_code)
    
    # 如果带区号查询不到，尝试只按手机号查询（兼容旧数据）
    if not user:
        user = get_user_by_mobile(mobile)
    
    if not user:
        # 记录失败并返回通用错误
        record_login_failure(request.phone, client_ip)
        new_fail_count = int(redis_client.get(f"login:fail:phone:{request.phone}") or 0)
        return {
            "success": False, 
            "code": 4003, 
            "detail": "手机号或密码错误",
            "need_captcha": new_fail_count >= CAPTCHA_THRESHOLD
        }
    
    # 验证密码
    if not verify_password(request.password, user.password_hash):
        # 记录失败
        record_login_failure(request.phone, client_ip)
        new_fail_count = int(redis_client.get(f"login:fail:phone:{request.phone}") or 0)
        return {
            "success": False, 
            "code": 4003, 
            "detail": "手机号或密码错误",
            "need_captcha": new_fail_count >= CAPTCHA_THRESHOLD
        }
    
    # 清除失败记录
    clear_login_failure(request.phone, client_ip)
    
    # 生成Token
    access_token = create_access_token(data={"user_id": user.id})
    
    logger.info(f"用户登录成功: {request.phone}")
    return {
        "success": True,
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "mobile": user.mobile
    }


@router.post("/register")
async def register(request: RegisterRequest, req: Request) -> Dict[str, Any]:
    """注册接口 - 需验证短信验证码"""
    client_ip = req.client.host if req.client else "unknown"
    
    # 验证手机号格式
    valid, phone_msg = validate_phone_number(request.phone)
    if not valid:
        return {"success": False, "detail": phone_msg}
    
    # 验证短信验证码
    if not sms_client.verify_code(request.phone, request.sms_code):
        return {"success": False, "detail": "验证码错误或已过期"}
    
    # 验证滑动验证码（如果提供了）
    if request.captcha_token:
        # TODO: 实际实现滑动验证码验证
        pass
    
    # 解析手机号，分离区号和手机号
    country_code, mobile = parse_phone_number(request.phone)
    
    # 检查用户是否已存在
    existing_user = get_user_by_mobile(mobile, country_code)
    
    # 如果带区号查询不到，尝试只按手机号查询（兼容旧数据）
    if not existing_user:
        existing_user = get_user_by_mobile(mobile)
    
    if existing_user:
        return {"success": False, "detail": "该手机号已被注册"}
    
    # 验证密码一致性
    if request.password != request.confirm_password:
        return {"success": False, "detail": "两次输入的密码不一致"}
    
    # 防刷检查：IP注册频率限制
    allowed, rate_limit_msg = check_registration_allowed(client_ip)
    if not allowed:
        return {"success": False, "detail": rate_limit_msg}
    
    # ========== 邀请相关检查 ==========
    inviter_id = request.inviter_id
    if inviter_id:
        # 检查邀请人是否存在
        inviter = get_user_by_id(inviter_id)
        if not inviter:
            return {"success": False, "detail": "邀请人不存在"}
        
        # 防刷检查：同一手机号只能被邀请一次
        if check_phone_has_been_invited(request.phone):
            return {"success": False, "detail": "该手机号已通过邀请注册"}
        
        # 防刷检查：同一IP 24小时内最多被邀请注册3次
        invitee_count = get_invitee_count_by_ip(client_ip)
        if invitee_count >= MAX_INVITEES_PER_IP_24H:
            return {"success": False, "detail": "操作频繁，请稍后再试"}
        
        # 防刷检查：禁止自我邀请
        if inviter.mobile == mobile:
            return {"success": False, "detail": "不能邀请自己注册"}
    
    # 创建用户（支持邀请人）
    user = create_user_with_invite(mobile, hash_password(request.password), inviter_id, country_code)
    
    # 为新用户赠送默认免费审查额度
    add_user_bonus_credits(user.id, NEW_USER_DEFAULT_CREDITS)
    
    # ========== 邀请奖励记录（pending状态，等待被邀请人完成首次审查后发放）==========
    if inviter_id:
        create_invite_reward(inviter_id, user.id, INVITE_REWARD_CREDITS, status="pending")
        logger.info(f"邀请记录创建成功 - 邀请人:{inviter_id}, 被邀请人:{user.id}, 等待首次审查后发放奖励")
    
    # 生成Token
    access_token = create_access_token(data={"user_id": user.id})
    
    logger.info(f"新用户注册成功: {request.phone}")
    return {
        "success": True,
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "mobile": user.mobile
    }


@router.get("/me")
async def get_current_user_info(user_id: int = Depends(get_current_user)):
    """获取当前用户信息"""
    from ..storage import get_user_by_id
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"user_id": user.id, "mobile": user.mobile, "created_at": user.created_at}
