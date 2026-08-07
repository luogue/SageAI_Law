"""Structural tests for the sale-contract review checklist."""

from review_v2.house_lease_checklist import ReviewCheckpoint
from review_v2.engine import COVERAGE_NOT_APPLICABLE, ISSUE_NOT_APPLICABLE, review_contract_v2
from review_v2.sale_contract_checklist import get_sale_checklist


def test_sale_review_checklist_has_48_points_and_12_modules():
    checklist = get_sale_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 48
    assert checklist[0].item_id == "S-01-01"
    assert checklist[-1].item_id == "S-12-04"
    assert module_ids == {f"S-{index:02d}" for index in range(1, 13)}
    assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_sale_review_checklist_fields_are_complete():
    checklist = get_sale_checklist()

    for checkpoint in checklist:
        assert checkpoint.item_id.startswith("S-")
        assert checkpoint.node_id
        assert checkpoint.title
        assert checkpoint.kind in {"required", "forbidden"}
        assert checkpoint.risk_level in {"高", "中", "低"}
        assert checkpoint.terms
        assert checkpoint.risk_point_missing
        assert checkpoint.risk_point_present
        assert checkpoint.suggested_clause
        assert checkpoint.legal_basis
        assert checkpoint.legal_consequence_if_missing
        assert checkpoint.semantic_question
        assert checkpoint.evidence_scope
        assert checkpoint.pass_criteria
        assert checkpoint.partial_criteria
        assert checkpoint.applicable_if


def test_sale_review_checklist_has_risk_levels_and_forbidden_items():
    checklist = get_sale_checklist()
    risk_levels = {checkpoint.risk_level for checkpoint in checklist}
    kinds = {checkpoint.kind for checkpoint in checklist}

    assert risk_levels == {"高", "中", "低"}
    assert kinds == {"required", "forbidden"}


def test_sale_review_checklist_covers_required_special_rules():
    checklist = get_sale_checklist()
    by_node = {checkpoint.node_id: checkpoint for checkpoint in checklist}

    expected_nodes = {
        "sale_risk_transfer_delivery",
        "sale_risk_carrier_delivery",
        "sale_risk_goods_in_transit",
        "sale_inspection_period_reasonable",
        "sale_liquidated_damages_adjustment",
        "sale_retention_registration",
        "sale_expectation_loss",
        "sale_expectation_loss_exclusion",
        "sale_trial_risk",
    }

    assert expected_nodes <= set(by_node)
    assert "第604条" in by_node["sale_risk_transfer_delivery"].legal_basis
    assert "第607条" in by_node["sale_risk_carrier_delivery"].legal_basis
    assert "第606条" in by_node["sale_risk_goods_in_transit"].legal_basis
    assert "第622条" in by_node["sale_inspection_period_reasonable"].legal_basis
    assert "第585条" in by_node["sale_liquidated_damages_adjustment"].legal_basis
    assert "第641条" in by_node["sale_retention_registration"].legal_basis
    assert "第584条" in by_node["sale_expectation_loss"].legal_basis
    assert "第640条" in by_node["sale_trial_risk"].legal_basis


def test_sale_review_risk_level_adjustments_for_intent_and_delivery_method():
    checklist = get_sale_checklist()
    by_id = {checkpoint.item_id: checkpoint for checkpoint in checklist}

    assert by_id["S-01-02"].risk_level == "中"
    assert by_id["S-03-03"].risk_level == "中"


def test_sale_review_checklist_has_template_blank_criteria():
    checklist = get_sale_checklist()

    assert any("__" in checkpoint.suggested_clause for checkpoint in checklist)
    assert all(
        "空白" in checkpoint.partial_criteria
        or "未勾选" in checkpoint.partial_criteria
        or checkpoint.kind == "forbidden"
        for checkpoint in checklist
    )


def test_review_v2_can_load_sale_contract_checklist():
    output = review_contract_v2(
        "出卖人向买受人出售设备一批，约定价款100000元，交付后验收，质量标准按附件执行。",
        "sale",
        use_llm=False,
    )

    assert output["success"] is True
    assert output["contract_type"] == "sale"
    assert output["contract_type_name"] == "买卖合同"
    assert output["all_items_count"] == 48
    assert len(output["items"]) == 48
    assert output["summary"]["高"] + output["summary"]["中"] + output["summary"]["低"] == (
        48 - output["coverage_summary"].get(COVERAGE_NOT_APPLICABLE, 0)
    )


