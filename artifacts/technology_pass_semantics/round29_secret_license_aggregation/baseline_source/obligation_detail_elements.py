"""Evidence-bound details for confidentiality, ancillary support and improvements.

The engine supplies its existing semantic-field extractor, avoiding a second
implementation of template blank detection or an import cycle with the engine.
Transaction applicability remains the caller's responsibility.
"""
import re
from review_v2.proposition_scope import component_states, scoped_propositions

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


def _delivery_sources(clauses):
    """Keep a delivery verb with each numbered deliverable, not an IP mention."""
    for clause in clauses:
        prefix = None
        for match in re.finditer(r"[^。；;\n]+[。；;]?", clause.text):
            quote = match[0].strip()
            headings = {re.sub(r'\s+', '', str(v)) for v in (
                getattr(clause, 'title', ''), getattr(clause, 'heading', ''),
                ' '.join(getattr(clause, 'heading_path', []) or [])) if v}
            if re.sub(r'\s+', '', quote) in headings and not re.search(
                    r'(?:应|须|必须|承诺|负责).{0,20}(?:提供|交付|提交)', quote):
                continue
            if re.search(r"(?:应|须|必须).{0,16}(?:提交|交付|提供)[：:]$", quote):
                prefix = match.start()
                continue
            # A colon opens an enumeration. Semicolon/newline noun phrases
            # carry that predicate even when the author omitted numbering.
            # A finite new obligation/negation closes it instead of borrowing
            # the preceding delivery verb.
            listed = bool(prefix is not None and (
                re.match(r"^(?:\d+|[一二三四五六七八九十]+)[、.．]", quote)
                or not re.search(r"双方|任何一方|[甲乙丙丁]方|未|不(?:得|再|予)|应|必须|通过|约定|承担|保存期限", quote)))
            if listed:
                yield clause, quote, clause.text[prefix:match.end()].strip()
                if quote.endswith('。'):
                    prefix = None
                continue
            prefix = None
            # A supplied document used as the subject of a warranty, exception
            # or damages clause is not a promise to deliver that document.
            # Require an operative predicate in such sentences, not just the
            # verb embedded in a noun phrase ("甲方提供的资料产生的纠纷").
            remedial = bool(re.search(r"纠纷|赔偿|免责|除外|不作保证|责任|存在错误", quote))
            performance = bool(re.search(r"(?:应|须|必须|负责|承诺).{0,20}(?:提交|交付|提供)", quote))
            if (re.search(r"提交|交付|提供", quote)
                    and (not remedial or performance)
                    and not re.search(r"无需|不(?:予|再)?(?:提交|交付|提供)|未(?:另行)?(?:提交|交付|提供|约定)", quote)):
                yield clause, quote, quote


def development_document_elements(clauses):
    """Each document type requires its own delivery predicate and exact span."""
    from review_v2.technology_fact_ontology import DOCUMENTS, document_concept, document_pattern, mentions_document
    from review_v2.contract_facts import canonical_fact_key
    keys = ('source_and_executable_delivery', 'generic_technical_documentation',
            'interface_document_delivery', 'architecture_document_delivery',
            'deployment_document_delivery', 'operation_document_delivery',
            'installation_document_delivery', 'test_report_delivery', 'defect_list_delivery')
    definitions = {key: (DOCUMENTS[document_concept(key)][0], document_pattern(key)) for key in keys}
    facts = {key: [] for key in definitions}
    for clause, object_text, quote in _delivery_sources(clauses):
        for key, (_, pattern) in definitions.items():
            if mentions_document(key, object_text, str(getattr(clause, 'heading', '')) + clause.text):
                facts[key].append(_fact(clause, quote, source_domain="TECHNICAL_MATERIAL"))
    return [_element(key, label, facts[key], source_fact_key=canonical_fact_key("development_documents." + key),
                     query_patterns=[pattern, "提交|交付|提供"])
            for key, (label, pattern) in definitions.items()]


