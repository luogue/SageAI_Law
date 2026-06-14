#!/usr/bin/env python
"""最终测试：过滤内容 + 安全检测"""
import sys
sys.path.insert(0, '.')

from layers.output_layer import OutputLayer
from security.output_guard import init_output_guard, check_output_leak
from layers.inference_layer import InferenceLayer

print("=" * 80)
print("1. 读取测试文件")
print("=" * 80)

# 读取测试文件
with open(r'f:\ai\Sage\退休人员返聘协议（模板）.docx_review.txt', 'r', encoding='utf-8') as f:
    raw_report = f.read()

print(f"原始报告长度: {len(raw_report)} 字符")
print(f"原始报告行数: {len(raw_report.split(chr(10)))}")

print("\n" + "=" * 80)
print("2. 执行内容过滤")
print("=" * 80)

# 创建输出层实例
output_layer = OutputLayer()

# 执行过滤
filtered_report = output_layer._filter_internal_content(raw_report)

print(f"过滤后长度: {len(filtered_report)} 字符")
print(f"过滤比例: {len(filtered_report)/len(raw_report)*100:.1f}%")

print("\n" + "=" * 80)
print("3. 过滤后的内容")
print("=" * 80)
print(filtered_report)

print("\n" + "=" * 80)
print("4. 执行安全检测")
print("=" * 80)

# 初始化输出守卫（需要系统提示词）
inference_layer = InferenceLayer()
system_prompt = inference_layer.prompt_template
init_output_guard(system_prompt)

# 执行安全检测
passed, detail = check_output_leak(filtered_report)

print(f"安全检测结果: {'通过' if passed else '失败'}")
print(f"检测详情: {detail}")

print("\n" + "=" * 80)
print("5. 总结")
print("=" * 80)
print(f"- 原始报告: {len(raw_report)} 字符")
print(f"- 过滤后: {len(filtered_report)} 字符")
print(f"- 安全检测: {'通过' if passed else '失败'}")
print(f"- 保留章节: 审查基准、风险评估、商业可行性评估、结论与行动建议")