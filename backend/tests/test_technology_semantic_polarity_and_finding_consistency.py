from review_v2.engine import ReviewItemResult, _build_narrative_state, _build_risk_findings, review_contract_v2
from review_v2.technology_patent_transfer_analysis import analyze_dispute_resolution_options
from review_v2.user_profile import UserRiskProfile


BASE = """专利权转让合同
甲方（受让方）受让乙方（让与方）所有的智能控制方法发明专利权，专利号CN202010000001。
乙方将专利权完整转让给甲方，价款100万元，双方办理专利权转让登记。
"""


def _review(extra: str) -> dict:
    return review_contract_v2(
        BASE + extra,
        "technology",
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/专利权受让方"),
    )


def test_inactive_arbitration_option_does_not_create_dual_selection():
    state = analyze_dispute_resolution_options(
        "1. 提交仲裁委员会仲裁：不适用。\n2. 向有管辖权的人民法院提起诉讼。"
    )
    assert state["arbitration_selected"] is False
    assert state["litigation_selected"] is True


def test_genuine_dual_dispute_selection_remains_detectable():
    state = analyze_dispute_resolution_options("争议提交仲裁委员会仲裁，也可向人民法院提起诉讼。")
    assert state["arbitration_selected"] is True
    assert state["litigation_selected"] is True


def test_prohibition_of_illegal_restriction_is_protective_not_risk():
    output = _review("任何一方不得非法限制另一方进行新的研究开发或者从其他渠道获得技术。")
    item = next(row for row in output["items"] if row["item_id"] == "TC-02-01")
    assert item["coverage_status"] == "通过"
    assert not any(row["risk_group"] == "illegal_monopoly_technology" for row in output["risk_findings"])


def test_affirmative_research_and_external_technology_restriction_remains_risk():
    output = _review("受让方不得自行研究开发与本专利相关的任何改进技术，也不得从第三方获得类似技术。")
    item = next(row for row in output["items"] if row["item_id"] == "TC-02-01")
    assert item["coverage_status"] == "风险条款"
    assert any(row["risk_group"] == "illegal_monopoly_technology" for row in output["risk_findings"])


def test_pure_patent_transfer_excludes_software_proof_requirements():
    output = _review("")
    item = next(row for row in output["items"] if row["item_id"] == "TC-03-04")
    element_ids = {row["element_id"] for row in item["coverage_elements"]}
    assert not element_ids & {"software_copyright", "open_source_component", "software_background_ip"}
    finding_text = " ".join(row["issue"] + row["recommendation"] for row in output["risk_findings"])
    assert "软件著作权" not in finding_text
    assert "开源组件" not in finding_text


def test_patent_software_mixed_transaction_preserves_software_trigger():
    output = _review("本合同同时转让软件著作权及源代码，软件包含第三方开源组件。")
    classification = output["deterministic_analysis"]["technology_classification"]
    assert classification["involves_software_or_data"] is True
    item = next(row for row in output["items"] if row["item_id"] == "TC-03-04")
    assert item["decision_trace"].get("scenario_pollution_removed") is None


def test_shared_third_party_fact_aggregates_top_finding_but_keeps_review_details():
    output = _review(
        "受让方按约实施专利侵犯第三方权利的，全部责任由受让方承担。"
        "第三方提出权利主张时，让与方仅提供必要协助，其他责任另行协商。"
    )
    finding = next(row for row in output["risk_findings"] if row["risk_group"] == "transferee_infringement_liability_shift")
    assert {"TC-12-01", "TC-12-02"} <= set(finding["source_review_ids"])
    assert sum(row["risk_group"] == "transferee_infringement_liability_shift" for row in output["risk_findings"]) == 1
    children = [row for row in output["items"] if row["item_id"] in finding["source_review_ids"]]
    assert len({row["risk_point_description"] for row in children}) == len(children)
    assert len({row["legal_consequence_if_missing"] for row in children}) == len(children)
    assert all(row["decision_trace"]["field_provenance"]["risk_description_source"] == "rule" for row in children)


def test_parent_finding_does_not_mutate_child_fields():
    def child(item_id: str, description: str, consequence: str) -> ReviewItemResult:
        return ReviewItemResult(
            item_id=item_id, node_id=item_id, title=item_id, risk_level="中", status="缺失",
            risk_point_description=description, suggested_clause_example=f"建议-{description}",
            legal_basis_index="", legal_consequence_if_missing=consequence, applicable_if="适用于测试",
            matched_terms=[], coverage_status="缺失", issue_type="MISSING", evidence_clauses=[],
            evidence_location="", reasoning_summary=description, risk_group="shared-parent",
            risk_severity="MEDIUM", residual_risk=consequence,
            applicability={"status": "APPLICABLE", "applicable": True},
            coverage_elements=[{"element_id": f"gap-{item_id}", "status": "MISSING", "proposition": f"未明确{description}"}],
            decision_trace={"effective_gap": {"effective_gap_valid": True, "remaining_gap": consequence}},
        )

    first = child("TC-X-01", "A", "后果A")
    second = child("TC-X-02", "B", "后果B")
    findings = _build_risk_findings([first, second])
    assert len(findings) == 1
    assert first.risk_point_description == "A"
    assert second.risk_point_description == "B"
    assert findings[0].source_review_ids == ["TC-X-01", "TC-X-02"]


