from __future__ import annotations

import asyncio
import io
from pathlib import Path
from types import SimpleNamespace

from review_v2.recommendation_impact import evaluate_recommendations
from review_v2.engine import ReviewItemResult, _combine_quality_gates, _coverage_elements_for_item, review_contract_v2
from routers.review_v2 import review_v2_file


ROOT = Path(__file__).resolve().parents[2]


class _Upload:
    def __init__(self, path: Path):
        self.filename = path.name
        self.file = io.BytesIO(path.read_bytes())


def _review_file(path: Path, contract_type: str) -> dict:
    return asyncio.run(
        review_v2_file(
            file=_Upload(path),
            contract_type=contract_type,
            include_low_risk=True,
            use_llm=False,
            profile_json="{}",
            current_user={"id": "service-transaction-structure-test"},
        )
    )


def _items_by_id(result: dict) -> dict:
    return {item["item_id"]: item for item in result["items"]}


def test_blocked_quality_gate_always_exposes_blocking_rule():
    gate = _combine_quality_gates({"status": "BLOCKED", "failures": [], "gate_results": {}})

    assert gate["status"] == "BLOCKED"
    assert gate["blocking_rules"]
    assert gate["blocking_rules"][0]["code"] == "QUALITY_GATE_INTERNAL_INCONSISTENCY"


def test_obvious_service_contract_routes_to_service_without_title_dependency():
    text = (
        "甲方委托乙方提供企业咨询。乙方应按服务内容清单提供服务，服务期限三个月。"
        "甲方向乙方支付服务费人民币50000元。乙方提交服务成果报告后，甲方应在五日内按验收标准完成验收。"
    )
    result = review_contract_v2(text, "service", use_llm=False)

    assert result["release_quality_gate"]["status"] == "REPORT_READY"
    assert result["contract_context"]["contract_family"] == "SERVICE"
    assert result["contract_context"]["transaction_structure"] == "SERVICE"
    assert result["contract_context"]["contract_subtype"] == "GENERAL_SERVICE"
    assert result["report_context"]["scenario_label"] == "一般服务合同"
    assert result["domain_selection_resolution"]["classification_evidence"]
    assert sum(1 for item in result["items"] if item["item_id"].startswith("SVC-")) > 0


def test_service_title_does_not_override_sale_substance():
    text = (
        "服务合同。甲方向乙方购买服务器设备100台，货物名称、规格型号、数量、单价详见订单。"
        "乙方负责交货，甲方验收合格后支付货款。"
    )
    result = review_contract_v2(text, "service", use_llm=False)

    assert result["release_quality_gate"]["status"] == "REPORT_READY"
    assert result["domain_selection_resolution"]["resolution"] == "DOCUMENT_OVERRIDE"
    assert result["domain_selection_resolution"]["selected_domain"] == "SALE"
    assert result["contract_type"] == "sale"
    assert result["contract_context"]["contract_family"] == "SALE"
    assert result["contract_context"]["transaction_structure"] == "SINGLE_TRANSACTION"
    assert sum(1 for item in result["items"] if item["item_id"].startswith("SVC-")) == 0


def test_real_service_contract_file_uses_service_scenario_and_reviews():
    path = next((ROOT / "test_data").glob("3*.docx"))
    result = _review_file(path, "service")

    assert result["release_quality_gate"]["status"] == "REPORT_READY"
    assert result["contract_context"]["contract_family"] == "SERVICE"
    assert result["contract_context"]["transaction_structure"] == "SERVICE"
    assert result["report_context"]["scenario_label"] == "一般服务合同"
    assert result["report_context"]["report_title"] == "服务合同审查报告"
    assert result["domain_selection_resolution"]["classification_evidence"]
    assert sum(1 for item in result["items"] if item["item_id"].startswith("SVC-")) == result["all_items_count"]


