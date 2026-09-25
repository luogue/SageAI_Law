# 劳动合同逐项证据诊断

输入文件：79 股权转让.docx
输入 SHA256：74950bb5c82aecd99e529d91ea44b4a2d6e62b689e5aa39ffe45167b10a39299
normalized SHA256：0738f87febef86eb4b80e282f154a9e9005119190805e327157862b8e4bee0b3

| rule_id | 最终状态 | 理由 |
|---|---|---|
| EQT-01-01 | MISSING | 未找到明确约定：交易主体及目标公司名称、持股比例及合法权属声明。 |
| EQT-02-01 | MISSING | 未找到明确约定：认缴、实缴金额及出资期限、未缴出资责任的承担及法定责任保留。 |
| EQT-11-01 | MISSING | 未找到明确约定：股权负担和财务债务的陈述保证、陈述不实的赔偿或退出救济。 |
| EQT-13-01 | PASS | 全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。 |
| EQT-03-01 | MISSING | 未找到明确约定：公司章程转让限制核对、向其他股东通知同等条件或不触发外部转让、优先购买权的依法行使或书面放弃。 |
| EQT-04-01 | MISSING | 未找到明确约定：价款或投资总额、支付节点、条件或期限。 |
| EQT-05-01 | MISSING | 未找到明确约定：交割条件及未满足的处理、股东名册及出资证明更新、办理变更登记的责任人与期限。 |
| S-00-01 | PASS | 正式合同条款或附件中已召回能够覆盖该审查点的实质约定，未发现明显空白项。 |
| S-00-03 | MISSING | 未在正式合同条款中找到能覆盖该审查点的有效约定。 |

## 全部 SEARCH_AUDIT NOT FOUND

