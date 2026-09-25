# AI合同审查系统

基于Vue3 + FastAPI的AI合同审查系统，采用四层架构设计。

## 技术栈

### 前端
- Vue 3 + Vite
- Element Plus
- marked (Markdown渲染)

### 后端
- FastAPI
- python-docx (Word文件读取)
- pypdf (PDF文件读取)
- requests (API调用)
- python-dotenv (环境变量)

## 四层架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        输入层 (Input Layer)                     │
│  接收原始输入 → 提取文本 → 识别关键事实 → 输出结构化JSON数据      │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       推理层 (Inference Layer)                  │
│  加载提示词模板 → 填充事实数据 → 调用DeepSeek API → 生成原始报告       │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       校验层 (Validation Layer)                 │
│  格式检查 → 置信度验证 → 信息来源抽查 → 标记警告(不阻断)          │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    输出封装层 (Output Layer)                    │
│  统一格式打包 → 添加元数据 → JSON+Markdown → 返回前端           │
└─────────────────────────────────────────────────────────────────┘
```

### 各层职责

| 层级 | 职责 | 关键功能 |
|------|------|----------|
| **输入层** | 接收和解析输入 | 文件上传、文本提取、事实识别 |
| **推理层** | 生成分析报告 | 提示词构建、DeepSeek API调用 |
| **校验层** | 验证报告质量 | 格式检查、置信度验证、来源抽查 |
| **输出封装层** | 格式化输出 | 统一格式、元数据、多格式支持 |

## 功能特性

- 文件上传：支持拖拽上传，支持 .docx、.txt、.pdf 格式
- 文件大小限制：单个文件最大10MB
- 额外审查要求：用户可输入额外的审查要求或背景说明
- 实时反馈：提交后显示loading状态
- 结果展示：支持Markdown格式渲染
- 下载功能：支持下载为TXT、Word、PDF格式
- 四层架构：输入层→推理层→校验层→输出封装层

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 18+

### 后端部署

1. 进入后端目录：
```bash
cd backend
```

2. 安装依赖（推荐使用虚拟环境）：
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

**requirements.txt 包含以下依赖：**
- `fastapi` - FastAPI 框架
- `uvicorn` - ASGI 服务器
- `python-multipart` - 文件上传处理
- `python-docx` - Word 文件读取
- `pypdf` - PDF 文件读取
- `python-dotenv` - 环境变量管理
- `requests` - HTTP 请求
- `python-jose[cryptography]` - JWT 认证
- `bcrypt` - 密码加密
- `sqlalchemy` - ORM 数据库操作

3. 配置环境变量：
```bash
cp .env.example .env
```
编辑 `backend/.env` 文件，添加你的DeepSeek API Key：
```
DEEPSEEK_API_KEY=your-api-key-here
```

4. 启动后端服务：
```bash
python main.py
```
服务将在 http://localhost:8000 启动

### 前端部署

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 启动开发服务器：
```bash
npm run dev
```
前端将在 http://localhost:5173 启动

### 生产部署

#### 前端构建
```bash
cd frontend
npm run build
```

#### 后端部署 (使用uvicorn)
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API接口

### POST /api/review

合同审查接口

**请求参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| file | File | 是 | 合同文件 (.docx, .txt, .pdf) |
| additional_instructions | String | 否 | 额外审查要求 |

**响应示例：**
```json
{
  "success": true,
  "message": "审查完成",
  "result": "合同审查报告内容...",
  "metadata": {
    "timestamp": "2024-01-01 12:00:00",
    "model_version": "deepseek-chat",
    "confidence_score": 0.85,
    "validation_status": "pass"
  },
  "validation": {
    "has_warnings": false,
    "warnings": [],
    "confidence_score": 0.85
  },
  "summary": {
    "risk_level": "中",
    "risk_count": 5,
    "suggestion_count": 3,
    "confidence": 0.85
  }
}
```

### GET /api/health

健康检查接口

### GET /api/layers

获取四层架构信息

## 项目结构

```
.
├── backend/                    # 后端服务
│   ├── layers/                # 四层模块
│   │   ├── input_layer.py      # 输入层
│   │   ├── inference_layer.py  # 推理层
│   │   ├── validation_layer.py # 校验层
│   │   └── output_layer.py     # 输出封装层
│   ├── contract_review_prompt.txt  # 提示词模板
│   ├── main.py                # FastAPI入口
│   └── requirements.txt       # Python依赖
├── frontend/                  # 前端应用
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadPage.vue    # 上传页面
│   │   │   └── ResultPage.vue    # 结果页面
│   │   ├── utils/
│   │   │   └── api.js            # API工具函数
│   │   ├── App.vue               # 根组件
│   │   └── main.js               # 入口文件
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── .env                       # 环境变量
├── .env.example               # 环境变量示例
└── README.md                  # 项目说明
```

## 注意事项

1. 请确保已正确配置DeepSeek API Key
2. 上传文件大小限制为10MB
3. 支持的文件格式：.docx、.txt、.pdf
4. 大模型调用可能产生费用，请合理使用

## License

MIT