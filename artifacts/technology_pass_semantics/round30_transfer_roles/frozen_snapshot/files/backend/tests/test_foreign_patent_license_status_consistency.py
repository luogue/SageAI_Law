from pathlib import Path
from types import SimpleNamespace

import pytest

from layers.input_layer import InputLayer
from review_v2.engine import INSUFFICIENT_CONTEXT, _manual_review_instruction, review_contract_v2
from review_v2.user_profile import UserRiskProfile


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "test_data" / "39 中外专利技术许可合同.docx"


def _review(text: str) -> dict:
    return review_contract_v2(
        text,
        "technology",
        include_low_risk=True,
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/被许可方"),
    )


@pytest.fixture(scope="module")
def foreign_patent_review() -> dict:
    text = InputLayer()._extract_from_docx_content(FIXTURE.read_bytes())
    return _review(text)


@pytest.fixture(scope="module")
def cross_border_cooperation_review() -> dict:
    return _review(
        """
        中外专利技术许可合同
        甲方为中国被许可方，乙方为德国许可方。
        乙方将名称为精密控制系统、专利号为DE-2026-1001的专利技术以普通许可方式许可甲方实施。
        许可地域为中国境内，许可期限五年，甲方支付专利许可使用费人民币100万元。
        技术来源国为德国，技术输入国为中国，本合同属于跨境专利实施许可。
        技术进出口合规：如依法需要办理技术进口合同登记、变更登记或技术进口许可，
        双方应相互配合办理，并及时提供所需文件和资料。
        """
    )


def _item(output: dict, review_id: str) -> dict:
    return next(row for row in output["items"] if row["item_id"] == review_id)


def test_missing_support_elements_are_not_rendered_as_existing_arrangements(
    foreign_patent_review: dict,
):
    item = _item(foreign_patent_review, "TC-07-04")
    statuses = {row["element_id"]: row["status"] for row in item["coverage_elements"]}
    recommendation = item["suggested_clause_example"]

    assert statuses == {
        "on_demand_technical_service": "COVERED",
        "technical_service_execution_details": "MISSING",
        "patent_fee_and_validity_maintenance": "MISSING",
        "patent_status_change_notice": "MISSING",
    }
    assert item["decision_trace"]["final_covered_element_ids"] == [
        "on_demand_technical_service"
    ]
    # Final-element actions need not repeat covered facts as an introductory
    # template; they must address the actual remaining execution parameters.
    assert "具体范围、响应时间和交付标准" in recommendation
    assert "补充" in recommendation
    assert "专利费用缴纳及有效性维持义务" in recommendation
    assert "专利法律状态变化通知义务" in recommendation
    assert "现有按需技术服务、专利维持和状态通知安排" not in recommendation

    finding = next(
        row for row in foreign_patent_review["risk_findings"]
        if "TC-07-04" in row.get("source_review_ids", [])
    )
    assert finding["recommendation"] == recommendation


def test_contractual_representation_is_not_independent_documentary_proof(
    foreign_patent_review: dict,
):
    for review_id in ("TC-03-04", "TC-13-02"):
        item = _item(foreign_patent_review, review_id)
        elements = {row["element_id"]: row for row in item["coverage_elements"]}

        representation = elements["licensor_authority_contractual_representation"]
        independent_proof = elements["licensor_authority_and_upstream_authorization"]
        assert representation["status"] == "COVERED"
        assert representation["evidence_level"] == "CONTRACTUAL_REPRESENTATION"
        assert independent_proof["status"] == "MISSING"
        assert independent_proof["evidence_level"] == "CONTRACTUAL_REPRESENTATION_ONLY"
        assert "虽已作出有权许可的合同陈述或保证" in independent_proof["proposition"]
        assert "licensor_authority_and_upstream_authorization" in item["decision_trace"][
            "final_missing_element_ids"
        ]
        assert item["decision_trace"]["ip_proof_model"]["evidence_level_policy"][
            "representation_does_not_satisfy_independent_proof"
        ] is True
        audit = item["decision_trace"].get("specialized_search_audit", {})
        assert "上游授权书" in audit.get("missing_elements", [])
    assert "许可权限及必要的上游授权、再许可权限有文件依据" not in foreign_patent_review["result"]


