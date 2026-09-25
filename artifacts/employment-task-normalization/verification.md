# 任务期限劳动合同：归一化与诊断验收

## 原始根因

原始失败响应见 original-failure.json（实际运行实例的历史审计记录）。失败阶段 NORMALIZATION，field=value。

| fact_key | 原始值形式 | 修复后的标准值 |
|---|---|---|
| contract.term_limit_mode | {mode: TASK_COMPLETION} | TASK_COMPLETION |
| contract.term_limit_mode | {mode: EMPLOYER_DETERMINES_COMPLETION, description: …} | EMPLOYER_DETERMINED_COMPLETION |
| capability.compensation（另次失败） | {type: WAIVED, text: …} | WAIVED（仍须核验其是否确属不能胜任解除语境） |

旧 normalizer 直接对 dict 执行 set 成员查询，导致 unhashable type 类型异常，被包装成 INVALID_FACT_VALUE；失败时没有产生 normalized_value。旧期限枚举仅 NONE、CALENDAR_EXPIRY、MAXIMUM_DURATION、EMPLOYER_RENEWAL，不含任务完成事件。这是结构表示适配与业务状态缺失两个问题。

历史来源为第一条 C0004：以项目完成作为终止时间；以及单位自行决定任务是否完成的安排。全部原文和来源在 original-failure.json 的 evidence 中，不在代码中写入项目名、合同句子或日期。

## 修复

- backend/review_v2/fact_enum_normalization.py：按concept映射明确同义值、全半角、大小写及单一value/mode/type包装。多种冲突包装、未知值、非法类型继续失败；不会默认为NONE/UNKNOWN。
- employment_indefinite.py：期限schema加入两个任务完成状态，独立核验器自动读取同一CONCEPTS定义；无固定期限规则继续消费冲突终止机制。
- employment_fact_rules.py：任务合同的单位自行决定完成状态进入EMP-10/16不利终止判断，普通任务完成不报同类风险。
- employment_fact_store.py：归一化事件保留原值/标准值；失败诊断补fact_key、raw_value、normalized_value、allowed_values和真实source_clause。
- backend/routers/review_v2.py：保留503/BLOCKED，统一返回stage、code、fact、field、value、evidence、clause、原因和诊断trace_id。
- frontend/src/utils/api.js、factDiagnostics.mjs、views/ContractReviewV2.vue：统一读取结构化错误，页面独立展示失败历史。按本浏览器用户和页面隔离存储最近20次失败，保留文件名/追踪编号；刷新、重入及后续审查不清空历史。模型完整修复响应不写入浏览器历史，以避免快速耗尽存储。

旧页面仅有临时错误变量，状态切换会清空且没有刷新持久化。本次新增独立持久化诊断列表，不依赖解析弹窗字符串。浏览器存储不可用时明确警告，仍展示内存诊断。

## 验证

- 现有EMP/NC、派遣、无固定期限、FactStore、极性及证据测试：160 passed。
- 新增 test_fact_enum_diagnostics.py：15 passed，涵盖同义/包装、未知与歧义拒绝、完整错误HTTP响应及下游任务终止判断。
- 前端 production build 成功。
- 浏览器自动化模拟503，检查所有诊断字段并刷新页面：通过。见 diagnostics-ui.png；test-ui.cjs保留可重复测试。
- 原109文件未修改，业务multipart处理器及重启后PID 18180的真实HTTP /review-v2/file 均重新调用DeepSeek完成全链路，HTTP 200，REPORT_READY。
- 当前子类型仍为以完成一定工作任务为期限劳动合同；EMP-IP与EMP-14通过，EMP-15任务合同试用期真实风险、EMP-16不利终止风险保持命中。没有回退模型/关键词或修改release gate。

最终本地HTTP响应：live/response.json；用户报告：live/report.md。测试的诊断截图为故障注入场景，当前原合同实际已成功生成报告。
