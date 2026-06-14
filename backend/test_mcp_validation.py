"""使用本地测试文件调用 chinese-law-mcp 校验法条"""
import sys
import os
import re

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.chinese_law_mcp_client import (
    get_mcp_client,
    ChineseLawMCPClientSync,
    ValidationResult,
    LawArticle,
    CHINESE_LAW_MCP_URL,
)
from layers.legal_check_layer import (
    check_and_correct_legal_citations,
    validate_single_citation,
    init_legal_check_layer,
    LegalCheckResult,
    LegalCitation,
    ChineseLawMCPAdapter,
    LEGAL_CITATION_PATTERN,
)

# 测试文件路径
TEST_FILES = [
    r"f:\ai\Sage\测试文件\指导案例171号：中天建设集团有限公司诉河南恒和置业有限公司建设工程施工合同纠纷案_审查结果.txt",
    r"f:\ai\Sage\测试文件\退休人员返聘协议（模板）.docx_review.txt",
]

# 增强正则：支持阿拉伯数字和中文数字
CN_NUMBERS = '〇零一二两三四五六七八九十百千万'
CN_DIGITS = {'〇': 0, '零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}

# 匹配《法律名称》第X条（X可以是阿拉伯数字或中文数字）
# 支持：第1条、第一条、第143条、第七百九十三条
# article_num 捕获组支持纯数字、纯中文数字、或混合
ARTICLE_NUM_PATTERN = r'(?:\d+|[' + CN_NUMBERS + r']+|\d+[' + CN_NUMBERS + r']*)'
ENHANCED_CITATION_PATTERN = re.compile(
    r'《([^》]+)》\s*第\s*(' + ARTICLE_NUM_PATTERN + r')\s*条(?:\s*第\s*(\d+)\s*款)?'
)


def chinese_to_arabic(cn: str) -> str:
    """将中文数字转换为阿拉伯数字（简化版）"""
    if not cn:
        return cn
    # 如果已经是纯数字，直接返回
    if cn.isdigit():
        return cn
    # 简单映射：逐字替换
    # 对于复杂中文数字如"七百九十三"，这里做简化处理
    # 先尝试整体匹配常见中文数字
    total = 0
    temp = 0
    for char in cn:
        if char in '0123456789':
            total = total * 10 + int(char)
            continue
        if char in CN_DIGITS:
            temp = CN_DIGITS[char]
        elif char == '十':
            if temp == 0:
                temp = 1
            total += temp * 10
            temp = 0
        elif char == '百':
            if temp == 0:
                temp = 1
            total += temp * 100
            temp = 0
        elif char == '千':
            if temp == 0:
                temp = 1
            total += temp * 1000
            temp = 0
        elif char == '万':
            if temp == 0:
                temp = 1
            total += temp * 10000
            temp = 0
    total += temp
    return str(total) if total > 0 else cn


def extract_citations_from_file(file_path: str) -> list:
    """从文件中提取法条引用（支持中文数字和阿拉伯数字）"""
    citations = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] 无法读取文件 {file_path}: {e}")
        return citations

    # 使用增强正则提取法条引用
    for match in ENHANCED_CITATION_PATTERN.finditer(content):
        article_num = match.group(2)
        # 转换中文数字为阿拉伯数字
        article_num_arabic = chinese_to_arabic(article_num)
        citation = {
            'original': match.group(0),
            'law_name': match.group(1),
            'article_num': article_num_arabic,
            'paragraph_num': match.group(3),
            'position': match.start(),
        }
        citations.append(citation)

    return citations


def test_mcp_service() -> bool:
    """测试 MCP 服务是否可用"""
    print(f"[INFO] MCP 服务端点: {CHINESE_LAW_MCP_URL}")
    client = ChineseLawMCPClientSync()
    try:
        # 尝试获取一个常见法条来测试连通性
        result = client.get_article("民法典", "1")
        if result:
            print("[OK] MCP 服务连接成功")
            return True
        else:
            print("[WARN] MCP 服务返回空结果")
            return False
    except Exception as e:
        print(f"[FAIL] MCP 服务连接失败: {e}")
        return False


