"""从 Round46 真实接口报告提取 target TC 状态（验证真实链路修复生效）。"""
import io
import json
from pathlib import Path

ROOT = Path(r"F:/ai/Sage")
OUT = ROOT / "artifacts" / "technology_pass_semantics" / "round46_consulting_generalization"
REPORT = ROOT / "scripts" / "_tmp_extract_round46_real.out.txt"

TARGETS = ["TC-01-03", "TC-08-01", "TC-08-02", "TC-08-03", "TC-08-04",
           "TC-11-01", "TC-11-02", "TC-11-03", "TC-11-04", "TC-12-02"]

buf = io.StringIO()


def w(s=""):
    buf.write(s + "\n")


for slug, label in (("final_party_a", "甲方"), ("final_party_b", "乙方")):
    p = OUT / slug / "report.json"
    if not p.exists():
        w(f"{label}: 无报告")
        continue
    data = json.loads(p.read_text(encoding="utf-8"))
    w("=" * 66)
    w(f"{label}  run={data.get('review_run_id')}  gate={data.get('release_quality_gate',{}).get('status')}")
    w("=" * 66)
    for item in data.get("items", []):
        iid = item.get("item_id")
        if iid not in TARGETS:
            continue
        covered = {r["element_id"] for r in item.get("coverage_elements", [])
                   if r.get("status") == "COVERED"}
        missing = {r["element_id"] for r in
                   (item.get("decision_trace", {}) or {}).get("element_absence_searches", [])
                   if r.get("result") == "NOT_FOUND"}
        conflict = covered & missing
        w(f"  [{iid}] {item.get('status')}")
        w(f"     COVERED={sorted(covered)}")
        if conflict:
            w(f"     *** 假MISSING冲突={sorted(conflict)}")
        else:
            w(f"     无假MISSING冲突")
    gf = data.get("release_quality_gate", {}).get("failures") or []
    w(f"\n  gate failures({len(gf)}):")
    for f in gf:
        req = f.get("requirement")
        if req == "NARRATIVE_EVIDENCE_GATE":
            det = f.get("details") or []
            w(f"     - {req}: {[d.get('element_id') for d in det]}")
        else:
            w(f"     - {req}: {f.get('root_cause','')[:80]}")
    w("")

REPORT.write_text(buf.getvalue(), encoding="utf-8")
print("written", REPORT)
