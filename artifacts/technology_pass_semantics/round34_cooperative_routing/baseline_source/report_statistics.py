"""Audit every summary against its published detail collection."""
from collections import Counter
import re


COVERAGE_BUCKETS = ("通过", "部分覆盖", "缺失", "风险条款", "不适用", "待核验", "法律提示")


def _value(row, key, default=None):
    return row.get(key, default) if isinstance(row, dict) else getattr(row, key, default)


def requires_verification(row):
    if _value(row, 'coverage_status') == '不适用':
        return False
    return bool(_value(row, 'needs_manual_review', False)
        or is_pending_verification(_value(row, 'coverage_status'))
        or any(e.get('status') in {'CONDITION_UNRESOLVED', 'PENDING_VERIFICATION'}
               for e in _value(row, 'coverage_elements', []) or []))


def report_status(row):
    status = _value(row, 'coverage_status')
    return '待核验' if status == '通过' and requires_verification(row) else coverage_bucket(status)


def coverage_bucket(status):
    """Reporting projection only: never mutate the rule's legal decision."""
    return "待核验" if status == "INSUFFICIENT_CONTEXT" else status


def coverage_counts(rows):
    return dict(Counter(report_status(r) for r in rows))


def is_pending_verification(status):
    return coverage_bucket(status) == "待核验"


