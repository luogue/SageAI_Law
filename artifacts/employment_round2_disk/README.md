# 同一劳动合同第二轮核验

输入仍为 `F:\ai\Sage\test_data\57 劳务派遣.docx`，SHA256 为 `253e17e70d97c328540acb7fdc16eff5f01d315e074ea326e2135ed7add15ab4`，与上一轮完全一致。未改写、拼接或替换合同。

## 原文差异是尚未完成验收的原因

逐一检查该 DOCX 全部 XML 文本（拼接拆分的文本节点）后，未找到“补休或支付加班工资”“办结工作交接时支付”、第二十三条及第二十四条。现存文件是“合同基本信息、甲方信息”等结构化内容，不是用户本轮描述的二十四条完整合同。见 `input_verification.json`。已请求同一合同完整版本的本地路径。

用户提供的条款用于独立回归测试，没有被当成磁盘合同的提取证据。

## 已修复

- EMP-05：识别先补休/调休、后支付加班工资的可选履行表达；原文匹配成功时不产生 NOT_FOUND 证据。
- EMP-12：识别“申请调解或仲裁”和劳动人事争议仲裁机构。
- EMP-10：识别法定解除终止及派遣届满/依法退回后的重新派遣；通知或解除日期独立判断。
- EMP-11：识别办结工作交接时支付经济补偿这一结算节点；缺少金额/计算标准时部分覆盖。
- 负向通过项不再生成正向必备占位要素，不挂入风险发现，不参与缺失要素聚合；搜索记录明确为 ADVERSE_CLAUSE_SEARCH / NO_ADVERSE_CLAUSE_FOUND。新增一致性门断言阻止污染再次出现。
- 风险摘要展示严重程度和处理建议的区别；高严重程度但非优先处理时展示已有合同保护。统计仍分别由风险发现和最终处置反算，没有人为把两个数字改成相等。

## 现存文件真实重审结果

质量门为 REPORT_READY，适用子门 PASS，failures=[]。

| 规则 | 实际结果 | 原因 |
|---|---|---|
| EMP-05 | PARTIAL | 此文件未包含本轮引用的加班补偿句 |
| EMP-10 | PARTIAL | 重新派遣已有证据，通知或明确解除日期尚缺 |
| EMP-11 | MISSING | 此文件未包含经济补偿及工作交接支付条款 |
| EMP-12 | PASS | 已明确劳动人事争议仲裁机构 |
| EMP-13 | PASS | 无不利条款，不再进入社保风险摘要及证据包 |

所以不能把“质量门通过”说成“用户本轮全部验收项已完成”。须取得包含所述条款的完整原合同，再按同一上传链路验收 EMP-05/11。

产物：`result.json` 为完整响应，`summary.json` 保留全部要素及 gate，`report.md / report.docx / report.pdf` 使用现有导出链路。

## 修改文件

- `backend/review_v2/employment_contract_checklist.py`：劳动专项匹配。
- `backend/review_v2/engine.py`：负向通过要素/聚合边界、负向检索说明、摘要严重程度与处理次序。
- `backend/review_v2/report_state_consistency.py`：负向通过聚合污染的阻断检查。
- `backend/tests/test_employment_round2_semantics.py`：本轮新增回归。

## 测试

其他合同及一致性测试：310 passed、2 failed。失败为上一轮已存在的建设工程部分覆盖断言和房屋租赁质量门断言（`../employment_round2_legacy.txt`）。未改这些规则或测试来消除失败。

共享代码在测试期间被其他任务修改，文件上传测试正确触发 STALE_REVIEW_RUNTIME。为保持该保护，复制代码快照到 `../employment_round2_snapshot` 复跑，而没有禁用源码漂移检查。快照复跑 **136 passed**，包括本轮新增 9 项测试、上轮 29 项劳动测试和 98 项新增类型测试。结果见 `../employment_round2_snapshot_tests.txt`。
