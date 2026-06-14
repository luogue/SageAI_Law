"""法条校验模块测试"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 测试导入
print("=" * 60)
print("测试法条校验模块导入")
print("=" * 60)

try:
    from layers.legal_check_layer import (
        check_and_correct_legal_citations,
        validate_single_citation,
        init_legal_check_layer,
        LegalCheckResult,
        LegalCitation,
        ChineseLawMCPAdapter,
        ENABLE_LEGAL_CHECK,
        LEGAL_CITATION_PATTERN,
    )
    print("[OK] 模块导入成功")
except ImportError as e:
    print(f"[FAIL] 模块导入失败: {e}")
    sys.exit(1)

# 测试 MCP 客户端导入
try:
    from utils.chinese_law_mcp_client import (
        get_mcp_client,
        ChineseLawMCPClientSync,
        ValidationResult,
        LawArticle,
    )
    print("[OK] MCP 客户端导入成功")
except ImportError as e:
    print(f"[FAIL] MCP 客户端导入失败: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("测试法条引用提取")
print("=" * 60)

test_report = """
根据《民法典》第143条规定，民事法律行为有效需要具备三个条件。
同时参考《民法典》第464条关于合同的定义。
另外，《合同法》第2条已废止，应适用民法典相关规定。
"""

# 测试正则匹配
citations = LEGAL_CITATION_PATTERN.findall(test_report)
print(f"提取到的法条引用: {citations}")
print(f"共 {len(citations)} 条引用")

print("\n" + "=" * 60)
print("测试单个法条校验（使用备用数据库）")
print("=" * 60)

# 初始化校验层（使用备用数据库，因为 MCP 服务可能不可用）
init_legal_check_layer(use_mcp=False)

# 测试单个法条校验
result = validate_single_citation("民法典", "143", "民事法律行为有效")
print(f"法律名称: 民法典")
print(f"条款号: 143")
print(f"状态: {result.status}")
print(f"修正内容: {result.corrected_content[:50]}...")

print("\n" + "=" * 60)
print("测试完整报告校验")
print("=" * 60)

corrected_report, records = check_and_correct_legal_citations(test_report)
print(f"修正记录数: {len(records)}")
for record in records:
    print(f"  - {record['original']} -> {record['corrected']} [{record['status']}]")

print("\n修正后的报告片段:")
print(corrected_report[:200])

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
print("\n使用说明:")
print("1. 导入模块: from layers.legal_check_layer import check_and_correct_legal_citations")
print("2. 校验报告: corrected_report, records = check_and_correct_legal_citations(report)")
print("3. 校验单条: result = validate_single_citation('民法典', '143', '内容')")
print("4. 配置 MCP URL: 设置环境变量 CHINESE_LAW_MCP_URL")
print("5. 启用/禁用: 设置环境变量 ENABLE_LEGAL_CHECK=true/false")