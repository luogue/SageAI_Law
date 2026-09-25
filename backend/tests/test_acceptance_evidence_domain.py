"""Acceptance proof must state the right action for the right transaction object."""
from pathlib import Path
from copy import deepcopy

import pytest

from layers.input_layer import InputLayer
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import _operative_technology_clauses
from review_v2.acceptance_evidence import (
    PRODUCT, SERVICE, MATERIAL, REQUIREMENTS,
    extract_acceptance_facts, acceptance_requirement_elements, acceptance_source_entailment,
)


def elements(text, domain):
    return {e["element_id"]: e for e in acceptance_requirement_elements(parse_contract_clauses(text), domain=domain)}


@pytest.mark.parametrize("text", [
    "2．涉密人员：直接参与项目研发、测试、管理及验收的人员。",
    "3．负责项目日常沟通、测试和验收协调。",
    "甲方提供的数据仅限本项目研发、测试和验收使用，乙方不得用于其他项目。",
    "5．《验收测试指标表》。",
])
def test_incidental_acceptance_words_and_forged_tags_never_prove_a_requirement(text):
    source = {"clause_id": "C1", "quote": text, "source_domain": SERVICE,
              "supporting_element_ids": list(REQUIREMENTS), "entailment_status": "SUPPORTS"}
    assert extract_acceptance_facts(parse_contract_clauses(text)) == []
    for key in REQUIREMENTS:
        assert acceptance_source_entailment(source, key, expected_domain=SERVICE)["status"] == "RELATED_NOT_SUPPORTING"


def test_product_service_and_material_acceptance_remain_distinct():
    text = ("第一条 产品验收\n产品抓取成功率不低于96%。甲方在收到产品后12个工作日内组织验收。\n"
            "第二条 技术服务验收\n技术服务响应时间不超过2小时。甲方在服务完成后8个工作日内组织验收。\n"
            "第三条 资料验收\n技术资料应齐全、完整且可读取。甲方在收到资料后5个工作日内组织验收。")
    clauses = parse_contract_clauses(text)
    facts = extract_acceptance_facts(clauses)
    assert {fact["source_domain"] for fact in facts} == {PRODUCT, SERVICE, MATERIAL}
    for domain, keyword in ((PRODUCT, "96%"), (SERVICE, "2小时"), (MATERIAL, "可读取")):
        rows = elements(text, domain)
        standard = rows["objective_acceptance_standard"]
        assert standard["status"] == "COVERED", rows
        assert all(keyword in f["quote"] for f in standard["supporting_evidence"])
        assert rows["acceptance_process"]["status"] == "COVERED"
        assert rows["acceptance_deadline"]["status"] == "COVERED"
        assert rows["rectification_mechanism"]["status"] == "MISSING"
        for fact in standard["supporting_evidence"]:
            assert acceptance_source_entailment(fact, standard["element_id"], expected_domain=domain)["status"] == "SUPPORTS"
            for other in {PRODUCT, SERVICE, MATERIAL} - {domain}:
                assert acceptance_source_entailment(fact, standard["element_id"], expected_domain=other)["status"] == "RELATED_NOT_SUPPORTING"


def test_support_duration_content_and_fee_are_not_service_acceptance():
    text = "第一条 技术指导和培训\n乙方提供6个月技术支持，内容包括部署和参数配置，采用远程支持方式，费用计入合同总价。"
    assert extract_acceptance_facts(parse_contract_clauses(text)) == []
    assert all(row["status"] == "MISSING" for row in elements(text, SERVICE).values())


def test_acceptance_number_is_not_a_remedy_number_and_personnel_are_not_an_acceptance_actor():
    rows = elements("第一条 技术服务验收\n验收人员包括研发和测试人员。甲方收到服务成果后10个工作日内组织验收。", SERVICE)
    assert rows["acceptance_process"]["status"] == "COVERED"
    assert rows["acceptance_deadline"]["status"] == "COVERED"
    assert all(rows[key]["status"] == "MISSING" for key in ("rectification_deadline", "reinspection_deadline", "objective_acceptance_standard"))
    assert all("验收人员" not in f["quote"] for row in rows.values() for f in row["supporting_evidence"])


