"""Evidence-bound details for confidentiality, ancillary support and improvements.

The engine supplies its existing semantic-field extractor, avoiding a second
implementation of template blank detection or an import cycle with the engine.
Transaction applicability remains the caller's responsibility.
"""
import re

from review_v2.technology_service_analysis import analyze_improvement_license_facts


_PARTIES = r"被许可方|许可方|受让方|让与方|出让方|转让方|委托方|开发方|甲方|乙方|丙方|买方|卖方"
_NUMBER = r"(?:\d+(?:\.\d+)?|[零〇一二两三四五六七八九十百]+)"
_DURATION = _NUMBER + r"\s*个?(?:年|月|工作日|日|天)"
_DEFERRED = r"另行(?:协商|约定|商定)|协商确定|待(?:定|协商|补充)|尚未(?:约定|明确)|未(?:约定|明确)"
_SERVICE = r"技术(?:服务|支持|指导|培训)|技术指导和培训|人员培训"
_IMPROVEMENT = r"后续改进|改进成果|改进技术|改进形成|后续开发成果"


def _compact(text):
    return re.sub(r"\s+", "", text or "")


def _party_heading(text):
    """Recognize standalone actor fields, including numbered template headings."""
    number = r"(?:\d+|[一二三四五六七八九十]+)"
    return re.fullmatch(rf"(?:(?:[（(]{number}[）)]|{number}[．.、]))?({_PARTIES})[：:]?", _compact(text))


def _segments(clauses):
    """Keep exact sentence quotes and their article context, including split fields."""
    for clause in clauses:
        heading = " ".join(getattr(clause, "heading_path", None) or [])
        matches = list(re.finditer(r"[^。；;\n]+[。；;]?", clause.text))
        index = 0
        while index < len(matches):
            match = matches[index]
            quote = match[0].strip()
            # Preserve a label and its next-line value as one exact source span
            # so the shared field extractor can apply its normal blank rules.
            if (quote.endswith(("：", ":")) and not _party_heading(quote)
                    and index + 1 < len(matches)):
                following = matches[index + 1][0].strip()
                if not (following.endswith(("：", ":")) or re.match(r"^(?:第.+条|\d+[．.、])", following)):
                    quote = clause.text[match.start():matches[index + 1].end()].strip()
                    index += 1
            if quote:
                yield clause, heading, quote
            index += 1


def _fact(clause, quote, **details):
    return {"clause_id": clause.clause_id, "quote": quote, **details}


def _element(key, label, sources, *, status=None, residuals=None, **details):
    state = status or ("COVERED" if sources else "MISSING")
    gaps = list(residuals if residuals is not None else ([] if state == "COVERED" else [label]))
    return {
        "element_id": key, "required_fact": label, "status": state,
        "proposition": label + ("已有明确约定。" if state == "COVERED" else "已有原则安排，具体条件待明确。" if state == "PARTIALLY_COVERED" else ""),
        "residual_gap": "、".join(gaps), "search_targets": gaps,
        "bound_evidence_ids": list(dict.fromkeys(row["clause_id"] for row in sources)),
        "supporting_evidence": sources, "risk_relevant": True, **details,
    }


def _field(extract_field, quote, labels):
    for label in labels:
        value = extract_field(quote, label)
        if value.get("is_filled") and value.get("field_value"):
            return {"field_name": label, "field_value": str(value["field_value"])}
    return {}


