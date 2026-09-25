"""Final, non-mutating checks of material narrative facts against report evidence.

The checker never retrieves extra contract text to rescue a report: only the
element's published source or an explicitly published calculation can support it.
Role, object, polarity and amounts remain part of the assertion.
"""
import re
from decimal import Decimal


def normalized(text):
    value = re.sub(r"\s+", "", str(text or ""))
    value = re.sub(r"被许可(?:方|人)|受让(?:方|人)|买方", "受让方", value)
    value = re.sub(r"(?<!被)许可(?:方|人)|让与(?:方|人)|转让方|出让方|卖方", "让与方", value)
    value = re.sub(r"(?<=\d),(?=\d{3}(?:\D|$))", "", value)
    value = re.sub(r"([\d,.]+)万元", lambda m: str(Decimal(m[1].replace(',', '')) * 10000) + "元", value)
    return value


def material_assertions(text):
    """Independent factual slots, not legal possibilities or recommendations."""
    value = normalized(text)
    assertions = []
    # Separate coordinated identity/attribution assertions: listing a person
    # does not grant, exercise or record that person's attribution right.
    for part in re.split(r"[。；;，,]", value):
        if re.search(r"未|缺少|需核验|应当|建议|若|如果", part):
            continue
        for kind, pattern in (
            ("creator_identity", r"(?:发明人|设计人|完成人).{0,12}(?:姓名|名单)|(?:姓名|名单).{0,12}(?:已列明|已明确)"),
            ("creator_attribution", r"署名.{0,18}(?:已|明确|记载|覆盖)|(?:已|明确).{0,18}署名"),
        ):
            if re.search(pattern, part):
                assertions.append({"kind": kind, "text": part})
    for match in re.finditer(r"(受让方|让与方)[^。；，]{0,90}?保密期限(?:仅为|仅限|为|：)[^。；，]*合同有效期内", value):
        assertions.append({"kind": "confidentiality_period", "text": match[0], "actor": match[1],
                           "limited": bool(re.search(r"仅为|仅限", match[0]))})
    for match in re.finditer(r"(?:违反|违背)([^，。；]{1,45}?(?:义务|约定))(?:时|的)?[，,]?[^。；]{0,35}?(\d+(?:\.\d+)?)元违约金", value):
        objects = [term for term in re.split(r"、|或|及|和", re.sub(r"(?:义务|约定)$", "", match[1])) if term]
        prefix = re.split(r"[。；]", value[:match.start()])[-1]
        actors = re.findall(r"受让方|让与方", prefix)
        assertions.append({"kind": "penalty_trigger", "text": match[0], "objects": objects,
                           "actor": actors[-1] if actors else "", "amount": Decimal(match[2])})
    for match in re.finditer(r"(?:每日|每天|每逾期一日)(\d+(?:\.\d+)?)%", value):
        assertions.append({"kind": "daily_penalty", "text": match[0], "rate": Decimal(match[1])})
    for match in re.finditer(r"(有效期限起始日|履行义务|履行开始日期|履行起始日)早于(?:合同)?(生效日|签署日|签订日期)", value):
        assertions.append({"kind": "date_order", "text": match[0],
                           "start_type": "validity_start_date" if match[1] == "有效期限起始日" else "performance_start_date",
                           "end_type": "contract_effective_date" if match[2] == "生效日" else "contract_signing_date"})
    return assertions


def assertion_supported(assertion, quotes):
    sources = [normalized(quote) for quote in quotes]
    if assertion["kind"] == "creator_identity":
        return any(re.search(r"(?:发明人|设计人|完成人)(?:姓名)?[：:]?[^。；]{1,50}", source) for source in sources)
    if assertion["kind"] == "creator_attribution":
        return any("署名" in source and not re.search(r"未.{0,8}署名|没有.{0,8}署名", source) for source in sources)
    if assertion["kind"] == "daily_penalty":
        return any(re.search(r"每日|每天|每逾期一日", source)
                   and any(Decimal(m[1]) == assertion["rate"] for m in re.finditer(r"(\d+(?:\.\d+)?)%", source))
                   for source in sources)
    if assertion["kind"] == "date_order":
        return False  # Date relations require typed calculation inputs below.
    if assertion["kind"] == "penalty_trigger":
        return any(all(term in source for term in assertion["objects"])
                   and (not assertion["actor"] or assertion["actor"] in source)
                   and any(Decimal(m[1]) == assertion["amount"] for m in re.finditer(r"(\d+(?:\.\d+)?)元", source))
                   and "违约金" in source for source in sources)
    # A party heading may be a separate, explicitly bound source. Never inherit
    # the actor from an unrelated element or another finding's evidence.
    return (any(assertion["actor"] in source for source in sources)
            and any("保密期限" in source and "合同有效期内" in source
                    and (not assertion["limited"] or "仅限" in source or "仅为" in source
                         or re.search(r"保密期限为(?:本)?合同有效期内[。；]?$", source))
                    for source in sources))


