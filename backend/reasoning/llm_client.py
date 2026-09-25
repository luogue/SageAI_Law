"""DeepSeek client with bounded retries and circuit protection; no provider fallback."""
import os
import json
import requests
import logging
import time
import threading
from typing import Optional, List, Dict, Tuple

# ========== 日志配置 ==========
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== 熔断器配置 ==========
CIRCUIT_BREAKER_THRESHOLD = int(os.getenv('CIRCUIT_BREAKER_THRESHOLD', '3'))
CIRCUIT_BREAKER_TIMEOUT = int(os.getenv('CIRCUIT_BREAKER_TIMEOUT_SECONDS', '30'))

from model_settings import MODEL_DEFINITIONS, configuration
from secret_redaction import redact_secrets

# 重试配置
MAX_RETRIES_PER_MODEL = 1   # 仅对瞬时网络错误重试1次（总耗时<5秒）
RETRY_BACKOFF_BASE = 1      # 初始等待秒数
RETRY_BACKOFF_MULTIPLIER = 2  # 指数倍增因子

# API 调用超时配置（分离连接和读取超时）
API_CONNECT_TIMEOUT = 5      # 连接超时（秒）- 短超时，快速检测网络闪断
API_READ_TIMEOUT = 180       # 读取响应超时（秒），模型推理可能需要较长时间
API_TOTAL_TIMEOUT = 180      # 单次请求总超时（秒）

# 兜底消息
FALLBACK_MESSAGE = "大模型服务暂时不可用，请稍后再试。"

# ========== 可重试异常判断 ==========

def _is_retryable_error(response_or_error) -> bool:
    """
    判断是否可重试
    可重试: 连接超时(ConnectTimeout)、连接错误(ConnectionError)、5xx 状态码
    不可重试: 读取超时(ReadTimeout)-模型处理慢时停止调用、401(无效密钥)、429(配额不足)、4xx(参数错误)
    """
    if isinstance(response_or_error, requests.exceptions.ConnectTimeout):
        return True  # 连接超时-网络闪断，可重试
    if isinstance(response_or_error, requests.exceptions.ReadTimeout):
        return False  # 读取超时-模型处理慢，不可重试，停止调用
    if isinstance(response_or_error, requests.exceptions.Timeout):
        return False  # 通用Timeout默认不可重试（应具体区分）
    if isinstance(response_or_error, requests.exceptions.ConnectionError):
        return True  # 连接错误，可重试
    if isinstance(response_or_error, requests.exceptions.RequestException):
        if hasattr(response_or_error, 'response') and response_or_error.response is not None:
            status = response_or_error.response.status_code
            if 500 <= status < 600:
                return True
            # 4xx 不可重试（包括401, 429, 400, 403等）
            return False
        return True  # 没有response的网络异常，重试
    return False


def _get_error_category(response_or_error) -> str:
    """获取错误分类描述（用于日志）"""
    if isinstance(response_or_error, requests.exceptions.ConnectTimeout):
        return "连接超时"
    if isinstance(response_or_error, requests.exceptions.ReadTimeout):
        return "读取超时(模型处理慢)"
    if isinstance(response_or_error, requests.exceptions.Timeout):
        return "网络超时"
    if isinstance(response_or_error, requests.exceptions.ConnectionError):
        return "连接错误"
    if isinstance(response_or_error, requests.exceptions.RequestException):
        if hasattr(response_or_error, 'response') and response_or_error.response is not None:
            status = response_or_error.response.status_code
            if status == 401:
                return f"无效密钥(401)"
            if status == 429:
                return f"配额不足/限流(429)"
            if 400 <= status < 500:
                return f"请求参数错误({status})"
            if 500 <= status < 600:
                return f"服务器错误({status})"
        return f"网络异常: {type(response_or_error).__name__}"
    if isinstance(response_or_error, ValueError):
        return f"响应格式错误: {type(response_or_error).__name__}"
    return f"未知错误: {type(response_or_error).__name__}"


def _current_llm_priority() -> List[str]:
    return ['deepseek']


def _get_model_config(model_id: str) -> Optional[Dict]:
    """获取模型配置"""
    config = MODEL_DEFINITIONS.get(model_id)
    if not config:
        return None
    resolved = dict(config)
    model_env = resolved.get("model_env")
    default_model = resolved.get("default_model")
    resolved["model"] = os.getenv(model_env, default_model).strip() if model_env else default_model
    return resolved


def _has_api_key(model_config: Dict) -> bool:
    """检查是否配置了API密钥"""
    key = os.getenv(model_config["api_key_env"], "").strip()
    return bool(key)


def _build_available_models() -> List[Tuple[str, Dict]]:
    """
    按优先级构建可用的模型列表
    返回: [(model_id, model_config), ...]
    """
    available = []
    for model_id in _current_llm_priority():
        config = _get_model_config(model_id)
        if config is None:
            continue
        if not _has_api_key(config):
            logger.info(f"[LLM] {config['name']} 未配置 API Key (环境变量 {config['api_key_env']})，跳过")
            continue
        available.append((model_id, config))
    
    if not available:
        logger.error("[LLM] 没有配置任何可用的模型 API Key！调用将报告服务不可用。")
    else:
        names = [cfg['name'] for _, cfg in available]
        logger.info(f"[LLM] 可用模型（按优先级）: {names}")
    
    return available


# ========== 熔断器 ==========

