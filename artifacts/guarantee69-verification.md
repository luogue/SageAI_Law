# 保证合同修复与真实接口回归

固定文件：69 保证合同.docx；SHA256：dec08149bef6064a8217056ac4ce81ea3b240fa4e065d8478f95fb2a0bd5da6c（未修改）。
入口：POST http://127.0.0.1:8016/review-v2/file；use_llm=false；HTTP 200。
运行追踪：CR-20260908-145115-933C40；worker PID：13500。
修复前数据来自同文件的本地引擎基线，修复后来自实际 HTTP 接口；不是把历史报告中的表述当成本轮复现结果。

## 统一事实

```json
{
  "guarantee_party_type": "NATURAL_PERSON",
  "guarantor_count": 1,
  "guarantee_type": "JOINT",
  "amount_mode": "FIXED",
  "fixed_principal_amount": 6000000.0
}
```

## 全量规则对比

|规则|修复前覆盖状态|修复前元素状态|修复后覆盖状态|修复后元素状态|
|---|---|---|---|---|
|GUA-01-01|通过|COVERED|部分覆盖|COVERED, COVERED, MISSING|
|GUA-01-02|通过|MISSING|通过|MISSING|
|GUA-01-03|通过|MISSING|通过|MISSING|
|GUA-01-04|通过|UNCERTAIN|不适用|—|
|GUA-02-01|通过|COVERED|通过|COVERED|
|GUA-02-02|缺失|MISSING|缺失|MISSING|
|GUA-02-03|通过|COVERED|通过|COVERED|
|GUA-02-04|通过|UNCERTAIN|通过|UNCERTAIN|
|GUA-03-01|法律提示|MISSING|法律提示|MISSING|
|GUA-03-02|通过|MISSING|通过|MISSING|
|GUA-03-03|缺失|MISSING|缺失|MISSING|
|GUA-03-04|通过|UNCERTAIN|通过|UNCERTAIN|
|GUA-04-01|通过|UNCERTAIN|通过|UNCERTAIN|
|GUA-04-02|通过|UNCERTAIN|通过|UNCERTAIN|
|GUA-04-03|不适用|—|不适用|—|
|GUA-04-04|不适用|—|不适用|—|
|GUA-05-01|通过|UNCERTAIN|通过|UNCERTAIN|
|GUA-05-02|通过|MISSING|通过|MISSING|
|GUA-05-03|通过|MISSING|通过|MISSING|
|GUA-05-04|通过|UNCERTAIN|通过|UNCERTAIN|
|GUA-06-01|不适用|—|不适用|—|
|GUA-06-02|不适用|—|不适用|—|
|GUA-06-03|不适用|—|不适用|—|
|GUA-06-04|不适用|—|不适用|—|
|GUA-07-01|通过|COVERED|通过|COVERED|
|GUA-07-02|通过|UNCERTAIN|通过|COVERED|
|GUA-07-03|通过|MISSING|通过|MISSING|
|GUA-07-04|缺失|MISSING|缺失|MISSING|
|GUA-08-01|通过|UNCERTAIN|通过|COVERED|
|GUA-08-02|缺失|MISSING|通过|COVERED|
|GUA-08-03|通过|MISSING|通过|COVERED|
|GUA-08-04|通过|UNCERTAIN|通过|COVERED|
|GUA-09-01|通过|UNCERTAIN|通过|UNCERTAIN|
|GUA-09-02|通过|UNCERTAIN|通过|UNCERTAIN|
|GUA-09-03|通过|UNCERTAIN|通过|UNCERTAIN|
|GUA-09-04|通过|UNCERTAIN|通过|UNCERTAIN|
|GUA-10-01|缺失|MISSING|不适用|—|
|GUA-10-02|缺失|MISSING|不适用|—|
|GUA-10-03|通过|UNCERTAIN|不适用|—|
|GUA-10-04|缺失|MISSING|不适用|—|
|GUA-11-01|通过|COVERED|通过|COVERED|
|GUA-11-02|通过|UNCERTAIN|通过|UNCERTAIN|
|GUA-11-03|缺失|MISSING|缺失|MISSING|
|GUA-11-04|缺失|MISSING|缺失|MISSING|
|GUA-12-01|缺失|MISSING|不适用|—|
|GUA-12-02|不适用|—|不适用|—|
|GUA-12-03|不适用|—|不适用|—|
|GUA-12-04|通过|COVERED|通过|COVERED|

说明：GUA-07-02、GUA-08-01、GUA-08-03 的修复前顶层曾显示“通过”，但元素为 UNCERTAIN/MISSING、无有效绑定；本轮修复的是该矛盾和真实证据覆盖。

## GUA-08 全部命中证据

### GUA-08-01：通过

- canonical location：第九条第1项；chunk：C0085；document_type：MAIN_CONTRACT
- 原文：1、债权人与借款人对主合同项下借款金额、借款利率作了变动，未经保证人同意的，如果减轻借款人的债务的，保证人仍应当对变更后的合同承担保证责任；如果加重借款人的债务的，保证人对加重的部分不承担保证责任；