def test_deferred_standard_and_vague_deadline_do_not_erase_actual_rectification_duty():
    rows = elements("第一条 技术服务验收\n服务验收标准由双方另行确认。验收不合格时乙方应在合理期限内完成整改。整改后重新验收。", SERVICE)
    assert rows["objective_acceptance_standard"]["status"] == "PARTIALLY_COVERED"
    assert rows["rectification_mechanism"]["status"] == "COVERED"
    assert rows["rectification_deadline"]["status"] == "PARTIALLY_COVERED"
    assert rows["reinspection_procedure"]["status"] == "COVERED"


def test_technical_target_is_not_an_acceptance_standard_without_a_binding():
    rows = elements("第一条 研发目标\n产品抓取成功率不低于95%。\n第二条 技术服务\n乙方提供部署支持。", PRODUCT)
    assert rows["objective_acceptance_standard"]["status"] == "MISSING"


def test_expressly_negated_acceptance_duties_cannot_support_positive_requirements():
    rows = elements("第一条 技术服务验收\n不要求服务响应时间不超过2小时。甲方无须在10日内组织验收。乙方无须在5日内整改，整改后不再复验。", SERVICE)
    assert all(rows[key]["status"] == "MISSING" for key in (
        "objective_acceptance_standard", "acceptance_process", "acceptance_deadline",
        "rectification_mechanism", "rectification_deadline", "reinspection_procedure",
    ))


def test_plain_service_acceptance_and_response_words_are_explicit_service_objects():
    rows = elements("第一条 服务验收\n服务响应时间不超过2小时。甲方在服务完成后8个工作日内组织验收。", SERVICE)
    assert all(rows[key]["status"] == "COVERED" for key in ("objective_acceptance_standard", "acceptance_process", "acceptance_deadline"))
    response_only = elements("第一条 技术服务\n服务响应时间不超过2小时。", SERVICE)
    assert response_only["objective_acceptance_standard"]["status"] == "COVERED"
    assert response_only["acceptance_process"]["status"] == "MISSING"


@pytest.mark.parametrize("separator", ["，", "。\n", "。\n1．"])
def test_named_service_software_deliverable_keeps_its_service_quality_domain(separator):
    rows = elements("第一条 技术服务验收\n技术服务成果为软件系统" + separator + "系统准确率不低于99%。", SERVICE)
    standard = rows["objective_acceptance_standard"]
    assert standard["status"] == "COVERED"
    for fact in standard["supporting_evidence"]:
        assert acceptance_source_entailment(fact, standard["element_id"], expected_domain=SERVICE)["status"] == "SUPPORTS"
    mixed = elements("第一条 技术服务及产品\n产品准确率不低于99%，技术服务提供远程支持。", SERVICE)
    assert mixed["objective_acceptance_standard"]["status"] == "MISSING"


SHARED_TARGET = "第一条 产品验收\n产品抓取成功率不低于97%。甲方在收到成果后15个工作日内组织验收。"