def test_only_substantive_attachment_content_reaches_independent_proof_level():
    common = """
        专利实施许可合同
        甲方为被许可方，乙方为许可方。
        乙方将精密控制装置专利以普通许可方式许可甲方实施，专利号DE-1，许可期限五年，许可地域中国。
        许可方保证其有权许可。
    """
    title_only = _review(common + "\n附件一：专利登记簿副本")
    substantive = _review(
        common
        + """
        附件一：专利登记簿副本
        专利权人：乙方
        专利号：DE-1
        授权日：2026年1月1日
        法律状态：有效
        """
    )

    title_element = {
        row["element_id"]: row for row in _item(title_only, "TC-03-04")["coverage_elements"]
    }["licensor_authority_and_upstream_authorization"]
    proof_element = {
        row["element_id"]: row for row in _item(substantive, "TC-03-04")["coverage_elements"]
    }["licensor_authority_and_upstream_authorization"]
    # A title-only register reference does not establish who the patent owner
    # is. The authorization prerequisite remains unresolved, not absent.
    assert title_element["status"] == "CONDITION_UNRESOLVED"
    assert title_element["evidence_level"] == "CONTRACTUAL_REPRESENTATION_ONLY"
    assert proof_element["status"] == "COVERED"
    assert proof_element["evidence_level"] == "INDEPENDENT_DOCUMENTARY_PROOF"


def test_uncertain_parent_confidentiality_applicability_propagates_to_children(
    foreign_patent_review: dict,
):
    for review_id in ("TC-11-01", "TC-11-02", "TC-11-03", "TC-11-04"):
        item = _item(foreign_patent_review, review_id)
        assert item["coverage_status"] == INSUFFICIENT_CONTEXT
        assert item["coverage_presence"] == "UNCERTAIN"
        assert item["applicability"]["status"] == "CONDITIONALLY_APPLICABLE"
        assert item["risk_severity"] == "NONE"
        assert item["needs_manual_review"] is True

    for review_id in ("TC-11-03", "TC-11-04"):
        propagation = _item(foreign_patent_review, review_id)["decision_trace"][
            "confidentiality_family_applicability_propagation"
        ]
        assert propagation["child_status"] == "INHERITED_INSUFFICIENT_CONTEXT"
        assert propagation["independent_evidence_ids"] == []


def test_direct_child_trigger_can_override_uncertain_parent_applicability():
    output = _review(
        """
        中外专利技术许可合同
        德国许可方将名称为精密控制装置、专利号为DE-2026-1001的专利以普通许可方式许可中国被许可方实施。
        许可地域为中国境内，许可期限五年，被许可方支付专利许可使用费人民币100万元。
        许可方保证其有权授予本合同项下许可。
        对明确标记为保密的资料，合同终止后十日内应返还或销毁全部载体和复制件，并书面确认处置结果。
        发生泄密后，责任方应立即停止披露和使用，采取措施防止继续扩散，赔偿损失并通知受影响方。
        """
    )

    assert _item(output, "TC-11-01")["coverage_status"] == INSUFFICIENT_CONTEXT
    assert _item(output, "TC-11-02")["coverage_status"] == INSUFFICIENT_CONTEXT
    for review_id in ("TC-11-03", "TC-11-04"):
        child = _item(output, review_id)
        propagation = child["decision_trace"][
            "confidentiality_family_applicability_propagation"
        ]
        assert child["coverage_status"] != INSUFFICIENT_CONTEXT
        assert child["applicability"]["status"] == "APPLICABLE"
        assert child["applicability"]["applicable"] is True
        assert propagation["child_status"] == "INDEPENDENTLY_APPLICABLE"
        assert propagation["independent_evidence_ids"]


