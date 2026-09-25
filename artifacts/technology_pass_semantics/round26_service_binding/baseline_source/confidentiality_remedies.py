"""Direct, party-scoped confidentiality remedies; money is not a penalty.

Keep the existing rule's element IDs, but retain each obligated party's own
atomic status and quote. A clause for one party never completes the other.
"""
import re

from review_v2.requirement_keys import canonical_requirement_key
from review_v2.technology_fact_ontology import CONFIDENTIALITY_BREACH, has_confidentiality_remedy


PARTIES = r"被许可方|许可方|受让方|让与方|出让方|转让方|买方|卖方|甲方|乙方|丙方"
COLLECTIVE = r"任何一方|任一方|违约方|责任方|泄密方|泄露方|双方|各方|(?<!另)一方"
REMEDIES = {
    "breach_damage_liability": ("泄密损失赔偿责任", r"赔偿|损失赔偿责任"),
    "stop_disclosure": ("泄密后停止披露", r"停止[^。；]{0,14}(?:披露|泄露)"),
    "stop_use": ("泄密后停止使用", r"停止[^。；]{0,14}使用|限制未经授权的?使用"),
    "mitigation_obligation": ("泄密后采取措施防止继续扩散或损失扩大", r"防止[^。；]{0,16}(?:扩大|扩散|泄露)|采取[^。；]{0,12}(?:补救|合理措施)"),
    "incident_notification": ("泄密后及时通知受影响方", r"(?:通知|告知)[^。；]{0,20}(?:对方|另一方|受影响方|买方|卖方|甲方|乙方|许可方|被许可方)"),
    "specific_confidentiality_penalty": ("泄密专项违约金", r"(?:支付|承担|赔付)[^。；]{0,35}违约金|违约金(?:为|金额|：|:)"),
    "excess_loss_compensation": ("泄密违约金不足部分的继续赔偿", r"(?:不足|超过|超出)[^。；]{0,25}(?:继续赔偿|赔偿|补足)|继续赔偿[^。；]{0,20}(?:不足|超过)"),
}
OPTIONAL_REMEDIES = {"specific_confidentiality_penalty", "excess_loss_compensation"}


def canonical_confidentiality_remedies(clauses):
    """The registry and all rule/verifier consumers use this same event scope."""
    return confidentiality_remedy_elements([c for c in clauses if has_confidentiality_remedy(c.text)])


