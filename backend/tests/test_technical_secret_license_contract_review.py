from pathlib import Path
import json

import pytest
from docx import Document

from review_v2.engine import review_contract_v2
from review_v2.technology_service_analysis import (
    analyze_patent_license_consistency,
    analyze_payment_schedule,
    analyze_technical_secret_loss_arrangement,
    classify_technology_transaction,
)
from review_v2.user_profile import UserRiskProfile


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "test_data" / "28 技术许可（技术秘密）合同.docx"


BASE_SECRET_LICENSE = """
技术许可（技术秘密）合同
甲方（被许可方）与乙方（许可方）订立本合同。
第一条 技术秘密内容：未公开的控制算法、源代码、控制参数和测试数据。
第二条 乙方将上述技术秘密以排他许可方式许可甲方实施，许可方应向被许可方交付完整技术秘密资料清单、源代码和接口说明。
第三条 许可期限五年，许可地域为中国境内，仅限生产合同产品。
第四条 技术秘密许可使用费为人民币100万元。
第五条 双方对在履行中取得的对方算法、源代码、控制参数、测试数据、生产数据、销售数据和客户资料承担保密义务，未经信息提供方书面同意不得向第三方披露或用于合同外目的；双方保密义务在合同终止后十年内持续有效。
"""


def _fixture_text() -> str:
    document = Document(str(FIXTURE))
    parts = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
    for table in document.tables:
        for row in table.rows:
            text = " | ".join(cell.text.strip() for cell in row.cells)
            if text.strip(" |"):
                parts.append(text)
    return "\n".join(parts)


def _review(text: str) -> dict:
    return review_contract_v2(
        text,
        "technology",
        include_low_risk=True,
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/被许可方"),
    )


@pytest.fixture(scope="module")
def contract_text() -> str:
    return _fixture_text()


@pytest.fixture(scope="module")
def review(contract_text: str) -> dict:
    return _review(contract_text)


@pytest.fixture(scope="module")
def balanced_review() -> dict:
    return _review(BASE_SECRET_LICENSE)


def test_case_a_b_c_secret_loss_content_reasonableness():
    reasonable = analyze_technical_secret_loss_arrangement(
        "第七条 技术秘密公开后的处理。技术秘密因第三方合法公开或进入公共领域后，"
        "被许可方停止支付未来许可费并有权解除合同；已提供且具有独立价值的技术服务据实结算。"
    )
    adverse = analyze_technical_secret_loss_arrangement(
        "第七条 技术秘密公开后的处理。技术秘密因第三方公开、进入公共领域或许可方申请专利导致公开后，"
        "被许可方仍须继续支付尚未到期的技术秘密许可使用费、技术服务费和提成费，已付款不退，不得单方解除合同。"
    )

    assert classify_technology_transaction(BASE_SECRET_LICENSE)["tertiary_subtype"] == "TECHNICAL_SECRET_LICENSE"
    assert reasonable["reasonable"] is True
    assert reasonable["adverse"] is False
    assert adverse["adverse"] is True
    assert adverse["unconditional_future_payment"] is True
    assert adverse["termination_restricted"] is True


def test_case_d_e_f_license_type_consistency():
    exclusive_clean = analyze_patent_license_consistency(
        "技术秘密排他实施许可合同。许可方保留自行实施权，但不得再许可任何第三方，并确认不存在既有许可。"
    )
    exclusive_conflict = analyze_patent_license_consistency(
        "技术秘密排他实施许可合同。许可方此前已向第三方授予普通许可，该许可期限与本合同重叠；"
        "许可方仍可向科研合作企业提供相关技术。"
    )
    ordinary = analyze_patent_license_consistency(
        "技术秘密普通许可合同。许可方可同时向多个第三方授予普通许可。"
    )

    assert exclusive_clean["exclusive_license_conflict"] is False
    assert exclusive_conflict["existing_third_party_license"] is True
    assert exclusive_conflict["reserved_collaboration_permission"] is True
    assert exclusive_conflict["exclusive_license_conflict"] is True
    assert ordinary["licensor_third_party_license_permission"] is True
    assert ordinary["exclusive_license_conflict"] is False


