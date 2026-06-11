"""
LLM 客户端封装：多模型支持，智能降级与重试

模型优先级（默认）：
    1. 千问 (Qwen)     —— DashScope API
    2. 火山方舟 (Doubao) —— Ark API
    3. DeepSeek          —— DeepSeek API

特性：
    - 指数退避重试（1s, 2s, 4s，最多3次/模型）
    - 不可重试错误立即切换模型（401 无效密钥、429 配额不足、4xx 参数错误）
    - 所有模型失败后返回兜底文本
    - 熔断器保护（跨模型共享）
    - 可通过 LLM_PRIORITY 环境变量自定义模型顺序
"""
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

# ========== 模型配置 ==========
# 注意：以下所有配置均可通过环境变量覆盖
MODEL_DEFINITIONS = {
    "qwen": {
        "name": "千问(Qwen)",
        "provider": "dashscope",
        "api_key_env": "DASHSCOPE_API_KEY",
        "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        "model": os.getenv("QWEN_MODEL", "qwen-max"),
        "max_tokens": 4096,
        "temperature": 0.1,
    },
    "doubao": {
        "name": "火山方舟(Doubao)",
        "provider": "ark",
        "api_key_env": "ARK_API_KEY",
        "url": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
        "model": os.getenv("ARK_ENDPOINT_ID", "doubao-pro-32k"),
        "max_tokens": 4096,
        "temperature": 0.1,
    },
    "deepseek": {
        "name": "DeepSeek",
        "provider": "deepseek",
        "api_key_env": "DEEPSEEK_API_KEY",
        "url": "https://api.deepseek.com/v1/chat/completions",
        "model": "deepseek-chat",
        "max_tokens": 4096,
        "temperature": 0.1,
    },
}

# 默认模型优先级：千问 -> 豆包 -> DeepSeek
DEFAULT_PRIORITY = ["qwen", "doubao", "deepseek"]

# 从环境变量读取自定义优先级（可选）
# 格式: LLM_PRIORITY=qwen,doubao,deepseek （逗号分隔）
_priority_env = os.getenv("LLM_PRIORITY", "").strip()
if _priority_env:
    LLM_PRIORITY = [p.strip().lower() for p in _priority_env.split(",") if p.strip()]
    # 验证所有指定的模型都在定义中
    for p in LLM_PRIORITY:
        if p not in MODEL_DEFINITIONS:
            logger.warning(f"[LLM] 未知的模型标识: '{p}'，将忽略。可用: {list(MODEL_DEFINITIONS.keys())}")
            LLM_PRIORITY.remove(p)
    if not LLM_PRIORITY:
        LLM_PRIORITY = DEFAULT_PRIORITY
        logger.warning("[LLM] LLM_PRIORITY 配置无效，使用默认顺序")
    else:
        logger.info(f"[LLM] 使用自定义模型优先级: {LLM_PRIORITY}")
else:
    LLM_PRIORITY = DEFAULT_PRIORITY

# 重试配置
MAX_RETRIES_PER_MODEL = 3  # 每个模型最多重试次数
RETRY_BACKOFF_BASE = 1      # 初始等待秒数
RETRY_BACKOFF_MULTIPLIER = 2  # 指数倍增因子

# 兜底消息
FALLBACK_MESSAGE = "大模型服务暂时不可用，请稍后再试。"

# ========== 可重试异常判断 ==========

def _is_retryable_error(response_or_error) -> bool:
    """
    判断是否可重试
    可重试: 网络超时、连接错误、5xx 状态码
    不可重试: 401(无效密钥)、429(配额不足)、4xx(参数错误)、非网络异常
    """
    if isinstance(response_or_error, requests.exceptions.Timeout):
        return True
    if isinstance(response_or_error, requests.exceptions.ConnectionError):
        return True
    if isinstance(response_or_error, requests.exceptions.RequestException):
        # 其他网络异常也可重试
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
        return f"网络异常: {str(response_or_error)[:100]}"
    if isinstance(response_or_error, ValueError):
        return f"响应格式错误: {str(response_or_error)[:100]}"
    return f"未知错误: {str(response_or_error)[:100]}"


