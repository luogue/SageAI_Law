# 劳动用工、担保物权与股权投资接入说明

本次沿用 `ReviewCheckpoint → 注册表 → 类型解析 → 适用性 → 原文要素覆盖 → 风险聚合 → 生产报告 → 导出` 链路，没有增加独立审查或报告引擎。保留工作区其他未提交改动，不修改已有合同专项规则的判断。

## 类型树及清单

`ContractTypeMeta.parent_family` 和 `CONTRACT_TYPE_TREE` 为新增的兼容字段；原有枚举、别名、响应键和扁平类型接口继续使用。

| 一级分类 | 响应键 | 合同类型 | 清单项数 |
|---|---|---|---:|
| EMPLOYMENT | labor | 劳动合同 | 19 |
| EMPLOYMENT | non_compete | 竞业限制协议 | 6 |
| EMPLOYMENT | confidentiality | 保密协议 | 8 |
| EMPLOYMENT | employment_termination | 劳动关系解除/终止协议 | 11 |
| SECURITY_PROPERTY | mortgage | 抵押合同 | 14 |
| SECURITY_PROPERTY | movable_pledge | 动产质押合同 | 14 |
| SECURITY_PROPERTY | equity_pledge | 股权质押合同 | 14 |
| SECURITY_PROPERTY | rights_pledge | 应收账款等权利质押合同 | 15 |
| EQUITY_INVESTMENT | equity_transfer | 股权转让协议 | 9 |
| EQUITY_INVESTMENT | capital_increase | 增资扩股协议 | 14 |
| EQUITY_INVESTMENT | investment | 投资协议 | 14 |
| EQUITY_INVESTMENT | shareholders | 股东协议 | 11 |

新增类型支持中文名称和常用协议名称别名。分类器优先匹配主合同标题；标题缺失时要求多个独立交易信号。已有借款、买卖、技术等主合同中的附属保密或抵质押文件名称不会单独触发新类型。明确的新增合同标题可以纠正错误的用户类型选择。泛称“质押合同”结合股权、应收账款等标的信号分流，信息不足时默认动产质押，需人工确认标的。

## 规则与复用

共56个独立专项节点：48个正向要素审查、8个不利条款审查。关联协议复用同一节点和要素定义，表中清单项数不能相加作为独立规则数量。

- 劳动：主体身份、期限、试用期和工资、工作内容地点、工时休息加班、工资支付、社保、劳动保护、培训服务期、解除终止、经济补偿、劳动争议；计算明确期限下的试用期上限，识别重复试用、社保放弃、任意解除免责及劳动者一般违约金。
- 竞业/保密/解除协议：秘密接触及范围、离职竞业期限补偿、保密内容及除外、使用披露限制、期限及资料返还、身份和违约救济、离职证明及转移交接。明确仅在职竞业不套用离职按月补偿要求；一般企业间保密不套用劳动者违约金限制。
- 抵质押：共享主债权、范围、权属处分、公司授权核验安排、在先担保及顺位、实现及清算、行权消灭、最高额场景。分别核对不动产/动产抵押登记、动产质押交付占有、股权出质登记、权利质押登记或凭证交付、应收账款回款控制；识别流押流质和以签约替代公示交付。
- 股权：主体权属、认缴实缴及法定出资责任、转让限制和其他股东权利、价格支付、交割与名册工商变更、治理知情权、增资认缴、估值及投后比例、陈述保证和救济、退出僵局。反稀释、优先权、回购及业绩承诺仅在约定该交易安排时触发。
- 直接复用原清单对象：`common_effective_clause`、`common_notice_delivery`。劳动争议单独配置劳动仲裁规则，避免套用普通商事仲裁条款。主债权、劳动报酬、股权交易价款等不能直接套用贷款人、买卖货物的专项判断，因此只复用适用的通用规则。
- 复用现有 `requirement`、`corpus_facts`、`direct_evidence`、覆盖要素验证、缺失检索、风险主题指纹、最终证据投射和PDF/Word生产Markdown导出。专项原文判定不交给模型改写；模型开关及通用规则原有路径保留。

