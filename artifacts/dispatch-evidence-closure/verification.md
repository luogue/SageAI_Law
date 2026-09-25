# 派遣期限与判断证据闭环验收

## 当前合同：REPORT_READY

已重启后端至 PID 23000，并通过 5173 前端代理 /review-v2/file 重新提交未修改的 114 外派岗位劳动协议.docx。

- DSP-01：固定期限；2027-04-01 至 2029-03-31（含终止日），完成两年实际计算，PASS。计算、日期原文均进入报告。
- DSP-03：待核验。证据区展示劳动者正常固定工资 9000 元、对照岗位基础工资约 11500 元，以及薪酬体系条款。工资组成、工作量和计酬口径未确认一致，未判同工同酬违法。
- 最终判断输入 fact IDs 与证据包集合一致，所有引文均在该规则明细的“规则判断证据”区显示。

## 修改与根因

- dispatch_assessment.py：此前无固定期限可直接通过，现明确非固定期限风险；明确不足两年风险；日期缺失、冲突、倒序待核验；可靠日期按日历两年含末日计算，保存计算详情。
- employment_dispatch.py：可比关系须包括同岗位、相同工作量、工资组成及计酬口径。
- priority_contract_review.py：保存规则输入 fact IDs 与已验证证据，不能只保存判断文本。
- employment_report_consistency.py / engine.py：独立渲染判断证据，覆盖证据不再是唯一显示入口；增加 DECISION_EVIDENCE_CLOSURE 门禁，对输入事实集合和逐项引文显示进行对账，缺失即 BLOCKED。
- deepseek_facts.py：新样本暴露可选关系子字段约束未传给模型；现从 Normalizer 的 FIELDS 自动提供子字段约束给抽取和 Verifier，空值仍拒绝，不放宽规则。
- test_dispatch_evidence_closure.py（新增）及 test_dispatch_completeness.py（调整期限预期）。

## 测试

相关自动化回归 196 passed / 0 failed。新增用例包括两年边界、闰日起算、少于两年、非固定期限、缺少日期、删掉已使用证据时门禁阻断、证据包漏事实阻断、未知关系字段可省略但空字符串仍拒绝。

## 新合同泛化：BLOCKED，不能计为通过

新编写 fresh-dispatch.docx，未参与本轮规则修改；原文从首次运行后未改。设计包含 18 个月劳动合同以及同岗、同工作量、同组成口径的较低报酬，目标为检验确定风险分支。

首次和再次请求均因模型输出空 recipient 被 Normalizer 拒绝，失败响应分别保留为 fresh-first-failure.json 和 fresh-second-failure.json。向模型传递真实子字段约束后，空 recipient 问题不再出现；但最新请求在 non_compete.duration_months 抽出字符串 NONE，而数值字段不能用 NONE，继续 fail-closed，尚未进入最终规则报告。最新结构化诊断见 fresh-response.json。

因此只能确认当前合同两处闭环通过，不能宣称全新合同端到端泛化已通过。未修改测试原文、未填默认值、未降低证据或发布门禁。