def development_result_elements(clauses):
    """Ownership, use, disclosure and disposition are not interchangeable facts."""
    from review_v2.technology_fact_ontology import ACTION_PATTERNS
    definitions = {
        "technical_secret_result_ownership": ("研发成果权属", r"(?:本项目|开发|研发|技术秘密|前景).{0,90}(?:成果|源代码|技术文档|技术信息).{0,50}归.{0,15}所有"),
        "commissioning_party_use_right": ("委托方使用开发成果的权利", r"(?:甲方|委托方).{0,8}(?:有权|可以|可).{0,12}(?:使用|商业利用).{0,15}(?:成果|开发软件|技术)"),
        "developer_use_restriction": ("开发方使用项目成果的边界", r"(?:乙方|开发方).{0,90}(?:不得|未经.{0,12}同意).{0,25}(?:使用|商业利用)|未经.{0,12}同意.{0,12}(?:乙方|开发方).{0,12}不得.{0,15}(?:使用|商业利用)"),
        "third_party_disclosure_transfer": ("成果向第三方许可或转让的条件", r"(?:开发成果|软件|源代码|技术成果).{0,30}(?:许可|转让).{0,15}第三方|(?:不得|须经.{0,12}同意).{0,20}(?:许可|转让).{0,15}(?:成果|软件|源代码)"),
        "developer_copy_retention": ("开发方副本留存范围和期限", r"(?:乙方|开发方).{0,20}(?:保留|留存).{0,20}(?:副本|复制件).{0,30}(?:期限|范围|仅限|日|年)"),
        "confidentiality_obligation": ("研发非公开信息的保密义务", r"(?:不得|禁止).{0,30}(?:披露|泄露).{0,40}|(?:应|须).{0,10}(?:予以|承担)?保密"),
        "post_project_use_and_disposition": ("项目结束后的资料返还或删除", r"(?:终止|解除|项目结束).{0,45}(?:返还|删除|销毁).{0,15}(?:资料|代码|成果|副本)"),
    }
    facts = {key: [] for key in definitions}
    for clause, heading, quote in _segments(clauses):
        text = _compact(quote)
        for key, (_, pattern) in definitions.items():
            if key == "confidentiality_obligation" and not re.search(r"保密|秘密", heading + clause.text):
                continue
            if re.search(pattern, text):
                facts[key].append(_fact(clause, quote, source_domain="DEVELOPMENT_RESULT"))
        if re.search(r'成果|技术|组件|代码', text):
            for key, actor, action in (
                ('commissioning_party_use_right', r'甲方|委托方', 'technical_use_entitlement'),
                ('developer_use_restriction', r'乙方|开发方', 'limited_technical_use')):
                # Restrict the predicate to this actor's proposition; a grant
                # to the other party in the same sentence is not interchangeable.
                for actor_match in re.finditer(actor, text):
                    tail = text[actor_match.end():]
                    if re.match(r'^.{0,5}' + ACTION_PATTERNS[action], tail):
                        facts[key].append(_fact(clause, quote, source_domain='DEVELOPMENT_RESULT',
                                                scope_limited=True))
                        break
    documents = development_document_elements(clauses)
    delivery = [source for e in documents if e["status"] == "COVERED"
                for source in e["supporting_evidence"]]
    elements = [_element(key, label, facts[key], source_fact_key="development_result." + key,
                         query_patterns=[pattern]) for key, (label, pattern) in definitions.items()]
    for element in elements:
        sources = element['supporting_evidence']
        if sources and all(s.get('scope_limited') for s in sources):
            gap = {
                'commissioning_party_use_right': '委托方对专门开发成果的使用权限及使用范围',
                'developer_use_restriction': '开发方对项目专门成果的再使用条件及范围',
            }[element['element_id']]
            element.update(status='PARTIALLY_COVERED', residual_gap=gap, search_targets=[gap],
                           proposition=element['required_fact'] + '已有范围限定的约定，其他成果的使用边界仍待明确。')
    elements.append(_element("source_algorithm_document_delivery", "源代码及技术资料交付安排", delivery,
                             source_fact_key="development_result.source_algorithm_document_delivery"))
    return elements


