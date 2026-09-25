# 承揽合同适用性定向复测

任务：CR-20260909-091634-5A78E7
质量门禁：REPORT_READY
覆盖统计：{'通过': 30, '不适用': 4, '缺失': 10, '部分覆盖': 3}
处理优先级：{'NONE': 30, 'NOT_APPLICABLE': 4, 'C_OPTIMIZATION': 11, 'B_PRACTICAL': 2}

## COMMON-23-01：不适用
未发现最低业绩或业务金额补差机制；普通清偿不足的债务余额不适用业务额补差规则。
- trigger_evidence=[]（未激活的专项不生成正向证据）

## W-03-03：不适用
未发现承揽人辅助工作交第三人完成；定作人完成辅助工作属于协助义务，不触发辅助分包责任。
- transfer: 1
  SOURCE-C0012-8cd3bc1fbfd3 / 第十一条 其他约定：未经定作方书面同意，承揽方不得将本合同主要加工工作转交第三方完成。
- auxiliary: 0
- customer_assistance: 1
  SOURCE-C0027-2f76164c4b92 / 三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。：三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。
- lien_excluded: 0
- lien_reserved: 0
- trigger_evidence=[]（未激活的专项不生成正向证据）

## W-03-04：通过
已识别承揽工作转交第三人，进一步检查是否允许未经同意全部或肢解转包。
- transfer: 1
  SOURCE-C0012-8cd3bc1fbfd3 / 第十一条 其他约定：未经定作方书面同意，承揽方不得将本合同主要加工工作转交第三方完成。
- auxiliary: 0
- customer_assistance: 1
  SOURCE-C0027-2f76164c4b92 / 三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。：三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。
- lien_excluded: 0
- lien_reserved: 0

## W-10-01：缺失
未选择排除留置方案；仅审查留置条件及范围，不建议同时补充排除留置。
- transfer: 1
  SOURCE-C0012-8cd3bc1fbfd3 / 第十一条 其他约定：未经定作方书面同意，承揽方不得将本合同主要加工工作转交第三方完成。
- auxiliary: 0
- customer_assistance: 1
  SOURCE-C0027-2f76164c4b92 / 三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。：三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。
- lien_excluded: 0
- lien_reserved: 0
- trigger_evidence=[]（未激活的专项不生成正向证据）

## W-10-02：缺失
未选择排除留置方案；仅审查留置条件及范围，不建议同时补充排除留置。
- transfer: 1
  SOURCE-C0012-8cd3bc1fbfd3 / 第十一条 其他约定：未经定作方书面同意，承揽方不得将本合同主要加工工作转交第三方完成。
- auxiliary: 0
- customer_assistance: 1
  SOURCE-C0027-2f76164c4b92 / 三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。：三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。
- lien_excluded: 0
- lien_reserved: 0
- trigger_evidence=[]（未激活的专项不生成正向证据）

## W-10-03：不适用
未选择排除留置方案；仅审查留置条件及范围，不建议同时补充排除留置。
- transfer: 1
  SOURCE-C0012-8cd3bc1fbfd3 / 第十一条 其他约定：未经定作方书面同意，承揽方不得将本合同主要加工工作转交第三方完成。
- auxiliary: 0
- customer_assistance: 1
  SOURCE-C0027-2f76164c4b92 / 三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。：三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。
- lien_excluded: 0
- lien_reserved: 0
- trigger_evidence=[]（未激活的专项不生成正向证据）

## W-04-03：部分覆盖
未声明条件审查规则，默认适用于当前合同。
- trigger_evidence=[]（未激活的专项不生成正向证据）
- 最终证据：{"evidence_id": "SOURCE-C0027-2f76164c4b92", "clause_id": "C0027", "location": "三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。", "text": "三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。", "quote": "三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。", "original_excerpt": "三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。", "raw_text": "三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。\n因此导致停工超过15日的，承揽方有权解除合同，并要求定作方赔偿实际损失。", "source_type": "SOURCE_CLAUSE", "entailment_status": "UNCERTAIN", "source_domain": "GOODS_SALE", "supported_elements": ["work_assistance_extension"], "element_ids": ["work_assistance_extension"], "normalization_reason": "原文同时满足对应法律要素的行为、对象及责任条件；非规则标题匹配。", "matched_requirements": [{"element_id": "work_assistance_extension", "proposition": "协助不足时顺延交付", "terms": [], "sale_patterns": ["(?:未[^。；]{0,30}提供[^。；]{0,25}(?:原材料|技术资料|图纸)|未[^。；]{0,25}(?:协助|辅助工作)|不履行[^。；]{0,12}协助)", "顺延|延长", "期限|工期"], "atomic": true}], "evidence_claim_id": "W-04-03-EC-01", "semantic_score": 0.25, "entity_match": false, "obligation_match": false, "consequence_match": false, "polarity_match": true, "supporting_element_ids": ["work_assistance_extension"], "canonical_fact_keys": [], "relevance_score": 1.0, "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.", "review_id": "W-04-03", "support_type": "DIRECT", "document_id": "contract_package/main", "document_type": "OTHER", "source_document_type": "OTHER", "evidence_block_type": "OPERATIVE_CLAUSE", "document_name": "合同附件/补充文件", "section": "三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。", "sentence_index": 1, "confidence": "high", "evidence_type": "CONTRACT_TEXT", "source_span": {"start_offset": 3566, "end_offset": 3625, "raw_text": "三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。"}, "source_start": 3566, "source_end": 3625, "source_document": "contract_package/main", "original_document_reference": "contract_package/main", "derived_or_original": "ORIGINAL", "evidence_source": {"document_id": "contract_package/other", "document_type": "OTHER", "document_name": "合同附件/补充文件", "clause_id": "C0027", "section": "三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。", "sentence_index": 1, "quote": "三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。", "confidence": "high", "evidence_block_type": "OPERATIVE_CLAUSE", "evidence_type": "DERIVED_FINDING", "source_span": {"start_offset": -1, "end_offset": -1, "raw_text": "三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。\n因此导致停工超过15日的，承揽方有权解除合同，并要求定作方赔偿实际损失。"}, "derived_or_original": "DERIVED"}, "evidence_polarity": "SUPPORTS_PARTIAL", "provenance_validation": {"status": "PASS", "evidence_type": "CONTRACT_TEXT", "errors": []}, "supports_element_ids": ["work_assistance_extension"], "supported_propositions": ["协助不足时顺延交付"], "support_summary": "证明合同已约定相关合同要素。"}

