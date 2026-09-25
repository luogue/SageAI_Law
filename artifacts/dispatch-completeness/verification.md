# 劳务派遣审查完整性验收

2026-09-11 16:18（北京时间），通过前端代理业务接口 POST /review-v2/file 重跑未修改的 `114 外派岗位劳动协议.docx`。

- trace：CR-20260911-161838-CB0B28
- 当前后端 PID：4268，工作目录 F:/ai/Sage/backend；启动时加载的代码哈希见 runtime-files.json。
- 原文件 SHA256：6df4e8f587aec49db0906d019dda4d16c0ec09620641682dc99e7c4c0d99a9b9。
- 分类：劳务派遣劳动合同；31 条规则；71 个事实经 DeepSeek 核验，128 个概念纳入检索。
- release_quality_gate=REPORT_READY；6 个独立风险主题、7 个规则命中，重大/中等/低风险=6/0/0。

## 根因及修改

1. 主体 schema 缺少法定代表人/主要负责人、劳动者住址；已补充到 EMP-01。新增 EMP-17-01 独立核验正常劳动报酬、支付日期、支付方式；不使用试用工资替代正常工资。非全日制继续由专用计酬规则替代。
2. DSP-01 原只检查派遣期限，新增根据已验证劳动合同类型、期限或起止日期计算不少于两年，拒绝以派遣期间代替劳动合同期间。本合同 2027-04-01 至 2029-03-31，符合两年。
3. DSP-03 原以差别待遇枚举推断较低，缺少双边报酬、可比口径。新增对照工资、双边报酬分配办法和可比事实；区分 DIFFERENT_SYSTEM 与 LOWER_ALLOWED，并检查单位及工资组成。当前抽到劳动者固定工资 9000、对照基础工资 11500，但未证实相同组成口径，因此待核验，未确定为实际低于。封闭比较事实的测试仍产生风险并绑定双边证据。
4. DSP-02 原把长期岗位直接当作三性全部不符。现在分别判断临时性、非主营辅助及认定程序、替代暂时离岗人员。只有三者均被排除才确定风险；本合同有常设主营、非临时替岗原文，所以保留风险。单独长期事实仅待核验。
5. 金额影响以前没有消费已验证保证金金额。现从 worker.security_payment 生成 1500 元直接经济影响，不将其自动视为最终损失；EMP-06/DSP-05 仍聚合成一个收费主题。
6. 形式覆盖和合法性以前未协调。新增 coverage_legality 关联，同一原文支持专项风险时，普通覆盖项明确“形式要素已覆盖，但相关约定存在风险，见 DSP-06-01、DSP-10-01”。最终显示门禁禁止恢复“无需修改”。事实、规则命中保持独立。
7. 专项合法性未知通过现有外部事实核验类型进入覆盖聚合，形式事实仍独立计算；未降低门禁。期间发现最终证据检查只匹配 evidence_id、遗漏 clause_id 命名空间，已修正双标识关联，仍要求真实原文出现在最终明细。

## 修改文件

- backend/review_v2/employment_fact_schema.py
- backend/review_v2/employment_contract_checklist.py
- backend/review_v2/employment_rule_adapter.py
- backend/review_v2/employment_dispatch.py
- backend/review_v2/employment_fact_store.py
- backend/review_v2/dispatch_assessment.py（新增）
- backend/review_v2/employment_fact_rules.py
- backend/review_v2/priority_contract_review.py
- backend/review_v2/employment_report_consistency.py（新增）
- backend/review_v2/final_context_consistency.py
- backend/review_v2/engine.py
- backend/tests/test_dispatch_completeness.py（新增）
- backend/tests/test_employment_dispatch.py（调整预期）

## 当前风险及核验事项

1. 违法向劳动者收取保证金或从工资扣收费用（EMP-06 + DSP-05，一个主题）。
2. 派遣岗位三性不符（DSP-02）。
3. 退回后重新派遣与解除条件过宽（DSP-06）。
4. 排除派遣协议相关内容告知（DSP-07）。
5. 用工单位再次派遣（DSP-09）。
6. 用工单位退回条件过宽（DSP-10）。

待核验两项：EMP-08 岗位实际职业危害因素；DSP-03 工资组成和计酬可比口径。其余已通过项目保持；EMP-14 不将保证金误作违约金。

## 验证

- 新增 20 个自动化用例：分别三性、同岗双边工资、不同组成不能比较、差异体系、不同证据位置、两年期限边界、劳动期限与派遣期限区分、主体字段、正常报酬与试用报酬隔离、金额及去重、跨规则冲突提示和旧标签阻断。
- 最终相关回归：188 passed，0 failed（final-tests.txt）；覆盖 EMP、DSP、PT、无固定期限、FactStore、IP、风险聚合和批量核验完整性。未宣称运行全仓库测试。
- 最终业务输出 acceptance.json 中所有断言通过；报告见 report.md，完整 JSON 见 response.json。
- 未修改合同、未切换模型、未关闭或降低质量门。

法律核验依据：[劳动合同法](https://www.mohrss.gov.cn/xxgk2020/fdzdgknr/zcfg/fl/202011/t20201102_394622_wap.html)、[劳务派遣暂行规定](https://www.beijing.gov.cn/zhengce/zhengcefagui/qtwj/201403/t20140301_781261.html)。