def development_subject_elements(clauses):
    definitions = {
        "project_identity": ("研发项目身份", r"项目名称[：:].+|(?:开发|研发)(?:名为|一套|一种).{2,40}(?:系统|平台|技术|设备)"),
        "functional_scope": ("研发功能范围", r"(?:主要功能|功能包括|功能范围|功能模块|开发内容)[：:]|实现.{0,50}(?:功能|算法|处理)"),
        "performance_scope": ("研发履行期限或节点", r"(?:阶段|最终|开发周期|开发期限).{0,45}(?:日前|日内|月底|个月|完成|提交)"),
    }
    facts = {key: [] for key in definitions}
    for clause, _, quote in _segments(clauses):
        for key, (_, pattern) in definitions.items():
            if re.search(pattern, _compact(quote)):
                facts[key].append(_fact(clause, quote))
    return [_element(key, label, facts[key], source_fact_key="development_subject." + key,
                     query_patterns=[pattern]) for key, (label, pattern) in definitions.items()]


def development_acceptance_detail_elements(clauses):
    """Acceptance methods never entail delivery of reports, cases or records."""
    definitions = {
        "acceptance_metrics": ("验收标准", r"(?:准确率|召回率|误差|运行|功能|响应时间|系统).{0,35}(?:不低于|不高于|不少于|不超过|小时|实现|一致)"),
        "acceptance_method": ("验收方法", r"(?:进行|采用|通过|组织).{0,35}(?:功能测试|数据测试|现场运行测试|性能测试|现场测试)"),
        "test_case_requirement": ("测试用例要求", r"(?:提供|交付|提交|编制|制定).{0,15}测试用例|测试用例.{0,15}(?:提供|交付|提交|编制|制定)"),
        "test_report_delivery": ("测试报告交付", r"(?:提供|交付|提交).{0,15}测试报告|测试报告.{0,15}(?:提供|交付|提交)"),
        "acceptance_record_requirement": ("验收记录要求", r"(?:形成|保存|签署|提交|交付).{0,15}验收记录|验收记录.{0,15}(?:形成|保存|签署|提交|交付)"),
        "acceptance_dispute_verification": ("验收争议的第三方检测或复测机制", r"(?:第三方|独立).{0,15}(?:检测|复测)|(?:争议|异议).{0,25}复测"),
    }
    sources = {key: [] for key in definitions}
    for clause, heading, quote in _segments(clauses):
        if not re.search(r"验收|测试|检测|技术要求|技术指标", heading + quote):
            continue
        if re.search(r"无需|不(?:提供|提交|交付)|另行协商|尚未", quote):
            continue
        for key, (_, pattern) in definitions.items():
            if key == "acceptance_metrics" and not re.search(r"验收|技术要求|技术指标", heading + quote):
                continue
            if re.search(pattern, _compact(quote)):
                sources[key].append(_fact(clause, quote))
    # The same delivered test report cannot be present in TC-13-01 and absent
    # in TC-13-03 just because the latter uses a different local vocabulary.
    from review_v2.contract_facts import canonical_fact_key
    documents = {e['element_id']: e for e in development_document_elements(clauses)}
    sources['test_report_delivery'] = documents['test_report_delivery']['supporting_evidence']
    return [_element(key, label, sources[key], source_fact_key=canonical_fact_key("development_acceptance." + key))
            for key, (label, _) in definitions.items()]


