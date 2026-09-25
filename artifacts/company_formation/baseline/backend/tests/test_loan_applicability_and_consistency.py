"""Regression coverage for scenario gates, shared facts and final projections."""
from collections import Counter
from dataclasses import replace
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET

import pytest

from review_v2.clause_parser import parse_contract_clauses, BLOCK_ANNEX
from review_v2.loan_facts import LoanFacts, extract, financing_charge
from review_v2.loan_contract_checklist import get_loan_checklist
from review_v2.engine import review_contract_v2
from review_v2.semantic_reviewer import judge_checkpoint, recall_candidate_clauses


PARTIES = "出借人（甲方）：陈某，身份证号：测试甲。\n借款人（乙方）：黄某，身份证号：测试乙。\n"
TERMS = "第一条 借款金额\n借款本金人民币80000元。\n第二条 借款期限\n借款期限自2028年1月1日起至2029年1月1日止。\n第三条 利率\n借款月利率为0.7%。\n第四条 保证\n保证人承担连带责任保证，保证期间为主债务履行期限届满之日起二年。\n"


def facts(text):
    return LoanFacts.from_clauses(parse_contract_clauses(text))


@pytest.mark.parametrize("lender,borrower,financial,enterprise", [
    ("张某，身份证号：测试甲", "赵某，身份证号：测试乙", False, False),
    ("晨曦银行股份有限公司", "赵某，身份证号：测试乙", True, False),
    ("晨曦贸易有限公司", "朝阳科技有限公司", False, True),
    ("晨曦贸易有限公司", "赵某，身份证号：测试乙", False, False),
    ("____", "____", None, None),
])
def test_role_bound_party_applicability(lender, borrower, financial, enterprise):
    f = facts(f"出借人：{lender}。\n借款人：{borrower}。\n还款账户开户行：中国银行。")
    assert f.applicability("loan_financial_interest_compliance")["applicable"] is financial
    assert f.applicability("loan_enterprise_business_need")["applicable"] is enterprise


@pytest.mark.parametrize("extra,node,expected", [
    ("", "loan_old_for_new_guarantor_notice", False),
    ("本借款用于偿还原贷款。", "loan_old_for_new_guarantor_notice", True),
    ("本借款不用于偿还原贷款。", "loan_old_for_new_guarantor_notice", False),
    ("若新贷款用于偿还旧贷款，应由保证人确认。", "loan_old_for_new_guarantor_notice", False),
    ("本次借款系借新还旧。", "loan_old_for_new_guarantor_notice", True),
    ("担保物应办理抵押登记。", "loan_sale_security_distinction", False),
    ("借款人将房屋过户至出借人名下担保本借款。", "loan_sale_security_distinction", True),
    ("本合同不采用买卖担保。", "loan_sale_security_distinction", False),
    ("如申请展期，须经出借人同意。", "loan_extension_request", True),
    ("双方不涉及展期。", "loan_extension_request", False),
    ("", "loan_extension_interest_rate", False),
    ("借款用于家庭日常生活。", "loan_daily_family_need", True),
    ("借款用于夫妻共同经营。", "loan_daily_family_need", False),
    ("借款不用于家庭日常生活。", "loan_daily_family_need", False),
    ("", "loan_interest_no_agreement_rule", False),
    ("", "loan_early_repayment_notice", False),
    ("借款人可以提前还款。", "loan_early_repayment_notice", True),
])
def test_scenarios_require_positive_evidence(extra, node, expected):
    f = facts(PARTIES + TERMS + "第五条 其他\n" + extra)
    assert f.applicability(node)["applicable"] is expected


