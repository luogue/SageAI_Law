#!/usr/bin/env python3
"""测试正则匹配修复"""
from backend.layers.output_layer import OutputLayer

# 使用原始报告内容测试
test_content = """<FINAL_REPORT>
**前置步骤：关键前提确认（强制执行）**  
本案合同属于房屋买卖合同，【法律关系性质】: 其他（买卖合同关系），关键审查前提是：1. 阴阳合同的效力认定需区分对外备案合同与对内真实合同；2. 需审查是否存在恶意串通损害国家利益情形。

**1. 自上而下建逻辑结构**
### a. 第一步：抽象能力

---

**3. 风险评估与商业可行性评估**
- 风险点：阴阳合同效力不确定性
  - 发生概率：高
  - 影响程度：高
  - 综合风险等级：高
  - 修改建议：建议明确合同效力条款

---

**5. 结论与行动建议**
应该怎么做：建议当事人明确真实意思表示，避免签订阴阳合同。
为什么是这样：引用推理步骤，阴阳合同可能因违反强制性规定而无效。
</FINAL_REPORT>"""

output_layer = OutputLayer()
result = output_layer.process(test_content)

print("修复后的处理结果:")
print("=" * 60)
print(result)
print("=" * 60)

# 验证各章节
print("\n章节验证:")
print(f"✓ 审查前提存在: {'1. 审查前提' in result}")
print(f"✓ 风险评估存在: {'2. 风险评估' in result}")
print(f"✓ 结论与行动建议存在: {'3. 结论与行动建议' in result}")
print(f"✓ 风险内容存在: {'阴阳合同效力不确定性' in result}")