def confidentiality_detail_elements(clauses, *, extract_field):
    """Recognize completed fields and prose without borrowing a different party's duty."""
    labels = {
        "confidential_information_scope": "保密信息类别和范围",
        "confidential_personnel_scope": "涉密人员范围",
        "during_contract_confidentiality": "合同履行期间的保密义务",
        "post_termination_confidentiality": "合同终止或解除后的继续保密义务",
        "confidentiality_duration": "保密义务的持续期间",
    }
    missing_quotes = [_compact(row['quote']) for row in scoped_propositions('\n'.join(c.text for c in clauses))
                      if row['polarity'] == 'MISSING']
    facts = {key: [] for key in labels}
    parties = []
    current_party = ""
    actor_source = None
    unbound_group = []
    group_closed = False
    previous_article = ""
    in_confidentiality_article = False
    exception_context = False
    exception_header = None
    exceptions = {key: [] for key in ("公开信息例外", "合法取得信息例外", "独立开发信息例外", "依法披露例外")}

    def remember(key, clause, quote, **details):
        mutual = re.search(r'(?:双方|各方|任何一方).{0,120}(?:承担|负有|履行)保密义务', _compact(quote))
        explicit_mutual = bool(mutual and not re.search(_PARTIES, mutual[0]))
        source_party = '双方' if explicit_mutual else current_party
        source = _fact(clause, quote, obligated_party=source_party, **details)
        if actor_source:
            source["actor_source_evidence"] = [dict(actor_source)]
        if not source_party:
            unbound_group.append(source)
        facts[key].append(source)

    for clause, heading, quote in _segments(clauses):
        article = (getattr(clause, "heading_path", None) or [""])[0]
        if article != previous_article:
            exception_context = False
            exception_header = None
            in_confidentiality_article = "保密" in article or bool(in_confidentiality_article and _party_heading(article))
            current_party = ""
            actor_source = None
            unbound_group = []
            group_closed = False
            previous_article = article
        compact = _compact(quote)
        if any(compact in missing or missing in compact for missing in missing_quotes):
            exception_context = False
            exception_header = None
            continue
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
        elif re.search(r"(?:保密信息|保密范围)(?:包括|包含|是指|涵盖).+|以下信息(?:均)?属于保密信息[：:].+|(?:资料|数据|信息|计划).{0,100}(?:均)?属于保密信息", compact) and not re.search(r"不属于保密|" + _DEFERRED, compact):
            remember("confidential_information_scope", clause, quote)
        elif (re.search(r"(?:对|知悉|获得|接触).{0,120}(?:资料|数据|信息|代码|算法|参数).{0,35}(?:承担|负有)(?:合理|相应)?保密义务", compact)
              and not re.search(r"(?:不承担|免除|无需承担).{0,8}保密|" + _DEFERRED, compact)):
            # An obligation's explicitly named object defines its scope just
            # as a definition field does; it is not another party's remedy.
            remember("confidential_information_scope", clause, quote)
        field = _field(extract_field, quote, ("涉密人员范围", "涉密人员", "允许披露人员"))
        if field and not re.search(_DEFERRED, field["field_value"]):
            remember("confidential_personnel_scope", clause, quote, **field)
        elif re.search(r'(?:仅可|只可|仅限|只限)[^。；]{0,20}(?:知悉必要|必要知悉|有必要知悉)[^。；]{0,20}(?:员工|人员)|仅因[^。；]{0,30}确有必要的人员可以接触', compact):
            remember("confidential_personnel_scope", clause, quote)
        # A court mention or a damages clause is not a disclosure exception.
        if re.search(r"(?:以下|下列)信息不属于(?:本合同(?:项下)?)?保密(?:信息|范围)|保密.{0,8}(?:例外|除外)[：:]", compact):
            exception_context = True
            exception_header = _fact(clause, quote)
        elif exception_context and not (
            re.match(r"(?:\d+[.、．]|[（(]\d+[）)])", compact)
            or re.search(r'^(?:已经|此后|其后|接收方|接收时|非因|从|根据|依法|(?:未|没有|不曾)使用).{0,60}(?:公开|公共领域|合法|取得|获得|掌握|独立(?:开发|研发|形成)|披露)', compact)
        ):
            exception_context = False
        if exception_context or re.search(r"例外|除外|不适用|不属于保密|不受.{0,8}保密|可以.{0,20}披露|允许披露|有权披露|(?:法律法规|有权机关).{0,25}披露.{0,12}不视为违约|(?:法律|监管|司法机关).{0,35}必须披露.{0,30}(?:可|应).{0,15}披露", compact):
            for label, pattern in (
                ("公开信息例外", r"公开|公共领域|公众知悉|公知"),
                ("合法取得信息例外", r"合法(?:取得|获取|获得)|(?:从|自|由)合法第三[方人].{0,12}(?:取得|获取|获得)|第三方合法|事先(?:知悉|持有)"),
                ("独立开发信息例外", r"独立(?:开发|研发|形成)"),
                ("依法披露例外", r"依法|法律(?:法规)?|司法|法院|行政机关|监管机关|有权机关"),
            ):
                if re.search(pattern, compact):
                    if exception_context and exception_header and exception_header['clause_id'] == clause.clause_id:
                        start = clause.text.find(exception_header['quote'])
                        end = clause.text.find(quote, start) + len(quote)
                        exceptions[label].append(_fact(clause, clause.text[start:end]))
                    else:
                        exceptions[label].append(_fact(clause, quote, **(
                            {'domain_context_evidence': [exception_header]} if exception_context and exception_header else {})))
        period = _field(extract_field, quote, ("保密期限", "保密义务期限"))
        period_text = _compact(period.get("field_value") or quote)
        period_context = bool(period or "保密" in compact or
                              ("保密" in heading and re.search(r"不得向.{0,12}(?:披露|泄露)", compact)))
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
            or re.search(r"(?:承担|负有|履行)(?:合理|相应)?保密义务|予以保密|不得向.{0,12}(?:披露|泄露)", compact)
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
                direct = [row for row in sources if row.get("obligated_party") in {party, '双方'}]
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
                             residuals=missing, source_fact_key="confidentiality.exceptions",
                             component_coverage=component_states([
                                 ('confidentiality_exception_' + key, label, exceptions[label])
                                 for key, label in zip(('public', 'lawful_acquisition', 'independent_development', 'legal_disclosure'), exceptions)])))
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
    ownership_boundary = {key: [] for key in ownership}
    terms = {key: [] for key in ("license_fee", "license_territory", "license_duration", "commercial_use", "improvement_sublicense")}
    for clause, heading, quote in segments:
        compact = _compact(quote)
        if re.search(r"优先(?:获得许可|取得许可|许可权|被许可|许可)", compact) and not re.search(r"不(?:享有|具有)|无.{0,6}优先", compact):
            priority.append(_fact(clause, quote))
        if re.search(r"许可|使用", compact) and re.search(_DEFERRED, compact):
            negotiation.append(_fact(clause, quote))
        for key, actors in (("licensee_improvement_ownership", r"甲方|买方|受让方|被许可方"), ("licensor_improvement_ownership", r"乙方|卖方|让与方|出让方|许可方")):
            improvement_object = re.search(_IMPROVEMENT + r"|新技术成果", compact) or (
                re.search(_IMPROVEMENT, heading) and re.search(r'独立开发|自行形成|后续升级', compact))
            if improvement_object and re.search(r'不(?:当然)?属于|不归|并非', compact):
                if re.search(rf'(?:{actors}).{{0,25}}独立开发', compact):
                    ownership_boundary[key].append(_fact(clause, quote))
            elif re.search(rf"(?:归|归属[：:]?|属于)(?:{actors})(?:所有)?", compact) and improvement_object:
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
    elements = [_element(key, label, ownership[key] or ownership_boundary[key],
        status='COVERED' if ownership[key] else 'PARTIALLY_COVERED' if ownership_boundary[key] else 'MISSING',
        residuals=[] if ownership[key] else [label], source_fact_key="improvement." + key) for key, label in (
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


def improvement_notification_elements(clauses):
    positive, absent = [], []
    for clause, heading, quote in _segments(clauses):
        text = _compact(quote)
        if not re.search(_IMPROVEMENT, heading + quote) or not re.search(r'通知|告知|披露', text):
            continue
        if re.search(r'未(?:另行)?约定|未明确|尚无|无需|不必|不负有', text):
            absent.append(_fact(clause, quote))
        # The notice must be the operative duty, concern improvements and be
        # addressed to the counterparty. Receiving an acceptance notice, or
        # disclosing information to third parties, proves none of these.
        elif (re.search(_IMPROVEMENT + r'|该成果|上述成果', text)
              and re.search(r'(?:应当?|须|必须|有义务)(?:(?!收到|接到|接收).){0,30}'
                            r'(?:通知|告知)', text)
              and re.search(r'(?:向|通知|告知)(?:另一方|对方|[甲乙丙]方|许可方|被许可方)', text)):
            positive.append(_fact(clause, quote))
    return [_element('improvement_result_notification', '改进成果形成后的通知义务', positive,
        source_fact_key='improvement.notification', explicit_absence_evidence=absent)]
