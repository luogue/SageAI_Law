"""Compatibility tests for Word document extraction."""

import io
from pathlib import Path

from layers.input_layer import InputLayer
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import review_contract_v2


class _UploadFile:
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self.file = io.BytesIO(content)


def test_extracts_legacy_word_file_renamed_as_docx():
    fixture = next((Path(__file__).resolve().parents[2] / "test_data").glob("1*.docx"))
    upload = _UploadFile(fixture.name, fixture.read_bytes())

    text = InputLayer().extract_text_from_file(upload)

    assert len(text) > 100
    assert "上海市房屋租赁合同" in text
    assert "出租方" in text
    assert "承租方" in text
    assert "月租金的2倍" in text
    assert "产证编号" in text


def test_real_house_lease_review_uses_structured_clauses_and_practical_ratings():
    fixture = next((Path(__file__).resolve().parents[2] / "test_data").glob("1*.docx"))
    upload = _UploadFile(fixture.name, fixture.read_bytes())
    text = InputLayer().extract_text_from_file(upload)

    clauses = parse_contract_clauses(text)
    assert any(clause.location == "九、第6项" and "逾期不支付租金累计超过 1 个月" in clause.text for clause in clauses)
    assert any(clause.location == "十、（六）" and "提前退租天数的租金的2倍" in clause.text for clause in clauses)

    output = review_contract_v2(text, "house_lease", include_low_risk=True, use_llm=False)
    by_id = {item["item_id"]: item for item in output["items"]}

    assert output["summary"]["高"] <= 2
    assert by_id["HL-005"]["coverage_status"] == "通过"
    assert by_id["HL-015"]["coverage_status"] == "通过"
    assert by_id["HL-010"]["risk_level"] == "中"
    assert by_id["HL-039"]["risk_level"] in {"中", "低"}
    assert by_id["HL-029"]["coverage_status"] == "通过"
    assert by_id["HL-030"]["coverage_status"] == "不适用"
    assert by_id["HL-031"]["coverage_status"] == "通过"
    assert by_id["HL-035"]["risk_level"] == "低"
    assert by_id["HL-035"]["coverage_status"] == "部分覆盖"
    assert "附件三" in by_id["HL-035"]["evidence_location"] or "家电" in by_id["HL-035"]["evidence_location"]
    assert "备案" not in by_id["HL-035"]["evidence_location"]
    assert "房地产经纪" not in by_id["HL-002"]["evidence_location"]