def test_real_service_contract_review_semantics_are_not_template_completeness_noise():
    path = next((ROOT / "test_data").glob("3*.docx"))
    result = _review_file(path, "service")
    by_id = _items_by_id(result)

    assert result["release_quality_gate"]["status"] == "REPORT_READY"
    assert len(result["risk_findings"]) < 26
    for review_id in ("SVC-01-02", "SVC-01-03", "SVC-01-04"):
        item = by_id[review_id]
        assert item["coverage_status"] == "通过"
        assert item["related_risks"] == []
        assert item["decision_trace"]["review_nature"] == "INTERNAL_CLASSIFICATION"
        assert item["decision_trace"]["requirement_medium"] == "LEGAL_CHARACTERIZATION"
        assert not [
            disposition for disposition in result["final_dispositions"]
            if review_id in disposition["review_ids"]
        ]

    assert by_id["SVC-06-04"]["coverage_status"] == "不适用"
    assert by_id["SVC-07-03"]["coverage_status"] == "不适用"
    assert by_id["SVC-03-04"]["coverage_status"] == "通过"
    assert by_id["SVC-02-04"]["coverage_status"] == "通过"
    assert by_id["SVC-10-01"]["coverage_status"] == "通过"
    assert by_id["SVC-05-02"]["decision_trace"]["requirement_medium"] == "SIGNING_PROCESS"
    assert by_id["SVC-05-02"]["decision_trace"]["action_type"] == "SIGNING_PROCESS"
    assert "其余关键要素" not in result["result"]
    assert all(
        disposition["final_reason"]
        for disposition in result["final_dispositions"]
        if disposition["severity"] in {"重大风险", "HIGH", "CRITICAL"} and disposition["final_action"] != "MUST_CHANGE"
    )


def test_real_service_contract_round3_aggregates_risks_and_keeps_element_gaps_specific():
    path = next((ROOT / "test_data").glob("3*.docx"))
    result = _review_file(path, "service")
    by_id = _items_by_id(result)
    findings_by_group = {finding["risk_group"]: finding for finding in result["risk_findings"]}

    problematic_review_count = sum(
        1 for item in result["items"]
        if item["coverage_status"] in {"缺失", "部分覆盖", "风险条款"}
    )
    assert result["release_quality_gate"]["status"] == "REPORT_READY"
    assert len(result["risk_findings"]) < problematic_review_count
    assert len(result["recommendations"]) < problematic_review_count

    refund = findings_by_group["service_refund_termination_settlement"]
    assert len(refund["source_review_ids"]) > 1
    assert {"SVC-06-01", "SVC-11-02", "SVC-11-03"} <= set(refund["source_review_ids"])

    performance = findings_by_group["service_performance_remedy_framework"]
    assert {"SVC-08-01", "SVC-08-02"} <= set(performance["source_review_ids"])

    scope = findings_by_group["service_scope_delivery_standard"]
    assert {"SVC-03-01", "SVC-03-02", "SVC-03-03"} <= set(scope["source_review_ids"])

    assert by_id["SVC-06-04"]["coverage_status"] == "不适用"
    assert by_id["SVC-06-04"]["related_risks"] == []
    assert by_id["SVC-06-04"]["narrative_state"]["recommendation_ids"] == []

    for review_id in ("SVC-06-01", "SVC-11-02", "SVC-11-03"):
        state = by_id[review_id]["narrative_state"]
        assert state["missing_elements"]
        assert "现有信息不足以确定具体缺失字段" not in state["missing_elements"]
        assert all(element != "core_contract_arrangement" for element in state["missing_elements"])

    assert "具体未明要素" not in result["result"]
    assert "其余关键要素" not in result["result"]
    assert "对应的核心安排" not in result["result"]
    assert all("legal_requirement_strength" in recommendation["impact"] for recommendation in result["recommendations"])
    assert all("dispute_reduction_value" in recommendation["impact"] for recommendation in result["recommendations"])
    assert all(
        disposition.get("severity_action_alignment") == "HIGH_DOWNGRADED_WITH_REASON"
        and disposition.get("downgrade_reason")
        for disposition in result["final_dispositions"]
        if disposition["severity"] in {"HIGH", "CRITICAL", "重大风险"} and disposition["final_action"] != "MUST_CHANGE"
    )


