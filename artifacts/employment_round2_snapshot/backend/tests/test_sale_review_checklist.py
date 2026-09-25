"""Structural tests for the sale-contract review checklist."""

from review_v2.house_lease_checklist import ReviewCheckpoint
from review_v2.engine import COVERAGE_NOT_APPLICABLE, ISSUE_NOT_APPLICABLE, review_contract_v2
from review_v2.sale_contract_checklist import get_sale_checklist
from review_v2.user_profile import UserRiskProfile


def test_sale_review_checklist_has_56_points_and_13_modules():
    checklist = get_sale_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 56
    assert checklist[0].item_id == "S-00-01"
    assert checklist[-1].item_id == "S-12-04"
    assert module_ids == {f"S-{index:02d}" for index in range(0, 13)}
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
        "sale_unilateral_price_adjustment",
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

    assert by_id["S-00-01"].risk_level == "低"
    assert by_id["S-01-02"].risk_level == "低"
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
    assert output["all_items_count"] == 56
    assert len(output["items"]) == 56
    assert output["summary"]["高"] + output["summary"]["中"] + output["summary"]["低"] == (
        56 - output["coverage_summary"].get(COVERAGE_NOT_APPLICABLE, 0)
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
    assert output["summary"]["高"] + output["summary"]["中"] + output["summary"]["低"] == 56 - output["coverage_summary"][COVERAGE_NOT_APPLICABLE]
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
        profile=UserRiskProfile(user_identity="卖方"),
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
    assert by_id["S-07-02"]["coverage_status"] == "INSUFFICIENT_CONTEXT"
    assert by_id["S-07-02"]["needs_manual_review"]

    assert by_id["S-07-03"]["risk_level"] == "中"
    assert by_id["S-07-03"]["coverage_status"] == "缺失"
    assert by_id["S-07-03"]["issue_type"] == "完全缺失"

    assert by_id["S-12-02"]["risk_level"] == "中"
    assert by_id["S-12-02"]["coverage_status"] == "缺失"
    assert by_id["S-12-02"]["issue_type"] == "完全缺失"
    assert not by_id["S-12-02"]["evidence_clauses"]


def test_sale_review_boundary_payment_account_reasonable_penalty_and_common_layer():
    output = review_contract_v2(
        """
        买卖合同
        第一条 标的物为普通水泥，数量100吨。
        第六条 货款支付：乙方应通过银行转账方式向甲方指定收款账户支付货款。开户行：中国银行上海分行，银行账号：622200001234。
        第八条 违约责任：乙方逾期付款的，每日按逾期未付款项的万分之三向甲方支付违约金。
        第十条 本合同自双方签字盖章之日起生效。
        第十一条 争议解决：双方协商不成的，依法向有管辖权的人民法院起诉；败诉方承担律师费、诉讼费等实现债权费用。
        （以下无正文）
        测试重点关注项：
        第四条）：S-08-01 应被判定为高风险。
        """,
        "sale",
        use_llm=False,
    )
    by_id = {item["item_id"]: item for item in output["items"]}

    for item in output["items"]:
        for clause in item["evidence_clauses"]:
            assert "测试重点" not in clause["text"]
            assert "应被判定为" not in clause["text"]

    assert by_id["S-05-03"]["risk_level"] == "低"
    assert by_id["S-05-03"]["coverage_status"] == "通过"
    assert any("开户行" in clause["text"] for clause in by_id["S-05-03"]["evidence_clauses"])

    assert by_id["S-08-02"]["risk_level"] == "低"
    assert by_id["S-08-02"]["coverage_status"] == "通过"
    assert "合理区间" in by_id["S-08-02"]["reasoning_summary"]

    assert by_id["S-00-01"]["coverage_status"] == "通过"
    assert by_id["S-00-04"]["risk_level"] == "中"
    assert by_id["S-00-04"]["coverage_status"] == "部分覆盖"
    assert "具体法院" in by_id["S-00-04"]["reasoning_summary"]
    assert by_id["S-00-05"]["risk_level"] == "低"
    assert by_id["S-00-05"]["coverage_status"] == "通过"


def test_sale_review_calibrates_payment_schedule_price_adjustment_intent_effectiveness_and_signoff():
    output = review_contract_v2(
        """
        水泥买卖合同
        甲乙双方经友好协商，达成如下协议。
        第一条 标的物为普通硅酸盐水泥，单价为500元/吨。若因市场行情变化，单价确需调整的，甲方可向乙方发出书面通知予以调整。
        第三条 由甲方负责运输，货物由乙方工作人员或指定人员签收，视为乙方签收。
        第六条 货款结算：每批次货物签收后，乙方应于次月10日前向甲方支付该批次全部货款。
        第七条 乙方逾期支付货款的，应当按天万分之三支付违约金。
        """,
        "sale",
        use_llm=False,
    )
    by_id = {item["item_id"]: item for item in output["items"]}

    assert by_id["S-05-02"]["risk_level"] == "低"
    assert by_id["S-05-02"]["coverage_status"] == "通过"
    assert "比例审查不适用" in by_id["S-05-02"]["reasoning_summary"]

    assert by_id["S-02-05"]["risk_level"] == "中"
    assert by_id["S-02-05"]["coverage_status"] == "风险条款"
    assert "无幅度限制" in by_id["S-02-05"]["reasoning_summary"] or "缺少幅度限制" in by_id["S-02-05"]["reasoning_summary"]

    assert by_id["S-01-02"]["risk_level"] == "低"
    assert by_id["S-01-02"]["coverage_status"] == "通过"
    assert "法律不强求" in by_id["S-01-02"]["reasoning_summary"]

    assert by_id["S-00-01"]["risk_level"] == "低"
    assert by_id["S-00-01"]["coverage_status"] == "缺失"
    assert by_id["S-00-01"]["review_priority"] == "C_OPTIMIZATION"
    assert "可选优化" in by_id["S-00-01"]["action_suggestion"]

    assert by_id["S-03-03"]["risk_level"] == "低"
    assert by_id["S-03-03"]["coverage_status"] == "部分覆盖"
    assert any(e["element_id"] == "goods_receipt_record" and e["status"] == "MISSING"
               for e in by_id["S-03-03"]["coverage_elements"])
    assert "凭证" in by_id["S-03-03"]["reasoning_summary"]
