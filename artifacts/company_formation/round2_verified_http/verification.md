# 股东合作协议第二轮修复验收

本轮保持分类器不变，修复事实判断、通用规则组合、引用核验、要素分类和报告状态一致性。

## 根因

- 治理完整性只检索表决相关正向内容，未将不设机关、单方最终决定作为治理规则的反向事实。
- 既有 CF-02 将实际履行凭证与应约定的合同要素混合，导致未来出资被要求补实缴证明。
- 设立公司清单只拼接生效、通知、争议三项通用规则，缺少通用救济和文件完整性审查。
- 引用条号没有通过目标条款、层级和主题核验；质量门禁又将“引用层级不存在”误当“没有风险”的反向叙事。

## 生产链路与修改文件

- [company_governance_facts.py](F:/ai/Sage/backend/review_v2/company_governance_facts.py)：多人/单人公司、未来变更条件、治理机关冲突和融资约束；实缴声明与外部凭证分离。
- [contract_references.py](F:/ai/Sage/backend/review_v2/contract_references.py)：通用条款/附件/相对引用解析；本地版本化法条主题校验；不确定指向和法规转人工核验。
- [equity_common_checklist.py](F:/ai/Sage/backend/review_v2/equity_common_checklist.py)：恢复解除终止、一般违约、违约金损失衔接、维权费用、附件和顺位；不可抗力按事实触发。
- [company_formation_checklist.py](F:/ai/Sage/backend/review_v2/company_formation_checklist.py)：新增 CF-15，CF-02 不再建议签署前补实缴凭证，使用完整通用组合。
- [employment_facts.py](F:/ai/Sage/backend/review_v2/employment_facts.py)：在统一要素解析入口动态分离外部核验要求及引用要素。
- [priority_contract_review.py](F:/ai/Sage/backend/review_v2/priority_contract_review.py)：初始判定与后置核验共用事实；治理上位规则反向证据优先；记录引用目标审计。
- [contract_registry.py](F:/ai/Sage/backend/review_v2/contract_registry.py)：组装 CF 专项和通用规则；普通股东协议也执行公司机关检查。
- [domain_selection.py](F:/ai/Sage/backend/review_v2/domain_selection.py)：将两项通用引用规则纳入允许的通用规则范围，不开放买卖专项。
- [engine.py](F:/ai/Sage/backend/review_v2/engine.py)：所有类型在正式判定前加载真实引用规则；通用后置核验；纠正叙事门禁中“对象不存在”与“风险不存在”的混淆；记录实际规则数量。
- [review_v2.py](F:/ai/Sage/backend/routers/review_v2.py)：新增模块纳入运行源码一致性保护，保留旧代码拒绝执行机制。
- [test_shareholder_governance_references.py](F:/ai/Sage/backend/tests/test_shareholder_governance_references.py)：新增 22 个参数化/生产回归案例，包括用户要求的 9 类及条件一人公司、跨领域买卖引用审查、嵌套层级与附件待核验。
- [test_review_v2_contract_registry.py](F:/ai/Sage/backend/tests/test_review_v2_contract_registry.py)：同步注册表中工作区已有的 operating_cooperation 清单断言；未改变其生产逻辑。

## 自动化测试

- 主回归：167 passed，8 warnings，106.91s。涵盖分类、SALES 条件适用、买卖原文上传、增资扩股、股权转让、股东合作及新增治理引用用例。
- 股权专项：28 passed，75 deselected，5 warnings，54.85s。
- 本轮最终执行合计 195 项通过，其中新增 22 个案例；未执行全仓所有测试。
- 早期运行中的 503 来自并发源码修改，未禁用或绕过旧代码门禁。重启后上述最终运行全部通过。

## 同一完整合同生产复测

- 文件：test_data/83 投资协议.docx，原文件 SHA256：8bdcbca80dba56ef998d4511d939bbca4ce4bf514895117042f33a1e3e502f12。
- 全文：3924 字；规范化 SHA256：64c9da2ab188f47cb00625c2b9142d3bbad20e5fb9bc04084e36c4bb824311f8。未改写/缩短原文。
- 实际页面 /review-v2/file 审查 ID：CR-20260909-072659-E55613；PID 21704；CURRENT；REPORT_READY。
- 另保存真实模型 multipart 生产处理器及响应模型复测结果（隔离测试认证），见 result.json / summary.json / report.md。
- contract_type=shareholders；scenario=股东合作协议；role=equity_party（股权协议当事人）。
- 总规则数26：CF专项15、通用11（其中不可抗力不适用）；买卖专项0。
- 风险主题21：重大9、中等6、低6。覆盖状态：通过4、部分覆盖6、风险条款9、缺失6、不适用1。

- CF-15-01 风险条款：发现多股东有限责任公司不设股东会的直接约定，存在效力或履行风险，需结合适用法律及具体事实核验。
- CF-05-01 风险条款：发现影响本项安排准确性或可执行性的直接约定。多股东有限责任公司约定不设股东会，混淆公司权力机关与会议形式。全体股东书面一致决定可以不召开会议，不等于不设股东会；另有例会不能消除该矛盾。；重大事项共同决策与单方最终决定或跳过协商的授权相冲突，不能仅因存在表决条款认定治理安排全部通过。
- CF-07-01 风险条款：发现影响本项安排准确性或可执行性的直接约定。持股比例锁定并限制股权融资，未跟投时可能限制融资选择并形成融资僵局。另有全体股东同意的调整出口，但仍依赖一致同意，建议明确无法一致时的融资及退出路径。
- COMMON-21-01 风险条款：发现影响本项安排准确性或可执行性的直接约定。本协议第九条第2款：被引用条款存在，但指定款/项层级不存在。引用目的为违约责任，但目标条款“九、送达方式及送达地址”内容属于其他事项，与引用语义不对应。
- COMMON-22-01 风险条款：发现影响本项安排准确性或可执行性的直接约定。《公司法》第三十八条：所引公司法第38条在2023修订版规定分公司设立登记，与此处股东重大事项职权不对应，存在旧模板条号或错引风险；应核对现行职权条款及合同适用时间。
- CF-02-01 部分覆盖：未找到明确约定：未按期出资的补足及违约责任。

已实缴但没有外部材料的新增用例保留 PENDING_VERIFICATION 评估，不生成“实缴凭证缺失”的合同修改要素。客户资源出资、非货币资产、个人临时账户、单方决定、僵局、利润留存、资本返还、转让效力、章程衔接等原有正确风险均保留。

## 核验边界

法条库当前只自动确认已维护的公司法版本主题，其他法律和条文转人工复核，不声称完成所有法规全文比对。相对引用或外部附件无法可靠定位时保留待核验，不推定文件不存在。

法源：[全国人大公布的公司法2023修订版](https://www.npc.gov.cn/npc/c2/c30834/202312/t20231229_433999.html)，第38条为分公司设立登记，第58—60条区分股东会组成、书面一致决定及一个股东的公司。
