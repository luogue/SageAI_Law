# 普通借款 V2 事实层迁移

范围仅为 `loan`，未启用保证、抵押、质押等独立合同类型的新事实链路。

## 当前调用路径

`review_contract_v2` → `fact_routing.resolve`（别名/重新分类）→ `unified_facts.loan_pipeline.run` → `loan.schema` → `pipeline.extract_verified` → `CandidateStore` → 独立 DeepSeek 全文核验 → `commit` → `VerifiedFactStore` → `loan_rules.evaluate` → `loan_costs.analyze` → 事实溯源门禁 → 原有 Markdown 报告格式器及处置/统计投影。

- 借款在注册表为 ACTIVE，只表示路由已启用，不代表真实模型泛化验收自动通过。
- `use_llm=False` 和旧候选环境开关均不能将 V2 借款退回旧引擎。模型未配置、类型/证据/遗漏核验失败时返回结构化阻断诊断。
- 48 个 L 节点均有显式概念绑定；此前剩余的 18 个节点已纳入。贷款人法律分类复用主体性质，期限与时效节点复用同一个到期事实。
- 旧清单、原子命题、适用条件、LPR 参考区间和计算阈值保留。LPR 计算从原来的文本入口拆出 `reference_for_date` / `assess_values`；旧入口仍用于兼容和历史基线，不参与新报告。

## 动态范围与严格状态

共 95 个概念，26 个根概念；没有已成立的父关系时基础 active scope 为 63 个。只发当前 active 字段；人的保证、担保附件、展期、提前还款、夫妻用途、收费等子模块按已核验父事实加载。UNKNOWN、冲突、低置信推断不加载子模块。

`PRESENT / ABSENT / EXPLICIT_NONE / DEFERRED / UNKNOWN / CONFLICT / NOT_APPLICABLE` 分开表达。输入的 UNCERTAIN 规范为 UNKNOWN；CONFLICT 由冲突的已核验候选推导；NOT_APPLICABLE 由模块适用性推导。只有 PRESENT 有强类型值。部分已知事实不转成完全缺失。

一次性费用保留 ONCE，不擅自年化；本金、未偿本金、未付利息分别保存，不混加不同基数。成本计算、风险谓词、建议和报告均只接收 Store 或从 Store 得出的决策，不接收合同原文重新查找事实。

每个提取/核验批次读取完整文档。发送的是分条对应的原始文本切片，Span 由代码逐字绑定。模型不能靠猜坐标取得有效证据。调试输出保留模型响应、归一化、证据 Span、全文核验、修正历史、规则输入 fact_id 和决策。

## 拒绝与隔离

类型/绑定/核验失败有有限修正预算。最终修正后的完整事实快照必须重新核验，不能沿用旧快照的证书。

若独立 Verifier 否决取值、且全文审计未发现明确遗漏，可将该字段隔离为无 value 的 UNKNOWN 候选。它仍须再次通过独立全文核验；存在明确遗漏时禁止隔离放行。被否决值只留在诊断区，不进入规则或正式报告。UNKNOWN 触发待核验，不能变成完全缺失或完全通过。整个机制不保证生成报告，更不等于法律风险为零。

## 测试与证据

- 新链路测试：`backend/tests/test_loan_verified_pipeline.py`，含所有 48 节点绑定、旧消费者禁用、跨条款、冲突/未知/否定、Span 防篡改、成本阈值、HTTP 文件入口及 Verifier 拒绝、有限修正与弃权二次核验。
- 通用/劳动/竞业/保密回归证据：`artifacts/loan_verified_acceptance/automated.xml`。
- 旧链路基线单独显式调用 `_review_contract_v2_legacy`，并非宣称原测试已在新链路通过：`legacy-baseline.xml`，104 通过、2 个原有失败（L-05-02、供用合同）。两处业务断言未修改。
- 真实 DeepSeek 运行：`scripts/run_loan_verified_acceptance.py 72 98 101`。输入为仓库已有 DOCX 文档，不是针对本轮编写的固定句子。每次运行新建时间目录，保留原文件/文本 SHA256、模型调用响应、最终报告或阻断诊断。
- 测试/脚本启动时安装临时数据库隔离；本轮未切换业务库、未部署、未执行 Docker 构建。

最终泛化结果以 `artifacts/loan_verified_acceptance/final-status.json` 为准；早期成功记录不能代替最后一轮失败，失败响应也不会冒充报告。

## 模型形态协议回归

