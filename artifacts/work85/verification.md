# 承揽合同85定向修复验证

## 根因
1. work_evidence 的固定短语未覆盖“主要加工工作/转交第三方”、具体质量参数、带修饰语的验收动作、封样及中途解除。现有合同原文完整存在，未修改正文或补充样本。
2. applicability 原先通过“转包/分包”词项判断，与逐要素证据口径不同；主要工作同意规则现在直接复用同一事实提取结果。
3. 催告/顺延、催告/解除、材料/成果保管合并为一个必须同时满足的原子，造成部分正向事实被整体抹掉。现在独立保存子要素，真实缺项保留 PARTIAL。
4. 通用引用规则在非 priority 合同路径未统一调用解析判定；引用主题还被同一大条款中的其他义务污染。现在调用通用解析器，以引用所在句识别目的，并区分主条款和嵌套项编号。
5. 动态部分价款基数未关联合同单价/总价定义。现在关联真实价格证据，未履行数量作为交易事实输入，不要求事先写固定违约金额；空白或待协商价格仍不认定可确定。

## 修改文件
- backend/review_v2/work_evidence.py：语义关系、独立子要素、共享适用性、全部要素 SEARCH_AUDIT。
- backend/review_v2/contract_references.py：主条款解析、引用所在句、目标解析元数据。
- backend/review_v2/penalty_base.py：部分价款与已有单价/总价定义绑定。
- backend/review_v2/engine.py：非 priority 合同也统一执行通用引用解析。
- backend/tests/test_work_semantic_relations.py：29个新增正反例与当前文件端到端校验。
- backend/tests/test_work_canonical_evidence.py：44项W规则加实际通用规则分别校验，通用证据使用其原本语义校验器。
- backend/tests/test_work_remedy_semantics.py：将公开响应转换为内部数据类时排除新增展示字段，原校验断言保留。
- scripts/run_work85_acceptance.py：不可变原文件生产HTTP回放。

## 结果
144 passed，含承揽既有集、动态基数、跨条款引用相关回归；无跳过、无手工PASS或注入证据。
最终实际入口：http://127.0.0.1:8016/review-v2/file；task CR-20260909-073632-6CC690；worker PID 22856。
46项 = 44承揽 + 2通用。修复前19通过/2部分覆盖/22缺失/3不适用；修复后29通过/3部分覆盖/12缺失/2不适用。
release_quality_gate=REPORT_READY；EXACT_ELEMENT_REPORT_INVARIANT=PASS。

W-04-03、W-04-04仍缺催告或补救期限；W-06-04仍缺成果保管。未为样本强行补齐。
W-07-01修复前整项为PARTIAL（已有质保期限），其中质量标准子要素为MISSING；修复后均覆盖。

## 交付
- before.json / after.json：完整生产响应。为避开并行任务反复重启共享端口，基线使用相同生产main:app的临时8017入口采集；最终在8016重跑。临时8017进程已关闭。
- rule-diff.md / rule-diff.json：13项状态、命中全文、真实evidence_id或已有evidence_refs、适用性、逐要素SEARCH_AUDIT。
- report.md：最终报告。
- acceptance.json：任务、哈希、运行状态、完整门禁。
- all-tests.txt：144项测试完整输出。

范围说明：本次确认列出的目标误判已修复，负例和现有回归未发现扩大误匹配；不声称所有未列举的合同措辞都已被穷尽验证。
