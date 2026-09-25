from pathlib import Path

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.domain_selection import resolve_domain_selection
from review_v2.technology_service_analysis import classify_technology_transaction
from review_v2.consulting_element_facts import elements as consulting_elements


FIXTURES = Path(__file__).parent / "fixtures"
ROUND43 = (FIXTURES / "round43_consulting.txt").read_text(encoding="utf8")


@pytest.mark.parametrize("fixture", ["round41_consulting.txt", "round42_consulting.txt", "round43_consulting.txt"])
def test_consulting_rounds_keep_high_confidence_consulting_route(fixture):
    text = (FIXTURES / fixture).read_text(encoding="utf8")
    classification = classify_technology_transaction(text)
    assert classification["primary_subtype"] == "TECHNICAL_CONSULTING"
    resolution, _, routed = resolve_domain_selection("technology", text, parse_contract_clauses(text), classification)
    assert routed == "technology"
    assert resolution.resolution == "AGREE"
    assert resolution.document_domain["primary_subtype"] == "TECHNICAL_CONSULTING"


def test_consulting_objects_and_express_exclusions_do_not_become_competing_transactions():
    classification = classify_technology_transaction(ROUND43)
    assert classification["confidence"] == "high"
    assert classification["candidate_scores"]["TECHNICAL_CONSULTING"] > classification["candidate_scores"]["TECHNICAL_SERVICE"]
    assert "boundary:no_direct_implementation" in classification["classification_evidence"]
    resolution, _, _ = resolve_domain_selection("technology", ROUND43, parse_contract_clauses(ROUND43), classification)
    scores = resolution.classification_context["candidate_scores"]
    assert scores["TECHNOLOGY"] > scores["SERVICE"]
    assert scores["TECHNOLOGY"] > scores["SALE"]


def test_real_service_and_entrusted_development_remain_separate():
    service = (FIXTURES / "round40_service.txt").read_text(encoding="utf8")
    development = (FIXTURES / "round35_entrusted_development.txt").read_text(encoding="utf8")
    assert classify_technology_transaction(service)["primary_subtype"] == "TECHNICAL_SERVICE"
    assert classify_technology_transaction(development)["primary_subtype"] == "ENTRUSTED_DEVELOPMENT"


def test_real_independent_implementation_still_activates_service_module():
    text = """技术咨询协议
甲方委托乙方分析设备能耗并提交咨询报告，咨询费十万元。
除咨询工作外，乙方还应独立完成能源管理系统部署、参数调试和现场技术支持。
"""
    classification = classify_technology_transaction(text)
    assert classification["primary_subtype"] in {"TECHNICAL_CONSULTING", "TECHNICAL_SERVICE"}
    assert (classification["primary_subtype"] == "TECHNICAL_SERVICE"
            or "TECHNICAL_SERVICE" in classification["secondary_modules"])


def test_incompatible_user_selection_is_detected_and_document_evidence_controls():
    classification = classify_technology_transaction(ROUND43)
    resolution, _, routed = resolve_domain_selection("service", ROUND43, parse_contract_clauses(ROUND43), classification)
    assert resolution.compatibility == "CONFLICT"
    assert resolution.classification_context["classification_conflict"]["detected"] is True
    assert resolution.resolution == "DOCUMENT_OVERRIDE"
    assert routed == "technology"


def test_round43_consulting_payment_atoms_keep_exact_owned_spans():
    atoms = {
        row["element_id"]: row
        for row in consulting_elements("consulting_payment", parse_contract_clauses(ROUND43))
    }
    total = atoms["consulting_fee_total"]
    milestones = atoms["payment_milestones"]
    assert total["status"] == "COVERED"
    assert any("顾问服务报酬总额" in row["quote"] and "560,000" in row["quote"]
               for row in total["supporting_evidence"])
    quotes = [row["quote"] for row in milestones["supporting_evidence"]]
    assert any("生效之日起5个工作日内支付168,000元" in quote for quote in quotes)
    assert any("成果初稿后支付224,000元" in quote for quote in quotes)
    assert any("最终报告并完成成果汇报后支付168,000元" in quote for quote in quotes)
    assert any("付款条件满足后的10个工作日内支付" in quote for quote in quotes)
    assert all("顾问服务报酬总额" not in quote for quote in quotes)


@pytest.mark.parametrize("identity", ["甲方/委托方", "乙方/咨询方"])
def test_round43_tc0805_pass_consumes_owned_direct_evidence(identity):
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile

    report = review_contract_v2(
        ROUND43, "technology", use_llm=False,
        profile=UserRiskProfile(user_identity=identity),
    )
    item = next(row for row in report["items"] if row["item_id"] == "TC-08-05")
    atoms = {row["element_id"]: row for row in item["coverage_elements"]}
    assert item["coverage_status"] == "通过"
    for key in ("consulting_fee_total", "payment_milestones"):
        assert atoms[key]["status"] == "COVERED"
        assert atoms[key]["supporting_evidence_ids"]
        sources = [row for row in item["evidence_clauses"]
                   if key in row.get("supporting_element_ids", [])]
        assert sources and all(row["support_type"] == "DIRECT" for row in sources)
    audit = item["decision_trace"]["pass_evidence_audit"]
    assert audit["status"] == "PASS"
    assert audit["deterministic_proposition_binding"] is True
    assert not audit["missing_element_ids"]
