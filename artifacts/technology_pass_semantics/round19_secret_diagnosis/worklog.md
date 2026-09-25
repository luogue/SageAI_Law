# Round19 技术秘密许可语义诊断

## 状态

本轮已完成语义修复、全量回归及11份冻结保护样本真实上传复验，但秘密许可专项尚未收口。冻结输入的提取文本哈希已与原请求日志一致；原请求立场和原始完整表单/报告未取得，不能将乙方/use_llm=false的本地诊断冒充原请求复现。

候选输入：`candidate_input/original.docx`，复制自 `test_data/122 测试2.docx`。
SHA256：`1ad8d39d8fe0905fb7a974a6f014a114c0f1d8d95d8411ad7381fd1f39677ce3`。
合同编号：TSL-2026-0915-01。

## 已证实的首个错误点

1. technology_adverse_evidence.has_actual_infringement 去掉全文空白后直接匹配，命中“已经明确知道有关技术侵犯第三方”，丢失同一句开头“如甲方…”的假设条件。候选修复前返回 True，详见 candidate_facts_before.json。
2. extract_claim_response_facts 按换行/分号拆句后保留上一句甲方主体，但未将“双方未明确约定：”作用于列表。其后的“由哪一方负责诉讼…”及“律师费、诉讼费…承担”被抽取为 LICENSOR 的肯定义务。
3. 原条件限制匹配仅覆盖“故意隐瞒/明知/已知”，漏掉“已经明确知悉而故意未披露”。条件在抽取和报告要素中均未完整表达。

## 本轮改动

- 新增 proposition_scope.py：源文本命题的条件、缺失列表作用域，保留精确文本。
- technology_adverse_evidence.py：逐命题判断实际侵权，排除假设、否定和未约定事项；保留真实侵权/允许侵权的肯定匹配。
- technology_service_analysis.py：索赔事实消费同一列表作用域，不从缺失成员继承主体；保留 condition/polarity，区分普通事件触发条件与过错限制，同时保留原有“仅提供协助”的限制。
- engine.py：多个既有侵权筛查消费同一个公共谓词；索赔报告要素明确展示适用条件。
- test_claim_semantic_scope.py：新增16项回归；未修改旧测试预期、未删除或跳过旧测试。
- 本轮未修改 Verifier/Gate，未恢复 fallback。

## 验证

- 第一阶段局部 exact_final.xml：69 PASS / 2 FAIL；当时14项新增回归全部通过。两项失败在 Full54 都已失败。后续Full57发现1项新增回归，已修正并补充2项测试；最终微回归scope_fixed.xml为17通过，完整最终结果以Full58为准。
- 已收口专利许可 + 10个冻结保护样本，真实入口 `localhost:5173/review-v2/file`：全部 REPORT_READY、0阻断，风险主题集合无增减。最终详见 guards_final.json。
- 已重启后端加载最终代码，PID7340。11份真实报告的 engine hash 均与磁盘一致。
- 最终全量运行Full58：1017 PASS /249 FAIL /0 SKIP；相对Full54新增失败0、历史恢复0、原测试状态变化0、新增16项全部通过、删除0。详见full58_comparison.json。
- Full55/56 为代码审查期间中断的中间运行，不作为验收。
- local.xml 是中间版本；其中上传测试出现 STALE_REVIEW_RUNTIME 503，不能计作最终代码回归。

## 候选秘密许可本地诊断

参数明确假设为 technology / use_llm=false / 乙方-被许可方，仅本地诊断。
最终报告：candidate_local_final3_assumed_licensee.json。

