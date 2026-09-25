# 保管合同：事实回归与法律依据隔离验收

最终结果：50 项，39 PASS / 2 PARTIAL / 3 MISSING / 6 N/A。release_quality_gate=REPORT_READY。
实际入口：http://localhost:5173/review-v2/file → 8016；PID 21252，runtime=CURRENT，HTTP 200。测试文件未修改，SHA256：de20c23652e7d1a1e00d78fbd231dfece6ae685db16dde5256e9bb79948742d3

## 根因与证据边界

本轮实际重现了 38 PASS / 2 PARTIAL / 4 MISSING / 6 N/A，未完整重现用户报告的 36 PASS。不能据此把三项退化都归因于某次 special-over-general 修改。
历史保存的稳定配置与修复前运行配置相比，这三项的业务 metadata 均无差异；没有发现 legal propositions 覆盖 required elements 的写入。当前生产重跑的不可变边界也未发现结果或规则对象被法律阶段改写。
D-07-03 的 C0039 已进入检索候选。模型原始理由却把出入库记录、监控保存视为不足，额外要求事故后的提供时限/责任分配；后续 SEARCH_AUDIT 使用 OBJECTIVE_LITERAL_TARGET 搜索“合同存在可验证的……实质条款内容”，无法把具体记录义务归一到抽象要求。失败发生在法律补充之前的事实判定与要素查询链。
D-11-03 还存在另一种旧路径矛盾：最终 PASS，但 core_contract_arrangement 为 UNCERTAIN、无证据绑定，并产生 NOT_FOUND。D-12-02 的旧单一抽象要素也无法稳定区分验收、封存和影像留存。三项原先未绑定共享事实概念，受模型判断和通用字面回查影响。
另外发现两处耦合隐患：事实判断的单项/批量提示词包含 legal_basis；法律 trace 的 required_elements 指向原 coverage_elements 列表。前者已移除，后者已深拷贝。历史业务 metadata 未改变，因此不把这两处潜在问题冒充已证实的本次直接原因。
历史报告未保存法律阶段前后的独立业务快照，stage-diagnostic.json 中明确标记 captured=false；没有从最终结论反推或伪造历史中间结果，也没有回滚整个共享工作区。

## 修改逻辑

- 使用现有 shared_fact_concepts / source-bound evaluator，为流转记录、影像留存、签认凭证、领取办理步骤、验收记录绑定显式原子要求。按既有要素聚合器计算；无 rule_id 强制结果，没有改动合同数据或法条映射。
- D-07-03 分别核对流转记录和可核验影像材料；D-11-03 分别核对凭证、领取办理步骤和签认记录；D-12-02 分别核对影像留存和验收/封存记录。仅找到部分证据时仍 PARTIAL；只出现设备/场所关键词、没有相应记录义务时不能 PASS。
- 法律阶段只接收业务结果和规则配置的深拷贝。对全部非法律字段做 SHA256 前后比较，只有 legal_basis_index、legal_references 和法律 trace 可以回写；改写业务字段、规则要求或删除审查项均 BLOCKED，原始事实不被提交覆盖。
- 增加正向事实一致性门禁：共享池有已验证事实、或存在已绑定的 COVERED 要素时，不能同时出现对应 MISSING / SEARCH_AUDIT NOT_FOUND / 整项完全缺失。
- A/B 开关使用请求级 ContextVar，避免并发请求串扰；诊断 OFF/ON 均走实际上传路由，use_llm=false 固定事实判断以隔离法律阶段变量。另行用 use_llm=true 从前端代理真实 HTTP 重跑验证最终服务。

## 三项最终结果

### D-07-03：通过

- 建立或保存财物出入、交接流转记录：COVERED；证据：C0039
- 保存可核验的照片、视频或监控资料：COVERED；证据：C0079

> 第十七条（二）：（二）未经甲方书面同意，乙方不得拆除保管物原有包装，但因发现包装破损、进水或者存在其他紧急情况，为防止损失扩大确需拆包检查的除外；乙方应及时通知甲方并保留照片或者视频记录。

> 第十条（七）：（七）乙方应当建立保管物出入库记录，并保存保管区域的视频监控资料不少于30日。

各要素 SEARCH_AUDIT=FOUND；无对应 NOT_FOUND。

### D-11-03：通过