def test_sale_review_skips_special_transaction_points_for_simple_template():
    output = review_contract_v2(
        "出卖人向买受人出售办公桌十张，总价款10000元。买受人一次性付款，出卖人于2026年8月10日前交付，验收合格后合同履行完毕。",
        "sale",
        use_llm=False,
    )

    skipped_ids = {
        "S-04-03",
        "S-09-01",
        "S-09-02",
        "S-09-03",
        "S-09-04",
        "S-10-01",
        "S-10-02",
        "S-10-03",
        "S-10-04",
    }
    by_id = {item["item_id"]: item for item in output["items"]}

    assert skipped_ids <= set(by_id)
    assert output["coverage_summary"][COVERAGE_NOT_APPLICABLE] >= len(skipped_ids)
    assert output["summary"]["高"] + output["summary"]["中"] + output["summary"]["低"] == 48 - output["coverage_summary"][COVERAGE_NOT_APPLICABLE]
    for item_id in skipped_ids:
        item = by_id[item_id]
        assert item["coverage_status"] == COVERAGE_NOT_APPLICABLE
        assert item["issue_type"] == ISSUE_NOT_APPLICABLE
        assert item["risk_level"] == COVERAGE_NOT_APPLICABLE
        assert item["judge_source"] == "applicability_filter"
        assert item["applicable_if"]


def test_sale_review_applies_special_points_when_trigger_keywords_exist():
    output = review_contract_v2(
        "本合同为分期付款买卖，买受人每期支付价款；买受人付清全款前，出卖人保留所有权。"
        "标的物为已发运的在途货物，并按封样样品交付。双方约定先试用三日。",
        "sale",
        use_llm=False,
    )

    triggered_ids = {
        "S-04-03",
        "S-09-01",
        "S-09-02",
        "S-09-03",
        "S-09-04",
        "S-10-01",
        "S-10-02",
        "S-10-03",
        "S-10-04",
    }
    by_id = {item["item_id"]: item for item in output["items"]}

    for item_id in triggered_ids:
        assert by_id[item_id]["coverage_status"] != COVERAGE_NOT_APPLICABLE


def test_sale_delivery_method_transport_only_is_partial_template_blank():
    output = review_contract_v2(
        "第三条 运输方式：由甲方负责运输。",
        "sale",
        use_llm=False,
    )
    item = next(item for item in output["items"] if item["item_id"] == "S-03-03")

    assert item["risk_level"] == "中"
    assert item["coverage_status"] == "部分覆盖"
    assert item["issue_type"] == "模板空白"
    assert any("运输方式" in clause["text"] for clause in item["evidence_clauses"])
    assert "签收" in item["reasoning_summary"]


def test_sale_delivery_method_with_signoff_terms_passes():
    output = review_contract_v2(
        "第三条 运输方式：由甲方负责运输。买受人或授权收货人在送货单、签收单或物流回执上签字即视为完成交付。",
        "sale",
        use_llm=False,
    )
    item = next(item for item in output["items"] if item["item_id"] == "S-03-03")

    assert item["coverage_status"] == "通过"
    assert item["risk_level"] == "低"
    assert item["issue_type"] == "通过"


def test_sale_quality_objection_with_replace_and_reship_is_partial():
    output = review_contract_v2(
        "第7.1条 买受人发现质量问题应在10日内提出，甲方应及时更换补发。",
        "sale",
        use_llm=False,
    )
    item = next(item for item in output["items"] if item["item_id"] == "S-06-03")

    assert item["risk_level"] == "中"
    assert item["coverage_status"] == "部分覆盖"
    assert item["issue_type"] == "条款缺陷"
    assert any("更换补发" in clause["text"] for clause in item["evidence_clauses"])
    assert "修理" in item["reasoning_summary"]


def test_sale_cement_contract_practical_risk_level_corrections():
    output = review_contract_v2(
        "本合同标的物为普通硅酸盐水泥，数量100吨。"
        "水泥到货后买受人当场验收，质量问题应在10日内提出，出卖人及时更换补发。"
        "质保期为验收合格后三个月。",
        "sale",
        use_llm=False,
    )
    by_id = {item["item_id"]: item for item in output["items"]}

    assert by_id["S-01-03"]["risk_level"] == "中"
    assert by_id["S-01-03"]["coverage_status"] == "缺失"
    assert by_id["S-01-03"]["issue_type"] == "完全缺失"

    assert by_id["S-07-02"]["risk_level"] == "中"
    assert by_id["S-07-02"]["coverage_status"] == "缺失"
    assert by_id["S-07-02"]["issue_type"] == "完全缺失"

    assert by_id["S-07-03"]["risk_level"] == "中"
    assert by_id["S-07-03"]["coverage_status"] == "缺失"
    assert by_id["S-07-03"]["issue_type"] == "完全缺失"

    assert by_id["S-12-02"]["risk_level"] == "中"
    assert by_id["S-12-02"]["coverage_status"] == "缺失"
    assert by_id["S-12-02"]["issue_type"] == "完全缺失"
    assert not by_id["S-12-02"]["evidence_clauses"]
