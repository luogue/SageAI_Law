"""注入攻击检测测试脚本 - 使用退休人员返聘协议文件测试"""
import os
import sys
import io

# 设置标准输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from security.injection_detector import get_injection_detector, check_input_injection

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

def test_injection_detection(content):
    """测试注入攻击检测"""
    print("\n" + "="*60)
    print("【注入攻击检测测试】")
    print("="*60)
    
    detector = get_injection_detector()
    result, msg, matched_rules = detector.check_input(content)
    
    if result:
        print("✅ 注入攻击检测通过")
        print("   消息: %s" % (msg if msg else "无"))
        print("   匹配规则: %s" % (matched_rules if matched_rules else "无"))
    else:
        print("❌ 注入攻击检测失败")
        print("   消息: %s" % msg)
        print("   匹配规则: %s" % matched_rules)
    
    return result, msg, matched_rules

def test_filtered_content():
    """测试过滤后的内容（仅三个部分）"""
    print("\n" + "="*60)
    print("【测试过滤后的内容】")
    print("="*60)
    
    filtered_file = r"f:\ai\Sage\test_filtered_output.txt"
    if os.path.exists(filtered_file):
        content = load_test_content(filtered_file)
        if content:
            test_injection_detection(content)
    else:
        print("ERR 过滤后的文件不存在，请先运行安全测试脚本")

def main():
    """主函数"""
    input_file = r"f:\ai\Sage\退休人员返聘协议（模板）.docx_review.txt"
    
    print("="*60)
    print("注入攻击检测测试脚本")
    print("="*60)
    
    # 1. 测试原始文件
    print("\n--- 测试1: 原始文件内容 ---")
    content = load_test_content(input_file)
    if content:
        test_injection_detection(content)
    
    # 2. 测试过滤后的文件
    test_filtered_content()
    
    print("\n" + "="*60)
    print("注入攻击检测测试完成！")
    print("="*60)

if __name__ == "__main__":
    main()
