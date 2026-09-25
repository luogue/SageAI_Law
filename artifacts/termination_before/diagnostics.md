# 劳动合同逐项证据诊断

输入文件：74 劳动关系解除.docx
输入 SHA256：c9a164f5d9e57929a0c4e43dcaa2862da1e12c970cad54a3425d9bc66a83bad6
normalized SHA256：45ab21d9dde273b8cd0dc54545f62bdeec6be3a4bc42ca149f18f18e2bd09c3a

| rule_id | 最终状态 | 理由 |
|---|---|---|
| EMP-01-01 | PARTIAL | 未找到明确约定：用人单位住所。 |
| EMP-02-01 | PARTIAL | 未找到明确约定：期限类型、生效或起始日期。 |
| EMP-03-01 | N/A | 未触发专项场景：试用期。 |
| EMP-15-01 | PASS | 全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。 |
| EMP-04-01 | MISSING | 未找到明确约定：具体工作岗位或职责、具体工作地点。 |
| EMP-05-01 | MISSING | 未找到明确约定：工时制度及工作时间、休息休假安排。 |
| EMP-06-01 | MISSING | 未找到明确约定：工资金额或可计算标准、工资支付日期、工资支付方式。 |
| EMP-07-01 | MISSING | 未找到明确约定：用人单位依法办理参保并缴费。 |
| EMP-08-01 | MISSING | 未找到明确约定：劳动防护和安全培训。岗位职业危害情况待核实，未将条件不明的专项义务判为合同缺失。 |
| EMP-09-01 | N/A | 未识别已约定的专项培训服务期义务；另行签订协议的预备性表述不触发。 |
| EMP-10-01 | PASS | 合同原文覆盖本项核心法定义务；可选完善项未单独作为实际风险：解除通知方式或明确解除日期。 |
| EMP-11-01 | RISK | 发现与本项法定保护相冲突的直接不利约定。另有基础义务约定：“上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。”；该正向约定不能消除上述不利条款的冲突。 |
| EMP-12-01 | MISSING | 未找到明确约定：劳动争议依法申请劳动仲裁。 |
| EMP-13-01 | PASS | 全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。 |
| EMP-16-01 | PASS | 全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。 |
| EMP-14-01 | PASS | 全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。 |
| NC-01-01 | PARTIAL | 未找到明确约定：明确约定竞业业务范围、明确约定竞业地域范围。 |
| NC-02-01 | MISSING | 未找到明确约定：离职竞业限制期限、离职后按月经济补偿的金额或计算标准。 |
| NC-03-01 | 待核验 | 合理性判断所需事实尚不完整：明确约定竞业业务范围、明确约定竞业地域范围、离职竞业限制期限、离职后按月经济补偿的金额或计算标准、劳动者具体岗位、公司实际业务覆盖范围；不能据此直接认定范围合理或违法。 |
| EMP-IP-01 | PASS | 全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。 |

## 全部 SEARCH_AUDIT NOT FOUND

