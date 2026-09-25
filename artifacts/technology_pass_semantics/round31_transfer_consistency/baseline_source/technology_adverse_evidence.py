"""Operative adverse predicates used by both evaluation and source verification."""
import re


ACTUAL_INFRINGEMENT_PATTERNS = (
    r"(?:明知|确认).{0,20}(?:无权|侵权).{0,20}(?:仍|继续)(?:转让|实施|许可)",
    r"无权许可仍继续许可|排除第三方合法权利|确认构成侵权",
    r"(?:允许|同意).{0,20}(?:侵害|侵犯).{0,20}(?:第三方|他人)",
    r"(?:标的技术|本项技术|受让方实施|转让方).{0,30}(?:已存在|已经发生|被认定|被判决).{0,20}(?:侵犯第三方|侵害他人|权属冲突)",
    r"(?:已经|已被认定|已被判决|确认).{0,18}(?:侵犯|侵害).{0,25}(?:第三方|他人)",
    r"(?:未经授权|明知无权).{0,25}(?:使用|实施|转让|许可).{0,25}(?:第三方|他人).{0,20}(?:专利|技术秘密|技术成果)",
    r"(?:收到|遭到).{0,20}(?:侵权起诉|侵权判决|侵权索赔).{0,30}(?:已经成立|确认侵权|构成侵权)",
)


def actual_infringement_sources(text):
    from review_v2.proposition_scope import scoped_propositions, event_polarity
    for source in scoped_propositions(text):
        if (source['inherited_missing'] or source['condition_context']) and not source['affirmative_tail']:
            continue
        # An inline missing arrangement is scoped by event_polarity. It must
        # not erase an earlier affirmative event in the same proposition.
        # Search the independent tail separately: a bounded regex match in
        # the negated head may otherwise consume a later affirmative match.
        for quote in (source['quote'], source['affirmative_tail']):
            sentence = re.sub(r'\s+', '', quote)
            for pattern in ACTUAL_INFRINGEMENT_PATTERNS:
                for match in re.finditer(pattern, sentence):
                    if event_polarity(sentence, match.start(), match.end()) == 'AFFIRMATIVE':
                        yield quote
                        break
                else:
                    continue
                break


def has_actual_infringement(text):
    return next(actual_infringement_sources(text), None) is not None


def transferred_asset_use_boundary(sentence, context):
    """A transferor's stop-use duty is not a prohibition of independent research."""
    if not re.search(r'(?:不得|禁止)[^。；]{0,12}(?:基于|利用|使用)[^。；]{0,20}(?:已经删除|已转让|已让与|返还)', sentence):
        return False
    from review_v2.technology_service_analysis import build_technology_fact_registry
    provider = build_technology_fact_registry(context)['third_party_claim']['response_party_patterns']['provider']
    return bool(re.search(provider + r'[^。；]{0,15}(?:不得|禁止)[^。；]{0,12}(?:基于|利用|使用)'
                          r'[^。；]{0,20}(?:已经删除|已转让|已让与|返还)[^。；]{0,25}(?:技术|秘密)'
                          r'[^。；]{0,25}(?:开发|研发)[^。；]{0,20}(?:相同|同类|类似)', sentence))


def _protective_restriction_operator(predicate):
    # Prohibiting a restriction protects the embedded activity; the negation
    # governs the outer verb, not the embedded research/transfer predicate.
    return bool(re.search(r'(?:不得|禁止|无权)[^。；;但]{0,8}(?:限制|阻止|禁止|干涉|要求)', predicate))


def independent_research_restriction_sources(text):
    from review_v2.proposition_scope import arrangement_matches
    actor = r'(?:买方|受让方|被许可方|让与方|转让方|许可方|甲方|乙方)'
    consent = r'(?:未经|未获|未取得|未获得)' + actor + r'[^。；，,]{0,12}(?:同意|许可|批准|授权)[，,]?'
    bridge = r'(?:' + consent + r'|(?!(?:' + actor + r'))[^。；]){0,18}'
    pattern = r'(?P<actor>' + actor + r')' + bridge + r'(?:不得|禁止)[^。；]{0,20}(?:自行|独立|继续)[^。；]{0,10}(?:研究|研发|开发)'
    for row in arrangement_matches(pattern, text):
        if _protective_restriction_operator(row['quote'][row['match_start']:row['match_end']]):
            continue
        if not transferred_asset_use_boundary(re.sub(r'\s+', '', row['quote']), text):
            yield row['quote']


def uncompensated_universal_assignment_owner(text):
    """Existing universal assignment fact, shared by ownership and competition."""
    compact = re.sub(r'\s+', '', text)
    owner = re.search(
        r'(?:后续改进|改进成果).{0,140}(?:无论|不论)由哪一方完成.{0,80}'
        r'(?:知识产权|专利申请权|成果权利).{0,30}(?:均|全部)?归([甲乙丙丁戊])方所有', compact)
    if not owner:
        return None
    limited = re.search(r'(?:基于|依赖|使用).{0,30}(?:本项目|项目成果|合同技术|共同成果).{0,30}(?:形成|产生|完成)', compact)
    consideration = any(term in compact for term in (
        '合理对价', '合理补偿', '另行支付', '有偿转让', '许可费', '双方另行协商对价', '各方另行协商对价'))
    return owner.group(1) if not limited and not consideration else None


