# 借款合同98生产回归

修复前任务：CR-20260909-170713-E3C110
修复后任务：CR-20260909-171413-7DDDCE
quality gate：REPORT_READY
原DOCX SHA256：b0add44adf035d4025d62b511645cb2cc324eab094a3511a27c9cc7129c2b809

|规则|修复前|修复后|
|---|---|---|
|L-01-01 借款合同性质|通过|通过|
|L-01-02 金融借款与民间借贷区分|通过|通过|
|L-01-03 以买卖担保借款识别|不适用|不适用|
|L-01-04 自然人间借款成立时间|不适用|不适用|
|L-02-01 套取金融机构贷款转贷|不适用|不适用|
|L-02-02 职业放贷人风险|不适用|不适用|
|L-02-03 明知违法用途出借|待核验|待核验|
|L-02-04 企业间借款经营需要|不适用|不适用|
|L-03-01 借款本金金额|通过|通过|
|L-03-02 实际放款和到账凭证|缺失|缺失|
|L-03-03 砍头息禁止|待核验|通过|
|L-03-04 债权凭证载明债权人|不适用|不适用|
|L-04-01 借期内利率|通过|通过|
|L-04-02 民间借贷LPR四倍上限|不适用|不适用|
|L-04-03 金融借款利率合规|缺失|缺失|
|L-04-04 变相高息费用|待核验|通过|
|L-05-01 利息计算基数和期间|部分覆盖|部分覆盖|
|L-05-02 逾期利息|待核验|通过|
|L-05-03 复利限制|缺失|缺失|
|L-05-04 未约定利息处理|不适用|不适用|
|L-06-01 还款期限|通过|通过|
|L-06-02 还款方式和账户|通过|通过|
|L-06-03 还款冲抵顺序|通过|缺失|
|L-06-04 还款确认和收据|缺失|缺失|
|L-07-01 提前还款权|通过|通过|
|L-07-02 提前还款利息计算|待核验|通过|
|L-07-03 不合理提前还款违约金|待核验|通过|
|L-07-04 提前还款通知程序|部分覆盖|部分覆盖|
|L-08-01 展期申请和同意|不适用|不适用|
|L-08-02 展期利率和费用|不适用|不适用|
|L-08-03 展期需保证人同意|不适用|不适用|
|L-08-04 未获同意仍按原期限履行|不适用|不适用|
|L-09-01 保证方式|不适用|不适用|
|L-09-02 保证期间|不适用|不适用|
|L-09-03 保证范围|不适用|不适用|
|L-09-04 借新还旧保证人知情|不适用|不适用|
|L-10-01 夫妻共同意思表示|不适用|不适用|
|L-10-02 家庭日常生活需要|不适用|不适用|
|L-10-03 共同经营用途|不适用|不适用|
|L-10-04 超出家用的大额借款证据|不适用|不适用|
|L-11-01 诉讼时效起算|通过|通过|
|L-11-02 时效中断留痕|缺失|缺失|
|L-11-03 催收和送达方式|部分覆盖|部分覆盖|
|L-11-04 保证期间内行权留痕|不适用|不适用|
|L-12-01 借据收据欠条附件|不适用|不适用|
|L-12-02 转账和放款凭证|缺失|缺失|
|L-12-03 保证和担保附件|不适用|不适用|
|L-12-04 催收和还款记录附件|缺失|缺失|

## L-01-01 借款合同性质
正式合同条款或附件中已召回能够覆盖该审查点的实质约定，未发现明显空白项。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
- SRC-cb516c35bbbab9202415 | 十三、还款账户 | 十三、还款账户
户名：张明远
账号：6217000012345678
开户行：山西银行股份有限公司太原迎泽支行
借款人授权贷款人在每期还款日从上述账户自动扣收应偿还的本金、利息及其他应付款项。
- SRC-c7fb3318766b2a4f7401 | 全文 | 【测试说明：以下主体、证件号码、账号、联系方式均为虚构模拟数据，仅用于合同审查系统测试】
合同编号：SX-YXD-2026-0915-TEST01
贷款人：山西银行股份有限公司太原迎泽支行
借款人：张明远
- SRC-6287f0fb7921b3441082 | 六、利息计算 / 计息方式： | 计息方式：
当期利息＝贷款正常本金余额×执行年利率÷360×计息天数
结息方式：按月结息
结息日：每月15日
付息日：每月15日
最后一次结息日：2028年9月15日
- SRC-a8d1182d258ccaa38ca1 | 十四、提前还款 | 十四、提前还款
借款人可以申请提前偿还全部贷款。
提前还款应事先向贷款人提出申请并取得贷款人同意。
提前还款利息按照实际贷款占用天数计算。
不允许提前偿还部分贷款本金。
要素：[{"review_id": "L-01-01", "element_id": "core_contract_arrangement", "proposition": "合同存在可验证的“借款合同性质”实质条款内容。", "status": "COVERED", "evidence_ids": ["SRC-cb516c35bbbab9202415", "SRC-c7fb3318766b2a4f7401", "SRC-6287f0fb7921b3441082", "SRC-a8d1182d258ccaa38ca1"], "entailment": "SUPPORTS", "verifier_confidence": "high", "reason": "元素级证据可支撑。", "claim_id": "", "source_clause_ids": ["C0015"], "source_spans": ["十三、还款账户\n户名：张明远\n账号：6217000012345678\n开户行：山西银行股份有限公司太原迎泽支行\n借款人授权贷款人在每期还款日从上述账户自动扣收应偿还的本金、利息及其他应付款项。"], "source_locations": ["十三、还款账户"], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "FOUND", "fact_value": null, "fact_evidence_refs": ["C0015"], "requirement_status": "SATISFIED", "requirement_reason": "元素级证据可支撑。", "evidence_refs": ["SRC-cb516c35bbbab9202415", "SRC-c7fb3318766b2a4f7401", "SRC-6287f0fb7921b3441082", "SRC-a8d1182d258ccaa38ca1"], "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.", "supporting_evidence_ids": ["SRC-cb516c35bbbab9202415", "SRC-c7fb3318766b2a4f7401", "SRC-6287f0fb7921b3441082", "SRC-a8d1182d258ccaa38ca1"], "bound_evidence_ids": ["SRC-cb516c35bbbab9202415", "SRC-c7fb3318766b2a4f7401", "SRC-6287f0fb7921b3441082", "SRC-a8d1182d258ccaa38ca1"], "supporting_evidence": [{"clause_id": "C0015", "quote": "十三、还款账户\n户名：张明远\n账号：6217000012345678\n开户行：山西银行股份有限公司太原迎泽支行\n借款人授权贷款人在每期还款日从上述账户自动扣收应偿还的本金、利息及其他应付款项。"}]}]

