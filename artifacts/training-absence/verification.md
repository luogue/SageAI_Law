# 培训负向事实核验修复

当前业务接口 POST /review-v2/file：HTTP 200，release_quality_gate=REPORT_READY。
使用原 test_data/111 小时制用工协议.docx，未修改前端、合同或数据库。

根因：原模型把普通安全培训引文绑定到服务期NONE；Verifier正确拒绝，但原协议没有全文缺失纠正通道，拒绝状态持续阻断。重试诊断原先只到抽取器，未到Verifier。

修改：
- employment_fact_schema.py：分别定义专项技术培训、费用、服务期、服务期违约金及普通劳动保护培训；声明负向安排的审计范围。
- deepseek_facts.py：DeepSeek验证协议加入absence_audits，要求全部条款和相关概念检索；重试反馈送达Verifier。
- fact_verification.py：校验审计覆盖范围、明确结论、理由、冲突和不确定事实；通过后投影VERIFIED_ABSENT。保留被拒事实ID和审计，不伪造合同引文。
- employment_fact_store.py：经过全文审计的缺失安排可读为NONE，不作为正向原文事实或保护覆盖。
- employment_fact_pipeline.py：贯通修复反馈；保留后续规则适配异常的上游gate及事实诊断。
- domain_selection.py：本次真实复测另发现旧分类将已验证的劳动用工关系覆盖成sale；以当前已验证、原文绑定的用工关系保留劳动规则路由，未改变各EMP/NC法律规则。
- tests/test_training_absence_verification.py：安全培训错误NONE纠正、明确无服务期、技术培训无服务期、培训费用服务期、服务期违约金、不完整审计阻断、冲突阻断、不确定相关事实阻断、Verifier收到修复反馈及已验证分类不被覆盖。

当前合同：安全培训原文只作为labor_protection.training；training.arrangement引文被拒后，全部15个条款的审计确认NONE，事实证据数组为空，审计证据独立保留。EMP-09不适用；LABOR_PART_TIME；PT-01至PT-07全部通过。

测试：最终相关集合143 passed（见tests-final.txt）。扩展task_term集合曾有EMP-11旧断言要求通过、实际部分覆盖的单项失败（该次115 passed / 1 failed），没有修改该规则或断言，也不把它算成全量通过。

验收证据：live/response.json、live/report.md、acceptance.json。数据库独立故障不在本轮处理范围，REPORT_READY仅是合同报告质量门。
