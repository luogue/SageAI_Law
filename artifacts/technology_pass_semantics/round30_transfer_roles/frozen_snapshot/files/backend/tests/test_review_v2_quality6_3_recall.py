from pathlib import Path

from layers.input_layer import InputLayer
from review_v2.clause_parser import document_integrity, parse_contract_clauses, strip_non_contract_tail
from review_v2.contract_facts import extract_contract_fact_graph
from review_v2.engine import review_contract_v2


class _Upload:
    def __init__(self, path: Path):
        self.filename = path.name
        self.file = path.open("rb")


def _historical_sale_text() -> str:
    path = next((Path(__file__).resolve().parents[2] / "test_data").glob("5*.docx"))
    upload = _Upload(path)
    try:
        return InputLayer().extract_text_from_file(upload)
    finally:
        upload.file.close()


def _by_id(output):
    return {item["item_id"]: item for item in output["items"]}


def test_sale_hb_002_raw_docx_recovers_explicit_contract_truth():
    text = _historical_sale_text()
    output = review_contract_v2(text, "sale", use_llm=False)
    by_id = _by_id(output)

    assert output["document_integrity"]["truncated"] is False
    assert output["document_integrity"]["parsed_character_ratio"] >= 0.99
    assert output["contract_context"]["contract_type"] == "sale"
    assert output["contract_context"]["user_perspective"] == "buyer"
    assert by_id["S-04-03"]["coverage_status"] == "不适用"

    for review_id in (
        "S-00-01",
        "S-01-01",
        "S-02-01",
        "S-02-02",
        "S-02-03",
        "S-03-01",
        "S-03-02",
        "S-05-01",
        "S-05-02",
        "S-06-02",
        "S-07-01",
        "S-07-04",
        "S-08-01",
        "S-08-03",
    ):
        assert by_id[review_id]["coverage_status"] != "缺失", review_id
        assert by_id[review_id]["evidence_clauses"], review_id

    standard_order = by_id["S-06-01"]
    standard_elements = {row["element_id"]: row["status"] for row in standard_order["coverage_elements"]}
    assert standard_elements["multiple_standards_exist"] == "COVERED"
    assert standard_elements["precedence_between_standards"] in {"MISSING", "UNCERTAIN"}

    facts = output["contract_facts"]["facts"]
    assert {fact["normalized_value"] for fact in facts["delivery.date"]} >= {"2026-09-10", "2026-09-20"}
    assert any(fact["normalized_value"] == 100 for fact in facts["quantity.total"])
    assert any(fact["normalized_value"] == "台" for fact in facts["quantity.unit"])
    assert any(fact["normalized_value"] == 576000 for fact in facts["price.total"])
    assert any(fact["normalized_value"] == 0.2 for fact in facts["prepayment.ratio"])
    assert any(fact["normalized_value"] == 115200 for fact in facts["prepayment.amount"])
    assert any(fact["normalized_value"] == "2026-09-10" for fact in facts["delivery.batch1.deadline"])
    assert any(fact["normalized_value"] == "2026-09-20" for fact in facts["delivery.batch2.deadline"])
    assert any(fact["normalized_value"] == "2026-09-20" for fact in facts["delivery.final_deadline"])
    assert any(fact["normalized_value"] == 0.2 for fact in facts["inspection.sample_ratio"])
    assert any(fact["normalized_value"] == "5个工作日" for fact in facts["seller_response.deadline"])
    assert any(fact["normalized_value"] == 0.15 for fact in facts["breach.seller_non_delivery_ratio"])
    assert any(fact["normalized_value"] == "2026-08-18" for fact in facts["contract.effective_date"])
    assert any(fact["normalized_value"] == "2027-08-17" for fact in facts["contract.expiry_date"])
    assert "damages.expectation_loss" in facts
    assert "damages.foreseeability_limit" in facts
    assert all(fact["source_clause_ids"] and fact["source_spans"] for rows in facts.values() for fact in rows)

    assert output["legal_reference_issues"]
    assert not any(finding["risk_group"] == "sale_unilateral_price_adjustment" for finding in output["risk_findings"])
    assert output["release_quality_gate"]["status"] == "REPORT_READY"


def test_long_contract_early_middle_tail_annex_and_cross_clause_recall():
    padding = "\n".join(f"背景条款{i}：双方按订单履行一般协作义务。" for i in range(1, 45))
    text = f"""
    买卖合同
    第一条 购货单位：甲公司；供货单位：乙公司。产品为设备A，共100台。
    {padding}
    第二十三条 乙方最迟应于2026年9月20日前完成全部供货。
    {padding}
    第四十六条 买方应在收货后7日内完成验收，抽检比例20%。
    第四十七条 质量异议应在7日内书面提出，卖方5个工作日内处理。
    第四十八条 质量问题可要求修理、更换、退货、减少价款或赔偿损失。
    第四十九条 本合同自2026年8月18日起生效。
    附件一 技术标准
    产品质量执行GB/T 12668.2国家标准及企业标准Q/HD 2026-03。
    """
    output = review_contract_v2(text, "sale", use_llm=False)
    by_id = _by_id(output)
    assert by_id["S-03-01"]["coverage_status"] != "缺失"
    assert by_id["S-07-01"]["coverage_status"] != "缺失"
    assert by_id["S-06-03"]["coverage_status"] in {"通过", "部分覆盖"}
    assert by_id["S-00-01"]["coverage_status"] != "缺失"
    assert by_id["S-02-03"]["coverage_status"] != "缺失"
    assembly = by_id["S-06-03"]["decision_trace"]["evidence_assembly"]
    assert len(assembly["candidate_evidence"]) >= 3


