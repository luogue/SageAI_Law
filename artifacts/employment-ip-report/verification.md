# 劳动成果与知识产权归属报告验收

- 当前文件：106 劳动合同.docx，原文件未修改。
- 业务入口：页面“开始审查” → /review-v2/file → DeepSeek 全文抽取及核验 → FactStore → 规则 → 最终报告。
- 新后端进程：23832，端口 8016；本轮代码已加载。
- EMP-IP-01：通过，第十一条劳动成果与知识产权归属为直接证据；不再将内部对象结构或枚举作为用户文案。
- 全文未约定：缺失／可选优化；明确的归属安排正常绑定原文；真实歧义保留待核验；直接不利归属保留风险判断。
- release_quality_gate：REPORT_READY，failures=[]。
- 自动化回归：112 passed，包含四种 IP 最终报告状态测试。
- 三份历史 DeepSeek 事实快照回放：除 EMP-IP-01 外所有规则状态一致，三个最终报告均 REPORT_READY。
- 本次实时重新抽取中 EMP-14 从风险条款变为通过。旧版将“本合同未约定普通离职违约金”抽成违约金义务；本次无此正向义务事实。未修改 EMP-14 规则；其他非 IP 项状态一致。

根因：模型 schema 说明曾直接拼入待核验文案；旧 IP 禁止性检查没有独立的归属约定覆盖要素；最终建议按“知识产权”标题一律升级，未区分普通归属约定缺省与实际侵权暴露。

修改：employment_contract_checklist.py、employment_fact_schema.py、employment_fact_store.py、priority_contract_review.py、engine.py；新增 test_employment_ip_report.py。质量门未放宽。
