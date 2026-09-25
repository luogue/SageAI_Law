"""Cross-clause loan cost and epistemic-boundary regressions."""
from collections import Counter

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import review_contract_v2
from review_v2.loan_costs import analyze_costs, external_assessment, EXTERNAL_FACT_NODES


PARTIES = "出借人：许某，身份证号：测试甲。\n借款人：周某，身份证号：测试乙。\n"
REGULAR = "第一条 利息\n借款月利率为0.6%，自实际交付之日起计算。\n"
OVERDUE = "第二条 逾期\n逾期每日按本金的0.015%支付逾期利息。\n"
CAP = "借期利息、逾期利息、违约金及其他融资费用合计不得超过合同成立时一年期LPR四倍。"


def analyze(text):
    return analyze_costs(parse_contract_clauses(PARTIES + text))


@pytest.mark.parametrize("regular,overdue,expected", [(0.6, 0.015, 12.675), (1.1, 0.03, 24.15), (0.8, 0.02, 16.9)])
def test_varied_rates_are_normalized_and_combined(regular, overdue, expected):
    text = f"第一条 利率\n借款月利率为{regular}%。\n第二条 逾期\n每逾期一日按本金的{overdue}%计收逾期利息。"
    a = analyze(text)
    assert a["stacking"] in {"AMBIGUOUS", "REPLACEMENT"}
    assert a["potential_annual_percent_estimate"] is None
    assert [c["annual_percent_estimate"] for c in a["components"]] == pytest.approx([regular*12,overdue*365])
    assert a["needs_check"]
    assert a["lpr_verification"] == "FORMATION_DATE_UNKNOWN"
    for c in a["components"]:
        assert c["evidence_id"] in {e["evidence_id"] for e in a["evidence"]}


def test_replacement_scope_does_not_add_regular_interest():
    a = analyze(REGULAR + OVERDUE + "逾期后不再计收借期利息，仅收取逾期利息。" + CAP)
    assert a["stacking"] == "REPLACEMENT"
    assert a["judicial_protection"]["normalized_totals"]["overdue_principal_annual_percent"] == pytest.approx(5.475)
    assert not a["needs_check"]


def test_explicit_cumulative_and_unquantified_fee_require_combined_check():
    a = analyze(REGULAR + OVERDUE + "逾期利息与借期利息同时计收，另行支付违约金及管理费2000元。")
    assert a["stacking"] == "CUMULATIVE"
    assert a["needs_check"]
    assert any(c["annual_percent_estimate"] is None for c in a["components"])


def test_individual_ceiling_does_not_prove_combined_ceiling():
    a = analyze(REGULAR + OVERDUE + "借款利率超过司法保护上限的部分按照法律执行。")
    assert not a["combined_contractual_cap"]
    assert a["needs_check"]


def test_combined_ceiling_is_not_external_verification():
    a = analyze(REGULAR + OVERDUE + "逾期后仅收取逾期利息。" + CAP)
    assert a["combined_contractual_cap"]
    assert not a["needs_check"]
    assert a["lpr_verification"] == "FORMATION_DATE_UNKNOWN"


def test_combined_cap_alone_does_not_resolve_time_scope_ambiguity():
    a = analyze(REGULAR + OVERDUE + CAP)
    assert a["combined_contractual_cap"]
    assert a["stacking"] in {"AMBIGUOUS", "REPLACEMENT"}
    assert a["judicial_protection"]["status"] == "PASS"
    assert a["lpr_verification"] == "FORMATION_DATE_UNKNOWN"


def test_declared_lpr_is_not_verified_but_effective_combined_cap_limits_claim():
    a = analyze(REGULAR + OVERDUE + "逾期利息与借期利息同时计收。合同成立时一年期LPR为3%。" + CAP)
    assert a["judicial_protection"]["cap_percent"] is None
    assert a["combined_contractual_cap"]
    assert a["judicial_protection"]["status"] == "PASS"


def test_enforcement_costs_and_prohibited_financing_fees_are_excluded():
    a = analyze(REGULAR + "第二条 费用\n实现债权的律师费、保全费、公证费、执行费、交通费及差旅费由借款人承担。不得收取咨询费、服务费或管理费。")
    assert {c["kind"] for c in a["components"]} == {"regular_interest"}


def test_repeated_annex_rate_is_not_a_second_charge_and_conflict_is_preserved():
    duplicate = analyze(REGULAR + OVERDUE + "附件：借条\n借款月利率为0.6%。")
    conflict = analyze(REGULAR + OVERDUE + "附件：借条\n借款月利率为0.9%。" + CAP)
    assert len(duplicate["components"]) == 2
    assert not duplicate["conflicting_rates"]
    assert conflict["conflicting_rates"]
    assert conflict["combined_contractual_cap"]
    assert conflict["potential_annual_percent_estimate"] is None


@pytest.mark.parametrize("node", EXTERNAL_FACT_NODES)
def test_external_facts_are_never_confirmed_from_silence(node):
    a = external_assessment(node, parse_contract_clauses(PARTIES + REGULAR))
    assert a["text_assessment"] == "NO_RISK_INDICATOR_FOUND"
    assert a["external_fact_status"] == "NOT_VERIFIED"
    assert not a["evidence"]