def test_case_g_h_ancillary_service_and_acceptance_are_fact_routed():
    composite = BASE_SECRET_LICENSE + """
第六条 技术服务和技术指导。许可方负责软件部署、参数标定、系统调试、现场技术支持和人员培训。
第七条 验收标准。项目完成后按照测试环境、测试数据、性能指标和测试方法进行验收；未通过验收应整改并重新验收，验收合格后付款。
"""
    composite_classification = classify_technology_transaction(composite)
    plain_classification = classify_technology_transaction(BASE_SECRET_LICENSE)

    assert composite_classification["tertiary_subtype"] == "TECHNICAL_SECRET_LICENSE"
    assert {"technical_service", "technical_guidance", "acceptance"} <= set(
        composite_classification["sub_transactions"]
    )
    assert "technical_service" not in plain_classification["sub_transactions"]
    assert "acceptance" not in plain_classification["sub_transactions"]


def test_case_i_j_confidentiality_balance_is_directional(
    balanced_review: dict,
    review: dict,
):
    balanced = {row["item_id"]: row for row in balanced_review["items"]}["TC-11-02"]
    asymmetric = {row["item_id"]: row for row in review["items"]}["TC-11-02"]

    assert balanced["coverage_status"] == "通过"
    assert balanced["issue_type"] == "通过"
    assert asymmetric["coverage_status"] == "风险条款"
    assert "明显不对等" in asymmetric["title"]
    assert any(
        row.get("element_id") == "licensor_post_termination_data_use"
        and row.get("status") == "ADVERSE"
        for row in asymmetric["coverage_elements"]
    )


def test_case_k_l_infringement_presence_is_separate_from_direction(
    balanced_review: dict,
    review: dict,
):
    adverse = {row["item_id"]: row for row in review["items"]}["TC-12-01"]
    absent = {row["item_id"]: row for row in balanced_review["items"]}["TC-12-01"]

    assert adverse["coverage_status"] == "风险条款"
    assert adverse["issue_type"] == "DEFAULT_LAW_DEVIATION"
    assert any(
        row.get("element_id") == "compliant_use_infringement_allocation"
        and row.get("status") == "ADVERSE"
        for row in adverse["coverage_elements"]
    )
    assert absent["coverage_status"] == "缺失"


def test_current_secret_license_full_regression(contract_text: str, review: dict):
    classification = classify_technology_transaction(contract_text)
    payment = analyze_payment_schedule(contract_text)
    by_id = {row["item_id"]: row for row in review["items"]}

    assert classification["primary_subtype"] == "TECHNOLOGY_LICENSE"
    assert classification["tertiary_subtype"] == "TECHNICAL_SECRET_LICENSE"
    assert classification["primary_contract_type"] == "technology_license_technical_secret"
    assert classification["scenario"] == "TECHNICAL_SECRET_LICENSE"
    assert {"technical_service", "technical_guidance", "acceptance", "technical_secret"} <= set(
        classification["sub_transactions"]
    )

    assert payment["status"] == "INCONSISTENT"
    assert payment["contract_total"] == 2_400_000
    assert payment["percentage_total"] == 120
    assert payment["amount_total"] == 2_880_000
    assert payment["amount_delta"] == 480_000

    assert "技术秘密许可合同" in by_id["TC-01-01"]["risk_point_description"]
    assert "专利实施许可合同" not in by_id["TC-01-01"]["risk_point_description"]
    assert by_id["TC-07-01"]["coverage_status"] == "风险条款"
    assert "既有第三方普通许可" in by_id["TC-07-01"]["risk_point_description"]
    assert by_id["TC-09-01"]["coverage_status"] != "不适用"
    assert by_id["TC-09-02"]["coverage_status"] == "风险条款"
    assert "单方控制" in by_id["TC-09-02"]["title"]
    assert by_id["TC-09-04"]["coverage_status"] != "不适用"
    assert by_id["TC-12-03"]["coverage_status"] == "风险条款"
    assert "持续付款" in by_id["TC-12-03"]["title"]
    assert not any(
        row.get("review_id") == "TC-12-01"
        for row in review["review_evidence_element_gate"].get("mismatches", [])
    )
    assert by_id["TC-13-03"]["coverage_status"] == "部分覆盖"
    test_elements = {row["element_id"]: row for row in by_id["TC-13-03"]["coverage_elements"]}
    assert test_elements["test_plan_attachment_arrangement"]["status"] == "COVERED"
    assert test_elements["retest_mechanism"]["status"] == "MISSING"

    for item_id in ("TC-03-04", "TC-13-02"):
        item = by_id[item_id]
        assert item["coverage_status"] == "部分覆盖"
        recommendation = str(item.get("suggested_clause_example") or item.get("action_suggestion") or "")
        assert "专利证书" not in recommendation
        assert "专利登记簿" not in recommendation


