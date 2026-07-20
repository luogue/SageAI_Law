"""认证路由 - 手机号+密码登录，注册由管理员后台操作"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional, Any, Dict

from .utils import create_access_token, verify_token, hash_password, verify_password
from storage.crud import (
    get_user_by_mobile, 
    get_user_by_id,
    parse_phone_number
)
from security.registration_rate_limiter import validate_phone_number
from utils.redis_client import redis_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 常量配置
MAX_LOGIN_ATTEMPTS = 5  # 最大登录失败次数
LOGIN_LOCK_DURATION = 15 * 60  # 登录锁定时长（秒）
CAPTCHA_THRESHOLD = 3  # 登录失败几次后需要验证码


class LoginRequest(BaseModel):
    phone: str
    password: str
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


def check_need_captcha(phone: str, client_ip: str) -> bool:
    """检查是否需要验证码（登录失败3次后需要）"""
    phone_fail_key = f"login:fail:phone:{phone}"
    phone_fail_count = redis_client.get(phone_fail_key)
    if phone_fail_count and int(phone_fail_count) >= CAPTCHA_THRESHOLD:
        return True
    
    ip_fail_key = f"login:fail:ip:{client_ip}"
    ip_fail_count = redis_client.get(ip_fail_key)
    if ip_fail_count and int(ip_fail_count) >= CAPTCHA_THRESHOLD:
        return True
    
    return False


@router.post("/login")
async def login(request: LoginRequest, req: Request) -> Dict[str, Any]:
    """登录接口 - 仅支持手机号+密码登录，pending用户需管理员审核后方可登录"""
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
        record_login_failure(request.phone, client_ip)
        new_fail_count = int(redis_client.get(f"login:fail:phone:{request.phone}") or 0)
        return {
            "success": False, 
            "code": 4003, 
            "detail": "手机号或密码错误",
            "need_captcha": new_fail_count >= CAPTCHA_THRESHOLD
        }
    
    # 检查用户状态：pending 需等待管理员审核
    if user.status == "pending":
        return {
            "success": False,
            "code": 4005,
            "detail": "您的账号正在审核中，请等待管理员审核通过后再登录"
        }
    
    # 检查用户状态：blocked 被封禁
    if user.status == "blocked":
        return {
            "success": False,
            "code": 4006,
            "detail": "您的账号已被封禁，请联系管理员"
        }
    
    # 验证密码
    if not verify_password(request.password, user.password_hash):
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


@router.get("/me")
async def get_current_user_info(user_id: int = Depends(get_current_user)):
    """获取当前用户信息"""
    from ..storage import get_user_by_id
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"user_id": user.id, "mobile": user.mobile, "created_at": user.created_at}
