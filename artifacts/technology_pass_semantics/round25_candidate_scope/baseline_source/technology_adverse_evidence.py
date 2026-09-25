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


def has_improvement_restriction(text):
    """The same sentence-scoped polarity predicate for search and verification."""
    for raw_sentence in re.split(r"[。；;\n]", text):
        sentence = re.sub(r'\s+', '', raw_sentence)
        if not any(term in sentence for term in ("改进", "后续研发", "竞争性技术")):
            continue
        if re.search(r"(?:不得|无权|禁止).{0,12}(?:限制|要求).{0,40}(?:自主改进|独立.{0,8}改进|无偿(?:共有|转让|移交|分享))", sentence):
            continue
        if re.search(
            r"(?:禁止|不得|无权|限制).{0,35}(?:自主)?(?:研发|研究|改进|使用竞争性技术)|"
            r"(?:必须|应当|应|须).{0,30}(?:无偿|免费).{0,20}(?:转让|移交|归属).{0,30}(?:改进|成果)|"
            r"(?:改进|后续研发).{0,40}(?:仅归|一律归|全部归).{0,16}(?:许可方|出让方|转让方)", sentence):
            return True
    return False


NEGATIVE_PREDICATES = {
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
