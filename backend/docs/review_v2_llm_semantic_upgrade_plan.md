# 合同审查第二版：大模型语义判定升级计划

## Summary

把当前 Review V2 从“规则语义判定”升级为“条款切分 + 候选召回 + 大模型语义判定 + 规则兜底”的真实语义审查流程。第一阶段只覆盖房屋租赁合同 50 个审查点，复用现有 DeepSeek 统一 `call_llm()`，不新建模型客户端，不影响裁判引擎和旧版合同审查主流程。

默认策略：大模型可用时由大模型判断；模型失败、超时、JSON 不合法时自动回退到现有规则版结果，并在结果中标记判定来源。

## Key Changes

- 新增大模型判定层：保留现有规则接口，新增 `judge_checkpoint_with_llm(checkpoint, candidate_clauses, rule_judgment) -> ReviewJudgment`。
- 判定流程改为四步：条款切分、候选召回、规则预判、大模型复核。
- API 返回新增 `judge_source`、`llm_confidence`、`llm_raw_reason`、`fallback_reason`。
- 前端报告展示判定来源、模型置信度、规则兜底原因，并支持筛选规则兜底项。

## Implementation Changes

- 新增 `backend/review_v2/llm_semantic_reviewer.py`，通过 `reasoning.llm_client.call_llm(prompt, response_format="json")` 调用现有云端模型。
- 模型只接收单个检查点和最多 4 个候选条款，不传完整合同全文，控制成本和上下文污染。
- 模型 JSON 输出固定字段：`coverage_status`、`risk_level`、`reasoning_summary`、`evidence_clause_ids`、`confidence`、`needs_human_review`。
- 后端必须校验模型输出：枚举值合法、证据 ID 来自候选条款、不得出现裁判式表述。
- 增加环境变量：`REVIEW_V2_LLM_ENABLED`、`REVIEW_V2_LLM_MAX_CANDIDATES`、`REVIEW_V2_LLM_MAX_RETRIES`。
- 模型失败、输出不合法或安全检查失败时，自动使用规则版结果，并写入 `fallback_reason`。

## Test Plan

- Mock `call_llm()` 返回合法 JSON，确认采用 LLM 判定结果。
- Mock 模型超时、非 JSON、非法枚举、非法证据 ID、裁判式表述，确认回退规则版。
- 关闭 `REVIEW_V2_LLM_ENABLED` 时，结果与当前规则版兼容。
- 用示范房屋租赁合同跑完整审查，确认仍输出 50 项，包含证据条款、判断理由和判定来源。
- PDF 导出与页面报告一致，不出现“判决结果 / 裁判结论 / 驳回请求 / 应赔偿”等裁判式表述。
- 回归运行 `backend/tests/test_review_v2_house_lease.py`、`python -m pytest backend/tests --ignore=backend/tests/test_security.py`、`npm run build`。

## Assumptions

- 当前阶段只升级房屋租赁合同审查原型，其余 17 类合同暂不开放。
- 使用项目已有云端模型客户端，不新增 OpenAI、LangChain 或其它模型依赖。
- 第一版采用逐检查点调用，优先保证可追溯和可回退；性能优化后续再做批量判定。
- 审查报告不保存合同全文到数据库，只展示候选证据片段。
- `backend/tests/test_security.py` 的既有失败不纳入本次改造范围。
