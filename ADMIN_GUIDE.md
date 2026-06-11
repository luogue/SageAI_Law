# SageAI 管理员操作指南

## 管理员审核反馈流程

### 1. 管理员认证

所有管理员接口需要在请求头中添加 `X-Admin-Token`，其值为环境变量 `ADMIN_TOKEN` 的值（在 `.env` 文件中配置）。

请求头示例：
```
X-Admin-Token: your-admin-token-here
```

### 2. 获取待审核的反馈列表

#### API 端点
```
GET /feedback?status=pending&page=1&limit=20
```

#### 可选参数
- `status`: 筛选状态，可选值为 `pending`（待审核）、`approved`（已通过）、`rejected`（已驳回）
- `page`: 页码，默认为 1
- `limit`: 每页数量，默认为 20，最大 100
- `category`: 按类别筛选（可选）

#### 响应示例
```json
{
  "success": true,
  "feedbacks": [
    {
      "id": 1,
      "user_id": 1,
      "report_id": "abc123",
      "feedback_type": "detailed",
      "categories": ["条款不明确"],
      "comment": "用户的反馈内容",
      "upload_consent": true,
      "contract_preview": "合同文本的前100个字符...",
      "bonus_awarded": 0,
      "status": "pending",
      "reviewed_at": null,
      "reject_reason": null,
      "created_at": "2026-05-31T08:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 20
}
```

### 3. 审核反馈

#### API 端点
```
POST /feedback/review
```

#### 请求体
```json
{
  "feedback_id": 1,
  "action": "approve",  // 或 "reject"
  "reject_reason": "不符合要求"  // 仅在 action 为 "reject" 时需要
}
```

#### 审核通过响应示例
```json
{
  "success": true,
  "message": "审核通过！已向用户赠送 3 次免费审查额度",
  "bonus_awarded": 3,
  "current_credits": 5
}
```

#### 审核驳回响应示例
```json
{
  "success": true,
  "message": "审核驳回，不赠送额度",
  "bonus_awarded": 0
}
```

## 使用 curl 命令示例

### 获取待审核的反馈
```bash
curl -X GET "http://localhost:8003/feedback?status=pending&page=1&limit=20" \
  -H "X-Admin-Token: your-admin-token-here"
```

### 审核通过
```bash
curl -X POST "http://localhost:8003/feedback/review" \
  -H "Content-Type: application/json" \
  -H "X-Admin-Token: your-admin-token-here" \
  -d '{
    "feedback_id": 1,
    "action": "approve"
  }'
```

### 审核驳回
```bash
curl -X POST "http://localhost:8003/feedback/review" \
  -H "Content-Type: application/json" \
  -H "X-Admin-Token: your-admin-token-here" \
  -d '{
    "feedback_id": 1,
    "action": "reject",
    "reject_reason": "反馈内容无效"
  }'
```

## 数据库字段说明

### feedback 表新增字段
| 字段 | 类型 | 说明 |
|------|------|------|
| status | String(20) | 状态：pending（待审核）、approved（已通过）、rejected（已驳回） |
| reviewed_at | DateTime | 审核时间 |
| reviewer_id | Integer | 审核人ID（外键，可选） |
| reject_reason | Text | 驳回原因（可选） |
