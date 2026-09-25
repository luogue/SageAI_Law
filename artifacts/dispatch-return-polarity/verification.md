# 115劳务派遣：退回事由极性验收

当前业务接口 POST http://127.0.0.1:5173/review-v2/file 完整复测通过，后端 PID 17568。
trace：CR-20260911-172205-69A498。

## 最终结果

- FACT_VERIFICATION：PASS，dispatch.return_terms 为 VERIFIED_PRESENT，没有残留 rejected_fact_ids 或 unresolved。
- 法律法规规定的退回情形：LEGAL_REFERENCE_ONLY，不虚构具体法定事由和程序。
- 配合度不足：独立 PROHIBITED_RETURN_REASON，保留原文。
- 不适合团队文化：独立 PROHIBITED_RETURN_REASON，保留原文。
- DSP-10-01：通过，保护性禁止条款没有进入“退回条件过宽”风险。
- release_quality_gate：REPORT_READY。
- 本次真实运行第1轮因 dispatch.return_terms 校验失败，第2轮在单次纠错预算内完成定向重抽并验证成功。原始诊断及两轮轨迹均保留在 response.json 的 structured_fact_debug.validation_attempts。
- 原115文件哈希与修复前一致，未修改合同。

## 根因及修改文件

1. backend/review_v2/employment_conditions.py：原关系对象没有允许/禁止/概括法律引用的独立维度，DSP-10 只看 basis。现在 disposition 必填，分三类；缺字段或禁止型还带允许依据会被严格拒绝。风险须同时是 ALLOWED_RETURN_REASON、REASON_ALONE 及对应过宽事由类型。
2. backend/review_v2/deepseek_facts.py：向抽取与 Verifier 提供必填极性及关系字段约束；要求解析否定作用范围、逐项列举、不得将法律概括引用当具体法定条件；要求显式 corrects_fact_id 关联替代纠正。对象内布尔false按字段含义验证，避免仅因出现费用名词忽略 required=false。
3. backend/review_v2/fact_verification.py：同概念另一条通过的事实不能掩盖拒绝项。同原文中的补充事实也不能自动当成纠正，须明确关联被纠正候选及来源。未纠正的核心事实继续触发现有一次定向重抽流程；再失败仍 BLOCK。
4. backend/tests/test_dispatch_return_polarity.py（新增）、backend/tests/test_dispatch_boundaries.py（更新结构）。

现有 employment_fact_pipeline 的单次预算和按失败概念重抽机制保持，不重抽其他概念，不更换模型、不以关键词改写结果、不删除证据绕过验证。

## 验证

- 208项相关自动化回归通过，0失败；包括允许/禁止/不当然/概括法律引用、混合极性保存、第一次纠错成功、第二次仍冲突则阻断、错误极性元数据拒绝、拒绝候选不能被同条款其他事实掩盖。
- 另有5组真实DeepSeek抽取测试通过，覆盖用户列出的不同措辞及允许/禁止并存，并验证输出引用确实属于输入原文。见 deepseek-phrasing-results.json。
- 完整生产报告见 report.md；结构化结果及全部纠错轨迹见 response.json；断言结果见 acceptance.json。

中间复测的培训审计范围漏项和布尔否定校验失败均曾正常BLOCK，诊断保留在 scope-failure.json、boolean-verifier-failure.json，没有关闭门禁或伪造通过。
