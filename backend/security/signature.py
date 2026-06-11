"""API签名校验与防逆向模块"""
import os
import time
import hashlib
from typing import Optional, Tuple
from functools import wraps
from fastapi import HTTPException, Request, Header
import logging

logger = logging.getLogger(__name__)

class APISignatureVerifier:
    def __init__(self):
        self.secret_key = os.getenv('API_SECRET_KEY', 'default_secret_change_in_production')
        self.timestamp_tolerance = 300

    def generate_signature(self, user_id: str, timestamp: str) -> str:
        data = f"{user_id}{timestamp}{self.secret_key}"
        return hashlib.md5(data.encode()).hexdigest()

    def verify(self, user_id: str, timestamp: str, signature: str) -> Tuple[bool, str]:
        try:
            ts = int(timestamp)
            now = int(time.time())

            if abs(now - ts) > self.timestamp_tolerance:
                return False, "签名已过期"

            expected = self.generate_signature(user_id, timestamp)
            if signature != expected:
                return False, "签名验证失败"

            return True, ""
        except ValueError:
            return False, "无效的时间戳格式"

    def verify_request(self, request: Request) -> Tuple[bool, str]:
        user_id = request.headers.get('X-User-ID')
        timestamp = request.headers.get('X-Timestamp')
        signature = request.headers.get('X-Signature')

        if not all([user_id, timestamp, signature]):
            return False, "缺少签名参数"

        return self.verify(user_id, timestamp, signature)

signature_verifier = APISignatureVerifier()

def verify_api_signature(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        if os.getenv('SKIP_SIGNATURE_VERIFY'):
            return await func(request, *args, **kwargs)

        valid, msg = signature_verifier.verify_request(request)
        if not valid:
            raise HTTPException(status_code=401, detail=f"签名校验失败: {msg}")

        return await func(request, *args, **kwargs)
    return wrapper