def narrative_evidence_gate(items, findings, report=None):
    failures, claims = [], []
    for finding in findings:
        sources = list((finding.evidence_bundle or {}).get("items") or [])
        reviews = [item for item in items if item.item_id in finding.source_review_ids]
        bindings = []
        for item in reviews:
            for element in item.coverage_elements:
                if element.get("status") not in {"COVERED", "PARTIALLY_COVERED", "ADVERSE", "CONFLICTING"}:
                    continue
                declared_ids = set(element.get("evidence_ids") or element.get("bound_evidence_ids") or [])
                rows = [row for row in sources if (
                        element["element_id"] in row.get("supporting_element_ids", [])
                        and item.item_id in row.get("supporting_review_ids", [])
                        or not element.get("supporting_evidence") and
                        (row.get("evidence_id") in declared_ids or row.get("clause_id") in declared_ids))
                        and row.get("source_type") != "SEARCH_AUDIT" and row.get("quoted_text")]
                claims.append({"risk_id": finding.finding_id, "field": "element_proposition",
                               "fact": element.get("proposition", ""), "element_ids": [element["element_id"]],
                               "supporting_evidence_ids": [row.get("evidence_id") for row in rows if row.get("evidence_id")]})
                if not rows and not element.get("internal_meta"):
                    failures.append({"risk_id": finding.finding_id, "element_id": element["element_id"],
                                     "reason": "FACT_ELEMENT_WITHOUT_PUBLISHED_BINDING"})
                if element.get("supporting_evidence") is not None:
                    for fact in element["supporting_evidence"]:
                        if not any(row.get("clause_id") == fact.get("clause_id")
                                   and normalized(row["quoted_text"]) == normalized(fact.get("quote")) for row in rows):
                            failures.append({"risk_id": finding.finding_id, "element_id": element["element_id"],
                                             "reason": "ELEMENT_SOURCE_NOT_PUBLISHED"})
                    if not rows:
                        failures.append({"risk_id": finding.finding_id, "element_id": element["element_id"],
                                         "reason": "ELEMENT_WITHOUT_SUPPORTING_EVIDENCE"})
                bindings.append((element, rows))
                # An element may contain multiple propositions. Validate each
                # recognized predicate against this element's own binding,
                # never against another predicate's successful validation.
                for assertion in material_assertions(element.get("proposition", "")):
                    if assertion["kind"] == "date_order":
                        continue  # Checked with typed calculation inputs below.
                    direct = [row for row in rows if assertion_supported(assertion, [row["quoted_text"]])]
                    supported = bool(direct) or assertion_supported(assertion, [row["quoted_text"] for row in rows])
                    claims.append({"risk_id": finding.finding_id, "field": "atomic_element_proposition",
                                   "fact": assertion["text"], "predicate": assertion["kind"],
                                   "element_ids": [element["element_id"]],
                                   "supporting_evidence_ids": [row.get("evidence_id") for row in (direct or rows) if supported]})
                    if not supported:
                        failures.append({"risk_id": finding.finding_id, "element_id": element["element_id"],
                                         "fact": assertion["text"], "reason": "ATOMIC_FACT_WITHOUT_SUPPORTING_EVIDENCE"})
        narratives = [("risk_description", finding.issue)]
        for item in reviews:
            narratives.extend((("risk_point_description", item.risk_point_description),
                               ("review_judgment", item.reasoning_summary),
                               ("narrative_judgment", (item.narrative_state or {}).get("judgment", ""))))
        for field, text in narratives:
            for assertion in material_assertions(text):
                supporting = [(element, rows) for element, rows in bindings
                              if assertion_supported(assertion, [row["quoted_text"] for row in rows])]
                if assertion["kind"] == "date_order":
                    supporting = [(element, rows) for element, rows in bindings
                                  if {assertion["start_type"], assertion["end_type"], "calculation_result"}
                                  <= {kind for row in rows for kind in row.get("fact_types") or [row.get("fact_type")]}]
                claims.append({"risk_id": finding.finding_id, "field": field, "fact": assertion["text"],
                               "element_ids": [element["element_id"] for element, _ in supporting],
                               "supporting_evidence_ids": list(dict.fromkeys(row.get("evidence_id")
                                   for _, rows in supporting for row in rows if row.get("evidence_id")))})
                if not supporting:
                    failures.append({"risk_id": finding.finding_id, "field": field,
                                     "fact": assertion["text"], "reason": "NARRATIVE_FACT_WITHOUT_ELEMENT_EVIDENCE"})
    if report is not None:
        # Renderers may serialize the validated facts, but cannot add another
        # independent assertion (even one outside the specialized slot lexicon).
        def units(text):
            return {part.strip("：:、，, ") for part in re.split(r"[。；;\n]", normalized(text)) if part.strip("：:、，, ")}
        canonical = set()
        for item in items:
            for value in (item.risk_point_description, item.reasoning_summary,
                          (item.narrative_state or {}).get("judgment", ""),
                          (item.narrative_state or {}).get("issue", "")):
                canonical.update(units(value))
        for finding in findings:
            canonical.update(units(finding.issue))
        for line in report.splitlines():
            match = re.match(r"- (?:风险说明|审查判断|【风险点描述】)：(.+)", line)
            if not match:
                continue
            for unit in units(match[1]):
                if unit not in canonical:
                    failures.append({"field": "rendered_risk_narrative", "fact": unit,
                                     "reason": "RENDERER_ADDED_UNREGISTERED_FACT"})
    return {"status": "BLOCKED" if failures else "REPORT_READY", "claims": claims,
            "failures": [{"requirement": "NARRATIVE_EVIDENCE_GATE", "failure_stage": "Narrative Evidence Validation",
                          "root_cause": "风险事实未绑定直接支持该事实的要素级报告证据。", "details": failures}] if failures else [],
            "gate_results": {"NARRATIVE_EVIDENCE_GATE": "FAIL" if failures else "PASS"}}