def confidentiality_detail_elements(clauses, *, extract_field):
    """Recognize completed fields and prose without borrowing a different party's duty."""
    labels = {
        "confidential_information_scope": "保密信息类别和范围",
        "confidential_personnel_scope": "涉密人员范围",
        "during_contract_confidentiality": "合同履行期间的保密义务",
        "post_termination_confidentiality": "合同终止或解除后的继续保密义务",
        "confidentiality_duration": "保密义务的持续期间",
    }
    facts = {key: [] for key in labels}
    parties = []
    current_party = ""
    actor_source = None
    unbound_group = []
    group_closed = False
    previous_article = ""
    in_confidentiality_article = False
    exceptions = {key: [] for key in ("公开信息例外", "合法取得信息例外", "独立开发信息例外", "依法披露例外")}

    def remember(key, clause, quote, **details):
        source = _fact(clause, quote, obligated_party=current_party, **details)
        if actor_source:
            source["actor_source_evidence"] = [dict(actor_source)]
        if not current_party:
            unbound_group.append(source)
        facts[key].append(source)

    for clause, heading, quote in _segments(clauses):
        article = (getattr(clause, "heading_path", None) or [""])[0]
        if article != previous_article:
            in_confidentiality_article = "保密" in article or bool(in_confidentiality_article and _party_heading(article))
            current_party = ""
            actor_source = None
            unbound_group = []
            group_closed = False
            previous_article = article
        compact = _compact(quote)
        party_heading = _party_heading(compact)
        if party_heading and (in_confidentiality_article or "保密" in heading):
            current_party = party_heading[1]
            actor_source = _fact(clause, quote, obligated_party=current_party, evidence_role="OBLIGATED_PARTY_CONTEXT")
            # A new actor starts a different field group. Unidentified facts
            # from the previous group must never become this party's evidence.
            unbound_group = []
            group_closed = False
            if current_party not in parties:
                parties.append(current_party)
            continue
        if not re.search(r"保密|涉密", heading + compact):
            continue
        if group_closed and re.search(r"(?:保密内容|保密范围|保密义务适用于|涉密人员|保密期限)[：:]", compact):
            current_party = ""
            actor_source = None
            unbound_group = []
            group_closed = False
        liability_actor = re.search(rf"(?:泄密责任|保密违约责任)[：:](?:由)?({_PARTIES})(?=违反|泄密|泄露|应|承担|负责)", compact)
        if liability_actor:
            # Production filtering can omit a short actor-only heading. The
            # explicit liability actor at the end of the same template group
            # recovers that group's actor; information ownership cannot do so.
            if not current_party:
                current_party = liability_actor[1]
                actor_source = _fact(clause, quote, obligated_party=current_party, evidence_role="OBLIGATED_PARTY_CONTEXT")
                for source in unbound_group:
                    source.update(obligated_party=current_party, actor_source_evidence=[dict(actor_source)])
                unbound_group = []
                if current_party not in parties:
                    parties.append(current_party)
            group_closed = True
        field = _field(extract_field, quote, ("保密义务适用于", "保密信息包括", "保密范围", "保密内容"))
        if field and not re.search(_DEFERRED, field["field_value"]):
            remember("confidential_information_scope", clause, quote, **field)
        elif re.search(r"(?:保密信息|保密范围)(?:包括|包含|是指|涵盖).+", compact) and not re.search(_DEFERRED, compact):
            remember("confidential_information_scope", clause, quote)
        field = _field(extract_field, quote, ("涉密人员范围", "涉密人员", "允许披露人员"))
        if field and not re.search(_DEFERRED, field["field_value"]):
            remember("confidential_personnel_scope", clause, quote, **field)
        # A court mention or a damages clause is not a disclosure exception.
        if re.search(r"例外|除外|不适用|不属于保密|不受.{0,8}保密|可以披露|允许披露|有权披露", compact):
            for label, pattern in (
                ("公开信息例外", r"公开|公众知悉|公知"),
                ("合法取得信息例外", r"合法(?:取得|获取|获得)|第三方合法|事先(?:知悉|持有)"),
                ("独立开发信息例外", r"独立(?:开发|研发|形成)"),
                ("依法披露例外", r"依法|法律法规|司法|法院|行政机关|监管机关"),
            ):
                if re.search(pattern, compact):
                    exceptions[label].append(_fact(clause, quote))
        period = _field(extract_field, quote, ("保密期限", "保密义务期限"))
        period_text = _compact(period.get("field_value") or quote)
        period_context = bool(period or "保密" in compact)
        if not period_context or re.search(_DEFERRED, period_text):
            continue
        positive = not re.search(r"不再(?:承担|负有|履行|继续)|无需(?:承担|保密|履行)|不承担保密", period_text)
        after = bool(positive and re.search(
            rf"(?:终止|解除|届满)(?:之后|以后|后).{{0,25}}(?:{_DURATION}|继续|持续|仍|有效)|"
            r"(?:保密义务|保密条款).{0,20}不因.{0,15}(?:终止|解除).{0,12}(?:失效|免除|消灭)", period_text,
        ))
        during = bool(positive and (
            re.search(r"(?:合同|履行|合作|研发)(?:有效期|存续期|期间|期)内", period_text)
            or re.search(r"自(?:首次)?(?:接触|获取|收到|获得).{0,16}(?:之日|之时|起).{0,30}(?:至|到|持续)", period_text)
            or re.search(r"(?:承担|负有|履行)保密义务|予以保密|不得向.{0,12}(?:披露|泄露)", compact)
        ))
        duration = bool(positive and (re.search(_DURATION, period_text) or re.search(
            r"长期|永久|持续有效|继续有效|仍需履行|合同(?:有效期内|履行期间|存续期间)", period_text,
        )))
        for key, covered in (("during_contract_confidentiality", during), ("post_termination_confidentiality", after), ("confidentiality_duration", duration)):
            if covered:
                remember(key, clause, quote, **period)
    elements = []
    for key, label in labels.items():
        # Actor provenance explains who owns a field; a liability sentence
        # cannot itself become direct proof of scope, personnel or duration.
        sources = facts[key]
        if parties:
            party_rows = []
            for party in parties:
                direct = [row for row in sources if row.get("obligated_party") == party]
                party_rows.append({"obligated_party": party, "required_fact": party + label,
                                   "status": "COVERED" if direct else "MISSING", "supporting_evidence": direct,
                                   "proposition": party + label + ("已有明确约定。" if direct else "")})
            missing = [row["required_fact"] for row in party_rows if row["status"] == "MISSING"]
            unknown = [row for row in sources if not row.get("obligated_party")]
            if unknown:
                unknown_label = "前组" + label + "对应的保密义务主体"
                missing.append(unknown_label)
                party_rows.append({"obligated_party": "UNKNOWN", "required_fact": unknown_label,
                                   "status": "UNCERTAIN", "supporting_evidence": unknown,
                                   "proposition": unknown_label + "尚未明确。"})
            state = "PARTIALLY_COVERED" if missing and sources else "MISSING" if missing else "COVERED"
            elements.append(_element(key, label, sources, status=state, residuals=missing,
                                     party_coverage=party_rows, source_fact_key="confidentiality." + key))
        else:
            elements.append(_element(key, label, sources, source_fact_key="confidentiality." + key))
    exception_sources = list({(row["clause_id"], row["quote"]): row for values in exceptions.values() for row in values}.values())
    missing = [label for label, sources in exceptions.items() if not sources]
    elements.append(_element("confidentiality_exceptions", "公开信息、合法取得、独立开发及依法披露例外", exception_sources,
                             status="PARTIALLY_COVERED" if missing and exception_sources else "MISSING" if missing else "COVERED",
                             residuals=missing, source_fact_key="confidentiality.exceptions"))
    return elements