```json
[
  {
    "rule_id": "EQT-01-01",
    "element_id": "equity_title_1",
    "review_id": "EQT-01-01",
    "search_targets": [
      "交易主体及目标公司名称"
    ],
    "query_patterns": [
      "(?:转让方|投资方|股东)[：:][^，。；_]{2,50}.{0,70}目标公司[：:][^，。；_]{2,50}"
    ],
    "query_semantic_target": "交易主体及目标公司名称",
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
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式"
      },
      {
        "clause_id": "C0003",
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
      },
      {
        "clause_id": "C0004",
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
      },
      {
        "clause_id": "C0005",
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证"
      },
      {
        "clause_id": "C0006",
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
      },
      {
        "clause_id": "C0007",
        "location": "第二条第2项",
        "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        ],
        "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
      },
      {
        "clause_id": "C0008",
        "location": "第二条第3项",
        "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        ],
        "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
      },
      {
        "clause_id": "C0009",
        "location": "第三条 盈亏分担",
        "title": "盈亏分担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条 盈亏分担"
        ],
        "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
      },
      {
        "clause_id": "C0010",
        "location": "第四条 费用负担",
        "title": "费用负担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条 费用负担"
        ],
        "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
      },
      {
        "clause_id": "C0011",
        "location": "第五条 合同的变更与解除",
        "title": "合同的变更与解除",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除"
        ],
        "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
      },
      {
        "clause_id": "C0012",
        "location": "第五条第1项",
        "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        ],
        "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
      },
      {
        "clause_id": "C0013",
        "location": "第五条第2项",
        "title": "2、一方当事人丧失实际履约能力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "2、一方当事人丧失实际履约能力。"
        ],
        "text": "2、一方当事人丧失实际履约能力。"
      },
      {
        "clause_id": "C0014",
        "location": "第五条第3项",
        "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        ],
        "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
      },
      {
        "clause_id": "C0015",
        "location": "第五条第4项",
        "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        ],
        "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
      },
      {
        "clause_id": "C0016",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "第六条 争议的解决"
      },
      {
        "clause_id": "C0017",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
      },
      {
        "clause_id": "C0018",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "☑ 向广州仲裁委员会申请仲裁；"
      },
      {
        "clause_id": "C0019",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "使用说明",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "□ 向有管辖权的人民法院起诉。"
      },
      {
        "clause_id": "C0020",
        "location": "第七条 合同生效的条件和日期",
        "title": "合同生效的条件和日期",
        "section_type": "正式合同条款",
        "heading_path": [
          "第七条 合同生效的条件和日期"
        ],
        "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
      },
      {
        "clause_id": "C0021",
        "location": "第八条",
        "title": "第八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第八条"
        ],
        "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
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
    "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EQT-01-01",
    "element_id": "equity_title_2",
    "review_id": "EQT-01-01",
    "search_targets": [
      "持股比例及合法权属声明"
    ],
    "query_patterns": [
      "(?:持有|转让|认购|股权比例).{0,15}\\d+(?:\\.\\d+)?[%％].{0,50}(?:合法|权属|处分权)"
    ],
    "query_semantic_target": "持股比例及合法权属声明",
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
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式"
      },
      {
        "clause_id": "C0003",
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
      },
      {
        "clause_id": "C0004",
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
      },
      {
        "clause_id": "C0005",
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证"
      },
      {
        "clause_id": "C0006",
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
      },
      {
        "clause_id": "C0007",
        "location": "第二条第2项",
        "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        ],
        "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
      },
      {
        "clause_id": "C0008",
        "location": "第二条第3项",
        "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        ],
        "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
      },
      {
        "clause_id": "C0009",
        "location": "第三条 盈亏分担",
        "title": "盈亏分担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条 盈亏分担"
        ],
        "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
      },
      {
        "clause_id": "C0010",
        "location": "第四条 费用负担",
        "title": "费用负担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条 费用负担"
        ],
        "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
      },
      {
        "clause_id": "C0011",
        "location": "第五条 合同的变更与解除",
        "title": "合同的变更与解除",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除"
        ],
        "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
      },
      {
        "clause_id": "C0012",
        "location": "第五条第1项",
        "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        ],
        "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
      },
      {
        "clause_id": "C0013",
        "location": "第五条第2项",
        "title": "2、一方当事人丧失实际履约能力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "2、一方当事人丧失实际履约能力。"
        ],
        "text": "2、一方当事人丧失实际履约能力。"
      },
      {
        "clause_id": "C0014",
        "location": "第五条第3项",
        "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        ],
        "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
      },
      {
        "clause_id": "C0015",
        "location": "第五条第4项",
        "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        ],
        "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
      },
      {
        "clause_id": "C0016",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "第六条 争议的解决"
      },
      {
        "clause_id": "C0017",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
      },
      {
        "clause_id": "C0018",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "☑ 向广州仲裁委员会申请仲裁；"
      },
      {
        "clause_id": "C0019",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "使用说明",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "□ 向有管辖权的人民法院起诉。"
      },
      {
        "clause_id": "C0020",
        "location": "第七条 合同生效的条件和日期",
        "title": "合同生效的条件和日期",
        "section_type": "正式合同条款",
        "heading_path": [
          "第七条 合同生效的条件和日期"
        ],
        "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
      },
      {
        "clause_id": "C0021",
        "location": "第八条",
        "title": "第八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第八条"
        ],
        "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
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
    "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EQT-02-01",
    "element_id": "equity_contribution_liability_1",
    "review_id": "EQT-02-01",
    "search_targets": [
      "认缴、实缴金额及出资期限"
    ],
    "query_patterns": [
      "认缴.{0,12}\\d+万?元.{0,35}实缴.{0,12}\\d+万?元.{0,50}(?:出资期限|缴付期限).{0,10}\\d{4}年\\d{1,2}月\\d{1,2}日"
    ],
    "query_semantic_target": "认缴、实缴金额及出资期限",
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
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式"
      },
      {
        "clause_id": "C0003",
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
      },
      {
        "clause_id": "C0004",
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
      },
      {
        "clause_id": "C0005",
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证"
      },
      {
        "clause_id": "C0006",
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
      },
      {
        "clause_id": "C0007",
        "location": "第二条第2项",
        "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        ],
        "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
      },
      {
        "clause_id": "C0008",
        "location": "第二条第3项",
        "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        ],
        "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
      },
      {
        "clause_id": "C0009",
        "location": "第三条 盈亏分担",
        "title": "盈亏分担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条 盈亏分担"
        ],
        "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
      },
      {
        "clause_id": "C0010",
        "location": "第四条 费用负担",
        "title": "费用负担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条 费用负担"
        ],
        "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
      },
      {
        "clause_id": "C0011",
        "location": "第五条 合同的变更与解除",
        "title": "合同的变更与解除",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除"
        ],
        "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
      },
      {
        "clause_id": "C0012",
        "location": "第五条第1项",
        "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        ],
        "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
      },
      {
        "clause_id": "C0013",
        "location": "第五条第2项",
        "title": "2、一方当事人丧失实际履约能力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "2、一方当事人丧失实际履约能力。"
        ],
        "text": "2、一方当事人丧失实际履约能力。"
      },
      {
        "clause_id": "C0014",
        "location": "第五条第3项",
        "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        ],
        "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
      },
      {
        "clause_id": "C0015",
        "location": "第五条第4项",
        "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        ],
        "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
      },
      {
        "clause_id": "C0016",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "第六条 争议的解决"
      },
      {
        "clause_id": "C0017",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
      },
      {
        "clause_id": "C0018",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "☑ 向广州仲裁委员会申请仲裁；"
      },
      {
        "clause_id": "C0019",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "使用说明",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "□ 向有管辖权的人民法院起诉。"
      },
      {
        "clause_id": "C0020",
        "location": "第七条 合同生效的条件和日期",
        "title": "合同生效的条件和日期",
        "section_type": "正式合同条款",
        "heading_path": [
          "第七条 合同生效的条件和日期"
        ],
        "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
      },
      {
        "clause_id": "C0021",
        "location": "第八条",
        "title": "第八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第八条"
        ],
        "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
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
    "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EQT-02-01",
    "element_id": "equity_contribution_liability_2",
    "review_id": "EQT-02-01",
    "search_targets": [
      "未缴出资责任的承担及法定责任保留"
    ],
    "query_patterns": [
      "(?:未缴出资|未届期出资|出资瑕疵).{0,60}(?:承担|责任).{0,45}(?:法定|不得对抗|不影响)",
      "全部实缴.{0,20}不存在出资瑕疵"
    ],
    "query_semantic_target": "未缴出资责任的承担及法定责任保留",
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
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式"
      },
      {
        "clause_id": "C0003",
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
      },
      {
        "clause_id": "C0004",
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
      },
      {
        "clause_id": "C0005",
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证"
      },
      {
        "clause_id": "C0006",
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
      },
      {
        "clause_id": "C0007",
        "location": "第二条第2项",
        "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        ],
        "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
      },
      {
        "clause_id": "C0008",
        "location": "第二条第3项",
        "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        ],
        "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
      },
      {
        "clause_id": "C0009",
        "location": "第三条 盈亏分担",
        "title": "盈亏分担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条 盈亏分担"
        ],
        "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
      },
      {
        "clause_id": "C0010",
        "location": "第四条 费用负担",
        "title": "费用负担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条 费用负担"
        ],
        "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
      },
      {
        "clause_id": "C0011",
        "location": "第五条 合同的变更与解除",
        "title": "合同的变更与解除",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除"
        ],
        "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
      },
      {
        "clause_id": "C0012",
        "location": "第五条第1项",
        "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        ],
        "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
      },
      {
        "clause_id": "C0013",
        "location": "第五条第2项",
        "title": "2、一方当事人丧失实际履约能力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "2、一方当事人丧失实际履约能力。"
        ],
        "text": "2、一方当事人丧失实际履约能力。"
      },
      {
        "clause_id": "C0014",
        "location": "第五条第3项",
        "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        ],
        "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
      },
      {
        "clause_id": "C0015",
        "location": "第五条第4项",
        "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        ],
        "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
      },
      {
        "clause_id": "C0016",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "第六条 争议的解决"
      },
      {
        "clause_id": "C0017",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
      },
      {
        "clause_id": "C0018",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "☑ 向广州仲裁委员会申请仲裁；"
      },
      {
        "clause_id": "C0019",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "使用说明",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "□ 向有管辖权的人民法院起诉。"
      },
      {
        "clause_id": "C0020",
        "location": "第七条 合同生效的条件和日期",
        "title": "合同生效的条件和日期",
        "section_type": "正式合同条款",
        "heading_path": [
          "第七条 合同生效的条件和日期"
        ],
        "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
      },
      {
        "clause_id": "C0021",
        "location": "第八条",
        "title": "第八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第八条"
        ],
        "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
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
    "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EQT-11-01",
    "element_id": "equity_warranties_remedies_1",
    "review_id": "EQT-11-01",
    "search_targets": [
      "股权负担和财务债务的陈述保证"
    ],
    "query_patterns": [
      "(?:保证|承诺).{0,60}(?:无质押|无冻结|无权利负担).{0,70}(?:债务|财务).{0,20}(?:披露|真实)"
    ],
    "query_semantic_target": "股权负担和财务债务的陈述保证",
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
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式"
      },
      {
        "clause_id": "C0003",
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
      },
      {
        "clause_id": "C0004",
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
      },
      {
        "clause_id": "C0005",
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证"
      },
      {
        "clause_id": "C0006",
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
      },
      {
        "clause_id": "C0007",
        "location": "第二条第2项",
        "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        ],
        "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
      },
      {
        "clause_id": "C0008",
        "location": "第二条第3项",
        "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        ],
        "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
      },
      {
        "clause_id": "C0009",
        "location": "第三条 盈亏分担",
        "title": "盈亏分担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条 盈亏分担"
        ],
        "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
      },
      {
        "clause_id": "C0010",
        "location": "第四条 费用负担",
        "title": "费用负担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条 费用负担"
        ],
        "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
      },
      {
        "clause_id": "C0011",
        "location": "第五条 合同的变更与解除",
        "title": "合同的变更与解除",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除"
        ],
        "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
      },
      {
        "clause_id": "C0012",
        "location": "第五条第1项",
        "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        ],
        "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
      },
      {
        "clause_id": "C0013",
        "location": "第五条第2项",
        "title": "2、一方当事人丧失实际履约能力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "2、一方当事人丧失实际履约能力。"
        ],
        "text": "2、一方当事人丧失实际履约能力。"
      },
      {
        "clause_id": "C0014",
        "location": "第五条第3项",
        "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        ],
        "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
      },
      {
        "clause_id": "C0015",
        "location": "第五条第4项",
        "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        ],
        "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
      },
      {
        "clause_id": "C0016",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "第六条 争议的解决"
      },
      {
        "clause_id": "C0017",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
      },
      {
        "clause_id": "C0018",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "☑ 向广州仲裁委员会申请仲裁；"
      },
      {
        "clause_id": "C0019",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "使用说明",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "□ 向有管辖权的人民法院起诉。"
      },
      {
        "clause_id": "C0020",
        "location": "第七条 合同生效的条件和日期",
        "title": "合同生效的条件和日期",
        "section_type": "正式合同条款",
        "heading_path": [
          "第七条 合同生效的条件和日期"
        ],
        "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
      },
      {
        "clause_id": "C0021",
        "location": "第八条",
        "title": "第八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第八条"
        ],
        "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
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
    "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EQT-11-01",
    "element_id": "equity_warranties_remedies_2",
    "review_id": "EQT-11-01",
    "search_targets": [
      "陈述不实的赔偿或退出救济"
    ],
    "query_patterns": [
      "(?:陈述不实|违反保证|隐瞒债务).{0,50}(?:赔偿|解除|退款)"
    ],
    "query_semantic_target": "陈述不实的赔偿或退出救济",
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
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式"
      },
      {
        "clause_id": "C0003",
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
      },
      {
        "clause_id": "C0004",
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
      },
      {
        "clause_id": "C0005",
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证"
      },
      {
        "clause_id": "C0006",
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
      },
      {
        "clause_id": "C0007",
        "location": "第二条第2项",
        "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        ],
        "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
      },
      {
        "clause_id": "C0008",
        "location": "第二条第3项",
        "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        ],
        "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
      },
      {
        "clause_id": "C0009",
        "location": "第三条 盈亏分担",
        "title": "盈亏分担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条 盈亏分担"
        ],
        "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
      },
      {
        "clause_id": "C0010",
        "location": "第四条 费用负担",
        "title": "费用负担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条 费用负担"
        ],
        "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
      },
      {
        "clause_id": "C0011",
        "location": "第五条 合同的变更与解除",
        "title": "合同的变更与解除",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除"
        ],
        "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
      },
      {
        "clause_id": "C0012",
        "location": "第五条第1项",
        "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        ],
        "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
      },
      {
        "clause_id": "C0013",
        "location": "第五条第2项",
        "title": "2、一方当事人丧失实际履约能力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "2、一方当事人丧失实际履约能力。"
        ],
        "text": "2、一方当事人丧失实际履约能力。"
      },
      {
        "clause_id": "C0014",
        "location": "第五条第3项",
        "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        ],
        "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
      },
      {
        "clause_id": "C0015",
        "location": "第五条第4项",
        "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        ],
        "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
      },
      {
        "clause_id": "C0016",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "第六条 争议的解决"
      },
      {
        "clause_id": "C0017",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
      },
      {
        "clause_id": "C0018",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "☑ 向广州仲裁委员会申请仲裁；"
      },
      {
        "clause_id": "C0019",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "使用说明",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "□ 向有管辖权的人民法院起诉。"
      },
      {
        "clause_id": "C0020",
        "location": "第七条 合同生效的条件和日期",
        "title": "合同生效的条件和日期",
        "section_type": "正式合同条款",
        "heading_path": [
          "第七条 合同生效的条件和日期"
        ],
        "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
      },
      {
        "clause_id": "C0021",
        "location": "第八条",
        "title": "第八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第八条"
        ],
        "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
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
    "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EQT-03-01",
    "element_id": "equity_transfer_restrictions_1",
    "review_id": "EQT-03-01",
    "search_targets": [
      "公司章程转让限制核对"
    ],
    "query_patterns": [
      "(?:核对|核验|遵守).{0,30}章程.{0,25}转让限制"
    ],
    "query_semantic_target": "公司章程转让限制核对",
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
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式"
      },
      {
        "clause_id": "C0003",
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
      },
      {
        "clause_id": "C0004",
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
      },
      {
        "clause_id": "C0005",
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证"
      },
      {
        "clause_id": "C0006",
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
      },
      {
        "clause_id": "C0007",
        "location": "第二条第2项",
        "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        ],
        "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
      },
      {
        "clause_id": "C0008",
        "location": "第二条第3项",
        "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        ],
        "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
      },
      {
        "clause_id": "C0009",
        "location": "第三条 盈亏分担",
        "title": "盈亏分担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条 盈亏分担"
        ],
        "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
      },
      {
        "clause_id": "C0010",
        "location": "第四条 费用负担",
        "title": "费用负担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条 费用负担"
        ],
        "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
      },
      {
        "clause_id": "C0011",
        "location": "第五条 合同的变更与解除",
        "title": "合同的变更与解除",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除"
        ],
        "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
      },
      {
        "clause_id": "C0012",
        "location": "第五条第1项",
        "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        ],
        "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
      },
      {
        "clause_id": "C0013",
        "location": "第五条第2项",
        "title": "2、一方当事人丧失实际履约能力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "2、一方当事人丧失实际履约能力。"
        ],
        "text": "2、一方当事人丧失实际履约能力。"
      },
      {
        "clause_id": "C0014",
        "location": "第五条第3项",
        "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        ],
        "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
      },
      {
        "clause_id": "C0015",
        "location": "第五条第4项",
        "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        ],
        "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
      },
      {
        "clause_id": "C0016",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "第六条 争议的解决"
      },
      {
        "clause_id": "C0017",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
      },
      {
        "clause_id": "C0018",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "☑ 向广州仲裁委员会申请仲裁；"
      },
      {
        "clause_id": "C0019",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "使用说明",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "□ 向有管辖权的人民法院起诉。"
      },
      {
        "clause_id": "C0020",
        "location": "第七条 合同生效的条件和日期",
        "title": "合同生效的条件和日期",
        "section_type": "正式合同条款",
        "heading_path": [
          "第七条 合同生效的条件和日期"
        ],
        "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
      },
      {
        "clause_id": "C0021",
        "location": "第八条",
        "title": "第八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第八条"
        ],
        "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
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
    "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EQT-03-01",
    "element_id": "equity_transfer_restrictions_2",
    "review_id": "EQT-03-01",
    "search_targets": [
      "向其他股东通知同等条件或不触发外部转让"
    ],
    "query_patterns": [
      "其他股东.{0,50}(?:数量|比例).{0,30}价格.{0,30}(?:支付|期限)",
      "股东之间内部转让"
    ],
    "query_semantic_target": "向其他股东通知同等条件或不触发外部转让",
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
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式"
      },
      {
        "clause_id": "C0003",
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
      },
      {
        "clause_id": "C0004",
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
      },
      {
        "clause_id": "C0005",
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证"
      },
      {
        "clause_id": "C0006",
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
      },
      {
        "clause_id": "C0007",
        "location": "第二条第2项",
        "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        ],
        "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
      },
      {
        "clause_id": "C0008",
        "location": "第二条第3项",
        "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        ],
        "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
      },
      {
        "clause_id": "C0009",
        "location": "第三条 盈亏分担",
        "title": "盈亏分担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条 盈亏分担"
        ],
        "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
      },
      {
        "clause_id": "C0010",
        "location": "第四条 费用负担",
        "title": "费用负担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条 费用负担"
        ],
        "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
      },
      {
        "clause_id": "C0011",
        "location": "第五条 合同的变更与解除",
        "title": "合同的变更与解除",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除"
        ],
        "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
      },
      {
        "clause_id": "C0012",
        "location": "第五条第1项",
        "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        ],
        "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
      },
      {
        "clause_id": "C0013",
        "location": "第五条第2项",
        "title": "2、一方当事人丧失实际履约能力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "2、一方当事人丧失实际履约能力。"
        ],
        "text": "2、一方当事人丧失实际履约能力。"
      },
      {
        "clause_id": "C0014",
        "location": "第五条第3项",
        "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        ],
        "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
      },
      {
        "clause_id": "C0015",
        "location": "第五条第4项",
        "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        ],
        "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
      },
      {
        "clause_id": "C0016",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "第六条 争议的解决"
      },
      {
        "clause_id": "C0017",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
      },
      {
        "clause_id": "C0018",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "☑ 向广州仲裁委员会申请仲裁；"
      },
      {
        "clause_id": "C0019",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "使用说明",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "□ 向有管辖权的人民法院起诉。"
      },
      {
        "clause_id": "C0020",
        "location": "第七条 合同生效的条件和日期",
        "title": "合同生效的条件和日期",
        "section_type": "正式合同条款",
        "heading_path": [
          "第七条 合同生效的条件和日期"
        ],
        "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
      },
      {
        "clause_id": "C0021",
        "location": "第八条",
        "title": "第八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第八条"
        ],
        "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
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
    "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EQT-03-01",
    "element_id": "equity_transfer_restrictions_3",
    "review_id": "EQT-03-01",
    "search_targets": [
      "优先购买权的依法行使或书面放弃"
    ],
    "query_patterns": [
      "优先购买权.{0,40}(?:三十|30)日|其他股东.{0,20}书面放弃.{0,15}优先购买权|股东之间内部转让"
    ],
    "query_semantic_target": "优先购买权的依法行使或书面放弃",
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
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式"
      },
      {
        "clause_id": "C0003",
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
      },
      {
        "clause_id": "C0004",
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
      },
      {
        "clause_id": "C0005",
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证"
      },
      {
        "clause_id": "C0006",
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
      },
      {
        "clause_id": "C0007",
        "location": "第二条第2项",
        "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        ],
        "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
      },
      {
        "clause_id": "C0008",
        "location": "第二条第3项",
        "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        ],
        "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
      },
      {
        "clause_id": "C0009",
        "location": "第三条 盈亏分担",
        "title": "盈亏分担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条 盈亏分担"
        ],
        "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
      },
      {
        "clause_id": "C0010",
        "location": "第四条 费用负担",
        "title": "费用负担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条 费用负担"
        ],
        "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
      },
      {
        "clause_id": "C0011",
        "location": "第五条 合同的变更与解除",
        "title": "合同的变更与解除",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除"
        ],
        "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
      },
      {
        "clause_id": "C0012",
        "location": "第五条第1项",
        "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        ],
        "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
      },
      {
        "clause_id": "C0013",
        "location": "第五条第2项",
        "title": "2、一方当事人丧失实际履约能力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "2、一方当事人丧失实际履约能力。"
        ],
        "text": "2、一方当事人丧失实际履约能力。"
      },
      {
        "clause_id": "C0014",
        "location": "第五条第3项",
        "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        ],
        "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
      },
      {
        "clause_id": "C0015",
        "location": "第五条第4项",
        "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        ],
        "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
      },
      {
        "clause_id": "C0016",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "第六条 争议的解决"
      },
      {
        "clause_id": "C0017",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
      },
      {
        "clause_id": "C0018",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "☑ 向广州仲裁委员会申请仲裁；"
      },
      {
        "clause_id": "C0019",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "使用说明",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "□ 向有管辖权的人民法院起诉。"
      },
      {
        "clause_id": "C0020",
        "location": "第七条 合同生效的条件和日期",
        "title": "合同生效的条件和日期",
        "section_type": "正式合同条款",
        "heading_path": [
          "第七条 合同生效的条件和日期"
        ],
        "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
      },
      {
        "clause_id": "C0021",
        "location": "第八条",
        "title": "第八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第八条"
        ],
        "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
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
    "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EQT-04-01",
    "element_id": "equity_price_payment_1",
    "review_id": "EQT-04-01",
    "search_targets": [
      "价款或投资总额"
    ],
    "query_patterns": [
      "(?:转让价款|投资款|增资款|投资总额)[为：:]?(?:人民币)?\\d+(?:\\.\\d+)?万?元"
    ],
    "query_semantic_target": "价款或投资总额",
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
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式"
      },
      {
        "clause_id": "C0003",
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
      },
      {
        "clause_id": "C0004",
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
      },
      {
        "clause_id": "C0005",
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证"
      },
      {
        "clause_id": "C0006",
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
      },
      {
        "clause_id": "C0007",
        "location": "第二条第2项",
        "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        ],
        "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
      },
      {
        "clause_id": "C0008",
        "location": "第二条第3项",
        "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        ],
        "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
      },
      {
        "clause_id": "C0009",
        "location": "第三条 盈亏分担",
        "title": "盈亏分担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条 盈亏分担"
        ],
        "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
      },
      {
        "clause_id": "C0010",
        "location": "第四条 费用负担",
        "title": "费用负担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条 费用负担"
        ],
        "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
      },
      {
        "clause_id": "C0011",
        "location": "第五条 合同的变更与解除",
        "title": "合同的变更与解除",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除"
        ],
        "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
      },
      {
        "clause_id": "C0012",
        "location": "第五条第1项",
        "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        ],
        "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
      },
      {
        "clause_id": "C0013",
        "location": "第五条第2项",
        "title": "2、一方当事人丧失实际履约能力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "2、一方当事人丧失实际履约能力。"
        ],
        "text": "2、一方当事人丧失实际履约能力。"
      },
      {
        "clause_id": "C0014",
        "location": "第五条第3项",
        "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        ],
        "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
      },
      {
        "clause_id": "C0015",
        "location": "第五条第4项",
        "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        ],
        "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
      },
      {
        "clause_id": "C0016",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "第六条 争议的解决"
      },
      {
        "clause_id": "C0017",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
      },
      {
        "clause_id": "C0018",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "☑ 向广州仲裁委员会申请仲裁；"
      },
      {
        "clause_id": "C0019",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "使用说明",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "□ 向有管辖权的人民法院起诉。"
      },
      {
        "clause_id": "C0020",
        "location": "第七条 合同生效的条件和日期",
        "title": "合同生效的条件和日期",
        "section_type": "正式合同条款",
        "heading_path": [
          "第七条 合同生效的条件和日期"
        ],
        "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
      },
      {
        "clause_id": "C0021",
        "location": "第八条",
        "title": "第八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第八条"
        ],
        "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
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
    "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EQT-04-01",
    "element_id": "equity_price_payment_2",
    "review_id": "EQT-04-01",
    "search_targets": [
      "支付节点、条件或期限"
    ],
    "query_patterns": [
      "(?:交割|签署|生效).{0,20}\\d+日内.{0,25}支付|支付.{0,30}\\d{4}年\\d{1,2}月\\d{1,2}日"
    ],
    "query_semantic_target": "支付节点、条件或期限",
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
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式"
      },
      {
        "clause_id": "C0003",
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
      },
      {
        "clause_id": "C0004",
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
      },
      {
        "clause_id": "C0005",
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证"
      },
      {
        "clause_id": "C0006",
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
      },
      {
        "clause_id": "C0007",
        "location": "第二条第2项",
        "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        ],
        "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
      },
      {
        "clause_id": "C0008",
        "location": "第二条第3项",
        "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        ],
        "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
      },
      {
        "clause_id": "C0009",
        "location": "第三条 盈亏分担",
        "title": "盈亏分担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条 盈亏分担"
        ],
        "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
      },
      {
        "clause_id": "C0010",
        "location": "第四条 费用负担",
        "title": "费用负担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条 费用负担"
        ],
        "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
      },
      {
        "clause_id": "C0011",
        "location": "第五条 合同的变更与解除",
        "title": "合同的变更与解除",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除"
        ],
        "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
      },
      {
        "clause_id": "C0012",
        "location": "第五条第1项",
        "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        ],
        "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
      },
      {
        "clause_id": "C0013",
        "location": "第五条第2项",
        "title": "2、一方当事人丧失实际履约能力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "2、一方当事人丧失实际履约能力。"
        ],
        "text": "2、一方当事人丧失实际履约能力。"
      },
      {
        "clause_id": "C0014",
        "location": "第五条第3项",
        "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        ],
        "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
      },
      {
        "clause_id": "C0015",
        "location": "第五条第4项",
        "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        ],
        "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
      },
      {
        "clause_id": "C0016",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "第六条 争议的解决"
      },
      {
        "clause_id": "C0017",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
      },
      {
        "clause_id": "C0018",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "☑ 向广州仲裁委员会申请仲裁；"
      },
      {
        "clause_id": "C0019",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "使用说明",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "□ 向有管辖权的人民法院起诉。"
      },
      {
        "clause_id": "C0020",
        "location": "第七条 合同生效的条件和日期",
        "title": "合同生效的条件和日期",
        "section_type": "正式合同条款",
        "heading_path": [
          "第七条 合同生效的条件和日期"
        ],
        "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
      },
      {
        "clause_id": "C0021",
        "location": "第八条",
        "title": "第八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第八条"
        ],
        "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
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
    "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EQT-05-01",
    "element_id": "equity_closing_registration_1",
    "review_id": "EQT-05-01",
    "search_targets": [
      "交割条件及未满足的处理"
    ],
    "query_patterns": [
      "交割条件.{0,40}(?:满足|完成|具备).{0,60}(?:未满足|未完成).{0,30}(?:解除|延期|退款)"
    ],
    "query_semantic_target": "交割条件及未满足的处理",
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
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式"
      },
      {
        "clause_id": "C0003",
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
      },
      {
        "clause_id": "C0004",
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
      },
      {
        "clause_id": "C0005",
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证"
      },
      {
        "clause_id": "C0006",
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
      },
      {
        "clause_id": "C0007",
        "location": "第二条第2项",
        "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        ],
        "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
      },
      {
        "clause_id": "C0008",
        "location": "第二条第3项",
        "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        ],
        "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
      },
      {
        "clause_id": "C0009",
        "location": "第三条 盈亏分担",
        "title": "盈亏分担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条 盈亏分担"
        ],
        "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
      },
      {
        "clause_id": "C0010",
        "location": "第四条 费用负担",
        "title": "费用负担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条 费用负担"
        ],
        "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
      },
      {
        "clause_id": "C0011",
        "location": "第五条 合同的变更与解除",
        "title": "合同的变更与解除",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除"
        ],
        "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
      },
      {
        "clause_id": "C0012",
        "location": "第五条第1项",
        "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        ],
        "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
      },
      {
        "clause_id": "C0013",
        "location": "第五条第2项",
        "title": "2、一方当事人丧失实际履约能力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "2、一方当事人丧失实际履约能力。"
        ],
        "text": "2、一方当事人丧失实际履约能力。"
      },
      {
        "clause_id": "C0014",
        "location": "第五条第3项",
        "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        ],
        "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
      },
      {
        "clause_id": "C0015",
        "location": "第五条第4项",
        "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        ],
        "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
      },
      {
        "clause_id": "C0016",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "第六条 争议的解决"
      },
      {
        "clause_id": "C0017",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
      },
      {
        "clause_id": "C0018",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "☑ 向广州仲裁委员会申请仲裁；"
      },
      {
        "clause_id": "C0019",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "使用说明",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "□ 向有管辖权的人民法院起诉。"
      },
      {
        "clause_id": "C0020",
        "location": "第七条 合同生效的条件和日期",
        "title": "合同生效的条件和日期",
        "section_type": "正式合同条款",
        "heading_path": [
          "第七条 合同生效的条件和日期"
        ],
        "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
      },
      {
        "clause_id": "C0021",
        "location": "第八条",
        "title": "第八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第八条"
        ],
        "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
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
    "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EQT-05-01",
    "element_id": "equity_closing_registration_2",
    "review_id": "EQT-05-01",
    "search_targets": [
      "股东名册及出资证明更新"
    ],
    "query_patterns": [
      "(?:更新|修改|记载).{0,15}股东名册.{0,50}(?:出资证明|公司章程)"
    ],
    "query_semantic_target": "股东名册及出资证明更新",
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
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式"
      },
      {
        "clause_id": "C0003",
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
      },
      {
        "clause_id": "C0004",
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
      },
      {
        "clause_id": "C0005",
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证"
      },
      {
        "clause_id": "C0006",
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
      },
      {
        "clause_id": "C0007",
        "location": "第二条第2项",
        "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        ],
        "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
      },
      {
        "clause_id": "C0008",
        "location": "第二条第3项",
        "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        ],
        "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
      },
      {
        "clause_id": "C0009",
        "location": "第三条 盈亏分担",
        "title": "盈亏分担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条 盈亏分担"
        ],
        "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
      },
      {
        "clause_id": "C0010",
        "location": "第四条 费用负担",
        "title": "费用负担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条 费用负担"
        ],
        "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
      },
      {
        "clause_id": "C0011",
        "location": "第五条 合同的变更与解除",
        "title": "合同的变更与解除",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除"
        ],
        "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
      },
      {
        "clause_id": "C0012",
        "location": "第五条第1项",
        "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        ],
        "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
      },
      {
        "clause_id": "C0013",
        "location": "第五条第2项",
        "title": "2、一方当事人丧失实际履约能力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "2、一方当事人丧失实际履约能力。"
        ],
        "text": "2、一方当事人丧失实际履约能力。"
      },
      {
        "clause_id": "C0014",
        "location": "第五条第3项",
        "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        ],
        "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
      },
      {
        "clause_id": "C0015",
        "location": "第五条第4项",
        "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        ],
        "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
      },
      {
        "clause_id": "C0016",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "第六条 争议的解决"
      },
      {
        "clause_id": "C0017",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
      },
      {
        "clause_id": "C0018",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "☑ 向广州仲裁委员会申请仲裁；"
      },
      {
        "clause_id": "C0019",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "使用说明",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "□ 向有管辖权的人民法院起诉。"
      },
      {
        "clause_id": "C0020",
        "location": "第七条 合同生效的条件和日期",
        "title": "合同生效的条件和日期",
        "section_type": "正式合同条款",
        "heading_path": [
          "第七条 合同生效的条件和日期"
        ],
        "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
      },
      {
        "clause_id": "C0021",
        "location": "第八条",
        "title": "第八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第八条"
        ],
        "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
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
    "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EQT-05-01",
    "element_id": "equity_closing_registration_3",
    "review_id": "EQT-05-01",
    "search_targets": [
      "办理变更登记的责任人与期限"
    ],
    "query_patterns": [
      "(?:目标公司|双方).{0,30}\\d+日内.{0,20}(?:工商变更|变更登记)"
    ],
    "query_semantic_target": "办理变更登记的责任人与期限",
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
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
      },
      {
        "clause_id": "C0002",
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式"
      },
      {
        "clause_id": "C0003",
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
      },
      {
        "clause_id": "C0004",
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
      },
      {
        "clause_id": "C0005",
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证"
      },
      {
        "clause_id": "C0006",
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
      },
      {
        "clause_id": "C0007",
        "location": "第二条第2项",
        "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        ],
        "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
      },
      {
        "clause_id": "C0008",
        "location": "第二条第3项",
        "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        ],
        "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
      },
      {
        "clause_id": "C0009",
        "location": "第三条 盈亏分担",
        "title": "盈亏分担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条 盈亏分担"
        ],
        "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
      },
      {
        "clause_id": "C0010",
        "location": "第四条 费用负担",
        "title": "费用负担",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条 费用负担"
        ],
        "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
      },
      {
        "clause_id": "C0011",
        "location": "第五条 合同的变更与解除",
        "title": "合同的变更与解除",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除"
        ],
        "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
      },
      {
        "clause_id": "C0012",
        "location": "第五条第1项",
        "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        ],
        "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
      },
      {
        "clause_id": "C0013",
        "location": "第五条第2项",
        "title": "2、一方当事人丧失实际履约能力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "2、一方当事人丧失实际履约能力。"
        ],
        "text": "2、一方当事人丧失实际履约能力。"
      },
      {
        "clause_id": "C0014",
        "location": "第五条第3项",
        "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        ],
        "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
      },
      {
        "clause_id": "C0015",
        "location": "第五条第4项",
        "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条 合同的变更与解除",
          "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        ],
        "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
      },
      {
        "clause_id": "C0016",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "第六条 争议的解决"
      },
      {
        "clause_id": "C0017",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
      },
      {
        "clause_id": "C0018",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "☑ 向广州仲裁委员会申请仲裁；"
      },
      {
        "clause_id": "C0019",
        "location": "第六条 争议的解决",
        "title": "争议的解决",
        "section_type": "使用说明",
        "heading_path": [
          "第六条 争议的解决"
        ],
        "text": "□ 向有管辖权的人民法院起诉。"
      },
      {
        "clause_id": "C0020",
        "location": "第七条 合同生效的条件和日期",
        "title": "合同生效的条件和日期",
        "section_type": "正式合同条款",
        "heading_path": [
          "第七条 合同生效的条件和日期"
        ],
        "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
      },
      {
        "clause_id": "C0021",
        "location": "第八条",
        "title": "第八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第八条"
        ],
        "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
        "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条 股权转让价格与付款方式",
        "title": "股权转让价格与付款方式",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式"
        ],
        "text": "第一条 股权转让价格与付款方式",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第1项",
        "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        ],
        "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第一条第2项",
        "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条 股权转让价格与付款方式",
          "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        ],
        "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条 保证",
        "title": "保证",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证"
        ],
        "text": "第二条 保证",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
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
        "location": "第二条第1项",
        "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条 保证",
          "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        ],
        "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
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
    "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "S-00-03",
    "element_id": "core_contract_arrangement",
    "review_id": "S-00-03",
    "search_targets": [
      "合同存在可验证的“通知与送达”实质条款内容"
    ],
    "query_patterns": [
      "合同存在可验证的“通知与送达”实质条款内容"
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
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021"
    ],
    "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  }
]
```

