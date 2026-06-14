#!/usr/bin/env python3
"""检查所有数据库中的任务记录"""
import sqlite3
import os

def check_all_databases():
    db_paths = [
        'backend/app.db',
        'backend/data/app.db',
        'backend/data/blacklist.db',
        'backend/security/intercept_logs.db'
    ]
    
    print("=" * 60)
    print("检查所有数据库文件")
    print("=" * 60)
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            print(f"\n[{db_path}]")
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                print(f"  表列表: {[t[0] for t in tables]}")
                
                # 检查tasks或contract_reviews表
                for table in ['tasks', 'contract_reviews']:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"  {table} 表记录数: {count}")
                    
                    # 显示最近的记录
                    cursor.execute(f"SELECT task_id, filename FROM {table} ORDER BY id DESC LIMIT 5")
                    rows = cursor.fetchall()
                    if rows:
                        print(f"  最近的task_id:")
                        for row in rows:
                            print(f"    - {row[0]} ({row[1]})")
                
                conn.close()
            except Exception as e:
                print(f"  错误: {e}")
        else:
            print(f"\n[{db_path}] - 文件不存在")

if __name__ == '__main__':
    check_all_databases()
