# 风险事实、标题和主题一致性修复

## 根因及生产链路

EMP-10与EMP-16复用同一任务终止事实，但没有向已有adverse_theme_projection传递语义聚合信号，退回按规则分组。EMP-16检查到单一终止风险后仍保留静态复合名称，标题比证据多断言了免补偿。

新增employment_risk_semantics将原文绑定的FactStore事实投影为风险原子。身份由归一化事实、合同范围、主体、对象、法律暴露及整改动作组成，不依赖rule_id、标题相似度、合同日期或固定原文。普通视角和专项视角消费相同原子时，使用已有主题聚合器合并，底层命中仍分别保留。不同法律问题即使位于同一条款也不因位置相同而合并。

标题、风险描述及正式建议从实际支持的风险原子生成：只有单方终止证据时使用单方终止名称；有独立补偿排除事实时才增加相应结论及其证据。没有删除EMP-16，也没有将缺失证据人工补为有效。

## 修改文件

- backend/review_v2/employment_risk_semantics.py：事实原子、标题/结论/建议投影、证据一致性校验。
- backend/review_v2/employment_fact_rules.py：不利事实结果携带原子信号。
- backend/review_v2/priority_contract_review.py：在规则明细进入聚合前生成与证据一致的名称及结论。
- backend/review_v2/engine.py：release gate加入RISK_TITLE_EVIDENCE_CONSISTENCY；标题、结论超出已验证证据则BLOCKED。
- backend/tests/test_employment_risk_semantics.py：单一/复合证据、故意扩大标题、删除证据、重复事实聚合、最终报告回归。

既有聚合器负责最高严重程度和优先级、related_rule_ids及证据包保留。本次未修改质量门既有条件，也未修改原始合同或FactStore抽取结果。

## 验证

整组179项通过；最后正式建议同步调整后，专项4项再次通过。覆盖EMP/NC、派遣、无固定期限、归一化、极性及证据原文绑定。

原109合同经multipart业务入口及重启后的真实本地HTTP入口重新调用DeepSeek。最终结果见live/response.json、live/report.md及acceptance.json。

预期独立问题为三个：任务合同违法试用期、单位单方认定任务完成并终止、项目完成后排除经济补偿。EMP-10和EMP-16继续是两个规则命中，合为一个终止风险主题；EMP-11独立保留补偿风险证据。