def _get_model_config(model_id: str) -> Optional[Dict]:
    """获取模型配置"""
    return MODEL_DEFINITIONS.get(model_id)


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
    for model_id in LLM_PRIORITY:
        config = _get_model_config(model_id)
        if config is None:
            continue
        if not _has_api_key(config):
            logger.info(f"[LLM] {config['name']} 未配置 API Key (环境变量 {config['api_key_env']})，跳过")
            continue
        available.append((model_id, config))
    
    if not available:
        logger.error("[LLM] 没有配置任何可用的模型 API Key！所有调用将返回兜底消息。")
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
    """
    调用 LLM API（多模型优先级 + 智能降级 + 重试）
    
    调用流程：
        1. 按优先级依次尝试每个可用模型
        2. 每个模型最多重试 max_retries 次（指数退避）
        3. 遇到不可重试错误（401/429/4xx）立即切换模型
        4. 所有模型均失败则返回兜底消息
    
    :param prompt: 提示词
    :param response_format: 响应格式，"json"或"text"
    :param max_retries: 每个模型最大重试次数
    :return: API 响应内容（或兜底消息）
    :raises AllModelsFailedError: 所有模型均失败
    :raises CircuitBreakerOpenError: 熔断器打开
    """
    # ========== 熔断器检查 ==========
    if not circuit_breaker.allow_request():
        logger.warning("[CircuitBreaker] 请求被熔断拦截")
        raise CircuitBreakerOpenError("服务暂时不可用，AI 请求过于频繁或出现临时故障，请稍后重试")

    # ========== 构建可用模型列表 ==========
    available_models = _build_available_models()
    if not available_models:
        logger.error("[LLM] 没有可用的模型，直接返回兜底消息")
        circuit_breaker.record_failure()
        raise AllModelsFailedError(FALLBACK_MESSAGE)

    # ========== JSON 格式包装 ==========
    if response_format == "json":
        prompt = f"""\
你现在是一个JSON格式输出助手。请严格按照JSON格式输出，不要添加任何额外内容。

:{prompt}

请输出严格的JSON格式，不要包含任何JSON以外的文本。
"""

    # ========== [调试] 打印完整prompt ==========
    try:
        print("\n" + "=" * 120)
        print("[DEBUG] 即将调用 LLM API，完整prompt内容如下：")
        print("=" * 120)
        import sys
        sys.stdout.buffer.write((prompt[:2000] + "..." if len(prompt) > 2000 else prompt).encode('utf-8'))
        print("")
        print("=" * 120)
        print(f"[DEBUG] prompt长度: {len(prompt)} 字符")
        print(f"[DEBUG] 可用模型: {[cfg['name'] for _, cfg in available_models]}")
        print("=" * 120 + "\n")
    except Exception as e:
        logger.error(f"[DEBUG] 打印prompt失败: {e}")

    # ========== 按优先级依次尝试模型 ==========
    all_errors = []  # 记录所有模型的所有错误

    for model_idx, (model_id, model_config) in enumerate(available_models):
        model_name = model_config["name"]
        api_key = os.getenv(model_config["api_key_env"], "").strip()
        url = model_config["url"]
        model_str = model_config["model"]

        logger.info(f"[LLM] ===== 尝试模型 [{model_idx + 1}/{len(available_models)}]: {model_name} ({model_str}) =====")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        data = {
            "model": model_str,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": model_config.get("max_tokens", 4096),
            "temperature": model_config.get("temperature", 0.1),
            "top_p": 0.95,
            "stream": False
        }

        # ========== 单模型重试循环（指数退避） ==========
        last_error = None
        model_success = False

        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    wait_seconds = RETRY_BACKOFF_BASE * (RETRY_BACKOFF_MULTIPLIER ** (attempt - 1))
                    logger.info(f"[LLM] {model_name} 第 {attempt + 1}/{max_retries} 次尝试，等待 {wait_seconds} 秒...")
                    time.sleep(wait_seconds)

                response = requests.post(url, headers=headers, json=data, timeout=180)

                if response.status_code == 200:
                    result = response.json()
                    content = _extract_content(result)
                    if content:
                        circuit_breaker.record_success()
                        logger.info(f"[LLM] ✅ {model_name} 调用成功（第 {attempt + 1} 次尝试），"
                                    f"返回长度: {len(content)} 字符")
                        return content
                    else:
                        raise ValueError(f"API 响应中未找到有效内容: {json.dumps(result, ensure_ascii=False)[:500]}")

                # HTTP 非 200 响应
                error_msg = f"HTTP {response.status_code}: {response.text[:300]}"
                logger.error(f"[LLM] {model_name} 返回错误（第 {attempt + 1} 次尝试）: {error_msg}")
                
                # 判断是否可重试
                if _is_retryable_for_status(response.status_code):
                    last_error = requests.exceptions.HTTPError(
                        error_msg, response=response
                    )
                    continue  # 重试
                else:
                    # 不可重试的 HTTP 错误（401, 429, 4xx）→ 立即切换模型
                    http_err = requests.exceptions.HTTPError(error_msg, response=response)
                    logger.warning(
                        f"[LLM] ❌ {model_name} 返回不可重试错误 "
                        f"({_get_error_category(http_err)})，"
                        f"立即切换模型"
                    )
                    all_errors.append(f"[{model_name}] {_get_error_category(http_err)}: {error_msg}")
                    model_success = False
                    break  # 跳出重试循环，进入下一个模型

            except requests.exceptions.Timeout as e:
                last_error = e
                error_cat = _get_error_category(e)
                logger.warning(f"[LLM] {model_name} {error_cat}（第 {attempt + 1}/{max_retries} 次尝试）")
                if attempt < max_retries - 1:
                    continue  # 可重试
                all_errors.append(f"[{model_name}] {error_cat}（{max_retries}次重试后失败）")

            except requests.exceptions.ConnectionError as e:
                last_error = e
                error_cat = _get_error_category(e)
                logger.warning(f"[LLM] {model_name} {error_cat}（第 {attempt + 1}/{max_retries} 次尝试）")
                if attempt < max_retries - 1:
                    continue  # 可重试
                all_errors.append(f"[{model_name}] {error_cat}（{max_retries}次重试后失败）")

            except requests.exceptions.RequestException as e:
                last_error = e
                error_cat = _get_error_category(e)
                
                if _is_retryable_error(e):
                    logger.warning(f"[LLM] {model_name} {error_cat}（第 {attempt + 1}/{max_retries} 次尝试）")
                    if attempt < max_retries - 1:
                        continue  # 可重试
                    all_errors.append(f"[{model_name}] {error_cat}（{max_retries}次重试后失败）")
                else:
                    # 不可重试 → 立即切换
                    logger.warning(f"[LLM] ❌ {model_name} {error_cat}，不可重试，立即切换模型")
                    all_errors.append(f"[{model_name}] {error_cat}")
                    model_success = False
                    break

            except ValueError as e:
                last_error = e
                logger.warning(f"[LLM] {model_name} {_get_error_category(e)}（第 {attempt + 1}/{max_retries} 次尝试）")
                if attempt < max_retries - 1:
                    continue
                all_errors.append(f"[{model_name}] {_get_error_category(e)}（{max_retries}次重试后失败）")

        # 当前模型的所有重试都失败了
        if not model_success:
            logger.warning(
                f"[LLM] ❌ {model_name} 不可用（{'不可重试错误' if last_error and not _is_retryable_error(last_error) else f'{max_retries}次重试后失败'}），"
                f"切换到下一个模型"
            )

    # ========== 所有模型均失败 ==========
    circuit_breaker.record_failure()
    
    error_summary = "; ".join(all_errors) if all_errors else "未知错误"
    logger.error(f"[LLM] ❌❌❌ 所有模型均失败！错误汇总: {error_summary}")
    logger.error(f"[LLM] 🔄 返回兜底消息: {FALLBACK_MESSAGE}")
    
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
    支持多种 API 响应格式（OpenAI 兼容、DashScope 等）
    """
    # OpenAI 兼容格式
    if "choices" in response_json and len(response_json["choices"]) > 0:
        choice = response_json["choices"][0]
        if "message" in choice and "content" in choice["message"]:
            return choice["message"]["content"].strip()
        if "text" in choice:
            return choice["text"].strip()

    # DashScope 旧版格式
    if "output" in response_json:
        output = response_json["output"]
        if "choices" in output and len(output["choices"]) > 0:
            choice = output["choices"][0]
            if "message" in choice and "content" in choice["message"]:
                return choice["message"]["content"].strip()
        if "text" in output:
            return output["text"].strip()

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
