"""Atomic evidence recall, scope isolation and partial principle regressions."""
from pathlib import Path

import pytest

from layers.input_layer import InputLayer
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import extract_semantic_field_value, _operative_technology_clauses, _partial_element_narrative_label
from review_v2.obligation_detail_elements import (
    ancillary_service_detail_elements,
    confidentiality_detail_elements,
    improvement_license_detail_elements,
)


def states(text, extractor):
    clauses = parse_contract_clauses(text)
    rows = extractor(clauses) if extractor is improvement_license_detail_elements else extractor(clauses, extract_field=extract_semantic_field_value)
    by_id = {clause.clause_id: clause for clause in clauses}
    for row in rows:
        for fact in row["supporting_evidence"]:
            assert fact["quote"] in by_id[fact["clause_id"]].text
    return {row["element_id"]: row for row in rows}


@pytest.mark.parametrize("duration", ["5年", "七年", "18个月"])
def test_filled_confidentiality_fields_cover_categories_personnel_and_actual_duration(duration):
    text = "第一条 保密义务\n"
    for party in ("甲方", "乙方"):
        text += f"{party}：\n1．保密内容：模型参数、源代码及非公开研究记录。\n2．涉密人员：参与测试及验收的人员。\n3．保密期限：自首次接触保密信息之日起至合同终止后{duration}。\n"
    rows = states(text, confidentiality_detail_elements)
    assert {key for key, row in rows.items() if row["status"] == "MISSING"} == {"confidentiality_exceptions"}
    assert all(row["status"] == "COVERED" for key, row in rows.items() if key != "confidentiality_exceptions")
    for key in ("during_contract_confidentiality", "post_termination_confidentiality", "confidentiality_duration"):
        assert all(duration in row["quote"] for row in rows[key]["supporting_evidence"]
                   if row.get("evidence_role") != "OBLIGATED_PARTY_CONTEXT")
        assert {p["obligated_party"] for p in rows[key]["party_coverage"]} == {"甲方", "乙方"}


def test_blank_fields_and_one_party_period_cannot_cover_other_party():
    rows = states("第一条 保密义务\n甲方：\n1．保密内容：算法。\n2．涉密人员：研发人员。\n3．保密期限：合同有效期内及终止后8年。\n乙方：\n1．保密内容：____。\n2．涉密人员：待填写。\n3．保密期限：待补充。", confidentiality_detail_elements)
    assert rows["confidential_information_scope"]["status"] == "PARTIALLY_COVERED"
    assert rows["post_termination_confidentiality"]["status"] == "PARTIALLY_COVERED"
    assert rows["post_termination_confidentiality"]["search_targets"] == ["乙方合同终止或解除后的继续保密义务"]


@pytest.mark.parametrize("a,b", [("(1)甲方", "（2）乙方"), ("一、甲方", "二、乙方"), ("甲方", "乙方")])
def test_numbered_actor_headings_bind_only_their_own_field_group(a, b):
    rows = states(f"第一条 保密义务\n{a}：\n1．保密内容：未公开算法。\n2．保密期限：自接触保密信息之日起至终止后6年。\n{b}：\n1．保密内容：客户信息。\n2．保密期限：合同有效期内。", confidentiality_detail_elements)
    scope = {row["obligated_party"]: row for row in rows["confidential_information_scope"]["party_coverage"]}
    assert set(scope) == {"甲方", "乙方"}
    for party, expected in (("甲方", "未公开算法"), ("乙方", "客户信息")):
        direct = [f for f in scope[party]["supporting_evidence"] if f.get("evidence_role") != "OBLIGATED_PARTY_CONTEXT"]
        assert direct and all(expected in f["quote"] for f in direct)
    period = {row["obligated_party"]: row for row in rows["post_termination_confidentiality"]["party_coverage"]}
    assert period["甲方"]["status"] == "COVERED"
    assert period["乙方"]["status"] == "MISSING"


def test_unidentified_group_does_not_borrow_a_later_actor():
    rows = states("第一条 保密义务\n1．保密内容：乙方提供的未公开算法。\n2．保密期限：自接触保密信息之日起至终止后6年。\n乙方：\n1．保密内容：客户信息。\n2．保密期限：合同有效期内。", confidentiality_detail_elements)
    scope = rows["confidential_information_scope"]
    assert scope["status"] == "PARTIALLY_COVERED"
    parties = {row["obligated_party"]: row for row in scope["party_coverage"]}
    assert set(parties) == {"UNKNOWN", "乙方"}
    assert parties["UNKNOWN"]["status"] == "UNCERTAIN"
    assert all("未公开算法" not in fact["quote"] for fact in parties["乙方"]["supporting_evidence"])
    period = {row["obligated_party"]: row for row in rows["post_termination_confidentiality"]["party_coverage"]}
    assert period["乙方"]["status"] == "MISSING"


