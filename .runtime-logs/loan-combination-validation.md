# 借款合同组合成本及外部事实边界验收

范围：通用规则引擎修复，当前借款合同48条全量确定性重跑。

覆盖：26通过 / 15不适用 / 2部分覆盖 / 5缺失。7条问题规则聚合为5个主题：1个中风险（建议修改），4个低风险（可选优化）。

月利率0.8%简单年化9.6%，逾期日利率0.02%按365天简单年化7.3%；若同期间同本金叠加，潜在年化估算16.9%。这不是已确认实际收费或法律超限结论；合同成立日期及对应一年期LPR仍需核验。

L-04-02/L-05-02：PARTIAL，共享融资成本证据和组合判断；L-11-02/L-12-04：合并为债务人催收证据保存主题；保证期间行权证据独立保留。

L-02-01/L-02-02/L-02-03：合同文本未发现风险线索；external_fact_status=NOT_VERIFIED，不确认外部事实不存在。

发布门控：REPORT_READY；证据、摘要与明细、计数一致性检查通过。

回归：192项借款及报告一致性相关测试通过；扩展买卖合同测试中test_full_production_recall失败，原因RENDERED_COVERAGE_CLOSURE，单独复现，不混入借款验收通过数。

组合上限依据：[最高人民法院2020年12月修订决定（民间借贷第28、29条）](https://www.court.gov.cn/zixun/xiangqing/282621.html)。

|规则|适用性|覆盖|严重度|行动优先级|证据条数|
|---|---|---|---|---|---|
|L-01-01 借款合同性质|APPLICABLE|通过|NONE|NONE|4|
|L-01-02 金融借款与民间借贷区分|APPLICABLE|通过|NONE|NONE|4|
|L-01-03 以买卖担保借款识别|NOT_APPLICABLE|不适用|NONE|NOT_APPLICABLE|0|
|L-01-04 自然人间借款成立时间|APPLICABLE|通过|NONE|NONE|1|
|L-02-01 套取金融机构贷款转贷|APPLICABLE|通过|NONE|NONE|0|
|L-02-02 职业放贷人风险|APPLICABLE|通过|NONE|NONE|0|
|L-02-03 明知违法用途出借|APPLICABLE|通过|NONE|NONE|0|
|L-02-04 企业间借款经营需要|NOT_APPLICABLE|不适用|NONE|NOT_APPLICABLE|0|
|L-03-01 借款本金金额|APPLICABLE|通过|NONE|NONE|4|
|L-03-02 实际放款和到账凭证|APPLICABLE|通过|NONE|NONE|2|
|L-03-03 砍头息禁止|APPLICABLE|通过|NONE|NONE|0|
|L-03-04 债权凭证载明债权人|APPLICABLE|通过|NONE|NONE|3|
|L-04-01 借期内利率|APPLICABLE|通过|NONE|NONE|2|
|L-04-02 民间借贷LPR四倍上限|APPLICABLE|部分覆盖|MEDIUM|B_PRACTICAL|5|
|L-04-03 金融借款利率合规|NOT_APPLICABLE|不适用|NONE|NOT_APPLICABLE|0|
|L-04-04 变相高息费用|APPLICABLE|通过|NONE|NONE|0|
|L-05-01 利息计算基数和期间|APPLICABLE|通过|NONE|NONE|1|
|L-05-02 逾期利息|APPLICABLE|部分覆盖|MEDIUM|B_PRACTICAL|5|
|L-05-03 复利限制|NOT_APPLICABLE|不适用|NONE|NOT_APPLICABLE|0|
|L-05-04 未约定利息处理|NOT_APPLICABLE|不适用|NONE|NOT_APPLICABLE|0|
|L-06-01 还款期限|APPLICABLE|通过|NONE|NONE|3|
|L-06-02 还款方式和账户|APPLICABLE|通过|NONE|NONE|4|
|L-06-03 还款冲抵顺序|APPLICABLE|缺失|LOW|C_OPTIMIZATION|0|
|L-06-04 还款确认和收据|APPLICABLE|缺失|LOW|C_OPTIMIZATION|0|
|L-07-01 提前还款权|NOT_APPLICABLE|不适用|NONE|NOT_APPLICABLE|0|
|L-07-02 提前还款利息计算|NOT_APPLICABLE|不适用|NONE|NOT_APPLICABLE|0|
|L-07-03 不合理提前还款违约金|NOT_APPLICABLE|不适用|NONE|NOT_APPLICABLE|0|
|L-07-04 提前还款通知程序|NOT_APPLICABLE|不适用|NONE|NOT_APPLICABLE|0|
|L-08-01 展期申请和同意|NOT_APPLICABLE|不适用|NONE|NOT_APPLICABLE|0|
|L-08-02 展期利率和费用|NOT_APPLICABLE|不适用|NONE|NOT_APPLICABLE|0|
|L-08-03 展期需保证人同意|NOT_APPLICABLE|不适用|NONE|NOT_APPLICABLE|0|
|L-08-04 未获同意仍按原期限履行|NOT_APPLICABLE|不适用|NONE|NOT_APPLICABLE|0|
|L-09-01 保证方式|APPLICABLE|通过|NONE|NONE|4|
|L-09-02 保证期间|APPLICABLE|通过|NONE|NONE|1|
|L-09-03 保证范围|APPLICABLE|通过|NONE|NONE|4|
|L-09-04 借新还旧保证人知情|NOT_APPLICABLE|不适用|NONE|NOT_APPLICABLE|0|
|L-10-01 夫妻共同意思表示|APPLICABLE|通过|NONE|NONE|1|
|L-10-02 家庭日常生活需要|NOT_APPLICABLE|不适用|NONE|NOT_APPLICABLE|0|
|L-10-03 共同经营用途|APPLICABLE|通过|NONE|NONE|4|
|L-10-04 超出家用的大额借款证据|APPLICABLE|通过|NONE|NONE|1|
|L-11-01 诉讼时效起算|APPLICABLE|通过|NONE|NONE|3|
|L-11-02 时效中断留痕|APPLICABLE|缺失|LOW|C_OPTIMIZATION|0|
|L-11-03 催收和送达方式|APPLICABLE|通过|NONE|NONE|1|
|L-11-04 保证期间内行权留痕|APPLICABLE|缺失|LOW|C_OPTIMIZATION|0|
|L-12-01 借据收据欠条附件|APPLICABLE|通过|NONE|NONE|2|
|L-12-02 转账和放款凭证|APPLICABLE|通过|NONE|NONE|2|
|L-12-03 保证和担保附件|APPLICABLE|通过|NONE|NONE|4|
|L-12-04 催收和还款记录附件|APPLICABLE|缺失|LOW|C_OPTIMIZATION|0|

## 风险主题

- loan_overdue_combined_cost：L-04-02, L-05-02；MEDIUM
- loan_repayment_offset_order：L-06-03；LOW
- loan_repayment_receipt_confirmation：L-06-04；LOW
- loan_collection_evidence_preservation：L-11-02, L-12-04；LOW
- loan_guarantor_collection_within_period：L-11-04；LOW

最终断言：明确合计限额仍不自动消除计息时间范围歧义；新增反例通过。

## 实际页面最终验收

最终使用确定性48条规则重跑，已在当前页面显示报告。进程21912，runtime_source_drift=CURRENT，changed_dependencies=[]，release_quality_gate=REPORT_READY，failures=[]。页面计数26/15/2/5与离线全量结果一致，核心摘要5个主题。

此前语义复核已得到相同核心计数；最后一轮语义请求被审查期间另一次本地后端重启中断。最终页面明确显示未启用大模型语义复核。
