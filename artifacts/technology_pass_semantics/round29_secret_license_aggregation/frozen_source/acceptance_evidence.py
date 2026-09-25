"""Acceptance evidence is a domain-bound obligation, not a mention of testing.

Product performance, ancillary service acceptance and document completeness
remain separate. Callers decide applicability; this module neither classifies
the main transaction nor treats a service-duration promise as acceptance proof.
"""
import re
from collections import defaultdict
from types import SimpleNamespace


PRODUCT = "PRODUCT_ACCEPTANCE"
SERVICE = "SERVICE_ACCEPTANCE"
MATERIAL = "MATERIAL_ACCEPTANCE"
UNKNOWN = "ACCEPTANCE_DOMAIN_UNRESOLVED"
DOMAINS = {PRODUCT, SERVICE, MATERIAL}
_NUMBER = r"(?:\d+(?:\.\d+)?|[一二两三四五六七八九十百]+)"
_TIME = _NUMBER + r"个?(?:工作日|日|天|小时|个月|月)"
_DEFERRED = r"另行(?:协商|约定|确认)|后续(?:确定|确认)|尚未(?:明确|约定)|待(?:定|补充|确认)|合理期限"
_SERVICE_OBJECT = r"技术服务|技术支持|技术指导|培训服务|培训成果|服务成果|服务质量|培训质量|服务报告|服务验收|服务响应|服务完成"
_MATERIAL_OBJECT = r"资料验收|文档验收|资料.{0,12}(?:完整性|齐全|可读性)|文档.{0,12}(?:完整性|齐全|可读性)|清点.{0,12}(?:资料|文件)|(?:技术资料|文件|文档).{0,10}(?:验收|核验|核对)"
_PRODUCT_OBJECT = r"研发成果|研究开发成果|产品|软件系统|控制系统|核心算法|抓取成功率|定位误差|识别.{0,8}时间|性能指标|运行.{0,10}(?:小时|稳定)|系统.{0,12}(?:运行|响应|准确率)"
_METRIC = re.compile(
    r"(?:成功率|准确率|误差|响应时间|计算时间|处理时间|可用率|稳定运行|连续运行|识别时间|完整率|可读率)"
    rf".{{0,30}}(?:不超过|不低于|不高于|不少于|达到|小于|大于|≤|≥|=).{{0,10}}{_NUMBER}", re.I,
)
_SPECIFIC_STANDARD = r"(?:符合|达到|按照|执行).{0,15}(?:GB[/T\-\s]*\d|ISO[\s/\-]*\d|《[^》]+》.{0,8}(?:第.{0,5}项|明确指标))"
REQUIREMENTS = {
    "objective_acceptance_standard": "客观质量和验收标准",
    "acceptance_process": "验收申请或组织程序",
    "acceptance_deadline": "验收期限",
    "written_objection_mechanism": "验收书面异议程序",
    "rectification_mechanism": "验收不合格后的整改机制",
    "rectification_deadline": "验收不合格后的整改期限",
    "reinspection_procedure": "整改后的复验程序",
    "reinspection_deadline": "复验期限",
}


def _compact(text):
    return re.sub(r"\s+", "", str(text or ""))


def _heading(clause):
    return " ".join(getattr(clause, "heading_path", None) or [getattr(clause, "title", "") or ""])


def _article_key(clause):
    return (getattr(clause, "heading_path", None) or [getattr(clause, "article_number", "") or clause.clause_id])[0]


def _domains(text):
    compact = _compact(text)
    result = set()
    if re.search(_SERVICE_OBJECT, compact):
        result.add(SERVICE)
    if re.search(_MATERIAL_OBJECT, compact):
        result.add(MATERIAL)
    if re.search(_PRODUCT_OBJECT, compact):
        result.add(PRODUCT)
    return result


def _incidental(text):
    compact = _compact(text)
    return bool(re.search(
        r"涉密人员[：:]|允许披露人员[：:]|(?:参与|负责).{0,30}(?:验收的人员|验收协调)|"
        r"(?:数据|资料|信息).{0,35}仅限.{0,30}(?:测试|验收).{0,8}使用|"
        r"(?:仅限|仅可).{0,30}(?:测试|验收).{0,8}使用", compact,
    ))


def _reference_only(text):
    return bool(re.fullmatch(r"(?:\d+[．.、])?《[^》]*(?:验收|测试|质量)[^》]*》[。；;]?", _compact(text)))


