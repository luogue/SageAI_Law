"""Source-bound atomic patent and failure requirements for commissioned R&D.

Presence is deliberately independent from the commercial direction of an
allocation.  A loss-sharing clause does not prove payment settlement; ownership
does not prove the application paperwork or the inventor-confirmation process.
Existing adverse/conflicting-allocation evaluation remains the caller's job.
"""
from __future__ import annotations

import re


ENTRUSTED_PATENT_REQUIREMENTS = {
    "patent_application_right_ownership": "专利申请权归属",
    "patent_right_after_grant": "专利授权后的专利权归属",
    "inventor_authorship": "实际完成人的发明人署名权",
    "application_filing_control": "专利申请决定和申请控制",
    "document_signature_cooperation": "专利申请文件签署配合",
    "registration_cooperation": "专利申请、登记及权利取得材料配合",
    "filing_cost_allocation": "专利申请费用承担",
    "inventor_confirmation": "发明人身份确认流程",
}

DEVELOPMENT_FAILURE_REQUIREMENTS = {
    "no_fault_technical_risk_trigger": "无过错技术风险导致研发失败的触发情形",
    "no_fault_technical_risk_allocation": "无过错技术风险损失分担",
    "failed_development_incurred_cost_settlement": "研发失败时已发生研发费用结算",
    "paid_fee_refund": "研发失败时已付款处理",
    "unpaid_fee_obligation": "研发失败时未付款处理",
    "failed_project_stage_result_disposition": "研发失败时阶段成果处置",
    "failed_project_source_code_disposition": "研发失败时源代码处置",
    "failed_project_material_disposition": "研发失败时研发资料处置",
}

_PATENT = r"专利(?:申请)?|申请专利"
_COOPERATE = r"配合|协助|提供.{0,8}协作"
_DEFERRED = r"另行(?:协商|商定|约定)|有待(?:明确|确定)|待(?:协商|商定|约定)|原则上|原则性"
_NO_ARRANGEMENT = r"未(?:明确|约定|规定)|尚未(?:明确|约定|规定)|尚无"
_FAILURE = r"研发失败|开发失败|研究开发失败|技术风险|技术困难|无法实现.{0,8}(?:研发|开发|技术|约定)?目标"
_SETTLEMENT = r"结算|结清|支付|退还|退回|返还|退付|免付|调减|扣除|抵扣"
_DISPOSITION = r"移交|交接|交付|返还|销毁|删除|归.{0,18}所有|使用权|继续使用|处置"

# Search the unresolved action/parameter, never the sentence describing a
# partly-covered state.  These labels are positive, objective requirements.
_PARTIAL_RESIDUALS = {
    "patent_application_right_ownership": "专利申请权的确定归属",
    "patent_right_after_grant": "专利授权后的确定权利归属",
    "inventor_authorship": "实际完成人的确定署名安排",
    "application_filing_control": "专利申请决定及申请控制程序",
    "document_signature_cooperation": "专利申请文件签署的具体配合义务",
    "registration_cooperation": "专利申请、登记及权利取得所需材料的具体提供安排",
    "filing_cost_allocation": "专利申请费用的具体分担方式",
    "inventor_confirmation": "发明人身份的具体确认流程",
    "no_fault_technical_risk_trigger": "无过错技术风险的具体认定条件",
    "no_fault_technical_risk_allocation": "无过错技术风险损失的具体分担方式",
    "failed_development_incurred_cost_settlement": "研发失败时已发生研发费用的具体结算方式",
    "paid_fee_refund": "研发失败时已付款的具体结算处理",
    "unpaid_fee_obligation": "研发失败时未付款的具体支付或免付安排",
    "failed_project_stage_result_disposition": "研发失败时阶段成果的具体处置安排",
    "failed_project_source_code_disposition": "研发失败时源代码的具体处置安排",
    "failed_project_material_disposition": "研发失败时研发资料的具体处置安排",
}


def _units(clauses):
    for clause in clauses:
        context = " ".join([
            *(getattr(clause, "heading_path", None) or []),
            getattr(clause, "title", "") or "",
        ])
        sentences = [part.strip() for part in re.split(r"[。；;\n]", clause.text) if part.strip()]
        for sentence in sentences:
            yield clause, sentence, re.sub(r"\s+", "", sentence), context


def _evidence(clause, quote, domain, *, principle=False):
    return {
        "clause_id": clause.clause_id,
        "quote": quote,
        "source_domain": domain,
        "support_strength": "PRINCIPLE_ONLY" if principle else "DIRECT",
    }


def _add(facts, key, clause, quote, domain, *, principle=False):
    evidence = _evidence(clause, quote, domain, principle=principle)
    if evidence not in facts[key]:
        facts[key].append(evidence)


def _positive_match(pattern, text):
    """Negation of this predicate, not an unrelated later duty, controls it."""
    for match in re.finditer(pattern, text):
        prefix = text[max(0, match.start() - 4):match.start()]
        if not re.search(r"(?:不|未|无权|不得|无需|无须|不必)$", prefix):
            return True
    return False