def test_missing_actor_headings_recover_from_only_the_same_group_liability():
    rows = states("第一条 保密义务\n1．保密内容：未公开算法。\n2．保密期限：自接触保密信息之日起至终止后6年。\n3．泄密责任：甲方违反保密义务应赔偿损失。\n1．保密内容：客户信息。\n2．保密期限：合同有效期内。\n3．泄密责任：乙方违反保密义务应赔偿损失。", confidentiality_detail_elements)
    scope = {row["obligated_party"]: row for row in rows["confidential_information_scope"]["party_coverage"]}
    assert set(scope) == {"甲方", "乙方"}
    for party, expected in (("甲方", "未公开算法"), ("乙方", "客户信息")):
        direct = [f for f in scope[party]["supporting_evidence"] if f.get("evidence_role") != "OBLIGATED_PARTY_CONTEXT"]
        assert direct and all(expected in f["quote"] for f in direct)
        assert all(party + "违反保密义务" in f["actor_source_evidence"][0]["quote"] for f in direct)


def test_field_value_on_next_line_uses_the_existing_semantic_extractor():
    rows = states("第一条 保密义务\n保密内容：\n原型设计和未公开算法。\n涉密人员：\n参与研发及验收的人员。\n保密期限：\n自首次接触保密信息之日起至合同终止后9年。", confidentiality_detail_elements)
    assert all(row["status"] == "COVERED" for key, row in rows.items() if key != "confidentiality_exceptions")
    assert "\n" in rows["confidential_information_scope"]["supporting_evidence"][0]["quote"]
    service = states("第一条 技术支持\n内容：\n系统部署和参数配置。\n方式：\n远程支持。\n乙方提供4个月技术支持。\n费用：\n合同总价已包含技术服务费用。", ancillary_service_detail_elements)
    assert all(row["status"] == "COVERED" for row in service.values()), service


def test_ordinary_period_and_court_reference_do_not_prove_survival_or_exception():
    rows = states("第一条 保密义务\n保密内容：非公开产品设计。\n保密期限：合同有效期内。\n合同终止后无需承担保密义务。发生争议由法院裁判。\n第二条 服务期限\n终止后提供3年技术支持。", confidentiality_detail_elements)
    assert rows["during_contract_confidentiality"]["status"] == "COVERED"
    assert rows["confidentiality_duration"]["status"] == "COVERED"
    assert rows["post_termination_confidentiality"]["status"] == "MISSING"
    assert rows["confidentiality_exceptions"]["status"] == "MISSING"


def test_public_exception_is_partial_until_other_exception_categories_are_found():
    rows = states("第一条 保密\n已经公开的信息不属于保密信息。", confidentiality_detail_elements)
    row = rows["confidentiality_exceptions"]
    assert row["status"] == "PARTIALLY_COVERED"
    assert row["search_targets"] == ["合法取得信息例外", "独立开发信息例外", "依法披露例外"]
    rows = states("第一条 保密\n已公开信息、合法取得的信息及独立开发的信息不属于保密信息。依法应司法机关要求可以披露的信息属于例外。", confidentiality_detail_elements)
    assert rows["confidentiality_exceptions"]["status"] == "COVERED"


@pytest.mark.parametrize("duration", ["3个月", "六个月"])
def test_ancillary_support_fields_recall_their_own_ordinary_parameters(duration):
    rows = states(f"第一条 技术指导和培训\n乙方在成果交付后提供{duration}技术支持。\n1．内容：系统部署、参数配置、故障排查及技术人员培训；\n2．地点和方式：远程支持与现场支持相结合；\n3．费用：合同总价已包含上述技术服务费用。", ancillary_service_detail_elements)
    assert all(row["status"] == "COVERED" for row in rows.values()), rows
    assert rows["service_content"]["supporting_evidence"][0]["quote"].startswith("1．内容")
    assert duration in rows["service_period"]["supporting_evidence"][0]["quote"]


def test_support_period_does_not_prove_content_method_or_fee():
    rows = states("第一条 技术支持\n交付后乙方提供2个月技术支持。\n第二条 研发工作\n内容：系统部署、参数配置。\n第三条 付款\n费用：10万元。", ancillary_service_detail_elements)
    assert rows["service_existence"]["status"] == "COVERED"
    assert rows["service_period"]["status"] == "COVERED"
    assert all(rows[key]["status"] == "MISSING" for key in ("service_content", "service_method", "service_fee"))


PRINCIPLE = "第一条 后续改进\n甲方后续改进成果归甲方所有。乙方后续改进成果归乙方所有。\n如乙方后续改进成果与甲方实施项目直接相关，甲方享有优先获得许可的权利，具体许可条件由双方另行协商。"