def test_real_service_contract_round4_preserves_semantic_element_truth():
    path = next((ROOT / "test_data").glob("3*.docx"))
    result = _review_file(path, "service")
    by_id = _items_by_id(result)

    def element_status(review_id: str) -> dict:
        return {
            element["element_id"]: element
            for element in by_id[review_id]["coverage_elements"]
        }

    schedule = element_status("SVC-03-03")
    assert schedule["service_time"]["status"] == "COVERED"
    assert schedule["start_date"]["status"] == "COVERED"
    assert schedule["end_date"]["status"] == "COVERED"
    assert "开课日期或服务开始日期明确" not in by_id["SVC-03-03"]["narrative_state"]["missing_elements"]
    assert "预计结课日期、结束日期或服务期限明确" not in by_id["SVC-03-03"]["narrative_state"]["missing_elements"]

    health = element_status("SVC-06-01")
    assert health["termination_trigger"]["status"] == "COVERED"
    assert health["proof_or_notice"]["status"] == "COVERED"
    assert health["provided_service_deduction"]["status"] == "COVERED"
    assert "健康原因、个人原因或其他解除触发条件明确" not in by_id["SVC-06-01"]["narrative_state"]["missing_elements"]

    withdrawal = by_id["SVC-09-01"]
    assert withdrawal["coverage_status"] != "缺失"
    assert any("第五条（一）" in (evidence.get("location") or "") for evidence in withdrawal["evidence_clauses"])
    assert element_status("SVC-09-01")["termination_trigger"]["status"] == "COVERED"

    partial_refund = element_status("SVC-04-04")
    assert by_id["SVC-04-04"]["coverage_status"] != "缺失"
    assert partial_refund["refund_trigger"]["status"] == "COVERED"
    assert partial_refund["provided_service_value"]["status"] == "COVERED"
    assert result["release_quality_gate"]["gate_results"]["ELEMENT_STATUS_CONTRADICTION"] == "PASS"
    assert result["release_quality_gate"]["gate_results"]["EVIDENCE_MONOTONICITY_VIOLATION"] == "PASS"


