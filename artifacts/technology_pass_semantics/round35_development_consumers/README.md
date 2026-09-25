# Round35：委托开发合同事实消费者一致性

## 验收文件

- `original_conflicts.json`：真实接口原始 Gate 冲突及同次响应的事实追踪；原始未输出字段明确为 null。
- `before_party_a` / `before_party_b`：修复前真实接口报告。
- `final_party_a` / `final_party_b`：最终源码的真实接口报告。
- `protection_*`：既有保护合同的真实接口报告。
- `acceptance.json`：仅在全部断言通过后生成的最终验收结果。
- `source_audit.json`、`runtime.json`、`*_source_integrity.json`：源码、进程、测试前后哈希与未修改旧测试的审计。
- `final_manifest.json`：产物完整性校验。
- `intermediate_before_creator_unification`、`initial_technical.*`：中间阶段诊断，不能作为最终通过结果。

## 顺序复现

在 `F:/ai/Sage` 目录使用 PowerShell，先执行 `scripts/run_round35_suite.ps1`。
该脚本以单逻辑 CPU、Idle 优先级依次运行新增定向、技术专项、冻结回归，不使用并行测试。

测试结束后依次执行：

1. `scripts/start_round35_backend.ps1`：加载最终源码，保存运行进程和哈希；保留现有 DeepSeek 环境配置。
2. `scripts/run_round35_current.ps1 -Phase final`：当前合同甲乙双方真实 `/review-v2/file`。
3. `scripts/run_round35_protection.ps1`：既有保护样本，逐份调用。
4. 使用 `scripts/run_round33_low_load.py` 分别运行 `scripts/audit_round35_artifacts.py` 与 `scripts/summarize_round35.py`。

不要同时启动测试与接口批量验收。模型输出发生变化时，使用固定输出的 baseline/final 对照；不能把模型波动直接声明为零漂移。

本轮没有执行全仓库全量测试，回归结论限定于验收文件列出的测试集合。未修改 Gate、Verifier、provider fallback 或旧测试预期。