## W-04-04：部分覆盖
未声明条件审查规则，默认适用于当前合同。
- trigger_evidence=[]（未激活的专项不生成正向证据）
- 最终证据：{"evidence_id": "SOURCE-C0027-0e70e0ef3324", "clause_id": "C0027", "location": "三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。", "text": "因此导致停工超过15日的，承揽方有权解除合同，并要求定作方赔偿实际损失。", "quote": "因此导致停工超过15日的，承揽方有权解除合同，并要求定作方赔偿实际损失。", "original_excerpt": "因此导致停工超过15日的，承揽方有权解除合同，并要求定作方赔偿实际损失。", "raw_text": "三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。\n因此导致停工超过15日的，承揽方有权解除合同，并要求定作方赔偿实际损失。", "source_type": "SOURCE_CLAUSE", "entailment_status": "UNCERTAIN", "source_domain": "GOODS_SALE", "supported_elements": ["work_assistance_exit"], "element_ids": ["work_assistance_exit"], "normalization_reason": "原文同时满足对应法律要素的行为、对象及责任条件；非规则标题匹配。", "matched_requirements": [{"element_id": "work_assistance_exit", "proposition": "未协助造成停工的解除权", "terms": [], "sale_patterns": ["停工|未履行协助", "承揽[人方][^。；]{0,12}有权解除"], "atomic": true}], "evidence_claim_id": "W-04-04-EC-01", "semantic_score": 0.25, "entity_match": false, "obligation_match": false, "consequence_match": true, "polarity_match": true, "supporting_element_ids": ["work_assistance_exit"], "canonical_fact_keys": [], "relevance_score": 1.0, "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.", "review_id": "W-04-04", "support_type": "DIRECT", "document_id": "contract_package/main", "document_type": "OTHER", "source_document_type": "OTHER", "evidence_block_type": "OPERATIVE_CLAUSE", "document_name": "合同附件/补充文件", "section": "三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。", "sentence_index": 1, "confidence": "high", "evidence_type": "CONTRACT_TEXT", "source_span": {"start_offset": 3626, "end_offset": 3662, "raw_text": "因此导致停工超过15日的，承揽方有权解除合同，并要求定作方赔偿实际损失。"}, "source_start": 3626, "source_end": 3662, "source_document": "contract_package/main", "original_document_reference": "contract_package/main", "derived_or_original": "ORIGINAL", "evidence_source": {"document_id": "contract_package/other", "document_type": "OTHER", "document_name": "合同附件/补充文件", "clause_id": "C0027", "section": "三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。", "sentence_index": 1, "quote": "因此导致停工超过15日的，承揽方有权解除合同，并要求定作方赔偿实际损失。", "confidence": "high", "evidence_block_type": "OPERATIVE_CLAUSE", "evidence_type": "DERIVED_FINDING", "source_span": {"start_offset": -1, "end_offset": -1, "raw_text": "三、定作方未按照合同规定时间和要求向承揽方提供原材料、技术资料或者完成必要辅助工作的，承揽方有权要求相应顺延交付期限。\n因此导致停工超过15日的，承揽方有权解除合同，并要求定作方赔偿实际损失。"}, "derived_or_original": "DERIVED"}, "evidence_polarity": "SUPPORTS_PARTIAL", "provenance_validation": {"status": "PASS", "evidence_type": "CONTRACT_TEXT", "errors": []}, "supports_element_ids": ["work_assistance_exit"], "supported_propositions": ["未协助造成停工的解除权"], "support_summary": "证明合同已约定相关合同要素。"}