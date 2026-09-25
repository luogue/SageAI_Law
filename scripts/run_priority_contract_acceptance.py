"""Export reproducible source contracts, production reports and gate summary.

Run from repository root: python scripts/run_priority_contract_acceptance.py
No cloud model calls; artifacts are written beneath the supplied output folder.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "backend"), str(ROOT / "backend/tests")]

from review_v2.engine import review_contract_v2
from review_v2.priority_contract_types import PRIORITY_TYPES
from review_v2.contract_registry import get_checklist
from priority_contract_fixtures import NORMAL, MISSING, RISKY


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/priority_contract_acceptance")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    summary = []
    for key, meta in PRIORITY_TYPES.items():
        for variant, contracts in (("normal", NORMAL), ("missing", MISSING), ("risky", RISKY)):
            source = contracts[key]
            result = review_contract_v2(source, key, use_llm=False)
            (args.output / f"{key}_{variant}.txt").write_text(source, encoding="utf-8")
            (args.output / f"{key}_{variant}.md").write_text(result.get("result", ""), encoding="utf-8")
            summary.append({
                "type": key, "name": meta.name, "variant": variant,
                "classified_type": result.get("contract_type"),
                "checklist_count": len(get_checklist(key)),
                "coverage": result.get("coverage_summary"),
                "risk_theme_count": result.get("risk_theme_count"),
                "release_quality_gate": result.get("release_quality_gate", {}).get("status"),
                "failures": result.get("release_quality_gate", {}).get("failures", []),
            })
    (args.output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    failed = [row for row in summary if row["release_quality_gate"] != "REPORT_READY" or row["classified_type"] != row["type"]]
    print(f"{len(summary)} contracts; {len(failed)} failures; output: {args.output.resolve()}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
