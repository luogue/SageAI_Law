# 劳动合同事实校验诊断修复

## 已复现根因

输入为未修改的 `test_data/105 劳动合同.docx`。
SHA256：`1a4fd2b9bfc97c680d266bf392877a01991ef1ed78ac7929b8a59ad7cab23b8f`。

不是单纯 JSON 解析错误。捕获的模型 JSON 可以解析，但包含：

1. `labor_protection.hazard_exists`：`coverage=UNCERTAIN`、`value=null`、
   `assertion=INFERRED`、`confidence=0.5`，引用的是“如岗位涉及特殊职业危害”的条件性约定。
   原 `FactStore -> normalize` 抛出 `EMPTY_EXTRACTED_VALUE`，直接中止整份合同。
2. `coverage.non_compete.arrangement=NONE`：把事实值枚举写进了抽取状态字段。
   旧代码只返回 `INVALID_EXTRACTION_COVERAGE`，未展示原始字段和值。
3. 实际页面重抽取还捕获到 `termination.grounds` 将字符串数组表示为多条字符串事实，
   原归一器按类型错误阻断。
4. 原修复循环只包围首次抽取/入库，没有覆盖独立核验后的第二次入库；JSON 错误又因
   `DEEPSEEK_` 前缀被笼统排除在可修复错误之外。
5. 格式回归发现 parser 对行首粗体只剥离开头星号，可能留下半边 Markdown 标记；
   原绑定器仅使用逐字 substring，不能容忍模型引用里的轻微排版差异。

修复前原始响应、错误和逐字段诊断保存在 `artifacts/employment-105-before/`。

## 修改文件与逻辑

| 文件 | 修改 |
|---|---|
| `backend/review_v2/fact_validation.py` | 结构化错误协议；格式归一和可逆字符映射 |
| `backend/review_v2/deepseek_facts.py` | JSON、响应字段、全文范围、核验结果诊断；同一 DeepSeek 调用 |
| `backend/review_v2/employment_fact_store.py` | 收集逐事实错误；字段/值/证据分类校验；原文绑定；非关键条件事实隔离；单字符串数组表示归一 |
| `backend/review_v2/employment_fact_schema.py` | 声明可安全进入待核验的条件/上下文字段，其余默认阻断 |
| `backend/review_v2/employment_fact_pipeline.py` | 全链路共一次修复预算，包含核验后入库；保留每次诊断和原始响应 |
| `backend/review_v2/clause_parser.py` | 成对处理粗体标记，避免破坏条款正文 |
| `backend/routers/review_v2.py` | 503 返回具体诊断；本地受控审计文件；加入新模块运行哈希 |
| `frontend/src/views/ContractReviewV2.vue` | 持续显示诊断，避免短暂 toast 丢失信息；切换输入清除旧诊断 |
| `backend/tests/test_fact_validation_diagnostics.py` | 格式、字段、真实性、隔离、修复预算和响应诊断回归 |

每个诊断包含 `failed_stage / fact_id / field / validation_rule / model_raw_value /
evidence / expected / actual / disposition`。没有模型 fact_id 时分配候选记录定位 ID。

## 不变的质量约束

- 字符对齐仅容忍空白、换行、成对 Markdown 标记、全半角和排版标点；不进行近似语义匹配、
  不改数字/否定、不跨到其他条款，不剥离脱敏占位符。最终证据使用真实原文切片，保留模型原始引用。
- 原文不存在、条款缺失、来源不真实等失败一律阻断。核心字段异常仍阻断。
- 条件性职业危害事实无法确定时隔离，并按既有条件规则进入人工核验；不能充当保护覆盖或缺失。
- 一个字符串转换为一个数组元素，只改变数据表示，保留原值、证据和归一化记录。
- 抽取、证据绑定和独立核验共用一个修复预算。只调用同一个 DeepSeek；再次失败返回完整诊断，
  不继续重试，不切供应商，不回退关键词。
- 未修改合同原文、法律规则或 release quality gate。

## 验收产物

最终真实页面复测（2026-09-10 18:22，后端进程17388）：39条归一化事实、20条审查项；
15项通过、4项不适用、1项待核验。EMP-08 保留劳动保护和安全培训覆盖，仅需核实实际职业危害。
一次 DeepSeek 同模型重抽取后校验成功，`release_quality_gate=REPORT_READY`，阻断失败为空。
源文件哈希未变，运行实例中新模块源码哈希均与磁盘一致。

新增24项诊断/格式测试；与30项事实链路、29项劳动规则基线合计83项通过。
前端生产构建通过，已有依赖弃用与 chunk size 提示未被隐藏。

- 当前合同真实页面上传结果、源码哈希、原始抽取、规则状态：`artifacts/employment-105-closure/`。
- 定向及劳动规则回归日志：`.runtime-logs/fact-validation-release-tests.log`。
- 前端构建日志：`.runtime-logs/fact-validation-build-final.log`。
