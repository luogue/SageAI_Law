"""千问(Qwen) 大模型连接测试脚本"""
import os
import sys
import time
import requests

# 添加 backend 目录到 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 读取 .env 文件
def load_env(env_path):
    """加载 .env 文件中的环境变量"""
    if not os.path.exists(env_path):
        print(f"[ERROR] .env 文件不存在: {env_path}")
        return
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, _, value = line.partition('=')
                key = key.strip()
                value = value.strip()
                if key and value:
                    os.environ[key] = value
                    if 'KEY' in key.upper():
                        print(f"  [ENV] {key} = ***已加载***")
                    else:
                        print(f"  [ENV] {key} = {value}")

# 加载环境变量
env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_env(env_file)

# ========== 测试1：直接 API 连接 ==========
print("\n" + "=" * 80)
print("【测试1】千问 DashScope API 直接连接测试")
print("=" * 80)

api_key = os.getenv("DASHSCOPE_API_KEY", "").strip()
model_name = os.getenv("QWEN_MODEL", "qwen-max")

if not api_key:
    print("[ERROR] DASHSCOPE_API_KEY 未配置！")
else:
    print(f"  API Key: ***{api_key[:4]}...{api_key[-4:]}***")
    print(f"  Model: {model_name}")
    print(f"  Endpoint: https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions")
    
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": "请回复：千问连接测试成功。当前时间是什么？用一句话回答。"}
        ],
        "max_tokens": 200,
        "temperature": 0.1,
    }
    
    start_time = time.time()
    try:
        response = requests.post(url, headers=headers, json=data, timeout=(5, 60))
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"\n  [SUCCESS] HTTP 200 (耗时 {elapsed:.1f}秒)")
            print(f"  响应内容: {content[:300]}")
            print(f"  Token 用量: {result.get('usage', 'N/A')}")
        else:
            print(f"\n  [FAILED] HTTP {response.status_code} (耗时 {elapsed:.1f}秒)")
            print(f"  错误详情: {response.text[:500]}")
    except requests.exceptions.ConnectTimeout:
        print(f"\n  [FAILED] 连接超时 (5秒) - 网络无法访问 DashScope")
    except requests.exceptions.ReadTimeout:
        print(f"\n  [FAILED] 读取超时 (60秒) - 模型响应太慢")
    except Exception as e:
        print(f"\n  [FAILED] 异常: {type(e).__name__}: {e}")

# ========== 测试2：通过 llm_client 调用 ==========
print("\n" + "=" * 80)
print("【测试2】通过 llm_client 调用（当前模型优先级）")
print("=" * 80)

from reasoning.llm_client import call_llm, AllModelsFailedError, LLM_PRIORITY

print(f"  模型优先级: {LLM_PRIORITY}")
print(f"  可用模型: (构建中...)")

start_time = time.time()
try:
    result = call_llm("请用一句话回答：中国的首都是哪里？", response_format="text")
    elapsed = time.time() - start_time
    print(f"\n  [SUCCESS] 调用成功 (耗时 {elapsed:.1f}秒)")
    print(f"  响应内容: {result[:300]}")
except AllModelsFailedError as e:
    elapsed = time.time() - start_time
    print(f"\n  [FAILED] AllModelsFailedError (耗时 {elapsed:.1f}秒): {e}")
except Exception as e:
    elapsed = time.time() - start_time
    print(f"\n  [ERROR] 异常 (耗时 {elapsed:.1f}秒): {type(e).__name__}: {e}")

# ========== 测试3：千问优先顺序验证 ==========
print("\n" + "=" * 80)
print("【测试3】优先级验证")
print("=" * 80)
print(f"  当前 DEFAULT_PRIORITY: {LLM_PRIORITY}")
print(f"  第一位模型: {LLM_PRIORITY[0] if LLM_PRIORITY else 'N/A'}")
if LLM_PRIORITY and LLM_PRIORITY[0] == 'qwen':
    print("  [PASS] 千问(Qwen) 已经是第一位优先模型！")
else:
    print("  [WARN] 千问不是第一位，请检查 LLM_PRIORITY 环境变量和 DEFAULT_PRIORITY")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
