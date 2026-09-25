# 竞业限制协议复核记录

本轮使用 `test_data/60 竞业限制协议.docx`，通过 FastAPI multipart 上传入口完整执行，并生成 Markdown、Word、PDF 报告。实际输入与用户描述的缺失版本不同：第1.1条有离职起2年竞业期限，第5.1条有离职前月平均工资30%、每月9,600元补偿。不能把这些实际条款判缺失。浏览器当前为另一份保证合同，本次没有替换页面合同。

## 根因及修改

- `backend/review_v2/employment_contract_checklist.py`：补齐“身份证号”及脱敏号码的身份要素匹配；竞业期限只接受持续义务语义，补偿标准支持带千位分隔符的金额与按月表述。
- `backend/review_v2/noncompete_semantics.py`：新增竞业持续期、提前通知期、解除期、支付周期、违约履行期的角色诊断；NC-03 根据前置规则事实完整性进入待核验；跨规则无条件通过冲突进入一致性门禁。
- `backend/review_v2/priority_contract_review.py`：在既有专项审查路径接入前置事实核验及期限角色诊断。
- `backend/review_v2/lease_semantics.py`：在既有一致性门禁接入竞业跨规则检查，保留已有正向证据/NOT_FOUND 冲突检查。
- `backend/routers/review_v2.py`：把新增语义模块与竞业实际依赖加入运行时版本检查。
- `scripts/run_employment_file_acceptance.py`：复用原有全链路验收工具，支持指定合同类型。
- `backend/tests/test_noncompete_semantics.py`：新增9个参数展开后的回归用例，覆盖身份脱敏、通知期排除、真实持续期、补偿缺失、五类时间角色、跨规则矛盾阻断、直接风险保留、实际文件全流程。
- `backend/tests/test_employment_standard_contract.py`：同步此前人工核验状态修复的旧断言；明确 EMP-08 文本义务已覆盖、职业危害事实待核验，不改规则。

## 实际文件六项结果

|规则|最终状态|结论|
|---|---|---|
|EMP-01-01|PASS|姓名、脱敏身份证号等身份要素已覆盖，无身份缺失 SEARCH_AUDIT|
|NC-01-01|PARTIAL|人员范围及实际接触秘密尚不明确|
|NC-02-01|PASS|证据为第1.1条2年持续期、第5.1条每月补偿；第6.2条提前1个月通知不作为竞业期限|
|NC-03-01|待核验|承接 NC-01 事实缺口，不再无条件 PASS，也不把事实不足直接定为违法|
|EMP-12-01|PASS|争议解决要素覆盖|
|EMP-14-01|PASS|未发现对应禁止性约定|

release_quality_gate = REPORT_READY，failures = []；各执行质量门通过。

仅含提前通知解除、没有竞业持续期与补偿标准的反例：NC-02 = 缺失，NC-03 = 待核验；明确离职后12/24个月但没有补偿标准的反例：NC-02 = 部分覆盖。人为制造正向证据与 NOT_FOUND 冲突、前序缺失与 NC-03 无条件通过冲突，均被一致性校验识别。

## 可追溯产物

- `normalized_input.txt`：实际归一化输入。
- `actual_rule_chunks.json`、`actual_element_inputs.json`：规则全文、检索要素、候选证据、最终证据与搜索记录。
- `not_found.json`：全部 NOT_FOUND，仅剩 NC-01 人员及实际秘密接触要素。
- `result.json`、`summary.json`：完整审查及质量门结果。
- `report.md`、`report.docx`、`report.pdf`：完整报告。

测试结果：275项用例全部获得通过结果（主批次263通过；12个上传用例因运行期间 engine 等文件变化被旧代码门禁阻断，新进程单独复跑12/12通过）。没有关闭或模拟绕过旧代码门禁。日志为 `artifacts/noncompete_tests_final.log` 与 `artifacts/noncompete_upload_final.log`。另一条旧 EMP-08 通过断言已与此前验收的人工核验语义同步。
