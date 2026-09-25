# 原失败路由簇：执行链核验

## 原始样本及预期依据

- 工业技术服务：原 `test_industrial_technical_service_routing_regression.CONTRACT` 全文，输入类型 `service`。正文约定数据建模、故障诊断、系统部署、预测模型和技术成果交付，支付技术服务报酬。并非因标题或测试名判技术合同。
- 专利许可：原 `test_patent_license_input_integrity_routing.FULL_PATENT_LICENSE` 全文，输入类型 `sale`。正文明确专利实施许可、不得转让专利权/再许可、按净销售额支付提成、专利资料交付及维持义务。销售是许可产品的经营行为，不是独立货物买卖对价。

## 首次偏离

1. 全文提取、规范化和条款切分无丢失。专利真实 HTTP 复测的 source/extracted/normalized/classifier/rule/search retention 均为 1.0。
2. `classify_technology_transaction` 已正确识别技术服务、专利实施许可。
3. `resolve_domain_selection` 已返回高置信 `DOCUMENT_OVERRIDE` / `TECHNOLOGY`。工业候选分数 TECHNOLOGY=28、SERVICE=13；专利 TECHNOLOGY=52、SALE=4。
4. **首次出错在 `fact_routing.resolve`**：忽略上述已接受结果，以“手动选择”为由无条件重新建立 `service/sale` DomainResolution。于是后续 dispatch/FactStore specialization/checklist/report 使用错误类型。
5. 旧类型链校验又要求 request/canonical/facts/checklist/report 全相同，无法表达合法重分类。

## 本次公共修复边界

保留已有 comparable-domain resolver 的决策，原始选择留作 prior，规范执行类型来自 accepted resolution。Gate 逐阶段与其字段契约比较：request 对照 selected；canonical/facts/checklist/report 对照 resolved。没有改分类阈值、抽取器、事实语义、evidence verifier 或发布条件。非可比较专项手动类型保留原有策略，不在本轮迁移。

### 全量首轮发现的第二个公共路由根因

full11 为 790 PASS / 289 FAIL，相对基线恢复 8 个历史失败，但新增 27 个失败。该中间版本不作为最终结果。

逐原文追踪 38 技术秘密许可、45 专利申请权转让、13 专利实施许可：专项模型均已识别高置信 TECHNOLOGY；`_classify_document_family` 也返回 TECHNOLOGY；随后 `primary_purpose` 因“买方/卖方、价款、交付”等通用词分别得到 SALE=20/20/16，覆盖已验证的许可/技术权利交易，最终加载买卖规则。首个偏离发生在 `resolve_domain_selection` 的 purpose 覆盖分支，不在 FactStore/规则字段。

修复该优先级：仅在已有高置信正文技术权利交易模型（dominant_family=TECHNOLOGY）时，禁止通用 SALE 词频候选覆盖；候选及被拒原因仍保留在 classification_context。无此正文模型时不保护技术标题；真实设备采购保护测试仍为 sale。未通过强制保留用户类型规避上游错误。

## 原簇断言结果（首轮）

- 专利模块原有 8 项全部通过，包含完整文件上传路由、后续 primary_transaction_model/许可要素/证据及输入完整性断言。
- 工业模块原有 8 项中 6 项通过。两个仍失败的测试是 `test_industrial_service_core_risks_survive_route_resolution` 和 `test_complete_review_rows_are_unique_and_partial_rows_have_real_gaps`。
- 两者继续要求 timeline conflict / TECH-SHARED-03；同模块的时间线测试却明确要求不能将有效期当履行截止日。当前原文有效期结束 2027-03-04，最终报告/验收另约定 2027-03-15/31，分析对象未发现独立履行结束日。未为了恢复计数制造时间线风险，也没有改动这两个旧断言。本轮没有测试迁移。

## 正常业务接口，不以单测代替发布验收

后端实际进程 18808，`routers.review_v2.review_v2_file`，run_mode=review，保留原始 prior，HTTP 200。

- 专利：sale → technology / TECHNOLOGY_LICENSE / PATENT_LICENSE；类型链 PASS；发布 **BLOCKED**，10 个原始拒绝对象（展开 11 个 tuple）。
- 工业：service → technology / TECHNICAL_SERVICE；类型链 PASS；发布 **BLOCKED**，41 个原始拒绝对象（展开 50 个 tuple）。
- 原委托开发保护样本：仍为 REPORT_READY，不用于替代原失败样本验收。