@pytest.mark.parametrize("reference", [
    "技术服务质量和验收标准、验收程序及期限均适用本合同第一条。",
    "服务验收标准、程序及期限按照第1条执行。",
    "第一条的验收标准、程序及期限适用于技术服务验收。",
])
def test_explicit_shared_acceptance_reference_binds_the_target_fact_and_context(reference):
    text = SHARED_TARGET + "\n第二条 技术服务验收\n" + reference
    clauses = parse_contract_clauses(text)
    by_id = {c.clause_id: c for c in clauses}
    rows = elements(text, SERVICE)
    for key in ("objective_acceptance_standard", "acceptance_process", "acceptance_deadline"):
        assert rows[key]["status"] == "COVERED", rows
        for fact in rows[key]["supporting_evidence"]:
            assert "第一条" in str(fact["source_heading_path"])
            assert fact["quote"] in by_id[fact["clause_id"]].text
            contexts = fact["domain_context_evidence"]
            assert any(c["evidence_role"] == "ACCEPTANCE_SCOPE_REFERENCE" and reference == c["quote"] for c in contexts)
            assert all(c["quote"] in by_id[c["clause_id"]].text for c in contexts)
            assert acceptance_source_entailment(fact, key, expected_domain=SERVICE)["status"] == "SUPPORTS"
            removed = {**fact, "domain_context_evidence": []}
            assert acceptance_source_entailment(removed, key, expected_domain=SERVICE)["status"] == "RELATED_NOT_SUPPORTING"
    assert rows["rectification_mechanism"]["status"] == "MISSING"


def test_adopting_only_standards_cannot_copy_procedure_or_deadline():
    rows = elements(SHARED_TARGET + "\n第二条 技术服务验收\n服务验收标准采用第一条。", SERVICE)
    assert rows["objective_acceptance_standard"]["status"] == "COVERED"
    assert rows["acceptance_process"]["status"] == "MISSING"
    assert rows["acceptance_deadline"]["status"] == "MISSING"


@pytest.mark.parametrize("reference", [
    "技术服务提供远程支持，第一条约定产品验收标准。",
    "技术服务验收标准不适用第一条。",
    "技术服务验收标准不依照第一条。",
    "技术服务验收标准另行协商是否适用第一条。",
    "技术服务验收标准适用第九条。",
])
def test_nearby_service_words_negation_and_missing_targets_do_not_create_shared_proof(reference):
    rows = elements(SHARED_TARGET + "\n第二条 技术服务\n" + reference, SERVICE)
    assert rows["objective_acceptance_standard"]["status"] != "COVERED"
    assert rows["acceptance_deadline"]["status"] == "MISSING"


def test_reference_chain_is_recomputed_and_a_broken_hop_loses_support():
    text = (SHARED_TARGET + "\n第二条 技术服务验收\n服务验收标准适用第一条。\n"
            "第三条 培训验收\n培训成果验收标准适用第二条。")
    facts = extract_acceptance_facts(parse_contract_clauses(text))
    fact = next(f for f in facts if f["effective_acceptance_article"] == "3" and f["fact_key"] == "objective_acceptance_standard")
    assert len(fact["domain_context_evidence"]) == 2
    assert acceptance_source_entailment(fact, fact["fact_key"], expected_domain=SERVICE)["status"] == "SUPPORTS"
    corrupt = deepcopy(fact)
    corrupt["domain_context_evidence"] = corrupt["domain_context_evidence"][1:]
    assert acceptance_source_entailment(corrupt, fact["fact_key"], expected_domain=SERVICE)["status"] == "RELATED_NOT_SUPPORTING"


def test_service_reference_to_material_standard_requires_the_actual_reference():
    text = "第一条 资料验收\n技术资料应齐全、完整且可读取。\n第二条 技术服务验收\n服务验收标准适用第一条。"
    rows = elements(text, SERVICE)
    standard = rows["objective_acceptance_standard"]
    assert standard["status"] == "COVERED"
    fact = standard["supporting_evidence"][0]
    assert acceptance_source_entailment(fact, standard["element_id"], expected_domain=SERVICE)["status"] == "SUPPORTS"
    assert acceptance_source_entailment({**fact, "domain_context_evidence": []}, standard["element_id"], expected_domain=SERVICE)["status"] == "RELATED_NOT_SUPPORTING"