@pytest.mark.parametrize("text,expected", [
    ("借款人承担实现债权的公证费、保全费、律师费、诉讼费、执行费、交通费、差旅费。", False),
    ("保证范围包括本金、利息、逾期利息、违约金以及维权费用。", False),
    ("借款人承担维权产生的律师咨询费。", False),
    ("借款人支付逾期违约金。", False),
    ("贷款人不得收取服务费、管理费、咨询费。", False),
    ("贷款人从本金中扣除服务费5000元。", True),
    ("借款人每月向出借人支付管理费300元。", True),
    ("咨询费为本金的2%。", True),
    ("借款人承担诉讼费。另向贷款人支付咨询费1000元。", True),
    ("不收取服务费，但收取管理费500元。", True),
])
def test_financing_fee_semantic_binding(text, expected):
    assert financing_charge(text) is expected
    c = next(c for c in get_loan_checklist() if c.item_id == "L-04-04")
    clauses = parse_contract_clauses("第一条 费用\n" + text)
    candidates, _ = recall_candidate_clauses(c, clauses)
    assert bool(candidates) is expected
    assert (judge_checkpoint(c, clauses).coverage_status == "风险条款") is expected
    evidence = extract(c.node_id, clauses)
    assert bool(evidence) is expected
    for row in evidence:
        assert row["quote"] in next(c.text for c in clauses if c.clause_id == row["clause_id"])


def test_separate_receipt_after_signatures_is_an_evidence_annex():
    clauses = parse_contract_clauses(PARTIES + TERMS + "乙方（签字）：黄某\n借 条\n本人确认借款已实际收到。")
    rows = extract("loan_natural_person_formation", clauses)
    assert rows
    assert all(next(c for c in clauses if c.clause_id == r["clause_id"]).block_type == BLOCK_ANNEX for r in rows)


@pytest.mark.parametrize("text,expected", [
    ("借款金额以转账凭证、收据或聊天记录等材料证明为准。", False),
    ("出借人收到还款后应出具收据。", True),
    ("贷款人应在全部清偿后出具结清证明。", True),
])
def test_disbursement_receipt_is_not_repayment_confirmation(text, expected):
    assert bool(extract("loan_repayment_receipt_confirmation", parse_contract_clauses("第一条 凭证\n" + text))) is expected


@pytest.mark.parametrize("group,title,action", [
    ("loan_repayment_receipt_confirmation", "还款收据", "OPTIONAL_IMPROVEMENT"),
    ("ownership_record", "权属记录", "OPTIONAL_IMPROVEMENT"),
    ("relationship_record", "关系记录", "OPTIONAL_IMPROVEMENT"),
    ("sale_ip_compliance", "合法授权", "SHOULD_CHANGE"),
    ("intellectual_property", "权利保障", "SHOULD_CHANGE"),
    ("patent_claim", "专利侵权", "SHOULD_CHANGE"),
])
def test_final_disposition_domain_tags_are_whole_words(group, title, action):
    from review_v2.engine import RiskFinding, _build_final_dispositions
    finding = RiskFinding("RF-test", group, title, "LOW", "C_OPTIMIZATION", ["TEST"], [], [])
    assert _build_final_dispositions([finding], [], [])[0].final_action == action


def test_absent_and_blank_rate_do_not_disable_no_agreement_rule():
    for text in ("", "借款月利率为__%。", "逾期利率为5%。"):
        assert facts(PARTIES + text).applicability("loan_interest_no_agreement_rule")["applicable"] is True


def test_multiline_party_declarations_and_interest_free_agreement():
    f = facts("出借人：林某\n身份证号：测试甲\n借款人：周某\n身份证号：测试乙\n第一条 利息\n本借款无息。")
    assert f.values["lender_kind"] == f.values["borrower_kind"] == "natural"
    assert f.applicability("loan_interest_no_agreement_rule")["applicable"] is False


@pytest.mark.parametrize("extra,expected", [
    ("仅支付律师费、诉讼费和保全费。", "通过"),
    ("甲方放款时扣收咨询费2000元。", "风险条款"),
])
def test_financing_fee_full_pipeline(extra, expected):
    r = review_contract_v2(PARTIES + TERMS + "第五条 费用\n" + extra, "loan", use_llm=False)
    item = next(i for i in r["items"] if i["item_id"] == "L-04-04")
    assert item["coverage_status"] == expected
    assert r["loan_shared_fact_consistency_gate"]["status"] == "REPORT_READY"
    if expected == "风险条款":
        assert item["evidence_clauses"]
        assert all(financing_charge(e.get("quote") or e["text"]) for e in item["evidence_clauses"])


