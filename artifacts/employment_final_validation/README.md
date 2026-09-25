# 劳动合同最终校验

## 实际输入

继续使用 `F:\ai\Sage\test_data\57 劳务派遣.docx`。源文件未修改、未拼接完整模板条款。

- 文件 SHA256：`253e17e70d97c328540acb7fdc16eff5f01d315e074ea326e2135ed7add15ab4`
- 规范化输入长度：1582 字符
- 规范化输入 SHA256：`4c0bea6b871d5321a5813e6c28d6081826fb03ddbcc116ee3cc545c2167c3b94`
- A“依法安排乙方补休或支付加班工资”：不存在。
- B“甲方依法应向乙方支付经济补偿的，在办结工作交接时支付”：不存在。

`normalized_input.txt` 保存实际输入，`input_audit.json` 保存提取诊断。该规范化哈希与生产上传处理函数返回的 document_hash 完全一致，分类、规则、检索使用同一全文。

## 修复范围

原来 EMP-07 的每一种缺口均继承主题“高”风险。现在专项规则支持为每个要素声明 gap_risk_level，按照**实际未覆盖要素的最高等级**确定该条规则风险级别：

- 用人单位参保缴费义务未覆盖：高。
- 仅个人应缴部分及代扣代缴未明确：中。
- 全部要素覆盖：通过。
- 明确放弃社保等禁止型不利条款：由 EMP-13 独立保持高风险，不受 EMP-07 剩余起草缺口降级影响。

具体决策和支持条款 ID 留存在 decision_trace.element_severity_assessment，后续复用原有 severity、priority、风险主题和统计流程；没有在报告末端改数字，没有改变质量门，没有删除规则或合理缺口。

本轮修改：

- backend/review_v2/priority_checklist_helpers.py：增加可选要素级风险配置及参数校验。
- backend/review_v2/employment_contract_checklist.py：仅为社保两个要素声明高/中等级。
- backend/review_v2/priority_contract_review.py：按实际未覆盖要素计算等级并保留证据审计。
- backend/tests/test_employment_element_severity.py：新增 9 项回归。
- backend/tests/test_employment_round2_semantics.py：统计断言区分社保缺口和其他独立高风险。

未修改其他合同类型的要素等级或判断逻辑，也未改本轮 EMP-05/10/11 的 evidence matching。

## 最终结果

| 规则 | 覆盖 | 严重度/处理 |
|---|---|---|
| EMP-05 | PARTIAL | 中等，建议处理 |
| EMP-07 | PARTIAL | 中等，建议处理；保留个人缴费代扣代缴缺口 |
| EMP-10 | PARTIAL | 中等，建议处理 |
| EMP-11 | MISSING | 低，可选优化 |

重大风险 **0**、中等风险 **3**、低风险 **1**；优先处理 **0**、建议处理 **3**、可选优化 **1**。总体可签署性为“建议修改后签署”。

生产质量门顶层成功状态为 **REPORT_READY**；failures=[]，适用子门 PASS。没有为了实现全 PASS 改动覆盖结论。`verification.json` 的 9 项断言全部为 true，包含输入哈希一致、合理缺口保留、要素严重度、质量门和正文统计一致性。

`result.json` 是完整上传处理函数响应，`summary.json` 包含规则与证据。`report.md`、`report.docx`、`report.pdf` 使用原有生成和导出链路。

## 回归验证

本轮运行 179 项测试，覆盖新增类型、劳动各轮修复、注册体系、买卖、借款和保证合同。首次 178 passed；剩余一个统计测试错误要求简短测试文本的所有主题均不为高风险，但该文本实际还缺主体和工资，断言已改为仅检查社保主题不得为高风险。该项复测通过。生产规则未为该测试降低其他风险。

测试记录：tests.txt、recheck.txt。新增 9 项覆盖：不同参保表达、参保义务整体缺失、仅个人部分存在、明确违法放弃、全部覆盖及合理缺口保留。
