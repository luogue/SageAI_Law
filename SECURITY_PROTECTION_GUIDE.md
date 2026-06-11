# SageAI 前置防护措施说明

## 概述

本文档详细说明了为 SageAI 后端实现的前置防护措施，用于防止恶意用户通过持续上传无效文件消耗算力。

## 实现的防护措施

### 1. 文件格式与大小限制（前后端双重校验）

#### 前端校验
- 在 `UploadPage.vue` 中已实现基本校验
- 只允许选择 `.docx`、`.txt`、`.pdf` 格式文件

#### 后端校验
- **文件格式**：严格校验扩展名，只允许 `{'.docx', '.txt', '.pdf'}`
- **文件大小**：单个文件最大 `10MB`
- **实现位置**：`security/pre_validation.py`

#### 错误码
- `INVALID_FORMAT`：文件格式不支持
- `FILE_TOO_LARGE`：文件大小超过限制

### 2. 文本内容预校验

在调用大模型之前，对提取的文本进行检查：

#### 内容长度检查
- 去除空白字符后，长度至少需要 **100 字符**
- 错误码：`CONTENT_TOO_SHORT`

#### 合同关键词检测
- 检查是否包含至少 **2 个** 合同关键词
- 关键词包括：合同、协议、甲方、乙方、权利、义务、违约、签署、生效等
- 错误码：`NOT_CONTRACT`

### 3. 用户/IP 限流（已优化）

现有限流机制已优化，配置：

| 接口类型 | 用户限制 | IP 限制 |
|---------|---------|--------|
| `/api/review` | 20次/小时 | 50次/小时 |
| `/api/batch/review` | 5次/分钟 | 10次/分钟 |

- 实现位置：`security/rate_limiter.py`
- 错误码：`RATE_LIMIT_EXCEEDED`

### 4. 恶意行为自动黑名单（新增）

当某个 IP 或用户触发多次违规时，自动封禁：

#### 触发条件
- 1小时内违规累计达到 **10次**（可通过 `MALICIOUS_THRESHOLD` 环境变量调整）

#### 违规类型
- `format_error`：文件格式错误
- `size_exceeded`：文件大小超限
- `content_too_short`：内容过短
- `not_contract`：非合同文件
- `sensitive_content`：敏感内容
- `rate_limit`：触发限流

#### 封禁时长
- 默认 **1小时**（可通过 `MALICIOUS_BAN_DURATION` 环境变量调整）
- 实现位置：`security/malicious_behavior_detector.py`
- 错误码：`AUTO_BANNED`

### 5. 收费/扣额度时机调整

**重要**：只有在以下条件都满足时，才扣减免费额度：
1. 文件通过所有前置校验
2. 大模型调用成功
3. 校验层通过
4. 最终报告生成完成

**不会扣费的情况**：
- 前置校验失败
- 大模型调用异常
- 校验层未通过
- 其他处理失败

## 环境变量配置

可在 `.env` 文件中配置以下参数：

```env
# 恶意行为检测配置
MALICIOUS_THRESHOLD=10          # 触发自动封禁的违规次数
MALICIOUS_BAN_DURATION=3600     # 封禁时长（秒）

# Redis 限流（可选）
REDIS_URL=redis://localhost:6379/0
```

## 新增的管理员接口

### 1. 查看恶意行为统计
```
GET /admin/malicious-stats?identifier=<ip_or_user_id>
```

**响应示例**：
```json
{
    "success": true,
    "identifier": "192.168.1.1",
    "stats": {
        "format_error": 3,
        "content_too_short": 5,
        "not_contract": 2
    },
    "is_banned": true,
    "ban_reason": "1小时内违规10次"
}
```

## 新增文件说明

| 文件 | 说明 |
|------|------|
| `security/pre_validation.py` | 前置校验模块：文件格式、大小、文本内容 |
| `security/malicious_behavior_detector.py` | 恶意行为检测和自动黑名单 |
| `SECURITY_PROTECTION_GUIDE.md` | 本文档 |

## 修改的文件说明

| 文件 | 修改内容 |
|------|---------|
| `main.py` | 整合所有防护措施，更新审查接口 |

## 防护执行流程

```
请求到达
   ↓
黑名单检查（手动 + 自动）
   ↓
限流检查
   ↓
文件格式、大小校验
   ↓
文本内容提取 + 预校验（长度、合同关键词）
   ↓
敏感词检查
   ↓
大模型调用 + 审查
   ↓
✅ 成功 → 扣减额度
❌ 失败 → 不扣减
```

## 违规记录处理

所有违规行为都会被记录并用于判断是否需要自动封禁。管理员可以通过 `/admin/malicious-stats` 查看详细统计。

## 注意事项

1. **前端校验**：请同步确保前端也有相应的校验提示，提升用户体验
2. **误判处理**：合同关键词检测可能有误判，如有需要可调整关键词列表
3. **自动封禁**：自动封禁会同时添加到黑名单数据库中
4. **测试建议**：在正式环境使用前，请进行充分的测试验证
