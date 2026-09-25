# 技术秘密许可合同：事实极性修复验收

## 最终结果

- 当前真实合同：甲方/许可方、乙方/被许可方两种立场均 `REPORT_READY`；原始阻断 0、展开阻断 0、evidence mismatch 0。
- TC-02-02：`通过`，未发现对应不利条款或安排，无 ADVERSE 要素及对应风险发现。
- TC-12-01：缺失；TC-12-02：部分覆盖。诉讼处理、律师费、诉讼费仍为 MISSING；已约定的条件责任保留原文适用条件。
- 11 个保护样本：全部 `REPORT_READY`、零阻断；相对 Round18 基线的风险项集合均无增减。
- 专项：57 通过、0 失败，其中新增极性/证据回归 42 项。
- 全量 Full61：**1043 通过、249 历史失败、0 跳过**，共 1292 项；并非全绿。
- 对比 Full54（1001/249）：新增 42 项全部通过，新增失败 0、旧用例状态变化 0、遗漏 0。
- 对比 Full58（1017/249）：新增 26 项全部通过，新增失败 0、旧用例状态变化 0、遗漏 0。
- 最终后端 PID 8004，源码哈希与冻结清单一致。

当前报告：`../round20_complete_current_licensee/report.md`、`../round20_complete_current_licensor/report.md`。
机器可核验汇总：`acceptance.json`；全量比较：`full61_comparison.json`、`full61_vs_full58.json`。

## 修改文件

1. `backend/review_v2/proposition_scope.py`：统一作用域、条件、否定、未明确/未确认语义。
2. `backend/review_v2/technology_adverse_evidence.py`：基于统一极性的侵权事实检测与原文提取。
3. `backend/review_v2/technology_service_analysis.py`：第三方主张的缺失列表、主体及责任条件提取。
4. `backend/review_v2/engine.py`：统一判定消费、ADVERSE 原文绑定、条件责任及缺失状态叙述投影。
5. `backend/tests/test_claim_semantic_scope.py`：42 项新增回归。

上述清单仅列本次修复涉及的源码/测试文件；工作区原有其他改动未清理或回退。

## 根因与修复

- 原侵权检测在压缩后的文本上进行关键词匹配，丢失条件前件。第十二条“如甲方……已经明确知道有关技术侵犯第三方……”和第十三条第三方主张条款不能证明侵权已经发生。
- 第三方主张提取器未继承“双方未明确约定：”对后续列表成员的作用域，并沿用前句责任主体，错误生成诉讼处理和费用承担事实。
- 统一 `proposition_scope.py` 保留原文片段并区分 AFFIRMATIVE、CONDITIONAL、NEGATED、MISSING。缺失列表作用域跨分号、换行延续；新条款、句号、显式独立约定终止该作用域。
- `technology_adverse_evidence.py` 的事实提取及搜索谓词共享上述极性语义。条件事件不能证明实际发生；条件后件仍可作为对应风险分配规则的有条件义务。
- `technology_service_analysis.py` 的第三方主张提取器使用统一作用域，清除缺失列表中的主体继承，保留赔偿义务的原始适用条件。
- `engine.py` 使用统一侵权谓词；明确侵权事实在候选事实投影阶段绑定原文 ADVERSE 要素，继续接受既有独立验证和 Gate。
- 同时补齐 TC-11-04 非独立风险的缺失要素在报告中的文本完整性记录，避免要素状态与叙述遗漏冲突；不把该记录加入风险建议。
- 没有修改 Verifier/Gate 判定条件、恢复结果 fallback 或修改旧测试预期。

## 输入与版本

- 当前合同冻结文件：`../round19_secret_diagnosis/candidate_input/original.docx`。
- SHA256：`1ad8d39d8fe0905fb7a974a6f014a114c0f1d8d95d8411ad7381fd1f39677ce3`。
- 原请求日志中的提取文本 SHA256：`af05442fbe35953987939f548426ba060244e2b05a9c6e7562dcae17da4a589a`，与当前真实上传一致。
- 原请求的审查立场表单没有记录。因此显式复跑甲方/许可方、乙方/被许可方两个立场，均 `contract_type=technology, use_llm=true`，不将其冒称为原请求参数恢复。
- 最终源码哈希见 `manifest.json`；最终上传使用 `round20_complete_*`。
- `round20_final_*`、`round20_verified_*` 是扩大通用否定/假设表达检查前的中间验收，不用于最终结论。
- Full59、Full60 为补充作用域边界修正前主动中止的运行，不用于验收。最终全量运行是 Full61 两批。

## 验证位置

- 专项回归最终文件：`focused7.xml`，57 项通过、0 失败（42 项新增极性/证据回归、15 项既有专利测试）；另保留各次边界补充的中间测试结果。
- 全量：`full61_batch0.xml`、`full61_batch1.xml`。
- 基线逐项比较：`full61_comparison.json`。
- 当前合同、11 个保护样本以及全量摘要：`acceptance.json`（由 `summarize.py` 校验生成）。

最终结果以完整生成的全量 XML、比较文件和 acceptance.json 为准。

## 新增测试边界

- 条件：如/若第三方主张、如签约前明知、若确认侵权、假如、当……时、在……情况下。
- 否定与未确认：未发现、未侵犯、并未侵犯、不会侵犯、不再侵犯、未确认、无法确认。
- 缺失列表：无主体的列表成员、带“甲方承担”等主体的列表成员、列表后的独立正向义务。
- 正向事实：明确确认目前侵权；缺失或否定后用“但”作独立侵权确认；侵权确认后另述处理方式缺失。
- 原文绑定与报告：真实侵权必须有 ADVERSE 要素及 DIRECT 原文证据；无实际侵权时不得产生该项风险；条件责任保留适用条件；非独立风险的缺失状态仍在报告中可见。
