"""Redis客户端模块"""
import os
import redis
from typing import Optional, Any

class RedisClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance._client = None
            cls._instance._connection_attempted = False  # 标记是否已尝试连接
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
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置键值对"""
        client = self.get_client()
        if client is None:
            return False
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
            return None
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
            return False
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
            return False
        try:
            return client.exists(key) > 0
        except Exception as e:
            print(f"Redis exists error: {e}")
            return False
    
    def incr(self, key: str, amount: int = 1) -> Optional[int]:
        """递增计数器"""
        client = self.get_client()
        if client is None:
            return None
        try:
            return client.incr(key, amount)
        except Exception as e:
            print(f"Redis incr error: {e}")
            return None
    
    def expire(self, key: str, ttl: int) -> bool:
        """设置过期时间"""
        client = self.get_client()
        if client is None:
            return False
        try:
            client.expire(key, ttl)
            return True
        except Exception as e:
            print(f"Redis expire error: {e}")
            return False

# 创建全局实例
redis_client = RedisClient()