def statistics_gate(report):
    rows = report.get("all_rule_statuses") or report.get("items", [])
    failures = []

    def check(ok, requirement, reason):
        if not ok:
            failures.append({"requirement": requirement, "failure_stage": "Final Summary Projection",
                             "root_cause": reason, "current_status": "FAIL"})

    coverage = coverage_counts(rows)
    check(set(coverage) <= set(COVERAGE_BUCKETS) and sum(coverage.get(k, 0) for k in COVERAGE_BUCKETS) == len(rows),
          "COVERAGE_BUCKET_TOTAL_CLOSURE", "七类覆盖状态之和必须等于全部审查项，未知状态不得遗漏。")
    check(coverage == {k: v for k, v in report.get("coverage_summary", {}).items() if v},
          "COVERAGE_STATISTICS_CLOSURE", "覆盖统计不能从全部规则状态反算。")
    check(len(rows) == report.get("all_items_count") == len({r["item_id"] for r in rows}),
          "RULE_COUNT_CLOSURE", "审查规则总数或唯一规则数不闭合。")
    expected_levels = {level: sum(r.get("risk_level") == level and r.get("coverage_status") != "不适用" for r in rows) for level in ("高", "中", "低")}
    check(report.get("summary") == expected_levels, "RULE_SEVERITY_CLOSURE", "规则风险统计与明细不一致。")
    manual = report.get("manual_review_items", [])
    manual_sources = {key for r in manual for key in r.get("source_rules", [r.get("item_id")])}
    check(not any(r.get('coverage_status') == '通过' and (requires_verification(r) or r['item_id'] in manual_sources) for r in rows),
          'MANUAL_REVIEW_PASS_CONTRADICTION', '待人工核验的审查项不得显示完全通过。')
    by_id = {r['item_id']: r for r in rows}
    check(all(r.get('coverage_status') == by_id.get(r['item_id'], {}).get('coverage_status') for r in report.get('items', [])),
          'DETAIL_STATUS_CLOSURE', '显示明细状态必须与统计的规则状态一致。')
    expected_manual_sources = {r["item_id"] for r in rows if r.get("needs_manual_review") or is_pending_verification(r.get("coverage_status"))}
    check(expected_manual_sources <= manual_sources, "PENDING_VERIFICATION_COUNT", "待核验或需人工复核的规则未计入人工复核明细。")
    counts = [report.get("manual_review_summary", {}).get("manual_review_count"),
              report.get("final_overview_summary", {}).get("manual_review"),
              report.get("risk_finding_summary", {}).get("人工复核")]
    check(all(c == len(manual) for c in counts), "MANUAL_REVIEW_COUNT_CLOSURE", "人工复核顶部数量与复核明细不一致。")
    findings = report.get("risk_findings", [])
    themes = report.get('risk_themes', [])
    aggregated = any(t.get('underlying_finding_count', 1) > 1 for t in themes)
    if aggregated:
        finding_by_id = {f['finding_id']: f for f in findings}
        members = [key for t in themes for key in t.get('member_finding_ids', [])]
        check(len(members) == len(set(members)) and set(members) == set(finding_by_id),
              'THEME_MEMBER_CLOSURE', '主题必须完整且不重复地保留全部规则级命中。')
        check(len(themes) == report.get('risk_theme_count'), 'THEME_COUNT_CLOSURE', '风险主题数与最终主题列表不一致。')
        for theme in themes:
            source = [finding_by_id[k] for k in theme.get('member_finding_ids', []) if k in finding_by_id]
            if not source:
                continue
            levels = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
            priorities = {'A_CORE': 0, 'B_PRACTICAL': 1, 'C_OPTIMIZATION': 2}
            check(theme.get('severity') == min((f['severity'] for f in source), key=lambda k: levels.get(k, 9)),
                  'THEME_MAX_SEVERITY', '聚合主题未保留成员最高风险等级。')
            check(theme.get('priority') == min((f['priority'] for f in source), key=lambda k: priorities.get(k, 9)),
                  'THEME_MAX_PRIORITY', '聚合主题未保留成员最高优先级。')
    overview = report.get("final_overview_summary", {})
    for label, key, levels in (("重大风险", "major_risk", {"HIGH", "CRITICAL"}), ("中等风险", "medium_risk", {"MEDIUM"}), ("低风险", "low_risk", {"LOW"})):
        expected = sum(f.get("severity") in levels for f in findings)
        visible_expected = sum(t.get('severity') in levels for t in themes) if aggregated else expected
        check(report.get("risk_finding_summary", {}).get(label) == expected and overview.get(key) == visible_expected,
              "FINDING_COUNT_CLOSURE", label + "未按风险明细统计。")
    if "final_dispositions" in report:
        dispositions = report["final_dispositions"]
        for action, summary_key, overview_key in (("MUST_CHANGE", "must_change", "priority_action"),
                                                  ("SHOULD_CHANGE", "should_change", "recommended_action"),
                                                  ("OPTIONAL_IMPROVEMENT", "optional_improvement", "optional_action")):
            expected = sum(d.get("final_action") == action for d in dispositions)
            visible_expected = sum(t.get('final_action') == action for t in themes) if aggregated else expected
            check(overview.get(overview_key) == visible_expected and expected == report.get("final_disposition_summary", {}).get(summary_key),
                  "ACTION_COUNT_CLOSURE", "行动数量与处置明细不一致。")
    markdown = report.get("result", "")
    if markdown and "### 审查覆盖统计" in markdown:
        section = markdown.split("### 审查覆盖统计", 1)[1].split("\n## ", 1)[0]
        for status, count in coverage.items():
            label = "已覆盖" if status == "通过" else "规则级风险命中" if status == "风险条款" else status
            check(bool(re.search(rf"- {re.escape(label)}：{count} 项(?:\n|$)", section)),
                  "RENDERED_COVERAGE_CLOSURE", f"报告缺少或错误统计{label}。")
        check(f"- 人工复核项：{len(manual)}" in markdown, "RENDERED_MANUAL_COUNT", "报告人工复核数量与明细不一致。")
        check(f"- 审查项总计：{len(rows)} 项" in section, "RENDERED_TOTAL_COUNT", "报告状态总计不闭合。")
    return {"status": "BLOCKED" if failures else "REPORT_READY", "failures": failures,
            "rule_count": len(rows), "coverage_counts": coverage, "manual_review_count": len(manual),
            "manual_review_rule_ids": sorted(manual_sources)}
