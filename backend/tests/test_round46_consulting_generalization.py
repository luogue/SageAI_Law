"""Round46: 新技术咨询合同（33 技术咨询服务合同）泛化回归。

固定输入：test_data/33 技术咨询服务合同.docx
  docx sha256 a2641cb765ee3aeb473781794c45ee2b2d1a54c9ab736a49c38da6970e65a9e2
  text sha256 b349675cb2c28efa03c987e6de1ce930d7fc9322b4a257220cf61fb5f7af7152

本轮修复的是公共能力，不是样本特判：
  1. 同义决策风险表述（"仅作为……决策参考""自行决定是否采用"）进入
     qualified_consulting_decision_risk 的 canonical 映射。
  2. 瑕疵触发允许以"服务"为主体，并识别"不能令人满意"这一同义表述。
  3. 补正期限支持"期限 + 动作"语序（"30天的期限改正或弥补"）。
  4. proposition_scope 不再把"任何时候"里的"何时"误判为疑问词而丢弃整句。

Gate 仍可能因本合同真实的付款/期限不一致而 BLOCKED；本测试不因
样本通过而放宽 Gate，只锁定"原文有事实即不应假 MISSING"。
"""
from pathlib import Path

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.consulting_element_facts import elements as consulting_elements
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile


TEXT = (Path(__file__).parent / "fixtures" / "round46_consulting_generalization.txt").read_text(encoding="utf-8")


def indexed(rows):
    return {row["element_id"]: row for row in rows}


def test_decision_risk_synonyms_project_qualified_canonical_fact():
    """决策风险由委托方承担：'仅作为决策参考'+'自行决定是否采用'的同义表述。"""
    clauses = parse_contract_clauses(TEXT)
    rows = indexed(consulting_elements("consulting_decision", clauses))
    assert rows["qualified_consulting_decision_risk"]["status"] == "COVERED"
    assert rows["qualified_consulting_decision_risk"]["supporting_evidence"]


def test_consultant_professional_error_is_a_fault_exception():
    """咨询方自身专业错误(重大计算/数据错误、违反技术标准)即过错例外。"""
    clauses = parse_contract_clauses(TEXT)
    rows = indexed(consulting_elements("consulting_decision", clauses))
    assert rows["consultant_fault_exception"]["status"] == "COVERED"
    assert rows["consultant_fault_exception"]["supporting_evidence"]


def test_incoterm_and_mailing_channel_are_delivery_forms():
    """交付形式不限于电子/纸质：Incoterm 与邮寄渠道同为明示交付形式。"""
    clauses = parse_contract_clauses(TEXT)
    rows = indexed(consulting_elements("consulting_quality", clauses))
    assert rows["delivery_form"]["status"] == "COVERED"
    assert rows["delivery_form"]["supporting_evidence"]


def test_service_satisfaction_and_deadline_first_wording_project_remedy_atoms():
    """瑕疵触发('服务不能令人满意')与补正期限('30天的期限改正')的语序变体。"""
    clauses = parse_contract_clauses(TEXT)
    rows = indexed(consulting_elements("consulting_remedy", clauses))
    for key in {"defect_trigger", "correction_period", "correction_remedy"}:
        assert rows[key]["status"] == "COVERED", key
        assert rows[key]["supporting_evidence"], key


def test_quantifier_anytime_is_not_treated_as_interrogative():
    """'在任何时候'不是疑问词：含该量词的条件义务不得被整体丢弃。"""
    from review_v2.proposition_scope import arrangement_matches
    sentence = ("如果咨询方在其控制的范围内在任何时候、以任何原因向委托方提供"
                "本合同附件一中的工作范围内的服务不能令人满意，委托方可将不满意之处"
                "通知咨询方，并给咨询方30天的期限改正或弥补。")
    assert list(arrangement_matches(r"服务不能令人满意", sentence))
    assert list(arrangement_matches(r"30天的期限改正或弥补", sentence))


@pytest.mark.parametrize("party", ["甲方", "乙方"])
def test_final_snapshot_has_no_false_missing_for_repaired_rules(party):
    """已修复规则：原文有事实即不得再出现 MISSING / 假缺失审计。"""
    result = review_contract_v2(
        TEXT, "technology", use_llm=False, include_low_risk=True,
        profile=UserRiskProfile(user_identity=party),
    )
    repaired = {"TC-08-01": {"delivery_form"},
                "TC-08-02": {"qualified_consulting_decision_risk"},
                "TC-08-04": {"defect_trigger", "correction_period"}}
    for item in result.get("items", []):
        iid = item.get("item_id")
        if iid not in repaired:
            continue
        covered = {r["element_id"] for r in item.get("coverage_elements", [])
                   if r.get("status") == "COVERED"}
        missing = {r["element_id"] for r in
                   (item.get("decision_trace", {}) or {}).get("element_absence_searches", [])
                   if r.get("result") == "NOT_FOUND"}
        assert repaired[iid] <= covered, iid
        # DIRECT affirmative evidence 与 NOT_FOUND 不得共存
        assert covered.isdisjoint(missing), iid
