"""数据库配置"""
from sqlalchemy import create_engine, event
from sqlalchemy.engine import make_url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime, timezone, timedelta
import logging
import sys
import tempfile
from pathlib import Path
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# 设置中国时区
CHINA_TZ = timezone(timedelta(hours=8))

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")


def validate_database_environment(url):
    """Fail closed before opening a database when invoked by tests."""
    parsed = make_url(url)
    testing = os.getenv("ENV", "").lower() == "test" or "pytest" in sys.modules
    if testing:
        root = Path(os.environ.get("SAGE_TEST_ROOT", "__missing_test_root__")).resolve()
        temp = Path(tempfile.gettempdir()).resolve()
        if not root.is_relative_to(temp) or not root.name.startswith("sageai-test-"):
            raise RuntimeError("Tests require a dedicated temporary SAGE_TEST_ROOT")
        if parsed.get_backend_name() != "sqlite" or not parsed.database:
            raise RuntimeError("Tests require an isolated file SQLite database")
        path = Path(parsed.database).resolve()
        if not path.is_relative_to(root) or path == root:
            raise RuntimeError("Test DATABASE_URL points outside SAGE_TEST_ROOT")
    if os.getenv("ENV", "").lower() == "production" and parsed.get_backend_name() == "sqlite":
        if not parsed.database or not Path(parsed.database).is_absolute():
            raise RuntimeError("Production SQLite requires an explicit absolute DATABASE_URL")
        if not Path(parsed.database).is_file() and os.getenv('ALLOW_DATABASE_INITIALIZE') != 'true':
            raise RuntimeError('Production database missing; refusing implicit empty initialization')


validate_database_environment(DATABASE_URL)

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
        try:
            cursor.execute("PRAGMA busy_timeout=5000")  # Also applies while selecting WAL mode.
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA synchronous=NORMAL")
            cursor.execute("PRAGMA cache_size=-64000")
            cursor.execute("PRAGMA foreign_keys=ON")
        finally:
            cursor.close()
    logger.info("[DB] SQLite PRAGMA 优化已配置 (WAL/NORMAL/64MB缓存)")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)

# 导出数据库 URL 供 Alembic 使用
SQLALCHEMY_DATABASE_URL = DATABASE_URL

Base = declarative_base()


@contextmanager
def session_scope():
    """One session per operation/thread; callers explicitly commit successful writes."""
    db = SessionLocal()
    try:
        yield db
    except BaseException:
        db.rollback()
        raise
    finally:
        # close() rolls back any uncommitted work, including early-return paths.
        db.close()


def get_db():
    """FastAPI yield dependency; non-dependency code must use session_scope()."""
    with session_scope() as db:
        yield db
