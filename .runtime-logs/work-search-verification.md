# W-08 实际 SEARCH_AUDIT 路径核验

2026-09-08。本轮先采集运行时 corpus，再修改判定入口；未修改合同文件、报告叙事或门禁标准。

## 实际输入

当前 `56 承揽合同.docx` 文件 SHA-256 为 `4e9ad23c61bcc361826f3ae3e46ffe22314e254baecce558785b55751647a8a4`，与此前上传一致。

| 检查层 | 重作 | 修理/修整 | 酌减酬金/减少价款 | 损失由承揽方赔偿 |
|---|---|---|---|---|
| DOCX XML 包与抽取正文 | 无 | 无 | 无 | 无 |
| fact extractor 实际输入 | 无 | 无 | 无 | 无 |
| W-08-01～04 SEARCH_AUDIT 实际输入 | 无 | 无 | 无 | 无 |

fact extractor 与四个 SEARCH_AUDIT 均收到57个 chunks，其拼接文本与完整抽取正文逐字相同，哈希均为 `760eadcdb907b76681cd7023a93f302182a216b67a090fddb143c8c95d4b1bc3`。第十二条以 C0053 进入全部检索输入，其中有第四款逾期交付责任与第五款不能交付责任，没有第一款。实际采集见 `work-search-corpus-audit.json`。未发现当前输入链路裁剪正文或仅搜索结构化补充字段的证据；工作区 scripts 中也未找到对应文件或模拟加工数据的组装逻辑，无法确认该文件创建前的模板编辑历史。

## 修复的代码缺陷

- `backend/review_v2/engine.py`：承揽事实提取使用原子语义匹配，但 `_search_final_element` 未调用该匹配器，可能退回要素描述字面搜索。现在直接调用 `work_evidence_for`，记录 `WORK_CANONICAL_REQUIREMENT`；发现正向证据时使用同一 canonical quote/evidence_id 恢复覆盖，不拼接整条原文。
- `backend/review_v2/work_evidence.py`：提供统一 `evidence_for` 入口，提取与 SEARCH_AUDIT 共用；重复主体声明保留首次原文证据，开头与落款同名不再形成两个身份事实。兼容“酬减酬金”的输入写法。
- `backend/tests/test_work_search_corpus.py`：9项新增直接断言，包含用户给出的救济原句、否定与调换边界，以及生产输入层到 fact extractor/每个 SEARCH_AUDIT 的逐字一致断言。

## 回归和重跑

- 检索路径、同义救济、当前承揽及正常买卖文件：33 passed。
- 承揽清单、承揽基本规则、买卖证据/清单/基本规则：100 passed。
- 另一份含上述救济条款的承揽回归，W-08 四项全部通过，真实原句绑定。
- 当前文件完整44条：19通过、24缺失、1不适用；24个风险主题、4项重大/优先修改、20项可选优化；REPORT_READY，无失败。
- W-02-01：通过；唯一绑定位置“全文”，coverage_elements.source_locations 同为“全文”，不再附带第十五条位置。
- 当前文件 W-08 四项仍为 NOT_FOUND，但已明确在实际运行路径使用共享 matcher。

完整最新结果：`work-search-fixed.json`。仍不能满足“当前文件 W-08 不得全部 MISSING”这一项，因为该文件没有相应正向原文；不得通过补造模板内容实现验收。需要含这些原句的实际文件或其明确原始来源，才能继续追查源文件形成前的覆盖/裁剪问题。
