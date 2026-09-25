# 解除/终止协议结构化事实链路验收

## 根因与修复

- employment_termination 未注册 ACTIVE employment fact family，业务入口落入旧规则/原文检索链路。EMP-01 未消费当前统一 verified FactStore，原文缺劳动者住址仍出现覆盖声明。现接入事实主链路，缺失地址不生成事实，EMP-01 保留所有适用主体要素，结果部分覆盖。
- NC 期限、地域、业务范围及 EMP-14 漏检：同一未接入原因，已有事实schema和确定性消费者原本没有被执行；此次复用既有能力，没有金额或句子特判。
- 证明、档案/社保/公积金转移及 ET 风险：除入口外，还缺独立事实定义、要素映射和 termination_ 前缀适配。新增 exit_settlement 模块，ET规则只读取核验事实。
- 工资与补偿期限：原共享 settlement_deadline 容易只保留一种付款安排；解除协议改用两个独立概念和要素，不以补偿日期替代工资日期。
- 报告声明覆盖的任何已映射要素，必须能在同一最终明细找到 verified 原文；新增公共 REPORT_PROJECTION 校验，没有有效事实或展示证据时阻断。
- 形式覆盖与关联不利条款分开：EMP-11 确认付款条款已写，但最终建议引用 ET-04，后续通用建议不再重置为无需修改。

## ET-04 法律边界

没有把“补偿与交接挂钩”本身一律判违法。代码区分已赚工资扣留、办结交接时支付补偿、办结后额外延期；本案绑定第三条额外20个工作日与第六条暂缓条款。依据[劳动合同法第五十条](https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/bgt/art/2023/art_0abfdd261c03417b949df19d869add8d.html)及现有清单，不删减门禁。

## 修改文件

- [fact_module_registry.py](F:/ai/Sage/backend/review_v2/fact_module_registry.py)
- [termination_facts.py](F:/ai/Sage/backend/review_v2/termination_facts.py)
- [employment_fact_schema.py](F:/ai/Sage/backend/review_v2/employment_fact_schema.py)
- [employment_rule_adapter.py](F:/ai/Sage/backend/review_v2/employment_rule_adapter.py)
- [employment_fact_rules.py](F:/ai/Sage/backend/review_v2/employment_fact_rules.py)
- [employment_fact_store.py](F:/ai/Sage/backend/review_v2/employment_fact_store.py)
- [fact_semantic_contracts.py](F:/ai/Sage/backend/review_v2/fact_semantic_contracts.py)
- [employment_fact_pipeline.py](F:/ai/Sage/backend/review_v2/employment_fact_pipeline.py)
- [employment_facts.py](F:/ai/Sage/backend/review_v2/employment_facts.py)
- [lease_semantics.py](F:/ai/Sage/backend/review_v2/lease_semantics.py)
- [priority_contract_review.py](F:/ai/Sage/backend/review_v2/priority_contract_review.py)
- [engine.py](F:/ai/Sage/backend/review_v2/engine.py)
- [test_termination_verified_pipeline.py](F:/ai/Sage/backend/tests/test_termination_verified_pipeline.py)

## 回归

新增8项测试：地址有/无两个最终报告场景；跨条款期限/证明/转移与多风险消费者；交接时支付与额外延期/救济否定两个场景；模块范围隔离；事实缺失与展示证据删除两个覆盖冲突场景。

正式验收：147 passed，3 skipped（可选在线测试开关未启用）。实际当前合同另通过真实HTTP业务接口、DeepSeek抽取与Verifier。

拓展检查另有4个未通过断言，未计入上面的通过数：3项直接调用旧 `_review_contract_v2_legacy` 的工资测试被 EMP-17 SEARCH_AUDIT_ELEMENT_CONFLICT 阻断；1项建设工程97历史样例的预期PASS断言失败。未修改这些旧链路/样例，也未据此声称整个仓库测试全部通过。

## 当前业务验收

```json
{
  "trace_id": "CR-20260913-104809-C9315A",
  "contract_type": "employment_termination",
  "process_id": 17788,
  "source_file": "F:\\ai\\Sage\\test_data\\121 测试1.docx",
  "source_file_sha256": "715995cd8bb4545d0e1686e9fe42ab4d98077e5bbabe230f21f205b43e65b7a6",
  "source_text_sha256": "151804ec4bebd70743be53e827f917dca8e58a595c5c9a66a42cb7a89367243c",
  "active_concept_count": 77,
  "verified_check_count": 43,
  "scope_equal": true,
  "rule_count": 18,
  "release_quality_gate": "REPORT_READY"
}
```

[最终报告](acceptance-report.md) · [完整响应](acceptance-response.json) · [逐项验收与原文](acceptance-summary.json) · [回归日志](final-regression.log)