def test_generic_fallback_without_concrete_gap_cannot_create_finding():
    item = ReviewItemResult(
        item_id="TC-X-03", node_id="TC-X-03", title="模板风险", risk_level="中", status="部分覆盖",
        risk_point_description="适用范围、履行标准和责任安排不完整", suggested_clause_example="建议补充明确",
        legal_basis_index="", legal_consequence_if_missing="责任安排不清", applicable_if="适用于测试",
        matched_terms=[], coverage_status="部分覆盖", issue_type="PARTIAL", evidence_clauses=[],
        evidence_location="", reasoning_summary="履行标准不明确", risk_group="generic-gap",
        risk_severity="MEDIUM", residual_risk="责任安排不清",
        applicability={"status": "APPLICABLE", "applicable": True},
        coverage_elements=[{"element_id": "core_contract_arrangement", "status": "MISSING", "proposition": "适用范围、履行标准和责任安排"}],
        decision_trace={"effective_gap": {"effective_gap_valid": True, "remaining_gap": "责任安排不清"}},
    )
    assert _build_risk_findings([item]) == []
    assert item.decision_trace["concrete_missing_element_gate"]["status"] == "SUPPRESSED"


def test_complete_material_list_in_body_passes_without_separate_attachment():
    output = _review("乙方应以电子文件方式向甲方交付专利证书、说明书、权利要求书及实施技术资料清单，甲方签收确认。")
    item = next(row for row in output["items"] if row["item_id"] == "TC-13-01")
    assert item["coverage_status"] == "通过"
    assert not any("TC-13-01" in row["source_review_ids"] for row in output["risk_findings"])


def test_vague_material_obligation_reports_specific_missing_elements():
    output = _review("乙方应提供相关技术资料。")
    item = next(row for row in output["items"] if row["item_id"] == "TC-13-01")
    assert item["coverage_status"] == "部分覆盖"
    assert "未明确技术资料具体清单及文件类型" in item["risk_point_description"]
    assert "适用范围、履行标准和责任安排" not in item["risk_point_description"]


def test_missing_partial_and_pass_narratives_preserve_status_polarity():
    missing = ReviewItemResult(
        item_id="TC-X-04", node_id="remedy_coordination", title="侵权责任与一般救济衔接",
        risk_level="中", status="缺失", risk_point_description="", suggested_clause_example="",
        legal_basis_index="", legal_consequence_if_missing="", applicable_if="适用", matched_terms=[],
        coverage_status="缺失", issue_type="MISSING", evidence_clauses=[], evidence_location="", reasoning_summary="",
        coverage_elements=[{"element_id": "coordination", "status": "MISSING", "proposition": "侵权专项责任与一般损失赔偿之间的适用关系明确。"}],
    )
    missing_state = _build_narrative_state(missing)
    assert all(marker not in missing_state["judgment"] + missing_state["issue"] for marker in ("已明确约定", "已覆盖", "无需修改"))

    partial = missing
    partial.coverage_status = "部分覆盖"
    partial.coverage_elements = [
        {"element_id": "existing", "status": "COVERED", "proposition": "侵权专项责任已约定。"},
        {"element_id": "coordination", "status": "MISSING", "proposition": "同一损失避免重复赔偿的规则明确。"},
    ]
    partial_state = _build_narrative_state(partial)
    assert "已覆盖" in partial_state["judgment"] and "尚未覆盖" in partial_state["judgment"]

    partial.coverage_status = "通过"
    partial.coverage_elements = [{"element_id": "existing", "status": "COVERED", "proposition": "侵权专项责任与一般救济衔接已明确约定。"}]
    pass_state = _build_narrative_state(partial)
    assert all(marker not in pass_state["judgment"] for marker in ("尚未覆盖", "缺失", "未明确"))


def test_rights_provenance_consequence_stays_in_ownership_and_registration_family():
    output = _review("")
    item = next(row for row in output["items"] if row["item_id"] == "TC-03-04")
    consequence = item["narrative_state"]["consequence"]
    assert any(term in consequence for term in ("权属", "处分权", "登记", "权利负担"))
    assert all(term not in consequence for term in ("律师选择", "抗辩控制", "停止侵权", "替代技术"))


def test_third_party_claim_rule_keeps_infringement_response_consequence():
    output = _review("第三方提出权利主张时，让与方仅提供必要协助，其他责任另行协商。")
    item = next(row for row in output["items"] if row["item_id"] == "TC-12-02")
    consequence = item["narrative_state"]["consequence"]
    assert any(term in consequence for term in ("第三方权利主张", "抗辩", "律师", "和解", "费用"))
