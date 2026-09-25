"""Redis客户端模块"""
import os
import redis
import time
from typing import Optional, Any
from collections import defaultdict

class RedisClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance._client = None
            cls._instance._connection_attempted = False  # 标记是否已尝试连接
            cls._instance._memory_cache = {}  # 内存缓存，用于Redis不可用时
            cls._instance._memory_expire = {}  # 内存缓存的过期时间
        return cls._instance
    
    def connect(self):
        """连接Redis"""
        # 如果已经尝试过连接且失败，直接返回False，避免重复尝试
        if self._connection_attempted and self._client is None:
            return False
        
        self._connection_attempted = True
        try:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
            # 设置较短的超时时间，避免长时间等待
            self._client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=2,  # 连接超时2秒
                socket_timeout=2  # 操作超时2秒
            )
            # 测试连接
            self._client.ping()
            return True
        except Exception as e:
            print(f"Redis连接失败: {e}")
            self._client = None
            return False
    
    def get_client(self):
        """获取Redis客户端"""
        if self._client is None and not self._connection_attempted:
            self.connect()
        return self._client
    
    def _clean_expired(self):
        """清理过期的内存缓存"""
        now = time.time()
        expired_keys = [k for k, expire_at in self._memory_expire.items() if expire_at > 0 and expire_at < now]
        for k in expired_keys:
            self._memory_cache.pop(k, None)
            self._memory_expire.pop(k, None)
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置键值对"""
        client = self.get_client()
        if client is None:
            # 使用内存模式
            self._memory_cache[key] = str(value)
            if ttl:
                self._memory_expire[key] = time.time() + ttl
            else:
                self._memory_expire[key] = -1  # -1 表示永不过期
            return True
        try:
            if ttl:
                client.set(key, value, ex=ttl)
            else:
                client.set(key, value)
            return True
        except Exception as e:
            print(f"Redis set error: {e}")
            return False
    
    def get(self, key: str) -> Optional[str]:
        """获取键值"""
        client = self.get_client()
        if client is None:
            # 使用内存模式
            self._clean_expired()
            return self._memory_cache.get(key)
        try:
            value = client.get(key)
            return value.decode('utf-8') if isinstance(value, bytes) else value
        except Exception as e:
            print(f"Redis get error: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """删除键"""
        client = self.get_client()
        if client is None:
            # 使用内存模式
            self._memory_cache.pop(key, None)
            self._memory_expire.pop(key, None)
            return True
        try:
            client.delete(key)
            return True
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        client = self.get_client()
        if client is None:
            # 使用内存模式
            self._clean_expired()
            return key in self._memory_cache
        try:
            return client.exists(key) > 0
        except Exception as e:
            print(f"Redis exists error: {e}")
            return False
    
    def incr(self, key: str, amount: int = 1) -> Optional[int]:
        """递增计数器"""
        client = self.get_client()
        if client is None:
            # 使用内存模式
            self._clean_expired()
            current = int(self._memory_cache.get(key, "0"))
            current += amount
            self._memory_cache[key] = str(current)
            # 默认设置过期时间为15分钟（登录锁定时间）
            if key not in self._memory_expire or self._memory_expire[key] == -1:
                self._memory_expire[key] = time.time() + 15 * 60
            return current
        try:
            return client.incr(key, amount)
        except Exception as e:
            print(f"Redis incr error: {e}")
            return None
    
    def expire(self, key: str, ttl: int) -> bool:
        """设置过期时间"""
        client = self.get_client()
        if client is None:
            # 使用内存模式
            self._memory_expire[key] = time.time() + ttl
            return True
        try:
            client.expire(key, ttl)
            return True
        except Exception as e:
            print(f"Redis expire error: {e}")
            return False

# 创建全局实例
redis_client = RedisClient()
