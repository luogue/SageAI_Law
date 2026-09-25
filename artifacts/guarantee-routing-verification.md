# 保证合同主类型与附属保密条款回归

根因：旧 resolver 缺少保证合同结构候选，confidentiality 参数在文档被判 UNCERTAIN 后被接受。NDA remedies 配置覆盖了原先的保密关联约束，接受了普通赔偿词。

本轮修改：primary_purpose.py 提供交易结构评分与附属特征；domain_selection.py 接入主类型及规则包冲突门禁；nda_semantics.py 要求保密行为与救济关联；engine.py 清理不兼容的旧场景参数；routers/review_v2.py 登记分类模块版本。

生产验证特意提交 contract_type=confidentiality、场景=保密协议，文件为原始 69 保证合同.docx，未修改。

{
  "primary_contract_type": "GUARANTEE",
  "contract_type_confidence": "high",
  "secondary_clause_features": [
    "CONFIDENTIALITY",
    "NOTICE",
    "DISPUTE_RESOLUTION"
  ],
  "classification_conflict": {
    "detected": true,
    "selected": "CONFIDENTIALITY",
    "document": "GUARANTEE",
    "resolved": true
  },
  "guarantee_features_detected": [
    "parties",
    "creditor_debtor",
    "secured_debt",
    "undertaking",
    "period",
    "scope",
    "recourse"
  ],
  "nda_primary_features_detected": [
    "information"
  ],
  "task_id": "CR-20260908-163233-6AF512",
  "worker_pid": 5440,
  "classification_evidence": [
    {
      "signal_type": "service_title_hint",
      "signal": "咨询服务",
      "target_family": "SERVICE",
      "weight": 1,
      "source_clause_ids": [
        "C0020"
      ]
    },
    {
      "signal_type": "parties",
      "signal": "保证人",
      "target_family": "GUARANTEE",
      "weight": 4,
      "source_clause_ids": [
        "C0007",
        "C0008",
        "C0019",
        "C0022",
        "C0026",
        "C0030",
        "C0031",
        "C0033"
      ]
    },
    {
      "signal_type": "creditor_debtor",
      "signal": "债权人",
      "target_family": "GUARANTEE",
      "weight": 4,
      "source_clause_ids": [
        "C0006",
        "C0024",
        "C0025",
        "C0033",
        "C0037",
        "C0038",
        "C0039",
        "C0040"
      ]
    },
    {
      "signal_type": "secured_debt",
      "signal": "主合同",
      "target_family": "GUARANTEE",
      "weight": 4,
      "source_clause_ids": [
        "C0023",
        "C0027",
        "C0029",
        "C0030",
        "C0031",
        "C0034",
        "C0035",
        "C0037"
      ]
    },
    {
      "signal_type": "undertaking",
      "signal": "连带责任保证",
      "target_family": "GUARANTEE",
      "weight": 4,
      "source_clause_ids": [
        "C0033",
        "C0083",
        "C0085",
        "C0087"
      ]
    },
    {
      "signal_type": "period",
      "signal": "保证期间",
      "target_family": "GUARANTEE",
      "weight": 4,
      "source_clause_ids": [
        "C0005",
        "C0036",
        "C0037",
        "C0038",
        "C0066",
        "C0084",
        "C0086"
      ]
    },
    {
      "signal_type": "scope",
      "signal": "担保的范围",
      "target_family": "GUARANTEE",
      "weight": 4,
      "source_clause_ids": [
        "C0003",
        "C0028",
        "C0035",
        "C0082"
      ]
    },
    {
      "signal_type": "recourse",
      "signal": "追偿",
      "target_family": "GUARANTEE",
      "weight": 4,
      "source_clause_ids": [
        "C0061"
      ]
    },
    {
      "signal_type": "obligation",
      "signal": "提供",
      "target_family": "TECHNOLOGY",
      "weight": 4,
      "source_clause_ids": [
        "C0022",
        "C0030",
        "C0040",
        "C0041",
        "C0044",
        "C0053",
        "C0054",
        "C0058"
      ]
    },
    {
      "signal_type": "information",
      "signal": "保密信息",
      "target_family": "CONFIDENTIALITY",
      "weight": 4,
      "source_clause_ids": [
        "C0095",
        "C0096"
      ]
    }
  ],
  "contract_hash": "dec08149bef6064a8217056ac4ce81ea3b240fa4e065d8478f95fb2a0bd5da6c",
  "selected_rule_packs": [
    "GUA"
  ],
  "nda_04_01": {
    "status": "NOT_APPLICABLE",
    "reason": "主类型为保证合同，未加载独立NDA规则包",
    "accepted_evidence": []
  },
  "final_contract_type": "guarantee",
  "contract_type_name": "保证合同",
  "statistics": {
    "风险条款": 1,
    "不适用": 20,
    "通过": 20,
    "法律提示": 5,
    "缺失": 1,
    "待核验": 2
  },
  "release_quality_gate": "REPORT_READY"
}

测试：test_primary_purpose_routing.py 新增20例（A-H、无标题保证、买卖附属保证、否定救济、错误规则包阻断及原DOCX）。

扩展已知失败：test_domain_selection_consistency.py 的买卖/租赁正式报告质量门2例；test_priority_contract_review.py 中竞业、NDA及动产质押8例。移除本轮分类和NDA匹配增量后，相应失败状态/原因保持一致，详见两个 isolation JSON；未改测试数据或放宽质量门。