def confidentiality_remedy_elements(clauses):
    records = []
    parties = []
    context_party = ""
    for clause in clauses:
        # A breach sentence does not turn the entire mixed liability article
        # into confidentiality remedies (nor transfer one actor's trigger).
        title = str(getattr(clause, 'title', '') or clause.text.splitlines()[0])
        liability_context = bool(re.fullmatch(r"(?:第.{1,8}条\s*)?(?:泄密责任|泄密处理|泄露处理|泄漏处理|保密违约责任|保密违约)", title.strip()))
        preceding_penalty = None
        for line in clause.text.splitlines():
            text = re.sub(r"^\s*\d+[．.、]\s*", "", line).strip()
            heading = re.fullmatch(f"({PARTIES})(?:义务|责任)?[：:]?", text)
            if heading:
                context_party = heading[1]
                if context_party not in parties:
                    parties.append(context_party)
                continue
            if not text:
                continue
            # Breach of an implementation/transfer boundary is not itself a
            # confidentiality breach. Match the breached obligation, not a
            # later mention of the transferred technical secret.
            # A carve-out from a general cap does not impose a secrecy remedy.
            if re.search(r'^除.{0,90}(?:保密|泄密).{0,10}(?:外|之外)', text):
                continue
            breach = bool(re.search(CONFIDENTIALITY_BREACH, text))
            # An immediately following excess-loss remedy refers to the
            # preceding scoped penalty, not to every liability in the article.
            # Retain the actual contiguous source (including its newline).
            if (not breach and preceding_penalty and re.search(REMEDIES['excess_loss_compensation'][1], text)
                    and '违约金' in text):
                prior_actor, prior_start = preceding_penalty
                end = clause.text.find(line, prior_start) + len(line)
                records.append((prior_actor, bool(re.fullmatch(COLLECTIVE, prior_actor)),
                                clause.clause_id, clause.text[prior_start:end].strip()))
                preceding_penalty = None
                continue
            preceding_penalty = None
            if not (breach or liability_context):
                continue
            subjects = [match for match in re.finditer(
                # A recipient introduced by 向/给/对 is an object, not a new
                # operative subject. Filter whole role tokens so 被许可方
                # cannot be retried as the shorter 许可方 after rejection.
                f"({PARTIES}|{COLLECTIVE})(?=发现|故意|重大过失|未经|违反|违背|泄|擅自|应|须|不得|在|未履行|支付|承担|赔偿|负责|向)", text,
            ) if not match.start() or text[match.start() - 1] not in '向给对']
            # A paragraph can contain multiple actors. Bind only the span up
            # to the next operative subject, never the whole shared paragraph.
            # Keep the conditional prefix before a collective obligor: removing
            # “因违反保密义务…” would leave only an unscoped penalty sentence.
            spans = [(match[1], text[0 if i == 0 and breach else match.start():subjects[i + 1].start() if i + 1 < len(subjects) else len(text)])
                     for i, match in enumerate(subjects)] if subjects else [(context_party, text)]
            for actor, quote in spans:
                if not actor or not any(re.search(pattern, quote) for _, pattern in REMEDIES.values()):
                    continue
                collective = bool(re.fullmatch(COLLECTIVE, actor))
                if not collective and actor not in parties:
                    parties.append(actor)
                if liability_context and not breach:
                    # A following incident duty inherits the explicit secrecy
                    # article scope. Keep that scope inside the exact quote so
                    # every consumer can independently re-evaluate it.
                    end = clause.text.find(line) + len(line)
                    quote = clause.text[:end].strip()
                records.append((actor, collective, clause.clause_id, quote.strip()))
                if breach and re.search(REMEDIES['specific_confidentiality_penalty'][1], quote):
                    preceding_penalty = (actor, clause.text.find(quote))
    if not parties:
        parties = ["责任方"]
    elements = []
    for key, (label, pattern) in REMEDIES.items():
        party_rows = []
        facts = []
        for party in parties:
            matches = []
            for actor, collective, clause_id, text in records:
                if not (actor == party or collective) or not re.search(pattern, text):
                    continue
                # Neither negated remedies nor compensation alone prove a penalty.
                if key in OPTIONAL_REMEDIES and (
                    "违约金" not in text or re.search(r"(?:不|无需|未约定|无须)[^，；。]{0,8}违约金", text)
                ):
                    continue
                if re.search(r"(?:不承担|无需赔偿|不予赔偿|免除赔偿)", text) and key == "breach_damage_liability":
                    continue
                matches.append({"clause_id": clause_id, "quote": text, "obligated_party": party,
                                "proposition": party + label + "已有约定。"})
            status = "COVERED" if matches else "NOT_APPLICABLE" if key in OPTIONAL_REMEDIES else "MISSING"
            party_rows.append({
                "obligated_party": party, "status": status, "supporting_evidence": matches,
                "required_fact": party + label,
                "proposition": party + label + ("已有约定。" if matches else ""),
            })
            facts.extend(matches)
        covered = [r["obligated_party"] for r in party_rows if r["status"] == "COVERED"]
        absent = [r["obligated_party"] for r in party_rows if r["status"] == "MISSING"]
        status = "PARTIALLY_COVERED" if covered and absent else "COVERED" if covered else "MISSING" if absent else "NOT_APPLICABLE"
        required = "、".join(p + label for p in absent) if absent else label
        elements.append({
            "element_id": key, "status": status,
            "proposition": "；".join(p + label + "已有约定" for p in covered) + "。" if covered else label,
            "required_fact": required, "residual_gap": required if absent else "",
            "search_targets": [p + label for p in absent],
            "recommendation_action": "明确" + required if absent else "",
            "bound_evidence_ids": list(dict.fromkeys(f["clause_id"] for f in facts)),
            "supporting_evidence": facts, "party_coverage": party_rows,
            "source_fact_key": "confidentiality." + key,
            "risk_relevant": key not in OPTIONAL_REMEDIES and (key != "breach_damage_liability" or bool(covered)),
        })
    return elements


