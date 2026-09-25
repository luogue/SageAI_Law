# 承揽合同救济、证据与适用性修复验收

2026-09-08。未修改、替换当前测试合同，未放宽或关闭质量门禁。

## 原文件核验

- 文件：`test_data/56 承揽合同.docx`，16176 字节。
- 文件 SHA-256：`4e9ad23c61bcc361826f3ae3e46ffe22314e254baecce558785b55751647a8a4`。
- 生产输入层抽取 2805 字，文本 SHA-256：`760eadcdb907b76681cd7023a93f302182a216b67a090fddb143c8c95d4b1bc3`。
- 浏览器本次上传的文件指纹和文本指纹与上述完全一致；各处理阶段保留率为 1。
- 此文件第三条是原材料提供条款，第十二条从第四款开始。用户引用的“要求重作、修理、减少价款或退货”“按质论价”“酌减酬金”“修整或调换”“由此造成的损失由承揽方赔偿”均不在此文件中。
- 因此这些原句作为独立回归用例验证，未补入原文件、未伪造本文件证据。当前文件 W-08 四项仍缺失，不能声称已经满足四项通过的验收要求。

## 根因与修改

1. `backend/review_v2/work_evidence.py`：质量救济的正向原子匹配要求显式质量词，遗漏权利列举、修整、酌减酬金及倒装赔偿表达。扩展同义及语法匹配；调换不等同重作；否定救济不作正向支持。增加专业资质实际场景门控，转包专项使用真实转包/分包场景。
2. `backend/review_v2/sale_evidence.py`：共享证据支持检查执行原子定义的否定模式，使召回和后续要素验证共用同一语义标准。
3. `backend/review_v2/work_contract_checklist.py`：专业资质和违法转包条目的条件不再使用默认“始终适用”。
4. `backend/review_v2/engine.py`：最终位置从最终证据集合生成，避免旧位置残留；适用性结果携带实际条件及 triggered，通用条件抽取使用当前合同类型，消除固定读取买卖条件和默认标签冲突；不适用/始终适用冲突加入既有硬门禁；买方视为验收的条件分支同步条件；反向审查通过不再叙述为有正向条款覆盖。
5. `backend/tests/test_work_remedy_semantics.py`：新增 17 个回归案例，覆盖用户原句、同义词、否定、调换边界、当前文件证据位置、适用性硬门禁、普通与专项许可场景，以及另一承揽合同完整流水线。

## 测试

以下九个测试文件合计 **170 passed**，6 个已有依赖/弃用警告。未更改原有测试数据或降低原有断言。

```text
tests/test_work_remedy_semantics.py
tests/test_work_canonical_evidence.py
tests/test_work_contract_review_checklist.py
tests/test_work_contract.py
tests/test_sale_package_evidence.py
tests/test_sale_review_checklist.py
tests/test_sale.py
tests/test_finance_lease_shared_facts.py
tests/test_loan_cost_combinations.py
```

独立承揽合同含用户提供的救济条款时，W-08-01/02/03/04 均通过，release_quality_gate=REPORT_READY。正常 `2 买卖合同.docx` 保持买卖路由且门禁通过；融资租赁和借款组合利率相关测试通过。

## 当前合同完整重跑

| 项目 | 结果 |
|---|---|
| 合同类型 / 规则数 | 承揽合同 / 44 |
| 通过 / 缺失 / 不适用 | 19 / 24 / 1 |
| 风险主题数 | 24 |
| 重大风险 / 优先处理 / 真正修改 | 4 / 4 / 4 |
| 建议处理 / 可选优化 | 0 / 20 |
| 人工复核 | 0 |
| W-02-02 | 不适用，不形成专业资质重大风险 |
| W-03-04 | 通过；适用条件为转包/分包场景 |
| W-08 四项 | 缺失；上述救济原句不在当前文件中 |
| 总体可签署性 | 建议修改后签署 |
| release_quality_gate | REPORT_READY，无失败 |
| statistics_consistency_gate | REPORT_READY，无失败 |

已扫描全部 44 项：审查项位置等于最终绑定证据位置集合；正向要素的 evidence_ids、source_locations 与支持原句一致；不适用项无始终适用冲突。报告统计由当前结果重新聚合，未沿用旧统计。

最终在线复核于本地时间 06:27:47 完成，进程 18352，runtime_source_drift=CURRENT，release_quality_gate=REPORT_READY、failures=[]。页面显示同一文件、44 项及上述统计；W-02-01 同时列出开头与落款的两个实际证据位置；无“无对应条款已覆盖”矛盾叙事。强化门禁断言后定向复测 1 passed。重启期间曾被共享工作区劳动规则缺字段暂时阻塞，该配置随后恢复，本轮未修改劳动规则或绕过注册校验。

详细结果见 `work-remedies-fixed.json`，逐项证据见 `work-remedy-evidence-audit.json`，源文档与重跑摘要见 `work-remedy-run-summary.json`，测试输出见 `work-remedy-tests.log`。

## 剩余问题

当前上传版本与用户所引完整条款不一致。只有取得含第三条第1款及第十二条第一款的实际文件，才能完成“同一合同四项救济不再缺失”的最终验收。当前文件与页面输入均已完整核验，不能以补造事实满足该条件。
