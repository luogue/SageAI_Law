# 房屋租赁期限与建议子项复测

**release_quality_gate=BLOCKED，发布保持阻断。**

根因：期限匹配漏掉“期限→将押金→返还”的语序；优先购买权依赖模型召回；建议聚合跳过通用复合要素，并按要素名去重，丢失不同规则的来源。未发现本轮问题由缓存命中造成。

修改文件：backend/review_v2/lease_semantics.py、engine.py、recommendation_children.py；backend/tests/test_lease_deadline_and_children.py；scripts/run_lease_children_acceptance.py；本地 backend/.env 的租赁发布阻断配置。

期限、优先购买权、入住瑕疵通知、异议和损坏举证均以全文语义要素核验；共享建议保留全部规则来源，聚合后增加明细—主题—正式建议—顶部子项集合检查。

原报告统计：{"通过": 31, "缺失": 9, "不适用": 4, "部分覆盖": 6}
新报告统计：{"通过": 32, "缺失": 9, "不适用": 4, "部分覆盖": 5}
自动化回归通过 214，失败 0。两次实际上传核心证据及状态一致：True；全部规则状态一致：True。

|规则|原报告|新报告|正向证据与检索|
|---|---|---|---|
|HL-001 争议管辖条款|通过|通过|第十九条第1项 dispute_forum=FOUND|
|HL-002 出租人与承租人身份信息|通过|通过|甲方（出租人）：深圳市恒瑞置业有限公司；乙方（承租人）：深圳市启明智能科技有限公司 |
|HL-003 出租权来源证明|通过|通过|第一条（二） ownership_document=FOUND|
|HL-004 代理签署和授权附件|通过|通过|甲方（出租人）：深圳市恒瑞置业有限公司；乙方（承租人）：深圳市启明智能科技有限公司；乙方（盖章）：深圳市启明智能科技有限公司；甲方（盖章）：深圳市恒瑞置业有限公司 |
|HL-005 通知送达与催告留痕|通过|通过|甲方（出租人）：深圳市恒瑞置业有限公司；乙方（承租人）：深圳市启明智能科技有限公司 change_duty=NOT_FOUND；deemed_service=NOT_FOUND|
|HL-006 第三方侵权分流|缺失|缺失| core_contract_arrangement=NOT_FOUND|
|HL-007 承租人死亡后的继续承租|不适用|不适用| |
|HL-008 无人继续承租时的交接|不适用|不适用| |
|HL-009 情势变更协商机制|缺失|缺失| core_contract_arrangement=NOT_FOUND|
|HL-010 房屋合法性保证|通过|通过|第一条（六）；第十三条（三） lawful_lease_basis=FOUND|
|HL-011 转租规则和责任链条|通过|通过|第三条（二）；第三条（三）；第三条（四）；第十六条（5） sublease_consent=FOUND|
|HL-012 出租人死亡或权利继受|不适用|不适用| |
|HL-013 期满续住转不定期租赁|缺失|缺失| post_expiry_continue_use=NOT_FOUND；no_objection_or_rent_acceptance=NOT_FOUND；reasonable_notice=NOT_FOUND|
|HL-014 不可抗力处理|部分覆盖|部分覆盖|第十七条（二）；第十六条第4项；第十七条（一）；第十七条（三） force_event=FOUND；force_notice=FOUND；force_settlement=NOT_FOUND|
|HL-015 欠租重大违约标准|通过|通过|第五条（五）；第七条（五）；第七条（四） arrears_remedy=FOUND|
|HL-016 擅自转租后果|通过|通过|第三条（四）；第十六条（5） |
|HL-017 约定解除事由|通过|通过|第五条（五）；第七条（五）；第七条（四）；第十条（四） termination_trigger=FOUND|
|HL-018 解除权行使期限|通过|通过|第三条（四） termination_exercise_period=FOUND|
|HL-019 解除通知送达|通过|通过|第五条（五）；第十二条 保密要求；第十八条（三）；第七条（五）；第七条（四）；第十五条（一）；第十条（四） termination_trigger=FOUND；termination_notice_delivery=FOUND；termination_effective_time=FOUND|
|HL-020 房屋出售后的租赁承继|缺失|缺失| core_contract_arrangement=NOT_FOUND|
|HL-021 出售通知与优先购买权|通过|通过|第十一条 优先购买权 sale_notice=FOUND；preemption_right=FOUND|
|HL-022 交付前瑕疵披露|缺失|缺失| core_contract_arrangement=NOT_FOUND|
|HL-023 第三方原因影响使用|缺失|缺失| core_contract_arrangement=NOT_FOUND|
|HL-024 征收拆迁处理|通过|通过|第十六条第3项 expropriation_event=FOUND|
|HL-025 重大安全隐患处理|部分覆盖|部分覆盖|第十六条（4） safety_trigger=FOUND；safety_notice=NOT_FOUND；safety_settlement=NOT_FOUND|
|HL-026 维修责任分工|通过|通过|第九条第1项；第十条（一）；第十条（三）；第十条（二） landlord_repair=FOUND|
|HL-027 合同效力基础|通过|通过|第二十条（三） severability=FOUND|
|HL-028 押金金额和性质|通过|通过|第六条（一）；第七条（五）；第六条（二）；第十三条（六） deposit_obligation=FOUND；deposit_sum=FOUND|
|HL-029 提前退租约定|通过|通过|第十五条（一） early_exit=FOUND|
|HL-030 无提前退租条款时的协商机制|不适用|不适用| |
|HL-031 租期届满结算|通过|通过|第一条（四）；第六条（三）；第四条（二） expiry_settlement=FOUND；expiry_handover=FOUND|
|HL-032 无损坏时押金返还|通过|通过|第六条（三）；第十五条（二） deposit_return=FOUND；undamaged_return=FOUND|
|HL-033 损坏范围定义|通过|通过|第八条（二）；第十条（四）；八、第3项 wear_exclusion=FOUND；fault_damage=FOUND|
|HL-034 自然损耗排除|通过|通过|第八条（二）；八、第3项 wear_exclusion=FOUND|
|HL-035 损坏举证责任|缺失|缺失| damage_proof_burden=NOT_FOUND|
|HL-036 承租人过错损坏|通过|通过|第十条（四） fault_damage=FOUND|
|HL-037 维修费用合理性|部分覆盖|部分覆盖|第十条（二）；第十条（三） repair_necessary=NOT_FOUND；repair_reasonable=FOUND；repair_actual=NOT_FOUND；repair_voucher=NOT_FOUND|
|HL-038 任何损坏均由租客赔偿|通过|通过| core_contract_arrangement=NOT_FOUND|
|HL-039 扣款和违约金调减|部分覆盖|部分覆盖|第十五条（六） loss_basis=FOUND；adjustment=NOT_FOUND|
|HL-040 入住时瑕疵告知|缺失|缺失| initial_defect_notice=NOT_FOUND|
|HL-041 出租人知情未异议|缺失|缺失| initial_defect_objection=NOT_FOUND|
|HL-042 押金抵扣顺序|部分覆盖|部分覆盖|第六条（三）；第七条（五） offset_items=FOUND；offset_order=NOT_FOUND|
|HL-043 押金返还期限|部分覆盖|通过|第六条（三）；第十五条（二） deposit_return=FOUND；return_deadline=FOUND|
|HL-044 交接证据清单|通过|通过|第八条（三） signed_handover=FOUND|
|HL-045 水电物业等费用结清|通过|通过|第七条（二） |
|HL-046 装修添附处理|通过|通过|第九条第1项 |
|HL-047 钥匙门禁和占有返还|通过|通过|第八条（三） |
|HL-048 用途和禁止行为|通过|通过|第二条 租赁用途；第九条（一） agreed_use_obligation=FOUND|
|HL-049 租金支付规则|通过|通过|第五条（三）；第十五条（四） rent_payment_arrangement=FOUND|
|HL-050 附件完整性|通过|通过|第一条（四） annex_reference=FOUND|

建议子项集合：{"status": "REPORT_READY", "failures": [], "rows": [{"risk_id": "RF-PROPERTY-DAMAGE-001", "actionable_child_ids": ["HL-035", "HL-037", "HL-040", "HL-041"], "theme_child_ids": ["HL-035", "HL-037", "HL-040", "HL-041"], "formal_child_ids": ["HL-035", "HL-037", "HL-040", "HL-041"], "missing_top_fragments": []}]}