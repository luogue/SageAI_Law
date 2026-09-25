# 房屋租赁审查复测记录

发布保持 `release_quality_gate=BLOCKED`，未解除房屋租赁类型复测限制。

## 根因与修改

- `backend/review_v2/lease_semantics.py`：维修费用要素此前仅匹配关键词。现在通过声明式责任主体、适用场景和排除场景约束，要求同一事实语句同时支持费用性质、承租人损坏责任及押金扣款场景。没有按 HL 编号或本合同结果特判。
- 同文件新增规则级证据投影：按当前要素语义选择正向原文，负向证据只来自该缺失要素实际执行的 NOT_FOUND 检索记录；用稳定合成 ID 标识缺少原 ID 的证据。
- `backend/review_v2/engine.py`：结构化结果提供 `rule_evidence_package`；规则明细使用该规则的投影，风险主题保留共享证据池。证据去重前补齐原文和定位身份，避免缺失字段导致错误合并；用户报告不显示空证据 ID。
- `backend/tests/test_lease_scenario_projection.py`：新增跨主体/场景反例、要素归属、负向检索归属、稳定 ID 和最终报告断言。
- `backend/tests/test_lease_evidence_alignment.py`：更新原先错误接受甲方维修费用证据的预期。
- `backend/tests/test_lease_http_consistency.py`：增加两次上传结果的证据映射、风险主题和风险分级统计一致性断言。
- `scripts/run_lease_scenario_acceptance.py`：同一 DOCX 两次完整接口复测，保存原始响应和验收结果。

## 结果

| 项目 | 修复前 | 修复后 |
| --- | --- | --- |
| 已覆盖 | 32 | 32 |
| 部分覆盖 | 5 | 4 |
| 缺失 | 9 | 10 |
| 不适用 | 4 | 4 |
| 总数 | 50 | 50 |
| HL-037 | 部分覆盖，误用甲方维修责任证据 | 缺失，四项押金扣款费用约束均无直接正向证据 |
| HL-043 | 已覆盖 | 已覆盖，30 个工作日原文保留 |
| HL-021 | 已覆盖 | 已覆盖，第十一条证据保留 |

227 项完整回归通过，最终调整后的 13 项针对性复验通过（与完整回归有重叠，不累加）。两次同一合同完整上传审查的覆盖状态、规则级证据映射、风险主题统计与分级统计一致。全部 actionable 子项进入顶部建议；最终报告无 None 证据 ID、无已知跨合同类型专属叙事。

完整报告：`report.md`；结构化报告：`report.json`；原始响应：`run-1.json`、`run-2.json`；验收数据：`validation.json`；测试：`regression.xml`、`final-regression.xml`。

复测通过隔离 FastAPI TestClient 调用真实 multipart 上传路由，仅测试应用覆盖认证依赖，生产认证未变，未替用户刷新浏览器中的旧报告。启用模型调用；当前千问与豆包接口不可用，日志显示自动降级至 DeepSeek 完成调用。