def _service_outcome(text):
    """A named service deliverable can be software; an adjacent product cannot."""
    compact = _compact(text)
    return bool(re.search(r"(?:技术)?服务成果(?:为|是|包括|包含)[^。；]{0,35}(?:软件系统|系统|算法|程序|报告|文档)", compact)
                and not re.search(r"另(?:行)?(?:交付|提供).{0,12}(?:产品|设备)|(?:产品|设备).{0,12}(?:另行|独立)", compact))


def _article_number(text):
    match = re.search(r"第([零〇一二两三四五六七八九十百千万\d]+)条", str(text or ""))
    if not match:
        return ""
    value = match[1]
    if value.isdigit():
        return str(int(value))
    digits = {c: n for n, c in enumerate("零一二三四五六七八九")}
    digits.update({"〇": 0, "两": 2})
    total, current = 0, 0
    for char in value:
        if char in digits:
            current = digits[char]
        else:
            total += (current or 1) * {"十": 10, "百": 100, "千": 1000, "万": 10000}[char]
            current = 0
    return str(total + current)


def _reference_scope(quote):
    compact = _compact(quote)
    if (not re.search(r"验收|质量标准|质量指标", compact)
            or re.search(r"不适用|不参照|不沿用|不按照|不采用|不依照|不执行|不按|不得|无需|无须|另行|待确认|后续确定", compact)):
        return None
    application = re.search(r"适用于|适用|参照|按照|沿用|执行|采用|依照|按(?=本合同|第)|同(?=本合同|第)", compact)
    if not application:
        return None
    subject = compact[application.end():] if application[0] == "适用于" else compact[:application.start()]
    domains = _domains(subject)
    if len(domains) != 1:
        return None
    references = list(dict.fromkeys(_article_number(match[0]) for match in re.finditer(r"第[零〇一二两三四五六七八九十百千万\d]+条", compact)))
    if not references:
        return None
    keys = set()
    if re.search(r"标准|质量指标", compact):
        keys.add("objective_acceptance_standard")
    if re.search(r"程序|流程|方式", compact) and not re.search(r"整改|复验|异议", compact):
        keys.add("acceptance_process")
    if "期限" in compact and not re.search(r"整改|复验", compact):
        keys.add("acceptance_deadline")
    if re.search(r"书面异议|异议程序", compact):
        keys.add("written_objection_mechanism")
    if "整改" in compact:
        keys.add("rectification_mechanism")
        if "期限" in compact:
            keys.add("rectification_deadline")
    if "复验" in compact:
        keys.add("reinspection_procedure")
        if "期限" in compact:
            keys.add("reinspection_deadline")
    return {"domain": next(iter(domains)), "references": references,
            "keys": keys or set(REQUIREMENTS), "explicit_keys": bool(keys)}


def _context_row(clause, quote, role):
    return {"clause_id": clause.clause_id, "quote": quote, "evidence_role": role,
            "source_heading_path": list(getattr(clause, "heading_path", None) or [])}


def _fact_keys(text, acceptance_context):
    """Find the operative action and its own value inside one sentence."""
    compact = _compact(text)
    keys = set()
    if _incidental(text) or _reference_only(text):
        return keys
    standard_negated = bool(re.search(r"不(?:要求|保证|适用)|无需(?:达到|符合)|不作为验收", compact))
    if acceptance_context and not standard_negated and (_METRIC.search(compact) or re.search(_SPECIFIC_STANDARD, compact, re.I)
                               or re.search(r"(?:资料|文件|文档).{0,15}(?:齐全|完整|可读取|可打开|格式正确)", compact)):
        keys.add("objective_acceptance_standard")
    if acceptance_context and re.search(r"验收标准|质量标准", compact) and re.search(_DEFERRED, compact):
        keys.add("objective_acceptance_standard")
    process_negated = bool(re.search(r"无需验收|(?:无需|无须|不必|不再).{0,18}(?:组织|进行|完成|开展|提交|提出).{0,12}验收|不(?:组织|进行|完成|开展|提交|提出).{0,12}验收", compact))
    if re.search(r"(?:组织|进行|完成|开展)验收|(?:提交|提出).{0,12}验收申请|(?:提交|发出)验收通知", compact) and not process_negated:
        keys.add("acceptance_process")
    if ("验收" in compact and not process_negated and not re.search(r"复验|再次验收|重新验收|二次验收", compact)
            and re.search(rf"{_TIME}内.{{0,12}}(?:组织|进行|完成)?验收|验收(?:期限|时间)[：:为]{{1,2}}{_TIME}", compact)):
        keys.add("acceptance_deadline")
    if acceptance_context and re.search(r"(?:提出|提交|出具).{0,12}书面异议|异议应.{0,8}书面", compact):
        keys.add("written_objection_mechanism")
    if (acceptance_context and re.search(r"整改|修改|修复|补正|补齐", compact)
            and not re.search(r"(?:无需|无须|不必|不得).{0,15}(?:整改|修改|修复|补正|补齐)", compact)
            and re.search(r"(?:应|须|负责|必须|在|完成).{0,30}(?:整改|修改|修复|补正|补齐)|整改(?:机制|程序|方式)[：:]", compact)):
        keys.add("rectification_mechanism")
        if re.search(rf"{_TIME}内.{{0,15}}(?:整改|修改|修复|补正|补齐)|(?:整改|修改|修复|补正)期限[：:为]{{1,2}}{_TIME}", compact):
            keys.add("rectification_deadline")
        elif re.search(r"合理期限|整改期限.{0,15}(?:另行|待定)", compact):
            keys.add("rectification_deadline")
    if (acceptance_context and re.search(r"复验|再次验收|重新验收|二次验收", compact)
            and not re.search(r"(?:无需|无须|不必|不得|不再).{0,15}(?:复验|再次验收|重新验收|二次验收)", compact)):
        keys.add("reinspection_procedure")
        if re.search(rf"{_TIME}内.{{0,15}}(?:复验|再次验收|重新验收|二次验收)|(?:复验|再次验收|重新验收|二次验收).{{0,15}}{_TIME}", compact):
            keys.add("reinspection_deadline")
    return keys


