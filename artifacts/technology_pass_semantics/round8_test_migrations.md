# Round8 独立测试迁移说明（不是业务缺陷恢复）

1. `test_negative_rule_requires_reproduced_complete_adverse_search`：原构造只有 `search_coverage/adverse_clause_exists/searched_scope`，没有检索命题。Round7 的生产契约增加 `predicate/result/query_semantics/producer`，原测试未调用检索生产者。改用真实 `prepare_negative_audits`；仍分别验证完整负检索通过、不完整检索阻断、存在实际侵权阻断。三种原文及预期状态不变。原26项中仅完整负检索那个参数项属于此迁移，另外两个参数为双向保护。
2. `test_tc_12_04_requires_same_loss_general_remedy_before_activation` 和 `test_d_party_interest_check_distinguishes_uncapped_and_low_capped_licensor_liability`：原断言强制连续文字“同一侵权损失”。现有句子“侵权专项责任与同一损失一般救济并存”表达同一前置条件。保留原 fixture、N/A、空 evidence、不得形成风险以及后续低上限案例断言；改查“同一/损失/侵权/一般救济”四个命题组成，而不要求修饰语顺序。未调整业务规则或状态。

迁移涉及三个测试函数、五个测试ID；其中三个属于本轮26项，两个是原有通过的负检索保护项。不得将这三个新增失败的迁移计入实现缺陷恢复。

3. `test_service_fee_and_confidentiality_use_only_direct_operational_clauses`：在修复生产者适配和“对明确资料承担保密义务”的范围事实后，真实第八条（C0009）的双方保密义务与期间分别以三个精确 source span 展示；不是恢复三个主题引文。旧列表断言只允许一个 C0009，改为唯一来源集合 C0009，同时增加 PASS、每条来源必须有 supporting_element_ids、正文包含保密事实的断言。服务费证据的两项原断言保持不动。这个测试有实现缺陷修复，也有来源展示契约迁移，必须单列，不算纯业务恢复。

累计迁移：四个测试函数、六个测试ID；原26项中四项涉及迁移（其中一项同时有实现修复），另两项为原通过保护参数。
