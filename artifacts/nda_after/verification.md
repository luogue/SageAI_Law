# NDA 本轮验收

当前文件：`test_data/71 保密协议.docx`，完整上传入口重新执行。原文 SHA256 为5b423e488330bdac95371bc608a07baaa18cb28d47c5bd5b0897a0aac7ad499d；normalized SHA256 为f0db0bb21d4ad60f16ad8412a48ef969d4ab96f84b7984ba71c50329f0ef3701。

## 实际根因

1. 文档解析与全文传递正常。除外编号清单完整进入 C0008，违约赔偿及其触发列表进入 C0020。
2. NDA-01 原查询要求“除外/不包括”与少量固定词在40/45字符窗口内；编号清单后面的独立开发、法定披露等未通过证据资格判断。现拆分除外子要素，使用完整条款及继承的除外标题上下文，逐项绑定原文。
3. NDA-03 原查询只认“披露方/用人单位：”“接收方/劳动者：”；没有甲乙方实名与信息角色定义的映射，且缺少“接受方”同义词。现分别核对双方实名与披露/接受流向，不将代称直接当实名。
4. NDA-04 原查询要求固定的“违反保密义务”在先、赔偿在后且间隔不超过65字符；正文为长编号条款及“违约情况下，除应赔偿……”结构。现支持违约章节及多种赔偿、补救语义，排除明确免赔的正向误绑。
5. 劳动叙事原按 employment_ 节点前缀选择；劳动违约金规则原按全文出现“员工/雇员”等关键词适用。现使用真实劳动关系/员工协议场景，机构间 NDA 使用中性后果及民法依据，劳动者 NDA 保留劳动场景。信息定义里提到“雇员”不再触发劳动关系。

## 修改文件

- backend/review_v2/nda_semantics.py：新增场景选择、NDA要素解析及模板选择。
- backend/review_v2/employment_facts.py：在现有 resolve_requirements 路径调用 NDA 解析。
- backend/review_v2/priority_contract_review.py：接入场景标记及劳动违约金适用门禁。
- backend/review_v2/engine.py：后果生成按真实 NDA 场景选择，优先于遗留节点前缀。
- backend/routers/review_v2.py：NDA模块及依赖纳入旧代码检测。
- backend/tests/test_nda_semantics.py：新增11项测试，覆盖当前文件、同义表达、编号清单、员工场景、关键词误触发、免赔反例及正反证据冲突。
- backend/tests/priority_contract_fixtures.py：正常 NDA 测试明确补齐原已知悉、合法第三人及法定披露除外，以符合逐要素的正常合同定义；未修改生产样本。

## 当前结果

|规则|最终状态|
|---|---|
|NDA-01-01|PASS|
|NDA-02-01|PARTIAL，建议处理，仅缺资料返还/销毁|
|NDA-03-01|PASS|
|NDA-04-01|PASS|
|EMP-14-01|N/A|
|NC-01-01|N/A|
|NC-02-01|N/A|
|NC-03-01|N/A|

NDA-01/03/04 没有 NOT_FOUND。最终 NOT_FOUND 仅剩 NDA-02 的资料返还或销毁。核心风险及四项 NDA 叙事无劳动关系、劳动者、用人单位模板污染；不适用劳动规则在完整清单中保留规则名称及不适用说明。

release_quality_gate=REPORT_READY，failures=[]。

## 证据和诊断

query_evidence_diagnosis.md 列出修复前后每个 required element 的实际 query、variant 和最终支持原文。

- normalized_input.txt：完整实际输入。
- actual_rule_chunks.json：实际规则 chunks。
- actual_element_inputs.json：实际 query、候选、最终证据及搜索审计。
- actual_applicability_inputs.json：适用性全文输入。
- not_found.json：最终全部负向检索。
- report.md / report.docx / report.pdf：完整报告。

## 测试结果

新增 NDA 测试11/11通过；NDA专题与相关既有导出定向14/14通过。最终广泛回归157通过、5失败。5项集中于原有竞业简化样本和动产质押；关闭本轮 NDA resolve/apply_scenario 的对照进程仍复现竞业 PARTIAL、动产质押 NARRATIVE_EVIDENCE_GATE/EXACT_ELEMENT_REPORT_INVARIANT 阻断。对照日志 nda_unrelated_baseline.log；未修改这些无关领域规则或弱化门禁。

最终日志：artifacts/nda_regression_final.log。

## 违约金基数规则缺口

合同写有“所应投资额的20%”，但全文未给该基数金额或确定方法。现有 sale_liquidated_damages_adjustment 仅识别违约金/比例等计算表述，借款、中介、租赁等模块有各自专用金额规则，NDA 的现有8项没有可直接复用的通用“比例基数是否可确定”检查。

本轮按要求不新增规则。建议在共享违约责任参数解析层增加“比例→基数引用→金额/公式/外部文件可确定性”检查，再由 NDA-04 救济规则关联，避免把“存在赔偿救济”和“违约金基数可执行”混为一项。法律背景可参考[民法典第585条](https://www.court.gov.cn/zixun/xiangqing/233181.html)；基数未明不自动等于全部违约条款无效。
