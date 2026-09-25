# 人工复核与明细状态一致性验收

当前输入：66 完成一定工作任务为期限的劳动合同.docx；沿用原文件，通过现有上传接口重跑。

## 实际结果

|统计项|数量|
|---|---:|
|已覆盖|14|
|部分覆盖|0|
|待核验|1|
|不适用|5|
|审查项总计|20|
|人工复核项（与覆盖状态交叉统计）|1|
|实际风险|0|

EMP-08-01 最终报告状态：待核验。

> 合同文本已覆盖：劳动防护和安全培训。仍需人工核验：核实岗位是否存在职业病危害因素，再确定告知和职业健康保护义务。

处理建议：人工核验后确认本项结论。明细不再显示“已覆盖，无需修改”。

release_quality_gate = REPORT_READY；statistics_consistency_gate = REPORT_READY。

## 通用状态决策

- 文本通过且没有人工核验：通过。
- 文本通过但有待确认条件或人工核验标记：待核验。
- 部分覆盖同时需要人工核验：保留部分覆盖，列入人工核验。
- 风险条款同时需要人工核验：保留风险条款及风险分级，列入人工核验。
- 不适用：不展示为待核验，不保留无效的人工核验展示标记。

报告明细、覆盖统计及全部规则状态使用同一决策函数；新增门禁拒绝人工复核来源中仍为“通过”的规则，以及明细和统计状态不一致。原规则判断、证据和风险处置不变，原文本通过状态记录在 report_status_resolution 中。

## 修改文件

- backend/review_v2/report_statistics.py：通用核验识别、最终报告状态、统计及一致性门禁。
- backend/review_v2/report_presentation.py：不修改原规则对象的最终状态及叙事展示。
- backend/review_v2/engine.py：人工复核记录、Markdown、公开结果及叙事门禁共同使用一致的报告状态。
- frontend/src/views/ContractReviewV2.vue：待核验说明，避免误显示缺失后果或建议新增条款。
- backend/tests/test_manual_review_state.py：23项新测试，覆盖状态优先顺序、非修改性、跨领域、统计反向校验及当前实际合同。

## 实际测试

182 passed，包含新增状态测试、建筑工程52项实际报告统计、通用报告一致性、复杂劳动合同和社保/知识产权风险回归。日志：../manual_state_tests.log。

前端生产构建通过：../manual_state_frontend.log。

重跑报告及导出：report.md、report.docx、report.pdf。逐项结果及完整门禁：result.json、diagnostics.md。

本地后端已重启。前端热更新后当前页面回到上传状态；完整新报告保存在本目录。