def test_service_contract_fact_registry_shared_consumers_in_production_pipeline():
    result = review_contract_v2(
        """
        培训服务合同
        甲方为培训机构，乙方为学员。
        第一条 服务内容
        （一）课程名称：小学数学思维拓展（奥数入门）
        班级编号：SX-2026-A01
        总课时：60节
        每次：2节，每节45分钟
        上课时间：每周六上午9:00-10:30
        开课日期：2026年9月10日
        预计结课日期：2027年6月30日
        第二条 收费标准附件
        培训费用合计：12600元
        课时费：12000元
        200元/节 × 60节
        培训资料费：600元
        第三条 退费
        乙方申请退费的，按实际消耗课时结算培训费用，未消耗课时对应费用退还。
        """,
        "service",
        use_llm=False,
    )
    by_id = _items_by_id(result)
    audit = result["observability"]["contract_fact_flow_audit"]
    rows = {row["canonical_fact_key"]: row for row in audit["facts"]}
    snapshot_id = result["contract_facts"]["fact_registry_snapshot_id"]

    assert result["release_quality_gate"]["status"] == "REPORT_READY"
    assert result["contract_fact_registry_gate"]["gate_results"]["FACT_REGISTRY_SNAPSHOT_CONSISTENCY"] == "PASS"
    assert result["contract_fact_registry_gate"]["gate_results"]["CROSS_REVIEW_FACT_CONFLICT"] == "PASS"
    assert audit["registry_created"] is True
    assert audit["registry_fact_count"] > 0
    assert audit["registry_snapshot_consistency"] == "PASS"
    assert audit["cross_review_fact_conflicts"] == []

    for key in (
        "service.course_name",
        "service.project_id",
        "service.total_sessions",
        "service.session_duration",
        "service.schedule",
        "service.start_date",
        "service.end_date",
        "payment.total_fee",
        "payment.session_fee_total",
        "payment.unit_price",
        "payment.total_sessions",
        "payment.material_fee",
    ):
        assert rows[key]["registry_status"] == "FOUND"

    assert "SVC-03-01" in rows["service.course_name"]["consumer_review_ids"]
    assert "SVC-03-03" in rows["service.schedule"]["consumer_review_ids"]
    assert {"SVC-04-02", "SVC-12-02"} <= set(rows["payment.unit_price"]["consumer_review_ids"])
    assert {"SVC-04-02", "SVC-12-02"} <= set(rows["payment.material_fee"]["consumer_review_ids"])

    assert by_id["SVC-03-01"]["decision_trace"]["fact_registry_snapshot_id"] == snapshot_id
    assert by_id["SVC-03-03"]["decision_trace"]["fact_registry_snapshot_id"] == snapshot_id
    assert by_id["SVC-04-02"]["decision_trace"]["fact_registry_snapshot_id"] == snapshot_id
    assert by_id["SVC-12-02"]["decision_trace"]["fact_registry_snapshot_id"] == snapshot_id

    svc_0301 = {element["element_id"]: element["status"] for element in by_id["SVC-03-01"]["coverage_elements"]}
    svc_0303 = {element["element_id"]: element["status"] for element in by_id["SVC-03-03"]["coverage_elements"]}
    svc_0402 = {element["element_id"]: element["status"] for element in by_id["SVC-04-02"]["coverage_elements"]}
    svc_1202 = {element["element_id"]: element["status"] for element in by_id["SVC-12-02"]["coverage_elements"]}
    assert svc_0301["service_name"] == "COVERED"
    assert svc_0301["class_or_project_id"] == "COVERED"
    assert svc_0301["service_hours"] == "COVERED"
    assert svc_0301["session_duration"] == "COVERED"
    assert svc_0303["service_time"] == "COVERED"
    assert svc_0303["start_date"] == "COVERED"
    assert svc_0303["end_date"] == "COVERED"
    assert svc_0402["total_fee"] == "COVERED"
    assert svc_0402["unit_price"] == "COVERED"
    assert svc_1202["fee_schedule_attachment"] == "COVERED"
    assert svc_1202["tuition_and_material_fee_split"] == "COVERED"
    assert svc_1202["refund_unit_price"] == "COVERED"


def test_registry_found_fact_is_not_overridden_by_empty_legacy_evidence():
    item = ReviewItemResult(
        item_id="SVC-03-01",
        node_id="service_content_standard",
        title="服务内容清单",
        risk_level="高",
        status="缺失或不明确",
        risk_point_description="",
        suggested_clause_example="",
        legal_basis_index="",
        legal_consequence_if_missing="",
        applicable_if="",
        matched_terms=[],
        coverage_status="缺失",
        issue_type="条款缺失",
        evidence_clauses=[],
        evidence_location="",
        reasoning_summary="",
    )
    item.decision_trace["contract_fact_registry_consumption"] = {
        "snapshot_id": "CFR-TEST",
        "required_fact_keys": ["service.course_name"],
        "facts": {
            "service.course_name": {
                "status": "FOUND",
                "value": "数学培训",
                "fact_ids": ["F-SERVICE-COURSE-NAME-001"],
                "source_clause_ids": ["C0001"],
                "source_spans": ["课程名称：数学培训"],
                "source_locations": [],
                "confidence": "high",
            }
        },
    }

    elements = _coverage_elements_for_item(item)
    by_element = {element.element_id: element for element in elements}

    assert by_element["service_name"].status == "COVERED"
    assert by_element["service_name"].claim_id == "service.course_name"


