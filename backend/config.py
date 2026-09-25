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
from model_settings import configuration as model_configuration
DEEPSEEK_API_KEY = model_configuration()['key']
DEEPSEEK_MODEL = model_configuration()['model']

# ========== 法条校验配置 ==========
ENABLE_LEGAL_CHECK = os.getenv("ENABLE_LEGAL_CHECK", "true").lower() == "true"
PKULAW_API_KEY = os.getenv("PKULAW_API_KEY", "")
PKULAW_API_URL = os.getenv("PKULAW_API_URL", "https://api.pkulaw.com")
