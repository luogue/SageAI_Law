# 专门法条召回与排序修复

COMMON-20-01根因：585原本就在静态候选中，但未接入显式命题选择；校验实际收到“合同原文覆盖全部专项要素。”这一结论占位句，585被判断UNCERTAIN。585本地摘要同时只记录调减救济，缺少首款的约定违约金/损失赔偿额计算方法。
D-04-02根因：只有902支付期限命题，缺少889支付义务命题；889未入本地法条库。旧选择器对所有命题统一评分100并按配置顺序选取，没有专门性等级。

修改文件及范围：
- backend/review_v2/legal_basis_selection.py：新增义务/违约金计算命题；ARTICLE_METADATA含article_id、legal_domain、contract_type、proposition_tags、normative_object、trigger_conditions、effect_type、specificity_level；rank_candidates按专门性和直接性排序。
- backend/review_v2/quality4.py：补入889官方法条，补全585首款计算方法及调整/迟延履行内容。
- backend/review_v2/penalty_base.py：仅绑定legal_basis_topics，未改计算基数解析。
- backend/review_v2/safekeeping_contract_checklist.py：仅增加支付保管费义务命题。
- backend/tests/test_legal_specificity.py：新增12项测试；test_legal_basis_production_path.py更新法条预期及单元输入coverage上下文。

评分：直接专门条款1.0；直接一般条款0.8；相关一般条款0.6；已触发补充条款0.3；未触发背景0.1且不入最终依据；无命题匹配0。不是词频匹配。
补充规则仅读取既有coverage结果，不做新事实抽取：已覆盖时不触发约定不明补充。当前两项均为已覆盖，因此510保留候选背景，排除最终依据。
门禁：存在适用SPECIAL时首项必须是SPECIAL；所需适用条文验证失败或排序违反约束，会通过现有selection_complete门禁阻断报告。未改renderer、SEARCH_AUDIT、coverage、evidence或chunking。

|规则|最终主要依据|辅助依据|
|---|---|---|
|COMMON-20-01|第585条|第577条|
|D-04-02|第889条、第902条|第509条|
|D-04-03|第509条|第510条|
|D-09-02|第450条、第453条、第903条||
|D-09-04|第450条、第448条、第903条||

D-04-03、D-09-02、D-09-04法律依据文本与修复前逐字相同；同模式集成重跑全部50项的coverage、要素、证据、covered/missing字段与修复前一致。实际开启模型复核重跑全部覆盖状态亦未变化。
50项：39 PASS、2 PARTIAL、3 MISSING、6 N/A。新增12项，整体135项通过（7个依赖/弃用警告）；最后排序定向复验12项通过。
实际完整报告质量门：REPORT_READY。
官方法条：https://www.spp.gov.cn/spp/fl/202006/t20200602_463888.shtml

## COMMON-20-01