def test_registry_conflicting_fact_blocks_report_instead_of_selecting_one_value():
    result = review_contract_v2(
        "培训服务合同。课程名称：数学培训。课程名称：英语培训。总课时：20节。上课时间：每周六上午。"
        "开课日期：2026年9月10日。预计结课日期：2027年6月30日。",
        "service",
        use_llm=False,
    )

    assert result["contract_fact_registry_gate"]["gate_results"]["FACT_REGISTRY_CONFLICTING_FACT"] == "FAIL"
    assert result["release_quality_gate"]["status"] == "BLOCKED"
    assert result["contract_fact_registry_gate"]["conflicting_fact_count"] >= 1
    rows = {
        row["canonical_fact_key"]: row
        for row in result["observability"]["contract_fact_flow_audit"]["facts"]
    }
    assert rows["service.course_name"]["registry_status"] == "CONFLICTING"


def test_service_round4_mutations_preserve_and_remove_explicit_evidence():
    with_start = review_contract_v2(
        "服务合同。课程名称：数学培训。总课时数：20节。"
        "上课时间：每周六上午9:00-10:30。"
        "开课日期：2026年9月10日。预计结课日期：2027年6月30日。",
        "service",
        use_llm=False,
    )
    no_start = review_contract_v2(
        "服务合同。课程名称：数学培训。总课时数：20节。"
        "上课时间：每周六上午9:00-10:30。预计结课日期：2027年6月30日。",
        "service",
        use_llm=False,
    )
    with_start_elements = _items_by_id(with_start)["SVC-03-03"]["coverage_elements"]
    no_start_elements = _items_by_id(no_start)["SVC-03-03"]["coverage_elements"]

    assert {e["element_id"]: e["status"] for e in with_start_elements}["start_date"] == "COVERED"
    assert {e["element_id"]: e["status"] for e in no_start_elements}["start_date"] in {"MISSING", "UNCERTAIN"}

    selected = review_contract_v2(
        "服务合同。乙方因身体健康状况不再适合参与培训，应及时书面通知甲方。"
        "☑按照实际消耗课时结算培训费用 □调整培训时间或内容。",
        "service",
        use_llm=False,
    )
    unselected = review_contract_v2(
        "服务合同。乙方因身体健康状况不再适合参与培训，应及时书面通知甲方。"
        "□按照实际消耗课时结算培训费用 □调整培训时间或内容。",
        "service",
        use_llm=False,
    )
    selected_health = {
        e["element_id"]: e["status"]
        for e in _items_by_id(selected)["SVC-06-01"]["coverage_elements"]
    }
    unselected_health = {
        e["element_id"]: e["status"]
        for e in _items_by_id(unselected)["SVC-06-01"]["coverage_elements"]
    }
    assert selected_health["provided_service_deduction"] == "COVERED"
    assert unselected_health["provided_service_deduction"] in {"MISSING", "UNCERTAIN"}


def test_service_negative_review_absent_passes_and_adverse_clause_triggers():
    clean = review_contract_v2(
        "服务合同。甲方向乙方提供培训服务，课程共60课时，服务期限三个月。乙方按约支付服务费，双方按实际课时结算退费。",
        "service",
        use_llm=False,
    )
    clean_items = _items_by_id(clean)
    assert clean_items["SVC-03-04"]["coverage_status"] == "通过"
    assert clean_items["SVC-10-01"]["coverage_status"] == "通过"
    assert clean_items["SVC-03-04"]["decision_trace"]["review_polarity"] == "NEGATIVE_CLAUSE_CHECK"

    adverse = review_contract_v2(
        "服务合同。甲方向乙方提供培训服务，甲方承诺保过包过、保证成绩。乙方付款后一律概不退款。",
        "service",
        use_llm=False,
    )
    adverse_items = _items_by_id(adverse)
    assert adverse_items["SVC-03-04"]["coverage_status"] == "风险条款"
    assert adverse_items["SVC-05-01"]["coverage_status"] == "风险条款"