def test_final_shared_fact_gate_detects_a_downstream_regression():
    from review_v2.engine import ReviewItemResult
    from review_v2.loan_facts import consistency_gate
    r = review_contract_v2(PARTIES + TERMS, "loan", use_llm=False)
    from dataclasses import fields
    allowed={f.name for f in fields(ReviewItemResult)}
    items = [ReviewItemResult(**{k:v for k,v in i.items() if k in allowed}) for i in r["items"]]
    consumer = next(i for i in items if i.item_id == "L-11-01")
    consumer.coverage_status = "缺失"
    gate = consistency_gate(items, facts(PARTIES + TERMS))
    assert gate["status"] == "BLOCKED"
    assert any(f["review_id"] == "L-11-01" for f in gate["failures"])


def test_active_scenario_does_not_itself_prove_guarantor_consent():
    r = review_contract_v2(PARTIES + TERMS + "第五条 借款用途\n本借款用于偿还原贷款。\n第六条 展期\n借款人可以申请展期。", "loan", use_llm=False)
    rows = {i["item_id"]: i for i in r["items"]}
    assert rows["L-09-04"]["applicability"]["applicable"] is True
    assert rows["L-09-04"]["coverage_status"] == "缺失"
    assert rows["L-08-03"]["applicability"]["applicable"] is True
    assert rows["L-08-03"]["coverage_status"] == "缺失"
    assert rows["L-08-01"]["coverage_status"] == "部分覆盖"


def test_llm_cannot_create_scenarios_or_contradict_shared_maturity(monkeypatch):
    import review_v2.engine as engine
    seen = []
    def contradictory(checkpoints, clauses, **kwargs):
        seen.extend(c.item_id for c in checkpoints)
        return {c.item_id: replace(judge_checkpoint(c, clauses), coverage_status="缺失", risk_level="高", status="缺失", issue_type="完全缺失", evidence_clauses=[], reasoning_summary="未明确还款期限和到期日") for c in checkpoints}
    monkeypatch.setattr(engine, "judge_checkpoints_with_llm", contradictory)
    r = engine.review_contract_v2(PARTIES + TERMS, "loan", use_llm=True)
    by_id = {i["item_id"]: i for i in r["items"]}
    assert not {"L-04-03", "L-02-04", "L-09-04", "L-08-01", "L-05-04"} & set(seen)
    for key in ("L-06-01", "L-11-01"):
        assert by_id[key]["coverage_status"] == "通过"
        assert "未明确还款期限" not in by_id[key]["reasoning_summary"]
    assert by_id["L-06-01"]["decision_trace"]["shared_fact_consumption"] == by_id["L-11-01"]["decision_trace"]["shared_fact_consumption"]


@pytest.mark.parametrize("specific", [False, True])
def test_evidence_management_only_escalates_on_concrete_exposure(specific):
    text = PARTIES + TERMS + ("第五条 现状\n该笔债权的诉讼时效已经届满。" if specific else "")
    r = review_contract_v2(text, "loan", use_llm=False)
    by_id = {i["item_id"]: i for i in r["items"]}
    assert by_id["L-06-03"]["action_priority"] == "C_OPTIMIZATION"
    assert by_id["L-06-03"]["decision_trace"]["default_law_assessment"]["status"] == "CLEAR_DEFAULT"
    item = by_id["L-11-02"]
    assert item["action_priority"] == ("A_CORE" if specific else "C_OPTIMIZATION")
    assert item["risk_severity"] == ("HIGH" if specific else "LOW")


@pytest.fixture(scope="module")
def current_report():
    # Acceptance fixture only. Production code never sees filenames or IDs.
    root = Path(__file__).resolve().parents[2]
    path = next((root / "test_data").glob("49 *.docx"))
    with zipfile.ZipFile(path) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    text = "\n".join("".join(n.text or "" for n in p.findall(".//w:t", ns)) for p in document.findall(".//w:p", ns))
    return text, review_contract_v2(text, "loan", use_llm=False)