def _elements(requirements, facts):
    result = []
    for key, label in requirements.items():
        sources = facts[key]
        direct = [source for source in sources if source["support_strength"] == "DIRECT"]
        supporting = direct or sources
        status = "COVERED" if direct else "PARTIALLY_COVERED" if supporting else "MISSING"
        # A partial proposition quotes only the general arrangement actually
        # supplied; it must not turn assistance into specific signed paperwork.
        proposition = "；".join(dict.fromkeys(source["quote"] for source in supporting)) if supporting else label
        residual = _PARTIAL_RESIDUALS[key] if status == "PARTIALLY_COVERED" else label
        result.append({
            "element_id": key,
            "source_fact_key": key,
            "required_fact": label,
            "status": status,
            "proposition": proposition,
            "risk_relevant": True,
            "residual_gap": residual if status != "COVERED" else "",
            "search_targets": [residual],
            "bound_evidence_ids": list(dict.fromkeys(source["clause_id"] for source in supporting)),
            "supporting_evidence": supporting,
        })
    return result


def entrusted_patent_application_elements(clauses):
    """Return patent ownership and procedure states without group inference.

    An express entitlement to apply proves application-right ownership, not
    granted-patent ownership.  General assistance is partial support for the
    paperwork requirements, not complete proof of signatures or documents.
    """
    facts = {key: [] for key in ENTRUSTED_PATENT_REQUIREMENTS}
    for clause, quote, text, context in _units(clauses):
        patent_context = bool(re.search(_PATENT, text + context))
        if re.search(_NO_ARRANGEMENT, text) and not re.search(_DEFERRED, text):
            continue
        deferred = bool(re.search(_DEFERRED, text))
        ownership = _positive_match(
            r"专利申请权.{0,25}(?:归|属于|由).{0,25}(?:所有|享有)|"
            r"(?:享有|拥有|取得|具有).{0,8}(?:申请专利的权利|专利申请权)|"
            r"专利申请权(?:归属)?[：:].+|专利申请权归(?:甲方|乙方|双方|委托方|受托方|开发方)", text,
        )
        if ownership:
            _add(facts, "patent_application_right_ownership", clause, quote, "PATENT_APPLICATION", principle=deferred)
        grant = bool(re.search(
            r"(?:专利授权后|授权后的专利权|专利权归属|专利权归|取得专利权后)", text,
        )) and _positive_match(r"归.{0,25}(?:所有|享有)|由.{0,25}享有|属于", text)
        if grant and not re.search(r"未(?:取得|获得|授权)|尚未授权", text):
            _add(facts, "patent_right_after_grant", clause, quote, "PATENT_APPLICATION", principle=deferred)
        if re.search(r"(?:发明人|设计人|完成.{0,8}人员|完成人).{0,25}(?:署名权|有权署名)|享有.{0,8}发明人署名权", text):
            if not re.search(r"不享有|无权署名|不得署名", text):
                _add(facts, "inventor_authorship", clause, quote, "PATENT_APPLICATION", principle=deferred)
        control = patent_context and bool(re.search(
            r"(?:是否|申请的时间|申请时间|申请策略).{0,18}(?:申请|决定)|"
            r"(?:专利申请|申请专利).{0,20}(?:决定|批准|控制)|"
            r"(?:决定|批准).{0,12}(?:专利申请|申请专利)|"
            r"未经.{0,15}(?:同意|批准).{0,12}不得.{0,15}申请|"
            r"不得以.{0,20}名义.{0,10}(?:申请|提出权利申请)", text,
        ))
        if control:
            _add(facts, "application_filing_control", clause, quote, "PATENT_APPLICATION", principle=deferred)
        elif ownership:
            _add(facts, "application_filing_control", clause, quote, "PATENT_APPLICATION", principle=True)

        cooperation = patent_context and _positive_match(_COOPERATE, text)
        signature = patent_context and _positive_match(r"签署|签字|盖章", text) and bool(re.search(r"申请文件|专利.{0,8}文件|请求书|声明书", text))
        if signature:
            _add(facts, "document_signature_cooperation", clause, quote, "PATENT_APPLICATION", principle=deferred)
        elif cooperation:
            _add(facts, "document_signature_cooperation", clause, quote, "PATENT_APPLICATION", principle=True)

        materials = patent_context and bool(re.search(r"材料|文件|资料|证明", text)) and _positive_match(r"配合|协助|提交|提供|交付", text)
        if materials:
            # A list limited to application documents does not establish later
            # registration/acquisition cooperation; retain its real subset.
            later_steps = bool(re.search(r"登记|权利取得|授权|相关手续|全部手续", text))
            _add(facts, "registration_cooperation", clause, quote, "PATENT_APPLICATION", principle=deferred or not later_steps)
        elif cooperation:
            _add(facts, "registration_cooperation", clause, quote, "PATENT_APPLICATION", principle=True)

        if patent_context and re.search(r"申请费|专利.{0,5}费用|申请.{0,5}费用|代理费", text) and re.search(r"承担|支付|负担|由.{0,20}负责", text):
            _add(facts, "filing_cost_allocation", clause, quote, "PATENT_APPLICATION", principle=deferred)
        if re.search(r"发明人|设计人|完成人", text) and re.search(r"确认|核定|确定|审核", text):
            if re.search(r"双方|各方|书面|名单|程序|流程|依据|根据|签字|签署|由.{0,15}确认", text):
                _add(facts, "inventor_confirmation", clause, quote, "PATENT_APPLICATION", principle=deferred)
    return _elements(ENTRUSTED_PATENT_REQUIREMENTS, facts)


