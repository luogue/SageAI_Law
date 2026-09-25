# 保管合同收尾验证

## 生产结果

同一文件82 保管合同.docx，4950字；未修改测试合同。页面保留大模型复核开启，通过真实 /review-v2/file 重跑。PID17520，CR-20260909-071058-DADAC8，runtime=CURRENT，HTTP200。release_quality_gate=REPORT_READY，failures为空。原始响应及全部来源指纹保存在同目录 result-17520-6d39b7d6773d4a83997d15e96b30beb5.json。

49项：38 PASS、2 PARTIAL、3 MISSING、6 N/A。重大0、中等2、低3；建议处理2、可选优化3、人工复核0。

## 根因与实现

1. 条件要素模型已经存在，但转交第三人后的责任没有声明前提。新增声明式 applicability_condition，通用 resolve_declared_conditions 按允许、明确禁止及未知前提处理；明确禁止时从活动要素集合移除，同时保留 NOT_APPLICABLE 及来源。未知前提保留核验状态，不能擅自认定禁止。原有 coverage 主流程消费过滤后的活动要素，不做规则ID分支。
2. 留置权缺少已核验默认法条元数据，原始缺失后果把合同沉默当作权利不明。DefaultRule 增加 legal_default_rule，当前绑定 SUPPLETIVE_CLEAR；第903条及官方来源进入法条库。实际风险层只在明确默认规则通过法条校验后生成操作细化后果，不把合同覆盖改为PASS。新增来源ID与法条库保持同一标识，来源传播门禁继续保留。
3. 返还目的仍走宽泛候选路径。声明式绑定 return_entrusted_property 直接义务概念，使用现有共享事实池和 supports 验证、排序。主体信息和贵重物品声明不符合该命题，不进入被接受证据；第七条（一）成为核心证据。本轮未重写全局排序算法、fact pool、SEARCH_AUDIT或renderer。

## 修改文件

- backend/review_v2/element_resolution.py：通用条件元数据解析。
- backend/review_v2/employment_facts.py：现有要素解析入口接入声明式条件。
- backend/review_v2/priority_contract_review.py：移除条件结果中的职业危害专用叙事。
- backend/review_v2/shared_fact_concepts.py：授权责任前提、直接返还义务概念。
- backend/review_v2/safekeeping_contract_checklist.py：返还目的概念绑定。
- backend/review_v2/domain_packs.py：默认规则字段及留置权元数据。
- backend/review_v2/quality4.py：已核验第903条法条来源。
- backend/review_v2/engine.py：明确默认规则的实际后果生成。
- backend/review_v2/lease_semantics.py：明确默认规则不得生成虚假法律不确定性的断言。
- backend/tests/test_declared_element_closure.py：7例新增测试。
- backend/tests/test_fact_condition_followup.py：未说明授权前提的旧测试改为待核验预期；已覆盖事实允许在风险描述中作为正向背景，禁止其被表述为未找到。

## 三项结果

D-08-03：PASS。未经授权转交造成损失的赔偿责任COVERED，证据为第十一条（五）。经授权转交后责任NOT_APPLICABLE，依据第二条（四）明确勾选不允许，不进入缺失计算，不形成风险或修改建议。

D-09-01：合同覆盖仍缺失，行动优先级C_OPTIMIZATION。最终风险描述全文：

> 合同未对“保管人留置权条件”的具体行使条件、通知、范围及操作程序进行细化；欠费时的法定留置权由法律直接规定，合同沉默不等于该权利不存在。实践中可能增加履行沟通或争议成本。

D-01-02：PASS。核心证据第七条（一）：

> （一）保管期限届满或者甲方提前领取保管物的，甲方按照约定支付保管费及其他费用后，乙方应当将保管物归还甲方。

## 回归及范围

新增7例，相关回归合计91例全部通过，5条已有警告。覆盖禁止/允许/允许且责任完备、勾选否、非活动要素不进入分母、直接返还证据排除主体信息及贵重物品元数据、法定默认后果。

D-01-03、D-02-03、D-07-01、D-07-02、COMMON-20-01保持PASS；D-04-04、D-09-03保持N/A；D-12-04保持PARTIAL。D-07-02保留无偿、故意或重大过失完整后句。生产门禁未发现共享事实/SEARCH_AUDIT/最终覆盖冲突。

额外扫描935个清单节点，记录18个明确默认规则绑定（含领域别名重复），见 ../safekeeping-closure/default-rule-scan.json。其他类型的旧配置仍有需结合最终默认法推理复核的宽泛后果文字，例如交付风险、部分还款顺序；本轮未扩大修改这些类型，不能据本次保管合同测试宣称所有合同类型均已完成复测。

官方法条来源：https://www.court.gov.cn/zixun/xiangqing/233181.html
