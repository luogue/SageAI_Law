"""数据库配置"""
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime, timezone, timedelta
import logging

logger = logging.getLogger(__name__)

# 设置中国时区
CHINA_TZ = timezone(timedelta(hours=8))

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

IS_SQLITE = "sqlite" in DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if IS_SQLITE else {}
)

# SQLite 性能优化 PRAGMA
if IS_SQLITE:
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")      # WAL 模式：并发读写性能更好
        cursor.execute("PRAGMA synchronous=NORMAL")     # 平衡安全与性能
        cursor.execute("PRAGMA cache_size=-64000")      # 64MB 缓存
        cursor.execute("PRAGMA busy_timeout=5000")      # 5秒忙等待超时
        cursor.execute("PRAGMA foreign_keys=ON")        # 启用外键约束
        cursor.close()
    logger.info("[DB] SQLite PRAGMA 优化已配置 (WAL/NORMAL/64MB缓存)")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 导出数据库 URL 供 Alembic 使用
SQLALCHEMY_DATABASE_URL = DATABASE_URL

Base = declarative_base()


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
