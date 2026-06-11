"""生产环境配置管理 - 所有敏感信息从环境变量读取"""
import os
from dotenv import load_dotenv

load_dotenv()

# 运行环境
ENV = os.getenv("ENV", "development")
IS_PRODUCTION = ENV == "production"
IS_DEVELOPMENT = ENV == "development"

# ========== 数据库 ==========
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# ========== JWT & 认证 ==========
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))  # 默认24小时

# ========== 管理员 ==========
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "")

# ========== CORS ==========
CORS_ORIGINS_STR = os.getenv("CORS_ORIGINS", "http://localhost:5173")
CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS_STR.split(",") if origin.strip()]

# ========== HTTPS & 安全 ==========
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "false").lower() == "true"
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "false").lower() == "true"

# ========== 生产环境默认安全设置 ==========
if IS_PRODUCTION:
    if not JWT_SECRET_KEY:
        raise ValueError("生产环境必须设置 JWT_SECRET_KEY")
    if not ADMIN_TOKEN:
        raise ValueError("生产环境必须设置 ADMIN_TOKEN")

# ========== 日志 ==========
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = os.getenv("LOG_DIR", "./logs")
LOG_MAX_DAYS = int(os.getenv("LOG_MAX_DAYS", "30"))
LOG_FORMAT = os.getenv(
    "LOG_FORMAT",
    "%(asctime)s | %(levelname)s | rid=%(request_id)s | uid=%(user_id)s | "
    "ip=%(client_ip)s | %(message)s"
)

# ========== 请求限制 ==========
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "180"))
MAX_CONNECTIONS = int(os.getenv("MAX_CONNECTIONS", "100"))

# ========== Gzip ==========
GZIP_MIN_SIZE = int(os.getenv("GZIP_MIN_SIZE", "500"))

# ========== LLM 模型配置 ==========
# 千问 (Qwen / DashScope) - 首选模型
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-max")

# 火山方舟 (豆包/Doubao / Ark) - 次选模型
ARK_API_KEY = os.getenv("ARK_API_KEY", "")
ARK_ENDPOINT_ID = os.getenv("ARK_ENDPOINT_ID", "")

# DeepSeek - 备选模型
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

# 模型优先级（可选，逗号分隔，默认: qwen,doubao,deepseek）
LLM_PRIORITY = os.getenv("LLM_PRIORITY", "qwen,doubao,deepseek")

# 备用模型列表（兼容旧配置）
ALTERNATIVE_MODELS = os.getenv("ALTERNATIVE_MODELS", "")