[
  {
    "article": "第585条",
    "matched_propositions": [
      "liquidated_damages_calculation"
    ],
    "metadata": {
      "article_id": "第585条",
      "legal_domain": "breach",
      "contract_type": "general",
      "proposition_tags": [
        "liquidated_damages_calculation",
        "liquidated_damages",
        "agreed_damages",
        "damages_calculation_method",
        "damages_adjustment"
      ],
      "normative_object": "当事人可以约定违约金及因违约产生的损失赔偿额计算方法",
      "trigger_conditions": [],
      "effect_type": "agreed_damages",
      "specificity_level": "SPECIAL"
    },
    "trigger_satisfied": true,
    "eligible": true,
    "relevance_score": 1.0,
    "score_semantics": "1.0=direct special; 0.6=related general; 0.3=triggered supplementary; 0.1=inactive background; 0=unmatched",
    "reason": "明确法律命题对应；按直接性及专门性排序，并非词频相似度",
    "authority_validation": {
      "status": "CURRENT",
      "entailment": "SUPPORTS",
      "support_type": "DIRECT_SUPPORT",
      "authority": {
        "authority_id": "CN-CIVIL-CODE-585",
        "jurisdiction": "CN",
        "law_name": "中华人民共和国民法典",
        "article": "第585条",
        "paragraph": "",
        "text": "当事人可以约定一方违约时应当根据违约情况向对方支付一定数额的违约金，也可以约定因违约产生的损失赔偿额的计算方法。约定的违约金低于造成的损失的，人民法院或者仲裁机构可以根据当事人的请求予以增加；约定的违约金过分高于造成的损失的，人民法院或者仲裁机构可以根据当事人的请求予以适当减少。当事人就迟延履行约定违约金的，违约方支付违约金后，还应当履行债务。",
        "authority_level": "法律",
        "effective_from": "2021-01-01",
        "effective_to": null,
        "status": "CURRENT",
        "replacement": null,
        "source": "legal_authority_kb_minimal",
        "last_verified_at": "2026-08-11"
      }
    }
  },
  {
    "article": "第577条",
    "matched_propositions": [
      "general_breach_liability"
    ],
    "metadata": {
      "article_id": "第577条",
      "legal_domain": "contract",
      "contract_type": "general",
      "proposition_tags": [
        "general_breach_liability"
      ],
      "normative_object": "不履行或履行不符合约定时的一般违约责任",
      "trigger_conditions": [],
      "effect_type": "statutory_rule",
      "specificity_level": "GENERAL"
    },
    "trigger_satisfied": true,
    "eligible": true,
    "relevance_score": 0.6,
    "score_semantics": "1.0=direct special; 0.6=related general; 0.3=triggered supplementary; 0.1=inactive background; 0=unmatched",
    "reason": "明确法律命题对应；按直接性及专门性排序，并非词频相似度",
    "authority_validation": {
      "status": "CURRENT",
      "entailment": "SUPPORTS",
      "support_type": "DIRECT_SUPPORT",
      "authority": {
        "authority_id": "CN-CC-577",
        "jurisdiction": "CN",
        "law_name": "中华人民共和国民法典",
        "article": "第577条",
        "paragraph": "",
        "text": "当事人一方不履行合同义务或者履行不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。",
        "authority_level": "法律",
        "effective_from": "2021-01-01",
        "effective_to": null,
        "status": "CURRENT",
        "replacement": null,
        "source": "National Laws and Regulations Database / Civil Code",
        "last_verified_at": "2026-08-14"
      }
    }
  },
  {
    "article": "第510条",
    "matched_propositions": [
      "unclear_contract_terms"
    ],
    "metadata": {
      "article_id": "第510条",
      "legal_domain": "contract",
      "contract_type": "general",
      "proposition_tags": [
        "unclear_contract_terms"
      ],
      "normative_object": "报酬、费用承担及履行方式约定不明时通过补充协议、相关条款或交易习惯确定",
      "trigger_conditions": [
        "unclear_terms"
      ],
      "effect_type": "statutory_rule",
      "specificity_level": "SUPPLEMENTARY"
    },
    "trigger_satisfied": false,
    "eligible": false,
    "relevance_score": 0.1,
    "score_semantics": "1.0=direct special; 0.6=related general; 0.3=triggered supplementary; 0.1=inactive background; 0=unmatched",
    "reason": "补充规则前提未触发，仅保留候选背景，不进入最终依据",
    "authority_validation": {
      "status": "CURRENT",
      "entailment": "SUPPORTS",
      "support_type": "DIRECT_SUPPORT",
      "authority": {
        "authority_id": "CN-CIVIL-CODE-510",
        "jurisdiction": "CN",
        "law_name": "中华人民共和国民法典",
        "article": "第510条",
        "paragraph": "",
        "text": "合同生效后，当事人就质量、价款或者报酬、履行地点等内容没有约定或者约定不明确的，可以协议补充；不能达成补充协议的，按照合同相关条款或者交易习惯确定。",
        "authority_level": "法律",
        "effective_from": "2021-01-01",
        "effective_to": null,
        "status": "CURRENT",
        "replacement": null,
        "source": "https://www.court.gov.cn/zixun/xiangqing/233181.html",
        "last_verified_at": "2026-09-09"
      }
    }
  }
]

## D-04-02