def _direct_acceptance_facts(clauses):
    """Return actual acceptance facts with their object domain and exact quotes."""
    articles = defaultdict(list)
    for clause in clauses:
        articles[_article_key(clause)].append(clause)
    facts = []
    for article, article_clauses in articles.items():
        article_text = "\n".join(c.text for c in article_clauses)
        article_domains = _domains(article + " " + article_text)
        article_acceptance = bool(re.search(r"验收|质量(?:标准|要求)|服务质量", str(article))) or bool(re.search(r"验收标准[：:]", article_text))
        for clause in article_clauses:
            for match in re.finditer(r"[^。；;\n]+[。；;]?", clause.text):
                quote = match[0].strip()
                if not quote or _incidental(quote) or _reference_only(quote):
                    continue
                compact = _compact(quote)
                acceptance_context = (article_acceptance or bool(re.search(r"验收|质量标准|服务质量", compact))
                                      or ((_domains(quote) == {SERVICE} or _service_outcome(quote)) and bool(_METRIC.search(compact))))
                keys = _fact_keys(quote, acceptance_context)
                if not keys:
                    continue
                direct_domains = _domains(quote)
                heading_domains = _domains(_heading(clause))
                # An explicit object in this sentence wins. Article context is
                # usable only when it identifies one domain, never an arbitrary
                # product/service mixture elsewhere in the contract.
                qualified = direct_domains or heading_domains or (article_domains if len(article_domains) == 1 else set())
                service_outcome_context = (
                    _service_outcome(quote)
                    or (_domains(article) == {SERVICE} and _service_outcome(article_text)
                        and direct_domains == {PRODUCT})
                )
                if service_outcome_context:
                    qualified = {SERVICE}
                domain = next(iter(qualified)) if len(qualified) == 1 else UNKNOWN
                for key in sorted(keys):
                    partial = bool(re.search(_DEFERRED, compact))
                    if key in {"rectification_mechanism", "acceptance_process", "reinspection_procedure"} and "合理期限" in compact:
                        partial = False
                    facts.append({
                        "fact_key": key, "source_domain": domain, "clause_id": clause.clause_id,
                        "quote": quote, "status": "PARTIALLY_COVERED" if partial else "COVERED",
                        "effective_acceptance_article": _article_number(article),
                        "source_heading_path": list(getattr(clause, "heading_path", None) or []),
                        "domain_context_evidence": [
                            _context_row(c, c.text, "ACCEPTANCE_OBJECT_CONTEXT")
                            for c in article_clauses if (len(_domains(c.text)) == 1 and domain in _domains(c.text))
                            or (service_outcome_context and _service_outcome(c.text))
                        ] if (not direct_domains and not heading_domains) or (service_outcome_context and not _service_outcome(quote)) else [],
                    })
    return facts


