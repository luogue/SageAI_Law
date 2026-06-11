"""Alembic 环境配置 - 数据库迁移管理"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# 导入 project 的 SQLAlchemy models
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from storage.models import Base
from storage.database import SQLALCHEMY_DATABASE_URL

# Alembic Config 对象
config = context.config

# 设置日志
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 设置 target_metadata
target_metadata = Base.metadata

# 从环境变量覆盖数据库 URL
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)


def run_migrations_offline() -> None:
    """离线模式：生成 SQL 但不执行"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """在线模式：直接执行数据库迁移"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
