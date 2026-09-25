# 股东合作协议最终收尾验收

当前阶段：通过。完成主题去重与条件元数据收尾；不再针对该测试文本继续迭代。

## 根因与修改

上位覆盖规则和专项风险缺少共享的原子风险身份，主题聚合仍沿用各自规则指纹；非技术类摘要、优先修改及总览卡片也使用规则级计数。CF-15 沿用了禁止性规则的始终适用默认值。

检测器生成有证据支撑的事实、范围、当事人、对象、法律暴露和整改动作身份。聚合器通过相同身份连接命中，上位多事实命中可以连接对应专项命中；不使用规则ID、标题、当前合同名称或同条款位置直接合并。不同位置的同一风险保留所有证据，相同条款的独立风险不合并。不完整或未知身份拒绝自动合并。

严重程度和优先级取组内最高；规则明细、规则级命中、related_rule_ids、evidence_ids、evidence_packages 均保留。建议按事实整改动作去重合成。摘要、建议优先修改和总览使用同一主题结果；统计门禁分别核验规则数与主题数，并校验成员闭合、最高等级和最高优先级。

CF-15 三个前提必须同时成立：有限责任公司、多股东、不设股东会机关。未触发为不适用，仍为 adverse-clause detector，不是缺失检测。CF-11至CF-14也仅修正明显的直接不利约定触发元数据。

## 修改文件

- [adverse_theme_projection.py](F:/ai/Sage/backend/review_v2/adverse_theme_projection.py)
- [company_governance_facts.py](F:/ai/Sage/backend/review_v2/company_governance_facts.py)
- [company_formation_checklist.py](F:/ai/Sage/backend/review_v2/company_formation_checklist.py)
- [priority_contract_review.py](F:/ai/Sage/backend/review_v2/priority_contract_review.py)
- [engine.py](F:/ai/Sage/backend/review_v2/engine.py)
- [report_statistics.py](F:/ai/Sage/backend/review_v2/report_statistics.py)
- [review_v2.py](F:/ai/Sage/backend/routers/review_v2.py)
- [test_adverse_theme_projection.py](F:/ai/Sage/backend/tests/test_adverse_theme_projection.py)

## 自动化测试

新增13例：parent+specific、相似标题不同事实、同风险不同位置、同位置不同暴露或整改动作、跨对象不合并、多事实上位连接、五组CF-15前提、两组完整报告不触发，以及同一原文生产上传与摘要/卡片/门禁一致性（参数化总数13）。

最终主回归259 passed；股权专项28 passed；合计287 passed。买卖合同、股权转让、增资、普通股东协议回归正常。全仓所有测试未执行。

## 同一完整原文生产结果

- 原文件：83 投资协议.docx，原文3924字；未截断或替换内容。
- 原文件SHA256：8bdcbca80dba56ef998d4511d939bbca4ce4bf514895117042f33a1e3e502f12。
- contract_type=shareholders；scenario=股东合作协议；role=equity_party（股权协议当事人）。
- 完整审查规则26；规则级风险命中21；聚合风险主题19。
- 重大/中等/低风险：8/5/6；优先/建议/可选：4/9/6。
- CF-05/12/15均保持风险条款，在完整明细中分别存在，最终聚合为1个治理风险主题。
- 聚合后的建议：建议保留多股东有限责任公司的股东会机关，区分机关设置与全体股东书面一致决定时可不召开会议；删除或限制重大事项的单方最终决定及跳过协商授权，明确合法表决与僵局解决机制。
- CF-15最终适用条件：同时涉及有限责任公司、存在多名股东且约定不设股东会机关时适用；一人公司、不召开会议或未约定该不利安排时不适用。
- 一人公司、不召开股东会会议、未讨论股东会、非有限责任公司均不触发。
- 真实模型 multipart 生产入口复测：release_quality_gate=REPORT_READY；统计门禁=REPORT_READY。

详见同目录 result.json、summary.json、report.md、closeout.json。

实际页面最终复测：CR-20260909-075755-D8EF50，PID 12920，CURRENT，REPORT_READY；页面总览8/5/6、4/9/6，治理主题摘要仅一条。前端5173与后端8016均已恢复并运行。