```json
[
  {
    "rule_id": "EMP-01-01",
    "element_id": "employment_identity_1",
    "review_id": "EMP-01-01",
    "search_targets": [
      "用人单位住所"
    ],
    "query_patterns": [
      "(?:用人单位|劳务派遣单位)[）)]?\\s*(?:名称|姓名)?\\s*[：:]\\s*[^\\n，；。_]{2,60}(?:公司|企业|事务所)(?:(?!乙方|劳动者|用工单位).){0,300}(?:住所|地址|注册地|注册登记地|实际经营地)[：:]\\s*[^\\n，；。_]{3,60}",
      "甲方(?:[（(][^）)\\n]{1,15}[）)])?[：:]\\s*[^\\n，；。_]{2,80}(?:(?!乙方)[\\s\\S]){0,200}(?:注册地址|经营地址|住所)[：:]\\s*[^\\n，；。_]{3,80}",
      "甲方[：:]\\s*[^\\n，；。_]{2,60}(?:(?!乙方)[\\s\\S]){0,120}(?:住所|地址)[：:]\\s*[^\\n，；。_]{3,60}"
    ],
    "query_semantic_target": "用人单位住所",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-02-01",
    "element_id": "employment_term_1",
    "review_id": "EMP-02-01",
    "search_targets": [
      "期限类型"
    ],
    "query_patterns": [
      "(?:固定期限|无固定期限|以完成.{1,30}工作任务为期限)"
    ],
    "query_semantic_target": "期限类型",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-02-01",
    "element_id": "employment_term_start",
    "review_id": "EMP-02-01",
    "search_targets": [
      "生效或起始日期"
    ],
    "query_patterns": [
      "(?:本合同|劳动合同|合同期限)(?:于|自|生效日期[为：:]?|起始日期[为：:]?)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?",
      "^\\s*自(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?起?\\s*(?:至|到)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?",
      "(?:本合同|合同期限)\\s*[：:]?\\s*自?(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?起?\\s*(?:至|到)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?",
      "起始日期[为：:]?\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?"
    ],
    "query_semantic_target": "生效或起始日期",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-04-01",
    "element_id": "employment_work_1",
    "review_id": "EMP-04-01",
    "search_targets": [
      "具体工作岗位或职责"
    ],
    "query_patterns": [
      "(?:工作岗位|工作内容|岗位)[为：:][^，。；_]{2,35}|安排(?:乙方|劳动者)在[^，。；_]{2,40}岗位|从事[^，。；_]{2,60}(?:开发|维护|测试|工作)",
      "(?:担任|从事)[^。；\\n]{2,60}岗位",
      "(?:负责|参与|承担)[^。；\\n]{2,80}(?:研发|开发|测试|维护|研究|设计|整理|编写)"
    ],
    "query_semantic_target": "具体工作岗位或职责",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-04-01",
    "element_id": "employment_work_2",
    "review_id": "EMP-04-01",
    "search_targets": [
      "具体工作地点"
    ],
    "query_patterns": [
      "工作地点[为：:][^，。；_]{3,60}"
    ],
    "query_semantic_target": "具体工作地点",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-05-01",
    "element_id": "employment_hours_1",
    "review_id": "EMP-05-01",
    "search_targets": [
      "工时制度及工作时间"
    ],
    "query_patterns": [
      "(?:标准工时|每天.{0,5}[八8]小时|每周.{0,5}40小时)",
      "(?:综合计算工时|不定时工作制).{0,45}(?:审批|批准)"
    ],
    "query_semantic_target": "工时制度及工作时间",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-05-01",
    "element_id": "employment_hours_2",
    "review_id": "EMP-05-01",
    "search_targets": [
      "休息休假安排"
    ],
    "query_patterns": [
      "(?:每周.{0,10}休息|(?:依法享有|依法享受).{0,15}(?:休假|年休假)|法定节假日.{0,10}休息)",
      "(?:休假制度|享受|享有)[^。；\\n]{0,40}(?:法定节假日|公休日|带薪年假)"
    ],
    "query_semantic_target": "休息休假安排",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-05-01",
    "element_id": "employment_hours_3",
    "review_id": "EMP-05-01",
    "search_targets": [
      "加班报酬或依法调休"
    ],
    "query_patterns": [
      "加班.{0,40}(?:依法支付|加班工资|补休|调休)",
      "依法安排[^。；\\n]{0,20}(?:补休|调休)或支付加班工资",
      "(?:支付|发放)加班工资"
    ],
    "query_semantic_target": "加班报酬或依法调休",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-06-01",
    "element_id": "employment_wage_1",
    "review_id": "EMP-06-01",
    "search_targets": [
      "工资金额或可计算标准"
    ],
    "query_patterns": [
      "(?<!试用期)(?:月工资|月正常工作时间工资|基本工资|工资标准)[为：:]?\\s*(?:人民币)?\\d+(?:\\.\\d+)?\\s*元",
      "(?:月工资标准|月工资|工资标准)\\s*(?:为|：|:)\\s*(?:税前|税后)?\\s*(?:人民币)?\\s*\\d+(?:\\.\\d+)?\\s*元(?:/月)?"
    ],
    "query_semantic_target": "工资金额或可计算标准",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-06-01",
    "element_id": "employment_wage_2",
    "review_id": "EMP-06-01",
    "search_targets": [
      "工资支付日期"
    ],
    "query_patterns": [
      "每月\\d{1,2}日.{0,20}(?:发放|支付|银行)|工资.{0,20}每月\\d{1,2}日",
      "每月[一二三四五六七八九十\\d]{1,3}日(?:前|内)?[^。；\\n]{0,30}支付[^。；\\n]{0,20}工资",
      "每月\\s*[一二三四五六七八九十\\d]{1,3}\\s*日\\s*(?:前|内)?[^。；\\n]{0,40}支付[^。；\\n]{0,25}工资"
    ],
    "query_semantic_target": "工资支付日期",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-06-01",
    "element_id": "employment_wage_3",
    "review_id": "EMP-06-01",
    "search_targets": [
      "工资支付方式"
    ],
    "query_patterns": [
      "工资.{0,40}(?:银行转账|银行账户|现金支付)|(?:银行转账|银行账户|现金支付)[^。；]{0,40}工资",
      "以货币形式支付[^。；\\n]{0,20}工资"
    ],
    "query_semantic_target": "工资支付方式",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-07-01",
    "element_id": "employment_insurance_1",
    "review_id": "EMP-07-01",
    "search_targets": [
      "用人单位依法办理参保并缴费"
    ],
    "query_patterns": [
      "(?:用人单位|甲方|甲乙双方).{0,80}(?:依法|按月).{0,15}(?:缴纳|缴付).{0,60}(?:社会保险|社保)",
      "(?:社会保险|社保)缴纳主体[：:]\\s*[^\\n，；。_]{2,60}(?:公司|企业|事务所)",
      "(?:甲乙双方|用人单位|甲方)(?:按|按照)[^。；\\n]{0,35}规定参加社会保险"
    ],
    "query_semantic_target": "用人单位依法办理参保并缴费",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-07-01",
    "element_id": "employment_insurance_2",
    "review_id": "EMP-07-01",
    "search_targets": [
      "个人应缴部分及代扣代缴"
    ],
    "query_patterns": [
      "(?:个人|劳动者|乙方).{0,15}(?:应缴|承担).{0,40}(?:代扣|代缴)|(?:代扣代缴).{0,45}(?:社会保险|社保).{0,15}个人缴费部分"
    ],
    "query_semantic_target": "个人应缴部分及代扣代缴",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-08-01",
    "element_id": "employment_safety_1",
    "review_id": "EMP-08-01",
    "search_targets": [
      "劳动防护和安全培训"
    ],
    "query_patterns": [
      "(?:提供|配备).{0,60}(?:劳动保护|劳动防护用品|防护用品)|安全(?:生产)?(?:教育和)?培训"
    ],
    "query_semantic_target": "劳动防护和安全培训",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-10-01",
    "element_id": "employment_exit_2",
    "review_id": "EMP-10-01",
    "search_targets": [
      "解除通知方式或明确解除日期"
    ],
    "query_patterns": [
      "(?:解除|终止).{0,40}(?:书面通知|\\d{4}年\\d{1,2}月\\d{1,2}日)|提前.{0,8}(?:三十|30)日.{0,8}书面通知"
    ],
    "query_semantic_target": "解除通知方式或明确解除日期",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-12-01",
    "element_id": "employment_dispute_1",
    "review_id": "EMP-12-01",
    "search_targets": [
      "劳动争议依法申请劳动仲裁"
    ],
    "query_patterns": [
      "(?:劳动争议|劳动合同争议).{0,60}(?:劳动仲裁|劳动(?:人事)?争议仲裁委员会)",
      "申请(?:调解或|调解、)?仲裁",
      "劳动争议仲裁机构[：:]\\s*[^。；\\n]{2,50}劳动人事争议仲裁委员会"
    ],
    "query_semantic_target": "劳动争议依法申请劳动仲裁",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "NC-01-01",
    "element_id": "employment_noncompete_scope_2",
    "review_id": "NC-01-01",
    "search_targets": [
      "明确约定竞业业务范围"
    ],
    "query_patterns": [
      "竞业(?:限制|禁止).{0,25}业务范围\\s*(?:为|包括|限于|：|:)[^。；_]{3,80}",
      "(?:不得|禁止).{0,20}(?:自营|经营|从事).{0,50}(?:竞争|同类).{0,20}业务"
    ],
    "query_semantic_target": "明确约定竞业业务范围",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "NC-01-01",
    "element_id": "employment_noncompete_scope_3",
    "review_id": "NC-01-01",
    "search_targets": [
      "明确约定竞业地域范围"
    ],
    "query_patterns": [
      "竞业(?:限制|禁止).{0,25}(?:地域|地区|区域)范围\\s*(?:为|包括|限于|：|:)[^。；_]{2,80}"
    ],
    "query_semantic_target": "明确约定竞业地域范围",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "NC-02-01",
    "element_id": "employment_noncompete_term_1",
    "review_id": "NC-02-01",
    "search_targets": [
      "离职竞业限制期限"
    ],
    "query_patterns": [
      "竞业(?:限制|禁止)(?:持续)?期(?:限)?\\s*(?:为|是|：|:)\\s*[一二两三四五六七八九十百\\d]+\\s*个?\\s*(?:月|年|日|天)",
      "离职后\\s*[一二两三四五六七八九十百\\d]+\\s*个?\\s*(?:月|年|日|天)(?:内)?[^。；\\n]{0,12}(?:承担|履行|遵守)竞业(?:限制|禁止)",
      "(?:离职|解除劳动合同|终止劳动合同)后[^。；\\n]{0,12}竞业(?:限制|禁止)(?:期(?:限)?)?\\s*(?:为|：|:)?\\s*[一二两三四五六七八九十百\\d]+\\s*个?\\s*(?:月|年|日|天)"
    ],
    "query_semantic_target": "离职竞业限制期限",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "NC-02-01",
    "element_id": "employment_noncompete_term_2",
    "review_id": "NC-02-01",
    "search_targets": [
      "离职后按月经济补偿的金额或计算标准"
    ],
    "query_patterns": [
      "(?:离职|解除|终止).{0,100}(?:每月|按月).{0,30}(?:补偿.{0,12}\\d+元|\\d+元.{0,12}补偿|补偿.{0,20}\\d+[%％])",
      "经济补偿(?:金)?(?:为|：|:)[^。；\\n]{0,80}(?:每月|按月)\\s*(?:人民币)?\\s*[\\d,，]+(?:\\.\\d+)?\\s*元",
      "(?:离职后|竞业限制期间)[^。；\\n]{0,40}(?:每月|按月)[^。；\\n]{0,20}(?:支付)?(?:经济)?补偿(?:金)?\\s*(?:为|：|:)?\\s*(?:人民币)?\\s*[\\d,，]+\\s*元"
    ],
    "query_semantic_target": "离职后按月经济补偿的金额或计算标准",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
      },
      {
        "clause_id": "C0005",
        "location": "4、关于乙方当月未结清劳动报酬的约定：",
        "title": "4、关于乙方当月未结清劳动报酬的约定：",
        "section_type": "正式合同条款",
        "heading_path": [
          "4、关于乙方当月未结清劳动报酬的约定："
        ],
        "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
      },
      {
        "clause_id": "C0006",
        "location": "第5项",
        "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
        "section_type": "正式合同条款",
        "heading_path": [
          "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
        ],
        "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
      },
      {
        "clause_id": "C0007",
        "location": "第6项",
        "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
        "section_type": "正式合同条款",
        "heading_path": [
          "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
        ],
        "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
      },
      {
        "clause_id": "C0008",
        "location": "第7项",
        "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
        "section_type": "正式合同条款",
        "heading_path": [
          "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
        ],
        "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
      },
      {
        "clause_id": "C0009",
        "location": "8、其他约定事项：",
        "title": "8、其他约定事项：",
        "section_type": "正式合同条款",
        "heading_path": [
          "8、其他约定事项："
        ],
        "text": "8、其他约定事项："
      },
      {
        "clause_id": "C0010",
        "location": "（1）",
        "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
        "section_type": "正式合同条款",
        "heading_path": [
          "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        ],
        "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
      },
      {
        "clause_id": "C0011",
        "location": "（2）",
        "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
        "section_type": "正式合同条款",
        "heading_path": [
          "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        ],
        "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      {
        "clause_id": "C0012",
        "location": "（3）",
        "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
        "section_type": "正式合同条款",
        "heading_path": [
          "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        ],
        "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
      },
      {
        "clause_id": "C0013",
        "location": "（4）",
        "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
        "section_type": "正式合同条款",
        "heading_path": [
          "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        ],
        "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
      },
      {
        "clause_id": "C0014",
        "location": "（5）",
        "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0015",
        "location": "甲方（签章）：北京华诚智能科技有限公司",
        "title": "甲方（签章）：北京华诚智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      {
        "clause_id": "C0016",
        "location": "乙方（签字）：张明远",
        "title": "乙方（签字）：张明远",
        "section_type": "正式合同条款",
        "heading_path": [
          "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
        ],
        "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1、因下列第（5）条情形，双方协商解除劳动合同："
        ],
        "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第2项",
        "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
        "section_type": "正式合同条款",
        "heading_path": [
          "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        ],
        "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "section_type": "正式合同条款",
        "heading_path": [
          "3、关于经济补偿金按以下第（2）条的约定执行："
        ],
        "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "NC-03-01",
    "element_id": "core_contract_arrangement",
    "review_id": "NC-03-01",
    "search_targets": [
      "合同存在可验证的“竞业范围或补偿明显不当”实质条款内容"
    ],
    "query_patterns": [
      "合同存在可验证的“竞业范围或补偿明显不当”实质条款内容"
    ],
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "OBJECTIVE_LITERAL_TARGET",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  }
]
```

## EMP-01-01