@pytest.mark.parametrize("node,positive,negative", [
    ("loan_relending_bank_loan_invalid", "出借人套取银行贷款转贷给借款人。", "出借人不得套取银行贷款转贷。"),
    ("loan_professional_lender_invalid", "出借人经常性向不特定对象放贷。", "出借人声明并非职业放贷人。"),
    ("loan_illegal_purpose_known_invalid", "出借人明知借款用于赌博仍然出借。", "借款人不得将借款用于赌博。"),
])
def test_external_risk_indicator_and_negative_statement_have_distinct_semantics(node, positive, negative):
    assert external_assessment(node, parse_contract_clauses(PARTIES + positive))["evidence"]
    a = external_assessment(node, parse_contract_clauses(PARTIES + negative))
    assert not a["evidence"]
    assert a["external_fact_status"] == "NOT_VERIFIED"


@pytest.mark.parametrize("cap", [False, True])
def test_full_pipeline_cost_truth_evidence_and_counters(cap):
    text = PARTIES + REGULAR + OVERDUE + ("逾期后仅收取逾期利息。" + CAP if cap else "")
    r = review_contract_v2(text, "loan", use_llm=False)
    rows = {i["item_id"]: i for i in r["items"]}
    assert r["release_quality_gate"]["status"] == "REPORT_READY", r["release_quality_gate"]["failures"]
    assert rows['L-04-02']['coverage_status']==('通过' if cap else '待核验')
    # The fixture gives a daily rate/base, but no explicit end of accrual.
    assert rows['L-05-02']['coverage_status']=='部分覆盖'
    assert 'loan_cost_assessment' not in rows['L-05-02']['decision_trace']
    assert dict(Counter(i['coverage_status'] for i in rows.values())) == r['coverage_summary']
    assert not any({'L-04-02','L-05-02'}<=set(f['source_review_ids']) for f in r['risk_findings'])
    if not cap:
        assert rows['L-04-02']['action_priority']=='NONE'
        assert all(e['status']=='COVERED' for e in rows['L-04-02']['coverage_elements'])
    collection = [f for f in r["risk_findings"] if set(f["source_review_ids"]) & {"L-11-02", "L-12-04"}]
    assert len(collection) == 1
    assert set(collection[0]["source_review_ids"]) == {"L-11-02", "L-12-04"}
    assert len(r["risk_themes"]) < sum(i["coverage_status"] in {"缺失", "部分覆盖", "风险条款"} for i in rows.values())


def test_financial_lender_does_not_inherit_private_lending_combination_cap():
    r = review_contract_v2("出借人：兴隆银行股份有限公司。\n借款人：周某，身份证号：测试乙。\n" + REGULAR + OVERDUE, "loan", use_llm=False)
    rows = {i["item_id"]: i for i in r["items"]}
    assert rows["L-04-02"]["coverage_status"] == "不适用"
    assert "loan_cost_assessment" not in rows["L-05-02"]["decision_trace"]


@pytest.mark.parametrize("node,text", [
    ("loan_relending_bank_loan_invalid", "本借款来源于出借人套取银行贷款转贷。"),
    ("loan_professional_lender_invalid", "出借人经常性向不特定对象放贷。"),
    ("loan_illegal_purpose_known_invalid", "出借人明知借款用于赌博仍然出借。"),
])
def test_external_positive_signal_survives_pipeline_without_claiming_verified_facts(node, text):
    r = review_contract_v2(PARTIES + REGULAR + "第二条 资金事实\n" + text, "loan", use_llm=False)
    item = next(i for i in r["items"] if i["node_id"] == node)
    assert item["coverage_status"] == "风险条款"
    assert item["decision_trace"]["external_fact_assessment"]["external_fact_status"] == "NOT_VERIFIED"
    assert "尚未核实" in item["reasoning_summary"]
    assert item["evidence_clauses"]
    assert r["release_quality_gate"]["status"] == "REPORT_READY", r["release_quality_gate"]["failures"]


def test_llm_pass_cannot_erase_cost_risk_or_confirm_external_facts(monkeypatch):
    from dataclasses import replace
    import review_v2.engine as engine
    from review_v2.semantic_reviewer import judge_checkpoint
    def excessive_pass(checkpoints, clauses, **kwargs):
        return {c.item_id: replace(judge_checkpoint(c, clauses), coverage_status="通过", status="已覆盖", risk_level="低", reasoning_summary="已确认不存在职业放贷，所有利率合法。") for c in checkpoints}
    monkeypatch.setattr(engine, "judge_checkpoints_with_llm", excessive_pass)
    r = engine.review_contract_v2(PARTIES + REGULAR + OVERDUE, "loan", use_llm=True)
    rows = {i["item_id"]: i for i in r["items"]}
    assert rows["L-04-02"]["coverage_status"] == "待核验"
    assert rows["L-05-02"]["coverage_status"] == "部分覆盖"
    for key in ("L-02-01", "L-02-02", "L-02-03"):
        assert "不能据此确认" in rows[key]["reasoning_summary"]


def test_same_sentence_interest_and_management_fee_are_distinct_components():
    a = analyze("第一条 利率\n借款月利率为0.6%，另按月支付管理费0.2%。\n" + OVERDUE)
    assert {c["kind"] for c in a["components"]} >= {"regular_interest", "financing_fee", "overdue_interest"}
    assert a["potential_annual_percent_estimate"] is None
    assert a["judicial_protection"]["status"] == "PENDING"


def test_distinct_financing_fees_with_equal_rates_are_both_counted():
    a = analyze(REGULAR + OVERDUE + "第三条 费用\n另按月支付管理费0.2%，另按月支付咨询费0.2%。")
    assert len([c for c in a["components"] if c["kind"] == "financing_fee"]) == 2
    assert a["potential_annual_percent_estimate"] is None
    assert a["judicial_protection"]["status"] == "PENDING"