```json
[
  {
    "review_id": "GUA-08-01",
    "element_id": "guarantee_change_consent",
    "proposition": "主合同变更同意机制或未经同意加重部分免责",
    "status": "COVERED",
    "evidence_ids": [
      "C0085"
    ],
    "entailment": "SUPPORTS",
    "verifier_confidence": "high",
    "reason": "元素级证据可支撑。",
    "claim_id": "",
    "source_clause_ids": [
      "C0085"
    ],
    "source_spans": [
      "1、债权人与借款人对主合同项下借款金额、借款利率作了变动，未经保证人同意的，如果减轻借款人的债务的，保证人仍应当对变更后的合同承担保证责任；如果加重借款人的债务的，保证人对加重的部分不承担保证责任；"
    ],
    "source_locations": [
      "第九条第1项"
    ],
    "atomic": true,
    "child_elements": [],
    "legal_proposition_ids": [],
    "required_fact_key": "",
    "fact_status": "FOUND",
    "fact_value": null,
    "fact_evidence_refs": [
      "C0085"
    ],
    "requirement_status": "SATISFIED",
    "requirement_reason": "元素级证据可支撑。",
    "evidence_refs": [
      "C0085"
    ],
    "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
    "supporting_evidence": [
      {
        "clause_id": "C0085",
        "quote": "1、债权人与借款人对主合同项下借款金额、借款利率作了变动，未经保证人同意的，如果减轻借款人的债务的，保证人仍应当对变更后的合同承担保证责任；如果加重借款人的债务的，保证人对加重的部分不承担保证责任；"
      }
    ]
  }
]
```

### GUA-08-02：通过

- canonical location：第九条第1项；chunk：C0085；document_type：MAIN_CONTRACT
- 原文：1、债权人与借款人对主合同项下借款金额、借款利率作了变动，未经保证人同意的，如果减轻借款人的债务的，保证人仍应当对变更后的合同承担保证责任；如果加重借款人的债务的，保证人对加重的部分不承担保证责任；

```json
[
  {
    "review_id": "GUA-08-02",
    "element_id": "guarantee_debt_reduction",
    "proposition": "减轻债务后继续承担保证责任",
    "status": "COVERED",
    "evidence_ids": [
      "C0085"
    ],
    "entailment": "SUPPORTS",
    "verifier_confidence": "high",
    "reason": "元素级证据可支撑。",
    "claim_id": "",
    "source_clause_ids": [
      "C0085"
    ],
    "source_spans": [
      "1、债权人与借款人对主合同项下借款金额、借款利率作了变动，未经保证人同意的，如果减轻借款人的债务的，保证人仍应当对变更后的合同承担保证责任；如果加重借款人的债务的，保证人对加重的部分不承担保证责任；"
    ],
    "source_locations": [
      "第九条第1项"
    ],
    "atomic": true,
    "child_elements": [],
    "legal_proposition_ids": [],
    "required_fact_key": "",
    "fact_status": "FOUND",
    "fact_value": null,
    "fact_evidence_refs": [
      "C0085"
    ],
    "requirement_status": "SATISFIED",
    "requirement_reason": "元素级证据可支撑。",
    "evidence_refs": [
      "C0085"
    ],
    "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
    "supporting_evidence": [
      {
        "clause_id": "C0085",
        "quote": "1、债权人与借款人对主合同项下借款金额、借款利率作了变动，未经保证人同意的，如果减轻借款人的债务的，保证人仍应当对变更后的合同承担保证责任；如果加重借款人的债务的，保证人对加重的部分不承担保证责任；"
      }
    ]
  }
]
```

### GUA-08-03：通过

- canonical location：第九条第2项；chunk：C0086；document_type：MAIN_CONTRACT
- 原文：2、债权人与借款人对主合同约定还款计划的履行期限做了变动，未经保证人书面同意的，保证期间为原合同约定的或者法律规定的期间；

```json
[
  {
    "review_id": "GUA-08-03",
    "element_id": "guarantee_extension_period",
    "proposition": "展期书面确认或未经同意时保留原保证期间",
    "status": "COVERED",
    "evidence_ids": [
      "C0086"
    ],
    "entailment": "SUPPORTS",
    "verifier_confidence": "high",
    "reason": "元素级证据可支撑。",
    "claim_id": "",
    "source_clause_ids": [
      "C0086"
    ],
    "source_spans": [
      "2、债权人与借款人对主合同约定还款计划的履行期限做了变动，未经保证人书面同意的，保证期间为原合同约定的或者法律规定的期间；"
    ],
    "source_locations": [
      "第九条第2项"
    ],
    "atomic": true,
    "child_elements": [],
    "legal_proposition_ids": [],
    "required_fact_key": "",
    "fact_status": "FOUND",
    "fact_value": null,
    "fact_evidence_refs": [
      "C0086"
    ],
    "requirement_status": "SATISFIED",
    "requirement_reason": "元素级证据可支撑。",
    "evidence_refs": [
      "C0086"
    ],
    "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
    "supporting_evidence": [
      {
        "clause_id": "C0086",
        "quote": "2、债权人与借款人对主合同约定还款计划的履行期限做了变动，未经保证人书面同意的，保证期间为原合同约定的或者法律规定的期间；"
      }
    ]
  }
]
```

