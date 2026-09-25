# Round30 技术秘密转让：复现说明

## 范围
本轮只修正既有规则的事实抽取、角色与对象作用域、canonical fact 到最终 component 的投影。没有增加规则 ID；没有修改 Gate/Verifier；没有恢复 provider 或审查 fallback；没有修改既有测试预期。

## 输入与源码
- `input/original.docx`：当前真实上传原件；`input/original.txt`：提取正文。
- `baseline_source`：修改前模块；`final_source`：最终模块快照。
- `validation_source_hashes.json`：最终验收开始前源码摘要；`validation_test_hashes.json`：测试摘要。
- `baseline_test_hashes.json`：既有测试摘要，用于确认无修改和删除。
- Round29 冻结验收产物不作修改。

## 复现入口（工作目录 F:/ai/Sage）
1. 正常启动 backend 的 `uvicorn main:app --host 0.0.0.0 --port 8016`，配置仅从环境变量/backend/.env 读取。
2. `scripts/run_round30_final_regression.ps1 -Batch 0/1/2/3`：沿用上一轮完整回归清单，加本轮新测试；输出 `full83_batch*.xml/out`。
3. 单独执行 `test_secret_license_production_closure.py::test_scope_liability_survives_file_pipeline`，输出 `focused_extra_final.xml`。专项其他 375 项从全量结果按相同测试标识提取。
4. `scripts/run_round30_protection.ps1`：25 个真实接口保护/补充对照样本。
5. 全量结束后执行 `scripts/run_round30_current.ps1 -Phase current`：当前原合同甲乙双立场真实 `/review-v2/file`。
6. `scripts/summarize_round30_acceptance.py`：校验最终源码、旧测试、逐项状态、真实接口绑定及回归差异，输出 acceptance.json。

## 结果解释
- `full81`、`full82`、`candidate_*`、`focused.xml`、`targeted.xml` 为过程诊断，不能冒充最终结果。
- `targeted_final.xml` 是 full82 前的 73 项新测试和 3 项受影响既有测试，仅作过程诊断；最终新增 77 项从 full83 完整结果核验。
- 历史全量失败以 Round29 `full80` 为基线逐项比较，不用总失败数相减替代新增失败检查。
- 保护样本有一项预期纠错：已有专利转让样本的明确总价可作为违约金基数，移除其 COMMON-20-01 误报。
- 实时模型波动单独记录，不宣称所有扩展样本风险组零漂移。`model_variation_control.json` 记录同一实时模型输出在新旧源码上的等值对照。该诊断不是生产接口验收替代品。
- 所有最终数量与限制以 `acceptance.json` 为准；未生成该文件前不代表最终验收已完成。