```json
{
  "rule_id": "EMP-01-01",
  "applicability": {
    "review_id": "EMP-01-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "部分覆盖",
  "reason": "未找到明确约定：用人单位住所。",
  "coverage_elements": [
    {
      "review_id": "EMP-01-01",
      "element_id": "employment_identity_1",
      "proposition": "用人单位住所",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    },
    {
      "review_id": "EMP-01-01",
      "element_id": "employment_identity_2",
      "proposition": "劳动者姓名与身份证明",
      "status": "COVERED",
      "evidence_ids": [
        "C0016"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0016"
      ],
      "source_spans": [
        "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      ],
      "source_locations": [
        "乙方（签字）：张明远"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0016"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0016"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0016",
          "quote": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ]
    },
    {
      "review_id": "EMP-01-01",
      "element_id": "employment_identity_name",
      "proposition": "用人单位名称",
      "status": "COVERED",
      "evidence_ids": [
        "C0001"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0001"
      ],
      "source_spans": [
        "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。"
      ],
      "source_locations": [
        "全文"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0001"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0001"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0001",
          "quote": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_identity_1",
      "review_id": "EMP-01-01",
      "search_targets": [
        "用人单位住所"
      ],
      "query_patterns": [
        "(?:用人单位|劳务派遣单位)[）)]?\\s*(?:名称|姓名)?\\s*[：:]\\s*[^\\n，；。_]{2,60}(?:公司|企业|事务所)(?:(?!乙方|劳动者|用工单位).){0,300}(?:住所|地址|注册地|注册登记地|实际经营地)[：:]\\s*[^\\n，；。_]{3,60}",
        "甲方(?:[（(][^）)\\n]{1,15}[）)])?[：:]\\s*[^\\n，；。_]{2,80}(?:(?!乙方)[\\s\\S]){0,200}(?:注册地址|经营地址|住所)[：:]\\s*[^\\n，；。_]{3,80}",
        "甲方[：:]\\s*[^\\n，；。_]{2,60}(?:(?!乙方)[\\s\\S]){0,120}(?:住所|地址)[：:]\\s*[^\\n，；。_]{3,60}"
      ],
      "query_semantic_target": "用人单位住所",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "employment_identity_2",
      "review_id": "EMP-01-01",
      "search_targets": [
        "劳动者姓名与身份证明"
      ],
      "query_patterns": [
        "劳动者[）)]?\\s*(?:名称|姓名)?\\s*[：:]\\s*[\\u4e00-\\u9fff·]{2,12}[^。；]{0,160}(?:居民身份证号码|身份证(?:号码)?|证件号码)[：:]?\\s*[0-9Xx]{8,18}",
        "乙方(?:[（(][^）)\\n]{1,15}[）)])?[：:]\\s*[\\u4e00-\\u9fff·]{2,12}(?:(?!甲方)[\\s\\S]){0,180}(?:居民身份证号码|身份证号码)[：:]\\s*[0-9Xx]{18}",
        "乙方[：:]?\\s*[\\u4e00-\\u9fff·]{2,12}[\\s\\S]{0,180}(?:居民身份证号码|身份证号码|证件号码)[：:]\\s*[0-9Xx]{8,18}",
        "乙方(?:[（(][^）)\\n]{1,15}[）)])?\\s*[：:]\\s*[\\u4e00-\\u9fff·]{2,12}(?:(?!甲方)[\\s\\S]){0,180}身份证号(?:码)?\\s*[：:]\\s*[0-9Xx*＊]{15,18}"
      ],
      "query_semantic_target": "劳动者姓名与身份证明",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "乙方(?:[（(][^）)\\n]{1,15}[）)])?\\s*[：:]\\s*[\\u4e00-\\u9fff·]{2,12}(?:(?!甲方)[\\s\\S]){0,180}身份证号(?:码)?\\s*[：:]\\s*[0-9Xx*＊]{15,18}"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日",
          "quote": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日",
          "original_excerpt": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "source_start": 0,
          "source_end": 70,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 100,
          "selection_reason": "DIRECT_OPERATIVE_WITH_VALUE"
        }
      ]
    },
    {
      "element_id": "employment_identity_name",
      "review_id": "EMP-01-01",
      "search_targets": [
        "用人单位名称"
      ],
      "query_patterns": [
        "甲方(?:[（(][^）)\\n]{1,20}[）)])?\\s*[：:]\\s*[^\\n，；。_]{2,60}",
        "甲方\\s*(?:名称|为|系)\\s*[：:]?\\s*[^\\n，；。_]{2,60}(?:大学|学院|医院|公司|研究所|中心)",
        "(?:用人单位|劳务派遣单位)[）)]?\\s*(?:名称)?\\s*[：:]\\s*[^\\n，；。_]{2,60}"
      ],
      "query_semantic_target": "用人单位名称",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "甲方(?:[（(][^）)\\n]{1,20}[）)])?\\s*[：:]\\s*[^\\n，；。_]{2,60}"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "甲方(?:[（(][^）)\\n]{1,20}[）)])?\\s*[：:]\\s*[^\\n，；。_]{2,60}"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "quote": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "original_excerpt": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 87,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 100,
          "selection_reason": "DIRECT_OPERATIVE_WITH_VALUE"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "text": "甲方（签章）：北京华诚智能科技有限公司",
          "quote": "甲方（签章）：北京华诚智能科技有限公司",
          "original_excerpt": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 10,
          "selection_reason": "HEADING_ONLY"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0016",
      "location": "乙方（签字）：张明远",
      "title": "乙方（签字）：张明远",
      "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日",
      "quote": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日",
      "original_excerpt": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日",
      "section_type": "正式合同条款",
      "heading_path": [
        "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
      ],
      "source_start": 1445,
      "source_end": 1515,
      "supports_element_ids": [
        "employment_identity_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 100,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "乙方（签字）：张明远",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日",
      "source_span": {
        "start_offset": 1445,
        "end_offset": 1515,
        "raw_text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0016",
        "section": "乙方（签字）：张明远",
        "sentence_index": 1,
        "quote": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_PARTIAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_identity_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "EMP-01-01",
      "element_ids": [
        "employment_identity_2"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "劳动者姓名与身份证明"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    },
    {
      "clause_id": "C0001",
      "location": "全文",
      "title": "全文",
      "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
      "quote": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
      "original_excerpt": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
      "section_type": "正式合同条款",
      "heading_path": [
        "全文"
      ],
      "source_start": 0,
      "source_end": 87,
      "supports_element_ids": [
        "employment_identity_name"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 100,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "全文",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
      "source_span": {
        "start_offset": 0,
        "end_offset": 87,
        "raw_text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0001",
        "section": "全文",
        "sentence_index": 1,
        "quote": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_PARTIAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_identity_name"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "EMP-01-01",
      "element_ids": [
        "employment_identity_name"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "用人单位名称"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    },
    {
      "clause_id": "C0015",
      "location": "甲方（签章）：北京华诚智能科技有限公司",
      "title": "甲方（签章）：北京华诚智能科技有限公司",
      "text": "甲方（签章）：北京华诚智能科技有限公司",
      "quote": "甲方（签章）：北京华诚智能科技有限公司",
      "original_excerpt": "甲方（签章）：北京华诚智能科技有限公司",
      "section_type": "正式合同条款",
      "heading_path": [
        "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
      ],
      "source_start": 1425,
      "source_end": 1444,
      "supports_element_ids": [
        "employment_identity_name"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 10,
      "selection_reason": "Contextual retrieval evidence does not directly support a resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "甲方（签章）：北京华诚智能科技有限公司",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "甲方（签章）：北京华诚智能科技有限公司",
      "source_span": {
        "start_offset": 1425,
        "end_offset": 1444,
        "raw_text": "甲方（签章）：北京华诚智能科技有限公司"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0015",
        "section": "甲方（签章）：北京华诚智能科技有限公司",
        "sentence_index": 1,
        "quote": "甲方（签章）：北京华诚智能科技有限公司",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_PARTIAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_identity_name"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 0.0,
      "review_id": "EMP-01-01",
      "element_ids": [
        "employment_identity_name"
      ],
      "support_type": "CONTEXTUAL",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "用人单位名称"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    }
  ],
  "termination_classification": []
}
```

## EMP-02-01

```json
{
  "rule_id": "EMP-02-01",
  "applicability": {
    "review_id": "EMP-02-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "部分覆盖",
  "reason": "未找到明确约定：期限类型、生效或起始日期。",
  "coverage_elements": [
    {
      "review_id": "EMP-02-01",
      "element_id": "employment_term_1",
      "proposition": "期限类型",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    },
    {
      "review_id": "EMP-02-01",
      "element_id": "employment_term_start",
      "proposition": "生效或起始日期",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    },
    {
      "review_id": "EMP-02-01",
      "element_id": "employment_term_end",
      "proposition": "终止日期",
      "status": "COVERED",
      "evidence_ids": [
        "C0001"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0001"
      ],
      "source_spans": [
        "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。"
      ],
      "source_locations": [
        "全文"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0001"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0001"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0001",
          "quote": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_term_1",
      "review_id": "EMP-02-01",
      "search_targets": [
        "期限类型"
      ],
      "query_patterns": [
        "(?:固定期限|无固定期限|以完成.{1,30}工作任务为期限)"
      ],
      "query_semantic_target": "期限类型",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "employment_term_start",
      "review_id": "EMP-02-01",
      "search_targets": [
        "生效或起始日期"
      ],
      "query_patterns": [
        "(?:本合同|劳动合同|合同期限)(?:于|自|生效日期[为：:]?|起始日期[为：:]?)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?",
        "^\\s*自(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?起?\\s*(?:至|到)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?",
        "(?:本合同|合同期限)\\s*[：:]?\\s*自?(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?起?\\s*(?:至|到)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?",
        "起始日期[为：:]?\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?"
      ],
      "query_semantic_target": "生效或起始日期",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "employment_term_end",
      "review_id": "EMP-02-01",
      "search_targets": [
        "终止日期"
      ],
      "query_patterns": [
        "^\\s*自(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?起?\\s*(?:至|到)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?",
        "(?:本合同|合同期限)\\s*[：:]?\\s*自?(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?起?\\s*(?:至|到)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?",
        "(?:终止日期|到期日期|合同至|期限至)[为：:]?\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?"
      ],
      "query_semantic_target": "终止日期",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:终止日期|到期日期|合同至|期限至)[为：:]?\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "quote": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "original_excerpt": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 87,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 100,
          "selection_reason": "DIRECT_OPERATIVE_WITH_VALUE"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0001",
      "location": "全文",
      "title": "全文",
      "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
      "quote": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
      "original_excerpt": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
      "section_type": "正式合同条款",
      "heading_path": [
        "全文"
      ],
      "source_start": 0,
      "source_end": 87,
      "supports_element_ids": [
        "employment_term_end"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 100,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "全文",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
      "source_span": {
        "start_offset": 0,
        "end_offset": 87,
        "raw_text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0001",
        "section": "全文",
        "sentence_index": 1,
        "quote": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_PARTIAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_term_end"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "EMP-02-01",
      "element_ids": [
        "employment_term_end"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "终止日期"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    }
  ],
  "termination_classification": []
}
```

