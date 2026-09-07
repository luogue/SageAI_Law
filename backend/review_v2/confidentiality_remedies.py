"""Direct, party-scoped confidentiality remedies; money is not a penalty.

Keep the existing rule's element IDs, but retain each obligated party's own
atomic status and quote. A clause for one party never completes the other.
"""
import re


PARTIES = r"被许可方|许可方|受让方|让与方|出让方|转让方|买方|卖方|甲方|乙方|丙方"
COLLECTIVE = r"任何一方|任一方|违约方|泄密方|泄露方|双方|各方"
REMEDIES = {
    "breach_damage_liability": ("泄密损失赔偿责任", r"赔偿|损失赔偿责任"),
    "stop_disclosure": ("泄密后停止披露", r"停止[^。；]{0,14}(?:披露|泄露)"),
    "stop_use": ("泄密后停止使用", r"停止[^。；]{0,14}使用"),
    "mitigation_obligation": ("泄密后采取措施防止继续扩散或损失扩大", r"防止[^。；]{0,16}(?:扩大|扩散|泄露)|采取[^。；]{0,12}(?:补救|合理措施)"),
    "incident_notification": ("泄密后及时通知受影响方", r"(?:通知|告知)[^。；]{0,20}(?:对方|另一方|受影响方|买方|卖方|甲方|乙方|许可方|被许可方)"),
    "specific_confidentiality_penalty": ("泄密专项违约金", r"(?:支付|承担|赔付)[^。；]{0,35}违约金|违约金(?:为|金额|：|:)"),
    "excess_loss_compensation": ("泄密违约金不足部分的继续赔偿", r"(?:不足|超过|超出)[^。；]{0,25}(?:继续赔偿|赔偿|补足)|继续赔偿[^。；]{0,20}(?:不足|超过)"),
}
OPTIONAL_REMEDIES = {"specific_confidentiality_penalty", "excess_loss_compensation"}


def confidentiality_remedy_elements(clauses):
    records = []
    parties = []
    context_party = ""
    for clause in clauses:
        liability_context = bool(re.search(r"泄密责任|违反.{0,15}保密|保密违约", clause.text))
        for line in clause.text.splitlines():
            text = re.sub(r"^\s*\d+[．.、]\s*", "", line).strip()
            heading = re.fullmatch(f"({PARTIES})[：:]", text)
            if heading:
                context_party = heading[1]
                if context_party not in parties:
                    parties.append(context_party)
                continue
            if not text:
                continue
            breach = bool(re.search(r"泄密|泄露|违反.{0,20}保密|未经授权披露|超出本合同目的使用", text))
            if not (breach or liability_context):
                continue
            subjects = list(re.finditer(
                f"({PARTIES}|{COLLECTIVE})(?=未经|违反|泄|擅自|应|须|不得|在|未履行|支付|承担|赔偿|负责)", text,
            ))
            # A paragraph can contain multiple actors. Bind only the span up
            # to the next operative subject, never the whole shared paragraph.
            spans = [(match[1], text[match.start():subjects[i + 1].start() if i + 1 < len(subjects) else len(text)])
                     for i, match in enumerate(subjects)] if subjects else [(context_party, text)]
            for actor, quote in spans:
                if not actor or not any(re.search(pattern, quote) for _, pattern in REMEDIES.values()):
                    continue
                collective = bool(re.fullmatch(COLLECTIVE, actor))
                if not collective and actor not in parties:
                    parties.append(actor)
                records.append((actor, collective, clause.clause_id, quote.strip()))
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
            party_rows.append({"obligated_party": party, "status": status, "supporting_evidence": matches})
            facts.extend(matches)
        covered = [r["obligated_party"] for r in party_rows if r["status"] == "COVERED"]
        absent = [r["obligated_party"] for r in party_rows if r["status"] == "MISSING"]
        status = "PARTIALLY_COVERED" if covered and absent else "COVERED" if covered else "MISSING" if absent else "NOT_APPLICABLE"
        required = "、".join(absent) + label if absent else label
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
        if row["status"] == "COVERED" and any(p["status"] == "MISSING" for p in row["party_coverage"]):
            failures.append({"element_id": row["element_id"], "reason": "PARTY_GAP_LOST_IN_COVERAGE"})
        source = " ".join(f["quote"] for f in row.get("supporting_evidence", []))
        if "违约金" in row.get("proposition", "") and row["status"] in {"COVERED", "PARTIALLY_COVERED"} and "违约金" not in source:
            failures.append({"element_id": row["element_id"], "reason": "PENALTY_NARRATIVE_WITHOUT_PENALTY_EVIDENCE"})
        for party in row["party_coverage"]:
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
            atomic = next(e for e in checked if e["element_id"] == row["element_id"])
            if not any(p["status"] == "COVERED" and p["obligated_party"] in {party["obligated_party"], "责任方"}
                       for p in atomic["party_coverage"]):
                failures.append({"element_id": row["element_id"], "reason": "REMEDY_OR_PARTY_NOT_ENTAILED"})
    return failures