完整拒绝对象与 source/span 在 `round6_patent_blockers.json`、`round6_industrial_blockers.json`。既有 Gate 没有输出 fact_id/element_id 的字段保持 null，不能捏造标识。

## 路由恢复后暴露的下游断点（未在本轮零散修补）

专利阶段快照见 `round6_patent_stages/transitions.json`：

- TC-11-04：保密专项处理得到 PARTIAL；`_apply_final_technology_fact_projection` 又改成 MISSING，同时保留 confidentiality_obligation_reference=COVERED，因此触发 MISSING_WITH_POSITIVE_EVIDENCE / POSITIVE_FACT_MONOTONICITY。
- TC-10-04：`_apply_technology_transaction_evidence_consistency` 把 negative check 改为 PASS；精确原文核验随后降为 INSUFFICIENT_CONTEXT；最终 projection 又改回 PASS（后续用户展示再次变为待核验）。这是状态源反复覆盖，不能通过更宽松 Gate 放行。
- TC-11-01：confidential_information_scope 的 EV-1a76c4d9ae0a4b0f 未满足 DIRECT element/source-clause ownership。第七条正文存在，仍需处理 projection 的 exact binding，不能用整个主题证据替代。
- TC-03-04：patent_identity_in_contract 的部分缺口进入 final missing，却无该子缺口的独立 absence evidence。
- license_infringement_responsibility：现有原文是许可方承担侵权处理，风险却要求证明被许可方承担，Gate 拒绝 INFRINGING_IMPLEMENTATION_TRIGGER / LICENSEE_LOSS_ALLOCATION / LICENSOR_ASSISTANCE_ONLY。
- TC-13-01：通用 core_contract_arrangement 把资料交付义务当作资料附件覆盖；专门 evidence proposition gate 拒绝。

因此本轮可报告路由历史失败恢复，但**不能报告专利或工业样本发布闭环已完成**。

## 最终代码复测记录

- 第二个路由根因修复后，对首轮新增的 27 个失败逐 ID 检查，27/27 已在局部原测试中恢复。未删除、跳过或迁移任何原断言。
- 新增路由保护共 9 项：正文许可结构覆盖泛型输入 prior、合法重分类阶段契约、错误执行阶段继续 BLOCKED、技术许可/申请权转让中的买卖称谓、真实设备采购不被附随技术词覆盖。
- 最终后端进程 17808。`round6_final_patent_live` 仍为正确专利许可类型、Gate BLOCKED（10）；`round6_final_industrial_live` 仍为技术服务、Gate BLOCKED（41）；`round6_final_guard_live` 保持 REPORT_READY（0）。这与前一接口轮一致。
- 最终拒绝 tuple：`round6_final_patent_blockers.json`、`round6_final_industrial_blockers.json`。原有 Gate 没有发布的 fact_id 等字段在诊断中标空，不将自然语言或证据包 ID 伪造为 canonical fact ID。
- full11 只作为新增回归定位记录。最终全量以 full12 全部六份 JUnit 和相对 full10 的逐 ID 比较为准，不混用两轮计数。

## 最终全量结论

full12：820 PASS / 262 FAIL / 0 SKIP，共 1082 项。原基线用例为 811 PASS / 262 FAIL；新增 9 项全部 PASS。相对 803/270 的基线，历史失败实际恢复 8 项，原 PASS 新变 FAIL 为 0，删除/跳过原测试为 0，测试迁移为 0。

历史恢复测试 ID（完整命名空间及 before/after 见 `round6_comparison_final.json`）：

- test_industrial_technical_service_routing_regression::test_b2b_industrial_service_uses_technical_service_route_and_roles
- test_industrial_technical_service_routing_regression::test_explicit_service_follow_on_improvement_still_activates_tc10
- test_industrial_technical_service_routing_regression::test_improvement_recommendation_does_not_invent_existing_mechanisms
- test_industrial_technical_service_routing_regression::test_payment_and_timeline_are_bound_to_current_contract_facts
- test_industrial_technical_service_routing_regression::test_service_current_project_outputs_do_not_activate_follow_on_improvement_rules
- test_industrial_technical_service_routing_regression::test_third_party_component_fact_is_shared_by_claim_and_proof_reviews
- test_patent_license_input_integrity_routing::test_complete_patent_license_uses_one_full_text_and_never_loads_sale_rules
- test_technology_license_primary_transaction::test_gold_routes_raw_docx_to_technology_license_not_sale

指定两个簇中的恢复数为 7，另 1 项是同一公共路由原因影响的现有原始 DOCX 许可路由测试。没有把新增保护测试计入上述恢复数。
