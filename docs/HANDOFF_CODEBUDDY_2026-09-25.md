# Sage / AI 合同审查开发交接（CodeBuddy + DeepSeek）

> 日期：2026-09-25  
> 仓库：`F:\ai\Sage`  
> 核查基线：Git `e1f0e683e312b6c21c1382be524784638f5abf63` + 当前未提交工作区  
> 模型约束：只使用 DeepSeek；配置来自环境变量或 `backend/.env`，不得引入 provider fallback。  
> 证据原则：本文以当前源码、测试和 `artifacts/` 为准。不能从仓库证明的结论标为 **UNKNOWN/TODO**。

## 目录

1. [先读结论](#1-先读结论)
2. [当前系统架构](#2-当前系统架构)
3. [关键目录与文件：问题到代码的导航](#3-关键目录与文件问题到代码的导航)
4. [合同类型与当前完成度](#4-合同类型与当前完成度)
5. [技术合同专项：Round41～Round45](#5-技术合同专项round41round45)
6. [不可破坏的设计原则](#6-不可破坏的设计原则)
7. [Evidence / Fact / Projection / SEARCH_AUDIT](#7-evidence--fact--projection--search_audit)
8. [测试体系与最低回归要求](#8-测试体系与最低回归要求)
9. [数据库与运行时数据结构](#9-数据库与运行时数据结构)
10. [Prompt 使用现状](#10-prompt-使用现状)
11. [Prompt Version Management 最小设计](#11-prompt-version-management-最小设计)
12. [待办优先级](#12-待办优先级)
13. [CodeBuddy 接手步骤](#13-codebuddy-接手步骤)
14. [已知坑](#14-已知坑)

## 1. 先读结论

当前 V2 是**统一路由入口下的混合事实架构**，不能描述成“所有合同均已使用同一 DeepSeek Verified FactStore”。

- `labor / non_compete / confidentiality / employment_termination` 注册为 employment 事实族，走 DeepSeek 全文抽取、劳动专用动态 schema、`FactStore`、独立 Verifier，再适配现有规则。
- `loan` 注册为 credit 事实族，走通用 `unified_facts` 框架、动态 schema、严格 normalization、snapshot certificate、`VerifiedFactStore`、48 个确定性规则；自动化 339/339，但最新真实 DeepSeek 六份验收仅 72 PASS，98/101/49/99/104 BLOCKED，因此普通借款**尚不能标记泛化 PASS**。
- 技术合同拥有很深的 canonical fact、component、element、证据反投影、SEARCH_AUDIT 和 Gate 体系，也有 Round1～45 的大量真实/保护回归；但 `fact_module_registry.py` 没有 technology family，入口仍标记 `LEGACY_COMPATIBILITY`。其“canonical facts”主要是现有确定性/专用语义层，不等同于 employment/loan 的 DeepSeek Verified FactStore。
- 其余合同均有 V2 checklist，许多也有专用 facts/evidence 模块，但尚未注册到统一动态事实框架；规则仍可能直接读取条款文本或专用提取结果。
- `Verifier` 目前是 employment 与 loan 新事实链路的门禁，不是所有 V2 合同的唯一门禁。
- 当前工作区非常脏：大量核心文件为 modified/untracked。提交、打包或交给另一工具前，必须以工作区文件哈希或完整 diff 标识版本，不能只报 Git commit。

## 2. 当前系统架构

### 2.1 前后端入口

前端路由在 `frontend/src/router/index.js`：

- `/` 与 `/review`：`ContractReviewV2.vue`，当前新版默认工作台。
- `/contract-review-v2`：重定向到 `/review`。
- `/review-legacy`：旧版 `UploadPage.vue`，静态 import 以避免旧 chunk 丢失。
- `/reports`、`/report/:id`：历史报告和详情。

新版调用封装在 `frontend/src/utils/api.js`：

- `POST /review-v2/file`：主文件入口。
- `POST /review-v2/checklist`：纯文本/清单入口。
- `GET /review-v2/llm-status`、`GET /review-v2/profile-options`。
- `POST /review-v2/export-pdf|export-docx`：只允许导出与 Gate 绑定的最新服务端快照。

后端入口在 `backend/routers/review_v2.py`。`review_v2_file()` 解析文件、构造输入诊断、启动 `SnapshotStore` run，再调用 `review_contract_v2()`；`review_v2_checklist()` 走同一引擎。事实抽取错误通过 `_review_with_fact_errors()` fail closed，返回 `BLOCKED`，不换模型。

### 2.2 类型规范化与分流

```text
用户选择/别名
  -> contract_registry.get_contract_meta()
  -> fact_routing.resolve()
       - 规范化别名
       - 清除非合同尾部
       - 条款解析
       - 文档域/技术子类型分类
       - 仅在可比较域 sale/lease/service/technology 内按证据重分类
  -> FactRoute(selected_type, resolved_type, source_sha256)
  -> FactModuleRegistry.family(resolved_type)
```

`fact_routing.finalize()` 校验 request、canonical、facts_pipeline、checklist、report 各阶段类型；冲突时加入 `CONTRACT_TYPE_CHAIN_CONFLICT` 并阻断报告。

### 2.3 ACTIVE 新事实链路

目标链路是：

```text
全文
 -> 合同类型规范化
 -> 当前合同族 dynamic schema / active concepts
 -> DeepSeek 全文事实抽取
 -> 强类型 normalization
 -> clause + 逐字 quote + source span 绑定
 -> CandidateStore / candidate snapshot hash
 -> 独立 DeepSeek Verifier（候选核验 + 每个 active concept 全文遗漏检查）
 -> certificate 与当前 snapshot/fact_id 严格绑定
 -> Verified FactStore 原子提交
 -> element/component projection
 -> 确定性适用性、阈值、计算、polarity 与法律规则
 -> risk aggregation
 -> narrative/report
 -> release quality gate
 -> 服务端 immutable final snapshot / export authorization
```

通用借款实现位于 `backend/review_v2/unified_facts/`：

1. `schema.py` 定义字段 kind、value schema、父子模块。
2. `loan.py` 注册普通借款 schema 和 active module 选择。
3. `pipeline.extract_verified()` 先抽 roots，再按 verified roots 加载子模块；每批都看全文，不发送全域 schema。
4. `normalization.py` 严格归一化，非法值不静默强转。
5. `store.CandidateStore` 绑定证据并产生 snapshot id/hash。
6. `certificates.verify_current()` 发起当前快照核验；旧 fact_id、旧 certificate、错 snapshot 直接判无效。
7. `store.commit()` 只接收完整当前证书，生成 `VerifiedFactStore`。
8. `loan_rules.py / loan_costs.py / loan_formulas.py` 只消费 Store 或 Store 派生决策。

劳动族沿用专用实现：`deepseek_facts.py` + `employment_fact_schema.py` + `employment_fact_store.py` + `fact_verification.py` + `employment_fact_pipeline.py`。它与通用框架共用 `deepseek_transport.py` 和部分 scalar/number normalization，但并非同一个 Store 类。

### 2.4 非 ACTIVE 的 V2 兼容链路

`engine.review_contract_v2()` 对未注册事实族调用 `_review_contract_v2_legacy()`，并写入：

```json
{"fact_migration":{"mode":"LEGACY_COMPATIBILITY","verified_factstore_only":false}}
```

这里的 legacy 是相对于新 Verified FactStore 的兼容引擎，并不等于“没有 V2 规则”。它仍包含合同清单、专用 facts、canonical claims、element resolution、技术合同语义层、风险聚合、报告和质量门。重要限制是：这些消费者仍可能直接扫描原文，Verifier 不是唯一事实门禁。

### 2.5 canonical fact、component、element 与报告

- `canonical_claims.py`、各专项 `*_facts.py` 把同义事实收敛到稳定 key/value。
- component 是一个规则主题下可复用的语义部件，例如付款节点、保密控制、侵权处理。
- element 是规则 coverage 的最小可判定要求；`coverage_elements` 决定 PASS/PARTIAL/MISSING。
- `element_evidence_projection.py` 从最终 canonical element 反投影报告证据；检索上下文不能冒充报告证明。
- `SEARCH_AUDIT` 是针对仍缺 element 的最终全文查漏记录，不是第二套事实抽取器。
- `risk aggregation` 位于 `engine.py` 的 `_risk_aggregation_group()` 及相邻聚合阶段；合并重复风险但不能改变事实状态。
- `narrative_composition.py`、`narrative_evidence.py` 和 `report_*` 生成用户叙事；确定性版本号记录在响应元数据中。
- `quality4.py` 与 `engine.py` 中的组合 Gate 检查 evidence、coverage、风险、报告状态与上下文一致性。Gate 失败必须保留 BLOCKED。

### 2.6 Release quality gate 与最终快照

`backend/review_v2/final_snapshot.py` 使用独立 SQLite `backend/data/review_snapshots.sqlite3`（可由 `REVIEW_V2_SNAPSHOT_DB` 改写）保存 `tasks/runs/exports`。它不做质量判断，只冻结引擎结果并绑定：

- `review_task_id`
- `review_run_id`
- `fact_snapshot_id`
- `rule_result_version`
- `report_version`
- `gate_version`
- `snapshot_hash`
- `passed_report_version`

导出时必须是当前任务最新 run、内容 hash 一致、Gate 为 `REPORT_READY` 且无 failures/blocking rules；不能回退到旧的 passing run。

## 3. 关键目录与文件：问题到代码的导航

### 3.1 总入口与注册

| 文件/目录 | 职责 | 遇到什么问题先看这里 |
|---|---|---|
| `backend/routers/review_v2.py` | HTTP 输入、文件解析、鉴权、运行快照、导出 | 接口 4xx/5xx、文件入口与纯文本入口不一致、响应字段缺失 |
| `backend/review_v2/engine.py` | 旧兼容主引擎、所有规则阶段编排、技术专项、风险聚合、报告和 Gate | coverage/risk/report 不一致、技术合同状态、Gate 阻断；文件超过 53k 行，先按 rule id/函数名定位 |
| `backend/review_v2/contract_registry.py` | 30 个 V2 类型、别名、显示名、checklist 映射 | 类型别名、错误 checklist、前后端枚举不一致 |
| `backend/review_v2/fact_routing.py` | 选择类型、文档重分类、阶段一致性 | employment/labor_contract 绕路、类型重识别、报告类型漂移 |
| `backend/review_v2/fact_module_registry.py` | ACTIVE 事实族注册 | 为什么某类型没走 Verified FactStore；禁止默认回退劳动 schema |
| `backend/review_v2/domain_selection.py`, `domain_resolution.py`, `domain_packs.py` | 文档域分类与冲突处理 | sale/service/technology 混淆、技术子类型分流 |

### 3.2 事实抽取与核验

| 文件/目录 | 职责 | 常见定位 |
|---|---|---|
| `backend/review_v2/deepseek_transport.py` | 家族无关 DeepSeek JSON transport | API 配置、JSON 失败、网络错误；不得加其他 provider |
| `backend/review_v2/deepseek_facts.py` | 劳动族抽取/核验 prompt 与批处理 | 劳动事实漏抽、Verifier response、劳动 prompt 协议 |
| `employment_fact_schema.py` | 劳动/竞业/保密概念与 element 映射 | EMP/NC/NDA 字段或 active scope |
| `employment_fact_store.py` | 劳动事实绑定、状态、debug 输出 | span、重复引文、证据/值校验、事实冲突 |
| `employment_fact_pipeline.py` | 劳动两阶段抽取、核验、规则适配 | 修复预算、失败关闭、请求级 Store 生命周期 |
| `fact_verification.py` | 劳动候选投影与 verified store | ABSENT/UNKNOWN/拒绝状态被错误放行 |
| `unified_facts/schema.py` | 通用概念、模块与动态选择抽象 | 新合同族 schema 的入口 |
| `unified_facts/pipeline.py` | 通用全文抽取、核验、修复、最终快照重核验 | stale certificate、跨批矛盾、遗漏检查、修复后复核 |
| `unified_facts/store.py` | Candidate/Verified Store、证据绑定、snapshot | fact_id、hash、span、scope 完整性 |
| `unified_facts/certificates.py` | 核验证书与当前候选绑定 | 旧 fact_id/旧响应被复用 |
| `unified_facts/normalization.py`, `ontology.py` | 强类型与 ontology 归一 | money/date/duration/formula、同义语义映射 |
| `fact_number_normalization.py`, `fact_scalar_normalization.py`, `fact_enum_normalization.py` | 公共 scalar 工具 | 中文金额、wrapper、枚举漂移 |

### 3.3 借款专项

| 文件 | 作用 |
|---|---|
| `unified_facts/loan.py` | 95 个概念、26 roots、动态子模块选择；无父关系时 active scope 63 |
| `unified_facts/loan_pipeline.py` | loan V2 唯一生产入口、Store 上下文、响应/debug |
| `unified_facts/loan_bindings.py` | 48 个 L 节点到 fact concepts/elements 的显式绑定 |
| `unified_facts/loan_rules.py` | 现有确定性借款规则适配 |
| `unified_facts/loan_costs.py` | Verified facts 驱动的成本分析 |
| `unified_facts/loan_formulas.py` | 年/月/日利率与计息公式确定性生成 |
| `loan_contract_checklist.py` | 原有 48 节点和法律判断定义 |
| `loan_facts.py`, `loan_costs.py`, `loan_semantics.py` | 旧兼容代码/公共语义；普通借款 V2 不得重新进入这些原文提取路径 |

### 3.4 技术合同专项

| 文件 | 作用/定位 |
|---|---|
| `technology_contract_checklist.py` | TC 清单和子类型适用性定义 |
| `technology_service_analysis.py` | 技术交易分类、技术咨询/服务识别、付款分析 session |
| `technology_fact_ontology.py` | 技术事实命名与同义映射 |
| `technical_component_facts.py` | 技术 component 层 |
| `consulting_element_facts.py` | 技术咨询项目、交付、付款、输入、保密等 element fact |
| `technology_service_elements.py` | 技术服务/咨询 element 投影与状态 |
| `obligation_detail_elements.py` | 义务细节、列表子项、期限/方式拆分 |
| `confidentiality_remedies.py` | 保密违约、停止使用/披露、减损、返还删除 |
| `technology_patent_transfer_analysis.py`, `patent_transfer_elements.py`, `application_transfer_elements.py` | 专利权/申请权转让 |
| `license_control_facts.py`, `license_terms.py` | 技术许可 |
| `entrusted_development_elements.py`, `cooperative_element_facts.py` | 委托/合作开发 |
| `element_evidence_projection.py` | canonical element 到报告 evidence 的最终反投影、旧 MISSING 刷新 |
| `scripts/run_round41_current.ps1` ～ `run_round45_current.ps1` | 两个审查立场的真实 `/review-v2/file` 验收 |
| `artifacts/technology_pass_semantics/round*/` | 输入、before/final 报告、acceptance、源码 hash；判断轮次状态的权威证据 |

### 3.5 Evidence、叙事与 Gate

- `clause_parser.py`：条款、section、block type、绝对 offset。列表引言/子项作用域问题先看此处。
- `canonical_claims.py`：canonical claim 注册与去重。
- `element_resolution.py`：element 状态合成。
- `element_evidence_projection.py`：最终证据反投影及完整性审计。
- `acceptance_evidence.py`、`narrative_evidence.py`：验收/叙事所用证据边界。
- `adverse_evidence.py`、`adverse_consistency.py`、`adverse_theme_projection.py`：不利事实与风险方向。
- `report_state_consistency.py`、`final_context_consistency.py`、`claim_scope_consistency.py`：跨层一致性。
- `quality4.py`：质量检查；禁止为了某样本直接放宽。
- `report_statistics.py`：coverage/risk 统计。
- `final_snapshot.py`：最终运行版本冻结及导出门禁。

### 3.6 测试、fixtures、artifacts

- `backend/tests/`：当前 360 个 `test_*.py` 文件；按领域和缺陷轮次组织。
- `backend/tests/fixtures/`：静态文本/JSON holdout；Round41～45 fixtures 明确存在。
- `test_data/`：真实 DOCX 样本，如借款 72/98/101/49/99/104。
- `scripts/`：真实接口验收、语义审计、历史聚类、投影扫描。
- `artifacts/`：每轮报告、JUnit、模型调用与 acceptance。旧 acceptance 只能说明其对应源码 hash，不能覆盖更新后的失败。

## 4. 合同类型与当前完成度

### 4.1 注册的 30 个 V2 类型

| 分组 | 类型 | checklist 节点数 | 统一 Verified FactStore 状态 |
|---|---|---:|---|
| 常规民商 | lease, sale, gift, deposit, work_contract, transportation, agency, service, guarantee, finance_lease, warehouse, construction, commission_agency, utility_supply, brokerage | 40～56 | 未迁移；`LEGACY_COMPATIBILITY` |
| 借款 | loan | 48 | ACTIVE；48/48 已绑定，真实泛化仍 BLOCKED |
| 技术 | technology | 53 | 未注册统一 Store；专用 canonical/projection 系统与大量真实回归 |
| 劳动族 | labor(22), non_compete(6), confidentiality(8), employment_termination(19) | 如左 | ACTIVE employment pipeline |
| 物权担保 | mortgage(14), movable_pledge(14), equity_pledge(14), rights_pledge(15) | 如左 | 未迁移 |
| 股权投资 | equity_transfer(9), capital_increase(17), investment(14), shareholders(11) | 如左 | 未迁移 |
| 商业经营 | operating_cooperation(11) | 11 | 未迁移 |

技术合同内部可识别的子类型至少包括：`ENTRUSTED_DEVELOPMENT`、`COOPERATIVE_DEVELOPMENT`、`TECHNICAL_CONSULTING`、`TECHNICAL_SERVICE`、`TECHNOLOGY_LICENSE`、`TECHNOLOGY_TRANSFER`；转让/许可又有专利权、专利申请权、技术秘密等专项模块。它们不是 `ContractType` 顶层枚举。

### 4.2 状态分层

**已稳定（就对应事实链和现有证据而言）**

- 劳动主合同：三份 fresh DeepSeek 合成 holdout 均 `REPORT_READY`，另有 102 劳动合同实跑记录；仍需留意独立竞业既存断言差异。
- Round45 对应的技术咨询样本：双立场 `REPORT_READY`，5/5 targeted、234/234 consulting/adjacent protection。
- 技术合同早期保护集覆盖技术咨询、服务、委托/合作开发、专利/申请权/秘密转让、专利/秘密许可等；“稳定”只代表各 acceptance 所绑定源码和样本，不代表统一 Verified Store 已完成。

**已完成真实合同测试但仍需泛化**

- 普通借款：自动化 339/339；真实六份仅 72 PASS，98/101/49/99/104 BLOCKED，权威文件为 `artifacts/loan_verified_acceptance/final-status.json`。
- 技术咨询：Round41、42、43 generalization、44、45 均形成真实/接口产物，但用户报告存在一份“新的技术咨询合同”暴露 TC-01/08/11/12 投影问题。仓库未发现该新样本的独立输入与 acceptance，故具体当前结果为 **UNKNOWN，优先复现**。

**尚未完成统一事实迁移**

- 除 employment 四类和 loan 外的全部类型。
- guarantee/mortgage/pledge 虽有专用 facts 模块，不等于已进入动态 schema + Verifier + Verified FactStore。
- 技术合同事实层仍是专用兼容架构，尚未成为通用框架 family。

**已知边界**

- 全文事实抽取硬上限 60,000 字符，超限阻断，不截断。
- 新事实链必须有 DeepSeek 配置；`use_llm=false` 不能绕过事实抽取。
- 借款真实模型仍存在 stale fact scope/ontology/verifier hallucination/formula 问题（详见第 12 节）。
- 旧基线有两个保留差异：`L-05-02` 与 utility supply；不得为新迁移篡改断言。
- `artifacts/fact_migration/migration-status.json` 是较早阶段历史，仍写 loan candidate；当前代码和 `loan-verified-migration.md` 已将 loan 注册为 ACTIVE。读状态时以新文件和实际 registry 为准。

## 5. 技术合同专项：Round41～Round45

### 5.1 各轮证据化历史

| Round | 根因/目标 | 修改重点 | 当前证据 |
|---|---|---|---|
| 41 | 技术咨询已有事实未完整进入 component/element，导致项目、交付、质量、责任等假缺失 | `consulting_element_facts.py`、`technology_service_elements.py`、`obligation_detail_elements.py`、`engine.py` 等，将咨询事实拆为可投影组件 | 双立场 `REPORT_READY`；acceptance 记录最终组件状态 |
| 42 | 第二种措辞下列表引言、跨条款输入义务、保密例外/退出安排未泛化 | 扩展公共事实与 element 组合，不改 Gate；运行 17 个技术保护样本 | 目标 5/5；Round41/36 projection 131/131；保密 penalty 38/38。保护集 15/17 ready，2 个模型依赖秘密转让样本 BLOCKED |
| 43 classification | 技术咨询被 service/sale 家族分数压过，产生 `UNCERTAIN_CONFLICT` | `technology_service_analysis.py`、`primary_purpose.py`、`domain_selection.py`；增强交易本质分类 | 分类 56/56；文档域回到 TECHNOLOGY。随后 TC-08-05 付款事实投影闭环，双立场 ready |
| 43 generalization | 63 万咨询费、里程碑付款和不同咨询措辞需要公共归一 | `consulting_element_facts.py`、`penalty_base.py` | targeted 156/156；双立场 ready |
| 44 | 新咨询合同中的保密控制、材料退出、责任 element 已有原文但投影未刷新 | 技术咨询/保密/义务 detail 的 canonical element 投影 | 最终报告显示 TC-01/08 多数已覆盖；TC-11-03 的“销毁”及 TC-12-02 若干项仍按原文真实缺失 |
| 45 | 新样本中同义 key、跨句/列表作用域、更新 evidence 后旧 MISSING 残留 | `consulting_element_facts.py`、`technology_service_elements.py`、`obligation_detail_elements.py`、`confidentiality_remedies.py`、`technology_service_analysis.py`、`engine.py`；统一刷新 projection/SEARCH_AUDIT | 双立场 `REPORT_READY`；targeted 5/5；保护集 234/234；full suite 未跑（按当轮请求） |

### 5.2 用户所述“当前新技术咨询合同”

必须先区分两件事：

1. `round45_consulting_projection` 仓库产物本身已通过。
2. 用户描述的另一份“新技术咨询合同”出现 TC-01-03、TC-08-01～04、TC-11-01～04、TC-12-02 泛化失败，但仓库中没有可唯一对应的新输入、run id 或 acceptance。其当前状态是 **UNKNOWN/TODO：先固定输入 hash 并复现**。

不能在没有该新报告的情况下武断把每个 MISSING 都标成假缺失。可用 Round45 before/final 解释已知模式：

| 规则 | Round45 已证实的假缺失/刷新问题 | Round45 final 中真实仍缺 |
|---|---|---|
| TC-01-03 | consulting project 原文已有但未映射；final 四要素全覆盖 | 无 |
| TC-08-01 | acceptance standard 未投影；final 全覆盖 | 无 |
| TC-08-02 | qualified decision risk 未从免责声明/责任条件组合投影；final 全覆盖 | 无 |
| TC-08-03 | truthfulness/completeness 未投影；final 全覆盖 | 无 |
| TC-08-04 | defect trigger、correction period、termination remedy 投影/刷新；final 为“通过” | `refund_remedy` element 仍 MISSING，但该规则按适用结构仍可通过 |
| TC-11-01 | third-party restriction/security 等原文事实未完整投影；final 全覆盖 | 无 |
| TC-11-02 | independent-development exception 未投影；final 全覆盖 | 无 |
| TC-11-03 | retained backup/copy deletion/disposal confirmation 等刷新 | `confidential_material_destruction` 真实 MISSING，因此部分覆盖 |
| TC-11-04 | damage、stop use/disclosure、mitigation 等未完整合并；final 通过 | 专项 penalty/excess loss 为 NOT_APPLICABLE，不是缺失 |
| TC-12-02 | direct damage、cost、notification deadline、remedies 等跨句事实未投影 | `lawyer_selection` 真实 MISSING；`defense_control` 仅 PARTIALLY_COVERED，因此规则部分覆盖 |

对用户的新合同，必须用其原文重新判定。判断假缺失的必要证据是：存在 DIRECT affirmative source evidence 或已验证 canonical fact，却仍有对应 element `MISSING`/SEARCH_AUDIT `NOT_FOUND`。没有原文支持的 element 必须保留真实缺失。

### 5.3 当前最大技术合同问题

- 技术专项能力分散在 `engine.py` 大量函数和多个 `*_facts/*_elements` 模块，更新顺序容易让旧 coverage/SEARCH_AUDIT 残留。
- canonical key 与 element fact key 并非总是单一注册源；同义事实可能进入不同 namespace。
- 技术事实不是统一 Verified FactStore 的事务快照，仍要靠多层一致性 Gate 阻止错报。
- Round45 full suite 未跑，因此不能把 234/234 等同全仓无回归。

## 6. 不可破坏的设计原则

1. 目标主链固定为：**全文 → DeepSeek 抽取 → canonical facts → FactStore → Verifier → rules → report**。
2. 在已迁移合同族中，Verifier 是唯一事实门禁；未经 verified 的候选不得进入规则、风险、叙事或报告。
3. 不恢复 legacy fallback。抽取/核验失败必须 BLOCKED，不能悄悄改用关键词报告。
4. 不允许规则重新扫原文产生第二套事实；原文只用于抽取输入、证据绑定和最终审计。
5. 不为单个合同编号、文件 hash 或固定句子写特判。
6. 不为 PASS 放宽 Gate、Verifier scope、证据强度或测试断言。
7. `MISSING` 必须代表全文真实不存在对应 active fact；部分事实应为 PARTIAL/UNKNOWN，而非完整缺失。
8. 同一命题存在 DIRECT affirmative evidence 时，不能同时保留对应 SEARCH_AUDIT `NOT_FOUND`。
9. 修公共能力：schema、normalization、ontology、span、projection、scope refresh；不修样本文字。
10. 修改公共模块后必须跑目标测试、相邻合同保护集和 Gate/证据一致性回归。
11. 法律阈值、期限计算、金额比较、适用性和 polarity 由确定性代码完成，不让模型自由裁决。
12. DeepSeek-only。错误不触发 OpenAI/Claude/Gemini 或任何 provider 替换。

## 7. Evidence / Fact / Projection / SEARCH_AUDIT

### 7.1 Source evidence

有效 source evidence 必须可以回到合同：

- `clause_id`：解析后的条款身份。
- `section/location`：章节位置。
- `quote/quoted_text`：逐字原文。
- clause-relative span 与可确认时的 document absolute span。
- `source_type`：如 DIRECT、CONTEXTUAL、SEARCH_AUDIT、LEGAL_AUTHORITY。

**DIRECT** 表示引文本身直接蕴含该属性。**CONTEXTUAL** 只提供上下文，不能单独支撑强肯定结论。法律条文不是合同事实证据；SEARCH_AUDIT 也不是正向证明。

### 7.2 Canonical fact

canonical fact 是对原文同义表达的稳定化：

- `concept/key`
- `normalized_value`
- state（PRESENT/ABSENT/EXPLICIT_NONE/DEFERRED/UNKNOWN/CONFLICT/NOT_APPLICABLE）
- assertion（EXPLICIT/INFERRED）
- confidence
- evidence ids/spans
- fact id 与所在 snapshot

强类型值不能用自然语言占位。只有 PRESENT 带 value；其他状态不能带 `null` 伪装值。

### 7.3 Component 与 element

- component 聚合同一业务语义的事实，例如 `consulting_payment` 或 `confidentiality_controls`。
- element 是某条规则中的原子要求，例如“付款总额”“支付节点”“通知期限”“通知渠道”。
- 一个事实可投影到多个 element，但每个 element 必须有明确 key 和支持证据。
- 多 element 规则：全部覆盖为 PASS；部分覆盖为 PARTIAL；全部且真实不存在才 MISSING；前提不成立为 NOT_APPLICABLE。

### 7.4 SEARCH_AUDIT

当 projection 后仍有缺口，`_record_specialized_search_audit()` / `_resolve_final_element_searches()` 对客观目标做最终查漏。正确语义：

- `FOUND`：找到可绑定 source evidence，应回写 canonical element 并刷新旧 MISSING。
- `NOT_FOUND`：全文审计未找到，作为缺失证明的一部分。
- 它不能凭关键词片段另造一个与 Store 冲突的事实，也不能作为 PASS evidence。

### 7.5 状态关系

| 状态 | 含义 |
|---|---|
| PASS/通过 | 所有必要、适用 element 都有足够 verified/DIRECT 支撑 |
| PARTIAL/部分覆盖 | 至少一个 element 已覆盖，另有真实缺口或仅部分事实 |
| MISSING/缺失 | active + applicable element 在结构化事实和全文审计中均无支持 |
| NOT_APPLICABLE | 父事实/交易结构使该要求不适用；不得当作 ABSENT |
| UNKNOWN/待核验 | 冲突、低置信、无法确定；不能转换为完全缺失或通过 |

### 7.6 高频 Bug 模式

1. canonical fact 已有，但未注册到对应 element key。
2. element 更新为 COVERED 后，旧 coverage/MISSING/SEARCH_AUDIT 未重新计算。
3. 列表引言定义共同主体、条件或动作，子项解析时丢失作用域。
4. 跨句“该报告/上述资料/前款情形”指代未合并。
5. 条件句把 trigger、义务、补救混成一个 boolean。
6. “五个工作日内”等期限未拆为 amount/unit，或期限与渠道相互误证。
7. heading 提供字段名、正文只给 value，二者未组合。
8. 同义事实写入不同 canonical key，projection 只看其中一个。
9. evidence id/span 更新后，旧 decision trace 或 absence bundle 仍引用上一版。
10. CONTEXTUAL evidence 被当成 DIRECT，或者 SEARCH_AUDIT 被报告成正向证据。

## 8. 测试体系与最低回归要求

### 8.1 测试层级

- **单元测试**：normalization、schema、ontology、span、element resolver、公式、规则谓词。
- **集成测试**：route → pipeline → Store → rules → response，通常 mock DeepSeek 协议但不 mock 核心业务层。
- **回归测试**：历史 bug rule id、投影刷新、Gate/报告一致性。
- **真实合同测试**：真实 DOCX 经 `/review-v2/file` 和真实 DeepSeek；必须保存文件 SHA256、模型响应、run id、报告。
- **泛化测试**：此前未参与修复的不同结构/措辞，不能把 replay 当 fresh call。
- **protection set**：技术合同其他子类型、相邻合同、双审查立场，防公共修改退化。
- **release gate 测试**：错误证据、状态冲突、旧快照、BLOCKED 导出等必须 fail closed。

### 8.2 当前可证实的结果

- 测试文件数量：360 个 `backend/tests/test_*.py`（不是通过数）。
- Employment：文档记录专项 30；扩展 88 中 87 pass、1 个既存 noncompete 失败；三份 fresh DeepSeek holdout 均 ready。
- Loan：`final-status.json` 记录自动化 339/339；legacy baseline 104 pass / 2 个既存失败；真实六份仅 1 PASS。
- Technology Round45：5/5 targeted，234/234 consulting/adjacent protection；full suite `NOT_RUN_BY_REQUEST`。
- Round43 generalization：156/156 targeted。
- 仓库当前没有一份“全 360 文件最新全量 pytest 全绿”的证据，状态为 **UNKNOWN/NOT RUN**。

### 8.3 修改后的最低命令集

修改技术咨询公共 projection 前：

```powershell
python -m pytest -q backend/tests/test_round45_consulting_projection_refresh.py
python -m pytest -q backend/tests/test_round44_consulting_projection_refresh.py backend/tests/test_round43_consulting_fact_generalization.py
python -m pytest -q backend/tests/test_consulting_final_fact_binding.py backend/tests/test_consulting_final_projection.py backend/tests/test_consulting_verified_fact_projection.py
python -m pytest -q backend/tests/test_technology_element_evidence_integrity.py backend/tests/test_technology_pass_semantic_sources.py backend/tests/test_technology_verified_decision_boundary.py
```

若改 `engine.py`、clause parser、canonical/evidence/projection 公共层，再跑技术保护集（Round42 protected 对应的开发、转让、许可、服务、咨询测试）以及 Gate/状态一致性测试。真实验收使用 `scripts/run_round45_current.ps1` 的模式，但输出到新 Round 目录，不覆盖旧证据。

若改 employment/loan 通用事实层，至少运行：

```powershell
python -m pytest -q backend/tests/test_employment_fact_pipeline.py backend/tests/test_verified_fact_coverage.py
python -m pytest -q backend/tests/test_unified_fact_framework.py backend/tests/test_loan_verified_pipeline.py backend/tests/test_loan_model_shapes.py backend/tests/test_loan_certificate_semantics.py
```

最终发布前才跑全量；不要因全量耗时而把局部 targeted 结果描述成全仓通过。

## 9. 数据库与运行时数据结构

### 9.1 业务数据库 `backend/app.db`

SQLAlchemy 配置在 `backend/storage/database.py`，默认 `sqlite:///./app.db`；SQLite 启用 WAL/NORMAL 等 pragma。测试环境要求 `DATABASE_URL` 指向 `SAGE_TEST_ROOT` 下的隔离文件；生产 SQLite 要显式绝对路径。

`backend/storage/models.py` 的实际表：

- `user`
- `record`：`report_markdown/raw_output/metadata_json`
- `feedback`
- `bonus_log`
- `reward_logs`
- `invite_rewards`
- `blacklist`
- `intercept_logs`
- `file_hash_cache`
- `admin_logs`
- `admins`
- `security_events`
- `task_record`：task_id、文件、状态、result/error、metadata/validation/summary、trace_id 等。

本地 `backend/app.db` 已知损坏，不能修改、覆盖、切换或删除；生产数据库此前只读复核健康且与本地库独立。数据库恢复不是本交接的第一优先级。

### 9.2 Run 与审查快照

业务 ORM 中**没有**名为 `Run` 的 SQLAlchemy 模型。V2 Run 是 `final_snapshot.SnapshotStore` 自建 SQLite `runs` 表：

- `id/task/created_at/updated_at/state`
- `payload`：完整最终响应 JSON
- `payload_hash`
- `binding`：版本与 Gate 绑定

`FactStore` 不是业务 ORM 表：

- employment `FactStore` 是请求级内存对象，其公共/调试投影进入最终响应 payload。
- loan `VerifiedFactStore` 同样是请求级内存对象；snapshot/debug 被投影进响应，再由 `SnapshotStore` 作为 payload 一部分冻结。
- 尚未实现独立、可查询、规范化的 `facts/evidence/rule_results` 数据库表。

### 9.3 Evidence、rule result、report

- evidence 作为 item/coverage element/structured fact 内嵌 JSON 存放。
- rule result 是响应 `items[]`，版本为 `rule_result_version = digest(items)`。
- report 是响应 `result`/相关报告字段；`report_version` 为 run 完成时 UUID。
- `record` 表属于历史报告功能，与 V2 immutable run store 不是同一套结构。
- prompt 的实际 template/content hash 尚未作为一等字段持久化；这是 Prompt Version Management 的缺口。

## 10. Prompt 使用现状

### 10.1 实际 DeepSeek 配置

- `backend/model_settings.py`：唯一 `MODEL_DEFINITIONS['deepseek']`，默认 `deepseek-chat`，URL `https://api.deepseek.com/v1/chat/completions`。
- `backend/reasoning/llm_client.py`：DeepSeek-only 的通用调用，有界重试/熔断，无 provider substitution。
- `backend/review_v2/deepseek_transport.py`：结构化 JSON 调用，供 facts pipeline 使用。

### 10.2 Prompt 清单

| 用途 | 定义位置 | 调用位置 | 输入/输出 | 版本与持久化 |
|---|---|---|---|---|
| Employment extraction | `deepseek_facts.py::SYSTEM` + `employment_fact_schema.INSTRUCTIONS` + `fact_semantic_contracts.INSTRUCTIONS` | `deepseek_facts.extract()` | 全条款、active concepts、value schema → observations JSON | schema version 有；完整 prompt 无独立 ID/hash；raw result 进入 `structured_fact_debug` |
| Employment verifier | `deepseek_facts.py::verify()` 内 `system/instruction` | `employment_fact_pipeline.run()` | candidates、required fact ids、active concepts、全文 → checks/audits | 响应记录 model/usage；无正式 prompt registry |
| Unified extraction | `unified_facts/pipeline.py::EXTRACTION` | `extract_verified()` | family、active concepts、public schema、全文、verified roots → observations | schema `contract-facts-1.0`；prompt 内容无 hash/id |
| Unified verifier | `unified_facts/pipeline.py::VERIFICATION` | `certificates.verify_current()` | snapshot hash、current fact ids、context facts、全文 → checks/audits/corrections | certificate 绑定候选 hash；prompt 本身无 registry version |
| V2 semantic review | `llm_semantic_reviewer.py::_build_prompt/_build_batch_prompt` | `review_checkpoint_semantics` 相邻函数通过 `reasoning.llm_client.call_llm()` | checkpoint、候选证据、确定性 judgment → JSON semantic verdict | 元数据有 prompt version 字段，但模板未统一版本管理 |
| 旧主链单次综合审查 | `layers/inference_layer.py::_load_prompt_template()` | `InferenceLayer.process()` → `call_llm()` | 合同/额外要求 → 文本报告 | 属于旧版/非 V2 facts-first 入口；存在 fallback report，不能引入 ACTIVE V2 |
| 确定性 narrative/risk/recommendation | `engine.py`、`narrative_composition.py` 等 | V2 后处理 | facts/rule results → deterministic strings | `engine.py` 暴露版本常量：`PROMPT_VERSION`、`FACT_PROMPT_VERSION`、`VERIFIER_PROMPT_VERSION`、`RISK_AGGREGATION_PROMPT_VERSION`、`RECOMMENDATION_PROMPT_VERSION`；其中部分实际是确定性算法标签，不代表真实 prompt template 版本 |

分类主要由 `technology_service_analysis.py`、`domain_selection.py` 等确定性打分/规则完成；当前未发现一个独立 DeepSeek“全合同分类 prompt”作为 V2 必经步骤。应标为：**分类 prompt 尚未实现；当前分类以代码为主**。

Prompt 元数据会出现在引擎响应/system metadata 和部分 artifact，但 `SnapshotStore` 没有结构化 `run_prompt_versions` 字段；只能从 payload 间接读取，且没有 content hash。下一阶段准备补 Prompt Version Management。

## 11. Prompt Version Management 最小设计

不要先重构调用链。最小方案：

1. 新增不可变 `PromptDefinition`（可先用代码 registry + JSON，后续数据库）：
   - `prompt_id`：稳定用途 ID，如 `employment.extract`。
   - `prompt_name`
   - `prompt_version`：显式语义版本。
   - `template_hash/content_hash`：对最终 system/template 字节做 SHA256。
   - `model`：实际 DeepSeek model。
   - `created_at`
   - `status`: `CANDIDATE | PRODUCTION | RETIRED`。
2. 每次模型调用返回 `PromptUse`：prompt_id/version/hash/model/stage/request id。
3. 每次 Run 在最终 payload 和 binding 中记录去重后的 `prompt_uses[]`；`fact_snapshot_id` 和 `snapshot_hash` 自然覆盖它。
4. production/candidate 切换通过显式配置选择版本；一个用途同时只能有一个 production。
5. 回滚只切 registry 指针到已冻结版本，不改旧模板内容；旧 Run 仍能还原真实版本。
6. regression runner 对同一输入在 production/candidate 上并行生成 artifact，比较 facts、evidence、rule state、Gate、token/latency；禁止只比最终 Markdown。
7. DeepSeek model 名、温度、JSON mode、schema version也进入调用指纹。

暂不建议把 prompt 内容直接做可在线任意编辑的数据库 CRUD；先解决可识别、可冻结、可回滚和可对比。

## 12. 待办优先级

### P0：复现并修复当前“新技术咨询合同”Round45 后的泛化失败

1. 固定新 DOCX、提取文本、SHA256、双立场、run id；新建 Round46（或下一顺序）artifact，不能覆盖 Round45。
2. 对 TC-01-03、TC-08-01～04、TC-11-01～04、TC-12-02 输出：source evidence → canonical fact → component → element → SEARCH_AUDIT → final decision。
3. 将每个缺口分为：抽取/解析、canonical key、projection、旧状态刷新、或真实缺失。
4. 只修公共能力，并至少加入一个措辞变体；跑 Round41～45 与其他技术子类型保护集。
5. 只有新样本双立场、targeted、protection、Gate/evidence integrity 全通过才关闭。

### P1：第三份完全不同表达的技术咨询泛化

使用此前未参与修复的结构：不同标题层级、列表、跨句指代、条件/期限、付款/保密/侵权机制。必须 fresh interface run，不能 replay 旧 extraction。

### P2：Prompt Version Management

按第 11 节实现最小 registry、Run 记录、production/candidate、回滚和 regression diff。

### P3：普通借款真实 DeepSeek 阻塞

`final-status.json` 当前仍是 BLOCKED：

- 98：复利/凭证机制被 Verifier 拒绝，且出现 `INCOMPLETE_FACT_SCOPE`。
- 101：报告 pipeline PASS，但年利率转日公式缺明确除数/日利率依据。
- 49/104：`实际占用本金` 应统一为 `UNPAID_PRINCIPAL`。
- 99：Verifier 幻觉出短信/微信/邮件/书面渠道。

用户此前要求的 stale certificate、ontology、evidence hallucination post-validation、确定性公式修复尚无“12 份全 PASS”权威 artifact，不能宣称完成。

### P4：其余合同族迁移

在 loan 泛化关闭后，才按族推进 guarantee/mortgage/pledge 等。每族必须注册动态 schema、Verifier、Store、消费者清单和 protection set；不能仅增加 registry 名称。

### P5：发布与数据事项（独立）

- `docs/release-acceptance-pending.md` 记录的 Docker 最终验收环境问题曾为 BLOCKED；之后会话发生过生产部署，但仓库没有一份更新后的统一 release gate artifact。当前正式发布状态应人工重新核实，标为 **UNKNOWN**。
- 本地坏库的 `DATABASE_SWITCH_GATE` 与代码发布分开，继续等待四条残缺任务的人工处置。

## 13. CodeBuddy 接手步骤

### 13.1 先读

按顺序：

1. 本文。
2. `AGENTS.md`（DeepSeek-only）。
3. `engine.py::review_contract_v2()`、`fact_routing.py`、`fact_module_registry.py`。
4. 当前任务若是技术咨询：`technology_contract_checklist.py`、`technology_service_analysis.py`、`consulting_element_facts.py`、`technology_service_elements.py`、`obligation_detail_elements.py`、`element_evidence_projection.py`。
5. `backend/tests/test_round41...45*` 与对应 fixtures/artifacts。
6. 若是统一事实层：`unified_facts/pipeline.py/store.py/certificates.py/schema.py`。

### 13.2 修改前

- `git status --short`，记录当前 dirty worktree；不要 reset/clean。
- 记录目标输入和关键源码 SHA256。
- 跑目标测试，保留“修改前”状态。
- 从失败报告提取每个 rule 的 coverage elements、evidence ids、absence searches、Gate failures。

### 13.3 定位顺序

```text
原文是否有明确事实？
 -> clause/section/span 是否正确？
 -> canonical key/value/state 是否存在？
 -> component 是否合并跨条款事实？
 -> element 是否投影？
 -> 更新后旧 MISSING/SEARCH_AUDIT 是否刷新？
 -> deterministic rule 是否按 element 判断？
 -> risk/narrative/report 是否同源？
 -> Gate 是否指出真实不一致？
```

不要从最终 Markdown 反向加关键词。先看 structured debug、`decision_trace`、`coverage_elements`、`element_absence_searches`。

### 13.4 验收

- 最小单测 + 一个变体。
- 目标真实合同双立场。
- 相邻轮次/子类型 protection set。
- evidence integrity：每个 COVERED 可回溯，DIRECT 文本真实存在。
- absence integrity：DIRECT affirmative 与 NOT_FOUND 不共存。
- Gate 未放宽，无 legacy fallback，无样本 id/hash/原句特判。
- 生成 acceptance JSON：输入 hash、run id、源码 hash、测试计数、Gate、未解决项。

### 13.5 汇报格式

```text
范围：
根因（按抽取/归一/绑定/projection/rule/report 分类）：
修改文件与公共机制：
未修改的业务规则/Gate：
自动化测试：X passed / Y failed（列既存失败）：
真实合同：输入 hash、双立场、Gate、关键 rule 状态：
保护集：
仍 BLOCKED 的事项：
artifact 路径与源码 hash：
```

## 14. 已知坑

1. **commit 不代表当前代码**：核心新模块大量 untracked，必须记录工作区/hash。
2. **历史 artifact 会过期**：某轮 PASS 不覆盖更晚源码或新样本；以输入+源码 hash 配对。
3. **技术 canonical facts ≠ Verified FactStore**：不要误称所有合同已统一迁移。
4. **旧 migration-status 会误导**：它还写 loan candidate；实际 registry 已 ACTIVE，但真实泛化仍 BLOCKED。
5. **关键词补丁会制造交叉误证**：通知期限不能证明通知渠道；清偿顺序中的“复利”不能证明计收复利；账户/扣收不能证明债权凭证。
6. **列表引言丢失**：共同动词/主体/条件常在冒号前，子项只有宾语。
7. **跨句指代**：不能只看单句，也不能无证据扩张“该/上述”。
8. **heading/value 拆开**：标题定义语义，值在下一行；parser 与 evidence 仍要保留真实 span。
9. **状态刷新顺序**：补 fact 后必须重算 component、element、coverage、absence、risk、report，不能局部 mutate。
10. **stale verifier certificate**：候选变化后旧 snapshot/fact_id 永不复用；无效响应应重新核验当前候选。
11. **Verifier reason 不是证据**：任何 PRESENT correction/omission 必须有 clause + quote/span，并经确定性 post-validation。
12. **UNKNOWN 不是 ABSENT**：不确定不能产生“合同未约定”的确定结论。
13. **NOT_APPLICABLE 由父关系决定**：模型不能输出；父事实不成立时不加载子 schema。
14. **公式不能让模型自由创作**：利率单位、计息基数、day-count basis 由 verified facts 和代码决定。
15. **use_llm=false 不关闭 ACTIVE facts pipeline**：不能用它规避 DeepSeek 或 Verifier。
16. **fixture/replay 不等于 fresh DeepSeek**：验收报告必须标明 fresh/replay。
17. **Gate 是安全边界**：报告看似合理但 evidence/状态不一致仍应 BLOCKED。
18. **业务 DB 与 snapshot DB 不同**：`app.db`、`review_snapshots.sqlite3`、测试临时库不要混用。
19. **不要碰本地损坏 app.db**：恢复/切换有独立审批流程。
20. **前端历史 chunk/MIME**：部署时旧 HTML 可能请求已删除 hash，Nginx fallback 返回 `text/html` 导致 module MIME 错误；必须原子发布或保留兼容静态资产。
21. **`crypto.randomUUID` 兼容**：非安全上下文/旧浏览器不可直接依赖，当前有 `frontend/src/utils/runtimeId.mjs` 兼容实现。
22. **healthcheck 地址族**：显式 `127.0.0.1`，避免 localhost 解析 `::1` 而 Nginx 只监听 IPv4。
23. **低资源主机**：曾发生前端 Docker build OOM；资源错误不能记成代码 FAIL，也不能通过删构建步骤规避。

---

交接起点：先为用户所说的新技术咨询合同建立可复现的 Round46 证据包，再修 projection/SEARCH_AUDIT 公共链。不要先开发新合同族或 Prompt 管理。
