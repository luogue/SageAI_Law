# 无固定期限劳动合同专项验收

## 根因

原 FactStore 只有合同声明期限类型和起止日期，缺乏“另行固定终止、最长期限、由单位决定续签”的独立法律语义。EMP-16 原有判断依赖 employer_unrestricted 等笼统事实，无法稳定消费以不能胜任为名排除前置程序的约定。

## 修改文件与链路

- backend/review_v2/employment_indefinite.py：新增独立 OET-01-01 期限风险规则、期限上限与不能胜任解除事实定义、确定性判断。
- backend/review_v2/employment_fact_schema.py：注册事实和允许的类型。
- backend/review_v2/employment_fact_store.py：无固定期限专项适用性及不确定事实的自然语言复核提示。
- backend/review_v2/employment_fact_rules.py：EMP-16 与 EMP-10 消费不能胜任解除的不利事实，风险优先于覆盖。
- backend/review_v2/contract_registry.py：在普通 EMP/NC 基础上按已验证期限类型叠加 OET；与派遣形式独立组合。
- backend/review_v2/employment_fact_pipeline.py：保留专项决策调试记录。
- backend/tests/test_employment_indefinite.py：16项测试，包括最终报告、六个月试用、否定极性、培训或调岗二择一、跨段证据及内部枚举不泄漏。

期限声明继续采用兼容的 INDEFINITE（无确定终止时间）事实值；固定终止机制独立保存，不将相互冲突的条款改写成普通固定期限。培训与调岗是替代前置措施，不能因缺其中一项就认定违法；排名末位不等于实质不能胜任，未提及程序与明确排除程序也分别处理。所有判断使用核验后的 FactStore，无新增原文关键词匹配。

依据核对：[劳动合同法第14、40、46条](https://www.mohrss.gov.cn/xxgk2020/fdzdgknr/zcfg/fl/202011/t20201102_394622_wap.html)。

## 完整复测

原始文档：test_data/108 无固定期限劳动合同.docx，未修改。已通过 /review-v2/file multipart 业务处理器重跑，又在重启后的本地服务 PID 17684 上使用短效本地测试身份，经真实 HTTP 端口8016重跑；没有放宽鉴权或质量门配置。

- 分类：无固定期限劳动合同。
- OET-01-01：第一条最长期限及自动终止风险命中。
- EMP-16-01：第十三条排名末位直接不能胜任、立即解除、排除培训调岗和补偿风险命中。
- EMP-10-01：存在风险条款，不再纯正向通过。
- EMP-IP-01、EMP-14-01、EMP-15-01：通过；六个月试用未误报。
- EMP-08-01：仅保留实际职业病危害因素的外部事实核验。
- 最终质量门 REPORT_READY，failures 为空；报告未泄漏本次内部枚举。

自动化整组158项通过；新增两个自然语言复核提示断言后，专项16项再次全部通过。普通106重新调用DeepSeek的20项结果与上轮逐项一致，无OET；派遣107的28项中四个DSP风险仍命中，无OET，EMP-IP/14/15通过；两份回归质量门均为REPORT_READY。

最终报告：live/report.md；HTTP响应：live/response.json；生产断言：acceptance.json。current、ordinary、dispatch目录保留业务回归原始模型输出、验证结果及报告。