## EQT-01-01

```json
{
  "rule_id": "EQT-01-01",
  "applicability": {
    "review_id": "EQT-01-01",
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
  "reason": "未找到明确约定：交易主体及目标公司名称、持股比例及合法权属声明。",
  "coverage_elements": [
    {
      "review_id": "EQT-01-01",
      "element_id": "equity_title_1",
      "proposition": "交易主体及目标公司名称",
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
      "review_id": "EQT-01-01",
      "element_id": "equity_title_2",
      "proposition": "持股比例及合法权属声明",
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
      "element_id": "equity_title_1",
      "review_id": "EQT-01-01",
      "search_targets": [
        "交易主体及目标公司名称"
      ],
      "query_patterns": [
        "(?:转让方|投资方|股东)[：:][^，。；_]{2,50}.{0,70}目标公司[：:][^，。；_]{2,50}"
      ],
      "query_semantic_target": "交易主体及目标公司名称",
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
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式"
        },
        {
          "clause_id": "C0003",
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        },
        {
          "clause_id": "C0004",
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        },
        {
          "clause_id": "C0005",
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证"
        },
        {
          "clause_id": "C0006",
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        },
        {
          "clause_id": "C0007",
          "location": "第二条第2项",
          "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
          ],
          "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        },
        {
          "clause_id": "C0008",
          "location": "第二条第3项",
          "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
          ],
          "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        },
        {
          "clause_id": "C0009",
          "location": "第三条 盈亏分担",
          "title": "盈亏分担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条 盈亏分担"
          ],
          "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
        },
        {
          "clause_id": "C0010",
          "location": "第四条 费用负担",
          "title": "费用负担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条 费用负担"
          ],
          "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
        },
        {
          "clause_id": "C0011",
          "location": "第五条 合同的变更与解除",
          "title": "合同的变更与解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除"
          ],
          "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
        },
        {
          "clause_id": "C0012",
          "location": "第五条第1项",
          "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
          ],
          "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        },
        {
          "clause_id": "C0013",
          "location": "第五条第2项",
          "title": "2、一方当事人丧失实际履约能力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "2、一方当事人丧失实际履约能力。"
          ],
          "text": "2、一方当事人丧失实际履约能力。"
        },
        {
          "clause_id": "C0014",
          "location": "第五条第3项",
          "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
          ],
          "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        },
        {
          "clause_id": "C0015",
          "location": "第五条第4项",
          "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "4、因情况发生变化，经过双方协商同意变更或解除合同。"
          ],
          "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        },
        {
          "clause_id": "C0016",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "第六条 争议的解决"
        },
        {
          "clause_id": "C0017",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
        },
        {
          "clause_id": "C0018",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "☑ 向广州仲裁委员会申请仲裁；"
        },
        {
          "clause_id": "C0019",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "使用说明",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "□ 向有管辖权的人民法院起诉。"
        },
        {
          "clause_id": "C0020",
          "location": "第七条 合同生效的条件和日期",
          "title": "合同生效的条件和日期",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条 合同生效的条件和日期"
          ],
          "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
        },
        {
          "clause_id": "C0021",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
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
      "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "equity_title_2",
      "review_id": "EQT-01-01",
      "search_targets": [
        "持股比例及合法权属声明"
      ],
      "query_patterns": [
        "(?:持有|转让|认购|股权比例).{0,15}\\d+(?:\\.\\d+)?[%％].{0,50}(?:合法|权属|处分权)"
      ],
      "query_semantic_target": "持股比例及合法权属声明",
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
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式"
        },
        {
          "clause_id": "C0003",
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        },
        {
          "clause_id": "C0004",
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        },
        {
          "clause_id": "C0005",
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证"
        },
        {
          "clause_id": "C0006",
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        },
        {
          "clause_id": "C0007",
          "location": "第二条第2项",
          "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
          ],
          "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        },
        {
          "clause_id": "C0008",
          "location": "第二条第3项",
          "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
          ],
          "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        },
        {
          "clause_id": "C0009",
          "location": "第三条 盈亏分担",
          "title": "盈亏分担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条 盈亏分担"
          ],
          "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
        },
        {
          "clause_id": "C0010",
          "location": "第四条 费用负担",
          "title": "费用负担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条 费用负担"
          ],
          "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
        },
        {
          "clause_id": "C0011",
          "location": "第五条 合同的变更与解除",
          "title": "合同的变更与解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除"
          ],
          "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
        },
        {
          "clause_id": "C0012",
          "location": "第五条第1项",
          "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
          ],
          "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        },
        {
          "clause_id": "C0013",
          "location": "第五条第2项",
          "title": "2、一方当事人丧失实际履约能力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "2、一方当事人丧失实际履约能力。"
          ],
          "text": "2、一方当事人丧失实际履约能力。"
        },
        {
          "clause_id": "C0014",
          "location": "第五条第3项",
          "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
          ],
          "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        },
        {
          "clause_id": "C0015",
          "location": "第五条第4项",
          "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "4、因情况发生变化，经过双方协商同意变更或解除合同。"
          ],
          "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        },
        {
          "clause_id": "C0016",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "第六条 争议的解决"
        },
        {
          "clause_id": "C0017",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
        },
        {
          "clause_id": "C0018",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "☑ 向广州仲裁委员会申请仲裁；"
        },
        {
          "clause_id": "C0019",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "使用说明",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "□ 向有管辖权的人民法院起诉。"
        },
        {
          "clause_id": "C0020",
          "location": "第七条 合同生效的条件和日期",
          "title": "合同生效的条件和日期",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条 合同生效的条件和日期"
          ],
          "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
        },
        {
          "clause_id": "C0021",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
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
      "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EQT-02-01

```json
{
  "rule_id": "EQT-02-01",
  "applicability": {
    "review_id": "EQT-02-01",
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
  "reason": "未找到明确约定：认缴、实缴金额及出资期限、未缴出资责任的承担及法定责任保留。",
  "coverage_elements": [
    {
      "review_id": "EQT-02-01",
      "element_id": "equity_contribution_liability_1",
      "proposition": "认缴、实缴金额及出资期限",
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
      "review_id": "EQT-02-01",
      "element_id": "equity_contribution_liability_2",
      "proposition": "未缴出资责任的承担及法定责任保留",
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
      "element_id": "equity_contribution_liability_1",
      "review_id": "EQT-02-01",
      "search_targets": [
        "认缴、实缴金额及出资期限"
      ],
      "query_patterns": [
        "认缴.{0,12}\\d+万?元.{0,35}实缴.{0,12}\\d+万?元.{0,50}(?:出资期限|缴付期限).{0,10}\\d{4}年\\d{1,2}月\\d{1,2}日"
      ],
      "query_semantic_target": "认缴、实缴金额及出资期限",
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
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式"
        },
        {
          "clause_id": "C0003",
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        },
        {
          "clause_id": "C0004",
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        },
        {
          "clause_id": "C0005",
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证"
        },
        {
          "clause_id": "C0006",
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        },
        {
          "clause_id": "C0007",
          "location": "第二条第2项",
          "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
          ],
          "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        },
        {
          "clause_id": "C0008",
          "location": "第二条第3项",
          "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
          ],
          "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        },
        {
          "clause_id": "C0009",
          "location": "第三条 盈亏分担",
          "title": "盈亏分担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条 盈亏分担"
          ],
          "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
        },
        {
          "clause_id": "C0010",
          "location": "第四条 费用负担",
          "title": "费用负担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条 费用负担"
          ],
          "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
        },
        {
          "clause_id": "C0011",
          "location": "第五条 合同的变更与解除",
          "title": "合同的变更与解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除"
          ],
          "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
        },
        {
          "clause_id": "C0012",
          "location": "第五条第1项",
          "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
          ],
          "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        },
        {
          "clause_id": "C0013",
          "location": "第五条第2项",
          "title": "2、一方当事人丧失实际履约能力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "2、一方当事人丧失实际履约能力。"
          ],
          "text": "2、一方当事人丧失实际履约能力。"
        },
        {
          "clause_id": "C0014",
          "location": "第五条第3项",
          "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
          ],
          "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        },
        {
          "clause_id": "C0015",
          "location": "第五条第4项",
          "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "4、因情况发生变化，经过双方协商同意变更或解除合同。"
          ],
          "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        },
        {
          "clause_id": "C0016",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "第六条 争议的解决"
        },
        {
          "clause_id": "C0017",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
        },
        {
          "clause_id": "C0018",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "☑ 向广州仲裁委员会申请仲裁；"
        },
        {
          "clause_id": "C0019",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "使用说明",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "□ 向有管辖权的人民法院起诉。"
        },
        {
          "clause_id": "C0020",
          "location": "第七条 合同生效的条件和日期",
          "title": "合同生效的条件和日期",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条 合同生效的条件和日期"
          ],
          "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
        },
        {
          "clause_id": "C0021",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
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
      "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "equity_contribution_liability_2",
      "review_id": "EQT-02-01",
      "search_targets": [
        "未缴出资责任的承担及法定责任保留"
      ],
      "query_patterns": [
        "(?:未缴出资|未届期出资|出资瑕疵).{0,60}(?:承担|责任).{0,45}(?:法定|不得对抗|不影响)",
        "全部实缴.{0,20}不存在出资瑕疵"
      ],
      "query_semantic_target": "未缴出资责任的承担及法定责任保留",
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
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式"
        },
        {
          "clause_id": "C0003",
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        },
        {
          "clause_id": "C0004",
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        },
        {
          "clause_id": "C0005",
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证"
        },
        {
          "clause_id": "C0006",
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        },
        {
          "clause_id": "C0007",
          "location": "第二条第2项",
          "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
          ],
          "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        },
        {
          "clause_id": "C0008",
          "location": "第二条第3项",
          "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
          ],
          "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        },
        {
          "clause_id": "C0009",
          "location": "第三条 盈亏分担",
          "title": "盈亏分担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条 盈亏分担"
          ],
          "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
        },
        {
          "clause_id": "C0010",
          "location": "第四条 费用负担",
          "title": "费用负担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条 费用负担"
          ],
          "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
        },
        {
          "clause_id": "C0011",
          "location": "第五条 合同的变更与解除",
          "title": "合同的变更与解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除"
          ],
          "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
        },
        {
          "clause_id": "C0012",
          "location": "第五条第1项",
          "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
          ],
          "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        },
        {
          "clause_id": "C0013",
          "location": "第五条第2项",
          "title": "2、一方当事人丧失实际履约能力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "2、一方当事人丧失实际履约能力。"
          ],
          "text": "2、一方当事人丧失实际履约能力。"
        },
        {
          "clause_id": "C0014",
          "location": "第五条第3项",
          "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
          ],
          "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        },
        {
          "clause_id": "C0015",
          "location": "第五条第4项",
          "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "4、因情况发生变化，经过双方协商同意变更或解除合同。"
          ],
          "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        },
        {
          "clause_id": "C0016",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "第六条 争议的解决"
        },
        {
          "clause_id": "C0017",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
        },
        {
          "clause_id": "C0018",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "☑ 向广州仲裁委员会申请仲裁；"
        },
        {
          "clause_id": "C0019",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "使用说明",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "□ 向有管辖权的人民法院起诉。"
        },
        {
          "clause_id": "C0020",
          "location": "第七条 合同生效的条件和日期",
          "title": "合同生效的条件和日期",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条 合同生效的条件和日期"
          ],
          "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
        },
        {
          "clause_id": "C0021",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
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
      "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EQT-11-01

```json
{
  "rule_id": "EQT-11-01",
  "applicability": {
    "review_id": "EQT-11-01",
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
  "reason": "未找到明确约定：股权负担和财务债务的陈述保证、陈述不实的赔偿或退出救济。",
  "coverage_elements": [
    {
      "review_id": "EQT-11-01",
      "element_id": "equity_warranties_remedies_1",
      "proposition": "股权负担和财务债务的陈述保证",
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
      "review_id": "EQT-11-01",
      "element_id": "equity_warranties_remedies_2",
      "proposition": "陈述不实的赔偿或退出救济",
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
      "element_id": "equity_warranties_remedies_1",
      "review_id": "EQT-11-01",
      "search_targets": [
        "股权负担和财务债务的陈述保证"
      ],
      "query_patterns": [
        "(?:保证|承诺).{0,60}(?:无质押|无冻结|无权利负担).{0,70}(?:债务|财务).{0,20}(?:披露|真实)"
      ],
      "query_semantic_target": "股权负担和财务债务的陈述保证",
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
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式"
        },
        {
          "clause_id": "C0003",
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        },
        {
          "clause_id": "C0004",
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        },
        {
          "clause_id": "C0005",
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证"
        },
        {
          "clause_id": "C0006",
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        },
        {
          "clause_id": "C0007",
          "location": "第二条第2项",
          "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
          ],
          "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        },
        {
          "clause_id": "C0008",
          "location": "第二条第3项",
          "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
          ],
          "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        },
        {
          "clause_id": "C0009",
          "location": "第三条 盈亏分担",
          "title": "盈亏分担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条 盈亏分担"
          ],
          "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
        },
        {
          "clause_id": "C0010",
          "location": "第四条 费用负担",
          "title": "费用负担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条 费用负担"
          ],
          "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
        },
        {
          "clause_id": "C0011",
          "location": "第五条 合同的变更与解除",
          "title": "合同的变更与解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除"
          ],
          "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
        },
        {
          "clause_id": "C0012",
          "location": "第五条第1项",
          "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
          ],
          "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        },
        {
          "clause_id": "C0013",
          "location": "第五条第2项",
          "title": "2、一方当事人丧失实际履约能力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "2、一方当事人丧失实际履约能力。"
          ],
          "text": "2、一方当事人丧失实际履约能力。"
        },
        {
          "clause_id": "C0014",
          "location": "第五条第3项",
          "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
          ],
          "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        },
        {
          "clause_id": "C0015",
          "location": "第五条第4项",
          "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "4、因情况发生变化，经过双方协商同意变更或解除合同。"
          ],
          "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        },
        {
          "clause_id": "C0016",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "第六条 争议的解决"
        },
        {
          "clause_id": "C0017",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
        },
        {
          "clause_id": "C0018",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "☑ 向广州仲裁委员会申请仲裁；"
        },
        {
          "clause_id": "C0019",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "使用说明",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "□ 向有管辖权的人民法院起诉。"
        },
        {
          "clause_id": "C0020",
          "location": "第七条 合同生效的条件和日期",
          "title": "合同生效的条件和日期",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条 合同生效的条件和日期"
          ],
          "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
        },
        {
          "clause_id": "C0021",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
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
      "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "equity_warranties_remedies_2",
      "review_id": "EQT-11-01",
      "search_targets": [
        "陈述不实的赔偿或退出救济"
      ],
      "query_patterns": [
        "(?:陈述不实|违反保证|隐瞒债务).{0,50}(?:赔偿|解除|退款)"
      ],
      "query_semantic_target": "陈述不实的赔偿或退出救济",
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
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式"
        },
        {
          "clause_id": "C0003",
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        },
        {
          "clause_id": "C0004",
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        },
        {
          "clause_id": "C0005",
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证"
        },
        {
          "clause_id": "C0006",
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        },
        {
          "clause_id": "C0007",
          "location": "第二条第2项",
          "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
          ],
          "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        },
        {
          "clause_id": "C0008",
          "location": "第二条第3项",
          "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
          ],
          "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        },
        {
          "clause_id": "C0009",
          "location": "第三条 盈亏分担",
          "title": "盈亏分担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条 盈亏分担"
          ],
          "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
        },
        {
          "clause_id": "C0010",
          "location": "第四条 费用负担",
          "title": "费用负担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条 费用负担"
          ],
          "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
        },
        {
          "clause_id": "C0011",
          "location": "第五条 合同的变更与解除",
          "title": "合同的变更与解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除"
          ],
          "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
        },
        {
          "clause_id": "C0012",
          "location": "第五条第1项",
          "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
          ],
          "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        },
        {
          "clause_id": "C0013",
          "location": "第五条第2项",
          "title": "2、一方当事人丧失实际履约能力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "2、一方当事人丧失实际履约能力。"
          ],
          "text": "2、一方当事人丧失实际履约能力。"
        },
        {
          "clause_id": "C0014",
          "location": "第五条第3项",
          "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
          ],
          "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        },
        {
          "clause_id": "C0015",
          "location": "第五条第4项",
          "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "4、因情况发生变化，经过双方协商同意变更或解除合同。"
          ],
          "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        },
        {
          "clause_id": "C0016",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "第六条 争议的解决"
        },
        {
          "clause_id": "C0017",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
        },
        {
          "clause_id": "C0018",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "☑ 向广州仲裁委员会申请仲裁；"
        },
        {
          "clause_id": "C0019",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "使用说明",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "□ 向有管辖权的人民法院起诉。"
        },
        {
          "clause_id": "C0020",
          "location": "第七条 合同生效的条件和日期",
          "title": "合同生效的条件和日期",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条 合同生效的条件和日期"
          ],
          "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
        },
        {
          "clause_id": "C0021",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
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
      "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EQT-13-01

```json
{
  "rule_id": "EQT-13-01",
  "applicability": {
    "review_id": "EQT-13-01",
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
    "review_id": "EQT-13-01",
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
      "C0016",
      "C0017",
      "C0018",
      "C0020",
      "C0021"
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

## EQT-03-01

```json
{
  "rule_id": "EQT-03-01",
  "applicability": {
    "review_id": "EQT-03-01",
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
  "reason": "未找到明确约定：公司章程转让限制核对、向其他股东通知同等条件或不触发外部转让、优先购买权的依法行使或书面放弃。",
  "coverage_elements": [
    {
      "review_id": "EQT-03-01",
      "element_id": "equity_transfer_restrictions_1",
      "proposition": "公司章程转让限制核对",
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
      "review_id": "EQT-03-01",
      "element_id": "equity_transfer_restrictions_2",
      "proposition": "向其他股东通知同等条件或不触发外部转让",
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
      "review_id": "EQT-03-01",
      "element_id": "equity_transfer_restrictions_3",
      "proposition": "优先购买权的依法行使或书面放弃",
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
      "element_id": "equity_transfer_restrictions_1",
      "review_id": "EQT-03-01",
      "search_targets": [
        "公司章程转让限制核对"
      ],
      "query_patterns": [
        "(?:核对|核验|遵守).{0,30}章程.{0,25}转让限制"
      ],
      "query_semantic_target": "公司章程转让限制核对",
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
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式"
        },
        {
          "clause_id": "C0003",
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        },
        {
          "clause_id": "C0004",
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        },
        {
          "clause_id": "C0005",
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证"
        },
        {
          "clause_id": "C0006",
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        },
        {
          "clause_id": "C0007",
          "location": "第二条第2项",
          "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
          ],
          "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        },
        {
          "clause_id": "C0008",
          "location": "第二条第3项",
          "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
          ],
          "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        },
        {
          "clause_id": "C0009",
          "location": "第三条 盈亏分担",
          "title": "盈亏分担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条 盈亏分担"
          ],
          "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
        },
        {
          "clause_id": "C0010",
          "location": "第四条 费用负担",
          "title": "费用负担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条 费用负担"
          ],
          "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
        },
        {
          "clause_id": "C0011",
          "location": "第五条 合同的变更与解除",
          "title": "合同的变更与解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除"
          ],
          "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
        },
        {
          "clause_id": "C0012",
          "location": "第五条第1项",
          "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
          ],
          "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        },
        {
          "clause_id": "C0013",
          "location": "第五条第2项",
          "title": "2、一方当事人丧失实际履约能力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "2、一方当事人丧失实际履约能力。"
          ],
          "text": "2、一方当事人丧失实际履约能力。"
        },
        {
          "clause_id": "C0014",
          "location": "第五条第3项",
          "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
          ],
          "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        },
        {
          "clause_id": "C0015",
          "location": "第五条第4项",
          "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "4、因情况发生变化，经过双方协商同意变更或解除合同。"
          ],
          "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        },
        {
          "clause_id": "C0016",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "第六条 争议的解决"
        },
        {
          "clause_id": "C0017",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
        },
        {
          "clause_id": "C0018",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "☑ 向广州仲裁委员会申请仲裁；"
        },
        {
          "clause_id": "C0019",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "使用说明",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "□ 向有管辖权的人民法院起诉。"
        },
        {
          "clause_id": "C0020",
          "location": "第七条 合同生效的条件和日期",
          "title": "合同生效的条件和日期",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条 合同生效的条件和日期"
          ],
          "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
        },
        {
          "clause_id": "C0021",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
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
      "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "equity_transfer_restrictions_2",
      "review_id": "EQT-03-01",
      "search_targets": [
        "向其他股东通知同等条件或不触发外部转让"
      ],
      "query_patterns": [
        "其他股东.{0,50}(?:数量|比例).{0,30}价格.{0,30}(?:支付|期限)",
        "股东之间内部转让"
      ],
      "query_semantic_target": "向其他股东通知同等条件或不触发外部转让",
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
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式"
        },
        {
          "clause_id": "C0003",
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        },
        {
          "clause_id": "C0004",
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        },
        {
          "clause_id": "C0005",
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证"
        },
        {
          "clause_id": "C0006",
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        },
        {
          "clause_id": "C0007",
          "location": "第二条第2项",
          "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
          ],
          "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        },
        {
          "clause_id": "C0008",
          "location": "第二条第3项",
          "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
          ],
          "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        },
        {
          "clause_id": "C0009",
          "location": "第三条 盈亏分担",
          "title": "盈亏分担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条 盈亏分担"
          ],
          "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
        },
        {
          "clause_id": "C0010",
          "location": "第四条 费用负担",
          "title": "费用负担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条 费用负担"
          ],
          "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
        },
        {
          "clause_id": "C0011",
          "location": "第五条 合同的变更与解除",
          "title": "合同的变更与解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除"
          ],
          "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
        },
        {
          "clause_id": "C0012",
          "location": "第五条第1项",
          "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
          ],
          "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        },
        {
          "clause_id": "C0013",
          "location": "第五条第2项",
          "title": "2、一方当事人丧失实际履约能力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "2、一方当事人丧失实际履约能力。"
          ],
          "text": "2、一方当事人丧失实际履约能力。"
        },
        {
          "clause_id": "C0014",
          "location": "第五条第3项",
          "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
          ],
          "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        },
        {
          "clause_id": "C0015",
          "location": "第五条第4项",
          "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "4、因情况发生变化，经过双方协商同意变更或解除合同。"
          ],
          "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        },
        {
          "clause_id": "C0016",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "第六条 争议的解决"
        },
        {
          "clause_id": "C0017",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
        },
        {
          "clause_id": "C0018",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "☑ 向广州仲裁委员会申请仲裁；"
        },
        {
          "clause_id": "C0019",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "使用说明",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "□ 向有管辖权的人民法院起诉。"
        },
        {
          "clause_id": "C0020",
          "location": "第七条 合同生效的条件和日期",
          "title": "合同生效的条件和日期",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条 合同生效的条件和日期"
          ],
          "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
        },
        {
          "clause_id": "C0021",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
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
      "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "equity_transfer_restrictions_3",
      "review_id": "EQT-03-01",
      "search_targets": [
        "优先购买权的依法行使或书面放弃"
      ],
      "query_patterns": [
        "优先购买权.{0,40}(?:三十|30)日|其他股东.{0,20}书面放弃.{0,15}优先购买权|股东之间内部转让"
      ],
      "query_semantic_target": "优先购买权的依法行使或书面放弃",
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
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式"
        },
        {
          "clause_id": "C0003",
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        },
        {
          "clause_id": "C0004",
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        },
        {
          "clause_id": "C0005",
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证"
        },
        {
          "clause_id": "C0006",
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        },
        {
          "clause_id": "C0007",
          "location": "第二条第2项",
          "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
          ],
          "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        },
        {
          "clause_id": "C0008",
          "location": "第二条第3项",
          "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
          ],
          "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        },
        {
          "clause_id": "C0009",
          "location": "第三条 盈亏分担",
          "title": "盈亏分担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条 盈亏分担"
          ],
          "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
        },
        {
          "clause_id": "C0010",
          "location": "第四条 费用负担",
          "title": "费用负担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条 费用负担"
          ],
          "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
        },
        {
          "clause_id": "C0011",
          "location": "第五条 合同的变更与解除",
          "title": "合同的变更与解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除"
          ],
          "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
        },
        {
          "clause_id": "C0012",
          "location": "第五条第1项",
          "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
          ],
          "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        },
        {
          "clause_id": "C0013",
          "location": "第五条第2项",
          "title": "2、一方当事人丧失实际履约能力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "2、一方当事人丧失实际履约能力。"
          ],
          "text": "2、一方当事人丧失实际履约能力。"
        },
        {
          "clause_id": "C0014",
          "location": "第五条第3项",
          "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
          ],
          "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        },
        {
          "clause_id": "C0015",
          "location": "第五条第4项",
          "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "4、因情况发生变化，经过双方协商同意变更或解除合同。"
          ],
          "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        },
        {
          "clause_id": "C0016",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "第六条 争议的解决"
        },
        {
          "clause_id": "C0017",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
        },
        {
          "clause_id": "C0018",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "☑ 向广州仲裁委员会申请仲裁；"
        },
        {
          "clause_id": "C0019",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "使用说明",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "□ 向有管辖权的人民法院起诉。"
        },
        {
          "clause_id": "C0020",
          "location": "第七条 合同生效的条件和日期",
          "title": "合同生效的条件和日期",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条 合同生效的条件和日期"
          ],
          "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
        },
        {
          "clause_id": "C0021",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
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
      "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EQT-04-01

```json
{
  "rule_id": "EQT-04-01",
  "applicability": {
    "review_id": "EQT-04-01",
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
  "reason": "未找到明确约定：价款或投资总额、支付节点、条件或期限。",
  "coverage_elements": [
    {
      "review_id": "EQT-04-01",
      "element_id": "equity_price_payment_1",
      "proposition": "价款或投资总额",
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
      "review_id": "EQT-04-01",
      "element_id": "equity_price_payment_2",
      "proposition": "支付节点、条件或期限",
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
      "element_id": "equity_price_payment_1",
      "review_id": "EQT-04-01",
      "search_targets": [
        "价款或投资总额"
      ],
      "query_patterns": [
        "(?:转让价款|投资款|增资款|投资总额)[为：:]?(?:人民币)?\\d+(?:\\.\\d+)?万?元"
      ],
      "query_semantic_target": "价款或投资总额",
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
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式"
        },
        {
          "clause_id": "C0003",
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        },
        {
          "clause_id": "C0004",
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        },
        {
          "clause_id": "C0005",
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证"
        },
        {
          "clause_id": "C0006",
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        },
        {
          "clause_id": "C0007",
          "location": "第二条第2项",
          "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
          ],
          "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        },
        {
          "clause_id": "C0008",
          "location": "第二条第3项",
          "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
          ],
          "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        },
        {
          "clause_id": "C0009",
          "location": "第三条 盈亏分担",
          "title": "盈亏分担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条 盈亏分担"
          ],
          "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
        },
        {
          "clause_id": "C0010",
          "location": "第四条 费用负担",
          "title": "费用负担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条 费用负担"
          ],
          "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
        },
        {
          "clause_id": "C0011",
          "location": "第五条 合同的变更与解除",
          "title": "合同的变更与解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除"
          ],
          "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
        },
        {
          "clause_id": "C0012",
          "location": "第五条第1项",
          "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
          ],
          "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        },
        {
          "clause_id": "C0013",
          "location": "第五条第2项",
          "title": "2、一方当事人丧失实际履约能力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "2、一方当事人丧失实际履约能力。"
          ],
          "text": "2、一方当事人丧失实际履约能力。"
        },
        {
          "clause_id": "C0014",
          "location": "第五条第3项",
          "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
          ],
          "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        },
        {
          "clause_id": "C0015",
          "location": "第五条第4项",
          "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "4、因情况发生变化，经过双方协商同意变更或解除合同。"
          ],
          "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        },
        {
          "clause_id": "C0016",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "第六条 争议的解决"
        },
        {
          "clause_id": "C0017",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
        },
        {
          "clause_id": "C0018",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "☑ 向广州仲裁委员会申请仲裁；"
        },
        {
          "clause_id": "C0019",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "使用说明",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "□ 向有管辖权的人民法院起诉。"
        },
        {
          "clause_id": "C0020",
          "location": "第七条 合同生效的条件和日期",
          "title": "合同生效的条件和日期",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条 合同生效的条件和日期"
          ],
          "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
        },
        {
          "clause_id": "C0021",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
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
      "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "equity_price_payment_2",
      "review_id": "EQT-04-01",
      "search_targets": [
        "支付节点、条件或期限"
      ],
      "query_patterns": [
        "(?:交割|签署|生效).{0,20}\\d+日内.{0,25}支付|支付.{0,30}\\d{4}年\\d{1,2}月\\d{1,2}日"
      ],
      "query_semantic_target": "支付节点、条件或期限",
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
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式"
        },
        {
          "clause_id": "C0003",
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        },
        {
          "clause_id": "C0004",
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        },
        {
          "clause_id": "C0005",
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证"
        },
        {
          "clause_id": "C0006",
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        },
        {
          "clause_id": "C0007",
          "location": "第二条第2项",
          "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
          ],
          "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        },
        {
          "clause_id": "C0008",
          "location": "第二条第3项",
          "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
          ],
          "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        },
        {
          "clause_id": "C0009",
          "location": "第三条 盈亏分担",
          "title": "盈亏分担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条 盈亏分担"
          ],
          "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
        },
        {
          "clause_id": "C0010",
          "location": "第四条 费用负担",
          "title": "费用负担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条 费用负担"
          ],
          "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
        },
        {
          "clause_id": "C0011",
          "location": "第五条 合同的变更与解除",
          "title": "合同的变更与解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除"
          ],
          "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
        },
        {
          "clause_id": "C0012",
          "location": "第五条第1项",
          "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
          ],
          "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        },
        {
          "clause_id": "C0013",
          "location": "第五条第2项",
          "title": "2、一方当事人丧失实际履约能力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "2、一方当事人丧失实际履约能力。"
          ],
          "text": "2、一方当事人丧失实际履约能力。"
        },
        {
          "clause_id": "C0014",
          "location": "第五条第3项",
          "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
          ],
          "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        },
        {
          "clause_id": "C0015",
          "location": "第五条第4项",
          "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "4、因情况发生变化，经过双方协商同意变更或解除合同。"
          ],
          "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        },
        {
          "clause_id": "C0016",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "第六条 争议的解决"
        },
        {
          "clause_id": "C0017",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
        },
        {
          "clause_id": "C0018",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "☑ 向广州仲裁委员会申请仲裁；"
        },
        {
          "clause_id": "C0019",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "使用说明",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "□ 向有管辖权的人民法院起诉。"
        },
        {
          "clause_id": "C0020",
          "location": "第七条 合同生效的条件和日期",
          "title": "合同生效的条件和日期",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条 合同生效的条件和日期"
          ],
          "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
        },
        {
          "clause_id": "C0021",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
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
      "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EQT-05-01

```json
{
  "rule_id": "EQT-05-01",
  "applicability": {
    "review_id": "EQT-05-01",
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
  "reason": "未找到明确约定：交割条件及未满足的处理、股东名册及出资证明更新、办理变更登记的责任人与期限。",
  "coverage_elements": [
    {
      "review_id": "EQT-05-01",
      "element_id": "equity_closing_registration_1",
      "proposition": "交割条件及未满足的处理",
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
      "review_id": "EQT-05-01",
      "element_id": "equity_closing_registration_2",
      "proposition": "股东名册及出资证明更新",
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
      "review_id": "EQT-05-01",
      "element_id": "equity_closing_registration_3",
      "proposition": "办理变更登记的责任人与期限",
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
      "element_id": "equity_closing_registration_1",
      "review_id": "EQT-05-01",
      "search_targets": [
        "交割条件及未满足的处理"
      ],
      "query_patterns": [
        "交割条件.{0,40}(?:满足|完成|具备).{0,60}(?:未满足|未完成).{0,30}(?:解除|延期|退款)"
      ],
      "query_semantic_target": "交割条件及未满足的处理",
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
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式"
        },
        {
          "clause_id": "C0003",
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        },
        {
          "clause_id": "C0004",
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        },
        {
          "clause_id": "C0005",
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证"
        },
        {
          "clause_id": "C0006",
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        },
        {
          "clause_id": "C0007",
          "location": "第二条第2项",
          "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
          ],
          "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        },
        {
          "clause_id": "C0008",
          "location": "第二条第3项",
          "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
          ],
          "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        },
        {
          "clause_id": "C0009",
          "location": "第三条 盈亏分担",
          "title": "盈亏分担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条 盈亏分担"
          ],
          "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
        },
        {
          "clause_id": "C0010",
          "location": "第四条 费用负担",
          "title": "费用负担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条 费用负担"
          ],
          "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
        },
        {
          "clause_id": "C0011",
          "location": "第五条 合同的变更与解除",
          "title": "合同的变更与解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除"
          ],
          "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
        },
        {
          "clause_id": "C0012",
          "location": "第五条第1项",
          "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
          ],
          "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        },
        {
          "clause_id": "C0013",
          "location": "第五条第2项",
          "title": "2、一方当事人丧失实际履约能力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "2、一方当事人丧失实际履约能力。"
          ],
          "text": "2、一方当事人丧失实际履约能力。"
        },
        {
          "clause_id": "C0014",
          "location": "第五条第3项",
          "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
          ],
          "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        },
        {
          "clause_id": "C0015",
          "location": "第五条第4项",
          "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "4、因情况发生变化，经过双方协商同意变更或解除合同。"
          ],
          "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        },
        {
          "clause_id": "C0016",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "第六条 争议的解决"
        },
        {
          "clause_id": "C0017",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
        },
        {
          "clause_id": "C0018",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "☑ 向广州仲裁委员会申请仲裁；"
        },
        {
          "clause_id": "C0019",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "使用说明",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "□ 向有管辖权的人民法院起诉。"
        },
        {
          "clause_id": "C0020",
          "location": "第七条 合同生效的条件和日期",
          "title": "合同生效的条件和日期",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条 合同生效的条件和日期"
          ],
          "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
        },
        {
          "clause_id": "C0021",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
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
      "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "equity_closing_registration_2",
      "review_id": "EQT-05-01",
      "search_targets": [
        "股东名册及出资证明更新"
      ],
      "query_patterns": [
        "(?:更新|修改|记载).{0,15}股东名册.{0,50}(?:出资证明|公司章程)"
      ],
      "query_semantic_target": "股东名册及出资证明更新",
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
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式"
        },
        {
          "clause_id": "C0003",
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        },
        {
          "clause_id": "C0004",
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        },
        {
          "clause_id": "C0005",
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证"
        },
        {
          "clause_id": "C0006",
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        },
        {
          "clause_id": "C0007",
          "location": "第二条第2项",
          "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
          ],
          "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        },
        {
          "clause_id": "C0008",
          "location": "第二条第3项",
          "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
          ],
          "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        },
        {
          "clause_id": "C0009",
          "location": "第三条 盈亏分担",
          "title": "盈亏分担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条 盈亏分担"
          ],
          "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
        },
        {
          "clause_id": "C0010",
          "location": "第四条 费用负担",
          "title": "费用负担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条 费用负担"
          ],
          "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
        },
        {
          "clause_id": "C0011",
          "location": "第五条 合同的变更与解除",
          "title": "合同的变更与解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除"
          ],
          "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
        },
        {
          "clause_id": "C0012",
          "location": "第五条第1项",
          "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
          ],
          "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        },
        {
          "clause_id": "C0013",
          "location": "第五条第2项",
          "title": "2、一方当事人丧失实际履约能力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "2、一方当事人丧失实际履约能力。"
          ],
          "text": "2、一方当事人丧失实际履约能力。"
        },
        {
          "clause_id": "C0014",
          "location": "第五条第3项",
          "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
          ],
          "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        },
        {
          "clause_id": "C0015",
          "location": "第五条第4项",
          "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "4、因情况发生变化，经过双方协商同意变更或解除合同。"
          ],
          "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        },
        {
          "clause_id": "C0016",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "第六条 争议的解决"
        },
        {
          "clause_id": "C0017",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
        },
        {
          "clause_id": "C0018",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "☑ 向广州仲裁委员会申请仲裁；"
        },
        {
          "clause_id": "C0019",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "使用说明",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "□ 向有管辖权的人民法院起诉。"
        },
        {
          "clause_id": "C0020",
          "location": "第七条 合同生效的条件和日期",
          "title": "合同生效的条件和日期",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条 合同生效的条件和日期"
          ],
          "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
        },
        {
          "clause_id": "C0021",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
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
      "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "equity_closing_registration_3",
      "review_id": "EQT-05-01",
      "search_targets": [
        "办理变更登记的责任人与期限"
      ],
      "query_patterns": [
        "(?:目标公司|双方).{0,30}\\d+日内.{0,20}(?:工商变更|变更登记)"
      ],
      "query_semantic_target": "办理变更登记的责任人与期限",
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
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。\n甲乙双方本着平等互利的原则，经友好协商，达成如下协议："
        },
        {
          "clause_id": "C0002",
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式"
        },
        {
          "clause_id": "C0003",
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
        },
        {
          "clause_id": "C0004",
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
        },
        {
          "clause_id": "C0005",
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证"
        },
        {
          "clause_id": "C0006",
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
        },
        {
          "clause_id": "C0007",
          "location": "第二条第2项",
          "title": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
          ],
          "text": "2、甲方转让其股权后，其在广州启辰智能科技有限公司原享有的权利和应承担的义务，随股权转让而转由乙方享有与承担。"
        },
        {
          "clause_id": "C0008",
          "location": "第二条第3项",
          "title": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
          ],
          "text": "3、乙方承认广州启辰智能科技有限公司章程，保证按章程规定履行义务和责任。"
        },
        {
          "clause_id": "C0009",
          "location": "第三条 盈亏分担",
          "title": "盈亏分担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条 盈亏分担"
          ],
          "text": "第三条 盈亏分担\n从2026年10月1日起，乙方即成为广州启辰智能科技有限公司的股东。"
        },
        {
          "clause_id": "C0010",
          "location": "第四条 费用负担",
          "title": "费用负担",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条 费用负担"
          ],
          "text": "第四条 费用负担\n本次股权转让有关费用，由双方承担。"
        },
        {
          "clause_id": "C0011",
          "location": "第五条 合同的变更与解除",
          "title": "合同的变更与解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除"
          ],
          "text": "第五条 合同的变更与解除\n发生下列情况之一时，可变更或解除合同，但双方必须就此签订书面变更或解除合同。"
        },
        {
          "clause_id": "C0012",
          "location": "第五条第1项",
          "title": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
          ],
          "text": "1、由于不可抗力或由于一方当事人虽无过失但无法防止的外因，致使本合同无法履行。"
        },
        {
          "clause_id": "C0013",
          "location": "第五条第2项",
          "title": "2、一方当事人丧失实际履约能力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "2、一方当事人丧失实际履约能力。"
          ],
          "text": "2、一方当事人丧失实际履约能力。"
        },
        {
          "clause_id": "C0014",
          "location": "第五条第3项",
          "title": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
          ],
          "text": "3、由于一方或二方违约，严重影响了守约方的经济利益，使合同履行成为不必要。"
        },
        {
          "clause_id": "C0015",
          "location": "第五条第4项",
          "title": "4、因情况发生变化，经过双方协商同意变更或解除合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条 合同的变更与解除",
            "4、因情况发生变化，经过双方协商同意变更或解除合同。"
          ],
          "text": "4、因情况发生变化，经过双方协商同意变更或解除合同。"
        },
        {
          "clause_id": "C0016",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "第六条 争议的解决"
        },
        {
          "clause_id": "C0017",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "因本协议书引起的或与本协议书有关的任何争议，甲乙双方应友好协商解决，如协商不成，按照下列方式解决（任选一项，且只能选择一项，在选定的一项前的方框内打“√”）："
        },
        {
          "clause_id": "C0018",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "☑ 向广州仲裁委员会申请仲裁；"
        },
        {
          "clause_id": "C0019",
          "location": "第六条 争议的解决",
          "title": "争议的解决",
          "section_type": "使用说明",
          "heading_path": [
            "第六条 争议的解决"
          ],
          "text": "□ 向有管辖权的人民法院起诉。"
        },
        {
          "clause_id": "C0020",
          "location": "第七条 合同生效的条件和日期",
          "title": "合同生效的条件和日期",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条 合同生效的条件和日期"
          ],
          "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
        },
        {
          "clause_id": "C0021",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n本合同于2026年9月8日签订，合同正本一式四份，甲、乙双方各执一份，报工商行政管理机关一份，广州启辰智能科技有限公司存一份，均具有同等法律效力。\n甲方签署：张明远\n乙方签署：李浩然\n其他股东签署：\n王志鹏\n陈嘉怡\n2026年9月8日\n注：涉及签署的，自然人的由本人签字，股东为法人或其他组织的由其法定代表人或负责人（有权签字人）签字，并加盖公章。"
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
          "text": "广州启辰智能科技有限公司股权转让合同\n转让方：张明远（甲方）\n住所：广东省广州市天河区珠江新城华夏路88号1203室\n受让方：李浩然（乙方）\n住所：广东省广州市海珠区新港中路368号1506室\n本合同由甲方与乙方就广州启辰智能科技有限公司的股权转让事宜，于2026年9月8日在广州市订立。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "text": "甲乙双方本着平等互利的原则，经友好协商，达成如下协议：",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条 股权转让价格与付款方式",
          "title": "股权转让价格与付款方式",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式"
          ],
          "text": "第一条 股权转让价格与付款方式",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第1项",
          "title": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；"
          ],
          "text": "1、甲方将原认缴出资300万元（占公司注册资本的30%）转让给乙方，转让金360万元；",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第一条第2项",
          "title": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条 股权转让价格与付款方式",
            "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。"
          ],
          "text": "2、乙方同意在2026年9月30日前，向甲方支付上述股权转让款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条 保证",
          "title": "保证",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证"
          ],
          "text": "第二条 保证",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
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
          "location": "第二条第1项",
          "title": "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条 保证",
            "1、甲方保证所转让给乙方的股权是甲方在广州启辰智能科技有限公司合法拥有的股权，甲方拥有完全的处分权。甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。否则，由此引起的所有责任，由甲方承担。"
          ],
          "text": "甲方保证对所转让的股权，没有设置任何抵押、质押或担保，并免遭任何第三人的追索。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
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
      "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## S-00-01

```json
{
  "rule_id": "S-00-01",
  "applicability": {
    "review_id": "S-00-01",
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
  "reason": "正式合同条款或附件中已召回能够覆盖该审查点的实质约定，未发现明显空白项。",
  "coverage_elements": [
    {
      "review_id": "S-00-01",
      "element_id": "contract_effective_condition",
      "proposition": "本合同生效条件或日期",
      "status": "COVERED",
      "evidence_ids": [
        "C0020"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0020"
      ],
      "source_spans": [
        "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
      ],
      "source_locations": [
        "第七条 合同生效的条件和日期"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0020"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0020"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0020",
          "quote": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [],
  "evidence_clauses": [
    {
      "clause_id": "C0020",
      "location": "第七条 合同生效的条件和日期",
      "title": "合同生效的条件和日期",
      "text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。",
      "section_type": "正式合同条款",
      "block_type": "OPERATIVE_CLAUSE",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第七条 合同生效的条件和日期",
      "sentence_index": 1,
      "quote": "第七条 合同生效的条件和日期 本合同经各方签字后生效。",
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。",
      "source_span": {
        "start_offset": 842,
        "end_offset": 869,
        "raw_text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
      },
      "source_start": 842,
      "source_end": 869,
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0020",
        "section": "第七条 合同生效的条件和日期",
        "sentence_index": 1,
        "quote": "第七条 合同生效的条件和日期 本合同经各方签字后生效。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "第七条 合同生效的条件和日期\n本合同经各方签字后生效。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "evidence_claim_id": "S-00-01-EC-01",
      "entailment_status": "UNCERTAIN",
      "semantic_score": 0.25,
      "entity_match": false,
      "obligation_match": false,
      "consequence_match": false,
      "polarity_match": true,
      "supporting_element_ids": [
        "contract_effective_condition"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "S-00-01",
      "element_ids": [
        "contract_effective_condition"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supports_element_ids": [
        "contract_effective_condition"
      ],
      "supported_propositions": [
        "本合同生效条件或日期"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    }
  ],
  "termination_classification": []
}
```

## S-00-03

```json
{
  "rule_id": "S-00-03",
  "applicability": {
    "review_id": "S-00-03",
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
  "reason": "未在正式合同条款中找到能覆盖该审查点的有效约定。",
  "coverage_elements": [
    {
      "review_id": "S-00-03",
      "element_id": "core_contract_arrangement",
      "proposition": "合同存在可验证的“通知与送达”实质条款内容。",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NEGATIVE_SEARCH_NOT_FOUND",
      "verifier_confidence": "high",
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
      "element_id": "core_contract_arrangement",
      "review_id": "S-00-03",
      "search_targets": [
        "合同存在可验证的“通知与送达”实质条款内容"
      ],
      "query_patterns": [
        "合同存在可验证的“通知与送达”实质条款内容"
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
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021"
      ],
      "searched_document_hash": "cc13a74aaacf925f7a9bf01aeec2d8810275775bbd381e826d750484e2d90e0b",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
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
    "high_finding_count": 5,
    "core_priority_count": 5,
    "consistency": "CONSISTENT",
    "explanations": [],
    "needs_recalibration": false
  },
  "context_consistency": {
    "status": "PASS",
    "failures": [],
    "contract_type": "equity_transfer",
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