"""安全检测测试脚本 - 使用退休人员返聘协议文件测试"""
import os
import sys
import io
import re

# 设置标准输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from security.sensitive_filter import get_sensitive_filter
from security.content_safety import ContentSafety, check_text_safety

def load_test_content(filepath):
    """加载测试文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        print("OK 成功加载文件: %s" % filepath)
        print("  文件大小: %d 字符" % len(content))
        return content
    except Exception as e:
        print("ERR 加载文件失败: %s" % str(e))
        return None

def extract_sections(content):
    """提取指定的三个部分内容"""
    sections = {}
    
    # 1. 提取前置步骤：关键前提确认
    premise_pattern = r'(前置步骤：关键前提确认（强制执行）.*?)(?=\n---\n|\Z)'
    premise_match = re.search(premise_pattern, content, re.DOTALL)
    if premise_match:
        # 替换标题：前置步骤：关键前提确认（强制执行）→ 1. 审查前提
        premise_content = premise_match.group(1).strip()
        premise_content = re.sub(r'^前置步骤：关键前提确认（强制执行）', '1. 审查前提', premise_content)
        sections['premise'] = premise_content
        print("OK 提取到前置步骤部分（标题已替换）")
    else:
        sections['premise'] = ""
        print("ERR 未找到前置步骤部分")
    
    # 2. 提取风险评估与商业可行性评估
    risk_pattern = r'(3. 风险评估与商业可行性评估.*?)(?=\n---\n|\Z)'
    risk_match = re.search(risk_pattern, content, re.DOTALL)
    if risk_match:
        # 替换标题：3. 风险评估与商业可行性评估 → 2. 风险评估
        risk_content = risk_match.group(1).strip()
        risk_content = re.sub(r'^3\. 风险评估与商业可行性评估', '2. 风险评估', risk_content)
        sections['risk'] = risk_content
        print("OK 提取到风险评估部分（标题已替换）")
    else:
        # 尝试另一种模式
        risk_pattern2 = r'(风险评估与商业可行性评估.*?)(?=\n---\n|\Z)'
        risk_match2 = re.search(risk_pattern2, content, re.DOTALL)
        if risk_match2:
            # 替换标题
            risk_content = risk_match2.group(1).strip()
            risk_content = re.sub(r'^风险评估与商业可行性评估', '2. 风险评估', risk_content)
            sections['risk'] = risk_content
            print("OK 提取到风险评估部分（备用模式，标题已替换）")
        else:
            sections['risk'] = ""
            print("ERR 未找到风险评估部分")
    
    # 3. 提取结论与行动建议
    conclusion_pattern = r'(5. 结论与行动建议.*?)(?=\n---\n|\Z)'
    conclusion_match = re.search(conclusion_pattern, content, re.DOTALL)
    if conclusion_match:
        # 替换标题：5. 结论与行动建议 → 3. 结论与行动建议
        conclusion_content = conclusion_match.group(1).strip()
        conclusion_content = re.sub(r'^5\. 结论与行动建议', '3. 结论与行动建议', conclusion_content)
        sections['conclusion'] = conclusion_content
        print("OK 提取到结论与行动建议部分（标题已替换）")
    else:
        # 尝试另一种模式
        conclusion_pattern2 = r'(结论与行动建议.*?)(?=\n---\n|\Z)'
        conclusion_match2 = re.search(conclusion_pattern2, content, re.DOTALL)
        if conclusion_match2:
            # 替换标题
            conclusion_content = conclusion_match2.group(1).strip()
            conclusion_content = re.sub(r'^结论与行动建议', '3. 结论与行动建议', conclusion_content)
            sections['conclusion'] = conclusion_content
            print("OK 提取到结论与行动建议部分（备用模式，标题已替换）")
        else:
            sections['conclusion'] = ""
            print("ERR 未找到结论与行动建议部分")
    
    return sections

def save_filtered_content(sections, output_file):
    """保存过滤后的内容（只包含三个指定部分）"""
    print("\n" + "="*60)
    print("【保存】过滤后的内容（仅包含三个指定部分）")
    print("="*60)
    
    # 组合三个部分
    filtered = "\n\n".join([
        sections.get('premise', ''),
        sections.get('risk', ''),
        sections.get('conclusion', '')
    ])
    
    # 移除多余空行
    filtered = re.sub(r'\n{3,}', '\n\n', filtered).strip()
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(filtered)
        print("OK 过滤后的内容已保存到: %s" % output_file)
        return True
    except Exception as e:
        print("ERR 保存文件失败: %s" % str(e))
        return False

def test_sensitive_filter(content):
    """测试敏感词过滤"""
    print("\n" + "="*60)
    print("【测试1】敏感词过滤测试")
    print("="*60)
    
    filter = get_sensitive_filter()
    ok, hit_words = filter.filter(content)
    
    if ok:
        print("OK 敏感词检测通过")
        if hit_words:
            print("  命中白名单词: %s" % hit_words)
        else:
            print("  未命中任何敏感词")
    else:
        print("ERR 敏感词检测失败")
        print("  命中敏感词: %s" % hit_words)
    
    return ok, hit_words

def test_content_safety(content):
    """测试内容安全审核"""
    print("\n" + "="*60)
    print("【测试2】内容安全审核测试")
    print("="*60)
    
    # 测试原有接口
    safety = ContentSafety()
    ok, msg = safety.check_text(content[:5000])  # 限制长度
    result_str = "通过" if ok else "拦截"
    print("原有接口 - 结果: %s, 消息: %s" % (result_str, msg))
    
    # 测试新接口
    result = check_text_safety(content[:5000])
    print("新接口 - 成功: %s, 建议: %s, 标签: %s" % (result['success'], result['suggestion'], result['label']))
    if 'message' in result and result['message']:
        print("         消息: %s" % result['message'])
    
    return ok, result

def main():
    """主函数"""
    input_file = r"f:\ai\Sage\退休人员返聘协议（模板）.docx_review.txt"
    output_file = r"f:\ai\Sage\test_filtered_output.txt"
    
    print("="*60)
    print("安全检测测试脚本 - 仅提取三个指定部分")
    print("="*60)
    
    # 1. 加载文件内容
    content = load_test_content(input_file)
    if not content:
        print("ERR 无法加载测试文件，退出")
        return
    
    # 2. 提取指定部分
    sections = extract_sections(content)
    
    # 3. 保存过滤后的内容（仅三个部分）
    save_filtered_content(sections, output_file)
    
    # 4. 测试敏感词过滤（使用过滤后的内容）
    filtered_content = "\n\n".join([sections.get('premise', ''), sections.get('risk', ''), sections.get('conclusion', '')])
    test_sensitive_filter(filtered_content)
    
    # 5. 测试内容安全审核
    test_content_safety(filtered_content)
    
    print("\n" + "="*60)
    print("测试完成！")
    print("="*60)

if __name__ == "__main__":
    main()