def test_service_conditional_applicability_fixed_term_vs_indefinite_and_platform():
    fixed = review_contract_v2(
        "服务合同。甲方向乙方提供固定课程培训，课程共60课时，开课日期为2026年9月1日，结课日期为2026年12月1日。",
        "service",
        use_llm=False,
    )
    fixed_items = _items_by_id(fixed)
    assert fixed_items["SVC-06-04"]["coverage_status"] == "不适用"
    assert fixed_items["SVC-07-03"]["coverage_status"] == "不适用"

    indefinite = review_contract_v2(
        "服务合同。甲方向乙方提供长期持续服务，无固定期限。双方可随时解除，但应提前十日通知并按实际接受服务情况结算。",
        "service",
        use_llm=False,
    )
    assert _items_by_id(indefinite)["SVC-06-04"]["coverage_status"] != "不适用"

    platform = review_contract_v2(
        "服务合同。甲方通过线上平台提供服务，用户协议和平台规则如发生重大权益变更，应提前通知用户并取得明确同意。",
        "service",
        use_llm=False,
    )
    assert _items_by_id(platform)["SVC-07-03"]["coverage_status"] != "不适用"


def test_service_provider_client_interest_blocks_only_optional_consumer_benefits():
    def run(strength: str):
        recommendation = SimpleNamespace(
            recommendation_id=f"REC-{strength}",
            target_finding_ids=["RF-X"],
            proposed_change="服务方应允许消费者随时解除并全额退费。",
            suggested_text="服务方应允许消费者随时解除并全额退费。",
            status="ACTIVE",
            impact={},
            perspective="",
        )
        finding = SimpleNamespace(finding_id="RF-X", risk_group="optional_refund", source_review_ids=["SVC-X"])
        item = SimpleNamespace(
            item_id="SVC-X",
            node_id="optional_refund",
            coverage_elements=[],
            decision_trace={"legal_requirement_strength": strength, "effective_gap": {"authority_ids": []}},
        )
        accepted, impacts, gate = evaluate_recommendations([recommendation], [finding], [item], "SERVICE_PROVIDER")
        return recommendation, accepted, impacts, gate

    optional_rec, optional_accepted, optional_impacts, _ = run("OPTIONAL")
    assert optional_accepted == []
    assert optional_rec.status == "BLOCKED_NON_DEGRADATION"
    assert optional_impacts[0].gate_result == "BLOCKED"

    mandatory_rec, mandatory_accepted, mandatory_impacts, _ = run("MANDATORY")
    assert mandatory_accepted == [mandatory_rec]
    assert mandatory_impacts[0].gate_result == "PASS"

    risk_control_rec, risk_control_accepted, risk_control_impacts, _ = run("RISK_CONTROL")
    assert risk_control_accepted == [risk_control_rec]
    assert risk_control_impacts[0].gate_result == "PASS"


def test_existing_sale_and_lease_regressions_keep_their_transaction_structure():
    sale = review_contract_v2(
        "买卖合同。甲方向乙方购买普通硅酸盐水泥100吨，乙方交货后甲方验收并支付货款。",
        "sale",
        use_llm=False,
    )
    lease = review_contract_v2(
        "房屋租赁合同。出租人将住宅出租给承租人，月租金3000元，租赁期限一年。",
        "house_lease",
        use_llm=False,
    )

    assert sale["contract_context"]["contract_family"] == "SALE"
    assert sale["contract_context"]["transaction_structure"] == "SINGLE_TRANSACTION"
    assert lease["contract_context"]["contract_family"] in {"LEASE", "HOUSE_LEASE"}
    assert lease["contract_context"]["transaction_structure"] == "SINGLE_TRANSACTION"