def extract_acceptance_facts(clauses):
    """Resolve explicit acceptance references while retaining both ends of the chain."""
    clauses = list(clauses)
    facts = _direct_acceptance_facts(clauses)
    references = []
    for clause in clauses:
        for match in re.finditer(r"[^。；;\n]+[。；;]?", clause.text):
            quote = match[0].strip()
            scope = _reference_scope(quote)
            if scope and not _incidental(quote):
                references.append((clause, quote, scope))
    seen = {(f["source_domain"], f["fact_key"], f["clause_id"], f["quote"], f["effective_acceptance_article"]) for f in facts}
    # Only already evidenced target atoms can cross a reference. A clause that
    # adopts standards cannot also copy the target's deadlines or remedies.
    for _ in range(len(references)):
        added = []
        for clause, quote, scope in references:
            owner_article = _article_number(_article_key(clause))
            target_facts = [f for f in facts if f["effective_acceptance_article"] in scope["references"]
                            and f["fact_key"] in scope["keys"]]
            for fact in target_facts:
                key = (scope["domain"], fact["fact_key"], fact["clause_id"], fact["quote"], owner_article)
                if key in seen:
                    continue
                context = [*fact.get("domain_context_evidence", []), _context_row(clause, quote, "ACCEPTANCE_SCOPE_REFERENCE")]
                added.append({**fact, "source_domain": scope["domain"], "effective_acceptance_article": owner_article,
                              "domain_context_evidence": list({(row["clause_id"], row["quote"]): row for row in context}.values()),
                              "reference_resolution": "TARGET_FACT_BOUND"})
                seen.add(key)
        if not added:
            break
        facts.extend(added)
    return facts


def acceptance_requirement_elements(clauses, *, domain):
    """Evaluate only the requested acceptance domain; missing sources stay missing."""
    if domain not in DOMAINS:
        raise ValueError("An explicit product, service or material acceptance domain is required")
    facts = extract_acceptance_facts(clauses)
    label_prefix = {PRODUCT: "研发成果或产品", SERVICE: "附随技术服务", MATERIAL: "交付资料"}[domain]
    elements = []
    for key, label in REQUIREMENTS.items():
        sources = [fact for fact in facts if fact["fact_key"] == key and fact["source_domain"] == domain]
        direct = [fact for fact in sources if fact["status"] == "COVERED"]
        state = "COVERED" if direct else "PARTIALLY_COVERED" if sources else "MISSING"
        required = label_prefix + label
        gaps = [] if direct else [required]
        elements.append({"element_id": key, "source_fact_key": key, "source_domain": domain,
                         "required_fact": required, "status": state, "risk_relevant": True,
                         "proposition": required + ("已有明确约定。" if direct else "已有原则安排，但具体内容尚未确定。" if sources else ""),
                         "residual_gap": "、".join(gaps), "search_targets": gaps,
                         "supporting_evidence": direct or sources,
                         "bound_evidence_ids": list(dict.fromkeys(fact["clause_id"] for fact in direct or sources))})
    return elements


def acceptance_source_entailment(source, requirement_key, *, expected_domain):
    """Recompute support from source text, without trusting preassigned evidence tags."""
    if expected_domain not in DOMAINS:
        raise ValueError("An explicit acceptance domain is required")
    quote = str(source.get("quote") or source.get("text") or "")
    heading = list(source.get("heading_path") or source.get("source_heading_path") or [])
    primary = SimpleNamespace(clause_id=str(source.get("clause_id") or "source"), text=quote,
                              heading_path=heading, title=source.get("title") or "")
    context = [SimpleNamespace(clause_id=str(row.get("clause_id") or "context"), text=str(row.get("quote") or ""),
                               heading_path=list(row.get("source_heading_path") or heading), title="")
               for row in source.get("domain_context_evidence", [])]
    facts = [fact for fact in extract_acceptance_facts([primary, *context])
             if fact["clause_id"] == primary.clause_id and fact["quote"] in quote]
    relevant = [fact for fact in facts if fact["fact_key"] == requirement_key]
    matched = [fact for fact in relevant if fact["source_domain"] == expected_domain]
    return {
        "status": "SUPPORTS" if any(f["status"] == "COVERED" for f in matched) else "PARTIAL_SUPPORT" if matched else "RELATED_NOT_SUPPORTING",
        "reason": "DIRECT_DOMAIN_BOUND_ACCEPTANCE_FACT" if matched else "ACCEPTANCE_SOURCE_DOMAIN_MISMATCH" if relevant else "NO_OPERATIVE_ACCEPTANCE_REQUIREMENT",
        "expected_domain": expected_domain, "actual_domains": sorted({fact["source_domain"] for fact in relevant}),
        "requirement_key": requirement_key, "supporting_evidence": matched,
    }
