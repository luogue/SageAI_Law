"""限流模块 - Redis/内存双模式"""
import os
import time
import threading
import hashlib
from typing import Dict, Tuple
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

# 尝试导入Redis
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis未安装，将使用内存模式进行限流")


class MemoryRateLimiter:
    """内存版限流器 - 单机使用"""

    def __init__(self):
        self._counters: Dict[str, list] = {}
        self._lock = threading.Lock()

    def _cleanup(self, key: str, window: int):
        """清理过期记录"""
        now = time.time()
        if key in self._counters:
            self._counters[key] = [t for t in self._counters[key] if now - t < window]

    def check(self, identifier: str, limit: int, window: int) -> Tuple[bool, str]:
        """检查是否超出限流，返回 (是否允许, 提示信息)"""
        key = f"{identifier}:{limit}:{window}"
        with self._lock:
            self._cleanup(key, window)
            if key in self._counters and len(self._counters[key]) >= limit:
                return False, f"请求过于频繁，请{window//60}分钟后重试"
            self._counters.setdefault(key, []).append(time.time())
            return True, ""


class RedisRateLimiter:
    """Redis版限流器 - 支持分布式"""

    def __init__(self, redis_url: str):
        try:
            # 设置较短的超时时间，避免长时间等待
            self.redis_client = redis.from_url(
                redis_url, 
                decode_responses=True,
                socket_connect_timeout=2,  # 连接超时2秒
                socket_timeout=2  # 操作超时2秒
            )
            self.redis_client.ping()
            logger.info(f"Redis连接成功: {redis_url}")
        except Exception as e:
            logger.error(f"Redis连接失败: {e}，将回退到内存模式")
            self.redis_client = None

    def check(self, identifier: str, limit: int, window: int) -> Tuple[bool, str]:
        """检查是否超出限流"""
        if not self.redis_client:
            return True, ""  # Redis不可用时不过度阻止

        key = f"rate_limit:{hashlib.md5(identifier.encode()).hexdigest()}"
        try:
            pipeline = self.redis_client.pipeline(transaction=True)
            pipeline.incr(key)
            pipeline.expire(key, window)
            count, _ = pipeline.execute()

            if count > limit:
                return False, f"请求过于频繁，请{window//60}分钟后重试"
            return True, ""
        except Exception as e:
            logger.error(f"Redis限流检查失败: {e}")
            return True, ""  # 限流失败时放行


class RateLimiter:
    """统一限流器"""

    def __init__(self):
        self._config = {
            "upload": {
                "user": (5, 60),   # 用户：5次/分钟
                "ip": (10, 60)    # IP：10次/分钟
            },
            "review": {
                "user": (5, 60),   # 用户：5次/分钟（符合安全要求）
                "ip": (5, 60)     # IP：5次/分钟（符合安全要求）
            }
        }

        redis_url = os.getenv("REDIS_URL")
        if redis_url and REDIS_AVAILABLE:
            self._limiter = RedisRateLimiter(redis_url)
        else:
            self._limiter = MemoryRateLimiter()
            logger.info("使用内存模式限流")

    def is_allowed(self, user_id: str, ip: str, limit_type: str = "review") -> Tuple[bool, str]:
        """检查是否允许请求"""
        if limit_type not in self._config:
            return True, ""

        config = self._config[limit_type]

        # 检查用户限流（如果已登录）
        if user_id and user_id != "anonymous":
            user_limit, user_window = config["user"]
            allowed, msg = self._limiter.check(f"user:{user_id}", user_limit, user_window)
            if not allowed:
                return False, f"用户限流: {msg}"

        # 检查IP限流
        if ip:
            ip_limit, ip_window = config["ip"]
            allowed, msg = self._limiter.check(f"ip:{ip}", ip_limit, ip_window)
            if not allowed:
                return False, f"IP限流: {msg}"

        return True, ""


# 全局限流器实例
_rate_limiter: RateLimiter = None


def get_rate_limiter() -> RateLimiter:
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter
