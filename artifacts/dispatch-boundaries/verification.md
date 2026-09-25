# 劳务派遣专项验收

根因：原DSP只判断重新派遣后的解除，没有建模再次派遣的主体流转与原用工单位退回事由；保证金未有独立收费事实，旧违约金schema还把“不属于违约金”引导为imposed=false，形成伪否定事实。

修改文件：backend/review_v2/employment_conditions.py（新关系事实与严格对象验证）、employment_dispatch.py（DSP-09/10与收费事务选择）、employment_fact_rules.py（工资扣收消费同一保证金事实）、employment_fact_schema.py（违约金和保证金语境区分）、employment_risk_semantics.py（事实主题投影）；backend/tests/test_dispatch_boundaries.py及test_employment_dispatch.py。

新增事实：dispatch.onward_assignment（派遣单位、当前用工单位、新主体、实施者、主体是否变化、处理方式、是否允许）；dispatch.return_terms（每个退回理由、类型、法定条件约束、原文阈值）；worker.security_payment（收款主体、可退还性质、收费及工资扣收、金额、退款条件）。均通过现有DeepSeek→Normalizer→Verifier→FactStore，规则不搜索样本关键词。

新增DSP-09-01、DSP-10-01；DSP-05-01和EMP-06-01共享收费事实。EMP-14仅消费真正违约金事实，不以押金名称或退款条件推断违约责任。

114合同同源业务接口POST /review-v2/file：HTTP200，REPORT_READY，劳务派遣劳动合同。7主题、8规则命中。保证金主题包含DSP-05和EMP-06；EMP-14通过，penalties.obligations为空。DSP-09、DSP-10证据已绑定。其余风险保留：岗位三性、同工同酬、重新派遣解除、派遣协议告知。无工作期间报酬、主体岗位期限、义务分工依当前文本通过。EMP-08仍有既有待核验，不声称所有条款均通过。没有PT/OET污染。

新增12个泛化测试（含最终报告），相关回归153通过；最后schema措辞修正后44个DSP及边界测试再次通过。合同未修改，Verifier和发布门禁未放宽。完整报告report.md，事实及验收acceptance.json。

法律依据：[劳动合同法](https://www.mohrss.gov.cn/xxgk2020/fdzdgknr/zcfg/fl/202011/t20201102_394622_wap.html)第62、65条；[人社部对劳务派遣暂行规定的说明](https://www.mohrss.gov.cn/ldgxs/LDGXhetong/ldht/201401/t20140127_123361.html)。
