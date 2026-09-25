# Verifier批次与身份校验验收

原始失败文件：artifacts/report-topic-labels/fact-error-5be71b2c791c453a8fc93b5bb9a9029d.json。
原始第二轮是62个候选、63个checks；missing为空，unexpected为EF-4a7f7b00479f53ab。不是63漏成62。
该旧事实为salary.withheld_for_handover=true，证据C0009第六条“甲方可从乙方首月工资中直接扣除上述保证金。”，不属于DSP新增专项事实。
第一轮Verifier明确拒绝；第二轮修复后候选已移除该事实，但完整历史诊断携带旧ID，模型响应再次输出它。JSON可解析，旧校验未去重或过滤，集合比较正确阻断。没有响应截断证据；原解析器只接受finish_reason=stop。并非请求漏发。

修改：
- backend/review_v2/verification_batches.py：稳定20个/批；逐批和合并集合检查；精确缺失、多余、重复诊断。
- backend/review_v2/deepseek_facts.py：每批保留完整原文和上下文，限定本批ID；历史反馈去除旧事实ID但保留语义；首批全文遗漏审计，其余批仅候选核验；保存各批响应、ID及usage。
- backend/review_v2/fact_verification.py：最终事务使用同一严格集合校验。
- backend/review_v2/employment_fact_pipeline.py：失败保留批次响应。
- frontend/src/views/ContractReviewV2.vue：结构化展示计数、差异和缺失事实；历史生命周期不变。
- backend/tests/test_verification_batches.py、frontend/tests/factDiagnostics.test.mjs：20/50/80/100规模、错集合阻断、历史诊断保留。

测试：相关后端94通过；最终批次专项7通过（包含于上述范围）；前端6通过，生产构建通过。
114合同真实POST /review-v2/file最终实测：第一轮67/67、修复轮64/64，全部分批集合相等，无INCOMPLETE_FACT_VERIFICATION。事实数量随重新抽取变化，未伪造固定63。
但第二轮salary.withheld_for_handover和penalties.obligations仍被语义Verifier拒绝，HTTP503、release_quality_gate=BLOCKED，未生成报告。故DSP规则报告级验收尚未通过，不能以集合完整冒充报告成功。输入合同未修改，没有默认supported或关闭门禁。
详情见acceptance.json、response.json。
