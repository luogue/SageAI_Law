"""测试 Mock LLM 功能"""
import os
import time
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置 Mock 模式
os.environ['LLM_MOCK_MODE'] = 'true'

from reasoning.llm_client import call_llm

def test_mock_text():
    """测试文本格式响应"""
    print("=" * 60)
    print("测试 1: 文本格式 Mock 响应")
    print("=" * 60)
    
    start_time = time.time()
    result = call_llm("这是一个测试提示词", response_format="text")
    end_time = time.time()
    
    print(f"\n响应时间：{end_time - start_time:.2f}秒")
    print(f"\n响应内容:\n{result}")
    print("\n" + "=" * 60)

def test_mock_json():
    """测试 JSON 格式响应"""
    print("=" * 60)
    print("测试 2: JSON 格式 Mock 响应")
    print("=" * 60)
    
    start_time = time.time()
    result = call_llm("这是一个测试提示词", response_format="json")
    end_time = time.time()
    
    print(f"\n响应时间：{end_time - start_time:.2f}秒")
    print(f"\n响应内容:\n{result}")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    print("\n开始测试 Mock LLM 功能...\n")
    
    test_mock_text()
    test_mock_json()
    
    print("\n测试完成！\n")
