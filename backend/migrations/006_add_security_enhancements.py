"""数据库迁移：添加安全增强字段 - blacklist扩展 + admin_logs + security_events"""
import sqlite3
import os
import sys



def migrate():
    from storage.database import engine
    if engine.dialect.name != "sqlite":
        return
    db_path = engine.url.database
    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}，跳过迁移（将在应用启动时由 SQLAlchemy 自动创建）")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # ========== 1. 扩展 blacklist 表 ==========
        blacklist_cols = [
            ("ban_type", "TEXT DEFAULT 'manual'"),
            ("input_preview", "TEXT"),
            ("trigger_rule", "TEXT"),
            ("is_unbanned", "INTEGER DEFAULT 0"),
            ("unbanned_by", "TEXT"),
            ("unban_reason", "TEXT"),
            ("unbanned_at", "TIMESTAMP"),
        ]
        try:
            cursor.execute("PRAGMA table_info(blacklist)")
            existing_blacklist_cols = [col[1] for col in cursor.fetchall()]
            for col_name, col_def in blacklist_cols:
                if col_name not in existing_blacklist_cols:
                    cursor.execute(f"ALTER TABLE blacklist ADD COLUMN {col_name} {col_def}")
                    print(f"  OK blacklist: added {col_name}")
        except sqlite3.OperationalError as e:
            print(f"  SKIP blacklist: {e} (table will be created by SQLAlchemy)")

        # ========== 2. 创建 admin_logs 表 ==========
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_user VARCHAR(50) NOT NULL,
                action VARCHAR(50) NOT NULL,
                target_type VARCHAR(50) NOT NULL,
                target_value VARCHAR(200) NOT NULL,
                detail TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_admin_logs_created ON admin_logs(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_admin_logs_admin ON admin_logs(admin_user)")
        print("  OK created admin_logs table")

        # ========== 3. 创建 security_events 表 ==========
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS security_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type VARCHAR(50) NOT NULL,
                severity VARCHAR(20) NOT NULL DEFAULT 'warning',
                source VARCHAR(50) NOT NULL DEFAULT 'system',
                detail TEXT,
                user_id VARCHAR(50),
                ip VARCHAR(45),
                meta_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_security_events_type ON security_events(event_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_security_events_created ON security_events(created_at)")
        print("  OK created security_events table")

        conn.commit()
        print("\nMigration completed successfully!")
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    migrate()