## L-01-02 金融借款与民间借贷区分
共享事实及直接原文证据已覆盖：贷款人主体身份可用于区分金融借款与民间借贷。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
- SRC-c7fb3318766b2a4f7401 | 全文 | 【测试说明：以下主体、证件号码、账号、联系方式均为虚构模拟数据，仅用于合同审查系统测试】
合同编号：SX-YXD-2026-0915-TEST01
贷款人：山西银行股份有限公司太原迎泽支行
借款人：张明远
- SRC-a6fdac8ddd5a423dcc44 | 二十、合同签署 | 二十、合同签署
签署方式：线上电子签署
贷款人：山西银行股份有限公司太原迎泽支行
贷款人签署方式：电子签章
借款人：张明远
借款人签署方式：电子签名
签订日期：2026年9月15日
签订地点：山西省太原市
要素：[{"review_id": "L-01-02", "element_id": "loan_lender_identity", "proposition": "贷款人主体身份可用于区分金融借款与民间借贷", "status": "COVERED", "evidence_ids": ["SRC-c7fb3318766b2a4f7401", "SRC-a6fdac8ddd5a423dcc44"], "entailment": "SUPPORTS", "verifier_confidence": "high", "reason": "元素级证据可支撑。", "claim_id": "", "source_clause_ids": ["C0001"], "source_spans": ["【测试说明：以下主体、证件号码、账号、联系方式均为虚构模拟数据，仅用于合同审查系统测试】\n合同编号：SX-YXD-2026-0915-TEST01\n贷款人：山西银行股份有限公司太原迎泽支行\n借款人：张明远"], "source_locations": ["全文"], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "FOUND", "fact_value": null, "fact_evidence_refs": ["C0001-LOAN-1"], "requirement_status": "SATISFIED", "requirement_reason": "元素级证据可支撑。", "evidence_refs": ["SRC-c7fb3318766b2a4f7401", "SRC-a6fdac8ddd5a423dcc44"], "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.", "supporting_evidence_ids": ["SRC-c7fb3318766b2a4f7401", "SRC-a6fdac8ddd5a423dcc44"], "bound_evidence_ids": ["SRC-c7fb3318766b2a4f7401", "SRC-a6fdac8ddd5a423dcc44"], "supporting_evidence": [{"clause_id": "C0001", "quote": "【测试说明：以下主体、证件号码、账号、联系方式均为虚构模拟数据，仅用于合同审查系统测试】\n合同编号：SX-YXD-2026-0915-TEST01\n贷款人：山西银行股份有限公司太原迎泽支行\n借款人：张明远"}]}]

## L-01-03 以买卖担保借款识别
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["sale_security"], "trigger_facts": {"sale_security": false}, "source_evidence": {"sale_security": []}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_sale_security_distinction", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-01-04 自然人间借款成立时间
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["lender_kind", "borrower_kind"], "trigger_facts": {"lender_kind": "financial", "borrower_kind": "natural"}, "source_evidence": {"lender_kind": ["C0001", "C0023"], "borrower_kind": ["C0001"]}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_natural_person_formation", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-02-01 套取金融机构贷款转贷
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["lender_kind"], "trigger_facts": {"lender_kind": "financial"}, "source_evidence": {"lender_kind": ["C0001", "C0023"]}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_relending_bank_loan_invalid", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-02-02 职业放贷人风险
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["lender_kind"], "trigger_facts": {"lender_kind": "financial"}, "source_evidence": {"lender_kind": ["C0001", "C0023"]}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_professional_lender_invalid", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-02-03 明知违法用途出借
合同文本未发现异常，相关实际事实需结合资金来源、历史放贷行为、实际用途等核验；不能据此确认相关风险事实不存在。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
要素：[{"review_id": "L-02-03", "element_id": "core_contract_arrangement", "proposition": "合同存在可验证的“明知违法用途出借”实质条款内容。", "status": "MISSING", "evidence_ids": [], "entailment": "NOT_RELEVANT", "verifier_confidence": "medium", "reason": "未找到可支撑该元素的合同证据。", "claim_id": "", "source_clause_ids": [], "source_spans": [], "source_locations": [], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "MISSING", "fact_value": null, "fact_evidence_refs": [], "requirement_status": "NOT_SATISFIED", "requirement_reason": "未找到可支撑该元素的合同证据。", "evidence_refs": [], "evidence_selection_reason": "No direct supporting evidence was selected for this element."}]

## L-02-04 企业间借款经营需要
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["lender_kind", "borrower_kind"], "trigger_facts": {"lender_kind": "financial", "borrower_kind": "natural"}, "source_evidence": {"lender_kind": ["C0001", "C0023"], "borrower_kind": ["C0001"]}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_enterprise_business_need", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-03-01 借款本金金额
正式合同条款或附件中已召回能够覆盖该审查点的实质约定，未发现明显空白项。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
- SRC-7c51b91bbca474b4359a | 二、贷款种类与金额 | 二、贷款种类与金额
贷款种类：消费性贷款
贷款金额（大写）：人民币壹拾贰万元整
贷款金额（小写）：¥120,000.00
要素：[{"review_id": "L-03-01", "element_id": "core_contract_arrangement", "proposition": "合同存在可验证的“借款本金金额”实质条款内容。", "status": "COVERED", "evidence_ids": ["SRC-7c51b91bbca474b4359a"], "entailment": "SUPPORTS", "verifier_confidence": "high", "reason": "元素级证据可支撑。", "claim_id": "", "source_clause_ids": ["C0003"], "source_spans": ["二、贷款种类与金额\n贷款种类：消费性贷款\n贷款金额（大写）：人民币壹拾贰万元整\n贷款金额（小写）：¥120,000.00"], "source_locations": ["二、贷款种类与金额"], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "FOUND", "fact_value": null, "fact_evidence_refs": ["C0003"], "requirement_status": "SATISFIED", "requirement_reason": "元素级证据可支撑。", "evidence_refs": ["SRC-7c51b91bbca474b4359a"], "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.", "supporting_evidence_ids": ["SRC-7c51b91bbca474b4359a"], "bound_evidence_ids": ["SRC-7c51b91bbca474b4359a"], "supporting_evidence": [{"clause_id": "C0003", "quote": "二、贷款种类与金额\n贷款种类：消费性贷款\n贷款金额（大写）：人民币壹拾贰万元整\n贷款金额（小写）：¥120,000.00"}]}]