- 公共 `common.term` 和借款 `loan.duration` 使用 `term`，可保存明确的长度（amount/unit）或完整日期区间（start_date/end_date）；两者不互相计算。仅对完整无歧义日期表达、明确数值和单位作确定性转换，不接受相对日期、估计期限或缺失年份。仍声明为 `duration` 的长度字段继续拒绝日期区间。
- `multiple` 明确规定成员结构。单对象、重复 observation 和非空数组统一到逐成员候选；数组共有证据完整保留，成员自带证据时分别绑定。每个成员独立生成 fact_id、独立通过 Verifier。空数组仅在明确 ABSENT 且空证据时可转换，仍须全文审计；PRESENT 空集合拒绝。
- 收费模型输入改为 `accrual_window.start_event/end_event`，代码按固定映射投影 scope，不交给模型判断法律适用。原文的起算/终止事件与“叠加、替代、择一”的关系分开。Verifier 视图保留全部直接事实、证据和完整候选 fact_id，去掉代码派生 scope；commit 额外校验 scope 与事件一致。任何直接事实核验失败或全文遗漏仍阻断，未减少核验范围或次数。旧 scope 对象仅保留强类型形态兼容，不调用旧事实抽取。
- 新回归文件 `backend/tests/test_loan_model_shapes.py` 覆盖期限、集合、证据和收费范围协议及变体。验收脚本记录每次 system prompt、代码 SHA256，语义审计要求最后运行与当前代码一致。
- 六份现有借款文件的真实 DeepSeek 验收：分别运行 `python scripts/run_loan_verified_acceptance.py <编号>`，编号为 72、98、101、49、99、104；之后运行 `python scripts/audit_loan_verified_acceptance.py`。审计检查原始本金、利率、期间、关系和计息边界，不将返回报告自动等同泛化通过。

上一轮历史代码快照回归：339/339 自动化通过。真实模型六份最终验收为 72 PASS；98、101、49、99、104 BLOCKED（见 final-status.json 中最后一次运行目录及原始调用）。72 的期限、98 的集合形态、101 的计息范围原阻塞已在对应真实阶段解决，不能据此宣称整份报告全部通过。

新增阻塞：98/49/104 的核验响应引用旧候选或遗漏当前 fact_id，严格范围检查保持拒绝；99 最终核验将其他用途的通知方式误归入提前还款渠道；101 虽返回报告且计息范围正确，公式的 RATE/DAYS 未明确表达原文年转日除数或绑定日利率，人工/离线语义审计仍判 BLOCKED。未为这些新问题改法律规则、关闭遗漏检查、补造核验证书或扩大本轮修复范围。

## 当前快照证书与语义门禁

1. `CandidateStore.snapshot_hash` 覆盖独立候选轮次标识、原文哈希、active schema、全部当前观察及证据；每个 verifier 响应必须返回同一哈希及完整当前 fact_id 集合。旧隔离上下文混入了旧候选/证书，是已由日志重放确认的 stale ID 来源，证据保存在 `stale-certificate-evidence.json`；没有将其猜测为线程竞争。
2. `certificates.verify_current` 只发送当前候选，其他字段上下文不携带可核验 ID。无效响应（hash/ID/范围/证据协议错误）最多重新核验同一快照三次，失败返回 `VERIFICATION_RESPONSE_INVALID`，不重抽取、不按顺序匹配、不补造证书。事实内容被有效否决时才进入原有重抽取流程。
3. 否决的 correction 和全文 omitted_facts 必须使用完整观察结构、逐字 clause/quote 绑定，并通过同样的属性验证。reason 仅用于诊断。通知期限和渠道分开，收款确认渠道不得借用为提前还款渠道；清偿顺序提及复利、付款账户等不自动成立计收复利或凭证机制。
4. 费用 `base_expression` 保留直接引用的原文短语，ontology 统一归一为原始总额/未偿本金/未付利息；证据无明确基数时为 UNKNOWN。排版空白仅用于 ontology 匹配，原始 quote/span 不变。
5. 删除模型输入中的 `loan.interest_formula`，改抽取 `loan.day_count_basis`，利率期间复用 `loan.regular_rate_period`。`loan_formulas` 只使用已核验 Store 构建报告表达；按年转日明确写出合同分母，未约定不得默认。固定日/月利率按相应周期表达；复利独立参数不足时待核验，不套用单利公式。原司法保护阈值和确定性法律规则未修改。
6. 当前自动化测试见 `automated.xml`；原六份加六份 blind 的完整重放结果见 `final-generalization.json`。六份 blind 是独立 DeepSeek 预先生成并哈希封存的构造合同，不是新增真实业务文件；其正文未用于修复。任何失败不得重写样本或冒充通过。

本轮最终状态：378/378 自动化通过；最终冻结版本的原六份真实调用全部在首次请求收到 HTTP 402，没有获得抽取结果。服务端单独确认错误为 `Insufficient Balance`（见 `provider-availability.json`）。六份 blind 已封存但尚未调用验收，保持 NOT_RUN/BLOCKED。此前中间版本成功报告不计入最终通过数量；当前普通借款状态仍为 BLOCKED，不能据此宣称剩余语义问题已全部消除。