def has_competition_restriction(text):
    # The negative search must include every existing affirmative competition
    # family. Absence of a research ban cannot erase a forced transfer or a
    # ban on obtaining third-party/substitute technology.
    if next(independent_research_restriction_sources(text), None) or has_improvement_restriction(text):
        return True
    from review_v2.clause_parser import parse_contract_clauses
    if any(uncompensated_universal_assignment_owner(c.text) for c in parse_contract_clauses(text)):
        return True
    from review_v2.technology_service_analysis import analyze_improvement_license_facts
    if analyze_improvement_license_facts(text).get('forced_free_improvement_transfer'):
        return True
    from review_v2.proposition_scope import arrangement_matches
    patterns = (
        r'(?:不得|禁止)[^。；]{0,30}(?:采购|购买|使用|推荐)[^。；]{0,35}(?:替代|竞争)(?:性)?(?:技术|方案)',
        r'(?:不得|禁止)[^。；]{0,22}(?:从|向)[^。；]{0,18}(?:第三方|其他渠道|竞争对手)[^。；]{0,18}(?:获得|取得|购买)',
        r'(?:不得|禁止)[^。；]{0,25}(?:竞争性)?替代(?:技术|方案)',
        r'(?:不得|禁止)[^。；]{0,25}(?:绕开|规避)[^。；]{0,25}(?:合同专利|许可技术)',
        r'(?:研发|竞争技术|替代技术|替代方案)[^。；]{0,80}(?:合同终止后|终止后)[^。；]{0,30}(?:继续有效|仍然有效)[^。；]{0,12}(?:五|5)年',
        r'(?:合同终止后|终止后)[^。；]{0,30}(?:五|5)年[^。；]{0,80}(?:研发|竞争技术|替代技术|替代方案)',
    )
    return any(not _protective_restriction_operator(row['quote'][row['match_start']:row['match_end']])
               for pattern in patterns for row in arrangement_matches(pattern, text))


def has_improvement_restriction(text, *, context=None):
    """Resolve the operative predicate, preserving absence-list and actor scope."""
    from review_v2.proposition_scope import arrangement_matches
    patterns = (
        r"(?:禁止|不得|无权|限制)[^。；;但]{0,35}(?:自主)?(?:研发|研究|改进|使用竞争性技术)",
        r"(?:必须|应当|应|须)[^。；;但]{0,30}(?:无偿|免费)[^。；;但]{0,20}(?:转让|移交|归属)[^。；;但]{0,30}(?:改进|成果)",
        r"(?:必须|应当|应|须)[^。；;但]{0,30}(?:改进成果|知识产权)[^。；;但]{0,25}(?:无偿|免费)[^。；;但]{0,12}(?:转让|移交|转归)",
        r"(?:改进|后续研发)[^。；;但]{0,40}(?:仅归|一律归|全部归)[^。；;但]{0,16}(?:许可方|出让方|转让方)",
    )
    for pattern in patterns:
        for row in arrangement_matches(pattern, text):
            quote = row['quote']
            predicate = quote[row['match_start']:row['match_end']]
            if _protective_restriction_operator(predicate):
                continue
            if not any(term in quote for term in ('改进', '后续研发', '竞争性技术')):
                continue
            if transferred_asset_use_boundary(re.sub(r'\s+', '', quote), context or text):
                continue
            return True
    return False


NEGATIVE_PREDICATES = {
    'TC-02-01': ('UNLAWFUL_COMPETITION_RESTRICTION', has_competition_restriction),
    'TC-02-02': ('ACTUAL_INFRINGEMENT', has_actual_infringement),
    'TC-10-04': ('UNREASONABLE_IMPROVEMENT_RESTRICTION', has_improvement_restriction),
}


def prepare_negative_audits(items, clauses):
    """Produce the rule's search evidence before positive-source verification.

    Previously checklist metadata added an audit only after the source gate had
    treated a no-adverse-fact decision as an empty positive requirement set.
    """
    predicates = NEGATIVE_PREDICATES
    for item in items:
        if item.item_id not in predicates or not clauses:
            continue
        name, predicate = predicates[item.item_id]
        found = predicate('\n'.join(c.text for c in clauses))
        item.decision_trace['review_polarity'] = 'NEGATIVE_CLAUSE_CHECK'
        item.decision_trace['negative_clause_check'] = dict(
            review_id=item.item_id, predicate=name, query_semantics='ADVERSE_CLAUSE_SEARCH',
            result='ADVERSE_CLAUSE_FOUND' if found else 'NO_ADVERSE_CLAUSE_FOUND',
            searched_scope=[c.clause_id for c in clauses], search_coverage='SUFFICIENT',
            adverse_clause_exists=found, confidence='high',
            producer='CANONICAL_ADVERSE_PREDICATE_SEARCH')


def verify_negative_search(item, clauses):
    """A negative rule needs a complete, independently reproduced search.

    This is deliberately not a positive-element exception: allocation clauses
    do not become affirmative proof of actual infringement or its absence.
    """
    audit = item.decision_trace.get('negative_clause_check') or {}
    definition = NEGATIVE_PREDICATES.get(item.item_id)
    if not (definition
            and item.decision_trace.get('review_polarity') == 'NEGATIVE_CLAUSE_CHECK'
            and audit.get('search_coverage') == 'SUFFICIENT'
            and audit.get('adverse_clause_exists') is False
            and clauses and set(audit.get('searched_scope') or []) == {c.clause_id for c in clauses}):
        return None
    name, predicate = definition
    if audit.get('predicate') != name or predicate('\n'.join(c.text for c in clauses)):
        return None
    return dict(status='PASS', assessment='FULL_CORPUS_NO_ADVERSE_FACT',
                searched_scope=list(audit['searched_scope']),
                predicate=name, failures=[])
