"""Regression tests for utility-supply semantic evidence and contradictions."""

from review_v2.engine import review_contract_v2


def _item(output, item_id):
    return next(row for row in output["items"] if row["item_id"] == item_id)


def test_utility_supply_direct_suspension_is_adverse_not_pass():
    text = (
        "供用电合同。第5.6条 用户欠费5日后，供电方无需催告、无需给予合理期限、"
        "无需另行通知即可中止供电。"
    )
    output = review_contract_v2(text, "utility_supply", use_llm=False)

    for item_id in ("US-07-03", "US-07-04"):
        item = _item(output, item_id)
        assert item["coverage_status"] == "风险条款"
        assert "无需催告" in item["reasoning_summary"]
        assert item["evidence_clauses"]


def test_utility_supply_interruption_disclaimer_overrides_keyword_pass():
    text = (
        "供用电合同。第7.1条 计划检修仅提前24小时通知用户。"
        "第7.2条 临时检修可以先停电后通知。第7.4条 未提前通知停电造成损失的，供电方免责。"
    )
    output = review_contract_v2(text, "utility_supply", use_llm=False)

    assert _item(output, "US-05-01")["coverage_status"] == "风险条款"
    assert _item(output, "US-05-02")["coverage_status"] == "风险条款"


def test_utility_supply_repair_no_completion_commitment_not_pass():
    text = "供用电合同。第8.4条 供电方接到报修后及时抢修，但不承诺具体抢修完成时间，抢修时间过长用户也不得要求赔偿。"
    output = review_contract_v2(text, "utility_supply", use_llm=False)

    item = _item(output, "US-06-02")
    assert item["coverage_status"] == "风险条款"
    assert "未承诺具体抢修完成时间" in item["reasoning_summary"]


def test_utility_supply_partial_existing_illegal_use_and_billing_not_missing():
    text = (
        "供用电合同。第4条 按电表计量结果和政府公示电价计费，每月出具账单，用户应在5日内支付。"
        "第9条 用户不得擅自改动用电设施，不得危害电网安全。"
    )
    output = review_contract_v2(text, "utility_supply", use_llm=False)

    illegal_use = _item(output, "US-08-02")
    billing = _item(output, "US-10-02")
    assert illegal_use["coverage_status"] == "部分覆盖"
    assert "禁止擅自改动供用设施" not in illegal_use["reasoning_summary"]
    assert billing["coverage_status"] in {"部分覆盖", "通过"}
    assert billing["coverage_status"] != "缺失"


def test_utility_supply_billing_settlement_basis_synonyms_are_covered():
    samples = [
        "供用电合同。双方以电能计量装置记录的数据作为结算依据。电价执行政府公示标准，每月结算，用户应在5日内付款。",
        "供用电合同。电费按实际抄表数结算，电价执行政府公示标准，每月结算，用户应在5日内付款。",
        "供用电合同。电费按计量表记录电量计算，电价执行政府公示标准，每月结算，用户应在5日内付款。",
        "供用电合同。以计量装置显示数量作为收费依据，电价执行政府公示标准，每月结算，用户应在5日内付款。",
    ]
    for text in samples:
        output = review_contract_v2(text, "utility_supply", use_llm=False)
        item = _item(output, "US-10-02")
        elements = {
            row["element_id"]: row["status"]
            for row in item.get("coverage_elements", [])
        }
        assert elements["metering_basis"] == "COVERED"
        assert item["coverage_status"] == "通过"


def test_utility_supply_safe_use_only_is_partial_not_missing_or_pass():
    output = review_contract_v2("供用电合同。用户应安全用电。", "utility_supply", use_llm=False)
    item = _item(output, "US-08-01")
    elements = {
        row["element_id"]: row["status"]
        for row in item.get("coverage_elements", [])
    }
    assert item["coverage_status"] == "部分覆盖"
    assert elements["safe_use"] == "COVERED"
    assert elements["economical_use"] == "MISSING"
    assert elements["planned_use"] == "MISSING"


def test_utility_supply_no_notice_interruption_clause_is_not_pass():
    output = review_contract_v2(
        "供用电合同。甲方未提前通知停电的，无论是否造成损失均不承担责任。",
        "utility_supply",
        use_llm=False,
    )
    item = _item(output, "US-05-04")
    assert item["coverage_status"] == "风险条款"
    assert item["evidence_clauses"]


