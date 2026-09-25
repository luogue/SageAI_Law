# 保管合同定向回归记录

本轮使用原文件 `test_data/82 保管合同.docx`，未修改样本。最终通过页面实际调用 `/review-v2/file`，保留大模型复核开启。实际服务 PID 16180，审查编号 CR-20260909-063535-766E78，运行指纹检查 CURRENT，HTTP 200。完整指纹及文件 SHA256 见 consistency-audit.json。

## 根因及修改

1. 费用不明补充规则没有消费基础费用已确定的事实。新增通用 `unless_fact_concepts` 前提配置，依据可定位事实先判适用性，并保留 premise_evidence；未触发的规则不进入缺失风险。报酬金额必须直接修饰费用计算，违约金、例示金额不能充当报酬已确定的证据。
2. 转交第三人责任未区分授权场景。配置未经授权损失赔偿、经授权后责任两个独立概念；同一源句可被限制转交和损失责任规则复用，最终按全部原子状态聚合。
3. 无偿过错责任仍走宽泛候选片段。改用完整法律命题的源句绑定，选取真正包含无偿、故意或重大过失责任标准的后句。沿用通用 supports 校验与展示引文门禁，不修改 renderer。
4. 适用性结果增加条件状态及前提证据，质量门检查未触发事项不得输出缺失风险；保留共享事实、SEARCH_AUDIT、逐要素聚合和展示证据一致性校验。

本轮同时修改声明式规则配置和通用引擎，未通过 rule_id 强制结果。全部49项适用性输出见 applicability-audit.json；该表记录现有规则的实际前提结果，不代表新建了全部法律场景的事实分类器。

## 修改文件

- backend/review_v2/house_lease_checklist.py：通用前提字段。
- backend/review_v2/shared_fact_concepts.py：费用确定性、授权场景责任、无偿过错标准概念。
- backend/review_v2/safekeeping_contract_checklist.py：声明式概念/前提绑定。
- backend/review_v2/engine.py：先前提后覆盖，前提证据及状态输出。
- backend/review_v2/lease_semantics.py：未触发规则一致性断言。
- backend/tests/test_fact_condition_followup.py：18个新增参数化测试用例。
- backend/tests/test_safekeeping_review_checklist.py：明确费用场景的N/A统计预期。
- scripts/run_safekeeping_acceptance.py：扩展回归明细输出。
- scripts/audit_safekeeping_followup.py：审计真实入口结果，原样保存报告及49项适用性结果。

## 测试

本轮新增18例。与共享事实、保管规则、保管结构及违约金基数回归合计84例全部通过，5条已有警告。覆盖确定/不确定/免费/例示/违约金负例、不同授权场景、同源跨规则复用、后句证据完整性、普通过失不能证明无偿标准、部分覆盖聚合及正负审计一致性。

## 最终结果

|规则|结果|证据或剩余缺口|
|---|---|---|
|D-04-04|N/A|第四条（一）每月2000元及按实际天数折算，费用不明前提不成立|
|D-08-03|PARTIAL|第十一条（五）未经同意转交第三人造成损失的赔偿责任已覆盖；经授权转交后的对外责任仍缺失|
|D-07-02|PASS|第十一条（一）完整后句，见下|

转交责任原文：“（五）乙方未经甲方同意，将保管物转交第三人保管，造成保管物损失的，应当承担损失赔偿责任。”

无偿责任原文：“无偿保管的，乙方证明自己没有故意或者重大过失的，不承担赔偿责任。”

上一轮 D-01-03、D-02-03、D-07-01、COMMON-20-01 保持PASS；D-09-03保持N/A；D-12-04保持PARTIAL。

49项：37 PASS + 3 PARTIAL + 3 MISSING + 6 N/A。重大0、中等3、低3；优先处理0、建议处理3、可选优化3、人工复核0。详细统计及生产指纹见 consistency-audit.json。

本轮自动审计未发现 FOUND/NOT_FOUND、共享事实投影、逐要素覆盖、条件未触发计风险或目标引文冲突。最终生产质量门 `REPORT_READY`，failures为空。完整生产报告见 report.md，完整原始响应保留在 result-16180-d28078968ac44d1c91810c53c822021f.json。
