# LLM Mock 模式使用指南

## 功能说明

Mock 模式允许在不消耗真实 API 配额的情况下测试系统功能。启用后，所有 LLM 调用会在 3 秒延迟后返回模拟响应。

## 启用方法

### 方法 1: 修改 `.env` 文件（推荐）

编辑 `backend/.env` 文件，设置：

```bash
LLM_MOCK_MODE=true
```

### 方法 2: 设置环境变量（临时）

在启动后端服务前设置环境变量：

**Windows PowerShell:**
```powershell
$env:LLM_MOCK_MODE="true"
python main.py
```

**Linux/Mac:**
```bash
export LLM_MOCK_MODE=true
python main.py
```

### 方法 3: 代码中设置（仅用于测试）

```python
import os
os.environ['LLM_MOCK_MODE'] = 'true'
```

## Mock 响应示例

### 文本格式响应

```
这是模拟的大模型响应文本。

测试信息：
- 提示词长度：123 字符
- 响应格式：text
- 延迟时间：3 秒

此响应由 Mock 模式生成，用于测试目的。
```

### JSON 格式响应

```json
{
  "status": "success",
  "message": "这是模拟的 JSON 响应",
  "test_data": {
    "prompt_length": 123,
    "response_format": "json"
  }
}
```

## 使用场景

1. **开发测试**: 在不消耗 API 配额的情况下开发和测试功能
2. **演示环境**: 快速演示系统功能，无需真实 API 调用
3. **性能测试**: 测试系统性能，排除网络延迟影响
4. **离线开发**: 在没有网络连接的环境下开发

## 注意事项

- ⚠️ Mock 模式下的响应是固定的测试文本，不包含真实的 AI 分析结果
- ⚠️ 生产环境必须关闭 Mock 模式（`LLM_MOCK_MODE=false`）
- ⚠️ Mock 模式会固定延迟 3 秒，模拟真实 API 调用的响应时间

## 关闭 Mock 模式

编辑 `.env` 文件，设置：

```bash
LLM_MOCK_MODE=false
```

重启后端服务后生效。

## 验证 Mock 模式状态

查看后端日志，如果看到以下信息，说明 Mock 模式已启用：

```
[MOCK MODE] 使用模拟 LLM 响应，3 秒后返回测试文本...
```

## 测试 Mock 功能

运行测试脚本验证 Mock 功能是否正常工作：

```bash
cd backend
python test_mock_llm.py
```

预期输出：
- 文本格式 Mock 响应
- JSON 格式 Mock 响应
- 响应时间约 3 秒
