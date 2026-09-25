# Round36：技术咨询事实与最终报告版本绑定

## 原始证据

- `input/original.docx/txt`：本轮输入快照。
- `before_party_a/b/report.json`：修改前真实接口返回。
- `original_version_diagnostics.json`：原始版本字段均未生成；真实阻断为 TC-08-05 的 DIRECT 证据不足。没有证据证明请求命中了某一旧缓存。
- `baseline_source/`、`baseline_router.py`、`baseline_frontend.vue`：修复前源文件快照。

## 最终证据

- `final_party_a/b/report.json`：真实审查结果及完整 task/run/fact/rule/report/gate 版本、哈希与时间。
- `final_party_a/b/export.docx/pdf`：通过真实导出接口取得的文件。
- `export_receipts.json`：导出版本、文件哈希；旧 run、正文混用、Gate 混用和无版本请求的拒绝诊断。
- `runtime.json`、`source_audit.json`：最终源码哈希、进程和修改审计。
- `acceptance.json`、`final_manifest.json`：最终验收与产物哈希清单；只有验证完成后生成。

## 复现

在 F:/ai/Sage 使用现有 Python 3.10 环境，所有重型任务通过 `scripts/run_round33_low_load.py` 串行执行，单核、Idle 优先级。

1. `scripts/start_round36_backend.ps1` 加载当前最终代码。
2. `scripts/run_round36_current.ps1 -Phase final` 审查两种立场。
3. 通过低负载启动器运行 `scripts/export_round36.py` 校验真实导出。
4. `scripts/run_round36_tests.py targeted` 及 `scripts/run_round36_suite.ps1` 执行定向、专项、冻结及相邻测试。
5. `scripts/run_round36_protection.ps1` 执行既有 17 份立场样本。
6. 低负载启动器运行 `scripts/build_round36_frontend.py`、`scripts/audit_round36.py`、`scripts/summarize_round36.py`。

服务端快照持久化到 `backend/data/review_snapshots.sqlite3`（Git 已忽略），不是用文件修改时间选择报告。跨主机复现应创建新 task/run；既有 UUID 对应原机器服务端记录，不是可移植授权。

`intermediate_version_binding/`、`intermediate_actor_routing/` 和 `intermediate_parallel_exclusion/` 是中间版本诊断材料，不能作为最终验收。最终测试为 61 项定向、376 项技术专项、152 项冻结回归，以及 220 项相邻测试；相邻测试的 14 项失败须与 `adjacent_baseline.xml` 逐项比较。仓库全量测试未运行；测试结论仅覆盖记录的选择集。实时模型波动与同输出源码对照结果分别记录。
