# 劳动合同结构化事实链路

劳动合同 `/review-v2/file`、`/review-v2/checklist` 以及
`engine.review_contract_v2(..., 'labor')` 均先调用 DeepSeek，再进入原有报告与质量门。
`use_llm=false` 不关闭劳动合同事实抽取；它不再表示允许关键词回退。
非劳动合同类型仍使用原有链路。

## 数据流

1. 完整原文按既有 parser 划分可定位条款，不做关键词 top-k 召回。
2. `deepseek_facts.extract` 按事实主题分两次输出；每次均包含全文。
3. `FactStore` 校验 schema、全文/概念检索覆盖、值类型、逐字引用及条款归属。
4. DeepSeek 独立核验候选事实是否由引文明示支持，复核遗漏，撤销错误事实。
5. 再次做确定性 schema、金额、引用、位置校验；每次请求有独立 ContextVar 事实库。
6. EMP/NC 原有规则要求通过 concept 映射消费事实。并列必要事实拆成子要素；跨条款证据合并。
7. 试用期上限、竞业24个月、普通辞职通知、违约金适用场景、义务冲突由代码判断。
8. 后续 coverage 和 SEARCH_AUDIT 消费同一个事实库；报告、JSON 和现有质量门保持同源。

## Schema 与审计

`employment_fact_schema.CONCEPTS` 是领域 schema；`ELEMENTS` 为规则要素的或/且概念映射。
每个事实保存 `fact_id / concept / normalized_value / evidence / confidence / assertion`。
evidence 包含条款 ID、section、原文、相对 `clause.text` 的 Unicode 字符 span；只有全文精确匹配时
提供 `document_span`，不虚构偏移。中文大写、千分位等金额由代码归一。

`structured_fact_debug` 同时保存输入、DeepSeek 原始响应、独立核验、归一事件、事实、规则决策。
该调试数据含合同原文，仅通过已鉴权的原有审查接口返回；不加入外部遥测。

EXPLICIT 且置信度达到阈值、通过原文绑定与语义核验的事实才支持 coverage。
INFERRED 仍保存在调试数据中，不直接充当明示约定。存在不确定抽取时，相关事项进入待核验，
不能生成 NOT_FOUND。只有全文覆盖完备且相应概念没有可用正向事实，才生成带事实查询证明的缺失审计。

## Provider 与故障

字段诊断、格式对齐及修复预算的后续修复见 [事实校验诊断修复](employment-fact-validation.md)。

仅使用 `reasoning.llm_client.MODEL_DEFINITIONS['deepseek']` 的端点、模型环境变量及现有密钥。
不调用通用多模型降级客户端。JSON 模式使用 DeepSeek 官方参数：
[JSON Output](https://api-docs.deepseek.com/guides/json_mode/)。

抽取/核验允许一次有界的同模型纠正；网络、配额、无密钥、校验仍失败时返回
HTTP 503 / `FACT_EXTRACTION_BLOCKED`，不生成虚假的缺失结论，不切其他供应商。
全文超过60,000字符时明确拒绝，不静默截断。抽取没有持久缓存。

同一引文在全文重复出现时，document span 通过其所属条款定位；不能可靠确定时仅提供
精确 clause span，不将其错误绑定到第一次出现的位置。非法日期等模型值统一按抽取校验错误处理。

## 验证

新链路测试：`backend/tests/test_employment_fact_pipeline.py`。
旧匹配器基线测试显式调用 `_review_contract_v2_legacy`，不能用于声称新生产链路已通过。
真实模型及业务入口回放脚本：`scripts/run_employment_fact_acceptance.py`。
使用 `--replay-extraction` / `--replay-verification` 时是已捕获模型输出的确定性回归，
不能视为一次新的模型抽取。新合成文本固定在 `backend/tests/fixtures/employment_fact_holdouts.json`。

`scripts/verify_employment_fact_acceptance.py` 校验捕获的最终业务 JSON：预期规则状态、
DeepSeek 来源、逐字 span、已覆盖要素的证据、原文哈希和质量门。

## 2026-09-10 验收记录

- 新事实链路专项测试30项；本次扩展测试总计88项，87通过、1失败。
- 失败项：`test_noncompete_semantics.py::test_actual_file_uses_actual_term_and_compensation`。
  该独立竞业协议仍走未迁移链路；直接调用旧 evaluator 也可复现：测试预期6项、实际7项，
  多出的 `COMMON-23-01` 被该路径的 domain consistency gate 阻断。未修改测试预期或质量门来掩盖该问题。
- 三份新编合成合同（中文金额、跨条款部分覆盖、冲突义务）重新调用真实 DeepSeek，
  经 multipart `/review-v2/file` 和最终 JSON 验证全部 `REPORT_READY`，输入文件哈希未变。
  结果在 `artifacts/employment-fact-holdouts/final-acceptance.json`；不是外部真实合同盲测结论。
- 当前 `102 劳动合同.docx` 通过已登录页面重新上传审查：进程18984，实际工作目录
  `F:\ai\Sage\backend`，新模块源码哈希全部匹配。45条事实、20条规则，`REPORT_READY`。
  EMP-03/06/07通过；EMP-08部分覆盖（安全培训缺失，职业危害事实待核验）；
  EMP-11部分覆盖（依法支付补偿已覆盖，结算期限缺失）。
- 当前输入 SHA256：`0849e6d52ba119f2acc84346eed182d0b4c8eadd7ae9993e422b7fe11ef98d57`。
  完整报告、事实调试和运行证明：`artifacts/employment-fact-acceptance-final/`。
- 前端生产构建通过；现有 chunk size 警告保留。
