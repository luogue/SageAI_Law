import sqlite3

# 连接到数据库
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

try:
    # 检查并添加 user 表的 invited_by 字段
    cursor.execute("PRAGMA table_info(user)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'invited_by' not in columns:
        cursor.execute("ALTER TABLE user ADD COLUMN invited_by INTEGER")
        print("Added 'invited_by' column to user table")
    
    # 检查并添加 invite_rewards 表的新字段
    cursor.execute("PRAGMA table_info(invite_rewards)")
    invite_columns = [col[1] for col in cursor.fetchall()]
    
    if 'invitee_first_review_at' not in invite_columns:
        cursor.execute("ALTER TABLE invite_rewards ADD COLUMN invitee_first_review_at TEXT")
        print("Added 'invitee_first_review_at' column to invite_rewards table")
    
    if 'reward_granted_at' not in invite_columns:
        cursor.execute("ALTER TABLE invite_rewards ADD COLUMN reward_granted_at TEXT")
        print("Added 'reward_granted_at' column to invite_rewards table")
    
    conn.commit()
    print("Database migration completed successfully")
    
except Exception as e:
    print(f"Error during migration: {e}")
    conn.rollback()
finally:
    conn.close()
