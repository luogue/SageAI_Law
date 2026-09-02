"""Quality 6.1 integration assertions through the real upload route."""

import asyncio
import io
from pathlib import Path

from docx import Document

from routers import review_v2 as review_router
from routers.review_v2 import review_v2_file


ROOT = Path(__file__).resolve().parents[2]


class _UploadFile:
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self.file = io.BytesIO(content)


def _docx_bytes(text: str) -> bytes:
    document = Document()
    for line in text.splitlines():
        document.add_paragraph(line)
    output = io.BytesIO()
    document.save(output)
    return output.getvalue()


def _review_bytes(content: bytes, contract_type: str, profile_json: str = "{}"):
    return asyncio.run(
        review_v2_file(
            file=_UploadFile(f"{contract_type}.docx", content),
            contract_type=contract_type,
            include_low_risk=True,
            use_llm=False,
            profile_json=profile_json,
            current_user={"id": 1},
        )
    )


def _fixture(pattern: str) -> bytes:
    return next((ROOT / "test_data").glob(pattern)).read_bytes()


def test_review_upload_runtime_source_guard_detects_stale_loaded_code(monkeypatch):
    assert review_router._runtime_source_drift_status()["status"] == "CURRENT"

    monkeypatch.setitem(
        review_router._LOADED_DEPENDENCY_SOURCES["engine"],
        "sha256",
        "stale-loaded-engine-source",
    )
    status = review_router._runtime_source_drift_status()

    assert status["status"] == "STALE_RUNTIME"
    assert status["changed_dependencies"] == ["engine"]


def test_sale_production_trace_and_legal_claim_scope():
    output = _review_bytes(_fixture("2*.docx"), "sale")
    by_id = {item["item_id"]: item for item in output["items"]}
    trace = output["observability"]["production_trace"]

    assert output["system_metadata"]["system_version"] == "contract-review-quality-6.4"
    assert output["contract_context"]["usage_scenario"] == "GENERAL_GOODS_SALE"
    assert output["profile"]["contract_scenario"] == "商品买卖"
    assert output["observability"]["domain_pack_snapshot"]["contract_type"] == "sale"
    assert output["release_quality_gate"]["status"] == "REPORT_READY"
    assert output["observability"]["pre_render_quality_gate"]["status"] == "REPORT_READY"
    assert trace["active_pipeline"].endswith("engine.py:review_contract_v2")
    assert "SaleDomainPack loaded" in trace["active_components"]
    assert "FindingEvidenceGate executed" in trace["active_components"]
    assert "PriorityConsistencyVerifier executed" in trace["active_components"]
    assert all(output["observability"]["output_hashes"].values())

    unilateral = by_id["S-02-05"]
    assert unilateral["coverage_status"] == "风险条款"
    assert any(row.get("entailment_status") == "SUPPORTS" for row in unilateral["evidence_clauses"])
    finding = next(row for row in output["risk_findings"] if "S-02-05" in row["source_review_ids"])
    assert finding["provenance"]["created_by"].endswith("engine.py:_build_risk_findings")
    assert finding["provenance"]["evidence_ids"]

    litigation_cost = by_id["S-00-05"]
    assert not any(claim.get("article") == "第585条" for claim in litigation_cost["legal_references"])
    for claim in output["legal_citation_claims"]:
        if claim.get("article"):
            assert claim.get("authority_links")
            assert claim.get("support_scope")


def test_independent_verifier_accepts_element_level_partial_support(monkeypatch):
    from review_v2 import engine as review_engine

    monkeypatch.setattr(
        review_engine,
        "_finding_needs_verification",
        lambda finding: finding.risk_group == "sale_quality_remedy",
    )
    output = _review_bytes(
        _fixture("2*.docx"),
        "sale",
        '{"risk_appetite":"保守","bargaining_position":"弱势方","jurisdiction":"成都"}',
    )
    quality_remedy = next(
        finding
        for finding in output["risk_findings"]
        if finding["risk_group"] == "sale_quality_remedy"
    )
    source_item = next(
        item
        for item in output["items"]
        if item["item_id"] in quality_remedy["source_review_ids"]
    )

    assert source_item["coverage_status"] == "部分覆盖"
    assert any(
        element["status"] in {"COVERED", "PARTIALLY_COVERED"}
        and element["entailment"] in {"SUPPORTS", "PARTIAL_SUPPORT"}
        for element in source_item["coverage_elements"]
    )
    assert quality_remedy["verification"]["status"] == "PASS"
    assert output["release_quality_gate"]["status"] == "REPORT_READY"


def test_fixed_price_table_does_not_create_unilateral_price_finding():
    contract = """买卖合同
甲方（出卖人）：甲公司
乙方（买受人）：乙公司
一、货物及价款
产品A，单价420元，数量500吨。合同价格固定，任何价格变更须经双方书面协商一致。
二、交付
甲方应于2026年9月1日前交付至乙方仓库。
三、质量
乙方应在收货后五日内提出质量异议，甲方负责更换或退货。
"""
    output = _review_bytes(_docx_bytes(contract), "sale")
    by_id = {item["item_id"]: item for item in output["items"]}

    assert by_id["S-02-05"]["coverage_status"] != "风险条款"
    assert not any("S-02-05" in finding["source_review_ids"] for finding in output["risk_findings"])
    assert "存在单方调价" not in output["result"]
    assert output["release_quality_gate"]["status"] == "REPORT_READY"


def test_contract_context_is_fresh_across_request_order():
    samples = [
        ("house_lease", _fixture("1*.docx")),
        ("sale", _fixture("2*.docx")),
        ("service", _fixture("3*.docx")),
        ("sale", _fixture("2*.docx")),
        ("house_lease", _fixture("1*.docx")),
    ]
    outputs = [_review_bytes(content, contract_type) for contract_type, content in samples]

    first_lease, first_sale, service, second_sale, second_lease = outputs
    assert first_sale["contract_context"] == second_sale["contract_context"]
    assert first_lease["contract_context"] == second_lease["contract_context"]
    assert first_sale["contract_context"]["usage_scenario"] == "GENERAL_GOODS_SALE"
    assert first_sale["contract_context"]["domain_attributes"]["lease_fields_used"] is False
    assert first_lease["contract_context"]["usage_scenario"] == "residential_living"
    assert service["contract_context"]["usage_scenario"] == "GENERAL_SERVICE"
    assert service["contract_context"]["transaction_structure"] == "SERVICE"
    assert service["contract_context"]["domain_attributes"]["lease_fields_used"] is False
    assert len({output["contract_review_trace_id"] for output in outputs}) == len(outputs)


def test_partial_quality_narrative_has_single_structured_truth():
    output = _review_bytes(_fixture("2*.docx"), "sale")
    quality = next(item for item in output["items"] if item["item_id"] == "S-06-03")

    assert quality["coverage_status"] == "部分覆盖"
    assert quality["evidence_clauses"]
    assert "未约定质量异议处理机制" not in quality["reasoning_summary"]
    assert output["observability"]["narrative_state_debug_report"]
    assert next(row for row in output["observability"]["narrative_state_debug_report"] if row["review_id"] == "S-06-03")["status"] == "PASS"