## EMP-03-01

```json
{
  "rule_id": "EMP-03-01",
  "applicability": {
    "review_id": "EMP-03-01",
    "applicable": false,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "未触发专项场景：试用期。",
    "confidence": "medium",
    "status": "NOT_APPLICABLE",
    "machine_reason": "未触发专项场景：试用期。",
    "user_reason": "未触发专项场景：试用期。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "出现试用期安排时适用",
    "triggered": false,
    "condition_text": "出现试用期安排时适用"
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "不适用",
  "reason": "未触发专项场景：试用期。",
  "coverage_elements": [],
  "negative_clause_check": null,
  "element_absence_searches": [],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EMP-15-01

```json
{
  "rule_id": "EMP-15-01",
  "applicability": {
    "review_id": "EMP-15-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "NEGATIVE_CLAUSE_CHECK",
  "actual_status": "通过",
  "reason": "全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。",
  "coverage_elements": [],
  "negative_clause_check": {
    "review_id": "EMP-15-01",
    "query_semantics": "ADVERSE_CLAUSE_SEARCH",
    "result": "NO_ADVERSE_CLAUSE_FOUND",
    "description": "未发现对应禁止性/不利约定。",
    "searched_scope": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "candidate_adverse_clauses": [],
    "counter_evidence": [],
    "search_coverage": "SUFFICIENT",
    "adverse_clause_exists": false,
    "confidence": "high",
    "coverage_result": "通过"
  },
  "element_absence_searches": [],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EMP-04-01

```json
{
  "rule_id": "EMP-04-01",
  "applicability": {
    "review_id": "EMP-04-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "缺失",
  "reason": "未找到明确约定：具体工作岗位或职责、具体工作地点。",
  "coverage_elements": [
    {
      "review_id": "EMP-04-01",
      "element_id": "employment_work_1",
      "proposition": "具体工作岗位或职责",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    },
    {
      "review_id": "EMP-04-01",
      "element_id": "employment_work_2",
      "proposition": "具体工作地点",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_work_1",
      "review_id": "EMP-04-01",
      "search_targets": [
        "具体工作岗位或职责"
      ],
      "query_patterns": [
        "(?:工作岗位|工作内容|岗位)[为：:][^，。；_]{2,35}|安排(?:乙方|劳动者)在[^，。；_]{2,40}岗位|从事[^，。；_]{2,60}(?:开发|维护|测试|工作)",
        "(?:担任|从事)[^。；\\n]{2,60}岗位",
        "(?:负责|参与|承担)[^。；\\n]{2,80}(?:研发|开发|测试|维护|研究|设计|整理|编写)"
      ],
      "query_semantic_target": "具体工作岗位或职责",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "employment_work_2",
      "review_id": "EMP-04-01",
      "search_targets": [
        "具体工作地点"
      ],
      "query_patterns": [
        "工作地点[为：:][^，。；_]{3,60}"
      ],
      "query_semantic_target": "具体工作地点",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EMP-05-01

```json
{
  "rule_id": "EMP-05-01",
  "applicability": {
    "review_id": "EMP-05-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "缺失",
  "reason": "未找到明确约定：工时制度及工作时间、休息休假安排。",
  "coverage_elements": [
    {
      "review_id": "EMP-05-01",
      "element_id": "employment_hours_1",
      "proposition": "工时制度及工作时间",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    },
    {
      "review_id": "EMP-05-01",
      "element_id": "employment_hours_2",
      "proposition": "休息休假安排",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    },
    {
      "review_id": "EMP-05-01",
      "element_id": "employment_hours_3",
      "proposition": "加班报酬或依法调休",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "recommendation_action": "OPTIONAL",
      "risk_relevant": false,
      "residual_gap": "法定加班报酬规则无需在合同中重复列明；明确不利约定仍独立审查",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_hours_1",
      "review_id": "EMP-05-01",
      "search_targets": [
        "工时制度及工作时间"
      ],
      "query_patterns": [
        "(?:标准工时|每天.{0,5}[八8]小时|每周.{0,5}40小时)",
        "(?:综合计算工时|不定时工作制).{0,45}(?:审批|批准)"
      ],
      "query_semantic_target": "工时制度及工作时间",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "employment_hours_2",
      "review_id": "EMP-05-01",
      "search_targets": [
        "休息休假安排"
      ],
      "query_patterns": [
        "(?:每周.{0,10}休息|(?:依法享有|依法享受).{0,15}(?:休假|年休假)|法定节假日.{0,10}休息)",
        "(?:休假制度|享受|享有)[^。；\\n]{0,40}(?:法定节假日|公休日|带薪年假)"
      ],
      "query_semantic_target": "休息休假安排",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "employment_hours_3",
      "review_id": "EMP-05-01",
      "search_targets": [
        "加班报酬或依法调休"
      ],
      "query_patterns": [
        "加班.{0,40}(?:依法支付|加班工资|补休|调休)",
        "依法安排[^。；\\n]{0,20}(?:补休|调休)或支付加班工资",
        "(?:支付|发放)加班工资"
      ],
      "query_semantic_target": "加班报酬或依法调休",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EMP-06-01

```json
{
  "rule_id": "EMP-06-01",
  "applicability": {
    "review_id": "EMP-06-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "缺失",
  "reason": "未找到明确约定：工资金额或可计算标准、工资支付日期、工资支付方式。",
  "coverage_elements": [
    {
      "review_id": "EMP-06-01",
      "element_id": "employment_wage_1",
      "proposition": "工资金额或可计算标准",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    },
    {
      "review_id": "EMP-06-01",
      "element_id": "employment_wage_2",
      "proposition": "工资支付日期",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    },
    {
      "review_id": "EMP-06-01",
      "element_id": "employment_wage_3",
      "proposition": "工资支付方式",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_wage_1",
      "review_id": "EMP-06-01",
      "search_targets": [
        "工资金额或可计算标准"
      ],
      "query_patterns": [
        "(?<!试用期)(?:月工资|月正常工作时间工资|基本工资|工资标准)[为：:]?\\s*(?:人民币)?\\d+(?:\\.\\d+)?\\s*元",
        "(?:月工资标准|月工资|工资标准)\\s*(?:为|：|:)\\s*(?:税前|税后)?\\s*(?:人民币)?\\s*\\d+(?:\\.\\d+)?\\s*元(?:/月)?"
      ],
      "query_semantic_target": "工资金额或可计算标准",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "employment_wage_2",
      "review_id": "EMP-06-01",
      "search_targets": [
        "工资支付日期"
      ],
      "query_patterns": [
        "每月\\d{1,2}日.{0,20}(?:发放|支付|银行)|工资.{0,20}每月\\d{1,2}日",
        "每月[一二三四五六七八九十\\d]{1,3}日(?:前|内)?[^。；\\n]{0,30}支付[^。；\\n]{0,20}工资",
        "每月\\s*[一二三四五六七八九十\\d]{1,3}\\s*日\\s*(?:前|内)?[^。；\\n]{0,40}支付[^。；\\n]{0,25}工资"
      ],
      "query_semantic_target": "工资支付日期",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "employment_wage_3",
      "review_id": "EMP-06-01",
      "search_targets": [
        "工资支付方式"
      ],
      "query_patterns": [
        "工资.{0,40}(?:银行转账|银行账户|现金支付)|(?:银行转账|银行账户|现金支付)[^。；]{0,40}工资",
        "以货币形式支付[^。；\\n]{0,20}工资"
      ],
      "query_semantic_target": "工资支付方式",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EMP-07-01

```json
{
  "rule_id": "EMP-07-01",
  "applicability": {
    "review_id": "EMP-07-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "缺失",
  "reason": "未找到明确约定：用人单位依法办理参保并缴费。",
  "coverage_elements": [
    {
      "review_id": "EMP-07-01",
      "element_id": "employment_insurance_1",
      "proposition": "用人单位依法办理参保并缴费",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    },
    {
      "review_id": "EMP-07-01",
      "element_id": "employment_insurance_2",
      "proposition": "个人应缴部分及代扣代缴",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "recommendation_action": "OPTIONAL",
      "risk_relevant": false,
      "residual_gap": "法定个人缴费及代扣代缴机制无需在普通劳动合同中重复列明",
      "gap_risk_level": "中",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_insurance_1",
      "review_id": "EMP-07-01",
      "search_targets": [
        "用人单位依法办理参保并缴费"
      ],
      "query_patterns": [
        "(?:用人单位|甲方|甲乙双方).{0,80}(?:依法|按月).{0,15}(?:缴纳|缴付).{0,60}(?:社会保险|社保)",
        "(?:社会保险|社保)缴纳主体[：:]\\s*[^\\n，；。_]{2,60}(?:公司|企业|事务所)",
        "(?:甲乙双方|用人单位|甲方)(?:按|按照)[^。；\\n]{0,35}规定参加社会保险"
      ],
      "query_semantic_target": "用人单位依法办理参保并缴费",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "employment_insurance_2",
      "review_id": "EMP-07-01",
      "search_targets": [
        "个人应缴部分及代扣代缴"
      ],
      "query_patterns": [
        "(?:个人|劳动者|乙方).{0,15}(?:应缴|承担).{0,40}(?:代扣|代缴)|(?:代扣代缴).{0,45}(?:社会保险|社保).{0,15}个人缴费部分"
      ],
      "query_semantic_target": "个人应缴部分及代扣代缴",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EMP-08-01

```json
{
  "rule_id": "EMP-08-01",
  "applicability": {
    "review_id": "EMP-08-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "缺失",
  "reason": "未找到明确约定：劳动防护和安全培训。岗位职业危害情况待核实，未将条件不明的专项义务判为合同缺失。",
  "coverage_elements": [
    {
      "review_id": "EMP-08-01",
      "element_id": "employment_safety_1",
      "proposition": "劳动防护和安全培训",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    },
    {
      "element_id": "employment_safety_2",
      "status": "CONDITION_UNRESOLVED",
      "proposition": "核实岗位是否存在职业病危害因素，再确定告知和职业健康保护义务。",
      "required_fact": "职业危害告知和健康保护",
      "conditional_element": true,
      "prerequisite_status": "UNKNOWN",
      "prerequisite_fact": "工作岗位存在职业病危害因素",
      "verification_instruction": "核实岗位是否存在职业病危害因素，再确定告知和职业健康保护义务。",
      "risk_relevant": false,
      "bound_evidence_ids": [],
      "prerequisite_evidence": [],
      "source_clause_ids": [],
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_safety_1",
      "review_id": "EMP-08-01",
      "search_targets": [
        "劳动防护和安全培训"
      ],
      "query_patterns": [
        "(?:提供|配备).{0,60}(?:劳动保护|劳动防护用品|防护用品)|安全(?:生产)?(?:教育和)?培训"
      ],
      "query_semantic_target": "劳动防护和安全培训",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EMP-09-01

```json
{
  "rule_id": "EMP-09-01",
  "applicability": {
    "review_id": "EMP-09-01",
    "applicable": false,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "未识别已约定的专项培训服务期义务；另行签订协议的预备性表述不触发。",
    "confidence": "medium",
    "status": "NOT_APPLICABLE",
    "machine_reason": "未识别已约定的专项培训服务期义务；另行签订协议的预备性表述不触发。",
    "user_reason": "未识别已约定的专项培训服务期义务；另行签订协议的预备性表述不触发。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "出现服务期、专项培训安排时适用",
    "triggered": false,
    "condition_text": "出现服务期、专项培训安排时适用"
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "不适用",
  "reason": "未识别已约定的专项培训服务期义务；另行签订协议的预备性表述不触发。",
  "coverage_elements": [],
  "negative_clause_check": null,
  "element_absence_searches": [],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EMP-10-01

```json
{
  "rule_id": "EMP-10-01",
  "applicability": {
    "review_id": "EMP-10-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "通过",
  "reason": "合同原文覆盖本项核心法定义务；可选完善项未单独作为实际风险：解除通知方式或明确解除日期。",
  "coverage_elements": [
    {
      "review_id": "EMP-10-01",
      "element_id": "employment_exit_1",
      "proposition": "解除终止事由或协商一致",
      "status": "COVERED",
      "evidence_ids": [
        "C0002"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0002"
      ],
      "source_spans": [
        "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      ],
      "source_locations": [
        "第1项"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0002"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0002"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0002",
          "quote": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        }
      ]
    },
    {
      "review_id": "EMP-10-01",
      "element_id": "employment_exit_2",
      "proposition": "解除通知方式或明确解除日期",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "recommendation_action": "OPTIONAL",
      "risk_relevant": false,
      "residual_gap": "可选完善解除通知方式或未来解除日期确认机制",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_exit_1",
      "review_id": "EMP-10-01",
      "search_targets": [
        "解除终止事由或协商一致"
      ],
      "query_patterns": [
        "协商一致.{0,20}(?:解除|终止)|(?:解除|终止).{0,40}(?:法定条件|劳动合同法|法定事由)",
        "(?:解除|终止)[^。；\\n]{0,40}(?:按照|依照|根据|按)[^。；\\n]{0,10}法律法规[^。；\\n]{0,10}(?:执行|办理)",
        "(?:派遣.{0,10}(?:届满|期满)|依法退回)[^。；]{0,100}(?:重新派遣|另行安排.{0,20}派遣|依法解除)"
      ],
      "query_semantic_target": "解除终止事由或协商一致",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "协商一致.{0,20}(?:解除|终止)|(?:解除|终止).{0,40}(?:法定条件|劳动合同法|法定事由)"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "quote": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "original_excerpt": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "source_start": 0,
          "source_end": 137,
          "supports_element_ids": [
            "employment_exit_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 100,
          "selection_reason": "DIRECT_OPERATIVE_WITH_VALUE"
        }
      ]
    },
    {
      "element_id": "employment_exit_2",
      "review_id": "EMP-10-01",
      "search_targets": [
        "解除通知方式或明确解除日期"
      ],
      "query_patterns": [
        "(?:解除|终止).{0,40}(?:书面通知|\\d{4}年\\d{1,2}月\\d{1,2}日)|提前.{0,8}(?:三十|30)日.{0,8}书面通知"
      ],
      "query_semantic_target": "解除通知方式或明确解除日期",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0002",
      "location": "第1项",
      "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
      "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
      "quote": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
      "original_excerpt": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
      "section_type": "正式合同条款",
      "heading_path": [
        "1、因下列第（5）条情形，双方协商解除劳动合同："
      ],
      "source_start": 115,
      "source_end": 252,
      "supports_element_ids": [
        "employment_exit_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 100,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第1项",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
      "source_span": {
        "start_offset": 115,
        "end_offset": 252,
        "raw_text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0002",
        "section": "第1项",
        "sentence_index": 1,
        "quote": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_exit_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "EMP-10-01",
      "element_ids": [
        "employment_exit_1"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "解除终止事由或协商一致"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    }
  ],
  "termination_classification": []
}
```

## EMP-11-01

```json
{
  "rule_id": "EMP-11-01",
  "applicability": {
    "review_id": "EMP-11-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "风险条款",
  "reason": "发现与本项法定保护相冲突的直接不利约定。另有基础义务约定：“上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。”；该正向约定不能消除上述不利条款的冲突。",
  "coverage_elements": [
    {
      "review_id": "EMP-11-01",
      "element_id": "employment_compensation_adverse",
      "proposition": "经济补偿及结算存在直接不利约定",
      "status": "ADVERSE",
      "evidence_ids": [
        "C0004"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0004"
      ],
      "source_spans": [
        "(1)双方确认，甲方无需支付乙方经济补偿金。"
      ],
      "source_locations": [
        "3、关于经济补偿金按以下第（2）条的约定执行："
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0004"
      ],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0004"
      ],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0004",
          "quote": "(1)双方确认，甲方无需支付乙方经济补偿金。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [],
  "evidence_clauses": [
    {
      "clause_id": "C0004",
      "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
      "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
      "text": "(1)双方确认，甲方无需支付乙方经济补偿金。",
      "quote": "(1)双方确认，甲方无需支付乙方经济补偿金。",
      "section_type": "正式合同条款",
      "block_type": "OPERATIVE_CLAUSE",
      "predicate": "无需",
      "polarity": "AFFIRMED",
      "supports_element_ids": [
        "employment_compensation_adverse"
      ],
      "supporting_element_ids": [
        "employment_compensation_adverse"
      ],
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "3、关于经济补偿金按以下第（2）条的约定执行：",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
      "source_span": {
        "start_offset": 370,
        "end_offset": 392,
        "raw_text": "(1)双方确认，甲方无需支付乙方经济补偿金。"
      },
      "source_start": 370,
      "source_end": 392,
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0004",
        "section": "3、关于经济补偿金按以下第（2）条的约定执行：",
        "sentence_index": 1,
        "quote": "(1)双方确认，甲方无需支付乙方经济补偿金。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "(1)双方确认，甲方无需支付乙方经济补偿金。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "NEUTRAL",
      "entailment_status": "SUPPORTS",
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-11-01",
      "element_ids": [
        "employment_compensation_adverse"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "经济补偿及结算存在直接不利约定"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    }
  ],
  "termination_classification": []
}
```

## EMP-12-01

```json
{
  "rule_id": "EMP-12-01",
  "applicability": {
    "review_id": "EMP-12-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "缺失",
  "reason": "未找到明确约定：劳动争议依法申请劳动仲裁。",
  "coverage_elements": [
    {
      "review_id": "EMP-12-01",
      "element_id": "employment_dispute_1",
      "proposition": "劳动争议依法申请劳动仲裁",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_dispute_1",
      "review_id": "EMP-12-01",
      "search_targets": [
        "劳动争议依法申请劳动仲裁"
      ],
      "query_patterns": [
        "(?:劳动争议|劳动合同争议).{0,60}(?:劳动仲裁|劳动(?:人事)?争议仲裁委员会)",
        "申请(?:调解或|调解、)?仲裁",
        "劳动争议仲裁机构[：:]\\s*[^。；\\n]{2,50}劳动人事争议仲裁委员会"
      ],
      "query_semantic_target": "劳动争议依法申请劳动仲裁",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EMP-13-01

```json
{
  "rule_id": "EMP-13-01",
  "applicability": {
    "review_id": "EMP-13-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "NEGATIVE_CLAUSE_CHECK",
  "actual_status": "通过",
  "reason": "全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。",
  "coverage_elements": [],
  "negative_clause_check": {
    "review_id": "EMP-13-01",
    "query_semantics": "ADVERSE_CLAUSE_SEARCH",
    "result": "NO_ADVERSE_CLAUSE_FOUND",
    "description": "未发现对应禁止性/不利约定。",
    "searched_scope": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "candidate_adverse_clauses": [],
    "counter_evidence": [],
    "search_coverage": "SUFFICIENT",
    "adverse_clause_exists": false,
    "confidence": "high",
    "coverage_result": "通过"
  },
  "element_absence_searches": [],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EMP-16-01

```json
{
  "rule_id": "EMP-16-01",
  "applicability": {
    "review_id": "EMP-16-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "NEGATIVE_CLAUSE_CHECK",
  "actual_status": "通过",
  "reason": "全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。",
  "coverage_elements": [],
  "negative_clause_check": {
    "review_id": "EMP-16-01",
    "query_semantics": "ADVERSE_CLAUSE_SEARCH",
    "result": "NO_ADVERSE_CLAUSE_FOUND",
    "description": "未发现对应禁止性/不利约定。",
    "searched_scope": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "candidate_adverse_clauses": [],
    "counter_evidence": [],
    "search_coverage": "SUFFICIENT",
    "adverse_clause_exists": false,
    "confidence": "high",
    "coverage_result": "通过"
  },
  "element_absence_searches": [],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EMP-14-01

```json
{
  "rule_id": "EMP-14-01",
  "applicability": {
    "review_id": "EMP-14-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "NEGATIVE_CLAUSE_CHECK",
  "actual_status": "通过",
  "reason": "全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。",
  "coverage_elements": [],
  "negative_clause_check": {
    "review_id": "EMP-14-01",
    "query_semantics": "ADVERSE_CLAUSE_SEARCH",
    "result": "NO_ADVERSE_CLAUSE_FOUND",
    "description": "未发现对应禁止性/不利约定。",
    "searched_scope": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "candidate_adverse_clauses": [],
    "counter_evidence": [],
    "search_coverage": "SUFFICIENT",
    "adverse_clause_exists": false,
    "confidence": "high",
    "coverage_result": "通过"
  },
  "element_absence_searches": [],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## NC-01-01

```json
{
  "rule_id": "NC-01-01",
  "applicability": {
    "review_id": "NC-01-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "部分覆盖",
  "reason": "未找到明确约定：明确约定竞业业务范围、明确约定竞业地域范围。",
  "coverage_elements": [
    {
      "review_id": "NC-01-01",
      "element_id": "employment_noncompete_scope_1",
      "proposition": "人员范围及实际接触秘密",
      "status": "COVERED",
      "evidence_ids": [
        "C0011"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0011"
      ],
      "source_spans": [
        "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      ],
      "source_locations": [
        "（2）"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0011"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0011"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0011",
          "quote": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        }
      ]
    },
    {
      "review_id": "NC-01-01",
      "element_id": "employment_noncompete_scope_2",
      "proposition": "明确约定竞业业务范围",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    },
    {
      "review_id": "NC-01-01",
      "element_id": "employment_noncompete_scope_3",
      "proposition": "明确约定竞业地域范围",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_noncompete_scope_1",
      "review_id": "NC-01-01",
      "search_targets": [
        "人员范围及实际接触秘密"
      ],
      "query_patterns": [
        "(?:劳动者|乙方).{0,40}(?:实际接触|知悉|掌握).{0,35}(?:商业秘密|保密事项)"
      ],
      "query_semantic_target": "人员范围及实际接触秘密",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:劳动者|乙方).{0,40}(?:实际接触|知悉|掌握).{0,35}(?:商业秘密|保密事项)"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。",
          "quote": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。",
          "original_excerpt": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "source_start": 0,
          "source_end": 66,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 100,
          "selection_reason": "DIRECT_OPERATIVE_WITH_VALUE"
        }
      ]
    },
    {
      "element_id": "employment_noncompete_scope_2",
      "review_id": "NC-01-01",
      "search_targets": [
        "明确约定竞业业务范围"
      ],
      "query_patterns": [
        "竞业(?:限制|禁止).{0,25}业务范围\\s*(?:为|包括|限于|：|:)[^。；_]{3,80}",
        "(?:不得|禁止).{0,20}(?:自营|经营|从事).{0,50}(?:竞争|同类).{0,20}业务"
      ],
      "query_semantic_target": "明确约定竞业业务范围",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "employment_noncompete_scope_3",
      "review_id": "NC-01-01",
      "search_targets": [
        "明确约定竞业地域范围"
      ],
      "query_patterns": [
        "竞业(?:限制|禁止).{0,25}(?:地域|地区|区域)范围\\s*(?:为|包括|限于|：|:)[^。；_]{2,80}"
      ],
      "query_semantic_target": "明确约定竞业地域范围",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0011",
      "location": "（2）",
      "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
      "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。",
      "quote": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。",
      "original_excerpt": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。",
      "section_type": "正式合同条款",
      "heading_path": [
        "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      ],
      "source_start": 1135,
      "source_end": 1201,
      "supports_element_ids": [
        "employment_noncompete_scope_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 100,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "（2）",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。",
      "source_span": {
        "start_offset": 1135,
        "end_offset": 1201,
        "raw_text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0011",
        "section": "（2）",
        "sentence_index": 1,
        "quote": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_PARTIAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_noncompete_scope_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "NC-01-01",
      "element_ids": [
        "employment_noncompete_scope_1"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "人员范围及实际接触秘密"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    }
  ],
  "termination_classification": []
}
```

## NC-02-01

```json
{
  "rule_id": "NC-02-01",
  "applicability": {
    "review_id": "NC-02-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "核对离职竞业期限及补偿；未交代适用期间时不能直接按在职竞业豁免。",
    "confidence": "medium",
    "status": "APPLICABLE",
    "machine_reason": "核对离职竞业期限及补偿；未交代适用期间时不能直接按在职竞业豁免。",
    "user_reason": "合同已触发“出现离职、解除、终止安排时适用”这一适用条件。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "出现离职、解除、终止安排时适用",
    "triggered": true,
    "condition_text": "出现离职、解除、终止安排时适用"
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "缺失",
  "reason": "未找到明确约定：离职竞业限制期限、离职后按月经济补偿的金额或计算标准。",
  "coverage_elements": [
    {
      "review_id": "NC-02-01",
      "element_id": "employment_noncompete_term_1",
      "proposition": "离职竞业限制期限",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    },
    {
      "review_id": "NC-02-01",
      "element_id": "employment_noncompete_term_2",
      "proposition": "离职后按月经济补偿的金额或计算标准",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_noncompete_term_1",
      "review_id": "NC-02-01",
      "search_targets": [
        "离职竞业限制期限"
      ],
      "query_patterns": [
        "竞业(?:限制|禁止)(?:持续)?期(?:限)?\\s*(?:为|是|：|:)\\s*[一二两三四五六七八九十百\\d]+\\s*个?\\s*(?:月|年|日|天)",
        "离职后\\s*[一二两三四五六七八九十百\\d]+\\s*个?\\s*(?:月|年|日|天)(?:内)?[^。；\\n]{0,12}(?:承担|履行|遵守)竞业(?:限制|禁止)",
        "(?:离职|解除劳动合同|终止劳动合同)后[^。；\\n]{0,12}竞业(?:限制|禁止)(?:期(?:限)?)?\\s*(?:为|：|:)?\\s*[一二两三四五六七八九十百\\d]+\\s*个?\\s*(?:月|年|日|天)"
      ],
      "query_semantic_target": "离职竞业限制期限",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "employment_noncompete_term_2",
      "review_id": "NC-02-01",
      "search_targets": [
        "离职后按月经济补偿的金额或计算标准"
      ],
      "query_patterns": [
        "(?:离职|解除|终止).{0,100}(?:每月|按月).{0,30}(?:补偿.{0,12}\\d+元|\\d+元.{0,12}补偿|补偿.{0,20}\\d+[%％])",
        "经济补偿(?:金)?(?:为|：|:)[^。；\\n]{0,80}(?:每月|按月)\\s*(?:人民币)?\\s*[\\d,，]+(?:\\.\\d+)?\\s*元",
        "(?:离职后|竞业限制期间)[^。；\\n]{0,40}(?:每月|按月)[^。；\\n]{0,20}(?:支付)?(?:经济)?补偿(?:金)?\\s*(?:为|：|:)?\\s*(?:人民币)?\\s*[\\d,，]+\\s*元"
      ],
      "query_semantic_target": "离职后按月经济补偿的金额或计算标准",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。现经双方平等自愿协商，就解除劳动合同事宜达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。"
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。\n(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。\n上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。"
        },
        {
          "clause_id": "C0005",
          "location": "4、关于乙方当月未结清劳动报酬的约定：",
          "title": "4、关于乙方当月未结清劳动报酬的约定：",
          "section_type": "正式合同条款",
          "heading_path": [
            "4、关于乙方当月未结清劳动报酬的约定："
          ],
          "text": "4、关于乙方当月未结清劳动报酬的约定：\n双方确认，截至劳动合同解除之日，甲方尚未向乙方支付2026年9月份工资18000元及2026年第三季度绩效奖金4000元，合计22000元。上述款项由甲方在乙方完成全部工作交接及离职手续后统一结算支付。\n除上述款项外，乙方确认不存在其他未支付的工资、奖金、加班费、津贴、补贴、未休年休假工资等劳动报酬。"
        },
        {
          "clause_id": "C0006",
          "location": "第5项",
          "title": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离",
          "section_type": "正式合同条款",
          "heading_path": [
            "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。"
          ],
          "text": "5、乙方应在本协议签订之日起3天内，按照甲方的相关规定和要求办理所有工作交接及离职手续，包括但不限于移交工作文件、客户资料、账号密码、办公设备及其他公司财物。\n如乙方未在规定期限内完成工作交接，甲方有权暂缓支付尚未结清的劳动报酬及经济补偿金，直至乙方完成全部工作交接手续。"
        },
        {
          "clause_id": "C0007",
          "location": "第6项",
          "title": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳",
          "section_type": "正式合同条款",
          "heading_path": [
            "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。"
          ],
          "text": "6、甲方在确认乙方办理完毕工作交接、离职手续之日起15天内，将乙方当月未结清的劳动报酬及经济补偿金支付给乙方。\n甲方有权从上述应付款项中直接扣除乙方尚未归还的公司财物价值、借款、培训费用以及因乙方工作失误给甲方造成的损失。"
        },
        {
          "clause_id": "C0008",
          "location": "第7项",
          "title": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴",
          "section_type": "正式合同条款",
          "heading_path": [
            "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。"
          ],
          "text": "7、甲乙双方就与劳动关系有关的所有费用（包括但不限于劳动报酬、加班费、奖金、津贴补贴、经济补偿金、社会保险、住房公积金、未休年休假工资及其他任何费用）均已结算。\n乙方确认对上述结算无异议，并自愿放弃基于双方劳动关系向甲方提出任何其他请求、仲裁、诉讼、投诉或者举报的权利。双方确认不存在任何劳动争议及纠纷。"
        },
        {
          "clause_id": "C0009",
          "location": "8、其他约定事项：",
          "title": "8、其他约定事项：",
          "section_type": "正式合同条款",
          "heading_path": [
            "8、其他约定事项："
          ],
          "text": "8、其他约定事项："
        },
        {
          "clause_id": "C0010",
          "location": "（1）",
          "title": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档",
          "section_type": "正式合同条款",
          "heading_path": [
            "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
          ],
          "text": "（1）甲方应依法为乙方出具解除劳动合同证明，并在双方解除劳动合同后30日内办理档案及社会保险关系转移手续。"
        },
        {
          "clause_id": "C0011",
          "location": "（2）",
          "title": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信",
          "section_type": "正式合同条款",
          "heading_path": [
            "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
          ],
          "text": "（2）乙方在劳动关系存续期间知悉的甲方商业秘密、技术资料、客户信息、经营数据等信息，在劳动合同解除后仍负有保密义务，保密期限为永久。"
        },
        {
          "clause_id": "C0012",
          "location": "（3）",
          "title": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职",
          "section_type": "正式合同条款",
          "heading_path": [
            "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
          ],
          "text": "（3）乙方承诺，自劳动合同解除之日起两年内，不得进入与甲方存在竞争关系的企业任职，也不得自行经营与甲方相同或类似的业务。甲方无需就上述竞业限制义务另行向乙方支付经济补偿。"
        },
        {
          "clause_id": "C0013",
          "location": "（4）",
          "title": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥",
          "section_type": "正式合同条款",
          "heading_path": [
            "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
          ],
          "text": "（4）乙方违反本条约定的，应向甲方支付违约金人民币200000元；违约金不足以弥补甲方损失的，乙方还应赔偿全部损失。"
        },
        {
          "clause_id": "C0014",
          "location": "（5）",
          "title": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。\n本协议书一式三份，甲乙双方及北京华诚智能科技有限公司人力资源部各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0015",
          "location": "甲方（签章）：北京华诚智能科技有限公司",
          "title": "甲方（签章）：北京华诚智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "甲方（签章）：北京华诚智能科技有限公司"
        },
        {
          "clause_id": "C0016",
          "location": "乙方（签字）：张明远",
          "title": "乙方（签字）：张明远",
          "section_type": "正式合同条款",
          "heading_path": [
            "（5）本协议签署后，双方均不得以任何理由反悔或要求撤销本协议。"
          ],
          "text": "乙方（签字）：张明远\n委托代理人（签章）：李建国\n身份证号：110101199205168637\n2026年9月25日\n2026年9月25日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "解除或终止劳动合同协议书\n甲方：北京华诚智能科技有限公司（用人单位）\n乙方：张明远（职工姓名）\n甲乙双方于2021年4月15日签订了劳动合同，合同期限至2027年4月14日。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "现经双方平等自愿协商，就解除劳动合同事宜达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1、因下列第（5）条情形，双方协商解除劳动合同：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1、因下列第（5）条情形，双方协商解除劳动合同："
          ],
          "text": "1、因下列第（5）条情形，双方协商解除劳动合同：\n(1)乙方提出辞职，甲方同意；\n(2)合同到期，乙方提出不再续签；\n(3)合同到期，甲方提出不再续签；\n(4)乙方达到法定退休年龄；\n(5)其他原因：因甲方经营结构调整及部门岗位优化，由甲方提出，经双方协商一致解除劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第2项",
          "title": "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴",
          "section_type": "正式合同条款",
          "heading_path": [
            "2、双方同意于2026年9月30日解除劳动合同，劳动报酬及社会保险同时停发及停缴。其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。"
          ],
          "text": "其中劳动报酬发放至2026年9月30日，社会保险于2026年9月停缴、住房公积金于2026年9月停缴。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "3、关于经济补偿金按以下第（2）条的约定执行：\n(1)双方确认，甲方无需支付乙方经济补偿金。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "(2)双方确认，乙方自2021年4月起在甲方工作，连续工作5年5个月，甲方应支付乙方5.5个月工资，具体金额为99000元人民币。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "title": "3、关于经济补偿金按以下第（2）条的约定执行：",
          "section_type": "正式合同条款",
          "heading_path": [
            "3、关于经济补偿金按以下第（2）条的约定执行："
          ],
          "text": "上述经济补偿金按照乙方解除劳动合同前十二个月平均工资18000元/月计算。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## NC-03-01

```json
{
  "rule_id": "NC-03-01",
  "applicability": {
    "review_id": "NC-03-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "NEGATIVE_CLAUSE_CHECK",
  "actual_status": "待核验",
  "reason": "合理性判断所需事实尚不完整：明确约定竞业业务范围、明确约定竞业地域范围、离职竞业限制期限、离职后按月经济补偿的金额或计算标准、劳动者具体岗位、公司实际业务覆盖范围；不能据此直接认定范围合理或违法。",
  "coverage_elements": [
    {
      "review_id": "NC-03-01",
      "element_id": "core_contract_arrangement",
      "proposition": "合同存在可验证的“竞业范围或补偿明显不当”实质条款内容。",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    },
    {
      "element_id": "noncompete_reasonableness_prerequisites",
      "status": "CONDITION_UNRESOLVED",
      "proposition": "合理性判断所需事实尚不完整：明确约定竞业业务范围、明确约定竞业地域范围、离职竞业限制期限、离职后按月经济补偿的金额或计算标准、劳动者具体岗位、公司实际业务覆盖范围；不能据此直接认定范围合理或违法。",
      "required_fact": "竞业范围及补偿合理性判断前提",
      "conditional_element": true,
      "prerequisite_status": "UNKNOWN",
      "prerequisite_fact": "人员、秘密接触、范围、期限及补偿事实足以判断合理性",
      "verification_instruction": "合理性判断所需事实尚不完整：明确约定竞业业务范围、明确约定竞业地域范围、离职竞业限制期限、离职后按月经济补偿的金额或计算标准、劳动者具体岗位、公司实际业务覆盖范围；不能据此直接认定范围合理或违法。",
      "risk_relevant": false,
      "bound_evidence_ids": [],
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    }
  ],
  "negative_clause_check": {
    "review_id": "NC-03-01",
    "query_semantics": "ADVERSE_CLAUSE_SEARCH",
    "result": "NO_ADVERSE_CLAUSE_FOUND",
    "description": "未发现对应禁止性/不利约定。",
    "searched_scope": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "candidate_adverse_clauses": [],
    "counter_evidence": [],
    "search_coverage": "SUFFICIENT",
    "adverse_clause_exists": false,
    "confidence": "high",
    "coverage_result": "INSUFFICIENT_CONTEXT"
  },
  "element_absence_searches": [
    {
      "element_id": "core_contract_arrangement",
      "review_id": "NC-03-01",
      "search_targets": [
        "合同存在可验证的“竞业范围或补偿明显不当”实质条款内容"
      ],
      "query_patterns": [
        "合同存在可验证的“竞业范围或补偿明显不当”实质条款内容"
      ],
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "OBJECTIVE_LITERAL_TARGET",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016"
      ],
      "searched_document_hash": "7c47c40b44e97820ac325ec3018357c5111ec1a9f6db238a08b36e3ff2240e83",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EMP-IP-01

```json
{
  "rule_id": "EMP-IP-01",
  "applicability": {
    "review_id": "EMP-IP-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "NEGATIVE_CLAUSE_CHECK",
  "actual_status": "通过",
  "reason": "全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。",
  "coverage_elements": [],
  "negative_clause_check": {
    "review_id": "EMP-IP-01",
    "query_semantics": "ADVERSE_CLAUSE_SEARCH",
    "result": "NO_ADVERSE_CLAUSE_FOUND",
    "description": "未发现对应禁止性/不利约定。",
    "searched_scope": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016"
    ],
    "candidate_adverse_clauses": [],
    "counter_evidence": [],
    "search_coverage": "SUFFICIENT",
    "adverse_clause_exists": false,
    "confidence": "high",
    "coverage_result": "通过"
  },
  "element_absence_searches": [],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## release_quality_gate

```json
{
  "status": "REPORT_READY",
  "failures": [],
  "priority_consistency_verification": {
    "executed": true,
    "high_finding_count": 3,
    "core_priority_count": 3,
    "consistency": "CONSISTENT",
    "explanations": [],
    "needs_recalibration": false
  },
  "context_consistency": {
    "status": "PASS",
    "failures": [],
    "contract_type": "labor",
    "domain_pack": "priority-domain-1.0"
  },
  "gate_results": {
    "PASS_EVIDENCE_PROVENANCE_GATE": "PASS",
    "PARTIAL_ELEMENT_NARRATIVE_GATE": "PASS",
    "COVERAGE_SENTENCE_CONSISTENCY_GATE": "PASS",
    "ELEMENT_STATUS_CONTRADICTION": "PASS",
    "EVIDENCE_MONOTONICITY_VIOLATION": "PASS",
    "FINDING_EVIDENCE_GATE": "PASS",
    "CROSS_LAYER_CONSISTENCY_GATE": "PASS",
    "DEFAULT_LAW_COMPLETENESS_GATE": "PASS",
    "DEFAULT_LAW_EFFECTIVE_GAP_GATE": "PASS",
    "NARRATIVE_ELEMENT_CONSISTENCY_GATE": "PASS",
    "NARRATIVE_TRUTH_GATE": "PASS",
    "PRIORITY_CONSISTENCY_GATE": "PASS",
    "SIGNABILITY_GATE": "PASS",
    "CONFIDENCE_VALIDATION_GATE": "PASS",
    "DOMAIN_SUBTYPE_GATE": "PASS",
    "DOMAIN_REVIEW_ISOLATION_GATE": "PASS",
    "DOMAIN_MATERIAL_COVERAGE_GATE": "PASS",
    "TRANSACTION_STRUCTURE_GATE": "PASS",
    "FRAMEWORK_DOMAIN_GATE": "PASS",
    "ORDER_RELATION_GATE": "PASS",
    "DYNAMIC_QUANTITY_GATE": "PASS",
    "PRICE_MECHANISM_GATE": "PASS",
    "ALTERNATIVE_SATISFACTION_GATE": "PASS",
    "FALSE_RISK_EXISTENCE_GATE": "PASS",
    "FACT_REGISTRY_SNAPSHOT_CONSISTENCY": "PASS",
    "FACT_REGISTRY_CONFLICTING_FACT": "PASS",
    "CROSS_REVIEW_FACT_CONFLICT": "PASS",
    "FACT_TRUTH_OVERRIDE_VIOLATION": "PASS",
    "FACT_CONSUMER_MAPPING_MISSING": "PASS",
    "RISK_EVIDENCE_MISMATCH": "PASS",
    "REVIEW_EVIDENCE_ELEMENT_MISMATCH": "PASS",
    "APPLICABILITY_PRECONDITION_GATE": "PASS",
    "SHARED_CLAIM_CONSISTENCY_GATE": "PASS",
    "FINDING_PRECONDITION_GATE": "PASS",
    "REPORT_CONTEXT_GATE": "PASS",
    "REPORT_TRANSACTION_TRUTH_GATE": "PASS",
    "CROSS_REVIEW_CONSISTENCY_GATE": "PASS",
    "RECOMMENDATION_NON_DEGRADATION_GATE": "PASS",
    "COMMON_REVIEW_SATISFACTION_GATE": "PASS",
    "ELEMENT_IDENTITY_CONTRADICTION_GATE": "PASS",
    "PRODUCT_APPLICABILITY_GATE": "PASS",
    "SHARED_CLAIM_REUSE_GATE": "PASS",
    "FINDING_INDEPENDENCE_GATE": "PASS",
    "TECHNOLOGY_TRANSACTION_CONSISTENCY": "NOT_APPLICABLE",
    "PERSPECTIVE_DOMAIN_CONSISTENCY_GATE": "PASS",
    "PATENT_TRANSFER_QUALITY_GATE": "NOT_APPLICABLE",
    "PRODUCTION_FACT_POLARITY_GATE": "PASS",
    "RECOMMENDATION_SOURCE_UNMAPPED": "PASS",
    "RECOMMENDATION_ELEMENT_LEAKAGE": "PASS",
    "RECOMMENDATION_COVERED_ELEMENT_REINTRODUCED": "PASS",
    "RECOMMENDATION_PLACEHOLDER_TEXT": "PASS",
    "RECOMMENDATION_FINAL_DISPOSITION_MISMATCH": "PASS",
    "CLIENT_INTEREST_GATE": "PASS",
    "RISK_STATISTICS_INVARIANT": "PASS",
    "FINAL_DISPOSITION_INVARIANT": "PASS",
    "FORMAL_RECOMMENDATION_FINAL_DISPOSITION_INVARIANT": "PASS",
    "RECOMMENDATION_OWNERSHIP_INVARIANT": "PASS",
    "HIGH_NON_MUST_CHANGE_REASON_INVARIANT": "PASS",
    "OPTIONAL_IMPROVEMENT_VISIBILITY_INVARIANT": "PASS",
    "ACTIONABLE_RECOMMENDATION_COMPLETENESS_INVARIANT": "PASS",
    "LEGAL_AUTHORITY_DEDUP_GATE": "PASS",
    "LEGAL_AUTHORITY_SELECTION_GATE": "PASS",
    "CITATION_ENTAILMENT_GATE": "PASS",
    "LEGAL_DEFAULT_LAW_CONSISTENCY_GATE": "PASS",
    "ATOMIC_LEGAL_ELEMENT_GATE": "PASS",
    "DEFAULT_LAW_NARRATIVE_TRUTH_GATE": "PASS",
    "NOT_APPLICABLE_NARRATIVE_GATE": "PASS",
    "NOT_APPLICABLE_GAP_GATE": "PASS",
    "REVIEW_POLARITY_NARRATIVE_GATE": "PASS",
    "NEGATIVE_CHECK_PASS_GATE": "PASS",
    "CROSS_REVIEW_SHARED_CLAIM_GATE": "PASS",
    "NARRATIVE_EVIDENCE_GATE": "PASS",
    "EXACT_ELEMENT_REPORT_INVARIANT": "PASS",
    "PRODUCTION_INTERNAL_TOKEN_GATE": "PASS",
    "DEFAULT_LAW_PROVENANCE_GATE": "PASS",
    "RECOMMENDATION_SINGLE_SOURCE_GATE": "PASS",
    "RECOMMENDATION_CROSS_RENDERER_CONSISTENCY_GATE": "PASS",
    "REPORT_TEXT_VALIDATION": "PASS",
    "REPORT_DISPOSITION_PROJECTION_INVARIANT": "PASS",
    "EVIDENCE_BUNDLE_ENTAILMENT_GATE": "PASS",
    "RECOMMENDATION_SEMANTIC_BINDING_GATE": "PASS",
    "SUMMARY_DETAIL_RISK_ID_GATE": "PASS",
    "ISSUE_TYPE_NARRATIVE_GATE": "PASS",
    "OPTIONAL_REPORT_COUNT_GATE": "PASS",
    "REPORT_ROLE_PLACEHOLDER_GATE": "PASS",
    "ACTIONABLE_RECOMMENDATION_VISIBILITY_GATE": "PASS",
    "CLAIM_EVIDENCE_COVERAGE_GATE": "PASS",
    "EVIDENCE_FACT_ROLE_GATE": "PASS",
    "SINGLE_EVIDENCE_SOURCE_GATE": "PASS",
    "EVIDENCE_BUNDLE_RENDER_GATE": "PASS",
    "APPLICABILITY_DISPLAY_CONSISTENCY_GATE": "PASS",
    "ISSUE_TYPE_CONSISTENCY_GATE": "PASS",
    "PARTIAL_MISSING_ELEMENT_GATE": "PASS",
    "SUMMARY_TRUNCATION_DISCLOSURE_GATE": "PASS",
    "TECHNICAL_REPORT_PLACEHOLDER_GATE": "PASS",
    "FINAL_RISK_EVIDENCE_BUNDLE_GATE": "PASS",
    "EVIDENCE_ITEM_UNIQUENESS_GATE": "PASS",
    "CLAUSE_NODE_CONSISTENCY_GATE": "PASS",
    "MISSING_RISK_ABSENCE_EVIDENCE_GATE": "PASS",
    "COVERAGE_RISK_ACTION_CONSISTENCY_GATE": "PASS",
    "PATENT_ROLE_TERMINOLOGY_GATE": "PASS",
    "DUPLICATE_TEMPLATE_PHRASE_GATE": "PASS",
    "EVIDENCE_PROPOSITION_MATCH_GATE": "PASS",
    "PASS_EVIDENCE_PROPOSITION_MATCH_GATE": "PASS",
    "CANONICAL_RISK_COVERAGE_INVARIANT": "PASS",
    "CONSULTING_REPORT_CONTEXT_GATE": "PASS",
    "TERMINOLOGY_CONSISTENCY_GATE": "PASS",
    "APPLICABILITY_AND_EVIDENCE_BOUNDARY": "PASS"
  },
  "blocking_rules": [],
  "blocking_stage": "",
  "blocking_entities": [],
  "blocking_reasons": [],
  "post_render_status": "REPORT_READY"
}
```