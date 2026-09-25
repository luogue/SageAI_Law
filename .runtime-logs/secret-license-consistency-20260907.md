# 技术秘密许可合同一致性收尾验证

本轮仅修改覆盖状态归一、既有许可披露原子要素、人工复核聚合及对应测试。

## 根因与修改

- TC-07-03 的非核心“违约类型区分”原先无证据却生成内部 UNCERTAIN，同时早期 PARTIAL 的 deterministic_semantic_risk 标记阻止最终状态归一。现明确其非核心性质；最终必需要素满足且无实质缺口时归一 PASS，并同步重建证据极性、来源记录及叙事状态。质量门增加无真实缺口却 PARTIAL 的拦截。
- 权属证明把既有许可、测试使用及其他第三方使用合并判断，且许可存在性依赖附件清单完整性。现拆分许可披露、相对方、期限、地域、测试使用和其他第三方使用六个要素，各自直接绑定证据；absence 查询使用同一原子要素识别结果。否定的“未签署许可合同”不构成正向既有许可事实。
- 人工复核原来按规则逐条追加，总览另行按规则计数。现按核验主题、前置条件和规范化指令合并，保留 source_rules；页面、Markdown 和计数使用聚合结果。

## 文件

- backend/review_v2/engine.py
- frontend/src/views/ContractReviewV2.vue
- backend/tests/test_final_coverage_and_review_topics.py
- backend/tests/test_secret_license_production_closure.py
- backend/tests/test_final_element_recommendations_and_conditions.py
- backend/tests/test_technical_secret_license_contract_review.py
- backend/tests/test_technical_secret_transfer_contract_review.py

## 当前合同的生产验证

- 文件：test_data/38 技术许可（技术秘密）合同.docx
- 完整抽取正文：3626 字；正文 SHA256：73dc8704b30cf567f220f4120e08ba941fc8ae8b62852b5e12eb7adcda1b0fe7。
- 认证文件入口：POST /review-v2/file → 完整解析、分类、事实抽取、要素归一、规则审查、聚合、建议、报告生成。
- 生产入口测试：release_quality_gate=REPORT_READY，failures=[]，runtime_source_drift=CURRENT。
- 页面实际请求：CR-20260907-104913-2F2B24；实际执行 F:/ai/Sage/backend/routers/review_v2.py 与 F:/ai/Sage/backend/review_v2/engine.py。
- 页面最终显示 TC-07-03 通过，定位第十七条第1项，无明显残余风险、无独立修改主题。
- TC-03-04 / TC-13-02：既有许可、相对方、期限、地域均 COVERED，不进入最终 missing、建议或 SEARCH_AUDIT；测试使用及其他第三方使用独立保持 MISSING。
- 重复条件核验从两个来源规则合并为一个展示记录，source_rules=[TC-03-04, TC-13-02]；页面人工复核数=1。
- PDF、Word 导出按钮均可用；未绕过质量门。
- 当前合同验证通过后停止重跑。随后仅验证其他合成条款中否定许可和测试使用的证据边界，并重载服务。

## 自动验证结果

- 61 passed：原子覆盖/人工复核主题、完整文件生产入口、最终建议与条件状态、PARTIAL/角色投影。
- 29 passed：技术秘密许可既有回归，包括原有责任、保密、改进和路由断言。一个使用旧复合键 rectification_and_retest 的测试已改为既有整改原子要素断言，未修改验收实现。
- 15 passed：最终原子覆盖/主题测试与技术秘密转让证据分支测试（含前一批重复执行的用例）。
- npm run build 通过；git diff --check 通过。
- 扩展检查发现 test_secret_license_evidence_display_cleanup.py 中三个固定价款 helper 用例仍使用旧 recommendation 接口，未给 final element status，且预期绕过现行 action 映射；这三个历史 helper 用例未通过。该建议实现与这些用例均未在本轮改动，未纳入上述通过数量。

## 本地运行

- 前端 http://127.0.0.1:5173/contract-review-v2；后端 http://127.0.0.1:8016/health。
- 后端最终重载 PID：18148；工作目录 F:/ai/Sage/backend。
- 最终 engine.py SHA256：4cc567532380469085999c733c4f44f85c3a76ad8d58aeab524c789889f60280。
- 服务使用本地工作区源码，不新增规则、不修改主交易路由、不调整 recommendation generator、不降低质量门。