def test_current_48_rules_and_final_counters(current_report):
    text, r = current_report
    rows = {i["item_id"]: i for i in r["items"]}
    assert len(rows) == r["all_items_count"] == 48
    assert r["release_quality_gate"]["status"] == "REPORT_READY", r["release_quality_gate"]["failures"]
    assert dict(Counter(i["coverage_status"] for i in rows.values())) == r["coverage_summary"]
    na = {key for key, i in rows.items() if i["coverage_status"] == "不适用"}
    assert {"L-04-03", "L-02-04", "L-09-04", "L-01-03", "L-05-04", "L-10-02", *[f"L-08-0{n}" for n in range(1, 5)]} <= na
    for key in na:
        item = rows[key]
        assert item["applicability"]["applicable"] is False
        assert item["risk_severity"] == "NONE"
        assert not item["suggested_clause_example"]
    for f in r["risk_findings"]:
        assert not na.intersection(f["source_review_ids"])
    for suggestion in r["recommendations"]:
        assert not na.intersection(suggestion.get("target_review_ids", []))
    assert rows["L-04-04"]["coverage_status"] == "通过"
    assert not rows["L-04-04"]["evidence_clauses"]
    assert rows["L-04-02"]["coverage_status"] == rows["L-05-02"]["coverage_status"] == "部分覆盖"
    costs = rows["L-04-02"]["decision_trace"]["loan_cost_assessment"]
    assert costs["potential_annual_percent_estimate"] == pytest.approx(16.9)
    assert costs["stacking"] == "AMBIGUOUS"
    assert len(r['items'])==48
    assert r["coverage_summary"] == dict(Counter(i['coverage_status'] for i in r['items']))
    for key in ("L-02-01", "L-02-02", "L-02-03"):
        item = rows[key]
        assert item["coverage_status"] == "待核验"
        assert item["issue_type"] == "外部事实核验"
        assert item["risk_severity"] == item["action_priority"] == "NONE"
        assert item["decision_trace"]["review_nature"] == "EXTERNAL_FACT_VERIFICATION"
        assert "合同文本未发现异常，相关实际事实需结合" in item["reasoning_summary"]
        assert not item["suggested_clause_example"]
        assert not any(key in f["source_review_ids"] for f in r["risk_findings"])
    combined = next(f for f in r["risk_findings"] if f["risk_group"] == "loan_overdue_combined_cost")
    assert set(combined["source_review_ids"]) == {"L-04-02", "L-05-02"}
    assert r["final_overview_summary"]["medium_risk"] == 1
    assert r["final_overview_summary"]["low_risk"] == sum(f['severity']=='LOW' for f in r['risk_findings'])
    assert r["risk_theme_count"] == len(r['risk_findings'])
    assert rows["L-06-01"]["coverage_status"] == rows["L-11-01"]["coverage_status"] == "通过"
    for key in ("L-06-03", "L-06-04", "L-11-02", "L-11-04"):
        assert rows[key]["action_priority"] == "C_OPTIMIZATION"
        assert rows[key]["risk_severity"] == "LOW"
    overview = r["final_overview_summary"]
    assert overview["priority_action"] == overview["major_risk"] == 0
    assert overview["optional_action"] == r["final_disposition_summary"]["optional_improvement"]
    for i in rows.values():
        if i["decision_trace"].get("loan_evidence_binding"):
            for e in i["evidence_clauses"]:
                assert (e.get("quote") or e["text"]) in text


def test_core_summary_and_detail_share_final_dispositions(current_report):
    _, r = current_report
    rows = {i["item_id"]: i for i in r["items"]}
    for finding in r["risk_findings"]:
        assert all(rows[key]["coverage_status"] not in {"不适用", "通过"} for key in finding["source_review_ids"])
    assert r["risk_theme_count"] == len(r["risk_themes"])
    assert r["risk_finding_summary"]["低风险"] == r["final_overview_summary"]["low_risk"]
    assert r["report_disposition_projection_gate"]["status"] == "REPORT_READY"
