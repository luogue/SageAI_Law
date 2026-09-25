"""One operative guarantee-mode fact, shared by mutually exclusive reviews."""
import re

MODE_NODES = {
    "guarantee_type_joint_or_general", "joint_guarantee_explicit_wording",
    "general_guarantee_explicit_wording", "unclear_guarantee_type_clause",
}


def extract_mode(clauses):
    sources = {"GENERAL": [], "JOINT": []}
    for clause in clauses:
        for quote in re.split(r"(?<=[。；;，,])|\n", clause.text):
            text = re.sub(r"\s+", "", quote)
            for mode, pattern in (("GENERAL", r"一般保证(?:责任)?"), ("JOINT", r"连带(?:责任)?保证|连带清偿责任")):
                match = re.search(pattern, text)
                if not match:
                    continue
                prefix = text[:match.start()]
                # A current stipulation can follow a history recital in the
                # same sentence. Only qualifiers of this occurrence count.
                if '本合同' in prefix:
                    prefix = prefix[prefix.rfind('本合同'):]
                if re.search(r"[□☐]\s*$|(?:不|非|并非|不是|无需|不承担|不提供)\s*$", prefix):
                    continue
                if re.search(r"历史|曾经|原合同|原约定|旧合同|法律规定|民法典|例如|引用|示例|如选择|如约定|如果|假如", prefix):
                    continue
                if not re.search(r"承担|提供|方式[为是：:]|类型[为是：:]|选择|[☑✓✔]", prefix):
                    continue
                sources[mode].append({"clause_id": clause.clause_id, "location": clause.location,
                    "text": quote.strip(), "quote": quote.strip(), "source_type": "SOURCE_CLAUSE",
                    "section_type": getattr(clause, "section_type", "正式合同条款"),
                    "evidence_id": f"GUA-MODE-{clause.clause_id}-{mode}-{len(sources[mode])}",
                    "supported_elements": ["guarantee_mode"], "source_domain": "GUARANTEE_MODE"})
    modes = [mode for mode, rows in sources.items() if rows]
    return {"mode": modes[0] if len(modes) == 1 else "CONFLICT" if modes else "UNSPECIFIED",
            "evidence": [row for rows in sources.values() for row in rows]}


def apply_mode(items, clauses, checklist):
    # Import lazily to keep fact extraction usable independently of the engine.
    from review_v2.engine import _set_item_pass, _set_item_not_applicable, _set_item_missing, _insufficient_context_item
    fact = extract_mode(clauses)
    mode = fact['mode']
    for index, item in enumerate(items):
        if item.node_id not in MODE_NODES:
            continue
        item.decision_trace['guarantee_mode_fact'] = fact
        node = item.node_id
        enabled = (node == 'guarantee_type_joint_or_general'
                   or node == 'general_guarantee_explicit_wording' and mode == 'GENERAL'
                   or node == 'joint_guarantee_explicit_wording' and mode == 'JOINT'
                   or node == 'unclear_guarantee_type_clause' and mode == 'UNSPECIFIED')
        if mode == 'CONFLICT':
            if node == 'guarantee_type_joint_or_general':
                replacement = _insufficient_context_item(next(c for c in checklist if c.item_id == item.item_id),
                    '存在不同保证方式的实际约定，请核验是否针对不同保证人、债务或是否存在修订冲突；不能同时认定一般保证和连带保证。')
                replacement.evidence_clauses = fact['evidence']
                replacement.decision_trace['guarantee_mode_fact'] = fact
                items[index] = replacement
            else:
                _set_item_not_applicable(item, '保证方式存在待核验冲突，先由保证方式主项核验，不同时启动互斥分支。')
            continue
        if not enabled:
            label = {'GENERAL': '一般保证', 'JOINT': '连带责任保证'}.get(mode, '尚未明确保证方式')
            _set_item_not_applicable(item, f'当前实际约定为{label}，本保证方式专项分支未触发。')
            continue
        if mode == 'UNSPECIFIED' and node == 'guarantee_type_joint_or_general':
            replacement = _insufficient_context_item(next(c for c in checklist if c.item_id == item.item_id),
                '未取得明确选择一般保证或连带责任保证的实际条款；方式未明确的修改事项由保证方式未明确规则统一处理。')
            replacement.decision_trace['guarantee_mode_fact'] = fact
            items[index] = replacement
            continue
        item.decision_trace['guarantee_mode_elements'] = [{"element_id": "guarantee_mode",
            "proposition": "合同实际约定的保证方式", "terms": ["一般保证", "连带责任保证", "连带保证", "连带清偿责任"]}]
        item.applicability = {"status": "APPLICABLE", "applicable": True, "reason": "由共享的实际保证方式事实确定。"}
        item.needs_manual_review = False
        if mode == 'UNSPECIFIED':
            _set_item_missing(item, '中', '全文未找到实际选择一般保证或连带责任保证的条款；仅称保证人或担保人不能证明方式明确。',
                '保证方式尚未明确，依法适用一般保证默认规则；应根据交易意图明确方式，不自动建议加重保证人责任。', 'guarantee_mode_fact')
            item.suggested_clause_example = '建议根据真实交易意图明确一般保证或连带责任保证，不以保证人称谓或追偿条款替代方式约定。'
        else:
            label = '一般保证' if mode == 'GENERAL' else '连带责任保证'
            reason = f'实际保证条款明确选择{label}，保证方式已明确。'
            _set_item_pass(item, [], reason, reason)
            item.evidence_clauses = [dict(e) for e in fact['evidence']]
            item.evidence_location = '；'.join(dict.fromkeys(e['location'] for e in fact['evidence']))
            item.suggested_clause_example = ''
            item.legal_consequence_if_missing = '无独立修改缺口。'
        item.judge_source = 'guarantee_mode_fact'
        item.fallback_reason = '共享实际保证方式事实'
    return items


def consistency_gate(items):
    rows = {r.node_id: r for r in items if r.node_id in MODE_NODES}
    failures = []
    for row in items:
        prerequisite = row.decision_trace.get('guarantee_prerequisite', {})
        if prerequisite.get('applicable') is False and row.coverage_status != '不适用':
            failures.append({'requirement': 'GUARANTEE_BRANCH_PREREQUISITE', 'review_id': row.item_id,
                             'root_cause': '共同保证或先诉抗辩分支未满足前提却进入实质审查。'})
    for node, row in rows.items():
        mode = row.decision_trace.get('guarantee_mode_fact', {}).get('mode')
        inactive = (mode == 'GENERAL' and node in {'joint_guarantee_explicit_wording','unclear_guarantee_type_clause'}
                    or mode == 'JOINT' and node in {'general_guarantee_explicit_wording','unclear_guarantee_type_clause'}
                    or mode == 'UNSPECIFIED' and node in {'general_guarantee_explicit_wording','joint_guarantee_explicit_wording'}
                    or mode == 'CONFLICT' and node != 'guarantee_type_joint_or_general')
        if inactive and row.coverage_status != '不适用':
            failures.append({'requirement': 'GUARANTEE_MODE_EXCLUSIVITY', 'review_id': row.item_id,
                             'root_cause': '互斥保证方式分支与统一实际方式不一致。'})
    return {'status': 'BLOCKED' if failures else 'REPORT_READY', 'failures': failures}
