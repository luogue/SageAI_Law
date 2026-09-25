# 借款合同通用规则修复验收

验收对象：《49 借款合同.docx》。生产代码不依赖此文件名、当事人、金额或具体日期。

## 确定性引擎全量验收

- 全部48项：28项通过、15项不适用、5项缺失（均为低风险可选优化）。
- 优先处理0项，建议处理0项，可选优化5项，人工复核0项。
- release_quality_gate：REPORT_READY；LOAN_SHARED_FACT_CONSISTENCY：PASS。
- N/A不进入缺失、风险发现、风险主题或修改建议。
- L-06-01与L-11-01引用同一loan.maturity事实和相同证据ID。
- L-04-04仅接受实际融资收费证据，实现债权费用及一般违约金不会触发。
- 放款收据与还款确认凭证分别判定；签字页后的借条/收据纳入附件证据。
- 还款冲抵顺序使用民法典第561条法定默认保护；证据管理事项无具体风险时可选优化。

## 全部48项结果

| 规则 | 审查点 | Applicability | Coverage | Severity | Action |
|---|---|---|---|---|---|
| L-01-01 | 借款合同性质 | APPLICABLE | 通过 | NONE | NONE |
| L-01-02 | 金融借款与民间借贷区分 | APPLICABLE | 通过 | NONE | NONE |
| L-01-03 | 以买卖担保借款识别 | NOT_APPLICABLE | 不适用 | NONE | NOT_APPLICABLE |
| L-01-04 | 自然人间借款成立时间 | APPLICABLE | 通过 | NONE | NONE |
| L-02-01 | 套取金融机构贷款转贷 | APPLICABLE | 通过 | NONE | NONE |
| L-02-02 | 职业放贷人风险 | APPLICABLE | 通过 | NONE | NONE |
| L-02-03 | 明知违法用途出借 | APPLICABLE | 通过 | NONE | NONE |
| L-02-04 | 企业间借款经营需要 | NOT_APPLICABLE | 不适用 | NONE | NOT_APPLICABLE |
| L-03-01 | 借款本金金额 | APPLICABLE | 通过 | NONE | NONE |
| L-03-02 | 实际放款和到账凭证 | APPLICABLE | 通过 | NONE | NONE |
| L-03-03 | 砍头息禁止 | APPLICABLE | 通过 | NONE | NONE |
| L-03-04 | 债权凭证载明债权人 | APPLICABLE | 通过 | NONE | NONE |
| L-04-01 | 借期内利率 | APPLICABLE | 通过 | NONE | NONE |
| L-04-02 | 民间借贷LPR四倍上限 | APPLICABLE | 通过 | NONE | NONE |
| L-04-03 | 金融借款利率合规 | NOT_APPLICABLE | 不适用 | NONE | NOT_APPLICABLE |
| L-04-04 | 变相高息费用 | APPLICABLE | 通过 | NONE | NONE |
| L-05-01 | 利息计算基数和期间 | APPLICABLE | 通过 | NONE | NONE |
| L-05-02 | 逾期利息 | APPLICABLE | 通过 | NONE | NONE |
| L-05-03 | 复利限制 | NOT_APPLICABLE | 不适用 | NONE | NOT_APPLICABLE |
| L-05-04 | 未约定利息处理 | NOT_APPLICABLE | 不适用 | NONE | NOT_APPLICABLE |
| L-06-01 | 还款期限 | APPLICABLE | 通过 | NONE | NONE |
| L-06-02 | 还款方式和账户 | APPLICABLE | 通过 | NONE | NONE |
| L-06-03 | 还款冲抵顺序 | APPLICABLE | 缺失 | LOW | C_OPTIMIZATION |
| L-06-04 | 还款确认和收据 | APPLICABLE | 缺失 | LOW | C_OPTIMIZATION |
| L-07-01 | 提前还款权 | NOT_APPLICABLE | 不适用 | NONE | NOT_APPLICABLE |
| L-07-02 | 提前还款利息计算 | NOT_APPLICABLE | 不适用 | NONE | NOT_APPLICABLE |
| L-07-03 | 不合理提前还款违约金 | NOT_APPLICABLE | 不适用 | NONE | NOT_APPLICABLE |
| L-07-04 | 提前还款通知程序 | NOT_APPLICABLE | 不适用 | NONE | NOT_APPLICABLE |
| L-08-01 | 展期申请和同意 | NOT_APPLICABLE | 不适用 | NONE | NOT_APPLICABLE |
| L-08-02 | 展期利率和费用 | NOT_APPLICABLE | 不适用 | NONE | NOT_APPLICABLE |
| L-08-03 | 展期需保证人同意 | NOT_APPLICABLE | 不适用 | NONE | NOT_APPLICABLE |
| L-08-04 | 未获同意仍按原期限履行 | NOT_APPLICABLE | 不适用 | NONE | NOT_APPLICABLE |
| L-09-01 | 保证方式 | APPLICABLE | 通过 | NONE | NONE |
| L-09-02 | 保证期间 | APPLICABLE | 通过 | NONE | NONE |
| L-09-03 | 保证范围 | APPLICABLE | 通过 | NONE | NONE |
| L-09-04 | 借新还旧保证人知情 | NOT_APPLICABLE | 不适用 | NONE | NOT_APPLICABLE |
| L-10-01 | 夫妻共同意思表示 | APPLICABLE | 通过 | NONE | NONE |
| L-10-02 | 家庭日常生活需要 | NOT_APPLICABLE | 不适用 | NONE | NOT_APPLICABLE |
| L-10-03 | 共同经营用途 | APPLICABLE | 通过 | NONE | NONE |
| L-10-04 | 超出家用的大额借款证据 | APPLICABLE | 通过 | NONE | NONE |
| L-11-01 | 诉讼时效起算 | APPLICABLE | 通过 | NONE | NONE |
| L-11-02 | 时效中断留痕 | APPLICABLE | 缺失 | LOW | C_OPTIMIZATION |
| L-11-03 | 催收和送达方式 | APPLICABLE | 通过 | NONE | NONE |
| L-11-04 | 保证期间内行权留痕 | APPLICABLE | 缺失 | LOW | C_OPTIMIZATION |
| L-12-01 | 借据收据欠条附件 | APPLICABLE | 通过 | NONE | NONE |
| L-12-02 | 转账和放款凭证 | APPLICABLE | 通过 | NONE | NONE |
| L-12-03 | 保证和担保附件 | APPLICABLE | 通过 | NONE | NONE |
| L-12-04 | 催收和还款记录附件 | APPLICABLE | 缺失 | LOW | C_OPTIMIZATION |