覆盖继续使用原有输出：FULL/通过、PARTIAL/部分覆盖、MISSING/缺失、RISK/风险条款、N/A/不适用。只找到部分明确要素时保持部分覆盖；标题关键词和未填写的金额不能算完整覆盖。禁止性规则的通过表示“未发现该项不利约定”，不是“已约定禁止条款”。

新增类型复用 `_project_exact_element_evidence_bundles`，使部分覆盖和冲突场景同时保留正向证据、不利证据和缺失检索。没有绕过或降低发布质量门。唯一通用兼容修复为：法律时效检查用完整法名区分“劳动合同法”与已废止的“合同法”，仍检查真正的旧法引用。

## 文件清单（仅列本次范围）

新增：

- `backend/review_v2/priority_contract_types.py`：12个类型、层级元数据和主合同分类。
- `backend/review_v2/priority_checklist_helpers.py`：原清单构造器、原文要素配置、通用规则复用。
- `backend/review_v2/employment_contract_checklist.py`：劳动用工四类协议。
- `backend/review_v2/security_property_checklist.py`：抵押及三类质押。
- `backend/review_v2/equity_investment_checklist.py`：股权转让、增资、投资、股东协议。
- `backend/review_v2/priority_contract_review.py`：适用性、原文判定、试用期计算和风险主题绑定。
- `backend/tests/priority_contract_fixtures.py`：手写的12类正常、缺失、风险合同，独立于规则配置。
- `backend/tests/test_priority_contract_review.py`：98项接入验收测试。
- `scripts/run_priority_contract_acceptance.py`：输出36份原合同文本、生产报告和机器可读汇总。
- `backend/review_v2/PRIORITY_CONTRACTS.md`：本说明。

修改：

- `backend/review_v2/contract_registry.py`：枚举、别名、清单注册与类型树。
- `backend/review_v2/domain_selection.py`：新增类型识别、路由及清单隔离门；保留共享文件中的其他改动。
- `backend/review_v2/domain_resolution.py`：层级领域、标的和交易结构。
- `backend/review_v2/domain_packs.py`：新增领域包及父包关系。
- `backend/review_v2/semantic_reviewer.py`：现有判定入口接入专项规则。
- `backend/review_v2/engine.py`：适用性、确定性判定、专项后处理和最终证据投射的接入点。
- `backend/review_v2/report_context.py`：生产报告标题和场景。
- `backend/review_v2/perspective_resolution.py`：用人单位/劳动者、担保人/债权人及股权交易角色。
- `backend/review_v2/quality4.py`：“劳动合同法”名称误匹配修复。
- `backend/routers/review_v2.py`：API合同类型说明，复用原上传及导出端点。
- `frontend/src/views/ContractReviewV2.vue`：按三类分组展示12个新增选项。
- `backend/tests/test_review_v2_contract_registry.py`：类型集合、别名及原有建设工程动态清单访问器断言。实施前两个注册测试仍比较旧静态建设工程元组，现改为比较当前公开访问器，不改变建设工程规则。

## 验证与复现

在项目根目录使用PowerShell：

```powershell
$env:PYTHONPATH='backend;backend/tests'
$env:REVIEW_V2_LLM_ENABLED='false'
python -m pytest backend/tests/test_priority_contract_review.py -q
python scripts/run_priority_contract_acceptance.py
```

验收测试涵盖36个正常/缺失/高风险主场景，全部12类的分类纠偏、DOCX上传、PDF/DOCX导出，以及部分覆盖、空白模板、否定与防范条款、可选条款N/A、试用期阈值、重复风险主题、正反证据报告一致性、模型不能覆盖确定性结果、角色隔离和法律名称质量门。

新增类型最后独立验收为98项，日志为 `artifacts/priority_new_types_final.txt`。主要合同回归范围为注册表、买卖、借款、保证、建设工程、融资租赁和房屋租赁，共112项。此前与96项新增测试合并运行208项全部通过；共享工作区在执行期间仍有其他修改，最后与98项新增测试合并运行的结果为207通过、3项原有测试失败。最终记录以 `artifacts/priority_final_tests.txt` 为准，不能把当前主要回归描述为全绿。

