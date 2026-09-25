# 竞业限制范围与逐要素证据复核

实际文件：`test_data/60 竞业限制协议.docx`。已走完整 multipart 上传、审查、质量门及 Markdown/Word/PDF 导出流程，也已在当前浏览器重新提交同一文件并核对网页。

## 修改文件与根因

- `backend/review_v2/employment_contract_checklist.py`：原要素把宽泛范围匹配错误提升为“与秘密保护相称”。现拆为业务范围、地域范围的存在事实，保留人员与秘密接触要素，禁止以存在事实直接证明合理性。
- `backend/review_v2/noncompete_semantics.py`：合理性判断纳入岗位、实际秘密接触、公司实际业务等前置事实。缺失时 NC-03 待核验；NC-01 在前置事实不足时断言相称的矛盾进入门禁。
- `backend/review_v2/report_presentation.py`：复用既有原子证据包，生成带要素标签和完整原文的 element_citations。
- `backend/review_v2/engine.py`：无关联风险证据包时，优先展示逐要素证据，替代单条 citation 回退。已有风险证据包与专项证据链路径保持原先优先级。
- `frontend/src/views/ContractReviewV2.vue`：证据定位消费同一逐要素证据集合。NC-02 底层原本有补偿证据，漏项发生于单条 citation 展示分支。
- `backend/tests/test_noncompete_semantics.py`：本轮新增5项测试，与原有9项合计14项，覆盖地域存在不推定相称、充分前置事实、跨规则矛盾、双要素双证据展示、移除证据阻断；原有无补偿及仅通知期反例继续通过。

## 当前六项结果

|规则|状态|
|---|---|
|EMP-01-01|PASS|
|NC-01-01|PARTIAL|
|NC-02-01|PASS|
|NC-03-01|待核验|
|EMP-12-01|PASS|
|EMP-14-01|PASS|

NC-01 仅确认业务/地域存在，不输出“与秘密保护相称”；NC-03 因人员、实际接触秘密及具体岗位事实不足待核验，两者一致。

NC-02 证据定位分别显示：1.1 条离职起2年持续义务；第5项按离职前平均工资30%、每月9,600元补偿原文。网页及导出报告均已核对。

release_quality_gate：REPORT_READY；failures=[]。逐要素展示证据闭合核对见 citation_closure.json；完整要素、候选及最终证据见 actual_element_inputs.json。

## 测试结果及限制

- 竞业及劳动合同、一致性回归：182 passed。
- 其他报告展示、租赁证据回归：23 passed，1 failed。
- 唯一失败 test_report_counts_are_rederived 要求 RELEASE_HOLD/BLOCKED，但实际 REPORT_READY。关闭本轮新增渲染的对照进程仍得到 REPORT_READY、failures=[]，不是本轮渲染引入；未修改该无关旧断言。
- 前端生产构建通过，存在原有分包大小提示。

日志：artifacts/noncompete_scope_regression.log、noncompete_scope_presentation_tests.log、noncompete_scope_baseline_check.log、noncompete_scope_frontend.log。
