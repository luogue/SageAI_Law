"""Structural tests for the gift-contract review checklist."""

from review_v2.engine import review_contract_v2
from review_v2.gift_contract_checklist import get_gift_checklist
from review_v2.house_lease_checklist import ReviewCheckpoint


def test_gift_review_checklist_has_48_points_and_12_modules():
    checklist = get_gift_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 48
    assert checklist[0].item_id == "G-01-01"
    assert checklist[-1].item_id == "G-12-04"
    assert module_ids == {f"G-{index:02d}" for index in range(1, 13)}
    assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_gift_review_checklist_fields_are_complete():
    checklist = get_gift_checklist()

    for checkpoint in checklist:
        assert checkpoint.item_id.startswith("G-")
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


def test_gift_review_checklist_has_risk_levels_and_forbidden_items():
    checklist = get_gift_checklist()
    risk_levels = {checkpoint.risk_level for checkpoint in checklist}
    kinds = {checkpoint.kind for checkpoint in checklist}

    assert risk_levels == {"高", "中", "低"}
    assert kinds == {"required", "forbidden"}


def test_gift_review_checklist_covers_required_special_rules():
    checklist = get_gift_checklist()
    by_node = {checkpoint.node_id: checkpoint for checkpoint in checklist}

    expected_nodes = {
        "gift_gratuitous_intent",
        "gift_arbitrary_revocation_before_transfer",
        "gift_irrevocable_exceptions",
        "gift_statutory_revocation_one_year",
        "gift_heir_revocation_six_months",
        "gift_poverty_defense_condition",
        "gift_compulsory_delivery_notarized",
        "gift_donor_fault_damage",
        "gift_obligation_attached_defect_warranty",
        "gift_return_after_revocation",
    }

    assert expected_nodes <= set(by_node)
    assert "第657条" in by_node["gift_gratuitous_intent"].legal_basis
    assert "第658条" in by_node["gift_arbitrary_revocation_before_transfer"].legal_basis
    assert "第663条" in by_node["gift_statutory_revocation_one_year"].legal_basis
    assert "第664条" in by_node["gift_heir_revocation_six_months"].legal_basis
    assert "第666条" in by_node["gift_poverty_defense_condition"].legal_basis
    assert "第660条" in by_node["gift_compulsory_delivery_notarized"].legal_basis
    assert "第662条" in by_node["gift_obligation_attached_defect_warranty"].legal_basis
    assert "第665条" in by_node["gift_return_after_revocation"].legal_basis


def test_gift_review_checklist_has_template_blank_criteria():
    checklist = get_gift_checklist()

    assert any("__" in checkpoint.suggested_clause for checkpoint in checklist)
    assert all(
        "空白" in checkpoint.partial_criteria
        or "未勾选" in checkpoint.partial_criteria
        or checkpoint.kind == "forbidden"
        for checkpoint in checklist
    )


def test_review_v2_can_load_gift_contract_checklist():
    output = review_contract_v2(
        "赠与人自愿将名下车辆一辆无偿赠与受赠人，受赠人表示接受赠与。双方约定办理过户登记。",
        "gift",
        use_llm=False,
    )

    assert output["success"] is True
    assert output["contract_type"] == "gift"
    assert output["contract_type_name"] == "赠与合同"
    assert output["all_items_count"] == 48
    assert len(output["items"]) == 48
    assert output["summary"]["高"] + output["summary"]["中"] + output["summary"]["低"] == 48


def test_gift_consideration_clause_ignores_negated_counterparty_payment():
    output = review_contract_v2(
        "第一条 本合同为赠与合同。第二条 本赠与为无偿赠与，乙方无需向甲方支付任何对价。"
        "第三条 甲方将车辆一辆赠与乙方，乙方表示接受赠与。",
        "gift",
        use_llm=False,
    )
    item = next(item for item in output["items"] if item["item_id"] == "G-01-04")

    assert item["risk_level"] == "低"
    assert item["coverage_status"] == "通过"
    assert item["issue_type"] == "通过"
    assert "无偿赠与" in item["reasoning_summary"]


def test_gift_attached_obligation_remedy_depends_on_obligation_content():
    output = review_contract_v2(
        "第一条 本合同为赠与合同。第二条 本赠与为无偿赠与，乙方无需向甲方支付任何对价。"
        "第三条 甲方将车辆一辆赠与乙方，乙方表示接受赠与。"
        "第九条 本赠与为附义务赠与，乙方应履行以下义务：__；"
        "乙方不履行义务的，甲方可要求补救或撤销赠与。",
        "gift",
        use_llm=False,
    )
    by_id = {item["item_id"]: item for item in output["items"]}

    assert by_id["G-09-01"]["coverage_status"] == "部分覆盖"
    assert by_id["G-09-01"]["issue_type"] == "模板空白"
    assert by_id["G-09-03"]["risk_level"] == "中"
    assert by_id["G-09-03"]["coverage_status"] == "部分覆盖"
    assert by_id["G-09-03"]["issue_type"] == "模板空白"
    assert "G-09-01" in by_id["G-09-03"]["reasoning_summary"]


def test_gift_dependency_rules_sync_related_items():
    output = review_contract_v2(
        "第一条 本合同为赠与合同。甲方将车辆一辆赠与乙方，乙方表示接受赠与。"
        "第九条 本赠与为附义务赠与，乙方应履行以下义务：__；"
        "第十一条 赠与撤销后，乙方应返还赠与财产。",
        "gift",
        use_llm=False,
    )
    by_id = {item["item_id"]: item for item in output["items"]}

    assert by_id["G-10-04"]["risk_level"] == "中"
    assert by_id["G-10-04"]["coverage_status"] == by_id["G-09-01"]["coverage_status"]
    assert by_id["G-10-04"]["issue_type"] == by_id["G-09-01"]["issue_type"]
    assert "G-09-01" in by_id["G-10-04"]["reasoning_summary"]
    assert by_id["G-11-01"]["risk_level"] == "中"
    assert by_id["G-11-01"]["coverage_status"] == by_id["G-01-02"]["coverage_status"]
    assert by_id["G-11-01"]["issue_type"] == by_id["G-01-02"]["issue_type"]
    assert "G-01-02" in by_id["G-11-01"]["reasoning_summary"]