最后3项失败为：`test_sale_review_boundary_payment_account_reasonable_penalty_and_common_layer`、`test_construction_fixture_corrections_for_subcontract_and_tender_points`、`test_negated_phrase_does_not_pollute_later_matches`。逐项复测时买卖用例通过，其余2项失败；禁用新增适配器的对照也为1通过、2失败。对应记录为 `artifacts/priority_final_legacy_recheck.txt` 和 `artifacts/priority_final_disabled_control.txt`。为遵守本次不修改其他稳定规则的边界，未调整这些旧规则或放宽其断言。

前端 `npm run build` 已通过，日志为 `artifacts/priority_frontend_build.txt`，存在原有依赖包体积提示。

扩大回归为全部16种现有专项清单测试文件、注册表、房屋租赁、Quality4及6.7冻结测试，194通过、5失败。失败对照已禁用新增适配器复跑，5项仍同样失败，未为本次类型接入更改相关旧规则：

| 测试 | 当前问题 |
|---|---|
| `test_gift_attached_obligation_remedy_depends_on_obligation_content` | 附义务赠与被当前证据门判为缺失，测试期望部分覆盖 |
| `test_gift_dependency_rules_sync_related_items` | 当前下游叙事替换了旧依赖规则引用 |
| `test_technology_fixture_entrusted_development_filters_cooperative_points` | 缺少测试指定的本地DOCX样本 |
| `test_quality4_public_review_result_has_no_review_level_severity` | 既有租赁样本仍被发布质量门拦截 |
| `test_hb4_freeze_closure_production_regressions` | 缺少 `test_data/7*.docx` |

对照记录：`artifacts/priority_regression.txt`、`artifacts/priority_disabled_control.txt`；实施前基线记录：`artifacts/priority_baseline.txt`。不能将扩大回归描述为全部通过。

验收样本与生产报告位于 `artifacts/priority_contract_acceptance/`，每个类型各有 `normal`、`missing`、`risky` 的 `.txt` 和 `.md`；36份均分类正确且发布质量门为 `REPORT_READY`。`summary.json`记录分类、规则数、覆盖分布和发布质量门，`source_hashes.json`保留交付核对时的相关源码摘要。

## 已知边界和人工确认事项

- 本阶段核验合同内的明确约定和典型不利条款。合同声明不能证明实际参保、登记、交付、股权权属、实缴、授权决议或身份资格真实有效，这些仍须结合外部材料核验。
- 未覆盖所有表达方式；OCR错误、无标题的混合交易、跨附件的复杂引用或很规避的措辞可能导致召回不足。泛称权利质押需核实具体权利类别，非应收账款权利的登记机关、期限和处分限制仍需逐类扩展。
- 劳动规则尚未完整计算本地最低工资、工龄分段、税务和社保基数，也未穷尽特殊工时、劳务派遣、未成年/外国劳动者等场景。试用期计算仅使用明确中文日期或期限，不猜测模糊日期。
- 股权专项以境内非上市企业的基础股权交易为首期范围。国资、外商投资、上市公司、金融监管、税费和并购申报，以及复杂反稀释/回购估值公式，需要另行核验和扩展。
- 未接入在线权属、登记或社保查询，也未对云端模型服务可用性作真实付费调用。测试使用确定性路径，并通过模型桩验证专项结论不会被模型改写。

## 法律来源

配置核对日期：2026-09-07。以下为本阶段核对的一手公开来源，条文按审查问题分配，不把关联法律概括为整份合同当然无效。

- [劳动合同法现行文本（人社部门公开）](https://www.huaihua.gov.cn/rsj/c116048/201507/37d5be05017e4b05ab2d78b6ba367872.shtml)
- [人社部试用期规则说明](https://app.www.gov.cn/govdata/gov/202203/01/482315/article.html)
- [最高人民法院劳动争议司法解释（二）](https://gongbao.court.gov.cn/Details/bb72019c45453f84d920bd6375573e.html)
- [最高人民法院公布的民法典全文](https://www.court.gov.cn/zixun/xiangqing/233181.html)
- [市场监管总局公布的公司法](https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/fgs/art/2023/art_067c072db6ef4679a2e0180996be4cf8.html)
