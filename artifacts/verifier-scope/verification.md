# Verifier搜索范围验收

根因：旧批处理按事实ID拆分，但每批都要求返回全schema搜索清单，并向后续批发送“只核验候选、首批已审计全文”的冲突指令。本次原始第4批expected119、actual12、missing107、unexpected0；包含dispatch.onward_assignment、dispatch.return_terms、worker.security_payment在内的概念已经注册并进入原始请求，非parser删字段、非合并丢项、非schema遗漏。完整差异见original-diagnosis.json。

修改文件：
- backend/review_v2/verification_batches.py：当前schema生成概念责任批次，包含零候选概念；双上限20概念/20事实；逐批与合并搜索集合对账，紧凑结构化诊断。
- backend/review_v2/deepseek_facts.py：传递每批required_concepts、定义和允许的absence_audit范围；每批全文检索；仅合并模型实际返回的searched_concepts；保存责任范围、响应和ID。多事实概念可分事实批但只一个遗漏审计责任批，避免重复新增事实。
- backend/review_v2/fact_verification.py：最终FactStore使用同一搜索范围校验。
- frontend/src/views/ContractReviewV2.vue：展示expected_count/actual_count/missing_concepts/unexpected_concepts与批次，保留历史诊断和折叠生命周期。
- backend/tests/test_verification_scope_batches.py、test_verification_batches.py；frontend/tests/factDiagnostics.test.mjs。

测试：相关后端114通过；最终20/50/125概念、20/50/80/100事实协议测试15通过（属于前述范围）；前端7通过，构建通过。测试含零事实概念、自动纳入新增字段、多事实单概念、缺失/多余搜索声明fail-closed。

真实业务接口POST http://127.0.0.1:5173/review-v2/file，文件114 外派岗位劳动协议.docx未修改。最终HTTP200、REPORT_READY；119 required=119 searched，missing=[]、unexpected=[]。6批搜索数量20/20/20/20/20/19，候选67个均获对应checks。第2批含dispatch.onward_assignment、dispatch.return_terms；第6批含worker.security_payment；DSP-09/10风险命中。完整验收acceptance.json，报告report.md，原始响应response.json。

未自动补searched_concepts，未更改supported判断、证据门禁或DSP规则。首次本轮实测暴露模型把普通缺失概念写入特殊absence_audits，按原校验阻断；随后将允许的证明概念从既有ABSENCE_SCOPES明确传入每批请求，最终实测通过。
