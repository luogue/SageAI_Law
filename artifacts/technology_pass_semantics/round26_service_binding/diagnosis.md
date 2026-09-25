# 当前技术服务合同：原始 Gate 诊断与公共修复

完整机器诊断见 `before_diagnostics.json`。以下四项来自修复前甲、乙双方真实 `/review-v2/file`，不是根据用户描述推测。

| rule_id | element_key | final status | canonical fact key/value | evidence_id | clause_id | 原文坐标 | polarity | Gate 原因 |
|---|---|---|---|---|---|---|---|---|
| TC-09-01 | core_contract_arrangement | COVERED | null / null | SRC-72bb798cf502821cb89a | C0004 | 文档 [221,268)，条款 [0,47) | AFFIRMATIVE；CONTEXTUAL | 原文已核验，但没有与该 element 及 source-clause ownership 一致的 DIRECT 绑定 |
| TC-09-01 | PRIMARY_EVIDENCE | COVERED | null / null | SRC-72bb798cf502821cb89a | C0004 | 文档 [221,268)，条款 [0,47) | AFFIRMATIVE；CONTEXTUAL | 报告首条证据不能直接支持该规则的任一 COVERED element |
| TC-09-04 | technical_service_remuneration | COVERED | null / null | SRC-da3797658b20e5975099 | C0008 | 文档 [834,865)，条款 [0,31) | AFFIRMATIVE；CONTEXTUAL | 原文已核验，但没有与该 element 及 source-clause ownership 一致的 DIRECT 绑定 |
| TC-09-04 | PRIMARY_EVIDENCE | COVERED | null / null | SRC-da3797658b20e5975099 | C0008 | 文档 [834,865)，条款 [0,31) | AFFIRMATIVE；CONTEXTUAL | 报告首条证据不能直接支持该规则的任一 COVERED element |

## 原始 quote

C0004（前两项共用）：

> 第一条 服务内容
> 乙方向甲方提供以下技术服务：
> 对甲方现有动力电池模组装配线进行运行状态检测；

C0008（后两项共用）：

> 第五条 服务费用
> 本合同技术服务费总额为人民币96万元，含税。

## 公共根因

1. 服务内容和服务费用使用了旧的事项级覆盖判定，但没有在冻结事实库和最终 element 间登记同一 canonical key。检索拿到了真实原文，却只能成为 CONTEXTUAL evidence；主证据随之不合格。
2. 部分服务规则仍独立使用关键词布尔判断，绕开公共命题作用域。“未约定”后的并列控制权被错误当成肯定事实；列表中的独立开发、返还删除、服务活动等则漏映射。
3. 缺失子项和已覆盖子项没有统一投影到最终父级叙事；部分覆盖更新原文后也可能遗留空的证据 ID。
4. 数据风险检测和叙事没有共同保留行为主体、数据对象、用途及条件，导致匿名化统计数据与原始生产数据混淆，单一用途也可能被模板扩写。

## 公共修复

- 用同一组原子事实定义注册事实库、解析要素和生成精确证据；最终投影后刷新消费端的事实库视图，事实库本身不再被中途改写。
- 并列命题使用公共 polarity / scope 识别；缺失声明不能产生 COVERED，已有义务也不会被邻近缺失子项覆盖。
- 保留各 component 的独立状态、原文及证据 ID；部分基础处理责任只能证明 PARTIAL 抗辩控制，不能证明完整控制权。
- 数据许可同时绑定 actor、owner、object、purpose、condition；叙事和 evidence 使用同一原文。
- Gate 前增加独立核验：COVERED 必须有对应的直接原文，MISSING 不能同时存在直接正向事实，PARTIAL 必须有真实已覆盖部分，父级叙事必须与最终状态一致。
- 保持原有 Gate 阻断要求、分类及 provider 行为；不修改旧测试预期，不增加 fallback。

最终真实接口和测试数字以 `acceptance.json` 为准；未完成的测试不在此预先声明通过。
