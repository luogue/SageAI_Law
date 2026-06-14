#!/usr/bin/env python3
"""查找指定task_id的记录"""
import sqlite3
import os

def find_task(task_id):
    db_paths = [
        'backend/app.db',
        'backend/data/app.db',
    ]
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # 查询tasks表
                cursor.execute('SELECT * FROM tasks WHERE task_id = ?', (task_id,))
                result = cursor.fetchone()
                if result:
                    print(f"在 {db_path} 的 tasks 表中找到记录:")
                    print(result)
                    return
                
                # 查询contract_reviews表
                cursor.execute('SELECT * FROM contract_reviews WHERE task_id = ?', (task_id,))
                result = cursor.fetchone()
                if result:
                    print(f"在 {db_path} 的 contract_reviews 表中找到记录:")
                    print(result)
                    return
                
                conn.close()
            except Exception as e:
                print(f"查询 {db_path} 时出错: {e}")
    
    print(f"未找到 task_id: {task_id}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        find_task(sys.argv[1])
    else:
        print("请提供task_id作为参数")
