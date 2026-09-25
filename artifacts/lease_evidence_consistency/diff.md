# 房屋租赁证据—状态一致性修复复测

根因：旧 PASS 未受最终要素真值约束；缺失检索另用字面词，未共享正向关系谓词；维修事实使用同主题词共现，误召回转租违约；侵权后果模板未区分合同类型。

修复：统一正向事实召回与搜索审计，按必要要素聚合状态；维修费用拆分必要、合理、实际发生、凭证义务；事实图谱使用相同因果谓词；租赁后果模板按合同域选择。未按 HL 编号或本合同专属文本特判。

修改文件：backend/review_v2/engine.py、lease_semantics.py、lease_contract_facts.py；backend/tests/test_lease_evidence_alignment.py、test_review_v2_house_lease.py；scripts/run_lease_evidence_acceptance.py。

新增回归覆盖：无正向证据不允许 PASS、无关同主题证据不支持任何要素、supports 与目标要素对齐、搜索审计与正向谓词一致、维修成本原子要素、改编号后仍选择租赁模板、事实图谱来源、明细摘要统计一致。

修复前统计：{"通过": 31, "缺失": 9, "不适用": 4, "部分覆盖": 6}
修复后统计：{"通过": 31, "缺失": 9, "不适用": 4, "部分覆盖": 6}
修复后风险与建议：{"major_risk": 0, "medium_risk": 3, "low_risk": 9, "priority_action": 0, "recommended_action": 5, "optional_action": 7, "manual_review": 0}

|规则|修复前|修复后|已验证要素及直接引文位置|
|---|---|---|---|
|HL-001 争议管辖条款|通过|通过|dispute_forum：第十九条第1项|
|HL-002 出租人与承租人身份信息|通过|通过|core_contract_arrangement：甲方（出租人）：深圳市恒瑞置业有限公司|
|HL-003 出租权来源证明|通过|通过|ownership_document：第一条（二）|
|HL-004 代理签署和授权附件|通过|通过|core_contract_arrangement：甲方（出租人）：深圳市恒瑞置业有限公司|
|HL-005 通知送达与催告留痕|通过|通过|notice_channel：甲方（出租人）：深圳市恒瑞置业有限公司|
|HL-006 第三方侵权分流|缺失|缺失|无已验证正向要素/不适用|
|HL-007 承租人死亡后的继续承租|不适用|不适用|无已验证正向要素/不适用|
|HL-008 无人继续承租时的交接|不适用|不适用|无已验证正向要素/不适用|
|HL-009 情势变更协商机制|缺失|缺失|无已验证正向要素/不适用|
|HL-010 房屋合法性保证|通过|通过|lawful_lease_basis：第一条（六）|
|HL-011 转租规则和责任链条|通过|通过|sublease_consent：第三条（二）|
|HL-012 出租人死亡或权利继受|不适用|不适用|无已验证正向要素/不适用|
|HL-013 期满续住转不定期租赁|缺失|缺失|无已验证正向要素/不适用|
|HL-014 不可抗力处理|部分覆盖|部分覆盖|force_event：第十六条第4项；force_notice：第十七条（二）|
|HL-015 欠租重大违约标准|通过|通过|arrears_remedy：第五条（五）|
|HL-016 擅自转租后果|通过|通过|core_contract_arrangement：第三条（四）|
|HL-017 约定解除事由|通过|通过|termination_trigger：第五条（五）|
|HL-018 解除权行使期限|通过|通过|termination_exercise_period：第三条（四）|
|HL-019 解除通知送达|通过|通过|termination_trigger：第五条（五）；termination_notice_delivery：第十二条 保密要求；termination_effective_time：第十八条（三）|
|HL-020 房屋出售后的租赁承继|缺失|缺失|无已验证正向要素/不适用|
|HL-021 出售通知与优先购买权|通过|通过|core_contract_arrangement：第十一条 优先购买权|
|HL-022 交付前瑕疵披露|缺失|缺失|无已验证正向要素/不适用|
|HL-023 第三方原因影响使用|缺失|缺失|无已验证正向要素/不适用|
|HL-024 征收拆迁处理|通过|通过|expropriation_event：第十六条第3项|
|HL-025 重大安全隐患处理|部分覆盖|部分覆盖|safety_trigger：第十六条（4）|
|HL-026 维修责任分工|通过|通过|landlord_repair：第九条第1项|
|HL-027 合同效力基础|通过|通过|severability：第二十条（三）|
|HL-028 押金金额和性质|通过|通过|deposit_obligation：第六条（一）；deposit_sum：第六条（一）|
|HL-029 提前退租约定|通过|通过|early_exit：第十五条（一）|
|HL-030 无提前退租条款时的协商机制|不适用|不适用|无已验证正向要素/不适用|
|HL-031 租期届满结算|通过|通过|expiry_settlement：第六条（三）；expiry_handover：第一条（四）|
|HL-032 无损坏时押金返还|通过|通过|deposit_return：第六条（三）；undamaged_return：第六条（三）|
|HL-033 损坏范围定义|通过|通过|wear_exclusion：第八条（二）；fault_damage：第十条（四）|
|HL-034 自然损耗排除|通过|通过|wear_exclusion：第八条（二）|
|HL-035 损坏举证责任|缺失|缺失|无已验证正向要素/不适用|
|HL-036 承租人过错损坏|通过|通过|fault_damage：第十条（四）|
|HL-037 维修费用合理性|部分覆盖|部分覆盖|repair_reasonable：第十条（二）|
|HL-038 任何损坏均由租客赔偿|通过|通过|无已验证正向要素/不适用|
|HL-039 扣款和违约金调减|部分覆盖|部分覆盖|loss_basis：第十五条（六）|
|HL-040 入住时瑕疵告知|缺失|缺失|无已验证正向要素/不适用|
|HL-041 出租人知情未异议|缺失|缺失|无已验证正向要素/不适用|
|HL-042 押金抵扣顺序|部分覆盖|部分覆盖|offset_items：第六条（三）|
|HL-043 押金返还期限|部分覆盖|部分覆盖|deposit_return：第六条（三）|
|HL-044 交接证据清单|通过|通过|signed_handover：第八条（三）|
|HL-045 水电物业等费用结清|通过|通过|core_contract_arrangement：第四条（一）|
|HL-046 装修添附处理|通过|通过|core_contract_arrangement：第九条第1项|
|HL-047 钥匙门禁和占有返还|通过|通过|possession_return：第八条（三）|
|HL-048 用途和禁止行为|通过|通过|core_contract_arrangement：第二条 租赁用途|
|HL-049 租金支付规则|通过|通过|rent_payment_arrangement：第五条（三）|
|HL-050 附件完整性|通过|通过|annex_reference：第一条（四）|

回归通过 205；失败 0。release_quality_gate=PASSED。