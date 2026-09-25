# Round33：专利权转让与有限回授许可

## 输入与原始诊断

- `input/original.docx`、`input/original.txt`：本轮真实合同的固定副本。
- `before_transferee/`、`before_transferor/`：修复前真实接口报告。
- `original_scope_diagnostic.json`：原始 Gate 和 TC-06-01 完整数据。实际最终证据集合为空；旧聚合命题未通过验证。原 Gate 对空证据与仅付款证据使用相同错误文字。

## 复现

在 `F:/ai/Sage` 使用项目 Python 环境：

**资源限制：所有测试逐个执行，禁止并行。** Python 任务使用
`python -X utf8 scripts/run_round33_low_load.py <脚本路径> <参数>`，该启动器在导入项目代码前限制为一个逻辑 CPU、Idle 优先级。后端使用同一启动器的 `--module uvicorn` 模式，并在测试完成后再运行真实接口验收。

1. 设置 `PYTHONPATH=backend;backend/tests;.;scripts`，按现有环境变量或 `backend/.env` 启动后端。模型仅使用 DeepSeek。
2. `scripts/run_round33_current.ps1 -Phase final`：通过实际 `/review-v2/file` 运行甲乙双方，保存原始 JSON、Markdown。
3. `scripts/run_round33_protection.ps1`：8 个保护样本/立场的真实接口。
4. `scripts/run_round33_tests.py targeted`：本轮定向测试。
5. 同一测试脚本逐个运行 `technical0` 至 `technical3`、`patent`、`existing`。也可将 `patent` 拆成 `patent0` 至 `patent2` 后逐个执行；分片节点固定，不修改测试内容。
6. 运行 `scripts/merge_round33_patent_tests.py` 汇总专利分片，然后运行 `scripts/audit_round33_artifacts.py` 和 `scripts/summarize_round33_acceptance.py`。汇总程序拒绝新增失败、旧测试删除或不一致的源码哈希。

测试分片保存 JUnit XML、日志及测试前后源码哈希。`baseline_source/` 保存本轮修改前源码；`final_source/` 保存修改文件的最终副本。最终报告、状态对照和文件哈希见 `acceptance.json`、`final_manifest.json`。

## 边界与限制

- 不修改 Gate、Verifier、provider fallback 或旧测试预期，不处理既有回归失败。
- 本轮执行定向、技术专项、专利转让及申请权/金额基数回归，未重新运行仓库全量测试。
- 云端模型输出可能波动。对发生风险组差异的保护样本，`check_round33_fixed_protection.py` 将相同模型输出用于修复前后源码，单独比较最终状态。
- 技术秘密转让受让方的固定输出诊断重放，在修复前后均存在相同的三个 COMMON-21-01 历史阻断；它不计入真实接口 REPORT_READY 保护样本。