## L-03-02 实际放款和到账凭证
未找到直接覆盖以下要素的约定：实际放款或到账凭证及确认。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
要素：[{"review_id": "L-03-02", "element_id": "loan_disbursement_record", "proposition": "实际放款或到账凭证及确认", "status": "MISSING", "evidence_ids": [], "entailment": "NEGATIVE_SEARCH_NOT_FOUND", "verifier_confidence": "high", "reason": "未找到可支撑该元素的合同证据。", "claim_id": "", "source_clause_ids": [], "source_spans": [], "source_locations": [], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "MISSING", "fact_value": null, "fact_evidence_refs": [], "requirement_status": "NOT_SATISFIED", "requirement_reason": "未找到可支撑该元素的合同证据。", "evidence_refs": [], "evidence_selection_reason": "No direct supporting evidence was selected for this element."}]

## L-03-03 砍头息禁止
正式合同条款和附件中未召回该类明显风险表述。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
要素：[{"review_id": "L-03-03", "element_id": "core_contract_arrangement", "proposition": "合同存在可验证的“砍头息禁止”实质条款内容。", "status": "MISSING", "evidence_ids": [], "entailment": "NOT_RELEVANT", "verifier_confidence": "medium", "reason": "未找到可支撑该元素的合同证据。", "claim_id": "", "source_clause_ids": [], "source_spans": [], "source_locations": [], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "MISSING", "fact_value": null, "fact_evidence_refs": [], "requirement_status": "NOT_SATISFIED", "requirement_reason": "未找到可支撑该元素的合同证据。", "evidence_refs": [], "evidence_selection_reason": "No direct supporting evidence was selected for this element."}]

## L-03-04 债权凭证载明债权人
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["lender_kind", "voucher_mechanism"], "trigger_facts": {"lender_kind": "financial", "voucher_mechanism": false}, "source_evidence": {"lender_kind": ["C0001", "C0023"], "voucher_mechanism": []}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_voucher_creditor_identification", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-04-01 借期内利率
共享事实及直接原文证据已覆盖：明确的借期利率或无息安排。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
- SRC-997aeab795de0d977986 | 五、贷款利率 | 贷款年利率：4.20%
要素：[{"review_id": "L-04-01", "element_id": "loan_agreed_rate", "proposition": "明确的借期利率或无息安排", "status": "COVERED", "evidence_ids": ["SRC-997aeab795de0d977986"], "entailment": "SUPPORTS", "verifier_confidence": "high", "reason": "元素级证据可支撑。", "claim_id": "", "source_clause_ids": ["C0006"], "source_spans": ["贷款年利率：4.20%"], "source_locations": ["五、贷款利率"], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "FOUND", "fact_value": null, "fact_evidence_refs": ["C0006-LOAN-1"], "requirement_status": "SATISFIED", "requirement_reason": "元素级证据可支撑。", "evidence_refs": ["SRC-997aeab795de0d977986"], "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.", "supporting_evidence_ids": ["SRC-997aeab795de0d977986"], "bound_evidence_ids": ["SRC-997aeab795de0d977986"], "supporting_evidence": [{"clause_id": "C0006", "quote": "贷款年利率：4.20%"}]}]

## L-04-02 民间借贷LPR四倍上限
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["lender_kind"], "trigger_facts": {"lender_kind": "financial"}, "source_evidence": {"lender_kind": ["C0001", "C0023"]}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_interest_lpr_cap", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-04-03 金融借款利率合规
未找到直接覆盖以下要素的约定：金融贷款利率及费用符合监管要求。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": ["lender_kind"], "trigger_facts": {"lender_kind": "financial"}, "source_evidence": {"lender_kind": ["C0001", "C0023"]}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_financial_interest_compliance", "triggered": true, "condition_text": "已确认规则适用前提。"}
要素：[{"review_id": "L-04-03", "element_id": "loan_financial_rate_compliance", "proposition": "金融贷款利率及费用符合监管要求", "status": "MISSING", "evidence_ids": [], "entailment": "NEGATIVE_SEARCH_NOT_FOUND", "verifier_confidence": "high", "reason": "未找到可支撑该元素的合同证据。", "claim_id": "", "source_clause_ids": [], "source_spans": [], "source_locations": [], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "MISSING", "fact_value": null, "fact_evidence_refs": [], "requirement_status": "NOT_SATISFIED", "requirement_reason": "未找到可支撑该元素的合同证据。", "evidence_refs": [], "evidence_selection_reason": "No direct supporting evidence was selected for this element."}]

## L-04-04 变相高息费用
未发现实际收取服务费、管理费或咨询费等融资收费的安排；实现债权费用和一般违约金不作为该项证据。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
要素：[{"review_id": "L-04-04", "element_id": "core_contract_arrangement", "proposition": "合同存在可验证的“变相高息费用”实质条款内容。", "status": "MISSING", "evidence_ids": [], "entailment": "NOT_RELEVANT", "verifier_confidence": "medium", "reason": "未找到可支撑该元素的合同证据。", "claim_id": "", "source_clause_ids": [], "source_spans": [], "source_locations": [], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "MISSING", "fact_value": null, "fact_evidence_refs": [], "requirement_status": "NOT_SATISFIED", "requirement_reason": "未找到可支撑该元素的合同证据。", "evidence_refs": [], "evidence_selection_reason": "No direct supporting evidence was selected for this element."}]

