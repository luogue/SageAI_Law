# 解除终止协议精度收尾

仅修改三个文件：
- backend/review_v2/priority_contract_review.py：解析“本条”父级作用域，区分仅竞业/专项培训与一般义务；同时绑定 PENALTY_CLAUSE 和 COVERED_ORDINARY_OBLIGATION，记录共同 scope_evidence_ids；风险理由明确是作用域而非金额。
- backend/review_v2/employment_facts.py：仅解除终止目的下，将住所要素标记 OPTIONAL、risk_relevant=False；使用副本，不改变 ordinary employment 原始规则配置。
- backend/tests/test_termination_agreement.py：新增9项测试，覆盖金额变化、仅竞业/服务期、不同父条款、明确限定范围、混合义务双证据、住所策略不泄漏及完整报告。

94项回归全部通过，日志 ../termination_closeout_tests.log。
当前74号协议 REPORT_READY、failures=[]。相较上轮，仅EMP-01从部分覆盖变为核心通过，住所保留可选完善说明；其余17项状态不变。
EMP-14仍为风险条款：第8条（4）违约金与第8条（2）一般保密义务一起作为证据。并非因金额20万元而认定违法。
普通64号无固定期限劳动合同真实文件重跑：REPORT_READY，0实际风险；结果 ../termination_closeout_ordinary/result.json。

当前中等风险由3减为2，建议处理由3减为2；其余实际风险继续保留。
完整证据 closeout_evidence.json，完整报告 report.md。
本阶段 termination_agreement 测试收口。