[
  {
    "article": "第889条",
    "matched_propositions": [
      "custody_fee_obligation"
    ],
    "metadata": {
      "article_id": "第889条",
      "legal_domain": "custody",
      "contract_type": "custody",
      "proposition_tags": [
        "custody_fee_obligation"
      ],
      "normative_object": "寄存人应当按照约定向保管人支付保管费",
      "trigger_conditions": [],
      "effect_type": "statutory_rule",
      "specificity_level": "SPECIAL"
    },
    "trigger_satisfied": true,
    "eligible": true,
    "relevance_score": 1.0,
    "score_semantics": "1.0=direct special; 0.6=related general; 0.3=triggered supplementary; 0.1=inactive background; 0=unmatched",
    "reason": "明确法律命题对应；按直接性及专门性排序，并非词频相似度",
    "authority_validation": {
      "status": "CURRENT",
      "entailment": "SUPPORTS",
      "support_type": "DIRECT_SUPPORT",
      "authority": {
        "authority_id": "CN-CIVIL-CODE-889",
        "jurisdiction": "CN",
        "law_name": "中华人民共和国民法典",
        "article": "第889条",
        "paragraph": "",
        "text": "寄存人应当按照约定向保管人支付保管费。当事人对保管费没有约定或者约定不明确，依据本法第五百一十条的规定仍不能确定的，视为无偿保管。",
        "authority_level": "法律",
        "effective_from": "2021-01-01",
        "effective_to": null,
        "status": "CURRENT",
        "replacement": null,
        "source": "https://www.court.gov.cn/zixun/xiangqing/233181.html",
        "last_verified_at": "2026-09-09"
      }
    }
  },
  {
    "article": "第902条",
    "matched_propositions": [
      "remuneration_payment"
    ],
    "metadata": {
      "article_id": "第902条",
      "legal_domain": "custody",
      "contract_type": "custody",
      "proposition_tags": [
        "remuneration_payment"
      ],
      "normative_object": "有偿保管费用按约定期限支付；支付期限不明时的处理",
      "trigger_conditions": [],
      "effect_type": "statutory_rule",
      "specificity_level": "SPECIAL"
    },
    "trigger_satisfied": true,
    "eligible": true,
    "relevance_score": 1.0,
    "score_semantics": "1.0=direct special; 0.6=related general; 0.3=triggered supplementary; 0.1=inactive background; 0=unmatched",
    "reason": "明确法律命题对应；按直接性及专门性排序，并非词频相似度",
    "authority_validation": {
      "status": "CURRENT",
      "entailment": "SUPPORTS",
      "support_type": "DIRECT_SUPPORT",
      "authority": {
        "authority_id": "CN-CIVIL-CODE-902",
        "jurisdiction": "CN",
        "law_name": "中华人民共和国民法典",
        "article": "第902条",
        "paragraph": "",
        "text": "有偿的保管合同，寄存人应当按照约定的期限向保管人支付保管费。当事人对支付期限没有约定或者约定不明确，依据本法第五百一十条的规定仍不能确定的，应当在领取保管物的同时支付。",
        "authority_level": "法律",
        "effective_from": "2021-01-01",
        "effective_to": null,
        "status": "CURRENT",
        "replacement": null,
        "source": "https://www.court.gov.cn/zixun/xiangqing/233181.html",
        "last_verified_at": "2026-09-09"
      }
    }
  },
  {
    "article": "第509条",
    "matched_propositions": [
      "performance_cooperation"
    ],
    "metadata": {
      "article_id": "第509条",
      "legal_domain": "contract",
      "contract_type": "general",
      "proposition_tags": [
        "performance_cooperation"
      ],
      "normative_object": "依约全面履行并按诚信原则履行通知、协助等义务；具体费用及凭证安排属于合同细化",
      "trigger_conditions": [],
      "effect_type": "statutory_rule",
      "specificity_level": "GENERAL"
    },
    "trigger_satisfied": true,
    "eligible": true,
    "relevance_score": 0.6,
    "score_semantics": "1.0=direct special; 0.6=related general; 0.3=triggered supplementary; 0.1=inactive background; 0=unmatched",
    "reason": "明确法律命题对应；按直接性及专门性排序，并非词频相似度",
    "authority_validation": {
      "status": "CURRENT",
      "entailment": "SUPPORTS",
      "support_type": "DIRECT_SUPPORT",
      "authority": {
        "authority_id": "CN-CC-509",
        "jurisdiction": "CN",
        "law_name": "中华人民共和国民法典",
        "article": "第509条",
        "paragraph": "",
        "text": "当事人应当按照约定全面履行自己的义务，并遵循诚信原则履行通知、协助、保密等义务。",
        "authority_level": "法律",
        "effective_from": "2021-01-01",
        "effective_to": null,
        "status": "CURRENT",
        "replacement": null,
        "source": "National Laws and Regulations Database / Civil Code",
        "last_verified_at": "2026-08-14"
      }
    }
  },
  {
    "article": "第510条",
    "matched_propositions": [
      "unclear_contract_terms"
    ],
    "metadata": {
      "article_id": "第510条",
      "legal_domain": "contract",
      "contract_type": "general",
      "proposition_tags": [
        "unclear_contract_terms"
      ],
      "normative_object": "报酬、费用承担及履行方式约定不明时通过补充协议、相关条款或交易习惯确定",
      "trigger_conditions": [
        "unclear_terms"
      ],
      "effect_type": "statutory_rule",
      "specificity_level": "SUPPLEMENTARY"
    },
    "trigger_satisfied": false,
    "eligible": false,
    "relevance_score": 0.1,
    "score_semantics": "1.0=direct special; 0.6=related general; 0.3=triggered supplementary; 0.1=inactive background; 0=unmatched",
    "reason": "补充规则前提未触发，仅保留候选背景，不进入最终依据",
    "authority_validation": {
      "status": "CURRENT",
      "entailment": "SUPPORTS",
      "support_type": "DIRECT_SUPPORT",
      "authority": {
        "authority_id": "CN-CIVIL-CODE-510",
        "jurisdiction": "CN",
        "law_name": "中华人民共和国民法典",
        "article": "第510条",
        "paragraph": "",
        "text": "合同生效后，当事人就质量、价款或者报酬、履行地点等内容没有约定或者约定不明确的，可以协议补充；不能达成补充协议的，按照合同相关条款或者交易习惯确定。",
        "authority_level": "法律",
        "effective_from": "2021-01-01",
        "effective_to": null,
        "status": "CURRENT",
        "replacement": null,
        "source": "https://www.court.gov.cn/zixun/xiangqing/233181.html",
        "last_verified_at": "2026-09-09"
      }
    }
  },
  {
    "article": "第903条",
    "matched_propositions": [],
    "metadata": {
      "article_id": "第903条",
      "legal_domain": "custody",
      "contract_type": "custody",
      "proposition_tags": [
        "custody_lien_source"
      ],
      "normative_object": "欠付保管费或其他费用时的保管人留置权来源，不直接规定费用项目、金额或凭证",
      "trigger_conditions": [],
      "effect_type": "statutory_rule",
      "specificity_level": "SPECIAL"
    },
    "trigger_satisfied": true,
    "eligible": false,
    "relevance_score": 0,
    "score_semantics": "1.0=direct special; 0.6=related general; 0.3=triggered supplementary; 0.1=inactive background; 0=unmatched",
    "reason": "旧配置候选，但没有目标法律命题对应，不选择",
    "authority_validation": {
      "status": "CURRENT",
      "entailment": "SUPPORTS",
      "support_type": "DIRECT_SUPPORT",
      "authority": {
        "authority_id": "CN-CIVIL-CODE-903",
        "jurisdiction": "CN",
        "law_name": "中华人民共和国民法典",
        "article": "第903条",
        "paragraph": "",
        "text": "寄存人未按照约定支付保管费或者其他费用的，保管人对保管物享有留置权，但是当事人另有约定的除外。",
        "authority_level": "法律",
        "effective_from": "2021-01-01",
        "effective_to": null,
        "status": "CURRENT",
        "replacement": null,
        "source": "https://www.court.gov.cn/zixun/xiangqing/233181.html",
        "last_verified_at": "2026-09-09"
      }
    }
  }
]
