# 统一事实层：框架与借款候选迁移（上一阶段记录）

> 普通借款的后续实现已接入独立 VerifiedFactStore 入口，不再处于本页所述候选阶段。当前实现和验收证据见 [loan-verified-migration.md](loan-verified-migration.md)。下文保留为第一阶段的历史诊断，不代表当前路由状态。

本轮状态：**框架已实现；借款部分事实消费者已接通；第一批完整报告迁移尚未完成，不可启用为已验收新主链路。**

## 已实现的调用关系

```text
V2 文件/文本入口
  → fact_routing.resolve：别名规范化、全文合同类型重新识别
  → 固定请求内 FactRoute，报告阶段复用同一分类结果
  → FactModuleRegistry：显式选择合同族，无默认劳动族
      employment：现有 labor / non_compete / confidentiality 管线（ACTIVE）
      credit / loan：统一框架候选（CANDIDATE_NOT_RELEASED）
      未注册族：明确保留旧兼容链路，不假称已迁移

候选事实链路
  → 当前族公共/根关系字段 → DeepSeek 全文抽取
  → 严格类型归一化 → 逐字原文与绝对 span 绑定
  → 独立 DeepSeek 核验候选及每个 active concept 的全文遗漏
  → 根事实核验通过后，加载父关系成立的子模块
  → 按当前 active scope 分批再次核验跨批次事实与遗漏
  → 原子提交 VerifiedFactStore → 已迁移的确定性事实消费者
```

新旧劳动抽取与候选框架共用 `deepseek_transport`；使用现有 DeepSeek 配置，未接其他模型。旧劳动的数字接口委托公共 `fact_number_normalization`，新框架在入口增加严格格式检查。劳动专用 schema、FactStore 和 verifier 仍保留兼容，**不是已全部替换为同一个 Store 实现**。

## 当前字段选择

- `FactModuleRegistry` 中劳动三类沿用原有动态选择器；没有未知类型回退劳动字段的 `else`。
- 借款 schema 为 `common` 公共主体、金额、日期、期限、责任、争议解决 + `credit.loan.relationships` 根关系 + 借款金额日期和原子要素模块。
- 借款共注册 70 个概念；根阶段 25 个；父关系未成立时基础 active scope 为 56 个。最多 70 个，**不是全合同 schema**。
- 展期、保证、担保、提前还款等子字段仅在所有父事实为明确、高置信、verified PRESENT 且取值满足条件时加载。未加载字段在代码中为 NOT_APPLICABLE，不作 ABSENT 断言。
- 未实现保证/抵押/质押及其他合同族的模型 schema；这些类型保持未迁移状态，不能通过注册名称冒充支持。

## 状态、类型与证据约束

`PRESENT / ABSENT / EXPLICIT_NONE / DEFERRED / NOT_APPLICABLE / UNCERTAIN` 是事实状态，不是 number/money/date 等字段值。只有 PRESENT 可带 value，其他状态不接受 null 或自然语言占位。

number、money、date、duration、formula、party、enum 严格校验。数字使用 Decimal；日期不补全；金额不默认币种；公式只保留结构化操作数，不执行模型表达式。新数字入口拒绝歧义或未支持的中文数额格式，不静默保留最后一个数字。

PRESENT、EXPLICIT_NONE、DEFERRED 必须绑定有效合同条款中的原文证据；保留 clause、section、原文绝对 offset、confidence、EXPLICIT/INFERRED。不接受模板说明证据、错误位置或歧义 span。未核验候选不能构造规则可用 Store；拒绝、不完整范围、遗漏或失败均阻断，不回退关键词推断。

所有 getter 返回副本；请求上下文采用 ContextVar 并可靠复位。未解决冲突和低置信度保留为 UNCERTAIN，不能成为缺失结论。

## 借款实际迁移范围

已接通的候选接口：

- `LoanFacts.from_clauses` 在 verified 上下文中从 Store 投影，不调用旧主体识别或全文扫描。
- `LoanFacts.applicability` 保留现有判断条件，增加上游 UNCERTAIN 不被布尔表达式吞成“不适用”的边界。
- `loan_facts.extract / supports` 对 30 个已有原子要素节点读取共享 Store，复用原有要素语义；未把 regex 发给模型或让模型决定法律结论。
- 保留跨条款证据集合，多个消费者引用相同事实及源 span。

**未完成：**另有 18 个规则节点、成本/LPR 输入、部分风险谓词和旧后处理尚未全部改为 verified 输入。可通过 `unified_facts.loan.migration_inventory()` 取得完整清单。这里的 30 个节点仅指事实/证据接口接通，**不代表 30 条完整规则已通过新管线验收**。

保护措施：

- 借款未在生产入口默认切换；兼容结果显式标记 `fact_migration.mode=LEGACY_COMPATIBILITY`、`verified_factstore_only=false`，响应模型保留该字段。
- 若显式设置 `REVIEW_V2_VERIFIED_FACT_CANDIDATES=loan` 请求候选主链路，入口在调用模型和旧引擎前报 `FACT_CONSUMER_MIGRATION_INCOMPLETE`，不能回退旧引擎却输出“统一事实”报告。
- 新 verified 上下文中调用旧 `extract_contract_fact_graph`、`loan_facts.units` 或 `negative_scan` 会报 `RAW_FACT_REEXTRACTION_FORBIDDEN`。`loan_costs.analyze_costs` 经 units 也会被阻断。
- 这不是对全部旧引擎原文读取的完整拦截器。因此**不能声称 Verifier 已成为所有 V2 规则的唯一事实门禁**。

## 回归与本批次门禁

原有基线测试在本轮修改前已经为 117 passed / 1 failed：
`test_loan_applicability_and_consistency.py::test_current_48_rules_and_final_counters` 要求 L-05-02 为“通过”，旧代码实际为“待核验”。本轮未修改该规则或断言。

扩大回归发现原 verifier 测试夹具未传 active_concepts。本轮只补齐显式 scope，并加强“模型只能收到当前 scope”的断言；未放宽生产校验或修改业务结论。

供用合同上传回归还有一个既存报告门禁失败。`utility-routing-comparison.json` 记录同一输入分别走兼容入口与新路由：全部规则 coverage/risk 相同，两者均 BLOCKED。

最终合并回归为 **321 项：319 通过、2 失败；新增 92 项全部通过**。失败均为上述借款和供用合同的既存断言差异。数量和失败清单见 `artifacts/fact_migration/migration-status.json`、`final-regression.xml`，分组 JUnit 文件同时保留。这些是离线模型协议测试和原有规则回归；**本轮未完成真实 DeepSeek 调用的借款报告泛化验收**。

## 本批次继续完成前的必要工作

1. 在不篡改规则结论的前提下厘清借款既存 L-05-02 回归差异。
2. 完成剩余 18 个节点以及金额成本、外部事实、风险条件、后处理的 typed fact 输入适配；移除候选链路的全部原文事实再抽取路径。
3. 将现有报告/校验消费者逐一迁移，并用完整消费者清单替代当前阻断名单；候选必须在任意绕过路径上失败关闭。
4. 对真实 DeepSeek 的不同借款文本完成事实、证据和最终报告回归，原回归无新增退化后才激活借款。
5. 再继续第一批中的保证、抵押、动产质押、股权质押、权利质押；本轮没有把它们标成已迁移。

未改法律阈值，未删旧抽取代码，未部署，未修改或切换本地损坏数据库。
