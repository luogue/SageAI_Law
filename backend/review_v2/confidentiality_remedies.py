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
    "stop_disclosure": ("泄密后停止披露", r"停止[^。；]{0,14}(?:披露|泄露)|停止(?:相关|泄密|违约)行为"),
    "stop_use": ("泄密后停止使用", r"停止[^。；]{0,14}使用|限制未经授权(?:的?人员)?(?:继续)?的?使用|未经授权[^。；]{0,25}使用[^。；]{0,55}停止(?:相关)?行为"),
    "mitigation_obligation": ("泄密后采取措施防止继续扩散或损失扩大", r"防止[^。；]{0,16}(?:扩大|扩散|泄露)|采取[^。；]{0,12}(?:补救|合理措施)|控制[^。；]{0,18}(?:继续|进一步)?扩散"),
    "incident_notification": ("泄密后及时通知受影响方", r"(?:通知|告知)[^。；]{0,20}(?:对方|另一方|受影响方|信息提供方|买方|卖方|甲方|乙方|许可方|被许可方)"),
    "evidence_preservation": ("泄密后保存日志和证据", r"(?:保存|保全|留存)[^。；]{0,20}(?:日志|证据)"),
    "notification_deadline": ("泄密通知的具体期限", r"(?:\d+|[一二两三四五六七八九十]+)(?:个)?(?:小时|工作日|日|天)内[^。；]{0,15}通知"),
    "specific_confidentiality_penalty": ("泄密专项违约金", r"(?:支付|承担|赔付)[^。；]{0,35}违约金|违约金(?:为|金额|：|:)"),
    "excess_loss_compensation": ("泄密违约金不足部分的继续赔偿", r"(?:不足|超过|超出)[^。；]{0,25}(?:继续赔偿|赔偿|补足)|继续赔偿[^。；]{0,20}(?:不足|超过)"),
}
OPTIONAL_REMEDIES = {"specific_confidentiality_penalty", "excess_loss_compensation"}


def canonical_confidentiality_remedies(clauses):
    """The registry and all rule/verifier consumers use this same event scope."""
    roots = {
        (getattr(c, 'heading_path', None) or [c.title])[0]
        for c in clauses
        if has_confidentiality_remedy(c.text)
        or re.search(r'泄密|泄露|信息泄露|保密信息.{0,20}未经授权', c.title + c.text)
    }
    return confidentiality_remedy_elements([
        c for c in clauses if (getattr(c, 'heading_path', None) or [c.title])[0] in roots
    ])