def validate_citations_with_mcp(citations: list) -> list:
    """使用 MCP 服务校验法条引用"""
    client = ChineseLawMCPClientSync()
    results = []

    for cite in citations:
        print(f"\n  正在校验: {cite['original']} ...", end=" ")
        try:
            result = client.validate_citation(
                cite['law_name'],
                cite['article_num'],
                ""
            )
            print(f"[{result.status}] {result.message}")
            results.append({
                'citation': cite,
                'status': result.status,
                'message': result.message,
                'corrected_citation': result.corrected_citation,
                'corrected_content': result.corrected_content[:100] + "..." if result.corrected_content and len(result.corrected_content) > 100 else result.corrected_content,
                'law_article': result.law_article,
            })
        except Exception as e:
            print(f"[ERROR] {e}")
            results.append({
                'citation': cite,
                'status': 'error',
                'message': str(e),
            })

    return results


def main():
    print("=" * 70)
    print("Chinese Law MCP 法条校验测试")
    print("=" * 70)

    # 第一步：测试 MCP 服务连通性
    print("\n【步骤1】测试 MCP 服务连通性")
    print("-" * 70)
    mcp_available = test_mcp_service()

    if not mcp_available:
        print("\n[!] MCP 服务不可用，请检查:")
        print("    1. 网络连接是否正常")
        print("    2. MCP 服务地址是否正确 (当前: %s)" % CHINESE_LAW_MCP_URL)
        print("    3. 如需本地部署，可运行: npx @ansvar/chinese-law-mcp")
        print("\n[!] 将尝试使用备用数据库进行基础校验...")

    # 第二步：读取测试文件并提取法条
    print("\n【步骤2】读取测试文件并提取法条引用")
    print("-" * 70)

    all_citations = []
    for file_path in TEST_FILES:
        print(f"\n读取: {os.path.basename(file_path)}")
        citations = extract_citations_from_file(file_path)
        # 去重
        seen = set()
        unique_citations = []
        for c in citations:
            key = (c['law_name'], c['article_num'])
            if key not in seen:
                seen.add(key)
                unique_citations.append(c)

        print(f"  提取到 {len(citations)} 条引用，去重后 {len(unique_citations)} 条")
        all_citations.extend(unique_citations)

    # 全局去重
    seen = set()
    final_citations = []
    for c in all_citations:
        key = (c['law_name'], c['article_num'])
        if key not in seen:
            seen.add(key)
            final_citations.append(c)

    print(f"\n总计去重后法条引用数: {len(final_citations)}")

    # 第三步：校验法条
    print("\n【步骤3】法条校验")
    print("-" * 70)

    if mcp_available:
        results = validate_citations_with_mcp(final_citations)
    else:
        # 使用备用数据库进行基础校验
        print("使用备用数据库进行校验...")
        init_legal_check_layer(use_mcp=False)
        results = []
        for cite in final_citations:
            print(f"\n  校验: {cite['original']} ...", end=" ")
            result = validate_single_citation(cite['law_name'], cite['article_num'], "")
            print(f"[{result.status}] {result.message}")
            results.append({
                'citation': cite,
                'status': result.status,
                'message': result.message,
                'corrected_citation': result.corrected_citation,
                'corrected_content': result.corrected_content[:100] + "..." if result.corrected_content and len(result.corrected_content) > 100 else result.corrected_content,
            })

    # 第四步：输出报告
    print("\n【步骤4】校验报告")
    print("=" * 70)

    status_count = {}
    for r in results:
        status = r.get('status', 'unknown')
        status_count[status] = status_count.get(status, 0) + 1

    print("\n状态统计:")
    for status, count in status_count.items():
        print(f"  {status}: {count} 条")

    print("\n详细结果:")
    for r in results:
        cite = r['citation']
        print(f"\n  原始引用: {cite['original']}")
        print(f"  状态: {r.get('status', 'unknown')}")
        print(f"  说明: {r.get('message', '')}")
        if r.get('corrected_citation'):
            print(f"  修正引用: {r['corrected_citation']}")
        if r.get('corrected_content'):
            print(f"  修正内容: {r['corrected_content']}")

    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)


if __name__ == "__main__":
    main()
