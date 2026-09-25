# 保管合同生产复测

根因：旧规则缺少明确原子要素，关键词候选直接进入最终判断；通用事实没有成为这些规则的共享证据输入；期间费用别名、应付未付余额未归一化；特别约定默认始终适用。

修复：以共享概念ID独立抽取证据，配置规则到概念的映射，生产判断消费同一事实池并二次验证证据；最终缺失仅来自未覆盖原子要素。合同交付安排证明接收控制机制，不验证外部实际履行。周期费用跨条款引用仅在单价无冲突时成立。条件规则通过声明触发条件先判适用性。

生产入口：POST /review-v2/file；PID15084；runtime CURRENT；原合同字节hash未改变。

测试：新增28项通过；相关既有69项通过。更新1项旧统计断言，将未触发的排除留置权计入N/A，仍严格检查总数闭合。

最终统计：49项（原48项+比例基数审查），37通过、2部分覆盖、5缺失、5不适用。release_quality_gate=REPORT_READY，failures=[]。

重点结果：

- D-01-03：通过；合同原文覆盖全部专项要素。

- D-02-03：通过；合同原文覆盖全部专项要素。

- D-04-03：部分覆盖；未找到明确约定：额外费用的凭证或核验安排。

- D-07-01：通过；合同原文覆盖全部专项要素。

- D-09-03：不适用；未触发特别约定场景，不作为合同必备缺失项。

- D-12-04：部分覆盖；未找到明确约定：正文附件冲突时的适用顺序。

- COMMON-20-01：通过；合同原文覆盖全部专项要素。

## 修改文件

- backend/review_v2/shared_fact_concepts.py
- backend/review_v2/house_lease_checklist.py
- backend/review_v2/safekeeping_contract_checklist.py
- backend/review_v2/priority_contract_review.py
- backend/review_v2/penalty_base.py
- backend/review_v2/lease_semantics.py
- backend/review_v2/engine.py
- backend/routers/review_v2.py
- backend/tests/test_shared_fact_concepts.py
- backend/tests/test_safekeeping_review_checklist.py
- scripts/run_safekeeping_acceptance.py

保留真实缺口：额外费用的凭证/核验安排、附件冲突顺位，以及完整报告中其他实际缺失项。未删除风险规则或修改原合同。完整条件审计另见 artifacts/safekeeping-shared-facts/applicability-audit.json。