def confidentiality_remedy_elements(clauses):
    records = []
    parties = []
    context_party = ""
    article_intros = {}
    for clause in clauses:
        root = (getattr(clause, 'heading_path', None) or [getattr(clause, 'title', '')])[0]
        if re.search(CONFIDENTIALITY_BREACH, clause.text) and re.search(r'(?:应当|应|须|必须)(?:立即)?[：:]', clause.text):
            actor = re.search(rf'({PARTIES}|{COLLECTIVE})[^。；\n]{{0,45}}(?:发现|发生|出现)', clause.text)
            article_intros[root] = (actor[1] if actor else '任何一方', clause)
    for clause in clauses:
        # A breach sentence does not turn the entire mixed liability article
        # into confidentiality remedies (nor transfer one actor's trigger).
        title = str(getattr(clause, 'title', '') or clause.text.splitlines()[0])
        liability_context = bool(re.fullmatch(r"(?:第.{1,8}条\s*)?(?:泄密责任|泄密处理|泄露处理|泄漏处理|保密违约责任|保密违约)", title.strip()))
        preceding_penalty = None
        breach_scope_start = None
        list_start = None
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
            root = (getattr(clause, 'heading_path', None) or [getattr(clause, 'title', '')])[0]
            inherited = article_intros.get(root)
            if inherited and not re.search(CONFIDENTIALITY_BREACH, text) and any(
                    re.search(pattern, text) for _, pattern in REMEDIES.values()):
                inherited_actor, intro_clause = inherited
                records.append((inherited_actor, True, clause.clause_id,
                                (intro_clause.text + '\n' + text).strip()))
            # Keep the actual introduction in a child item's source. Its actor,
            # incident condition and mandatory modal govern the whole list.
            if text.endswith(('：', ':')) and re.search(CONFIDENTIALITY_BREACH, text) and re.search(r'应|须|必须', text):
                list_start = clause.text.find(line)
                continue
            if list_start is not None:
                from review_v2.proposition_scope import arrangement_matches
                if any(
                        list(arrangement_matches(pattern, text)) for _, pattern in REMEDIES.values()):
                    text = clause.text[list_start:clause.text.find(line, list_start)+len(line)].strip()
                else:
                    list_start = None
            # Breach of an implementation/transfer boundary is not itself a
            # confidentiality breach. Match the breached obligation, not a
            # later mention of the transferred technical secret.
            # A carve-out from a general cap does not impose a secrecy remedy.
            if re.search(r'^除.{0,90}(?:保密|泄密).{0,10}(?:外|之外)', text):
                continue
            breach = bool(re.search(CONFIDENTIALITY_BREACH, text))
            if breach:
                breach_scope_start = clause.text.find(line)
            elif breach_scope_start is not None and re.search(r'(?:造成|发生)[^。；]{0,18}损失[^。；]{0,18}(?:承担|赔偿)|因违约[^。；]{0,35}(?:承担|赔偿)', text):
                # A general damage sentence immediately following a scoped
                # confidentiality-breach duty inherits that incident only.
                end = clause.text.find(line, breach_scope_start) + len(line)
                text = clause.text[breach_scope_start:end].strip()
                breach = True
                breach_scope_start = None
            elif text:
                breach_scope_start = None
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
    # Colon-led incident lists inherit the confidentiality event, collective
    # actor and mandatory modality from their introduction. This is the same
    # proposition-scope rule used for other legal lists, not a keyword fallback.
    for clause in clauses:
        original = getattr(clause, 'raw_text', '') or clause.text
        intro = re.search(
            rf'(?P<actor>{COLLECTIVE})[^。；\n]{{0,35}}(?:未经授权|泄密|泄露|\u8fdd反[^。；\n]{{0,8}}保密)[^。；\n]{{0,60}}(?:事件|情形)?[^。；\n]{{0,10}}(?:应当|应|须|必须)[：:]',
            original,
        )
        if not intro:
            continue
        actor = intro.group('actor')
        for line in original[intro.end():].splitlines():
            child = line.strip()
            if not child:
                continue
            combined = original[intro.start():original.find(line, intro.end()) + len(line)].strip()
            if any(re.search(pattern, combined) for _, pattern in REMEDIES.values()):
                row = (actor, True, clause.clause_id, combined)
                if row not in records:
                    records.append(row)
    # The parser may expose an article title through ``text`` while the
    # verifiable source span lives in ``raw_text``.  List inheritance must
    # preserve that exact source boundary: a synthesized title + body string
    # is useful as context, but is not a source span and cannot be registered
    # in the verified FactStore.  Rebind inherited propositions to the exact
    # article body before publishing the canonical facts.
    clauses_by_id = {clause.clause_id: clause for clause in clauses}
    exact_records = []
    for actor, collective, clause_id, quote in records:
        clause = clauses_by_id.get(clause_id)
        original = (getattr(clause, 'raw_text', '') or clause.text) if clause else ''
        if original and quote not in original:
            quote = original.strip()
        row = (actor, collective, clause_id, quote)
        if quote and row not in exact_records:
            exact_records.append(row)
    records = exact_records
    if not parties:
        parties = ["责任方"]
    elements = []
    for key, (label, pattern) in REMEDIES.items():
        if key in {'evidence_preservation', 'notification_deadline'}:
            mentioned = r'日志|证据' if key == 'evidence_preservation' else r'通知.{0,15}(?:期限|小时|工作日)|具体.{0,8}通知'
            if not any(re.search(mentioned, c.text) for c in clauses):
                continue
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