## L-05-01 利息计算基数和期间
未找到直接覆盖以下要素的约定：利息起止期间。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
- SRC-645381eb36c3c0c7d033 | 六、利息计算 / 计息方式： | 当期利息＝贷款正常本金余额×执行年利率÷360×计息天数
要素：[{"review_id": "L-05-01", "element_id": "loan_interest_base", "proposition": "利息计算基数", "status": "COVERED", "evidence_ids": ["EV-383ec33f38b783ef"], "entailment": "SUPPORTS", "verifier_confidence": "high", "reason": "元素级证据可支撑。", "claim_id": "", "source_clause_ids": ["C0008"], "source_spans": ["当期利息＝贷款正常本金余额×执行年利率÷360×计息天数"], "source_locations": ["六、利息计算 / 计息方式："], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "FOUND", "fact_value": null, "fact_evidence_refs": ["C0008-LOAN-1"], "requirement_status": "SATISFIED", "requirement_reason": "元素级证据可支撑。", "evidence_refs": ["EV-383ec33f38b783ef"], "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.", "supporting_evidence": [{"clause_id": "C0008", "quote": "当期利息＝贷款正常本金余额×执行年利率÷360×计息天数"}], "supporting_evidence_ids": ["EV-383ec33f38b783ef"]}, {"review_id": "L-05-01", "element_id": "loan_interest_period", "proposition": "利息起止期间", "status": "MISSING", "evidence_ids": [], "entailment": "NOT_RELEVANT", "verifier_confidence": "medium", "reason": "未找到可支撑该元素的合同证据。", "claim_id": "", "source_clause_ids": [], "source_spans": [], "source_locations": [], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "MISSING", "fact_value": null, "fact_evidence_refs": [], "requirement_status": "NOT_SATISFIED", "requirement_reason": "未找到可支撑该元素的合同证据。", "evidence_refs": [], "evidence_selection_reason": "No direct supporting evidence was selected for this element."}]

## L-05-02 逾期利息
共享事实及直接原文证据已覆盖：逾期利率或可计算的加收标准。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
- SRC-40048ecdda342fd25d51 | 七、罚息 | 逾期贷款罚息：在合同执行利率基础上加收50%
- SRC-e7f7349496e25248e903 | 七、罚息 | 逾期罚息年利率：6.30%
要素：[{"review_id": "L-05-02", "element_id": "loan_overdue_rate", "proposition": "逾期利率或可计算的加收标准", "status": "COVERED", "evidence_ids": ["SRC-40048ecdda342fd25d51", "SRC-e7f7349496e25248e903"], "entailment": "SUPPORTS", "verifier_confidence": "high", "reason": "元素级证据可支撑。", "claim_id": "", "source_clause_ids": ["C0009"], "source_spans": ["逾期贷款罚息：在合同执行利率基础上加收50%"], "source_locations": ["七、罚息"], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "FOUND", "fact_value": null, "fact_evidence_refs": ["C0009-LOAN-1"], "requirement_status": "SATISFIED", "requirement_reason": "元素级证据可支撑。", "evidence_refs": ["SRC-40048ecdda342fd25d51", "SRC-e7f7349496e25248e903"], "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.", "supporting_evidence_ids": ["SRC-40048ecdda342fd25d51", "SRC-e7f7349496e25248e903"], "bound_evidence_ids": ["SRC-40048ecdda342fd25d51", "SRC-e7f7349496e25248e903"], "supporting_evidence": [{"clause_id": "C0009", "quote": "逾期贷款罚息：在合同执行利率基础上加收50%"}]}]

## L-05-03 复利限制
未找到直接覆盖以下要素的约定：复利计算对象及条件、复利标准或限制。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": ["compound"], "trigger_facts": {"compound": true}, "source_evidence": {"compound": ["C0019"]}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_compound_interest_limit", "triggered": true, "condition_text": "已确认规则适用前提。"}
要素：[{"review_id": "L-05-03", "element_id": "loan_compound_scope", "proposition": "复利计算对象及条件", "status": "MISSING", "evidence_ids": [], "entailment": "NEGATIVE_SEARCH_NOT_FOUND", "verifier_confidence": "high", "reason": "未找到可支撑该元素的合同证据。", "claim_id": "", "source_clause_ids": [], "source_spans": [], "source_locations": [], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "MISSING", "fact_value": null, "fact_evidence_refs": [], "requirement_status": "NOT_SATISFIED", "requirement_reason": "未找到可支撑该元素的合同证据。", "evidence_refs": [], "evidence_selection_reason": "No direct supporting evidence was selected for this element."}, {"review_id": "L-05-03", "element_id": "loan_compound_standard", "proposition": "复利标准或限制", "status": "MISSING", "evidence_ids": [], "entailment": "NEGATIVE_SEARCH_NOT_FOUND", "verifier_confidence": "high", "reason": "未找到可支撑该元素的合同证据。", "claim_id": "", "source_clause_ids": [], "source_spans": [], "source_locations": [], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "MISSING", "fact_value": null, "fact_evidence_refs": [], "requirement_status": "NOT_SATISFIED", "requirement_reason": "未找到可支撑该元素的合同证据。", "evidence_refs": [], "evidence_selection_reason": "No direct supporting evidence was selected for this element."}]

## L-05-04 未约定利息处理
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["agreed_rate"], "trigger_facts": {"agreed_rate": true}, "source_evidence": {"agreed_rate": [{"clause_id": "C0006", "text": "贷款年利率：4.20%", "quote": "贷款年利率：4.20%", "location": "五、贷款利率", "section_type": "正式合同条款", "block_type": "OPERATIVE_CLAUSE", "source_type": "CONTRACT_TEXT", "evidence_id": "C0006-LOAN-1", "entailment_status": "SUPPORTS", "semantic_score": 1.0, "supports_element_ids": ["loan_agreed_rate"]}]}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_interest_no_agreement_rule", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-06-01 还款期限
共享事实及直接原文证据已覆盖：借款到期日或可确定的还款期限。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
- SRC-989a622f63f89cf339bb | 四、贷款期限 | 贷款到期日：2028年9月15日
要素：[{"review_id": "L-06-01", "element_id": "loan_maturity", "proposition": "借款到期日或可确定的还款期限", "status": "COVERED", "evidence_ids": ["SRC-989a622f63f89cf339bb"], "entailment": "SUPPORTS", "verifier_confidence": "high", "reason": "元素级证据可支撑。", "claim_id": "", "source_clause_ids": ["C0005"], "source_spans": ["贷款到期日：2028年9月15日"], "source_locations": ["四、贷款期限"], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "FOUND", "fact_value": null, "fact_evidence_refs": ["C0005-LOAN-1"], "requirement_status": "SATISFIED", "requirement_reason": "元素级证据可支撑。", "evidence_refs": ["SRC-989a622f63f89cf339bb"], "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.", "supporting_evidence_ids": ["SRC-989a622f63f89cf339bb"], "bound_evidence_ids": ["SRC-989a622f63f89cf339bb"], "supporting_evidence": [{"clause_id": "C0005", "quote": "贷款到期日：2028年9月15日"}]}]