- 接收方出具交付接收凭证：COVERED；证据：C0017
- 约定领取、返还时的办理条件或协作步骤：COVERED；证据：C0022
- 交接凭证具备双方签认机制：COVERED；证据：C0017

> 第五条 保管物交付：交付完成后乙方应当向甲方出具双方签名（盖章）的《保管凭证》（详见附件）。

> 第七条（一）：（一）保管期限届满或者甲方提前领取保管物的，甲方按照约定支付保管费及其他费用后，乙方应当将保管物归还甲方。

> 第九条（五）：（五）甲方提前领取保管物的，应至少提前1个工作日通知乙方，以便乙方安排出库。

> 第十条（一）：（一）乙方收到甲方交付的保管物后，应当验收或者封存，并向甲方出具保管凭证。

各要素 SEARCH_AUDIT=FOUND；无对应 NOT_FOUND。

### D-12-02：通过

- 保存可核验的照片、视频或监控资料：COVERED；证据：C0079
- 验收或封存状态形成交接记录或凭证：COVERED；证据：C0033

> 第十七条（二）：（二）未经甲方书面同意，乙方不得拆除保管物原有包装，但因发现包装破损、进水或者存在其他紧急情况，为防止损失扩大确需拆包检查的除外；乙方应及时通知甲方并保留照片或者视频记录。

> 第十条（一）：（一）乙方收到甲方交付的保管物后，应当验收或者封存，并向甲方出具保管凭证。

> 第十条（七）：（七）乙方应当建立保管物出入库记录，并保存保管区域的视频监控资料不少于30日。

各要素 SEARCH_AUDIT=FOUND；无对应 NOT_FOUND。

## 回归与门禁

新增 28 项自动化测试，连同历史回归共 174 项通过（10 条既有依赖弃用警告）。涵盖同义表达、跨规则共享、部分覆盖、否定/弱证据负例、法律 metadata 不影响事实提示词、深拷贝快照、恶意业务/规则/集合改写阻断，以及真实上传路由 50 项 OFF/ON 对照。
完整 A/B 差异为 0：status、coverage、risk、action、applicability、required elements、shared facts、evidence/source spans、SEARCH_AUDIT 和要素叙事均比较一致。50 项法律阶段前后业务 hash 全部一致。
当前完整 HTTP 结果与已保存稳定版本的 50 项 coverage 差异为 0；三项已绑定正向事实，SEARCH_AUDIT 与覆盖一致。所有法律依据与上一轮已验证的全量 special-over-general 版本一致，special_over_general_violation=0。
保留真实缺口：D-04-03、D-12-04 为 PARTIAL；D-06-04、D-09-01、D-09-02 为合同层面 MISSING，未为提高 PASS 数更改这些事项。
法律依据保持：D-04-02=889/902/509；COMMON-20-01=585/577；D-08-03=894/577；D-09-02=450/453/903；D-09-04=450/448/903；其余条目见下表。

## 修改文件

- [backend/review_v2/legal_enrichment_boundary.py](F:/ai/Sage/backend/review_v2/legal_enrichment_boundary.py)
- [backend/review_v2/engine.py](F:/ai/Sage/backend/review_v2/engine.py)
- [backend/review_v2/llm_semantic_reviewer.py](F:/ai/Sage/backend/review_v2/llm_semantic_reviewer.py)
- [backend/review_v2/shared_fact_concepts.py](F:/ai/Sage/backend/review_v2/shared_fact_concepts.py)
- [backend/review_v2/safekeeping_contract_checklist.py](F:/ai/Sage/backend/review_v2/safekeeping_contract_checklist.py)
- [backend/review_v2/legal_basis_trace.py](F:/ai/Sage/backend/review_v2/legal_basis_trace.py)
- [backend/routers/review_v2.py](F:/ai/Sage/backend/routers/review_v2.py)
- [backend/tests/test_legal_fact_boundary.py](F:/ai/Sage/backend/tests/test_legal_fact_boundary.py)
- [scripts/audit_legal_fact_boundary.py](F:/ai/Sage/scripts/audit_legal_fact_boundary.py)

## 完整50项状态和法律依据

