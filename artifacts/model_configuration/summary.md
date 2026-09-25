# 模型配置修改与验证

## 修改文件

- `AGENTS.md`
- `README.md`
- `DEPLOY_CHECKLIST.md`
- `main.py`
- `sage_engine.py`
- `.env.example`
- `.env.production.example`
- `backend/.env.example`
- `backend/config.py`
- `backend/model_settings.py`
- `backend/secret_redaction.py`
- `backend/reasoning/llm_client.py`
- `backend/review_v2/deepseek_transport.py`
- `backend/review_v2/llm_semantic_reviewer.py`
- `backend/layers/inference_layer.py`
- `backend/layers/output_layer.py`
- `backend/logging_config.py`
- `backend/main.py`
- `backend/requirements.txt`
- `backend/tests/test_model_provider_configuration.py`
- `backend/tests/test_review_v2_house_lease.py`
- `backend/tests/test_input_layer_word_compat.py`
- `frontend/src/views/ContractReviewV2.vue`
- `backend/docs/algorithm_safety_self_assessment.md`
- `backend/docs/security_assessment_report_framework.md`
- `backend/docs/review_v2_llm_semantic_upgrade_plan.md`
- `scripts/run_quality6_7_final_release_hotfix.py`
- `scripts/run_quality6_7_freeze_closure.py`

本地环境文件：`.env`（删除旧配置）、`backend/.env`（本机 Key）、`.env.production`（Docker Key）。均未被 Git 跟踪，真实 Key 未写入源码或模板。

## 删除入口

删除 Qwen/DashScope、Doubao/Ark 的模型定义、环境读取、优先级选择和 provider fallback；删除 DashScope 旧响应分支和 SDK 依赖。状态接口只返回 DeepSeek。旧推理方法改为 `_call_model_api`，报告模型元数据同步；前端无旧 provider 选择项，复核开关明确为 DeepSeek。清理环境模板、CLI、说明文档及验收脚本元数据。

## 验证

- 新 Key 与 backend/.env 一致；主客户端、事实抽取真实 DeepSeek 调用各 HTTP 200，deepseek-chat。
- 已重启本地后端（PID 18000）；technology/labor 状态接口只返回 deepseek 且 available=true。
- 当前技术秘密许可合同真实上传：REPORT_READY，阻断 0。
- 相关测试：165 通过、10 项既有失败；与修改前 156 通过、10 失败逐项相比，新增失败 0、旧状态变化 0。新增 9 项全部通过。
- 技术秘密许可保护测试 46/46；前端构建通过（保留既有 chunk 大小提示）。
- 运行时代码扫描旧 provider 入口为 0；新 Key 在已检查源码、模板、报告及日志中出现次数为 0。
- 两个历史测试仅同步已移除 provider 的状态检查与旧方法名，其他预期未改；没有删除旧失败测试。