def development_failure_elements(clauses):
    """Keep no-fault loss allocation distinct from each financial/output item.

    Routine delivery and payment clauses are outside this event domain.  These
    are presence states; whether an express no-refund allocation is adverse is
    evaluated separately against the current review stance by the rule layer.
    """
    facts = {key: [] for key in DEVELOPMENT_FAILURE_REQUIREMENTS}
    for clause, quote, text, context in _units(clauses):
        if not re.search(_FAILURE, text + context):
            continue
        # A broad mixed heading must not turn ordinary payment/delivery into
        # an arrangement applying on failure.
        if re.search(r"正常履行|正常交付|验收合格后|项目完成时|项目完成后", text) and not re.search(_FAILURE, text):
            continue
        if re.search(r"因.{0,12}(?:违约|过错)|可归责|因(?:甲方|乙方)原因", text) and not re.search(r"无过错|不可归责|难以克服|无法克服", text):
            continue
        deferred = bool(re.search(_DEFERRED, text))
        if re.search(_NO_ARRANGEMENT, text) and not deferred:
            continue
        if re.search(r"无过错|不可归责|难以克服|无法克服|现有技术.{0,8}(?:条件|水平)", text):
            _add(facts, "no_fault_technical_risk_trigger", clause, quote, "DEVELOPMENT_FAILURE", principle=deferred)
        if re.search(r"(?:直接)?损失|技术风险", text) and re.search(r"各承担|分担|由.{0,30}承担|(?:甲方|乙方|双方|各方|委托方|受托方).{0,15}承担", text):
            _add(facts, "no_fault_technical_risk_allocation", clause, quote, "DEVELOPMENT_FAILURE", principle=deferred)
        settlement_specs = {
            "failed_development_incurred_cost_settlement": r"已发生.{0,8}(?:费用|成本|经费)|已投入.{0,8}(?:费用|成本|经费)|已完成.{0,15}(?:开发|研发).{0,12}(?:费用|结算)|(?:已发生|已完成)部分.{0,12}结算",
            "paid_fee_refund": r"已(?:经)?(?:支付|付|收取|收).{0,10}(?:款|费|经费|价款)|已付款|已收款",
            "unpaid_fee_obligation": r"(?:尚未|未)(?:支付|付).{0,10}(?:款|费|经费|价款)|未付款|剩余.{0,8}(?:款|费|经费|价款)|未到期.{0,8}(?:款|费|经费|价款)",
        }
        for key, subject in settlement_specs.items():
            if re.search(subject, text) and re.search(_SETTLEMENT, text):
                # Past-tense "已支付" alone is not settlement/handling.
                operative = re.sub(r"(?:已(?:经)?|尚未|未)(?:支付|付清)", "", text)
                if re.search(_SETTLEMENT, operative):
                    _add(facts, key, clause, quote, "DEVELOPMENT_FAILURE", principle=deferred)
        for key, subject in (
            ("failed_project_stage_result_disposition", r"阶段(?:性)?成果|已完成成果|未完成成果"),
            ("failed_project_source_code_disposition", r"源代码|源程序"),
            ("failed_project_material_disposition", r"研发资料|研究资料|开发文档|技术资料|研发记录"),
        ):
            if re.search(subject, text) and re.search(_DISPOSITION, text):
                _add(facts, key, clause, quote, "DEVELOPMENT_FAILURE", principle=deferred)
    return _elements(DEVELOPMENT_FAILURE_REQUIREMENTS, facts)


def entrusted_development_element_family(element_id, clauses):
    """Resolve a final requirement through the same extractor used at coverage.

    Returning ``None`` means this module does not own that requirement; an
    owned missing/partial requirement still returns its row and search target.
    """
    key = str(element_id).strip().casefold()
    extractor = (
        entrusted_patent_application_elements if key in ENTRUSTED_PATENT_REQUIREMENTS
        else development_failure_elements if key in DEVELOPMENT_FAILURE_REQUIREMENTS
        else None
    )
    if extractor is None:
        return None
    return next(row for row in extractor(clauses) if row["element_id"] == key)