def ancillary_service_detail_elements(clauses, *, extract_field):
    """Evaluate ordinary support content, duration, method and fees in their own article."""
    specs = {
        "service_existence": "技术服务或培训安排", "service_content": "技术服务具体内容",
        "service_period": "技术服务期限", "service_method": "技术服务方式", "service_fee": "技术服务费用安排",
    }
    facts = {key: [] for key in specs}
    for clause, heading, quote in _segments(clauses):
        compact = _compact(quote)
        context = bool(re.search(_SERVICE, heading + compact))
        if not context or re.search(r"不提供.{0,8}(?:技术服务|技术支持|培训)|不涉及技术服务", compact):
            continue
        field = _field(extract_field, quote, ("技术服务内容", "技术支持内容", "服务内容", "内容"))
        content = bool(field and not re.search(_DEFERRED, field["field_value"])) or bool(re.search(
            r"(?:提供|负责|包括|包含|内容[：:]).{0,40}(?:系统部署|参数配置|故障排查|安装调试|技术培训|人员培训|技术指导)", compact,
        ))
        method_field = _field(extract_field, quote, ("地点和方式", "服务方式", "技术服务方式", "方式"))
        method = bool(method_field and not re.search(_DEFERRED, method_field["field_value"])) or bool(re.search(r"远程(?:支持|服务|指导)|现场(?:支持|服务|指导)|电子邮件|线上培训", compact))
        period = bool(re.search(rf"(?:提供|持续|为期|期限|期限为|交付后|验收后).{{0,18}}{_DURATION}", compact)
                      and not re.search(_DEFERRED, compact))
        fee = bool(re.search(r"(?:总价|价款|费用).{0,15}(?:已)?包含.{0,20}(?:服务|支持|培训).{0,8}(?:费|费用)|(?:服务|支持|培训)(?:费|费用).{0,15}(?:包含在|计入|纳入)|(?:费用|服务费)[：:].{0,12}(?:免费|无偿|\d)|(?:免费|无偿)(?:提供)?(?:技术服务|技术支持|培训)", compact)
                   and not re.search(_DEFERRED, compact))
        for key, covered, details in (("service_content", content, field), ("service_method", method, method_field),
                                      ("service_period", period, {}), ("service_fee", fee, {})):
            if covered:
                facts[key].append(_fact(clause, quote, source_domain="ANCILLARY_TECHNICAL_SERVICE", **details))
        if content or period or re.search(r"(?:应|须|负责|提供).{0,25}" + _SERVICE, compact):
            facts["service_existence"].append(_fact(clause, quote, source_domain="ANCILLARY_TECHNICAL_SERVICE"))
    return [_element(key, label, facts[key], source_fact_key="technical_service." + key) for key, label in specs.items()]


