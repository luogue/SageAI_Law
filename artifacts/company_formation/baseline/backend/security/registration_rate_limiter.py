"""注册限流模块 - 防止恶意注册"""
import time
import threading
import os
import logging
from collections import defaultdict
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

# 配置
MAX_REGISTRATIONS_PER_IP = 5  # 每IP每小时最多注册5个账号
WINDOW_SIZE = 3600  # 1小时窗口（秒）

# 虚拟号段（禁止注册）
VIRTUAL_PHONE_PREFIXES = [
    '170', '171',  # 虚拟运营商
    '165', '167',  # 虚拟运营商
]


class RegistrationRateLimiter:
    """注册频率限制器"""

    def __init__(self):
        self._lock = threading.Lock()
        # 存储注册记录: {ip: [timestamps]}
        self._registrations: dict = defaultdict(list)
        # 启动清理线程
        self._stop_event = threading.Event()
        self._cleanup_thread = threading.Thread(target=self._cleanup_expired, daemon=True)
        self._cleanup_thread.start()

    def check(self, ip: str) -> Tuple[bool, str]:
        """
        检查是否允许注册
        返回: (是否允许, 错误信息)
        """
        current_time = time.time()
        one_hour_ago = current_time - WINDOW_SIZE

        with self._lock:
            # 清理过期记录
            self._registrations[ip] = [
                t for t in self._registrations[ip] if t >= one_hour_ago
            ]

            # 检查是否超过限制
            if len(self._registrations[ip]) >= MAX_REGISTRATIONS_PER_IP:
                remaining_time = int(
                    (self._registrations[ip][0] + WINDOW_SIZE - current_time) / 60
                )
                return False, f"该IP注册过于频繁，请{remaining_time}分钟后重试"

            # 记录本次注册
            self._registrations[ip].append(current_time)
            return True, ""

    def record_registration(self, ip: str):
        """记录注册（备用）"""
        with self._lock:
            self._registrations[ip].append(time.time())

    def _cleanup_expired(self):
        """清理过期的注册记录（后台线程）"""
        while not self._stop_event.is_set():
            try:
                cutoff_time = time.time() - WINDOW_SIZE * 2
                with self._lock:
                    for ip in list(self._registrations.keys()):
                        self._registrations[ip] = [
                            t for t in self._registrations[ip] if t >= cutoff_time
                        ]
                        if not self._registrations[ip]:
                            del self._registrations[ip]
            except Exception as e:
                logger.error(f"清理注册记录失败: {e}")

            # 每5分钟清理一次
            self._stop_event.wait(300)

    def close(self):
        """关闭"""
        self._stop_event.set()
        if self._cleanup_thread.is_alive():
            self._cleanup_thread.join(timeout=5)

    def get_stats(self, ip: str) -> dict:
        """获取IP的注册统计"""
        one_hour_ago = time.time() - WINDOW_SIZE
        with self._lock:
            recent = [t for t in self._registrations.get(ip, []) if t >= one_hour_ago]
            return {
                "ip": ip,
                "registrations_last_hour": len(recent),
                "max_allowed": MAX_REGISTRATIONS_PER_IP,
                "remaining": max(0, MAX_REGISTRATIONS_PER_IP - len(recent))
            }


class PhoneNumberValidator:
    """手机号验证器"""

    # 支持的国际区号
    COUNTRY_CODES = {
        '+86': {'name': '中国', 'min_length': 11, 'max_length': 11, 'pattern': r'^1[3-9]\d{9}$'},
        '+1': {'name': '美国', 'min_length': 10, 'max_length': 10, 'pattern': r'^\d{10}$'},
        '+44': {'name': '英国', 'min_length': 10, 'max_length': 11, 'pattern': r'^\d{10,11}$'},
    }

    @staticmethod
    def is_virtual_number(mobile: str) -> bool:
        """检查是否是虚拟号段"""
        if not mobile or len(mobile) < 3:
            return False
        prefix = mobile[:3]
        return prefix in VIRTUAL_PHONE_PREFIXES

    @staticmethod
    def validate_format(mobile: str) -> Tuple[bool, str]:
        """验证手机号格式（支持国际区号）"""
        if not mobile:
            return False, "手机号不能为空"

        # 去除所有非数字字符，保留纯数字
        digits = ''.join(filter(str.isdigit, mobile))
        
        if not digits:
            return False, "手机号不能为空"

        # 检查是否包含国际区号前缀
        country_code = None
        remaining = digits
        
        # 检查带+号的前缀（如 +86、+1、+44）
        if mobile.startswith('+'):
            for code in PhoneNumberValidator.COUNTRY_CODES:
                if mobile.startswith(code):
                    country_code = code
                    # 提取去掉区号后的数字部分
                    remaining = digits[len(code)-1:]  # code包含+号，所以减1
                    break
        
        # 根据国家代码进行验证
        if country_code == '+86':
            # 中国手机号：11位，以1开头，第二位3-9
            if len(remaining) != 11:
                return False, "中国手机号必须是11位"
            if not remaining.startswith('1'):
                return False, "手机号必须以1开头"
            second_digit = remaining[1]
            valid_second_digits = ['3', '4', '5', '6', '7', '8', '9']
            if second_digit not in valid_second_digits:
                return False, "手机号格式不正确"
            # 检查虚拟号段
            if PhoneNumberValidator.is_virtual_number(remaining):
                return False, "暂不支持虚拟运营商号码注册，请使用普通手机号"
        elif country_code == '+1':
            # 美国手机号：10位数字
            if len(remaining) != 10:
                return False, "美国手机号必须是10位数字"
        elif country_code == '+44':
            # 英国手机号：10位或11位（允许前导0）
            if len(remaining) not in [10, 11]:
                return False, "英国手机号应为10位或11位数字"
            # 如果是11位，必须以0开头
            if len(remaining) == 11 and not remaining.startswith('0'):
                return False, "英国11位手机号必须以0开头"
        else:
            # 默认：中国手机号格式（无前缀或其他未知前缀）
            if len(digits) != 11:
                return False, "手机号必须是11位"
            if not digits.startswith('1'):
                return False, "手机号必须以1开头"
            second_digit = digits[1]
            valid_second_digits = ['3', '4', '5', '6', '7', '8', '9']
            if second_digit not in valid_second_digits:
                return False, "手机号格式不正确"
            # 检查虚拟号段
            if PhoneNumberValidator.is_virtual_number(digits):
                return False, "暂不支持虚拟运营商号码注册，请使用普通手机号"

        return True, ""

    @staticmethod
    def validate(mobile: str) -> Tuple[bool, str]:
        """综合验证"""
        # 格式验证
        valid, msg = PhoneNumberValidator.validate_format(mobile)
        if not valid:
            return False, msg

        return True, ""


# 全局实例
_registration_limiter: Optional[RegistrationRateLimiter] = None


def get_registration_limiter() -> RegistrationRateLimiter:
    """获取全局注册限流器"""
    global _registration_limiter
    if _registration_limiter is None:
        _registration_limiter = RegistrationRateLimiter()
    return _registration_limiter


def check_registration_allowed(ip: str) -> Tuple[bool, str]:
    """检查是否允许注册（便捷函数）"""
    limiter = get_registration_limiter()
    return limiter.check(ip)


def validate_phone_number(mobile: str) -> Tuple[bool, str]:
    """验证手机号（便捷函数）"""
    return PhoneNumberValidator.validate(mobile)