## L-06-02 还款方式和账户
共享事实及直接原文证据已覆盖：还款支付方式、还款收款账户或指定机制。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
- SRC-58c69f88570ac05a4116 | 十三、还款账户 | 十三、还款账户
- SRC-3035e97df1e0b9bc6407 | 十二、还款方式 | 还款方式：按月等额本息还款
- SRC-5964a7e884be1bb4980a | 十三、还款账户 | 借款人授权贷款人在每期还款日从上述账户自动扣收应偿还的本金、利息及其他应付款项。
要素：[{"review_id": "L-06-02", "element_id": "loan_repayment_method", "proposition": "还款支付方式", "status": "COVERED", "evidence_ids": ["SRC-3035e97df1e0b9bc6407", "SRC-5964a7e884be1bb4980a"], "entailment": "SUPPORTS", "verifier_confidence": "high", "reason": "元素级证据可支撑。", "claim_id": "", "source_clause_ids": ["C0014"], "source_spans": ["还款方式：按月等额本息还款"], "source_locations": ["十二、还款方式"], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "FOUND", "fact_value": null, "fact_evidence_refs": ["C0014-LOAN-1"], "requirement_status": "SATISFIED", "requirement_reason": "元素级证据可支撑。", "evidence_refs": ["SRC-3035e97df1e0b9bc6407", "SRC-5964a7e884be1bb4980a"], "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.", "supporting_evidence_ids": ["SRC-3035e97df1e0b9bc6407", "SRC-5964a7e884be1bb4980a"], "bound_evidence_ids": ["SRC-3035e97df1e0b9bc6407", "SRC-5964a7e884be1bb4980a"], "supporting_evidence": [{"clause_id": "C0014", "quote": "还款方式：按月等额本息还款"}]}, {"review_id": "L-06-02", "element_id": "loan_repayment_account", "proposition": "还款收款账户或指定机制", "status": "COVERED", "evidence_ids": ["SRC-58c69f88570ac05a4116", "SRC-5964a7e884be1bb4980a"], "entailment": "SUPPORTS", "verifier_confidence": "high", "reason": "元素级证据可支撑。", "claim_id": "", "source_clause_ids": ["C0015"], "source_spans": ["十三、还款账户"], "source_locations": ["十三、还款账户"], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "FOUND", "fact_value": null, "fact_evidence_refs": ["C0015-LOAN-2"], "requirement_status": "SATISFIED", "requirement_reason": "元素级证据可支撑。", "evidence_refs": ["SRC-58c69f88570ac05a4116", "SRC-5964a7e884be1bb4980a"], "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.", "supporting_evidence_ids": ["SRC-58c69f88570ac05a4116", "SRC-5964a7e884be1bb4980a"], "bound_evidence_ids": ["SRC-58c69f88570ac05a4116", "SRC-5964a7e884be1bb4980a"], "supporting_evidence": [{"clause_id": "C0015", "quote": "十三、还款账户"}]}]

## L-06-03 还款冲抵顺序
未找到直接覆盖以下要素的约定：部分还款的抵充顺序。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
要素：[{"review_id": "L-06-03", "element_id": "loan_offset_order", "proposition": "部分还款的抵充顺序", "status": "MISSING", "evidence_ids": [], "entailment": "NEGATIVE_SEARCH_NOT_FOUND", "verifier_confidence": "high", "reason": "未找到可支撑该元素的合同证据。", "claim_id": "", "source_clause_ids": [], "source_spans": [], "source_locations": [], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "MISSING", "fact_value": null, "fact_evidence_refs": [], "requirement_status": "NOT_SATISFIED", "requirement_reason": "未找到可支撑该元素的合同证据。", "evidence_refs": [], "evidence_selection_reason": "No direct supporting evidence was selected for this element."}]

## L-06-04 还款确认和收据
未找到直接覆盖以下要素的约定：还款到账确认或结清凭证。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
要素：[{"review_id": "L-06-04", "element_id": "loan_repayment_receipt", "proposition": "还款到账确认或结清凭证", "status": "MISSING", "evidence_ids": [], "entailment": "NEGATIVE_SEARCH_NOT_FOUND", "verifier_confidence": "high", "reason": "未找到可支撑该元素的合同证据。", "claim_id": "", "source_clause_ids": [], "source_spans": [], "source_locations": [], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "MISSING", "fact_value": null, "fact_evidence_refs": [], "requirement_status": "NOT_SATISFIED", "requirement_reason": "未找到可支撑该元素的合同证据。", "evidence_refs": [], "evidence_selection_reason": "No direct supporting evidence was selected for this element."}]

