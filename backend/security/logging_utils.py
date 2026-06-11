"""日志与监控模块 - 脱敏处理"""
import os
import json
import time
import logging
import contextvars
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict

# 全局trace_id上下文变量
trace_id_context = contextvars.ContextVar('trace_id', default='unknown')


class TraceIdFilter(logging.Filter):
    """日志过滤器：自动注入trace_id"""
    
    def filter(self, record):
        record.trace_id = trace_id_context.get()
        return True


# 日志目录
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


class LogDesensitizer:
    """日志脱敏工具"""

    @staticmethod
    def mask_text(text: str, max_preview: int = 100) -> str:
        """隐藏合同和报告内容"""
        if not text:
            return ""
        return f"[content-length={len(text)}]"

    @staticmethod
    def mask_prompt(text: str) -> str:
        """隐藏系统提示词"""
        return "[system-prompt-hidden]"

    @staticmethod
    def mask_ip(ip: str) -> str:
        """部分隐藏IP地址"""
        if not ip or ip == "unknown":
            return "unknown"
        parts = ip.split(".")
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.xxx.xxx"
        return ip[:3] + "xxx"

    @staticmethod
    def mask_mobile(mobile: str) -> str:
        """隐藏手机号"""
        if not mobile or len(mobile) < 11:
            return "***"
        return f"{mobile[:3]}****{mobile[-4:]}"


desensitizer = LogDesensitizer()


def setup_logging():
    """配置日志"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 清除现有处理器
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # 日志格式 - 包含trace_id
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - [%(trace_id)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(TraceIdFilter())
    logger.addHandler(console_handler)

    # 文件输出 - 按天滚动
    today = datetime.now().strftime("%Y-%m-%d")
    file_handler = RotatingFileHandler(
        LOG_DIR / f"app_{today}.log",
        maxBytes=50 * 1024 * 1024,
        backupCount=30,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(TraceIdFilter())
    logger.addHandler(file_handler)


setup_logging()


class StructuredLogger:
    """结构化日志记录器"""

    def __init__(self):
        self.logger = logging.getLogger("sageai")

    def log_request(
        self,
        request_id: str,
        user_id: str,
        ip: str,
        path: str,
        method: str,
        duration: float,
        status_code: int,
        error: Optional[str] = None
    ):
        """记录请求日志"""
        data = {
            "type": "request",
            "request_id": request_id,
            "user_id": desensitizer.mask_ip(user_id) if user_id else "anonymous",
            "ip": desensitizer.mask_ip(ip),
            "path": path,
            "method": method,
            "duration_ms": round(duration * 1000, 2),
            "status_code": status_code,
            "error": error[:200] if error else None
        }
        self.logger.info(json.dumps(data, ensure_ascii=False))

    def log_security(self, event: str, ip: str = None, user_id: str = None, reason: str = None):
        """记录安全事件"""
        data = {
            "type": "security",
            "event": event,
            "ip": desensitizer.mask_ip(ip) if ip else None,
            "user_id": desensitizer.mask_ip(user_id) if user_id else None,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.warning(json.dumps(data, ensure_ascii=False))

    def log_audit(self, event: str, user_id: str = None, details: str = None):
        """记录审计事件"""
        data = {
            "type": "audit",
            "event": event,
            "user_id": desensitizer.mask_ip(user_id) if user_id else None,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(json.dumps(data, ensure_ascii=False))

    def log_error(self, msg: str, exc_info=None):
        """记录错误"""
        self.logger.error(msg, exc_info=exc_info)


# 全局日志实例
structured_logger = StructuredLogger()
