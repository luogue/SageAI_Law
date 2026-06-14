"""测试输出层的过滤功能"""
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from layers.output_layer import OutputLayer

def test_filter_content():
    """测试过滤功能"""
    # 加载测试文件
    input_file = r"f:\ai\Sage\退休人员返聘协议（模板）.docx_review.txt"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_report = f.read()
        print("OK 加载测试文件成功")
    except Exception as e:
        print("ERR 加载测试文件失败: %s" % str(e))
        return
    
    # 创建输出层实例
    output_layer = OutputLayer()
    
    # 测试过滤功能
    print("\n测试 _filter_internal_content 方法...")
    filtered = output_layer._filter_internal_content(raw_report)
    
    # 保存测试结果
    output_file = r"f:\ai\Sage\test_output_layer_result.txt"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(filtered)
        print("OK 过滤结果已保存到: %s" % output_file)
    except Exception as e:
        print("ERR 保存结果失败: %s" % str(e))
    
    # 验证标题替换
    print("\n验证标题替换:")
    if '1. 审查前提' in filtered:
        print("✓ 标题替换成功: '前置步骤：关键前提确认' → '1. 审查前提'")
    else:
        print("✗ 标题替换失败: 未找到 '1. 审查前提'")
    
    if '2. 风险评估' in filtered:
        print("✓ 标题替换成功: '风险评估与商业可行性评估' → '2. 风险评估'")
    else:
        print("✗ 标题替换失败: 未找到 '2. 风险评估'")
    
    if '3. 结论与行动建议' in filtered:
        print("✓ 标题替换成功: '结论与行动建议' → '3. 结论与行动建议'")
    else:
        print("✗ 标题替换失败: 未找到 '3. 结论与行动建议'")
    
    # 验证过滤掉不需要的内容
    print("\n验证过滤效果:")
    unwanted_sections = [
        '自上而下建逻辑结构',
        '逻辑推理',
        '自检',
        '约束合规链式推理',
        '层级标注',
        '模型补充'
    ]
    
    for section in unwanted_sections:
        if section not in filtered:
            print("✓ 已过滤: %s" % section)
        else:
            print("✗ 未过滤: %s" % section)
    
    print("\n过滤后内容预览（前500字符）:")
    print("="*60)
    print(filtered[:500] + "..." if len(filtered) > 500 else filtered)
    print("="*60)

if __name__ == "__main__":
    test_filter_content()