## L-07-01 提前还款权
正式合同条款或附件中已召回能够覆盖该审查点的实质约定，未发现明显空白项。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": ["early_repayment"], "trigger_facts": {"early_repayment": true}, "source_evidence": {"early_repayment": ["C0016", "C0016", "C0016", "C0016"]}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_early_repayment_right", "triggered": true, "condition_text": "已确认规则适用前提。"}
- SRC-a8d1182d258ccaa38ca1 | 十四、提前还款 | 十四、提前还款
借款人可以申请提前偿还全部贷款。
提前还款应事先向贷款人提出申请并取得贷款人同意。
提前还款利息按照实际贷款占用天数计算。
不允许提前偿还部分贷款本金。
要素：[{"review_id": "L-07-01", "element_id": "core_contract_arrangement", "proposition": "合同存在可验证的“提前还款权”实质条款内容。", "status": "COVERED", "evidence_ids": ["SRC-a8d1182d258ccaa38ca1"], "entailment": "SUPPORTS", "verifier_confidence": "high", "reason": "元素级证据可支撑。", "claim_id": "", "source_clause_ids": ["C0016"], "source_spans": ["十四、提前还款\n借款人可以申请提前偿还全部贷款。\n提前还款应事先向贷款人提出申请并取得贷款人同意。\n提前还款利息按照实际贷款占用天数计算。\n不允许提前偿还部分贷款本金。"], "source_locations": ["十四、提前还款"], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "FOUND", "fact_value": null, "fact_evidence_refs": ["C0016"], "requirement_status": "SATISFIED", "requirement_reason": "元素级证据可支撑。", "evidence_refs": ["SRC-a8d1182d258ccaa38ca1"], "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.", "supporting_evidence_ids": ["SRC-a8d1182d258ccaa38ca1"], "bound_evidence_ids": ["SRC-a8d1182d258ccaa38ca1"], "supporting_evidence": [{"clause_id": "C0016", "quote": "十四、提前还款\n借款人可以申请提前偿还全部贷款。\n提前还款应事先向贷款人提出申请并取得贷款人同意。\n提前还款利息按照实际贷款占用天数计算。\n不允许提前偿还部分贷款本金。"}]}]

## L-07-02 提前还款利息计算
共享事实及直接原文证据已覆盖：提前还款按实际占用期间计息。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": ["early_repayment"], "trigger_facts": {"early_repayment": true}, "source_evidence": {"early_repayment": ["C0016", "C0016", "C0016", "C0016"]}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_early_repayment_interest", "triggered": true, "condition_text": "已确认规则适用前提。"}
- SRC-c1d7a161119ea5462f76 | 十四、提前还款 | 提前还款利息按照实际贷款占用天数计算。
要素：[{"review_id": "L-07-02", "element_id": "loan_early_interest_period", "proposition": "提前还款按实际占用期间计息", "status": "COVERED", "evidence_ids": ["SRC-c1d7a161119ea5462f76"], "entailment": "SUPPORTS", "verifier_confidence": "high", "reason": "元素级证据可支撑。", "claim_id": "", "source_clause_ids": ["C0016"], "source_spans": ["提前还款利息按照实际贷款占用天数计算。"], "source_locations": ["十四、提前还款"], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "FOUND", "fact_value": null, "fact_evidence_refs": ["C0016-LOAN-1"], "requirement_status": "SATISFIED", "requirement_reason": "元素级证据可支撑。", "evidence_refs": ["SRC-c1d7a161119ea5462f76"], "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.", "supporting_evidence_ids": ["SRC-c1d7a161119ea5462f76"], "bound_evidence_ids": ["SRC-c1d7a161119ea5462f76"], "supporting_evidence": [{"clause_id": "C0016", "quote": "提前还款利息按照实际贷款占用天数计算。"}]}]

## L-07-03 不合理提前还款违约金
正式合同条款和附件中未召回该类明显风险表述。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": ["early_repayment"], "trigger_facts": {"early_repayment": true}, "source_evidence": {"early_repayment": ["C0016", "C0016", "C0016", "C0016"]}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_unreasonable_early_repayment_penalty", "triggered": true, "condition_text": "已确认规则适用前提。"}
要素：[{"review_id": "L-07-03", "element_id": "core_contract_arrangement", "proposition": "合同存在可验证的“不合理提前还款违约金”实质条款内容。", "status": "MISSING", "evidence_ids": [], "entailment": "NOT_RELEVANT", "verifier_confidence": "medium", "reason": "未找到可支撑该元素的合同证据。", "claim_id": "", "source_clause_ids": [], "source_spans": [], "source_locations": [], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "MISSING", "fact_value": null, "fact_evidence_refs": [], "requirement_status": "NOT_SATISFIED", "requirement_reason": "未找到可支撑该元素的合同证据。", "evidence_refs": [], "evidence_selection_reason": "No direct supporting evidence was selected for this element."}]

## L-07-04 提前还款通知程序
未找到直接覆盖以下要素的约定：提前还款通知渠道或明确提前期限。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": ["early_repayment"], "trigger_facts": {"early_repayment": true}, "source_evidence": {"early_repayment": ["C0016", "C0016", "C0016", "C0016"]}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_early_repayment_notice", "triggered": true, "condition_text": "已确认规则适用前提。"}
- SRC-d61f64315acca4e5d8db | 十四、提前还款 | 提前还款应事先向贷款人提出申请并取得贷款人同意。
要素：[{"review_id": "L-07-04", "element_id": "loan_early_application", "proposition": "提前还款申请及同意程序", "status": "COVERED", "evidence_ids": ["EV-b719b1ad016a9169"], "entailment": "SUPPORTS", "verifier_confidence": "high", "reason": "元素级证据可支撑。", "claim_id": "", "source_clause_ids": ["C0016"], "source_spans": ["提前还款应事先向贷款人提出申请并取得贷款人同意。"], "source_locations": ["十四、提前还款"], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "FOUND", "fact_value": null, "fact_evidence_refs": ["C0016-LOAN-1"], "requirement_status": "SATISFIED", "requirement_reason": "元素级证据可支撑。", "evidence_refs": ["EV-b719b1ad016a9169"], "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.", "supporting_evidence": [{"clause_id": "C0016", "quote": "提前还款应事先向贷款人提出申请并取得贷款人同意。"}], "supporting_evidence_ids": ["EV-b719b1ad016a9169"]}, {"review_id": "L-07-04", "element_id": "loan_early_channel", "proposition": "提前还款通知渠道或明确提前期限", "status": "MISSING", "evidence_ids": [], "entailment": "NOT_RELEVANT", "verifier_confidence": "medium", "reason": "未找到可支撑该元素的合同证据。", "claim_id": "", "source_clause_ids": [], "source_spans": [], "source_locations": [], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "MISSING", "fact_value": null, "fact_evidence_refs": [], "requirement_status": "NOT_SATISFIED", "requirement_reason": "未找到可支撑该元素的合同证据。", "evidence_refs": [], "evidence_selection_reason": "No direct supporting evidence was selected for this element."}]

