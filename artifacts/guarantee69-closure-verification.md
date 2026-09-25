# 保证合同收口验证

实际接口：POST /review-v2/file，HTTP 200；worker PID=17796；trace=CR-20260908-153652-98E324。
固定样本：test_data/69 保证合同.docx；SHA256=dec08149bef6064a8217056ac4ce81ea3b240fa4e065d8478f95fb2a0bd5da6c，文件未修改。
完整审查使用 use_llm=false，真实文件解析、规则、证据、聚合和质量门路径全部执行。原48项保留，新增 GUA-13-01 征信查询与报送资格，总计49项。

## 统一事实

```json
{
  "guarantee_party_type": "NATURAL_PERSON",
  "guarantor_count": 1,
  "guarantee_type": "JOINT",
  "fixed_principal_amount": 6000000.0,
  "main_contract_status": "UNMATURED",
  "maturity_date": "2027-09-07",
  "guarantee_scope_type": "FULL",
  "unilateral_guarantee_document_detected": false,
  "transfer_document_detected": false,
  "attachment_inventory": {
    "references": [
      "借款协议书"
    ],
    "provided_documents": [],
    "required": true,
    "status": "PENDING_VERIFICATION"
  },
  "signature_party_type_consistency": "MISMATCH",
  "credit_reporting_eligibility": {
    "status": "PENDING_VERIFICATION",
    "authorization_text": "FOUND",
    "purpose_text": "FOUND",
    "query_access_qualification": "UNVERIFIED",
    "reporting_institution_qualification": "UNVERIFIED",
    "authorization_confers_access": false
  }
}
```

UNMATURED 表示按正文约定、审查日期尚未到期，不是对实际履行或债务真实性作外部确认。

## 逐规则修复前后

|规则|标题|修复前|修复后|最终行动|
|---|---|---|---|---|
|GUA-01-01|保证人身份信息|部分覆盖|风险条款|B_PRACTICAL|
|GUA-01-02|机关法人保证限制|通过|不适用|NOT_APPLICABLE|
|GUA-01-03|公益非营利主体保证限制|通过|不适用|NOT_APPLICABLE|
|GUA-01-04|公司保证授权基础|不适用|不适用|NOT_APPLICABLE|
|GUA-02-01|书面保证合同|通过|通过|NONE|
|GUA-02-02|单方保证文件纳入|缺失|不适用|NOT_APPLICABLE|
|GUA-02-03|主合同指向明确|通过|通过|NONE|
|GUA-02-04|保证意思表示真实|通过|通过|NONE|
|GUA-03-01|主合同效力基础|法律提示|法律提示|NONE|
|GUA-03-02|独立保证条款|通过|通过|NONE|
|GUA-03-03|保证无效后的过错责任|缺失|法律提示|NONE|
|GUA-03-04|主债务时效状态披露|通过|不适用|NOT_APPLICABLE|
|GUA-04-01|保证方式明确|通过|通过|NONE|
|GUA-04-02|连带责任保证明确表述|通过|通过|NONE|
|GUA-04-03|一般保证规则提示|不适用|不适用|NOT_APPLICABLE|
|GUA-04-04|保证方式未明确|不适用|不适用|NOT_APPLICABLE|
|GUA-05-01|保证期间明确|通过|通过|NONE|
|GUA-05-02|保证至本息还清|通过|通过|NONE|
|GUA-05-03|保证期间早于或等于主债务期限|通过|通过|NONE|
|GUA-05-04|保证期间不中止不中断|通过|法律提示|NONE|
|GUA-06-01|先诉抗辩权提示|不适用|不适用|NOT_APPLICABLE|
|GUA-06-02|先诉抗辩权例外|不适用|不适用|NOT_APPLICABLE|
|GUA-06-03|书面放弃先诉抗辩权|不适用|不适用|NOT_APPLICABLE|
|GUA-06-04|口头放弃先诉抗辩权|不适用|不适用|NOT_APPLICABLE|
|GUA-07-01|保证范围明确|通过|通过|NONE|
|GUA-07-02|主债权金额上限|通过|通过|NONE|
|GUA-07-03|实现债权费用|通过|通过|NONE|
|GUA-07-04|保证范围限制列明|缺失|不适用|NOT_APPLICABLE|
|GUA-08-01|主合同变更需保证人同意|通过|通过|NONE|
|GUA-08-02|减轻债务变更|通过|通过|NONE|
|GUA-08-03|展期需保证人确认|通过|通过|NONE|
|GUA-08-04|变更通知和留痕|通过|通过|NONE|
|GUA-09-01|债权转让通知保证人|通过|通过|NONE|
|GUA-09-02|债务转移需保证人书面同意|通过|通过|NONE|
|GUA-09-03|债权转让不加重保证责任|通过|通过|NONE|
|GUA-09-04|转让转移文件附件|通过|不适用|NOT_APPLICABLE|
|GUA-10-01|共同保证人识别|不适用|不适用|NOT_APPLICABLE|
|GUA-10-02|保证份额约定|不适用|不适用|NOT_APPLICABLE|
|GUA-10-03|共同保证内部追偿|不适用|不适用|NOT_APPLICABLE|
|GUA-10-04|对部分保证人行权|不适用|不适用|NOT_APPLICABLE|
|GUA-11-01|保证人追偿权|通过|通过|NONE|
|GUA-11-02|保证人代位权|通过|法律提示|NONE|
|GUA-11-03|追偿资料移交|缺失|缺失|C_OPTIMIZATION|
|GUA-11-04|不得损害债权人利益|缺失|通过|NONE|
|GUA-12-01|公司对外担保决议|不适用|不适用|NOT_APPLICABLE|
|GUA-12-02|最高额保证期间|不适用|不适用|NOT_APPLICABLE|
|GUA-12-03|期间届满后签字效力|不适用|不适用|NOT_APPLICABLE|
|GUA-12-04|保证附件完整性|通过|待核验|NONE|
|GUA-13-01|征信查询与报送资格|新增|待核验|NONE|