### GUA-08-04：通过

- canonical location：第十一条　通知；chunk：C0091；document_type：MAIN_CONTRACT
- 原文：第十一条　通知
根据本合同需要发出的全部通知以及双方的文件往来及与本合同有关的通知和要求等，均以向联系地址及电子邮件发送快递及邮件的方式予以传递，自相关文件进入对方系统之日则视为已成功送达。

```json
[
  {
    "review_id": "GUA-08-04",
    "element_id": "guarantee_change_notice_record",
    "proposition": "变更通知或全部合同文件往来的可留痕传递方式",
    "status": "COVERED",
    "evidence_ids": [
      "C0091"
    ],
    "entailment": "SUPPORTS",
    "verifier_confidence": "high",
    "reason": "元素级证据可支撑。",
    "claim_id": "",
    "source_clause_ids": [
      "C0091"
    ],
    "source_spans": [
      "第十一条　通知\n根据本合同需要发出的全部通知以及双方的文件往来及与本合同有关的通知和要求等，均以向联系地址及电子邮件发送快递及邮件的方式予以传递，自相关文件进入对方系统之日则视为已成功送达。"
    ],
    "source_locations": [
      "第十一条　通知"
    ],
    "atomic": true,
    "child_elements": [],
    "legal_proposition_ids": [],
    "required_fact_key": "",
    "fact_status": "FOUND",
    "fact_value": null,
    "fact_evidence_refs": [
      "C0091"
    ],
    "requirement_status": "SATISFIED",
    "requirement_reason": "元素级证据可支撑。",
    "evidence_refs": [
      "C0091"
    ],
    "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
    "supporting_evidence": [
      {
        "clause_id": "C0091",
        "quote": "第十一条　通知\n根据本合同需要发出的全部通知以及双方的文件往来及与本合同有关的通知和要求等，均以向联系地址及电子邮件发送快递及邮件的方式予以传递，自相关文件进入对方系统之日则视为已成功送达。"
      }
    ]
  }
]
```

## 签署身份核验

保证人身份与签署栏模板不一致，需核验自然人签名或法人签署授权。

```json
[
  {
    "party": "陈昊",
    "quote": "乙方：陈昊（公章）\n法定代表人（或授权代理人）：陈昊（签字）",
    "reason": "主体身份与签署模板不一致，需核对实际签署主体及授权。"
  }
]
```

GUA-01-01 部分覆盖 / MANUAL_REVIEW。真实签署栏证据已绑定。自然人误用公司模板与公司只有个人签名栏均有回归，未直接判定实际签署无效。

## 最终统计与门禁

覆盖统计：{'部分覆盖': 1, '通过': 27, '不适用': 14, '缺失': 5, '法律提示': 1}
风险主题：6；风险统计：{'重大风险': 0, '中等风险': 0, '低风险': 6, '人工复核': 1}
行动统计：{'major_risk': 0, 'medium_risk': 0, 'low_risk': 6, 'priority_action': 0, 'recommended_action': 0, 'optional_action': 5, 'manual_review': 1}
可签署性：建议专业法律复核后决定
release_quality_gate：REPORT_READY；failures=[]
N/A 风险来源、修改建议来源、action_priority、related_risks 已逐项断言，无 N/A 泄漏。
证据来源统计：{'MAIN_CONTRACT': 67, 'APPENDIX': 1}

## 修改文件

- F:\ai\Sage\backend\review_v2\guarantee_party_facts.py
- F:\ai\Sage\backend\review_v2\guarantee_contract_facts.py
- F:\ai\Sage\backend\review_v2\guarantee_prerequisites.py
- F:\ai\Sage\backend\review_v2\guarantee_mode.py
- F:\ai\Sage\backend\review_v2\guarantee_scope.py
- F:\ai\Sage\backend\review_v2\guarantee_contract_checklist.py
- F:\ai\Sage\backend\review_v2\engine.py
- F:\ai\Sage\backend\routers\review_v2.py
- F:\ai\Sage\backend\tests\test_guarantee_shared_facts.py

根因：保证人类型/人数未统一用于分支门控；通用标题/元素匹配缺少固定本金和变更责任的直接语义约束；保证方式/范围证据漏传 section_type；原有身份审查没有比对签署模板。
汇总继续使用引擎最终重算链；未直接改计数、未降低 release gate。新增保证模块纳入现有运行版本检查，磁盘代码变化需重载。

## 回归测试

新增19项，保证专项总计53项，全部通过。覆盖自然人单保证、公司单保证、两名自然人、固定金额、最高额金额、完整变更条款、双向签署模板不匹配，以及历史/假设共同保证、无须同意、其他小写金额等负例。
命令：python -m pytest tests/test_guarantee_shared_facts.py tests/test_guarantee_branch_prerequisites.py tests/test_guarantee_mode_consistency.py tests/test_guarantee_scope_boundary.py tests/test_guarantee_review_checklist.py -q

已知环境问题：启动时 TaskDB 报 SQLite database disk image is malformed；本次同步上传审查返回200且质量门通过。未在本轮执行数据库修复。