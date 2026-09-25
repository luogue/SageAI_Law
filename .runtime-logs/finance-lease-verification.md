# 融资租赁通用引擎回归记录

2026-09-07。输入：test_data/52 融资租赁合同.docx。

## 页面实际重跑

启用大模型复核，后端进程22928，runtime_source_drift=CURRENT。
发布校验REPORT_READY，failures=[]。页面已显示新结果。

45条：24通过、2待核验、6法律提示、2风险条款、6缺失、3不适用、2部分覆盖。
顶部统计：2重大风险、1中等风险、4低风险；2优先处理、2建议处理、3可选优化；2待核验。

FL-07-03、FL-08-01、FL-09-01、FL-12-01/02/03、FL-15-01均通过，发布要素均为COVERED。
FL-04-01、FL-04-03、FL-09-03通过并重新绑定主体、使用付租、保险维修证据。
FL-03-03改为法律提示：期满返还证据不能证明合同无效后的归属。
FL-03-01/02均待核验，文本结构与外部真实性分开。
FL-14-01/02/03均不适用。
FL-10-01/02共同使用fl_remedy_election不利事实，合并为一个核心风险。
FL-10-03、FL-13-01/02/03清算估值事项合并为一个风险主题。
《担保法》作为过时引用独立提示，建议更新为民法典及现行担保制度规定。

附件额外校验：租金支付表不能证明登记、保险凭证；交付验收文件不能证明技术规格资料。FL-15-02/03输出部分覆盖并指明缺少的要素。

## 自动回归

120 passed：test_finance_lease_shared_facts.py、test_finance_lease_review_checklist.py、test_finance_lease.py、test_loan_cost_combinations.py、test_loan_applicability_and_consistency.py。
覆盖主体别名反转、直租/回租、供货方维修与承租人维修区分、期满返还与无效返还区分、双重救济/明确择一、外部虚构线索、排除拒收权、多部废止法律聚合、附件要素分离及45条报告闭环。
git diff --check通过。

确定性重跑完整JSON：finance-lease-fixed.json。其余未纳入本轮共享语义要素的审查项仍可由大模型复核改变；确定性运行与页面运行的全量数量并不完全相同。上述页面数量为最后一次实际运行结果。

## 法律来源

- 民法典（第735—760条及第1260条）：https://www.court.gov.cn/zixun/xiangqing/233181.html
- 最高人民法院关于适用民法典有关担保制度的解释：https://www.court.gov.cn/fabu/xiangqing/282721.html
