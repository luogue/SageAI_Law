#!/usr/bin/env python3
"""测试数据库查询和正则匹配"""
import sqlite3
import os

# 1. 测试数据库查询
print("=" * 60)
print("1. 数据库表查询")
print("=" * 60)

db_path = 'backend/data/app.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"数据库表: {tables}")
    
    # 查看所有表结构
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print(f"\n{table_name} 表结构:")
        for col in columns:
            print(f"  {col}")
    
    # 搜索记录
    print("\n搜索contract_reviews表中的记录:")
    cursor.execute("SELECT COUNT(*) FROM contract_reviews")
    count = cursor.fetchone()[0]
    print(f"contract_reviews 表共有 {count} 条记录")
    
    cursor.execute("SELECT task_id, created_at FROM contract_reviews ORDER BY created_at DESC LIMIT 10")
    rows = cursor.fetchall()
    for row in rows:
        print(f"  task_id: {row[0]}, created_at: {row[1]}")
    
    conn.close()
else:
    print(f"数据库文件不存在: {db_path}")

# 2. 测试正则匹配
print("\n" + "=" * 60)
print("2. 正则匹配测试")
print("=" * 60)

from backend.layers.output_layer import OutputLayer

test_raw_report = """<FINAL_REPORT>
**前置步骤：关键前提确认（强制执行）**  
本案合同属于房屋买卖合同，【法律关系性质】: 其他（买卖合同关系），关键审查前提是：1. 阴阳合同的效力认定需区分对外备案合同与对内真实合同；2. 需审查是否存在恶意串通损害国家利益情形；3. 合同签订时间及相关法律适用。

**1. 自上而下建逻辑结构**
### a. 第一步：抽象能力

---

**3. 风险评估与商业可行性评估**
- 风险点：阴阳合同效力不确定性
  - 发生概率：高
  - 影响程度：高
  - 综合风险等级：高
  - 修改建议：建议明确合同效力条款
  - 优先级：【强制】

---

**5. 结论与行动建议**
应该怎么做：建议当事人明确真实意思表示，避免签订阴阳合同。

为什么是这样：引用推理步骤，阴阳合同可能因违反强制性规定而无效。
</FINAL_REPORT>"""

output_layer = OutputLayer()
result = output_layer.process(test_raw_report)

print("处理结果:\n")
print(result)
print("\n" + "=" * 60)
print("章节验证:")
print("=" * 60)
print(f"审查前提存在: {'1. 审查前提' in result}")
print(f"风险评估存在: {'2. 风险评估' in result}")
print(f"结论与行动建议存在: {'3. 结论与行动建议' in result}")
print(f"风险内容存在: {'阴阳合同效力不确定性' in result}")