def confidentiality_binding_failures(elements):
    failures = []
    for row in elements:
        if "party_coverage" not in row:
            continue
        if canonical_requirement_key(row.get("element_id")) not in REMEDIES:
            # Party-scoped periods and information scope use their own
            # extractor. A shared metadata shape is not remedy applicability.
            continue
        if row["status"] == "COVERED" and any(p["status"] == "MISSING" for p in row["party_coverage"]):
            failures.append({"element_id": row["element_id"], "reason": "PARTY_GAP_LOST_IN_COVERAGE"})
        source = " ".join(f["quote"] for f in row.get("supporting_evidence", []))
        if "违约金" in row.get("proposition", "") and row["status"] in {"COVERED", "PARTIALLY_COVERED"} and "违约金" not in source:
            failures.append({"element_id": row["element_id"], "reason": "PENALTY_NARRATIVE_WITHOUT_PENALTY_EVIDENCE"})
        for party in row["party_coverage"]:
            if party.get("supporting_evidence") and party["status"] not in {"COVERED", "ADVERSE", "CONFLICTING"}:
                failures.append({"element_id": row["element_id"], "obligated_party": party["obligated_party"],
                                 "reason": "PARTY_POSITIVE_EVIDENCE_LOST"})
            if party["status"] != "COVERED":
                continue
            facts = party.get("supporting_evidence", [])
            if not facts or any(f.get("obligated_party") != party["obligated_party"] for f in facts):
                failures.append({"element_id": row["element_id"], "reason": "OBLIGATED_PARTY_EVIDENCE_MISMATCH"})
            # Re-run the same field/actor extractor on the exact source quotes.
            from types import SimpleNamespace
            checked = confidentiality_remedy_elements([
                SimpleNamespace(clause_id=f["clause_id"], text=f["quote"]) for f in facts
            ])
            atomic = next((e for e in checked if canonical_requirement_key(e["element_id"]) ==
                           canonical_requirement_key(row["element_id"])), None)
            if atomic is None:
                # A known remedy must never be accepted if re-extraction failed.
                failures.append({"element_id": row["element_id"],
                                 "reason": "PARTY_REQUIREMENT_WITHOUT_ENTAILMENT_VALIDATOR"})
                continue
            if not any(p["status"] == "COVERED" and p["obligated_party"] in {party["obligated_party"], "责任方"}
                       for p in atomic["party_coverage"]):
                failures.append({"element_id": row["element_id"], "reason": "REMEDY_OR_PARTY_NOT_ENTAILED"})
    return failures


def party_narrative_failures(elements, narrative, recommendation=""):
    """Actor-level display must agree with the evidence-bound actor state."""
    from review_v2.element_resolution import party_requirement_states
    failures = []
    labels = {party["required_fact"] for element in elements for party in party_requirement_states(element)}
    if not labels:
        return failures
    # Longest complete actor label wins: 许可方 is not 被许可方.
    pattern = re.compile("|".join(re.escape(label) for label in sorted(labels, key=len, reverse=True)))
    def mentioned(text):
        return {match[0] for match in pattern.finditer(text)}
    for element in elements:
        for party in party_requirement_states(element):
            if party["status"] == "NOT_APPLICABLE":
                continue
            label = party["required_fact"]
            if party["status"] == "COVERED":
                contradicted = any(label in mentioned(text) for key in ("partial_elements", "missing_elements")
                                   for text in narrative.get(key, [])) or label in mentioned(recommendation)
                omitted = bool(narrative) and not any(label in mentioned(text) for text in narrative.get("covered_elements", []))
            elif party["status"] == "MISSING":
                contradicted = any(label in mentioned(text) for text in narrative.get("covered_elements", []))
                omitted = bool(narrative) and not any(label in mentioned(text) for text in narrative.get("missing_elements", []))
            else:
                continue
            if contradicted or omitted:
                failures.append({"element_id": element["element_id"], "obligated_party": party["obligated_party"],
                                 "reason": "PARTY_NARRATIVE_STATUS_MISMATCH"})
    return failures