def test_import_formality_and_material_cooperation_are_independently_covered(
    cross_border_cooperation_review: dict,
):
    item = _item(cross_border_cooperation_review, "TC-13-04")
    statuses = {row["element_id"]: row["status"] for row in item["coverage_elements"]}

    assert statuses["technology_import_formality_cooperation"] == "COVERED"
    assert statuses["technology_import_material_cooperation"] == "COVERED"
    assert {
        "technology_import_formality_cooperation",
        "technology_import_material_cooperation",
    } <= set(item["decision_trace"]["final_covered_element_ids"])


def test_generic_cooperation_does_not_invent_a_specific_regulatory_owner(
    cross_border_cooperation_review: dict,
):
    item = _item(cross_border_cooperation_review, "TC-13-04")
    statuses = {row["element_id"]: row["status"] for row in item["coverage_elements"]}
    final_missing = set(item["decision_trace"]["final_missing_element_ids"])

    assert statuses["technology_import_license_responsible_party"] == "MISSING"
    assert statuses["technology_import_registration_responsible_party"] == "MISSING"
    assert {
        "technology_import_license_responsible_party",
        "technology_import_registration_responsible_party",
    } <= final_missing
    assert "technology_import_formality_cooperation" not in final_missing
    assert "technology_import_material_cooperation" not in final_missing
    assert "具体办理责任方" in item["suggested_clause_example"]
    assert "材料协作义务" not in item["suggested_clause_example"]
    assert "补充双方及时提供办理所需文件和资料" not in item["suggested_clause_example"]
    finding = next(
        row for row in cross_border_cooperation_review["risk_findings"]
        if row["risk_group"] == "technology_import_export_control"
    )
    assert {
        "technology_import_formality_cooperation",
        "technology_import_material_cooperation",
    }.isdisjoint({row["element_id"] for row in finding["final_missing_elements"]})
    assert "具体办理责任方" in finding["recommendation"]
    assert "材料协作义务" not in finding["recommendation"]
    assert "补充双方及时提供办理所需文件和资料" not in finding["recommendation"]
    assert "补充双方及时提供办理所需文件和资料" not in cross_border_cooperation_review["result"]


def test_absence_search_excludes_cooperation_supported_by_positive_evidence(
    cross_border_cooperation_review: dict,
):
    finding = next(
        row for row in cross_border_cooperation_review["risk_findings"]
        if row["risk_group"] == "technology_import_export_control"
    )
    search_rows = [
        row for row in (finding.get("evidence_bundle") or {}).get("items", [])
        if row.get("source_type") == "SEARCH_AUDIT"
    ]
    missing_targets = {
        str(value)
        for row in search_rows
        for value in row.get("missing_elements") or row.get("required_elements") or []
    }

    assert "技术进口许可由许可方或被许可方负责办理" in missing_targets
    assert "技术进口合同登记及变更登记由许可方或被许可方负责办理" in missing_targets
    assert "双方配合办理技术进口相关手续" not in missing_targets
    assert "双方及时提供办理所需文件和资料" not in missing_targets
    assert "办理材料协作义务" not in missing_targets


@pytest.mark.parametrize(
    "input_text",
    [
        "请确认技术秘密材料范围。",
        "人工复核：请确认技术秘密材料范围。",
        "人工复核：人工复核：请确认技术秘密材料范围。",
    ],
)
def test_manual_review_renderer_emits_exactly_one_prefix(input_text: str):
    item = SimpleNamespace(
        decision_trace={},
        evidence_clauses=[],
        title="保密事项",
        action_suggestion=input_text,
        quality_gate_failure_reason="",
    )

    rendered = _manual_review_instruction(item)
    assert rendered.startswith("人工复核：请确认")
    assert rendered.count("人工复核：") == 1
