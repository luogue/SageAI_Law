# 委托开发统一事实链路验收

## 最终验收

- 原文冻结副本：`round14_entrusted_input/original.docx`，SHA256 `0d435596e1bfc8def44bef5e7ed67520d2b7fe645a51a5ba5a484686816f2a15`。
- 正常接口：`POST /review-v2/file`，经5173代理至8016，`run_mode=review`，`use_llm=false`。没有诊断分支、鉴权依赖替换或Gate绕过。
- 最终后端PID 3652，启动时间2026-09-15 09:41:08；所有验收回包来自该进程。11个修改业务模块在接口验收和最终全量期间哈希均未变化。
- 当前合同：**REPORT_READY，原始阻断0，展开阻断0**。
- 全量full35：**948 PASS / 251 FAIL，1199项，无跳过或删除**。
- 对比full31的925/252：新增22项全部PASS，原FAIL→PASS 1项，原PASS→FAIL 0项，测试迁移0。
- 中途full33暴露的3项新增回归已全部修复，不采用full33或已中止的full34作为最终结果。
- 当前报告53项：7通过、11部分覆盖、5缺失、29不适用、1待核验；保留13个风险主题。

## 根因与公共修复

1. 已抽取或可识别的事实未进入当前规则的要素集合；规则投影仅看到缺失的索赔子项，继而整体MISSING。按统一原子事实族消费、精确要素证据聚合，保留独立缺口。
2. 列表继承依赖序号，未编号交付清单及保密例外后半段遗漏；修复谓词继承及列表边界，引用始终是原文连续span，不拼造原文。
3. 验收、文档、延期救济及改进事实跨规则使用不同映射；统一canonical key与事实族投影，保留主体、条件、对象和原始条款。
4. 明确未约定被识别为未来协商；否定归属被错误正向投影；分别保存明确absence、有限边界与正向覆盖。
5. 新增边界保护：第三方检测费不等于组件费，收到验收通知不等于改进通知，软件交付物不等于整个项目是纯软件。
6. 首次真实接口还有分类信号污染与N/A理由范围错误：系统功能中列举的合同类别不是当前标题，信息提供方/第三方供应商不是当前双方角色；缺少独立技术秘密收费基础不等于没有技术秘密。

修改模块位于`backend/review_v2/`：

- `obligation_detail_elements.py`：列表、例外、共享验收及改进、受限使用权原子事实。
- `technology_fact_ontology.py`：文档别名、验收canonical key、使用权行为归一。
- `technology_transaction_evidence.py`：验收与费用变更事实映射。
- `technical_component_facts.py`：组件选用、商业许可、费用、服务连续性；与侵权救济区分。
- `development_exit.py`：延期事件—解除/损失后果、退出交接、样品适用性。
- `entrusted_development_elements.py`：明确未约定与未来协商区分。
- `material_disposition.py`：业务数据归属、返还/删除及备份证明的否定边界。
- `engine.py`：统一事实注册、消费、精确投影及element级正向证据检查。
- `element_evidence_projection.py`：只接受有具体element归属的正向来源。
- `domain_selection.py`：标题与主体信号来源约束。
- `report_state_consistency.py`：区分收费前提缺少与技术秘密存在性否定。

## TC-12-02

整体 **MISSING → PARTIAL**。每个正向要素保留第十三条精确原文；每个缺口独立全文检索审计。

| 要素 | 最终状态 |
|---|---|
| 第三方组件选用权限 | COVERED |
| 商业许可合规限制 | COVERED |
| 开发期/上线后API费用承担 | COVERED |
| 第三方服务停止/接口调整后的替代安排 | COVERED |
| 自行开发内容侵权责任 | MISSING |
| 取得授权/替换修复的侵权救济 | MISSING |
| 第三方索赔通知 | MISSING |
| 抗辩与和解控制 | MISSING |
| 抗辩费用承担 | MISSING |

服务中断替代措施没有被用来证明侵权替换救济。

## 其他逐项变化

| 规则 | 修复前 → 修复后 |
|---|---|
| TC-04-01 | PARTIAL → PASS；验收标准MISSING → COVERED，与TC-13-03复用同一事实 |
| TC-05-04 | 整体仍PARTIAL；延期后果、研发资料交接MISSING → COVERED；纯软件样品MISSING → N/A；阶段交接MISSING → PARTIAL；代码、费用结算正向事实保留 |
| TC-10-01 | VERIFY → PARTIAL；甲方自行改进归属COVERED，乙方“不当然归甲”的边界PARTIAL，不推导完整乙方所有权 |
| TC-10-02 | 整体仍PARTIAL；复用独立改进归属，授权协商PARTIAL；许可费、地域、期限等真实缺口保留 |
| TC-10-03 | VERIFY → MISSING；明确未约定通知作为absence，不再因证据不足进入待核验 |
| TC-11-02 | 整体仍PARTIAL；保密例外PARTIAL → COVERED，独立开发与依法披露均命中；没有捏造终止后义务 |
| TC-13-01 | 整体仍PARTIAL；用户/操作资料、测试报告MISSING → COVERED |
| TC-13-03 | 整体仍PARTIAL；复用同一测试报告交付事实；测试用例、验收记录、第三方复测等仍独立判断 |

额外扫描修复：TC-04-02新增范围费用调整已覆盖；TC-04-03未约定专利费用从伪PARTIAL改为MISSING；TC-05-03受限使用权和开发方使用边界从MISSING改为PARTIAL；TC-05-03/TC-11-03共享业务数据处置事实，后者整体MISSING → PARTIAL。未把“删除备份后的证明程序未约定”倒推成已约定备份删除。

最终扫描：无正向span的伪PARTIAL=0，同canonical key的COVERED/MISSING冲突=0；报告证据污染、精确要素绑定等现有Gate均通过。

## 回归与限制

- 新增`backend/tests/test_development_shared_list_mapping.py`共22项全部通过；最终局部包含3项原回归，共25/25通过。
- 唯一历史恢复：`backend.tests.test_technology_exact_truth_pipeline::test_production_route_exit_has_exact_positive_and_separate_absence`。它依赖可变122文件，但本轮已冻结原文且哈希相同；同一原文的修复前真实报告中迟延后果为MISSING，修复后为COVERED，有直接前后证据。
- 7个真实保护样本：合作开发、跨条款保密、专利许可、技术咨询、服务方责任上限、保密方向、附随服务费用，全部REPORT_READY/0阻断；对照此前报告没有风险主题、缺失要素或不利要素集合丢失。
- 旧版委托开发保护原件（SHA256以e5463c90开头）仍缺失，**NOT_VERIFIED**；没有用当前新合同冒充。
- 技术全量之外的域选择专项额外跑了3项，2通过、1失败。该失败是既有S-03-02展示状态及house_lease请求类型链阻断；隔离移除本轮新增信号过滤后阻断对象完全相同，详见`round14_domain_guard_audit.json`。未将其放行或计入技术全量恢复。
- 251项技术历史失败未在本轮全部解决。

机器可读结果：`round14_final_summary.json`；最终真实报告：`round14_final_entrusted_live/report.json`及`report.md`；全量：`full35_batch0.xml`、`full35_batch1.xml`。