def _item(result: dict, item_id: str) -> dict:
    return next(row for row in result["items"] if row["item_id"] == item_id)


def test_over_scope_liability_a_missing_when_no_responsibility_clause(contract_text: str):
    result = _review(contract_text.replace(
        "3．买方违反许可范围的，应支付人民币3,000,000元违约金，并赔偿卖方全部损失。",
        "",
    ))
    assert _item(result, "TC-07-03")["coverage_status"] == "缺失"


def test_over_scope_liability_b_existing_clause_is_not_missing(contract_text: str):
    result = _review(contract_text.replace(
        "3．买方违反许可范围的，应支付人民币3,000,000元违约金，并赔偿卖方全部损失。",
        "3．买方违反许可范围的，应承担违约责任并赔偿卖方实际直接损失。",
    ))
    item = _item(result, "TC-07-03")
    assert item["coverage_status"] != "缺失"
    assert any(
        row.get("element_id") == "over_scope_breach_remedy"
        and row.get("status") == "COVERED"
        for row in item["coverage_elements"]
    )


def test_over_scope_liability_c_fixed_penalty_and_all_losses_checks_cumulative_relation(
    contract_text: str,
):
    result = _review(contract_text)
    item = _item(result, "TC-07-03")
    elements = {row["element_id"]: row for row in item["coverage_elements"]}
    assert item["coverage_status"] == "风险条款"
    assert elements["over_scope_breach_remedy"]["status"] == "COVERED"
    assert elements["cumulative_remedy_boundary"]["status"] == "MISSING"
    assert "累计" in item["risk_point_description"]


def test_over_scope_liability_d_reasonable_clause_can_pass_or_be_partial(contract_text: str):
    result = _review(contract_text.replace(
        "3．买方违反许可范围的，应支付人民币3,000,000元违约金，并赔偿卖方全部损失。",
        "3．买方超出许可范围的，应立即停止并赔偿实际直接损失；"
        "一般违约赔偿总额不超过已付许可费的30%，故意或重大过失不适用该上限。",
    ))
    item = _item(result, "TC-07-03")
    assert item["coverage_status"] in {"通过", "部分覆盖"}


def test_positive_fact_evidence_wins_over_search_audit_absence(review: dict):
    item = _item(review, "TC-12-01")
    cap = next(
        row for row in item["coverage_elements"]
        if row.get("element_id") == "licensor_rights_defect_liability"
    )
    assert cap["status"] == "ADVERSE"
    assert cap.get("evidence_ids")
    rendered = json.dumps(review, ensure_ascii=False)
    assert "未找到许可方对其提供技术的权利瑕疵责任受到低额责任上限限制" not in rendered


def test_secret_label_without_direct_measures_does_not_cover_measures():
    result = _review("""
技术秘密许可合同
甲方（被许可方）与乙方（许可方）订立本合同。
乙方将未公开的控制参数作为技术秘密许可甲方使用。
""")
    item = _item(result, "TC-03-04")
    measure = next((
        row for row in item["coverage_elements"]
        if row.get("element_id") == "existing_confidentiality_measures"
    ), None)
    assert measure is None or measure["status"] != "COVERED"


def test_explicit_employee_nda_access_control_and_secret_list_cover_measures():
    result = _review(BASE_SECRET_LICENSE + """
第六条 许可方已建立技术秘密清单和分级管理制度，对源代码设置系统访问控制及加密存储；
所有研发人员已签署员工保密协议，向第三方披露前要求签署第三方保密承诺。
""")
    item = _item(result, "TC-03-04")
    measure = next(
        row for row in item["coverage_elements"]
        if row.get("element_id") == "existing_confidentiality_measures"
    )
    assert measure["status"] == "COVERED"
    assert measure.get("evidence_ids")
