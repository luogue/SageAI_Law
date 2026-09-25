from review_v2.engine import (
    ReviewItemResult,
    _apply_evidence_claim_ceiling,
    _operative_technology_clauses,
    _technical_secret_transfer_proof_results,
    review_contract_v2,
)
from review_v2.user_profile import UserRiskProfile


def _review(text: str) -> dict:
    return review_contract_v2(
        text,
        "technology",
        include_low_risk=True,
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/技术秘密受让方"),
    )


BASE_TRANSFER = """
非专利技术转让合同
甲方（受让方）与乙方（转让方）订立本合同。
乙方将控制算法、参数和调试方法等非专利技术及技术秘密完整转让给甲方，
转让价款支付完成后相关技术权利归甲方，乙方不再保留实施、许可或处分权。
技术转让价款为100万元。
"""


def _bare_item() -> ReviewItemResult:
    return ReviewItemResult(
        item_id="TC-02-01",
        node_id="technology.illegal_monopoly",
        title="技术竞争限制",
        risk_level="高",
        status="发现不利条款",
        risk_point_description="受让方不得购买竞争技术。",
        suggested_clause_example="删除该限制。",
        legal_basis_index="",
        legal_consequence_if_missing="限制正常竞争。",
        applicable_if="",
        matched_terms=[],
        coverage_status="风险条款",
        issue_type="风险条款",
        evidence_clauses=[{
            "evidence_id": "AUDIT-1",
            "evidence_role": "ABSENCE_EVIDENCE",
            "evidence_semantics": "ABSENCE_SEARCH",
            "text": "未找到受让方购买竞争技术受到限制",
        }],
        evidence_location="",
        reasoning_summary="受让方不得购买竞争技术。",
    )


def test_case_1_negative_search_audit_cannot_be_reversed_into_a_risk_fact():
    item = _bare_item()
    item.coverage_elements = [{
        "element_id": "lawful_competing_technology_access",
        "status": "MISSING",
        "proposition": "未发现购买竞争技术限制。",
    }]
    item.decision_trace["core_factual_claims"] = [{
        "claim_id": "lawful_competing_technology_access",
        "text": "受让方不得购买竞争技术",
        "evidence_ids": ["AUDIT-1"],
    }]
    item.decision_trace["claim_render"] = {"suppress_when_empty": True}

    [resolved] = _apply_evidence_claim_ceiling([item])

    assert resolved.coverage_status == "通过"
    assert "不得购买竞争技术" not in resolved.risk_point_description
    assert resolved.decision_trace["evidence_claim_ceiling"]["status"] == "SUPPRESSED"


def test_case_2_improvement_transfer_does_not_imply_research_purchase_or_alternative_bans():
    result = _review(BASE_TRANSFER + "\n甲方独立形成的改进成果及知识产权无偿归乙方所有。")
    item = next(row for row in result["items"] if row["item_id"] == "TC-02-01")
    rendered = " ".join((
        item["risk_point_description"],
        item["reasoning_summary"],
        item["legal_consequence_if_missing"],
        str(item["decision_trace"].get("user_visible_risk_cluster") or ""),
    ))

    assert item["coverage_status"] == "风险条款"
    assert "改进成果" in item["risk_point_description"]
    assert "不得购买竞争技术" not in rendered
    assert "禁止购买竞争技术" not in rendered
    assert "形成替代方案" not in rendered
    assert "禁止独立研发" not in rendered


def test_case_3_rule_template_cannot_create_secret_loss_payment_fact_without_clause():
    result = _review(BASE_TRANSFER)
    item = next(row for row in result["items"] if row["item_id"] == "TC-12-03")
    rendered = " ".join((
        item["risk_point_description"],
        item["reasoning_summary"],
        item["legal_consequence_if_missing"],
    ))

    assert item["coverage_status"] != "风险条款"
    assert "公开后仍须继续支付" not in rendered
    assert "已付款不退" not in rendered
    assert "不得解除" not in rendered


def test_case_4_pure_technical_secret_transfer_makes_tc_01_04_not_applicable():
    result = _review(BASE_TRANSFER)
    item = next(row for row in result["items"] if row["item_id"] == "TC-01-04")

    assert item["coverage_status"] == "不适用"
    assert "未出现加工、制造、设备安装、施工或建设工程" in item["applicability"]["reason"]


def test_case_5_technical_service_with_equipment_install_activates_tc_01_04():
    text = """
软件技术服务合同
甲方（服务接受方）委托乙方（服务提供方）提供系统优化技术服务。
乙方负责服务器设备安装、现场施工、系统调试和竣工验收，不交付新软件所有权。
服务费为50万元。
"""
    result = review_contract_v2(text, "technology", include_low_risk=True, use_llm=False)
    item = next(row for row in result["items"] if row["item_id"] == "TC-01-04")

    assert item["coverage_status"] != "不适用"
    assert item["applicability"]["applicable"] is True


def test_case_6_each_proof_element_requires_its_own_direct_evidence():
    text = BASE_TRANSFER + """
附件一《技术秘密清单》列明技术边界、资料范围和交付内容。
附件二为研发记录和形成过程记录。
附件三为乙方合法持有该技术秘密的权利归属证明。
"""
    elements, _, _ = _technical_secret_transfer_proof_results(
        _operative_technology_clauses(text)
    )
    by_id = {row["element_id"]: row for row in elements}

    assert by_id["technical_secret_identity_and_delivery_scope"]["status"] == "COVERED"
    assert by_id["technical_source"]["status"] == "COVERED"
    assert by_id["lawful_possession_basis"]["status"] == "COVERED"
    assert by_id["historical_disclosure_objects"]["status"] == "MISSING"
    assert by_id["historical_disclosure_scope"]["status"] == "MISSING"
    assert by_id["third_party_confidentiality_obligations"]["status"] == "MISSING"
    assert by_id["joint_holder_disclosure"]["status"] == "MISSING"
    assert by_id["current_secret_status"]["status"] == "MISSING"
    assert by_id["existing_confidentiality_measures"]["status"] == "MISSING"


def test_generic_confidentiality_does_not_prove_historical_measures_but_direct_controls_do():
    generic = BASE_TRANSFER + "\n双方对技术秘密承担保密义务，未经同意不得披露。"
    direct = generic + "\n乙方已经建立访问权限控制，并与研发人员签订保密协议，形成技术秘密清单。"

    generic_elements, _, _ = _technical_secret_transfer_proof_results(
        _operative_technology_clauses(generic)
    )
    direct_elements, _, _ = _technical_secret_transfer_proof_results(
        _operative_technology_clauses(direct)
    )
    generic_by_id = {row["element_id"]: row for row in generic_elements}
    direct_by_id = {row["element_id"]: row for row in direct_elements}

    assert generic_by_id["existing_confidentiality_measures"]["status"] == "MISSING"
    assert direct_by_id["existing_confidentiality_measures"]["status"] == "COVERED"
