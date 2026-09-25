"""Metamorphic evidence regressions plus the complete EPC review."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest
from docx import Document

from review_v2.clause_parser import parse_contract_clauses
from review_v2.construction_contract_checklist import get_construction_checklist
from review_v2.construction_evidence import employer_coverage, evidence_failures
from review_v2.engine import review_contract_v2, _release_quality_gate
from review_v2.semantic_reviewer import judge_checkpoint


def judge(item_id, text):
    checkpoint = next(c for c in get_construction_checklist() if c.item_id == item_id)
    return judge_checkpoint(checkpoint, parse_contract_clauses(text))


@pytest.mark.parametrize("item_id,text", [
    ("CE-05-01", "承包人不进行转包及违法分包。"),
    ("CE-05-01", "承包人不转包工程。"),
    ("CE-05-01", "承包人不得将全部工程转包。"),
    ("CE-05-01", "若承包人将工程转包，发包人有权解除合同。"),
    ("CE-05-01", "承包人转包的行为无效。"),
    ("CE-05-01", "转包与分包"),
    ("CE-05-03", "分包单位不进行二次分包。"),
    ("CE-02-03", "承包人不得借用资质，不得挂靠。"),
    ("CE-02-03", "应保存实际施工人的工资记录。"),
    ("CE-03-03", "双方承诺不串通投标。"),
    ("CE-06-01", "双方不再签订与合同实质性内容相背离的协议。"),
    ("CE-06-01", "双方不得另行签订背离中标合同实质性内容的协议。"),
    ("CE-06-01", "补充协议不得背离中标合同实质性内容。"),
    ("CE-06-01", "双方可以签订补充协议处理设计变更。"),
    ("CE-10-03", "14.3 预付款\n发包人按时支付农民工工资。"),
    ("CE-10-03", "承包人不放弃工程价款优先受偿权。"),
    ("CE-10-03", "发包人不得要求承包人放弃优先受偿权。"),
    ("CE-10-03", "放弃优先受偿权的条款不生效。"),
])
def test_prevention_and_topics_are_not_adverse_evidence(item_id, text):
    result = judge(item_id, text)
    assert result.coverage_status == "通过"
    assert not result.evidence_clauses


@pytest.mark.parametrize("item_id,text", [
    ("CE-05-01", "承包人可以将全部工程转包给第三人。"),
    ("CE-05-01", "承包人不得转包，但经发包人同意可以转包。"),
    ("CE-05-01", "承包人不得拖欠工资，允许转包全部工程。"),
    ("CE-05-01", "承包人不得不将工程转包。"),
    ("CE-05-03", "分包人有权再分包。"),
    ("CE-02-03", "承包人同意由施工队借用资质施工。"),
    ("CE-03-03", "双方约定通过虚假招标确定承包人。"),
    ("CE-06-01", "双方另行签订背离中标合同实质性内容的协议。"),
    ("CE-06-01", "双方签订与合同实质性内容相背离的补充协议。"),
    ("CE-10-03", "承包人放弃优先受偿权。"),
    ("CE-10-03", "承包人不得主张工程价款优先受偿权。"),
])
def test_affirmative_and_exception_clauses_remain_risks(item_id, text):
    result = judge(item_id, text)
    assert result.coverage_status == "风险条款"
    assert result.evidence_clauses
    assert all(row["text"] in text and row["polarity"] == "AFFIRMED" for row in result.evidence_clauses)


def test_long_clause_quote_contains_actual_predicate():
    text = "14.3 预付款\n" + "发包人及时付款。" * 100 + "承包人放弃优先受偿权。"
    result = judge("CE-10-03", text)
    assert result.coverage_status == "风险条款"
    assert result.evidence_clauses[0]["text"] == "承包人放弃优先受偿权。"


def test_end_to_end_does_not_erase_affirmative_risks():
    output = review_contract_v2("建设工程施工合同\n第一条\n承包人不得转包，但经同意允许转包全部工程。\n第二条\n双方另行签订背离中标合同实质性内容的协议。\n第三条\n承包人放弃优先受偿权。", "construction", use_llm=False)
    for row in output["items"]:
        if row["item_id"] in {"CE-05-01", "CE-06-01", "CE-10-03"}:
            assert row["coverage_status"] == "风险条款"
            assert row["evidence_clauses"]
            assert not evidence_failures([SimpleNamespace(**row)])


def test_decimal_location_is_scoped_to_contract_part_and_excludes_toc():
    text = "目录\n第一部分 协议书\n第二部分 通用条款\n14.3 预付款\n第一部分 协议书\n双方签订EPC总承包合同。\n第二部分 通用条款\n14.3 预付款\n发包人应支付预付款。\n第三部分 专用条款\n14.3 预付款\n预付款为100万元。"
    clauses = parse_contract_clauses(text)
    rows = [c for c in clauses if "预付款为100万元" in c.text]
    assert rows[0].location == "第三部分 专用条款 / 14.3"
    assert next(c for c in clauses if c.text.startswith("目录")).section_type == "使用说明"


def test_cross_clause_recall_and_wrong_party_exclusion():
    text = "3.2 场地\n发包人应在开工前提供施工场地。\n6.1 资料\n发包人应提供技术资料。\n7.1 设备\n发包人应交付甲供设备。\n14.2 付款\n发包人应按月支付工程款。"
    assert set(employer_coverage(parse_contract_clauses(text))) == {"site", "funds", "documents", "materials"}
    assert not employer_coverage(parse_contract_clauses("发包人接收工程前，承包人应负责提供设备。"))
    assert not employer_coverage(parse_contract_clauses("发包人提供的现场条件"))
    assert set(employer_coverage(parse_contract_clauses("发包人应提供施工场地。"))) == {"site"}


@pytest.fixture(scope="module")
def epc_output():
    fixture = Path(__file__).resolve().parents[2] / "test_data" / "50 建设工程.docx"
    document = Document(fixture)
    text = "\n".join(p.text for p in document.paragraphs if p.text.strip())
    return review_contract_v2(text, "construction", use_llm=False)


def test_complete_epc_52_rules(epc_output):
    rows = {row["item_id"]: row for row in epc_output["items"]}
    assert len(rows) == 52
    for key in ("CE-05-01", "CE-06-01", "CE-10-03"):
        assert rows[key]["coverage_status"] == "通过"
        assert not rows[key]["evidence_clauses"]
    assert rows["CE-01-01"]["decision_trace"]["construction_subtype"] == "EPC设计-采购-施工总承包"
    assert all("五、其他" not in r["location"] for r in rows["CE-01-01"]["evidence_clauses"])
    for key in ("CE-09-04", "CE-10-01", "CE-10-02", "CE-10-04"):
        assert rows[key]["coverage_status"] == "法律提示"
        assert rows[key]["risk_severity"] == "NONE"
    assert rows["CE-02-01"]["coverage_status"] == "待核验"
    assert rows["CE-12-01"]["coverage_status"] in {"通过", "部分覆盖"}
    assert epc_output["release_quality_gate"]["status"] == "REPORT_READY"


@pytest.mark.parametrize("text", ["14.3预付款", "承包人不进行转包及违法分包。", "承包人可以转包全部工程。"])
def test_quality_gate_blocks_unrelated_negated_or_fabricated_evidence(epc_output, text):
    row = deepcopy(next(i for i in epc_output["items"] if i["item_id"] == "CE-05-01"))
    row["coverage_status"] = "风险条款"
    row["evidence_clauses"] = [{"clause_id": "fabricated", "text": text}]
    item = SimpleNamespace(**row)
    assert evidence_failures([item])
    # The production release gate consumes the same validator; avoid replacing
    # the full object model with a dict when exercising its remaining checks.
    from review_v2.engine import ReviewItemResult
    from dataclasses import fields
    actual = ReviewItemResult(**{f.name: row[f.name] for f in fields(ReviewItemResult) if f.name in row})
    gate = _release_quality_gate([actual], [], "")
    assert gate["status"] == "BLOCKED"
