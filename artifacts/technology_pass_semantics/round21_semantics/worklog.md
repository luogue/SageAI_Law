# 当前技术秘密许可合同：逐要素覆盖和命题极性修复

## 范围

- 仍使用冻结原件 `round19_secret_diagnosis/candidate_input/original.docx`。
- 原件 SHA256：`1ad8d39d8fe0905fb7a974a6f014a114c0f1d8d95d8411ad7381fd1f39677ce3`。
- 本轮没有进入下一份新合同；其他真实接口调用均为已有的 11 份保护样本。
- 没有修改旧测试预期，没有恢复结果 fallback，没有修改 Gate/Verifier 的通过标准。

## 根因和公共修改

1. 许可模式存在互不一致的词表。普通使用许可在候选判定和 canonical extractor 中都漏识别。新增 `license_terms.py`，让许可控制、许可事实本体、跨条款分析和候选生产共用模式词表及声明极性检查。
2. 保密例外列表的引导句只接受“保密信息”，漏掉“本合同保密范围”；列表连续性也遗漏“非因……公开”。在 `obligation_detail_elements.py` 修复通用列表作用域，并保留公开、合法取得、独立开发、依法披露四个独立的 `component_coverage`。
3. 秘密性丧失分析把整段压平后匹配“继续支付”，忽略前面的“是否”和后面的“双方未作明确约定”。`proposition_scope.py` 新增共享 arrangement predicate：区分条件安排的存在与事件实际发生，保留缺失列表、否定前缀、尾置缺失和条件列表的作用域。`technology_service_analysis.py` 的付款、解除、通知等生产者共同使用该机制。
4. 触发方式原来由窄词表聚合为一个布尔值。现在逐项提取主动公开、独立研究、反向工程、部分公开等原文，并由 `secret_loss_sources.py` 绑定 parser 原文和条件上下文。现有触发要求是替代关系，未把每一种可能原因新增为强制约定。
5. `element_resolution.py` 统一展开混合状态组件；全部缺失时保留既有复合要求标签。`engine.py` 注册精确事实键，沿用既有消费者绑定和严格校验，并使主引文指向已有的覆盖证据。没有通过降低覆盖标准或放宽校验消除阻断。
6. `technology_adverse_evidence.py` 消费条件列表作用域，避免列表中的假设侵权事实重新成为实际侵权证据。
7. 公共复合字段命题由独立子项生成，父级不再沿用“整组已有原则安排”或把没有证据的触发方式写进“已有约定”。已覆盖、未明确以及替代触发关系使用同一组件状态。

## 实际结果

机器可复核结果见 `acceptance.json`，两方原始响应和报告分别位于：

- `../round21_accepted_current_licensee/report.json`、`report.md`
- `../round21_accepted_current_licensor/report.json`、`report.md`

两次调用均走 `localhost:5173/review-v2/file`，technology、use_llm=true，甲乙双方分别指定立场。最终服务 PID 和源码 SHA256 见 `manifest.json`。

- 许可类型：COVERED，原文证据包含“普通使用许可”。
- 保密例外：公开信息/合法取得 COVERED；独立开发/依法披露 MISSING，SEARCH_AUDIT 只保留后两项。
- 秘密性丧失后未来费用：MISSING，NEUTRAL，没有 affirmative adverse payment evidence。
- 主动公开、第三方独立研究、反向工程及部分信息公开：分别 COVERED，条件及原文绑定保留；触发组不再 MISSING。
- TC-02-02 继续通过；TC-12-02 的诉讼处理、律师费及诉讼费缺失没有被回填为已覆盖。

## 验证记录

- 定向清单包含 123 项，其中本轮新增模块 46 项；保留原有 42 项侵权/第三方主张极性回归。最终输出为 `focused8.xml`。
- `round21_accepted_*` 为最终代码的当前合同甲乙双方和 11 份旧保护样本复跑结果；`acceptance.json` 严格断言 REPORT_READY、原始/展开阻断和 evidence mismatch 均为 0，并比较保护样本风险组。
- 全量清单沿用 Full61，增加本轮模块。最终 XML：`full64_batch0.xml`、`full64_batch1.xml`；逐测试状态差分：`full64_comparison.json`。
- 初始探索运行 `technology1.xml` 含两个不在 Full61 清单中的旧模块。为避免把缺少基线误报为新增失败，另以本轮修改的逆向补丁生成隔离源码覆盖进行前后同测；该补充对照不替代 Full61 历史结果。原工作区未回退，旧测试文件未改变。
- `supplemental_before.xml` / `supplemental_after4.xml`：41 项前后均为 30 PASS、11 FAIL、0 SKIP。`supplemental_comparison4.json` 中新增失败、状态变化、增删测试均为 0。这 11 项独立记录，不并入 Full61 的 249 项历史失败来掩盖新增失败。
- Full62 两批在完成前因发现父级命题残留整组覆盖文字而终止，未计入任何最终测试结论。中间运行保留诊断过程，最终验收以 frozen manifest、`focused8`、`round21_accepted_*`、Full64 为准。


## 全量发现的相邻回归及修复

Full63 完整执行结果为 1083 PASS / 252 FAIL；与 Full61 比较发现 3 项新增失败，未作为最终通过结果。两个合作开发旧测试发现通用覆盖证据排序改变了禁止性风险审查的已有证据顺序；另一个专利许可旧测试发现带授予上下文的正则可吞掉“非”字，将非独占误读成独占。

修复采用公共边界：许可模式正则禁止从“非独占”内部重新匹配独占；覆盖证据的主引文提升只用于正向要求，不覆盖 NEGATIVE_CLAUSE_CHECK 的风险证据排序。新增 3 项非独占长句变体，并将这 3 个原失败用例加入最终定向清单，旧测试预期未改。最终源码清单及后端见 manifest.json。

## 最终验收结果（Full64）

- 最终定向测试 focused8：123 PASS / 0 FAIL，包含本轮新增 46 项。
- 当前合同甲乙双方实际 POST /review-v2/file 均 REPORT_READY；原始阻断、展开阻断、evidence mismatch 均为 0。独立语义断言、父级命题文字和源码哈希均通过。
- 11 份既有保护样本均 REPORT_READY，原始/展开阻断和 evidence mismatch 均为 0；风险组与 round20_complete 完全一致。
- 既有全量清单 Full64：1338 项，1089 PASS / 249 FAIL / 0 SKIP。Full61 为 1043 PASS / 249 FAIL；逐项对照新增失败 0、旧状态变化 0、恢复 0、移除 0，新增 46 项全部 PASS。249 项均为同一批历史失败，全量不是全绿。
- 补充旧模块：41 项，30 PASS / 11 FAIL；supplemental_comparison4.json 显示与独立前测状态完全一致，新增失败 0。
- 最终独立断言脚本 summarize.py 已重新运行通过，结果保存于 acceptance.json；生产代码在完整验证期间与 manifest.json 的 SHA256 一致。
- git diff --check 针对本轮修改文件通过。没有修改旧测试预期、放宽 Verifier/Gate 或恢复结果 fallback。
