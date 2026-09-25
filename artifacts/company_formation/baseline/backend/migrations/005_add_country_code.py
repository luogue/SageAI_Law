"""数据库迁移：添加 country_code 字段"""
import sqlite3
import os

# 获取数据库路径
db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
db_path = os.path.abspath(db_path)

# 确保数据目录存在
os.makedirs(os.path.dirname(db_path), exist_ok=True)

def migrate():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 检查 country_code 字段是否已存在
        cursor.execute("PRAGMA table_info(user)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'country_code' not in columns:
            # 添加 country_code 字段
            cursor.execute("ALTER TABLE user ADD COLUMN country_code TEXT DEFAULT '+86'")
            print("✓ 已添加 country_code 字段")
            
            # 为现有记录设置默认值
            cursor.execute("UPDATE user SET country_code = '+86' WHERE country_code IS NULL")
            print("✓ 已为现有记录设置默认区号")
            
            conn.commit()
        else:
            print("✓ country_code 字段已存在")
            
    except Exception as e:
        print(f"✗ 迁移失败: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
    print("迁移完成")
