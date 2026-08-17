"""Quality 6.5 production-route acceptance and artifact generation."""

from __future__ import annotations

import asyncio
import hashlib
import io
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from routers.review_v2 import review_v2_file


class Upload:
    def __init__(self, path: Path):
        self.filename = path.name
        self.file = io.BytesIO(path.read_bytes())


async def review(path: Path, contract_type: str) -> Dict[str, Any]:
    return await review_v2_file(
        file=Upload(path), contract_type=contract_type, include_low_risk=True,
        use_llm=False, profile_json="{}", current_user={"id": "quality-6.5-audit"},
    )


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


async def main() -> int:
    out = ROOT / "output" / "quality6_5"
    out.mkdir(parents=True, exist_ok=True)
    hb_paths = {
        "SALE-HB-001": next((ROOT / "test_data").glob("2*.docx")),
        "SALE-HB-002": next((ROOT / "test_data").glob("5*.docx")),
        "SALE-HB-003": next((ROOT / "test_data").glob("6*.docx")),
        "RENTAL": next((ROOT / "test_data").glob("1*.docx")),
    }
    results = {
        name: await review(path, "house_lease" if name == "RENTAL" else "sale")
        for name, path in hb_paths.items()
    }
    hb3 = results["SALE-HB-003"]
    context = hb3["contract_context"]
    obs = hb3["observability"]
    facts = hb3["contract_facts"]["real_estate"]
    expected_subjects = {
        "SALE-HB-001": {"GOODS"}, "SALE-HB-002": {"GOODS", "EQUIPMENT"},
        "SALE-HB-003": {"REAL_ESTATE"},
    }
    wrong = [name for name in expected_subjects if results[name]["contract_context"]["subject_matter"] not in expected_subjects[name]]
    wrong_rate = len(wrong) / len(expected_subjects)
    gates = hb3["release_quality_gate"].get("gate_results") or {}
    requirements = {
        "SALE_FAMILY_GATE": context["contract_family"] == "SALE",
        "REAL_ESTATE_SUBJECT_GATE": context["subject_matter"] == "REAL_ESTATE",
        "REAL_ESTATE_DOMAIN_ROUTING": context["contract_subtype"] == "RESIDENTIAL_SECONDARY_REAL_ESTATE_SALE" and context["asset_usage"] == "RESIDENTIAL",
        "REAL_ESTATE_DOMAIN_PACK": obs["review_registry_debug"]["domain_owners"] == ["sale/common", "sale/real_estate"],
        "GOODS_REVIEW_ISOLATION": gates.get("DOMAIN_REVIEW_ISOLATION_GATE") == "PASS",
        "REAL_ESTATE_MATERIAL_COVERAGE": gates.get("DOMAIN_MATERIAL_COVERAGE_GATE") == "PASS",
        "NARRATIVE_TRUTH_GATE": gates.get("NARRATIVE_TRUTH_GATE") == "PASS",
        "SALE_HB_001": results["SALE-HB-001"]["release_quality_gate"]["status"] == "REPORT_READY",
        "SALE_HB_002": results["SALE-HB-002"]["release_quality_gate"]["status"] == "REPORT_READY",
        "SALE_HB_003": hb3["release_quality_gate"]["status"] == "REPORT_READY",
        "RENTAL_REGRESSION": results["RENTAL"]["release_quality_gate"]["status"] == "REPORT_READY",
        "REAL_PRODUCTION_INTEGRATION": all(result["success"] for result in results.values()),
    }
    overall = all(requirements.values()) and wrong_rate == 0

    write_json(out / "classification_trace.json", obs["classification_trace"])
    write_json(out / "domain_routing_debug.json", obs["domain_routing_debug"])
    write_json(out / "review_registry_debug.json", obs["review_registry_debug"])
    write_json(out / "real_estate_fact_debug.json", facts)
    write_json(out / "real_estate_applicability_debug.json", [{"review_id": item["item_id"], "applicability": item["applicability"], "domain_owner": item["decision_trace"].get("domain_owner")} for item in hb3["items"]])
    write_json(out / "domain_material_coverage.json", obs["domain_material_coverage"])
    write_json(out / "narrative_consistency_debug.json", obs["narrative_state_debug_report"])
    write_json(out / "regression_summary.json", {
        "requirements": {key: "PASS" if value else "FAIL" for key, value in requirements.items()},
        "wrong_domain_reports": wrong, "wrong_domain_report_rate": wrong_rate,
        "contexts": {name: result["contract_context"] for name, result in results.items()},
    })
    (out / "domain_ontology_ownership.md").write_text(
        "# Domain Ontology Ownership\n\n"
        "- `shared`: cross-contract invariants.\n"
        "- `sale/common`: family-level sale formation, price, payment, breach and dispute reviews.\n"
        "- `sale/goods/*`: movable-goods delivery, transport, packaging, inspection and warranty reviews.\n"
        "- `sale/real_estate/common`: title, encumbrance, property, land, registration, delivery and defect reviews.\n"
        "- `sale/real_estate/residential_secondary`: household registration and maintenance-fund concerns.\n\n"
        "Registry filtering uses checkpoint domain metadata; report IDs and fixture values do not select domains.\n",
        encoding="utf-8",
    )
    (out / "6_5_domain_root_cause_report.md").write_text(
        "# Quality 6.5 Domain Root Cause Report\n\n"
        "## First Broken Layer\n\n"
        "The parser preserved the real-estate contract. The first failure was sale subject resolution: every sale inherited `GENERAL_GOODS_SALE`, after which the monolithic sale checklist loaded goods-only reviews.\n\n"
        "## Repair\n\n"
        "The production route now resolves family, subject, transaction nature, subtype and asset usage from multiple source-backed signals before checklist selection. Review packs compose through explicit domain metadata, and real-estate facts enrich the shared fact graph with clause provenance.\n\n"
        f"## Result\n\nSALE-HB-003 resolved to `{context['contract_subtype']}`. Wrong-domain report rate: `{wrong_rate:.4f}`. Release gate: `{hb3['release_quality_gate']['status']}`.\n",
        encoding="utf-8",
    )
    manifest = {
        "quality_version": "Contract Review Quality 6.5",
        "created_at": datetime.now().isoformat(), "status": "PASS" if overall else "FAIL",
        "source_hashes": {name: source_hash(path) for name, path in hb_paths.items()},
        "requirements": {key: "PASS" if value else "FAIL" for key, value in requirements.items()},
        "wrong_domain_report_rate": wrong_rate,
        "sale_hb_003_frozen": overall, "next_blind_status": "READY" if overall else "NOT_READY",
        "next_blind": "SALE-BLIND-004",
    }
    write_json(out / "candidate_manifest.json", manifest)
    if overall:
        for destination in (
            ROOT / "benchmark" / "historical_blind" / "sale" / "SALE-HB-003",
            ROOT / "benchmark" / "regression" / "sale" / "real_estate" / "SALE-HB-003",
        ):
            destination.mkdir(parents=True, exist_ok=True)
            shutil.copy2(hb_paths["SALE-HB-003"], destination / "contract.docx")
            write_json(destination / "metadata.json", {
                "case_id": "SALE-HB-003", "source_case_id": "SALE-BLIND-003", "contract_type": "sale",
                "subject_matter": "REAL_ESTATE", "status": "FROZEN_REGRESSION",
                "frozen_version": "contract-review-quality-6.5", "source_hash": source_hash(hb_paths["SALE-HB-003"]),
                "next_blind_case": "SALE-BLIND-004",
            })
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