def test_retrieval_debug_contains_all_candidate_sources_and_missing_proof():
    output = review_contract_v2(
        "买卖合同。甲方为买方，乙方为卖方。产品A单价420元。双方无交付时间约定。",
        "sale",
        use_llm=False,
    )
    item = _by_id(output)["S-03-01"]
    trace = item["decision_trace"]["retrieval_trace"]
    assert set(trace) >= {
        "fact_clause_ids",
        "structural_clause_ids",
        "lexical_clause_ids",
        "semantic_clause_ids",
        "graph_clause_ids",
        "candidate_clause_ids",
    }
    assert item["decision_trace"]["missing_proof"]["exhaustive_enough"] is True
    assert item["system_confidence"]["retrieval_recall_confidence"] == "high"


def test_review_mode_and_in_transit_applicability_mutations():
    ordinary = review_contract_v2(
        "买卖合同。卖方负责送货到买方仓库。价格固定为420元，任何一方不得单方调价。",
        "sale",
        use_llm=False,
    )
    in_transit = review_contract_v2(
        "路货买卖合同。双方买卖一批已经发运、正在运输途中的货物。",
        "sale",
        use_llm=False,
    )
    ordinary_items = _by_id(ordinary)
    assert ordinary_items["S-04-03"]["coverage_status"] == "不适用"
    assert ordinary_items["S-02-05"]["coverage_status"] == "通过"
    assert ordinary_items["S-02-05"]["decision_trace"]["review_mode"] == "ABSENCE_REQUIRED"
    assert _by_id(in_transit)["S-04-03"]["coverage_status"] != "不适用"


def test_document_integrity_and_template_block_separation():
    text = """
    特别提示：本范本根据1999年《中华人民共和国合同法》制订。
    订立合同双方
    购货单位：甲公司；供货单位：乙公司。
    第一条 产品A应于2026年9月20日前交付。
    第十三条 本合同自2026年8月18日起生效。
    范本附注
    一、使用本范本时应咨询专业人士。
    """
    clauses = parse_contract_clauses(text)
    integrity = document_integrity(text, clauses)
    assert integrity.truncated is False
    assert integrity.parsed_character_ratio >= 0.99
    assert any(clause.block_type == "TEMPLATE_INSTRUCTION" for clause in clauses)
    assert any(clause.block_type == "OPERATIVE_CLAUSE" and "2026年9月20日" in clause.text for clause in clauses)


def test_contract_status_field_does_not_truncate_contract_body():
    text = """专利权转让合同
当前状态：已取得授权
转让方将完整专利权转让给受让方。
专利权转让登记完成后，专利权转移至受让方。
"""

    stripped = strip_non_contract_tail(text)

    assert "当前状态：已取得授权" in stripped
    assert "专利权转移至受让方" in stripped


def test_standalone_test_note_heading_still_starts_non_contract_tail():
    text = """专利权转让合同
转让方将完整专利权转让给受让方。
测试说明：
以下内容不是合同正文。
"""

    stripped = strip_non_contract_tail(text)

    assert "转让方将完整专利权转让给受让方" in stripped
    assert "以下内容不是合同正文" not in stripped


def test_generic_fact_normalization_and_source_trace():
    clauses = parse_contract_clauses(
        """
        买卖合同
        购货单位：甲公司，以下简称甲方；供货单位：乙公司，以下简称乙方。
        第一条 产品总数量：100台；合同总价576,000元。
        第二条 预付款为合同总价20%，人民币115200元。
        第三条 乙方于2026/09/20前完成供货。
        第四条 质保18个月，3个工作日响应，10个工作日维修或更换。
        """
    )
    graph = extract_contract_fact_graph(clauses)
    assert any(fact.normalized_value == 100 for fact in graph.facts["quantity.total"])
    assert any(fact.normalized_value == 576000 for fact in graph.facts["price.total"])
    assert any(fact.normalized_value == 0.2 for fact in graph.facts["prepayment.ratio"])
    assert any(fact.normalized_value == 115200 for fact in graph.facts["prepayment.amount"])
    assert any(fact.normalized_value == "2026-09-20" for fact in graph.facts["delivery.date"])
    assert graph.facts["party.buyer.name"][0].source_clause_ids
    assert graph.facts["party.seller.name"][0].source_spans