## L-08-01 展期申请和同意
合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。", "user_reason": "合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。", "machine_reason": "合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。", "depends_on": ["extension", "extension_excluded"], "trigger_facts": {"extension": false, "extension_excluded": true}, "source_evidence": {"extension": ["C0017"], "extension_excluded": ["C0017"]}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_extension_request", "triggered": false, "condition_text": "合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。"}
要素：[]

## L-08-02 展期利率和费用
合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。", "user_reason": "合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。", "machine_reason": "合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。", "depends_on": ["extension", "extension_excluded"], "trigger_facts": {"extension": false, "extension_excluded": true}, "source_evidence": {"extension": ["C0017"], "extension_excluded": ["C0017"]}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_extension_interest_rate", "triggered": false, "condition_text": "合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。"}
要素：[]

## L-08-03 展期需保证人同意
合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。", "user_reason": "合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。", "machine_reason": "合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。", "depends_on": ["extension", "guarantee", "extension_excluded"], "trigger_facts": {"extension": false, "guarantee": false, "extension_excluded": true}, "source_evidence": {"extension": ["C0017"], "guarantee": [], "extension_excluded": ["C0017"]}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_extension_guarantor_consent", "triggered": false, "condition_text": "合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。"}
要素：[]

## L-08-04 未获同意仍按原期限履行
合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。", "user_reason": "合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。", "machine_reason": "合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。", "depends_on": ["extension", "extension_excluded"], "trigger_facts": {"extension": false, "extension_excluded": true}, "source_evidence": {"extension": ["C0017"], "extension_excluded": ["C0017"]}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_extension_original_due_no_consent", "triggered": false, "condition_text": "合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。"}
要素：[]

## L-09-01 保证方式
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["guarantee"], "trigger_facts": {"guarantee": false}, "source_evidence": {"guarantee": []}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_guarantee_type_joint_or_general", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-09-02 保证期间
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["guarantee"], "trigger_facts": {"guarantee": false}, "source_evidence": {"guarantee": []}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_guarantee_period", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-09-03 保证范围
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["guarantee"], "trigger_facts": {"guarantee": false}, "source_evidence": {"guarantee": []}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_guarantee_scope", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-09-04 借新还旧保证人知情
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["refinancing", "guarantee"], "trigger_facts": {"refinancing": false, "guarantee": false}, "source_evidence": {"refinancing": [], "guarantee": []}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_old_for_new_guarantor_notice", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-10-01 夫妻共同意思表示
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["spouse"], "trigger_facts": {"spouse": false}, "source_evidence": {"spouse": []}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_spousal_joint_intent", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-10-02 家庭日常生活需要
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["household"], "trigger_facts": {"household": false}, "source_evidence": {"household": []}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_daily_family_need", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-10-03 共同经营用途
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["joint_business"], "trigger_facts": {"joint_business": false}, "source_evidence": {"joint_business": []}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_joint_business_need", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-10-04 超出家用的大额借款证据
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["spouse", "household", "joint_business"], "trigger_facts": {"spouse": false, "household": false, "joint_business": false}, "source_evidence": {"spouse": [], "household": [], "joint_business": []}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_beyond_family_need_evidence", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-11-01 诉讼时效起算
共享事实及直接原文证据已覆盖：借款到期日或可确定的还款期限。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
- SRC-989a622f63f89cf339bb | 四、贷款期限 | 贷款到期日：2028年9月15日
要素：[{"review_id": "L-11-01", "element_id": "loan_maturity", "proposition": "借款到期日或可确定的还款期限", "status": "COVERED", "evidence_ids": ["SRC-989a622f63f89cf339bb"], "entailment": "SUPPORTS", "verifier_confidence": "high", "reason": "元素级证据可支撑。", "claim_id": "", "source_clause_ids": ["C0005"], "source_spans": ["贷款到期日：2028年9月15日"], "source_locations": ["四、贷款期限"], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "FOUND", "fact_value": null, "fact_evidence_refs": ["C0005-LOAN-1"], "requirement_status": "SATISFIED", "requirement_reason": "元素级证据可支撑。", "evidence_refs": ["SRC-989a622f63f89cf339bb"], "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.", "supporting_evidence_ids": ["SRC-989a622f63f89cf339bb"], "bound_evidence_ids": ["SRC-989a622f63f89cf339bb"], "supporting_evidence": [{"clause_id": "C0005", "quote": "贷款到期日：2028年9月15日"}]}]

## L-11-02 时效中断留痕
未找到直接覆盖以下要素的约定：催收或债务确认的留痕安排。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
要素：[{"review_id": "L-11-02", "element_id": "loan_interruption_record", "proposition": "催收或债务确认的留痕安排", "status": "MISSING", "evidence_ids": [], "entailment": "NEGATIVE_SEARCH_NOT_FOUND", "verifier_confidence": "high", "reason": "未找到可支撑该元素的合同证据。", "claim_id": "", "source_clause_ids": [], "source_spans": [], "source_locations": [], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "MISSING", "fact_value": null, "fact_evidence_refs": [], "requirement_status": "NOT_SATISFIED", "requirement_reason": "未找到可支撑该元素的合同证据。", "evidence_refs": [], "evidence_selection_reason": "No direct supporting evidence was selected for this element."}]

