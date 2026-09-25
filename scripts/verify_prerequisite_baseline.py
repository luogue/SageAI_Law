"""Compare unrelated technology results with this turn's engine hooks removed.

The baseline is compiled in memory only: no worktree edits or gate bypass in
the running service. This diagnoses pre-existing failures in a dirty worktree.
"""
from pathlib import Path
import json
from layers.input_layer import InputLayer
from review_v2 import engine
from review_v2.user_profile import UserRiskProfile


def snapshot():
    path = next(Path("test_data").glob("46*.docx"))
    text = InputLayer()._extract_from_docx_content(path.read_bytes())
    output = engine.review_contract_v2(text, "technology", use_llm=False,
                                     profile=UserRiskProfile(user_identity="甲方/被许可方"))
    return dict(statuses={i["item_id"]: i["coverage_status"] for i in output["items"]},
                gate=output["release_quality_gate"]["status"],
                failures=output["release_quality_gate"]["failures"])


current = snapshot()
source = Path(engine.__file__).read_text(encoding="utf-8-sig")
def cut(start, end):
    global source
    begin = source.index(start)
    finish = source.index(end, begin)
    source = source[:begin] + source[finish:]
cut("    from review_v2.prerequisite_resolution import resolve_prerequisites\n", "    for checkpoint in checklist:\n")
cut("        predicate_gate = resolve_prerequisites(checkpoint, prerequisite_facts)\n", "        # Runtime scenario gates")
cut("    from review_v2.prerequisite_resolution import prerequisite_status_failures\n", '    if type_meta.key.value == "guarantee":\n')
source = source.replace('if is_applicable and (fact_applicability.get("applicable") is False or\n                              str(fact_applicability.get("status", "")).upper() in {"UNCERTAIN", INSUFFICIENT_CONTEXT, "CONDITION_UNRESOLVED"}):',
                        'if is_applicable and fact_applicability.get("applicable") is False:')
source = source.replace('{"UNCERTAIN", INSUFFICIENT_CONTEXT, "CONDITION_UNRESOLVED"}', '{"UNCERTAIN", INSUFFICIENT_CONTEXT}')
source = source.replace('"user_reason": uncertainty_reason,', '"user_reason": "现有合同材料不足以确认该事项是否适用，建议结合相关交易背景或补充材料核对。",')
exec(compile(source, engine.__file__, "exec"), engine.__dict__)
baseline = snapshot()
same = baseline == current
Path("artifacts/prerequisite_baseline_comparison.json").write_text(
    json.dumps(dict(identical=same, baseline=baseline, current=current), ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(dict(identical=same, baseline_gate=baseline["gate"], current_gate=current["gate"],
                     baseline_failures=len(baseline["failures"]), current_failures=len(current["failures"])), ensure_ascii=False))
assert same, "New engine hooks changed the unrelated technology result"
