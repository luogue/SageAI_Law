#!/usr/bin/env python3
"""检查task_record表中的记录"""
import sqlite3

conn = sqlite3.connect('backend/app.db')
cursor = conn.cursor()

# 查看task_record表结构
cursor.execute("PRAGMA table_info(task_record)")
columns = cursor.fetchall()
print("task_record 表结构:")
for col in columns:
    print(f"  {col}")

# 统计记录数
cursor.execute("SELECT COUNT(*) FROM task_record")
count = cursor.fetchone()[0]
print(f"\ntask_record 表共有 {count} 条记录")

# 显示所有记录
cursor.execute("SELECT * FROM task_record ORDER BY created_at DESC")
rows = cursor.fetchall()
print("\n所有任务记录:")
for row in rows:
    print(f"\n任务ID: {row[1]}")
    print(f"  文件名: {row[2]}")
    print(f"  状态: {row[3]}")
    print(f"  创建时间: {row[6]}")

# 搜索用户提供的task_id
target_task_id = 'cbe57f96-7856-448d-b494-dff19c6ad1a2'
cursor.execute("SELECT * FROM task_record WHERE task_id = ?", (target_task_id,))
result = cursor.fetchone()
print(f"\n搜索 task_id={target_task_id}:")
if result:
    print(f"找到记录: {result}")
else:
    print("未找到记录")

conn.close()
