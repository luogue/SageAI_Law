# 已验证事实与 coverage 一致性修复

## 实际故障

原始诊断：`artifacts/employment-105-closure/fact-error-8dc5314ce13147ef92d74579ebf21c53.json`。

关联规则为 EMP-05-01，冲突字段为 `working_hours.hours_per_week`。它是工时上下文，**不是**该规则的必需覆盖要素；必需要素为工时制度、休息安排和加班待遇。

旧调用链：`employment_fact_pipeline.run → deepseek_facts.verify → conflicts 列表 → VERIFICATION_COVERAGE_CONFLICT`。抽取库中该字段为 ABSENT；核验模型在 additional_facts 添加了 40 小时/周的 INFERRED 事实，却仍返回 coverage=ABSENT。旧代码用任意事实记录的存在性与另一个模型标签比较，未区分明确事实和推断事实，故在进入规则聚合前阻断。

## 当前状态来源

- 抽取及核验输出检索范围、未决概念和事实，不再独立生成规则 coverage。
- `fact_verification.verified_store` 按 fact_id 核验，过滤未支持候选，对补充事实重新绑定真实原文，归一化后生成唯一的已验证 FactStore。
- 明确且可信的已验证事实为 EXTRACTED；推断、低置信度或无法确认的事实为 UNCERTAIN；完成全文核验且无相应事实才为 ABSENT。False 是明确的否定值，不等同于 null、空值，也不会作为正向保护覆盖。
- 规则读取同一 FactStore。已有部分必要事实保持部分覆盖；已有全部正向必要事实且无不利安排时通过；不适用及待核验独立处理。法律阈值和不利事实判断继续由确定性规则执行。
- 核心事实验证失败继续 BLOCK；被否决的推断或否定候选保留未决状态，不伪装成已验证缺失。错误 JSON、事实类型、来源绑定、未知 fact_id 和不完整检索范围仍阻断。
- 现有一次 DeepSeek 修复预算用于定向重抽未决或失败要素，保留其他已验证事实，随后统一核验。没有其他模型或关键词回退。
- 保留 `VERIFICATION_COVERAGE_CONFLICT` 门禁，核对派生 coverage 与已验证库。报告调试对象记录 required_fact、原抽取状态、验证状态、coverage 状态及事实 ID。

## 修改文件

生产链路：

- `backend/review_v2/fact_verification.py`
- `backend/review_v2/employment_fact_store.py`
- `backend/review_v2/employment_fact_pipeline.py`
- `backend/review_v2/deepseek_facts.py`
- `backend/routers/review_v2.py`（运行版本来源登记）

测试：

- `backend/tests/test_verified_fact_coverage.py`
- `backend/tests/test_employment_fact_pipeline.py`
- `backend/tests/test_fact_validation_diagnostics.py`

## 验证

`test_verified_fact_coverage.py`、`test_employment_fact_pipeline.py`、`test_fact_validation_diagnostics.py`、`test_employment_fact_semantics.py` 合计 108 项通过。覆盖完整、部分、缺失、不适用、验证失败、跨条款及多证据、False/null/空字符串、旧协议兼容、重复事实合并、状态篡改阻断、定向修复保留已验证事实。

三份既有合成回归合同通过真实 multipart 业务处理器并重新调用 DeepSeek，最终断言、原文哈希和精确证据均通过。详情：`artifacts/employment-fact-holdouts/verified-coverage-acceptance.json`。这些是已固定的回归合同，不声称是外部盲测。

当前用户原合同通过页面 `/contract-review-v2` 提交至 `/review-v2/file` 的验收记录保存在 `artifacts/employment-105-verified-closure/`。
