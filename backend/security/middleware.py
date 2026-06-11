"""全局安全中间件"""
import os
import time
import uuid
from typing import Callable
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

from .sensitive_filter import get_sensitive_filter
from .rate_limiter import get_rate_limiter
from .logging_utils import structured_logger, desensitizer
from .blacklist import check_blacklist

logger = logging.getLogger(__name__)

# 环境变量控制功能开关
ENABLE_SENSITIVE_FILTER = os.getenv("ENABLE_SENSITIVE_FILTER", "true").lower() == "true"
ENABLE_RATE_LIMIT = os.getenv("ENABLE_RATE_LIMIT", "true").lower() == "true"
ENABLE_AUTO_BAN = os.getenv("AUTO_BAN_ENABLE", "true").lower() == "true"
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "admin_secure_token_change_me")


class SecurityMiddleware(BaseHTTPMiddleware):
    """综合安全中间件"""

    async def dispatch(self, request: Request, call_next: Callable):
        # 优先使用前端传递的trace_id，如果没有则生成新的
        trace_id = request.headers.get("X-Trace-ID") or str(uuid.uuid4())[:8]
        request.state.request_id = trace_id
        request.state.trace_id = trace_id
        
        # 设置trace_id到上下文变量，用于日志追踪
        from security.logging_utils import trace_id_context
        trace_id_context.set(trace_id)
        
        client_ip = request.client.host if request.client else "unknown"
        user_id = getattr(request.state, "user_id", "anonymous")
        start_time = time.time()

        # ========== 黑名单检查 ==========
        blacklisted = check_blacklist(client_ip, str(user_id) if user_id != "anonymous" else None)
        if blacklisted:
            structured_logger.log_security(
                "BLACKLIST_BLOCK", client_ip, str(user_id), reason=f"{blacklisted}在黑名单中"
            )
            return JSONResponse(
                status_code=403,
                content={"success": False, "detail": "您的访问已被禁止，如有疑问请联系管理员"}
            )

        # ========== 自动封禁检查 ==========
        if ENABLE_AUTO_BAN:
            try:
                from utils.security import check_auto_ban
                is_auto_banned = check_auto_ban(client_ip, user_id if user_id != "anonymous" else None)
                if is_auto_banned:
                    structured_logger.log_security(
                        "AUTO_BAN_BLOCK", client_ip, str(user_id), reason="自动封禁"
                    )
                    return JSONResponse(
                        status_code=403,
                        content={"success": False, "detail": "您的访问已被系统自动禁止，如有疑问请联系管理员"}
                    )
            except Exception as e:
                logger.error(f"[AUTO_BAN] 自动封禁检查失败: {e}")
                # 自动封禁检查失败不应影响正常请求

        # ========== 限流检查 ==========
        if ENABLE_RATE_LIMIT:
            path = request.url.path
            if path.startswith("/api/review") or path.startswith("/api/batch"):
                limiter = get_rate_limiter()
                allowed, msg = limiter.is_allowed(str(user_id), client_ip, "review")
                if not allowed:
                    structured_logger.log_security(
                        "RATE_LIMIT_BLOCK", client_ip, str(user_id), reason=msg
                    )
                    return JSONResponse(status_code=429, content={"success": False, "detail": msg})

        # ========== 敏感词检查（仅对特定输入） ==========
        # 注意：不在这里检查，因为需要读取请求体，而是放在业务逻辑中检查
        request.state.client_ip = client_ip

        response = await call_next(request)

        # ========== 日志记录 ==========
        duration = time.time() - start_time
        structured_logger.log_request(
            request.state.request_id,
            str(user_id),
            client_ip,
            request.url.path,
            request.method,
            duration,
            response.status_code
        )

        return response
