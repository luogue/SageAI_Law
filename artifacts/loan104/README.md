# 企业借款语义与证据绑定回归

固定样本：test_data/104 企业借款.docx，未修改。
SHA256：751a007d57090d24fa73e341f7f3ab2fcb8da546d26ca372a8050c88b15454ef
生产入口：POST /review-v2/file（原始DOCX，use_llm=false）。
任务：CR-20260910-145221-3B0B10

## 根因与修改文件

- backend/review_v2/loan_semantics.py：共享命题解析；引用利率的乘法/百分比/上浮算子，付款分配顺序，经营用途正负极性。
- backend/review_v2/loan_facts.py：候选检索和最终supports共用概念；去掉冲抵的窄关键词前置筛选；选择正向原句，合并相同证据支持的多个要素。
- backend/review_v2/loan_costs.py：倍率复用正常利率及其来源证据；未知或冲突的引用利率不伪造具体值，不把150%当独立年利率。
- backend/review_v2/clause_parser.py：冒号后的短列举保持连续上下文，不误拆成无主句的独立章节；真正的新章节仍分开。
- backend/tests/test_loan104_semantic_binding.py：29项正反例，覆盖不同倍率、比例、上浮、冲抵表达、用途极性、顺序交换、源文本完整性及固定原合同。

## 生产结果

### L-02-04 通过

- SRC-b11ec85ddf0fb1d09b1f：本合同借款用于乙方采购仓储设备、支付供应商货款及补充日常经营流动资金。
- SRC-cfd6e0b52ddaeae3dd07：鉴于乙方因日常经营及采购业务存在阶段性流动资金需求，甲方同意以自有资金向乙方提供借款。

### L-05-02 通过

- SRC-1a439f131539d5b52af8：乙方未按照约定期限偿还借款本金的，自逾期之日起，对逾期本金按照本合同正常借款利率的1.5倍计收逾期利息，直至实际清偿之日。

### L-06-03 通过

- SRC-b25a36c938e830d9ed22：乙方付款时未特别注明款项性质的，依次用于清偿实现债权费用、违约金及其他费用、利息、本金。

仅L-05-02与L-06-03的coverage状态改变，其余规则状态保持。L-02-04保持PASS，仅纠正证据极性和排序。
质量门：REPORT_READY，failures=[]。
完整日志：tests-final.txt；生产报告JSON：production.json；逐项证据：verified-diff.json。