|规则|coverage|法律依据|
|---|---|---|
|D-01-01|通过|《中华人民共和国民法典》第888条|
|D-01-02|通过|《中华人民共和国民法典》第888条；《中华人民共和国民法典》第900条|
|D-01-03|通过|《中华人民共和国民法典》第888条；《中华人民共和国民法典》第890条|
|D-01-04|通过|《中华人民共和国民法典》第888条|
|D-02-01|通过|《中华人民共和国民法典》第890条|
|D-02-02|通过|《中华人民共和国民法典》第890条|
|D-02-03|通过|《中华人民共和国民法典》第891条|
|D-02-04|通过|《中华人民共和国民法典》第577条|
|D-03-01|通过|《中华人民共和国民法典》第470条|
|D-03-02|通过|《中华人民共和国民法典》第509条|
|D-03-03|通过|《中华人民共和国民法典》第893条|
|D-03-04|通过|《中华人民共和国民法典》第584条|
|D-04-01|通过|《中华人民共和国民法典》第889条|
|D-04-02|通过|《中华人民共和国民法典》第889条；《中华人民共和国民法典》第902条；《中华人民共和国民法典》第509条|
|D-04-03|部分覆盖|《中华人民共和国民法典》第509条；《中华人民共和国民法典》第510条|
|D-04-04|不适用||
|D-05-01|通过|《中华人民共和国民法典》第892条；《中华人民共和国民法典》第897条|
|D-05-02|通过|《中华人民共和国民法典》第892条|
|D-05-03|通过|《中华人民共和国民法典》第892条|
|D-05-04|通过|《中华人民共和国民法典》第900条；《中华人民共和国民法典》第899条|
|D-06-01|通过|《中华人民共和国民法典》第893条|
|D-06-02|通过|《中华人民共和国民法典》第898条|
|D-06-03|通过|《中华人民共和国民法典》第898条|
|D-06-04|缺失|《中华人民共和国民法典》第509条|
|D-07-01|通过|《中华人民共和国民法典》第897条|
|D-07-02|通过|《中华人民共和国民法典》第897条|
|D-07-03|通过|《中华人民共和国民法典》第509条|
|D-07-04|通过|《中华人民共和国民法典》第897条|
|D-08-01|通过|《中华人民共和国民法典》第894条|
|D-08-02|通过|《中华人民共和国民法典》第894条|
|D-08-03|通过|《中华人民共和国民法典》第894条；《中华人民共和国民法典》第577条|
|D-08-04|通过|《中华人民共和国民法典》第894条；《中华人民共和国民法典》第593条|
|D-09-01|缺失|《中华人民共和国民法典》第903条|
|D-09-02|缺失|《中华人民共和国民法典》第450条；《中华人民共和国民法典》第453条；《中华人民共和国民法典》第903条|
|D-09-03|不适用||
|D-09-04|通过|《中华人民共和国民法典》第450条；《中华人民共和国民法典》第448条；《中华人民共和国民法典》第903条|
|D-10-01|不适用||
|D-10-02|不适用||
|D-10-03|不适用||
|D-10-04|不适用||
|D-11-01|通过|《中华人民共和国民法典》第899条|
|D-11-02|通过|《中华人民共和国民法典》第900条|
|D-11-03|通过|《中华人民共和国民法典》第509条|
|D-11-04|通过|《中华人民共和国民法典》第577条；《中华人民共和国民法典》第509条|
|D-12-01|通过|《中华人民共和国民法典》第470条；《中华人民共和国民法典》第469条|
|D-12-02|通过|《中华人民共和国民法典》第509条|
|D-12-03|通过|《中华人民共和国民法典》第893条；《中华人民共和国民法典》第469条|
|D-12-04|部分覆盖|《中华人民共和国民法典》第466条；《中华人民共和国民法典》第142条|
|COMMON-20-01|通过|《中华人民共和国民法典》第585条；《中华人民共和国民法典》第577条|
|COMMON-21-01|通过|《中华人民共和国民法典》第142条；《中华人民共和国民法典》第466条|

## 原始验收材料

- [真实 HTTP 新报告](F:/ai/Sage/artifacts/factual-regression-live/report.md)
- [运行版本与验收汇总](F:/ai/Sage/artifacts/factual-regression-live/verification.json)
- [50项 A/B 字段级比较](F:/ai/Sage/artifacts/factual-regression-ab/comparison.json)
- [STABLE / CURRENT / DIFF 13阶段诊断](F:/ai/Sage/artifacts/factual-regression-ab/stage-diagnostic.json)
- [174项测试日志](F:/ai/Sage/.runtime-logs/legal-fact-final-verification.log)
