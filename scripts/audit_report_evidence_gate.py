"""Run the actual non-mutating gate on a serialized production review."""
import argparse
import json
from pathlib import Path
from types import SimpleNamespace

from review_v2.narrative_evidence import narrative_evidence_gate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--rule")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    items = [SimpleNamespace(**i) for i in report["items"]]
    findings = [SimpleNamespace(**f) for f in report["risk_findings"]
                if not args.rule or args.rule in f["source_review_ids"]]
    result = narrative_evidence_gate(items, findings)
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
