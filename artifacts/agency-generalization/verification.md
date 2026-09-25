# 委托合同泛化回归记录

两个原始 DOCX 未改动。第三份为独立简洁商业委托协议，使用相同正式文件接口与同一判定器；use_llm=false，未 mock 或注入证据。

## 根因

1. 原语义模式把主体、动作、费用名称和词序绑定过紧；“委托费用”、修饰语插入和后置工作报告无法满足固定模式。
2. 未声明原子要素的规则仍使用 core_contract_arrangement 通用项，造成报销/利息混为一体，以及一般赔偿与越权赔偿混绑。
3. SEARCH_AUDIT 曾独立重建候选，丢失正式检索器解析的父条款条件；现记录 corpus_facts 的实际候选、过滤结果和接受证据。
4. 新关系模型按主体—行为—对象—后果组合匹配，并保留同句主语省略与有明确承接词的上下文证据。适用性、风险分级和测试 DOCX 均未改动。

## 三份生产回归

|样本|规则数|状态统计|任务|质量门禁|
|---|---:|---|---|---|
|A 77 委托合同.docx|43|{'通过': 31, '不适用': 11, '部分覆盖': 1}|CR-20260908-204535-7983A9|REPORT_READY|
|B 80 委托合同.docx|42|{'通过': 27, '不适用': 11, '部分覆盖': 2, '缺失': 2}|CR-20260908-204543-C66531|REPORT_READY|
|C 商业委托泛化回归.docx|42|{'通过': 22, '缺失': 7, '不适用': 13}|CR-20260908-204550-FC3013|REPORT_READY|

当前样本 worker PID：20796
当前样本 task_id：CR-20260908-204543-C66531

第一份 A-01-03 现为 PARTIAL：有协商合意，但没有独立明确的签约主体及手续合规声明。没有以相邻条款代替该要素。

## 当前样本要素与原文

### A-01-01 委托合同性质：通过

- mandate_relationship：COVERED / 受托人为委托人处理事务的关系

第一条 委托目的：
> 第一条 委托目的
> 为协助委托人开展华东地区工业自动化设备渠道合作伙伴筛选、背景调查、商务沟通及合作谈判准备工作，降低合作对象信用风险和履约风险，提高渠道拓展效率，委托人委托受托人按照本合同约定处理相关事务

### A-01-03 合同效力基础：通过

- mandate_voluntary_agreement：COVERED / 双方协商合意或理解合同含义
- mandate_lawful_formation：COVERED / 签约主体及必要手续的合规声明

第1项：
> 1、合同双方已相互提示就本合同各条款作全面、准确的理解，并应对方要求作了相应的说明，签约双方对本合同的含义认识一致

第2项：
> 2、合同双方均承诺自身符合法律对签约要求的强制性规定，并履行了必要的手续

### A-02-01 委托事务具体范围：通过

- mandate_affair_scope：COVERED / 具体列明受托处理的事务内容

第一条 委托目的：
> 第一条 委托目的
> 为协助委托人开展华东地区工业自动化设备渠道合作伙伴筛选、背景调查、商务沟通及合作谈判准备工作，降低合作对象信用风险和履约风险，提高渠道拓展效率，委托人委托受托人按照本合同约定处理相关事务

### A-03-03 不可归责未完成时相应报酬：通过

- mandate_proportional_remuneration：COVERED / 不可归责未完成的相应报酬

第六条（5）：
> （5）因不可归责于受托人的原因导致委托事务不能完成的，委托人仍应按照受托人已经实际完成的工作比例支付相应委托费用，并承担已经实际发生的必要费用

### A-04-02 垫付费用偿还和利息：部分覆盖

- mandate_expense_repayment：COVERED / 受托人处理事务费用的偿还或报销
- mandate_advance_interest：MISSING / 垫付费用的利息处理

第六条第2项：
> 2、其他费用的种类及分担方式
> 受托人为处理委托事务发生的必要差旅费、资料查询费、第三方公开信息查询费等合理费用，由委托人承担，但适用以下规则：

### A-07-03 越权代理责任：通过

- mandate_unauthorized_liability：COVERED / 超出委托授权造成损失的责任

第七条（6）：
> （6）受托人擅自超越委托权限，以委托人名义对外作出具有法律约束力的承诺。
> 出现第（3）、（4）、（5）、（6）项情形并造成委托人损失的，受托人还应赔偿委托人实际遭受的损失。

### A-12-01 双方任意解除权：通过

- mandate_mutual_exit：COVERED / 委托双方均可任意结束委托关系

第七条（1）：
> （1）根据法律规定，委托人和受托人均有权依法随时解除本合同

### A-12-02 任意解除赔偿范围：部分覆盖

- mandate_exit_loss_liability：COVERED / 因可归责解除造成损失时的赔偿责任
- mandate_exit_profit_scope：MISSING / 有偿委托解除赔偿涵盖履行利益

第七条（3）：
> （3）因解除时间不当或者其他可归责于解除方的原因给对方造成损失的，解除方应按照法律规定承担赔偿责任

### A-12-03 解除后的交接结算：通过

- mandate_exit_handover：COVERED / 终止解除后移交资料或工作文件
- mandate_exit_settlement：COVERED / 终止解除后费用或报酬结算

第七条（4）：
> （4）本合同解除后5个工作日内，受托人应向委托人提交截至解除日的工作报告，并完成文件、资料、财产及正在处理事项的交接

第七条（5）：
> （5）双方应在交接完成后10个工作日内对已完成工作、已支付委托费用及必要费用进行结算

### A-13-03 终止结果报告：通过

- mandate_final_report：COVERED / 终止解除时报告委托事务处理结果

第七条（4）：
> （4）本合同解除后5个工作日内，受托人应向委托人提交截至解除日的工作报告，并完成文件、资料、财产及正在处理事项的交接

第四条第7项：
> 7、受托人应在委托期限届满后5个工作日内提交《最终委托工作报告》及全部工作资料

## 验证边界

当前 A-04-02 缺少的是垫付利息安排；A-12-02 缺少的是明确的履行利益范围。A-06-02、A-06-03 保留 MISSING。
本轮语义要素在渲染前重新校验事实、要素状态、最终引用位置与原文，并对覆盖/NOT_FOUND冲突、无支持证据、错引和错位执行 BLOCKED。
专项测试见 ../agency80-final-tests.txt；扩展测试见 ../agency80-regression-final.txt。扩展测试未全绿，不将三份生产验收通过等同整个仓库回归通过。

## 修改文件

- [backend/review_v2/agency_facts.py](F:/ai/Sage/backend/review_v2/agency_facts.py)
- [backend/review_v2/semantic_relations.py](F:/ai/Sage/backend/review_v2/semantic_relations.py)
- [backend/review_v2/lease_semantics.py](F:/ai/Sage/backend/review_v2/lease_semantics.py)
- [backend/review_v2/semantic_consistency.py](F:/ai/Sage/backend/review_v2/semantic_consistency.py)
- [backend/review_v2/engine.py](F:/ai/Sage/backend/review_v2/engine.py)
- [backend/routers/review_v2.py](F:/ai/Sage/backend/routers/review_v2.py)
- [backend/tests/test_agency_generalization.py](F:/ai/Sage/backend/tests/test_agency_generalization.py)
- [scripts/run_agency_generalization.py](F:/ai/Sage/scripts/run_agency_generalization.py)