def test_utility_supply_shared_safety_evidence_is_not_missing_in_sibling_rule():
    output = review_contract_v2(
        "供用电合同。第九条 用户应安全用电，不得采用危害电网安全的设备或者方式用电。",
        "utility_supply",
        use_llm=False,
    )
    assert _item(output, "US-08-02")["coverage_status"] in {"部分覆盖", "通过"}
    assert _item(output, "US-08-01")["coverage_status"] != "缺失"


def test_utility_supply_body_clause_does_not_prove_attachment_exists():
    text = (
        "供用电合同。第4条 计量装置资料、收费标准、抄表规则和账单样式按正文执行。"
        "第9条 产权分界处、供用设施图和线路图由双方现场确认。"
        "第10条 检修公告、欠费催告、抢修工单和恢复供应通知应保存。"
    )
    output = review_contract_v2(text, "utility_supply", use_llm=False)

    for item_id in ("US-12-02", "US-12-03", "US-12-04"):
        assert _item(output, item_id)["coverage_status"] != "通过"


def test_utility_supply_explicit_attachment_can_pass_attachment_rule():
    text = "供用电合同。附件一计量计费资料：计量装置资料、检定证书、收费标准、抄表规则和账单样式。"
    output = review_contract_v2(text, "utility_supply", use_llm=False)

    assert _item(output, "US-12-02")["coverage_status"] == "通过"


def test_utility_supply_missing_when_no_related_arrangement():
    output = review_contract_v2("供用电合同。双方签字盖章。", "utility_supply", use_llm=False)

    assert _item(output, "US-08-02")["coverage_status"] == "缺失"
    assert _item(output, "US-10-02")["coverage_status"] == "缺失"


def test_current_utility_supply_fixture_blocks_keyword_only_passes():
    from docx import Document

    text = "\n".join(
        paragraph.text
        for paragraph in Document("test_data/62 供用水电气热力合同.docx").paragraphs
        if paragraph.text.strip()
    )
    output = review_contract_v2(text, "utility_supply", use_llm=False)

    assert output["release_quality_gate"]["status"] == "REPORT_READY"
    assert _item(output, "US-03-04")["coverage_status"] == "缺失"
    assert not _item(output, "US-03-04")["evidence_clauses"]
    for key in ("US-06-04", "US-11-03"):
        assert _item(output, key)["coverage_status"] == "INSUFFICIENT_CONTEXT"
        assert _item(output, key)["applicability"]["applicable"] is None
    assert output["coverage_summary"]["待核验"] == 2
    assert sum(output["coverage_summary"].values()) == len(output["items"])
    assert _item(output, "US-04-04")["coverage_status"] == "风险条款"
    assert _item(output, "US-07-02")["coverage_status"] == "风险条款"
    assert _item(output, "US-12-01")["coverage_status"] == "部分覆盖"
    assert _item(output, "US-02-01")["coverage_status"] == "法律提示"
    for key in ("US-03-03", "US-04-01", "US-11-01"):
        assert _item(output, key)["coverage_status"] == "风险条款"
    termination = _item(output, "US-11-01")
    quotes = "\n".join(e["text"] for e in termination["evidence_clauses"])
    assert "不经济" in quotes and "经营成本" in quotes
    assert _item(output, "US-05-01")["coverage_status"] == "风险条款"
    assert _item(output, "US-05-02")["coverage_status"] == "风险条款"
    assert _item(output, "US-06-02")["coverage_status"] == "风险条款"
    assert _item(output, "US-07-03")["coverage_status"] == "风险条款"
    assert _item(output, "US-07-04")["coverage_status"] == "风险条款"
    assert _item(output, "US-08-02")["coverage_status"] == "部分覆盖"
    assert _item(output, "US-08-01")["coverage_status"] == "部分覆盖"
    assert _item(output, "US-10-02")["coverage_status"] == "通过"
    assert _item(output, "US-05-04")["coverage_status"] == "风险条款"
    for item_id in ("US-12-02", "US-12-03", "US-12-04"):
        assert _item(output, item_id)["coverage_status"] != "通过"
