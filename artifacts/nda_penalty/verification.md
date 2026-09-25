# 通用违约金基数检查验收

## 现有能力与根因

现有 sale_liquidated_damages_adjustment 识别违约金或比例表述，借款、租赁、中介有领域计算规则，但没有可直接复用的跨合同“比例基数能否从正文确定”的检查。本轮属于规则能力缺失，不是 NDA 原有救济规则漏召回。NDA-04 的损失赔偿存在与违约金基数可确定是两个不同事实。

## 修改文件

- backend/review_v2/penalty_base.py：新增 COMMON-20-01 通用规则；解析比例、基数名称，全文查找金额定义、可验证公式及未付款余额计算条件。只有无法确定的基数触发通用缺口审查，不以百分比本身判断风险。
- backend/review_v2/engine.py：所有合同共用审查入口动态接入通用检查，沿用专项要素、风险聚合、报告及质量门。
- backend/review_v2/employment_facts.py：在既有要素解析入口调用通用基数解析。
- backend/review_v2/priority_contract_review.py：注册通用检查映射，保存 base/rate/definitions/status 的实际解析诊断。
- backend/review_v2/domain_selection.py：将明确注册的通用规则加入可加载集合，不放开其他跨领域规则。
- backend/review_v2/nda_semantics.py：主体定义从完整字段起始识别，排除复合角色定义标题；为保密信息完整定义配置优先证据。
- backend/review_v2/lease_semantics.py：可选的优先证据配置，仅在已通过原有证据资格检查的候选中选择；未配置的规则不变。
- backend/routers/review_v2.py：通用模块加入运行时版本检查。
- backend/tests/test_penalty_base.py：新增11项测试。
- backend/tests/test_nda_semantics.py：当前文件预期从8项更新为8项原规则＋1项通用检查，并断言新缺口。

## 核心判断

比例基数已有明确金额不报缺口；合同总价及付款金额/付款记录使未付余额可计算时不报缺口；公式的操作数也必须能确定，不能只看到“减去/合计”便视为可计算。定义金额与任意第三方费用不混同。

未定义基数保留其原文比例证据，同时对该基数的金额或可验证确定方法产生真实缺口。不会用 NDA-04 的赔偿证据证明违约金基数确定。

## 当前完整结果

|规则|状态|
|---|---|
|NDA-01-01|PASS|
|NDA-02-01|PARTIAL，仅缺返还或销毁|
|NDA-03-01|PASS|
|NDA-04-01|PASS|
|EMP-14-01|N/A|
|NC-01-01|N/A|
|NC-02-01|N/A|
|NC-03-01|N/A|
|COMMON-20-01|PARTIAL，中等风险，建议处理|

新增项命中第三章第1项“还应支付所应投资额的20%作为违约金”。全文未发现所应投资额的金额或确定方法。比例与缺口分别取证，release_quality_gate=REPORT_READY，failures=[]。

## 证据精度

- NDA-03第二方实名：修复前可能绑定“信息披露方/接受方”复合定义标题；修复后绑定首页乙方实名及尾部乙方签署位置。角色定义继续只用于流向要素。
- NDA-01信息内容：修复前主要为第二章标记方式；修复后优先第一章第4项完整保密信息定义。两项仍PASS。

## 测试

75项全部通过：通用基数11项、NDA11项、竞业32项、标准劳动合同21项。覆盖用户A–E、其他比例和基数名称、缺少付款数据、未定义公式操作数、NDA与买卖跨类型接入、当前协议全链路及证据精度。

日志：artifacts/penalty_regression.log。解析记录：base_resolution.json；全文与逐要素查询：normalized_input.txt、actual_element_inputs.json；完整报告：report.md、report.docx、report.pdf。