def test_current47_production_parsed_sources_identify_product_metrics_and_no_service_acceptance():
    fixture = Path(__file__).resolve().parents[2] / "test_data" / "47 技术开发（委托）合同.docx"
    text = InputLayer()._extract_from_docx_content(fixture.read_bytes())
    clauses = _operative_technology_clauses(text)
    facts = extract_acceptance_facts(clauses)
    standards = [fact for fact in facts if fact["fact_key"] == "objective_acceptance_standard"]
    assert len(standards) == 4
    assert all(fact["source_domain"] == PRODUCT for fact in standards)
    assert all("第十三条" in str(fact["source_heading_path"]) for fact in standards)
    assert all("涉密人员" not in fact["quote"] and "验收协调" not in fact["quote"] for fact in facts)
    product = {row["element_id"]: row for row in acceptance_requirement_elements(clauses, domain=PRODUCT)}
    assert product["acceptance_deadline"]["status"] == "COVERED"
    assert "15个工作日" in product["acceptance_deadline"]["supporting_evidence"][0]["quote"]
    for row in acceptance_requirement_elements(clauses, domain=SERVICE):
        assert row["status"] == "MISSING"
        assert row["supporting_evidence"] == []
    for fact in facts:
        checked = acceptance_source_entailment(fact, fact["fact_key"], expected_domain=fact["source_domain"])
        assert checked["status"] == "SUPPORTS", checked


def test_real_upload_report_source_is_checked_without_trusting_its_legacy_pass_tag():
    # Exercise the actual file/upload/report pipeline as well as parsed helpers.
    # While a legacy generic element still exists, the domain guard must reject
    # its incidental source. Once the caller integrates atomic service review,
    # every positive acceptance atom must have independently valid service proof.
    from tests.test_entrusted_development_production_closure import report
    response = report.__wrapped__()
    assert response["contract_context"]["canonical_classification"]["contract_subtype"] == "ENTRUSTED_DEVELOPMENT"
    review = next(row for row in response["items"] if row["item_id"] == "TC-09-02")
    assert review["applicability"]["status"] == "APPLICABLE"
    for element in review["coverage_elements"]:
        if element["status"] != "COVERED":
            continue
        for source in element["supporting_evidence"]:
            checked = acceptance_source_entailment(source, element["element_id"], expected_domain=SERVICE)
            if element["element_id"] == "core_contract_arrangement":
                assert checked["status"] == "RELATED_NOT_SUPPORTING"
            else:
                assert checked["status"] == "SUPPORTS", checked


def test_current47_production_review_keeps_explicitly_shared_acceptance_and_reference_provenance():
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile
    fixture = Path(__file__).resolve().parents[2] / "test_data" / "47 技术开发（委托）合同.docx"
    text = InputLayer()._extract_from_docx_content(fixture.read_bytes())
    reference = "技术服务质量和验收标准、验收程序及期限均适用本合同第十三条。"
    text = text.replace("第二十条 违约责任", reference + "\n第二十条 违约责任")
    response = review_contract_v2(text, "technology", use_llm=False, profile=UserRiskProfile(user_identity="甲方/委托方"))
    assert response["contract_context"]["canonical_classification"]["contract_subtype"] == "ENTRUSTED_DEVELOPMENT"
    review = next(row for row in response["items"] if row["item_id"] == "TC-09-02")
    rows = {row["element_id"]: row for row in review["coverage_elements"]}
    covered = {"objective_acceptance_standard", "acceptance_process", "acceptance_deadline"}
    assert {key for key, row in rows.items() if row["status"] == "COVERED"} == covered
    assert not covered.intersection(review["decision_trace"]["final_missing_element_ids"])
    for key in covered:
        for source in rows[key]["supporting_evidence"]:
            assert "第十三条" in str(source["source_heading_path"])
            assert any(context["quote"] == reference for context in source["domain_context_evidence"])
            assert acceptance_source_entailment(source, key, expected_domain=SERVICE)["status"] == "SUPPORTS"
    assert response["release_quality_gate"]["status"] == "REPORT_READY", response["release_quality_gate"]
