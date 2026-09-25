# 技术秘密许可合同：主体证据与 PARTIAL 聚合一致性回归

## 根因与修复

- TC-11-04 将一般泄密赔偿覆盖布尔值扩写为“违约金及不足部分继续赔偿”；同时把不同责任主体的条款拼接后进行全局搜索。现改为逐责任种类、逐主体抽取，每个字段保留直接引文；同段不同主体也分别绑定。专项违约金及不足部分赔偿独立判断。
- PARTIAL 子项没有 residual_gap 时，被聚合建议生成器跳过。现统一 unresolved_requirements = 可处理的部分未完成项 + 完全缺失项；权属材料明确提供剩余要求，摘要、明细、建议、证据包共享该集合。
- 质量门新增主体/责任证据校验、无违约金证据的叙事拦截、聚合及证据包 unresolved 集合校验、PARTIAL 叙事漏项校验。未降低或关闭原有门禁。

## 修改文件

- backend/review_v2/confidentiality_remedies.py：主体级责任事实及精确证据校验。
- backend/review_v2/element_resolution.py：统一 unresolved 要求投影。
- backend/review_v2/engine.py：接入事实抽取、直接证据登记、PARTIAL 聚合/建议/渲染及质量门。
- backend/tests/test_confidentiality_party_and_unresolved.py：不同角色、同段不同主体、赔偿与违约金区分、PARTIAL 聚合测试。
- backend/tests/test_secret_license_production_closure.py：文件上传生产入口及篡改数据后的门禁阻断测试。
- backend/tests/test_technical_secret_license_contract_review.py：纠正旧测试中将买方防扩散义务扩张至卖方的预期。

## 验证

联合 pytest：140 passed，11 warnings（71.53 秒）。覆盖当前文件生产入口、既有技术秘密许可测试、最终建议及条件性元素、原子证据门禁、第三方索赔精确绑定、角色投影。

通过五种故障注入验证门禁仍会 BLOCKED：虚构违约金、跨主体绑定、聚合漏 PARTIAL、证据包漏 unresolved、叙事漏 unresolved。

当前 DOCX：test_data/38 技术许可（技术秘密）合同.docx，解析 3626 字。

合同文本 hash：73dc8704b30cf567f220f4120e08ba941fc8ae8b62852b5e12eb7adcda1b0fe7。

最终后端 PID：19372，入口 F:/ai/Sage/backend/routers/review_v2.py:1021，审查引擎 F:/ai/Sage/backend/review_v2/engine.py:47841。

引擎 SHA256：1E8B9EDAF032F4FD2A29ACD762DE270266C076D701B68C96DA8686328043C98D。

页面实际复核：保持已上传的同一文件和“启用大模型复核”设置，生成 CR-20260907-111807-5170B2。生产日志确认 TECHNOLOGY_LICENSE 主路由、一次分类、同一文本 hash。页面无 release/quality4 门禁警告；文件生产入口测试 release_quality_gate=REPORT_READY，failures 为空。

## 最终抽查

- TC-11-04：PARTIAL。双方赔偿、停止使用及披露已覆盖；买方防扩散已覆盖，卖方防扩散未覆盖；双方泄密通知未覆盖。未认定已有专项违约金或违约金不足部分继续赔偿。
- TC-03-04 / TC-13-02：部分明确的历史披露对象、披露内容范围、当前秘密状态核验依据均保留在最终未完成集合、风险说明和正式建议中，不再在聚合时丢失。
- 完整明细不再将正向 PARTIAL 描述直接拼入缺失列表；泄密责任首条引文直接展示责任条款，而非只有“泄密责任”标题。
- 上一轮 TC-07-03 PASS、TC-12-02 责任主体、TC-10-03 absence evidence、条件性人工复核聚合等回归通过。

本轮未新增规则、未变更主交易路由，也未放宽 release_quality_gate。
