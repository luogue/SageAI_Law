"""生产级日志配置：按天滚动，保留30天，结构化格式"""
import os
import logging
from secret_redaction import SecretFormatter
import logging.handlers
import uuid
from datetime import datetime

LOG_DIR = os.getenv("LOG_DIR", "./logs")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_MAX_DAYS = int(os.getenv("LOG_MAX_DAYS", "30"))


class RequestIdFilter(logging.Filter):
    """为每条日志添加 request_id"""
    def filter(self, record):
        import contextvars
        request_id_var = contextvars.ContextVar('request_id', default='-')
        user_id_var = contextvars.ContextVar('user_id', default='-')
        client_ip_var = contextvars.ContextVar('client_ip', default='-')

        record.request_id = request_id_var.get()
        record.user_id = user_id_var.get()
        record.client_ip = client_ip_var.get()
        return True


def setup_logging():
    """配置生产级日志系统"""
    os.makedirs(LOG_DIR, exist_ok=True)

    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)

    # 文件处理器：按天滚动
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=os.path.join(LOG_DIR, "sageai.log"),
        when="midnight",
        interval=1,
        backupCount=LOG_MAX_DAYS,
        encoding="utf-8"
    )
    file_handler.setLevel(level)
    file_formatter = SecretFormatter(
        "%(asctime)s | %(levelname)-8s | rid=%(request_id)s | "
        "uid=%(user_id)s | ip=%(client_ip)s | "
        "%(name)s:%(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.addFilter(RequestIdFilter())

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_formatter = SecretFormatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)

    # 错误文件单独记录
    error_handler = logging.handlers.TimedRotatingFileHandler(
        filename=os.path.join(LOG_DIR, "error.log"),
        when="midnight",
        interval=1,
        backupCount=LOG_MAX_DAYS,
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    error_handler.addFilter(RequestIdFilter())

    # 配置根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(error_handler)

    # 降低第三方库日志级别
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

    logging.info(f"[LOGGING] 日志系统已初始化 - 级别:{LOG_LEVEL}, 目录:{LOG_DIR}, 保留:{LOG_MAX_DAYS}天")
    return root_logger


# 请求追踪中间件使用的 context vars
request_id_var = None
user_id_var = None
client_ip_var = None


def _init_context_vars():
    """延迟初始化 context vars"""
    import contextvars
    global request_id_var, user_id_var, client_ip_var
    request_id_var = contextvars.ContextVar('request_id', default='-')
    user_id_var = contextvars.ContextVar('user_id', default='-')
    client_ip_var = contextvars.ContextVar('client_ip', default='-')


_init_context_vars()
