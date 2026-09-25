"""Atomic, event-bound development delay and exit coverage regressions."""
from review_v2.clause_parser import parse_contract_clauses
from review_v2.development_exit import development_exit_elements


def states(text):
    return {row["element_id"]: row for row in development_exit_elements(parse_contract_clauses(text))}


def test_delay_liability_does_not_prove_payment_delay_or_termination():
    rows = states("第一条 违约责任\n乙方逾期未完成研发任务，应承担违约责任并赔偿甲方损失。")
    assert rows["development_delay_liability"]["status"] == "COVERED"
    for key in ("payment_delay_liability", "development_termination_mechanism", "exit_development_cost_settlement"):
        assert rows[key]["status"] == "MISSING"
        assert rows[key]["supporting_evidence"] == []


def test_normal_delivery_cannot_cover_exit_handover():
    rows = states("第一条 成果交付\n乙方应于项目完成时交付源代码、研发资料、样品及阶段成果。\n第二条 解除\n乙方严重违约时，甲方有权解除合同。")
    assert rows["development_termination_mechanism"]["status"] == "COVERED"
    for key in ("exit_source_code_handover", "exit_research_material_handover", "exit_sample_handover", "exit_stage_result_handover"):
        assert rows[key]["status"] == "MISSING", rows[key]


def test_exit_objects_ownership_and_settlement_are_independent():
    rows = states("第一条 提前解除\n合同解除后，乙方应向甲方交接源代码。\n未完成成果归甲方所有。\n开发费用的结算方式另行协商。")
    assert rows["exit_source_code_handover"]["status"] == "COVERED"
    assert rows["exit_unfinished_result_ownership"]["status"] == "COVERED"
    assert rows["exit_development_cost_settlement"]["status"] == "PARTIALLY_COVERED"
    assert rows["exit_sample_handover"]["status"] == "MISSING"


def test_all_required_atoms_can_be_covered_without_composite_claims():
    rows = states("第一条 开发和付款迟延\n乙方逾期开发应赔偿损失。甲方逾期付款应支付违约金。\n第二条 解除\n项目研发失败时一方可以通知另一方解除合同。合同解除后乙方应移交研发资料、源代码、样品和阶段成果。未完成成果归甲方所有。开发费用按已完成工作比例结算。")
    assert len(rows) == 9
    assert all(row["status"] == "COVERED" and row["supporting_evidence"] for row in rows.values()), rows


def test_express_contrary_bargain_is_not_absence_and_settlement_is_not_refund():
    rows = states("第一条 解除\n合同解除时研发费用不予退还。解除后乙方无需交付源代码。")
    assert rows["exit_development_cost_settlement"]["status"] == "COVERED"
    assert rows["exit_source_code_handover"]["status"] == "ADVERSE"
    assert rows["exit_source_code_handover"]["supporting_evidence"]


def test_exit_heading_does_not_turn_past_delivery_into_handover_duty():
    rows = states("第一条 合同解除\n合同正常履行时乙方交付源代码。合同解除后乙方可以收回已交付的源代码。")
    assert rows["exit_source_code_handover"]["status"] == "MISSING"