def test_priority_is_covered_while_each_negotiated_condition_is_missing():
    rows = states(PRINCIPLE, improvement_license_detail_elements)
    assert rows["priority_license"]["status"] == "COVERED"
    assert "优先获得许可" in rows["priority_license"]["supporting_evidence"][0]["quote"]
    principle = rows["priority_or_negotiated_license"]
    assert principle["status"] == "PARTIALLY_COVERED"
    assert "但" in principle["proposition"]
    assert _partial_element_narrative_label(principle["proposition"]) == principle["proposition"].rstrip("。")
    conditions = {"license_fee", "license_territory", "license_duration", "commercial_use", "improvement_sublicense"}
    assert {key for key, row in rows.items() if row["status"] == "MISSING"} == conditions
    assert set(principle["search_targets"]) == {rows[key]["required_fact"] for key in conditions}


def test_primary_license_terms_cannot_complete_improvement_terms():
    rows = states(PRINCIPLE + "\n第二条 现有专利许可\n许可费10万元；许可地域为全球；许可期限3年；允许商业使用；禁止分许可。", improvement_license_detail_elements)
    assert all(rows[key]["status"] == "MISSING" for key in ("license_fee", "license_territory", "license_duration", "commercial_use", "improvement_sublicense"))


def test_separate_improvement_terms_cover_only_their_own_conditions():
    rows = states(PRINCIPLE + "\n改进成果许可费为8万元；改进成果许可地域为中国境内；改进成果许可期限为4年；改进成果允许商业使用，但不得分许可。", improvement_license_detail_elements)
    assert all(rows[key]["status"] == "COVERED" for key in ("license_fee", "license_territory", "license_duration", "commercial_use", "improvement_sublicense")), rows
    assert rows["priority_or_negotiated_license"]["status"] == "COVERED"
    rows = states(PRINCIPLE + "\n改进成果允许商业使用，分许可条件另行协商。", improvement_license_detail_elements)
    assert rows["commercial_use"]["status"] == "COVERED"
    assert rows["improvement_sublicense"]["status"] == "MISSING"


def test_current_uploaded_contract_has_direct_atoms_and_only_actual_residuals():
    fixture = Path(__file__).resolve().parents[2] / "test_data" / "47 技术开发（委托）合同.docx"
    text = InputLayer()._extract_from_docx_content(fixture.read_bytes())
    confidentiality = states(text, confidentiality_detail_elements)
    assert {key for key, row in confidentiality.items() if row["status"] == "MISSING"} == {"confidentiality_exceptions"}
    assert all(row["status"] == "COVERED" for key, row in confidentiality.items() if key != "confidentiality_exceptions")
    service = states(text, ancillary_service_detail_elements)
    assert all(row["status"] == "COVERED" for row in service.values()), service
    improvement = states(text, improvement_license_detail_elements)
    assert improvement["priority_license"]["status"] == "COVERED"
    assert improvement["priority_or_negotiated_license"]["status"] == "PARTIALLY_COVERED"
    assert {key for key, row in improvement.items() if row["status"] == "MISSING"} == {"license_fee", "license_territory", "license_duration", "commercial_use", "improvement_sublicense"}


def test_current_uploaded_contract_production_clauses_keep_five_direct_atoms_for_each_party():
    fixture = Path(__file__).resolve().parents[2] / "test_data" / "47 技术开发（委托）合同.docx"
    text = InputLayer()._extract_from_docx_content(fixture.read_bytes())
    clauses = _operative_technology_clauses(text)
    by_clause = {clause.clause_id: clause for clause in clauses}
    rows = confidentiality_detail_elements(clauses, extract_field=extract_semantic_field_value)
    five = [row for row in rows if row["element_id"] != "confidentiality_exceptions"]
    assert len(five) == 5
    actor_fields = {"甲方": set(), "乙方": set()}
    for row in five:
        parties = {p["obligated_party"]: p for p in row["party_coverage"]}
        assert set(parties) == {"甲方", "乙方"}, row
        for party, atom in parties.items():
            assert atom["status"] == "COVERED"
            direct = [f for f in atom["supporting_evidence"] if f.get("evidence_role") != "OBLIGATED_PARTY_CONTEXT"]
            context = [f for direct_fact in direct for f in direct_fact.get("actor_source_evidence", [])]
            assert direct and context
            assert len(direct) == len(atom["supporting_evidence"])
            assert all(f["obligated_party"] == party for f in atom["supporting_evidence"])
            assert all(party in f["quote"] for f in context)
            for fact in [*atom["supporting_evidence"], *context]:
                assert fact["quote"] in by_clause[fact["clause_id"]].text
            actor_fields[party].update(f["clause_id"] for f in direct)
    assert actor_fields["甲方"].isdisjoint(actor_fields["乙方"])
