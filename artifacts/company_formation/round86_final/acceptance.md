# 股东合作协议第86号样本修复验收

最终状态：PASSED；真实页面及multipart生产处理入口均REPORT_READY。原文件未修改。

## 实际四个违规与根因

修改前真实违规ID是CF-11-01、CF-12-01、CF-13-01、CF-14-01；均为NOT_APPLICABLE_HAS_GAP_NARRATIVE，不是猜测的CF-03/04/05/12。四项实际applicability均NOT_APPLICABLE，门禁expected_status也为NOT_APPLICABLE，polarity均NEGATIVE_CLAUSE_CHECK；证据及evidence_id为空。适用条件和理由含“合同缺失”，与不适用叙述契约冲突。已统一修正条件型检查的非触发状态说明，未放宽门禁。完整修改前字段见../round86_before/violations.json。

同时独立修复：CF-03/04使用局部关键词触发而遗漏交易结构与收款主体；CF-12仅覆盖最终决定/直接决定而遗漏否决权、保留事项单方审批；CF-05关键词证据未区别权利保障与查阅审批限制。

## 生产链修改

transaction_facts识别财产作价出资、自然人认购款接收、单方保留事项、查阅条件及回购主体；同一事实用于applicability、adverse evidence和独立source assertion。保护型要素标记polarity_policy；corpus_facts生成四类极性元数据，supports重新核验原文，避免synthesis伪装正向。

SEARCH_AUDIT和coverage共用同一requirements；新增日期缴足、通知后终止、章程不一致以协议为准等语义方向。正文源证据独立保存在source_requirement_facts，最终NOT_FOUND或NOT_APPLICABLE与源事实冲突时BLOCKED。多句直接不利证据按原句绑定，避免完整段落正则无法匹配逐句检索而产生假NOT_FOUND。

consistency比较同一股权表比例/认缴总额、签约主体与股东、受基础租赁约束的期限；按付款主体裁剪公司返还资本要素；利润费用豁免凭证及责任限制进入不利条款判断。未修改主分类器或大范围路由。

## 修改文件

- backend/review_v2/shareholder_transaction_facts.py
- backend/review_v2/priority_contract_review.py
- backend/review_v2/company_formation_checklist.py
- backend/review_v2/equity_common_checklist.py
- backend/review_v2/employment_facts.py
- backend/review_v2/lease_semantics.py
- backend/routers/review_v2.py
- backend/tests/test_shareholder_transaction_semantics.py
- backend/tests/test_adverse_theme_projection.py

## 测试

新增23个参数化用例，覆盖七类非货币权益、个人账户同义表达、控制权、四种知情权极性、反例、完整multipart入口及三种故意破坏门禁测试。回归282项+股权专项28项=310项通过；最终代码另重复36项全部通过。未宣称全仓库测试通过。旧83号聚合测试的角色断言适配并行引入的合法shareholder立场，未修改分类/角色实现。

## 生产结果

contract_type=shareholders；scenario=股东合作协议；role=shareholder（股东，当前工作区共享立场解析结果）。

24规则；14规则级风险命中；13风险主题；重大/中等/低=4/5/4；优先/建议/可选=1/9/3。

真实浏览器请求CR-20260909-093809-9EBF7D；PID3528；runtime=CURRENT；REPORT_READY。

## 逐项断言

| 断言 | 结果 |
|---|---|
| 租赁权益作价出资适用 | PASS |
| 自然人账户收取认购款适用 | PASS |
| 单方重大事项权限适用 | PASS |
| 一票否决识别 | PASS |
| 单方借款担保处分识别 | PASS |
| 查账须甲方同意为限制性证据 | PASS |
| 股权比例合计110% | PASS |
| 认缴110万与注册资本100万冲突 | PASS |
| 非签约戊方持股 | PASS |
| 合作期限超过基础租赁期限 | PASS |
| 2035年缴付期限FOUND | PASS |
| 第十一条终止通知FOUND | PASS |
| 章程冲突条款FOUND | PASS |
| 甲方或第三方回购不作为公司返还资本 | PASS |
| 净利润按比例提取公关费用 | PASS |
| 免提供发票合同支出凭证 | PASS |
| 甲方自行支配 | PASS |
| 违约责任不对称 | PASS |
| restrictive证据不得单独满足保护要素 | PASS |
| 正文有事实但NOT_FOUND必须BLOCKED | PASS |
| 触发场景存在但NOT_APPLICABLE必须BLOCKED | PASS |
| 限制性证据伪装POSITIVE必须BLOCKED | PASS |
| 生产门禁通过 | PASS |
| 无买卖专项污染 | PASS |
| 原合同未修改 | PASS |