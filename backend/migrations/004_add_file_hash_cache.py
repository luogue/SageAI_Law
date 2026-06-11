"""数据库迁移脚本 - 添加文件哈希缓存表"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import os

# 获取数据库URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()


class FileHashCache(Base):
    """文件哈希缓存表 - 用于检测重复上传"""
    __tablename__ = "file_hash_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    file_hash = Column(String(64), nullable=False, index=True)
    filename = Column(String, nullable=True)
    first_upload_time = Column(DateTime(timezone=True), server_default=func.now())
    last_upload_time = Column(DateTime(timezone=True), server_default=func.now())
    upload_count = Column(Integer, default=1, nullable=False)


def migrate():
    """执行迁移"""
    print("开始创建 file_hash_cache 表...")
    Base.metadata.create_all(bind=engine, tables=[FileHashCache.__table__])
    print("file_hash_cache 表创建成功！")


if __name__ == "__main__":
    migrate()
