"""References from rule elements to the immutable contract fact registry."""
import re


def compact(value):
    return re.sub(r"\s+|[。；;]$", "", str(value or ""))


def bind(items, graph):
    facts = graph.matching(["liability.penalty"])
    for item in items:
        for element in item.coverage_elements:
            requirement = str(element.get("required_fact") or element.get("proposition") or "")
            if not re.search(r"违约金|违约后果|违约责任", requirement):
                continue
            proofs = element.get("supporting_evidence") or []
            refs = []
            for fact in facts:
                raw = compact(fact.value["raw_clause"])
                # A missing consumer has no evidence spans; retain its semantic
                # dependency so the gate can detect positive-vs-missing drift.
                if (element.get("element_id") == "development_delay_liability"
                        and fact.value["trigger"] in {"迟延交付", "逾期交付", "延期交付", "延迟交付"}):
                    refs.append(fact.fact_id)
                    continue
                if any(p.get("clause_id") in fact.source_clause_ids and p.get("quote")
                       and (compact(p["quote"]) in raw or raw in compact(p["quote"]))
                       and fact.value["rate"] in p["quote"] for p in proofs):
                    refs.append(fact.fact_id)
            if refs:
                element["canonical_fact_keys"] = refs
                if len(refs) == 1:
                    element["source_fact_key"] = refs[0]
                    # Re-key both ends of the existing exact binding together.
                    # Renaming only the element leaves the verifier looking up
                    # its validated source under the obsolete local fact key.
                    fact = next(f for f in facts if f.fact_id == refs[0])
                    direct = [p for p in proofs if p.get('clause_id') in fact.source_clause_ids
                              and p.get('quote') and compact(p['quote']) in compact(fact.value['raw_clause'])]
                    if direct:
                        if not hasattr(item, 'decision_trace'):
                            item.decision_trace = {}
                        item.decision_trace.setdefault('direct_fact_bindings', {})[refs[0]] = direct
                        item.decision_trace.setdefault('direct_element_fact_keys', {})[element['element_id']] = refs[0]


def gate(items, findings, graph):
    failures = []
    facts = {fact.fact_id: fact for fact in graph.matching(["liability.penalty"])}
    observations = {}
    for item in items:
        rows = [row for finding in findings if item.item_id in finding.source_review_ids
                for row in (finding.evidence_bundle or {}).get("items", [])]
        if not any(item.item_id in finding.source_review_ids for finding in findings):
            rows = item.evidence_clauses
        for element in item.coverage_elements:
            for fact_id in element.get("canonical_fact_keys") or []:
                if fact_id not in facts:
                    if str(fact_id).startswith("f_penalty_"):
                        failures.append({"rule_id": item.item_id, "fact_id": fact_id,
                                         "element_key": element["element_id"], "expected_evidence": "registry fact",
                                         "actual_evidence": [], "reject_reason": "UNKNOWN_CANONICAL_FACT_ID"})
                    continue
                observations.setdefault(fact_id, []).append((item.item_id, element.get("status")))
                if element.get("status") not in {"COVERED", "ADVERSE", "CONFLICTING", "PARTIALLY_COVERED"}:
                    continue
                fact = facts[fact_id]
                for slot in element.get('fact_elements', []):
                    if slot.get('value') != fact.value.get(slot.get('element_key')):
                        failures.append({'rule_id': item.item_id, 'fact_id': fact_id,
                                         'element_key': slot.get('element_key'),
                                         'expected_evidence': fact.source_spans,
                                         'actual_evidence': slot.get('bound_evidence_ids', []),
                                         'reject_reason': 'SOURCE_SLOT_DIFFERS_FROM_CANONICAL_FACT'})
                actual = [row for row in rows if row.get("source_fact_key") == fact_id
                          and element["element_id"] in (row.get("supporting_element_ids") or [])
                          and item.item_id in (row.get("supporting_review_ids") or [])
                          and row.get("source_type") == "BODY"
                          and compact(row.get("quoted_text")) == compact(fact.value["raw_clause"])]
                if not actual:
                    failures.append({"rule_id": item.item_id, "fact_id": fact_id,
                                     "element_key": element["element_id"],
                                     "expected_evidence": fact.source_spans,
                                     "actual_evidence": [r.get("evidence_id") for r in rows if r.get("source_fact_key") == fact_id],
                                     "reject_reason": "CANONICAL_FACT_WITHOUT_EXACT_REPORT_BINDING"})
    conflicts = []
    for fact_id, observations_for_fact in observations.items():
        positive = [rule for rule, status in observations_for_fact if status in {"COVERED", "ADVERSE", "CONFLICTING"}]
        missing = [rule for rule, status in observations_for_fact if status == "MISSING"]
        if positive and missing:
            conflicts.append({"fact_id": fact_id, "covered_rule_ids": positive, "missing_rule_ids": missing,
                              "reject_reason": "CROSS_RULE_FACT_CONFLICT"})
    return {"status": "BLOCKED" if failures or conflicts else "PASS",
            "failures": failures + conflicts, "risk_fact_direct_evidence_mismatch": len(failures),
            "cross_rule_fact_conflict": len(conflicts),
            "gate_results": {"CANONICAL_PENALTY_BINDING": "FAIL" if failures or conflicts else "PASS"}}
