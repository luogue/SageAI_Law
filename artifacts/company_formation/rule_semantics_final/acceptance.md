# 股东合作协议规则语义验收

最终：REPORT_READY。原86号完整文件未修改；真实页面与启用LLM的multipart生产入口均通过。

## 修改文件

- backend/review_v2/formation_rule_semantics.py
- backend/review_v2/company_formation_checklist.py
- backend/review_v2/priority_contract_review.py
- backend/review_v2/employment_facts.py
- backend/routers/review_v2.py
- backend/tests/test_formation_rule_semantics.py

## 修改逻辑

CF-02保留出资期限存在性及FOUND，新增CF-16独立核验法定上限。deadline_present与deadline_compliant分离，成立时间按明确日期/年份区间计算；未知成立日不认定合法，存量公司不机械套用新设公司五年上限。样本以拟设及合作安排推定2026年，并明确标记为推定而非登记成立日；2035截止触发上限风险，登记日及法定例外仍需核对。

CF-09增加书面通知、通知内容、同等条件和行权期限。旧过半数同意无章程依据时引用原文提示机制衔接；声明有章程特别规定时核验章程与合法性，不直接宣告无效。仅有优先购买权仍为部分覆盖。退出与公司资本返还要素仍按交易主体触发。

CF-04移除保护要素中的账户身份，将其记录为fund_receiver_context，含personal_account_receiver_identified、NEUTRAL、TRIGGER_CONTEXT及protective_coverage=false。资金隔离、共同审批、限期转账核对和退款才参与保护覆盖。

未修改质量门、主分类器或大范围路由。

## 测试

新增16个参数化用例；298项综合回归+28项股权回归=326项通过。最终补齐年份和相对期限的存在性匹配后，106项股东协议相关测试重复通过。未运行全仓库测试。

## 实际生产结果

contract_type=shareholders；scenario=股东合作协议；role=shareholder。规则25，规则风险命中16，风险主题15。

{'major_risk': 6, 'medium_risk': 5, 'low_risk': 4, 'priority_action': 4, 'recommended_action': 8, 'optional_action': 3, 'manual_review': 0}

浏览器请求CR-20260909-105421-717D0E；PID15692；runtime=CURRENT；REPORT_READY；failures=[]。

## 逐项断言

| 检查 | 结果 |
|---|---|
| deadline_present | PASS |
| deadline_risk | PASS |
| deadline_FOUND | PASS |
| old_transfer_source_risk | PASS |
| account_context_only | PASS |
| equity_total | PASS |
| capital_total | PASS |
| party_mismatch | PASS |
| dependent_dates | PASS |
| nonmonetary_applicable | PASS |
| personal_account_applicable | PASS |
| veto_and_unilateral_risk | PASS |
| restrictive_inspection | PASS |
| charter_conflict_FOUND | PASS |
| termination_FOUND | PASS |
| private_exit_not_company_return | PASS |
| unvouched_expenses | PASS |
| unequal_liability | PASS |
| no_sales_rules | PASS |
| release_quality_gate | PASS |
| original_unchanged | PASS |

法律依据：[现行公司法第47、84条](https://www.samr.gov.cn/xyjgs/flfg/art/2024/art_d4e84936a8a744f8928ac7aec7594345.html)。