class CircuitBreaker:
    """熔断器实现"""
    
    def __init__(self, threshold: int = 3, timeout: int = 30):
        self.threshold = threshold
        self.timeout = timeout
        
        self.STATE_CLOSED = "closed"
        self.STATE_OPEN = "open"
        self.STATE_HALF_OPEN = "half_open"
        
        self._state = self.STATE_CLOSED
        self._failure_count = 0
        self._last_failure_time = None
        self._lock = threading.Lock()
        
        logger.info(f"[CircuitBreaker] 熔断器初始化 - 阈值:{threshold}次, 超时:{timeout}秒")
    
    @property
    def state(self) -> str:
        with self._lock:
            if self._state == self.STATE_OPEN:
                if self._last_failure_time and (time.time() - self._last_failure_time) >= self.timeout:
                    self._state = self.STATE_HALF_OPEN
                    logger.info("[CircuitBreaker] 熔断超时，进入半开状态")
            return self._state
    
    def allow_request(self) -> bool:
        return self.state != self.STATE_OPEN
    
    def record_success(self):
        with self._lock:
            if self._state == self.STATE_HALF_OPEN:
                self._reset()
                logger.info("[CircuitBreaker] 半开状态下请求成功，熔断器关闭")
            elif self._state == self.STATE_CLOSED:
                self._failure_count = 0
    
    def record_failure(self):
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()
            
            if self._state == self.STATE_HALF_OPEN:
                self._state = self.STATE_OPEN
                logger.warning("[CircuitBreaker] 半开状态下请求失败，重新进入熔断状态")
            elif self._state == self.STATE_CLOSED:
                if self._failure_count >= self.threshold:
                    self._state = self.STATE_OPEN
                    logger.warning(f"[CircuitBreaker] 连续失败{self._failure_count}次，触发熔断")
    
    def _reset(self):
        self._state = self.STATE_CLOSED
        self._failure_count = 0
        self._last_failure_time = None
    
    def get_status(self) -> dict:
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "threshold": self.threshold,
                "timeout": self.timeout
            }


# 全局熔断器实例
circuit_breaker = CircuitBreaker(
    threshold=CIRCUIT_BREAKER_THRESHOLD,
    timeout=CIRCUIT_BREAKER_TIMEOUT
)


# ========== 异常定义 ==========

class CircuitBreakerOpenError(Exception):
    """熔断器打开异常"""
    pass


class AllModelsFailedError(Exception):
    """所有模型均失败异常"""
    def __init__(self, message: str = FALLBACK_MESSAGE):
        self.fallback_message = message
        super().__init__(message)


# ========== 核心调用函数 ==========

def call_llm(prompt: str, response_format: str = "text", max_retries: int = 3) -> str:
    """Call DeepSeek only. Failures raise; no provider substitution."""
    if not circuit_breaker.allow_request():
        raise CircuitBreakerOpenError("服务暂时不可用，请稍后重试")
    config = configuration()
    if not config['key']:
        circuit_breaker.record_failure()
        raise AllModelsFailedError(FALLBACK_MESSAGE)
    if response_format == 'json':
        prompt = '请严格输出JSON，不要添加额外内容。\n' + prompt
    data = {'model': config['model'], 'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 8192, 'temperature': 0.1, 'top_p': 0.95, 'stream': False}
    attempts = max(1, max_retries)
    for attempt in range(attempts):
        if attempt:
            time.sleep(RETRY_BACKOFF_BASE * RETRY_BACKOFF_MULTIPLIER ** (attempt - 1))
        try:
            response = requests.post(config['url'],
                headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + config['key']},
                json=data, timeout=(API_CONNECT_TIMEOUT, API_READ_TIMEOUT))
            if response.status_code != 200:
                # Provider error bodies may echo credentials; never publish them.
                logger.warning('[LLM] DeepSeek HTTP %s', response.status_code)
                if _is_retryable_for_status(response.status_code):
                    continue
                break
            content = _extract_content(response.json())
            if not content:
                raise ValueError('Missing response content')
            circuit_breaker.record_success()
            logger.info('[LLM] DeepSeek succeeded model=%s', redact_secrets(config['model']))
            return redact_secrets(content)
        except requests.RequestException as exc:
            logger.warning('[LLM] DeepSeek request failed: %s', type(exc).__name__)
            if not _is_retryable_error(exc):
                break
        except (ValueError, TypeError, AttributeError):
            logger.warning('[LLM] DeepSeek returned an invalid response')
    circuit_breaker.record_failure()
    raise AllModelsFailedError(FALLBACK_MESSAGE)


def _is_retryable_for_status(status_code: int) -> bool:
    """判断 HTTP 状态码是否可重试"""
    if 500 <= status_code < 600:
        return True  # 5xx 服务器错误可重试
    if status_code == 429:
        return False  # 429 限流不可重试（配额不足）
    if 400 <= status_code < 500:
        return False  # 4xx 不可重试
    return False


def _extract_content(response_json: dict) -> Optional[str]:
    """
    从 API 响应中提取文本内容
    解析当前 API 的响应格式
    """
    # OpenAI 兼容格式
    if "choices" in response_json and len(response_json["choices"]) > 0:
        choice = response_json["choices"][0]
        if "message" in choice and "content" in choice["message"]:
            return choice["message"]["content"].strip()
        if "text" in choice:
            return choice["text"].strip()

    # 直接文本字段
    if "content" in response_json:
        return response_json["content"].strip()
    if "text" in response_json:
        return response_json["text"].strip()

    return None


# ========== 辅助函数 ==========

def validate_json_output(output: str, required_fields: list) -> bool:
    """
    验证JSON输出格式是否正确
    
    :param output: JSON字符串
    :param required_fields: 必需字段列表
    :return: 是否有效
    """
    try:
        data = json.loads(output)
        for field in required_fields:
            if field not in data:
                return False
        return True
    except json.JSONDecodeError:
        return False


def get_circuit_breaker_status() -> dict:
    """获取熔断器状态（供外部监控使用）"""
    return circuit_breaker.get_status()
