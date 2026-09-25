# 劳动合同事实与质量门修复记录

## 复现边界与实际 diagnostics

原日志 `backend/logs/app_2026-09-08.log` 留存审查 `CR-20260908-061452-A03BCA`（文件 `57 劳务派遣.docx`，后端 PID 15460，runtime=CURRENT）：status=BLOCKED，failures 中出现两条 `NOT_APPLICABLE_NARRATIVE_GATE`。日志未保存对应 review 列表，也没有 expected_status / actual_status。两个相同的门失败条目不能据此推断为 EMP-15 和 EMP-16。

在本次修改前，用磁盘文件分别执行文本引擎和真实文件上传处理函数（use_llm=True）均得到 REPORT_READY、failures=[]。完整修改前结果保存在 `../employment_before.json`、`../employment_route_before.json`，没有删除 diagnostics。因此目前不能诚实地输出原始两个失败 review 的六字段实值；已向用户索取原始 BLOCKED 响应。工作区同时存在其他任务的未提交修改，不回滚其他任务代码来构造所谓原始结果。

已复现的事实误判：EMP-01/03/07 为缺失，EMP-06/08 为部分覆盖。修复后真实上传处理函数得到 REPORT_READY，所有适用 gate 子项 PASS，failures=[]。项目顶层成功值叫 REPORT_READY，不将其改名为 PASS。

## 最终结果

| 规则 | 修改前 | 修改后 | 核验重点 |
|---|---|---|---|
| EMP-01-01 | 缺失 | 通过 | 括号角色、单位注册地、姓名及居民身份证号码 |
| EMP-03-01 | 缺失 | 通过 | 分行起止日期、试用期月正常工作时间工资 |
| EMP-06-01 | 部分覆盖 | 通过 | 正常工资、支付日、银行转账；无工资金额 NOT_FOUND 审计 |
| EMP-07-01 | 缺失 | 部分覆盖 | 缴纳主体已有证据，仅个人应缴部分及代扣代缴缺失 |
| EMP-08-01 | 部分覆盖 | 通过 | 一般保护 COVERED，职业危害专项 NOT_APPLICABLE，保留否定触发证据 |
| EMP-13/14/15/16 | 通过 | 通过 | NEGATIVE_CLAUSE_CHECK，无不利条款不产生缺失或风险 |

通过不表示整份合同不存在风险，其他实际缺口仍保留在报告中。

## 根因修复

- 扩展专项语义模式，支持结构化字段、角色括号、分行日期；不包含样例人名、公司、工资金额或具体日期常量。
- 日历日期与显式月数统一检查试用期上限，保护性禁止句不作为不利事实；重复约定的否定范围限定到实际谓词。
- 职业危害使用现有 conditional_element：明确不存在为 N/A，存在则核对专项保护，条件未知保留核实状态。一般劳动保护独立核对。
- 保留负向规则 metadata；适用但被后续投影误写为 N/A 的负向规则，在充分否定检索证据存在时恢复“未发现不利条款”的 PASS，不能按正向要素缺失修复。
- 不利谓词/日期计算确认的原文绑定至具体证据要素，防止后续通用相似度判断降格并导致风险聚合丢失。
- 质量门保留原强度及阻断条件，失败对象增加 reviews 原始明细，包含 rule_id、applicability、polarity、expected_status、actual_status、violation_reason。人工注入不一致状态的单元测试只用于验证该门仍阻断，不冒充原始失败复现。

## 修改文件

- backend/review_v2/employment_contract_checklist.py
- backend/review_v2/employment_facts.py（新增）
- backend/review_v2/priority_checklist_helpers.py
- backend/review_v2/priority_contract_review.py
- backend/review_v2/engine.py（条件投影、负向状态修复、失败明细；该文件另有其他任务修改）
- backend/review_v2/lease_semantics.py（共享一致性校验区分条件 N/A 和负向规则）
- backend/tests/test_employment_fact_semantics.py（新增）
- scripts/run_employment_file_acceptance.py（新增，任意输入文件可复用）

## 可复现命令与产物

PowerShell 设置 `$env:PYTHONPATH='F:\ai\Sage\backend;F:\ai\Sage\backend\tests'` 后执行：

```text
python -m pytest backend/tests/test_employment_fact_semantics.py backend/tests/test_priority_contract_review.py -q
python scripts/run_employment_file_acceptance.py "test_data/57 劳务派遣.docx" --use-llm
```

`result.json` 是完整生产响应；`summary.json` 包含源文件 SHA256、全部 gate 和劳动规则逐项证据。`report.md`、`report.docx`、`report.pdf` 由现有报告/导出链路生成。

劳动与新增类型组合测试 127 passed；最终劳动测试单独复核 29 passed。

既有合同及一致性回归 381 passed、4 failed。禁用新增类型适配器后四项仍然失败（`../employment_legacy_control.txt`），未修改它们的业务判断或放宽断言：

- 建设工程 `test_construction_fixture_corrections_for_subcontract_and_tender_points`：期望部分覆盖，实际缺失。
- 赠与 `test_gift_attached_obligation_remedy_depends_on_obligation_content`：期望部分覆盖，实际缺失。
- 赠与 `test_gift_dependency_rules_sync_related_items`：依赖说明断言不一致。
- 房屋租赁 `test_quality_phase_two_separates_coverage_risk_priority_and_findings`：原质量门测试仍 BLOCKED。

详见 `../employment_combined_tests.txt`、`../employment_final_semantics.txt`、`../employment_legacy_regression.txt`。不能把当前工作区描述为全量回归全绿。

已于 2026-09-08 06:38 重启 8016 端口后端以加载此次改动（启动 PID 12540）。

日期上限依据：[市场监管总局公布的《劳动合同法》第十九条](https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/bgt/art/2023/art_0abfdd261c03417b949df19d869add8d.html)。岗位职业危害的合同声明用于文本审查条件判定，不代替实际工作场所的职业卫生调查。
