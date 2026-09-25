# EMP-05 风险门槛收尾

本轮仅调整 EMP-05 的加班规则重复表述要素及直接不利约定检查。

|实际合同|EMP-05|需要真正修改的风险数|质量门|
|---|---|---|---|
|64 无固定期限劳动合同|PASS|0|REPORT_READY|
|61 正常固定期限劳动合同|PASS|0|REPORT_READY|
|63 北京师范大学复杂劳动合同|PARTIAL / MEDIUM / 建议处理|6（整份合同）|REPORT_READY|

逐规则对比：无固定期限合同仅 EMP-05 状态变化；其余两份合同所有规则状态、严重度及优先级均保持不变。复杂合同 EMP-05 仍缺“工时制度及工作时间”；加班规则不重复列明不再单独计入实际风险。

修改文件：

- backend/review_v2/employment_contract_checklist.py：加班报酬或依法调休要素设为非强制完善项。
- backend/review_v2/priority_contract_review.py：EMP-05 检查直接排除加班报酬、无边界包干、法定节假日仅以调休替代、剥夺休息等不利约定；复用现有否定作用域及证据绑定。
- backend/tests/test_employment_hours_threshold.py：13项正反例，包含保护性否定及差额依法补足的边界。
- backend/tests/test_employment_term_branches.py：更新无固定期限合同 EMP-05 的验收期望。

完整证据、内部审计及报告见同目录 result.json、diagnostics.md、report.md、report.docx、report.pdf；另两份报告分别在 ../hours_fixed 和 ../hours_complex。

法律核验：[劳动法第四十四条](https://www.mohrss.gov.cn/xxgk2020/fdzdgknr/zcfg/fl/202011/t20201102_394625.html)。休息日补休与法定节假日加班报酬分开审查，未因一般法定补位而忽略直接相反约定。

回归：249项覆盖，整组248通过；1条旧测试仍将仅缺加班规则期望为PARTIAL，已更新本轮期望（test_employment_element_severity.py），其所在9项测试全部复跑通过。日志 ../hours_regression.log、../hours_severity_recheck.log。本地后端已在修改后重新启动。
