# Round34 合作开发路由验收

输入冻结于 input/original.docx、input/original.txt。before_party_a/b 是修复前真实接口输出；final_party_a/b 是最终源码真实接口输出。baseline_source 保留修复前 review_v2 全部源码，final_source 保留本轮修改文件。

全部计算均通过 scripts/run_round33_low_load.py 限制 Windows 单逻辑核、Idle 优先级；测试与真实接口串行执行。

复现：依次使用低负载启动器运行 scripts/run_round34_tests.py targeted、frozen、technical。配置沿用 backend/.env，不在产物中保存密钥。后端8016通过同一低负载启动器启动 uvicorn，再执行 scripts/record_round34_runtime.py <PID>、scripts/run_round34_current.ps1 -Phase final、scripts/run_round34_protection.ps1。

最后运行 scripts/audit_round34_artifacts.py 和 scripts/summarize_round34.py。acceptance.json 汇总实际结果，final_manifest.json 保存文件校验值。测试前后源码校验值必须一致，真实接口进程必须与 runtime.json 一致。

initial_technical.* 为首次发现6个退化的诊断产物，不能用作最终验收。最终 technical.* 是修复后完整376项重跑结果。旧测试预期不修改。仓库全量未在本轮执行，不宣称全量通过。