- TC-02-02：通过；没有从条件责任推断实际侵权。
- TC-12-01：缺失；不得将列表里的未确定处理方当成肯定主体。
- TC-12-02：部分覆盖；通知义务、条件赔偿保留，律师费/诉讼费/处理主体等缺项保留，赔偿要素明确展示条件。
- Gate：BLOCKED，原始1项/展开1项。
- 剩余阻断：TC-11-04 / breach_damage_liability / PARTY_NARRATIVE_STATUS_MISMATCH。责任方赔偿要素为 MISSING 且 risk_relevant=false，被叙述缺失列表排除；主体级核验要求其状态与叙述一致。本轮未放宽检查或强制 READY。
- 最终完整拒绝对象、要素、引用与可取得ID在 diagnosis_final.json；缺失ID保持null。

## 验收限制

- test_data/122 测试2.docx 已由上一轮专利许可换为本轮秘密许可，但检索未发现全量测试直接读取该文件的证据。先前关于多项测试读取此文件的推断不成立，已向用户更正。全量比较以逐ID结果为准，不以输入变化解释未经核实的失败。
- 原用户请求参数/报告仍 NOT_VERIFIED；尚未用猜测参数重新上传秘密许可。
- 缺失原委托开发文件 SHA e5463c90d88b68b07544d560894b0d0487b67aa4e163bb96e817c50206283ef5 仍 NOT_VERIFIED。
- 原有未提交文件均保留；工作区改动清单见 workspace_*_before.txt。没有提交、整体回滚或清理。


## Full57发现的新增回归与修正

Full57为1014 PASS /250 FAIL，新增失败1：test_missing_procedure_does_not_erase_neighboring_cost_duty。根因为整句未约定判定吞掉了转折后独立的律师费承担义务。已保留原断言并修复公共转折作用域，同时保留完整原文条件，新增两项否定/缺失后肯定事实的回归。scope_fixed.xml为17通过（16新增+1旧回归）。最终保护复验详见guards_final.json：11份全部READY，风险主题无增减，PID7340。Full58最终通过回归比较：1017 PASS /249 FAIL，新增失败0。



## 追加：找回原请求日志

backend/logs/app_2026-09-16.log 中找到2026-09-16 05:56:20请求：trace_mu37oipr_gem094mcq，review_id=CR-20260916-055620-A6A270，PID9276，文件名122 测试2.docx、合同编号TSL-2026-0915-01与候选吻合。
原提取文本SHA256：af05442fbe35953987939f548426ba060244e2b05a9c6e7562dcae17da4a589a（这是文本哈希，不能冒充原DOCX文件哈希）。
日志已证实原Gate为BLOCKED，类别为RISK_CLAUSE_REQUIRES_AFFIRMATIVE_RISK_EVIDENCE及EXACT_ELEMENT_REPORT_INVARIANT；后者未记录展开项，不能据此断言原来就是TC-11-04。
同一trace存在真实云调用：Qwen返回400 Arrearage，Doubao返回404 InvalidEndpointOrModel.NotFound，随后DeepSeek调用成功。未改变模型配置。原审查立场及明确表单use_llm值没有在该日志中取得；本地false诊断不是云端请求复现。
筛选日志证据保存在original_request_log_evidence.txt。

候选冻结DOCX经项目InputLayer提取后的全文SHA256，与原请求extracted_full_text完全一致：af05442fbe35953987939f548426ba060244e2b05a9c6e7562dcae17da4a589a。合同文本匹配已验证；原始DOCX二进制哈希未在旧日志中保存。剩余关键缺失信息是原审查立场（原始表单其他参数也未直接取得）。

## 最终汇总

- final_summary.json：整体NOT_CLOSED，原因是秘密许可原请求未完成同参数复现，且该合同本地诊断仍有TC-11-04阻断。
- Full58相对Full54：原1250项状态全部不变；16项新增回归全通过。249项历史失败未修复。
- Full57引入的转折作用域回归已修复，旧测试断言未改。
- guards_final.json：11份冻结样本正常入口复验均READY、0阻断、风险主题无增减，PID7340。
- diagnosis_final.json：同源合同乙方/use_llm=false本地诊断，原始1项/展开1项阻断。
- 待补充：原审查立场，及可取得的原始请求表单或完整报告。