def improvement_license_detail_elements(clauses):
    """Retain priority and negotiation principles without inventing settled licence terms."""
    segments = [(clause, heading, quote) for clause, heading, quote in _segments(clauses)
                if re.search(_IMPROVEMENT, heading + quote)]
    # Reuse the established directional extractor, but never feed it unrelated
    # primary-licence, fee, confidentiality or ordinary project-delivery clauses.
    analysis = analyze_improvement_license_facts("\n".join(quote for _, _, quote in segments))
    priority, negotiation = [], []
    ownership = {"licensee_improvement_ownership": [], "licensor_improvement_ownership": []}
    terms = {key: [] for key in ("license_fee", "license_territory", "license_duration", "commercial_use", "improvement_sublicense")}
    for clause, heading, quote in segments:
        compact = _compact(quote)
        if re.search(r"优先(?:获得许可|取得许可|许可权|被许可|许可)", compact) and not re.search(r"不(?:享有|具有)|无.{0,6}优先", compact):
            priority.append(_fact(clause, quote))
        if re.search(r"许可|使用", compact) and re.search(_DEFERRED, compact):
            negotiation.append(_fact(clause, quote))
        for key, actors in (("licensee_improvement_ownership", r"甲方|买方|受让方|被许可方"), ("licensor_improvement_ownership", r"乙方|卖方|让与方|出让方|许可方")):
            if re.search(rf"(?:归|归属[：:]?|属于)(?:{actors})(?:所有)?", compact) and re.search(_IMPROVEMENT + r"|新技术成果", compact):
                ownership[key].append(_fact(clause, quote))
        for unit in re.split(r"[，,]", quote):
            unit_text = _compact(unit)
            if re.search(_DEFERRED, unit_text):
                continue
            # The current sentence or a licence-specific heading must bind the
            # value to improvement use, not just to the surrounding contract.
            if not re.search(r"许可|使用|分享", compact + heading):
                continue
            patterns = {
                "license_fee": rf"(?:许可费|许可价格|许可对价|使用费|定价).{{0,20}}(?:{_NUMBER}|按|依据|参照)|(?:免费|无偿).{{0,12}}(?:许可|使用)|(?:许可|使用).{{0,12}}(?:免费|无偿)",
                "license_territory": r"(?:许可|使用)?(?:地域|区域|范围)[：:为是限于]*.{0,12}(?:中国|全球|全国|境内|境外|地区|省|市)|(?:全球|全国|中国境内).{0,12}(?:许可|使用)",
                "license_duration": rf"(?:许可|使用)(?:期限|期间|期).{{0,12}}{_DURATION}|(?:许可|使用).{{0,12}}(?:永久|合同有效期)|(?:永久|合同有效期内).{{0,12}}(?:许可|使用)",
                "commercial_use": r"(?:可以|允许|有权|不得|禁止|仅限).{0,14}(?:商业使用|商业化|商业目的)|(?:商业使用|商业化).{0,12}(?:允许|禁止|同意|限制)",
                "improvement_sublicense": r"(?:可以|允许|有权|不得|禁止|须经.{0,10}同意).{0,12}(?:分许可|转许可|再许可)|(?:分许可|转许可|再许可).{0,15}(?:须经|应经|不得|禁止|允许)",
            }
            for key, pattern in patterns.items():
                if re.search(pattern, unit_text):
                    terms[key].append(_fact(clause, quote))
    elements = [_element(key, label, ownership[key], source_fact_key="improvement." + key) for key, label in (
        ("licensee_improvement_ownership", "甲方或受让方独立改进成果归属"),
        ("licensor_improvement_ownership", "乙方或提供方独立改进成果归属"),
    )]
    elements.append(_element("priority_license", "改进成果优先获得许可的权利", priority, source_fact_key="improvement.priority_license"))
    condition_rows = [_element(key, label, terms[key], source_fact_key="improvement." + key) for key, label in (
        ("license_fee", "改进成果许可费或定价机制"), ("license_territory", "改进成果许可地域"),
        ("license_duration", "改进成果许可期限"), ("commercial_use", "改进成果商业使用边界"),
        ("improvement_sublicense", "改进成果分许可条件"),
    )]
    gaps = [row["required_fact"] for row in condition_rows if row["status"] == "MISSING"]
    principles = list({(row["clause_id"], row["quote"]): row for row in [*priority, *negotiation]}.values())
    elements.append(_element("priority_or_negotiated_license", "优先许可或另行协商机制", principles,
                             status="PARTIALLY_COVERED" if principles and gaps else "COVERED" if principles else "MISSING",
                             residuals=gaps, risk_relevant=False, source_fact_key="improvement.license_principle",
                             **({"proposition": "优先许可或另行协商机制已有原则安排，但" + "、".join(gaps) + "尚未明确。"} if principles and gaps else {}),
                             stable_analysis_status=analysis.get("arrangement_status")))
    return [*elements, *condition_rows]