## 回归验证

- 借款场景、语义、全量报告、原有借款裁判、共享报告一致性及买卖证据回归：199项通过。
- 扩展租赁架构测试另有1项失败（既有叙述证据绑定问题）；恢复旧附件识别规则后仍可复现，未改动该租赁逻辑。
- 借款专项覆盖主体不明、开户行误识别、否定/假设场景、融资与维权费用、放款与还款凭证、大模型覆盖冲突、时效风险升级、N/A计数及摘要一致性。

法定抵充顺序已核对[最高人民法院公布的民法典第561条](https://www.court.gov.cn/zixun/xiangqing/233181.html)。

完整机器结果：[loan-final-rule.json](loan-final-rule.json)。

## 真实页面复审

已重启本地8016端口后端，并在已登录的合同审查页面启用大模型复核完成实际文件审查。页面结果与规则验收一致：48项、28项通过、15项N/A、5项低风险可选优化，优先处理/建议处理/人工复核均为0；BLOCKED提示消失。核心风险摘要仅列出还款冲抵、还款确认、时效中断留痕、保证行权留痕、催收还款记录五项。

额外修复：最终建议层的英文ip匹配改为完整词匹配，避免receipt、ownership、relationship被误判为知识产权风险；真实ip/intellectual/专利侵权仍保留原有升级规则。
