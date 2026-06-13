"""迁移脚本008 - 为record表添加raw_output字段"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import text
from storage.database import engine


def migrate():
    """执行数据库迁移：为record表添加raw_output字段"""
    print("开始数据库迁移 008 - 添加 raw_output 字段...")
    
    try:
        with engine.connect() as conn:
            # 检查字段是否已存在
            result = conn.execute(text("PRAGMA table_info(record)"))
            columns = [row[1] for row in result.fetchall()]
            
            if "raw_output" in columns:
                print("raw_output 字段已存在，跳过迁移")
                return
            
            # 添加 raw_output 字段
            conn.execute(text("ALTER TABLE record ADD COLUMN raw_output TEXT"))
            conn.commit()
            print("成功添加 raw_output 字段到 record 表")
            
    except Exception as e:
        print(f"迁移失败: {e}")
        raise


if __name__ == "__main__":
    migrate()