## GUA-11-04 原文绑定

- 第七条（六） / C0061 / MAIN_CONTRACT
但如果债务人同时面临保证人的追偿和债权人在主合同项下的任何支付要求，保证人同意债务人优先偿付其对债权人的债务。

## 签署错误与资格核验分离

保证人主体已明确，但签署栏使用了与该主体类型不一致的字段，应修改签署模板。
将签署栏改为“乙方（保证人）：陈昊（签字/捺印）”，删除法人专用的公章、法定代表人字段。
签署错误为低风险、B_PRACTICAL / SHOULD_CHANGE；不产生人工复核。实际缺失的引用附件文件及征信查询/报送机构资格分别待核验，均不被正文承诺替代。

## 最终统计

|覆盖状态|修复前|修复后|
|---|---:|---:|
|通过|27|21|
|部分覆盖|1|0|
|缺失|5|1|
|不适用|14|20|
|法律提示|1|4|
|风险条款|0|1|
|待核验|0|2|

人工复核（独立标注，不与覆盖状态重复相加）：1 → 2。
风险主题：6 → 2。
真正修改数：0 → 1。
行动统计：{'major_risk': 0, 'medium_risk': 0, 'low_risk': 2, 'priority_action': 0, 'recommended_action': 1, 'optional_action': 1, 'manual_review': 2}。
总体可签署性：建议修改后签署。
release_quality_gate=REPORT_READY；failures=[]。
N/A 已断言不进入风险、修改建议或人工核验来源。既有正确主体门控、固定本金、GUA-08 与 GUA-09-01 均未回退。

## 根因与实现位置

- guarantee_scenarios.py：统一主体类型、债务到期、独立文件、限制意图、实际附件目录，前置门控。
- guarantee_closure.py：法定规则与直接冲突分离；追偿语义证据；签署模板风险；附件及征信外部资格核验。
- guarantee_party_facts.py / guarantee_prerequisites.py / guarantee_contract_facts.py：统一事实消费者，移除旧的签署模板人工核验分支。
- guarantee_contract_checklist.py：场景适用条件、新增征信检查点。
- clause_parser.py / lease_semantics.py：附件内条款与主体段落保留附件来源；语义证据支持可声明必要文档范围。
- engine.py：接入收口；有实证、可修正的文档错误与可选优化区分，按最终发现重新聚合签署结论。
- routers/review_v2.py：新模块纳入运行时来源版本校验。

## 测试

本轮新增34项保证收口回归；保证专项总计87项全部通过。测试数据原文件未改；仅随新增征信规则更新规则总数断言，并按用户要求将全范围保证的限制规则及签署分类断言更新为新语义。
额外签署决策4项通过，额外附件/解析检查4项通过。跨类型检查尚有4项失败：买卖聚合/适用性/人工核验3项，技术服务条款定位1项。隔离本轮新增决策及附件继承分支后的输出一致，详见 guarantee-closure-sale-isolation.json 与 guarantee-closure-parser-isolation.json；本轮未修改这些其他合同规则。
已知环境告警：TaskDB 启动恢复报 SQLite database disk image is malformed；本次同步上传审查成功，未在本轮修数据库。

## 核验法律来源

[最高人民法院公布的民法典](https://www.court.gov.cn/zixun/xiangqing/233181.html)：第682、692、696、700条。法定规则未复述不作为合同缺陷；当事人另行约定或实际冲突仍单独判断。
[市场监管总局公布的征信业管理条例](https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/bgt/art/2023/art_f06d5be45fcf464abe3fbdb9b2b3b37c.html)：第18、28、29条。授权、用途与查询接入/信贷信息报送资格分离。