## L-11-03 催收和送达方式
未找到直接覆盖以下要素的约定：催收通知方式或渠道。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
- SRC-b3b392691c71f987d5a1 | 一、借款人基本信息 | 送达地址：山西省太原市迎泽区测试路88号测试小区3号楼2单元801室
- SRC-341d593155b8cea31051 | 十七、借款人承诺 | 借款人的联系方式、住所、工作单位、收入状况或其他可能影响偿债能力的信息发生重大变化时，应及时通知贷款人。
要素：[{"review_id": "L-11-03", "element_id": "loan_service_address", "proposition": "指定送达地址", "status": "COVERED", "evidence_ids": ["EV-dedf3dbabde93ed3"], "entailment": "SUPPORTS", "verifier_confidence": "high", "reason": "元素级证据可支撑。", "claim_id": "", "source_clause_ids": ["C0002"], "source_spans": ["送达地址：山西省太原市迎泽区测试路88号测试小区3号楼2单元801室"], "source_locations": ["一、借款人基本信息"], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "FOUND", "fact_value": null, "fact_evidence_refs": ["C0002-LOAN-1"], "requirement_status": "SATISFIED", "requirement_reason": "元素级证据可支撑。", "evidence_refs": ["EV-dedf3dbabde93ed3"], "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.", "supporting_evidence": [{"clause_id": "C0002", "quote": "送达地址：山西省太原市迎泽区测试路88号测试小区3号楼2单元801室"}], "supporting_evidence_ids": ["EV-dedf3dbabde93ed3"]}, {"review_id": "L-11-03", "element_id": "loan_address_change_notice", "proposition": "地址变更通知", "status": "COVERED", "evidence_ids": ["EV-76fa009a86120eb3"], "entailment": "SUPPORTS", "verifier_confidence": "high", "reason": "元素级证据可支撑。", "claim_id": "", "source_clause_ids": ["C0020"], "source_spans": ["借款人的联系方式、住所、工作单位、收入状况或其他可能影响偿债能力的信息发生重大变化时，应及时通知贷款人。"], "source_locations": ["十七、借款人承诺"], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "FOUND", "fact_value": null, "fact_evidence_refs": ["C0020-LOAN-2"], "requirement_status": "SATISFIED", "requirement_reason": "元素级证据可支撑。", "evidence_refs": ["EV-76fa009a86120eb3"], "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.", "supporting_evidence": [{"clause_id": "C0020", "quote": "借款人的联系方式、住所、工作单位、收入状况或其他可能影响偿债能力的信息发生重大变化时，应及时通知贷款人。"}], "supporting_evidence_ids": ["EV-76fa009a86120eb3"]}, {"review_id": "L-11-03", "element_id": "loan_collection_channel", "proposition": "催收通知方式或渠道", "status": "MISSING", "evidence_ids": [], "entailment": "NOT_RELEVANT", "verifier_confidence": "medium", "reason": "未找到可支撑该元素的合同证据。", "claim_id": "", "source_clause_ids": [], "source_spans": [], "source_locations": [], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "MISSING", "fact_value": null, "fact_evidence_refs": [], "requirement_status": "NOT_SATISFIED", "requirement_reason": "未找到可支撑该元素的合同证据。", "evidence_refs": [], "evidence_selection_reason": "No direct supporting evidence was selected for this element."}]

## L-11-04 保证期间内行权留痕
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["guarantee"], "trigger_facts": {"guarantee": false}, "source_evidence": {"guarantee": []}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_guarantor_collection_within_period", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-12-01 借据收据欠条附件
金融借款不强制采用民间借贷纸质借据；放款记录与电子凭证由实际放款证据规则核验。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "金融借款不强制采用民间借贷纸质借据；放款记录与电子凭证由实际放款证据规则核验。", "user_reason": "金融借款不强制采用民间借贷纸质借据；放款记录与电子凭证由实际放款证据规则核验。", "machine_reason": "金融借款不强制采用民间借贷纸质借据；放款记录与电子凭证由实际放款证据规则核验。", "depends_on": ["lender_kind"], "trigger_facts": {"lender_kind": "financial"}, "source_evidence": {"lender_kind": ["C0001", "C0023"]}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_note_receipt_attachment", "triggered": false, "condition_text": "金融借款不强制采用民间借贷纸质借据；放款记录与电子凭证由实际放款证据规则核验。"}
要素：[]

## L-12-02 转账和放款凭证
未找到直接覆盖以下要素的约定：实际放款或到账凭证及确认。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
要素：[{"review_id": "L-12-02", "element_id": "loan_disbursement_record", "proposition": "实际放款或到账凭证及确认", "status": "MISSING", "evidence_ids": [], "entailment": "NEGATIVE_SEARCH_NOT_FOUND", "verifier_confidence": "high", "reason": "未找到可支撑该元素的合同证据。", "claim_id": "", "source_clause_ids": [], "source_spans": [], "source_locations": [], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "MISSING", "fact_value": null, "fact_evidence_refs": [], "requirement_status": "NOT_SATISFIED", "requirement_reason": "未找到可支撑该元素的合同证据。", "evidence_refs": [], "evidence_selection_reason": "No direct supporting evidence was selected for this element."}]

## L-12-03 保证和担保附件
合同未触发该专项规则的适用场景，不要求补写该场景条款。
适用性：{"status": "NOT_APPLICABLE", "applicable": false, "reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "user_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "machine_reason": "合同未触发该专项规则的适用场景，不要求补写该场景条款。", "depends_on": ["security"], "trigger_facts": {"security": false}, "source_evidence": {"security": []}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "SCENARIO:loan_guarantee_attachment", "triggered": false, "condition_text": "合同未触发该专项规则的适用场景，不要求补写该场景条款。"}
要素：[]

## L-12-04 催收和还款记录附件
未找到直接覆盖以下要素的约定：催收或还款记录的保存安排。
适用性：{"status": "APPLICABLE", "applicable": true, "reason": "已确认规则适用前提。", "user_reason": "已确认规则适用前提。", "machine_reason": "已确认规则适用前提。", "depends_on": [], "trigger_facts": {}, "source_evidence": {}, "searched_clause_ids": ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010", "C0011", "C0012", "C0013", "C0014", "C0015", "C0016", "C0017", "C0018", "C0019", "C0020", "C0021", "C0022", "C0023"], "confidence": "high", "condition": "ALWAYS_APPLICABLE", "triggered": true}
要素：[{"review_id": "L-12-04", "element_id": "loan_collection_records", "proposition": "催收或还款记录的保存安排", "status": "MISSING", "evidence_ids": [], "entailment": "NEGATIVE_SEARCH_NOT_FOUND", "verifier_confidence": "high", "reason": "未找到可支撑该元素的合同证据。", "claim_id": "", "source_clause_ids": [], "source_spans": [], "source_locations": [], "atomic": true, "child_elements": [], "legal_proposition_ids": [], "required_fact_key": "", "fact_status": "MISSING", "fact_value": null, "fact_evidence_refs": [], "requirement_status": "NOT_SATISFIED", "requirement_reason": "未找到可支撑该元素的合同证据。", "evidence_refs": [], "evidence_selection_reason": "No direct supporting evidence was selected for this element."}]