"""Positive construction obligations: full-corpus retrieval and intent verification.

Each element requires a relationship, not an isolated topic keyword. Matches
are returned as exact source spans; section numbers are provenance, never a
condition for satisfying a rule. All elements may be satisfied across clauses.
"""
from __future__ import annotations

import re


def element(key, proposition, *patterns):
    return {"element_id": key, "proposition": proposition, "construction_patterns": patterns}


CONSISTENCY = (
    r"(?:不再|不得|禁止).{0,30}签订.{0,100}(?:实质性内容.{0,15}背离|背离.{0,25}(?:中标合同|实质性内容))",
    r"(?:本合同|补充协议|实质性内容).{0,100}(?:应|须|保持|与).{0,30}中标合同.{0,20}一致",
)
DOCUMENT = r"(?:组成本?合同的(?:各个)?文件|本?合同(?:的)?组成文件|合同文件的组成|合同文件包括|本?合同(?:包括|包含)以下文件)"

PROFILES = {
    "construction_scope_and_site": [
        element("scope", "工程承包范围", r"(?:承包范围|工程范围|施工范围)(?:，包括以下)?[：:].{2,180}"),
        element("site", "工程地点", r"工程地点[：:].{2,120}"),
    ],
    "qualification_before_completion": [element("qualification_continuity", "资质有效期及持续保持义务", r"资质(?:证书)?.{0,50}(?:有效期|到期|延续|撤销|补正|失效)", r"(?:持续|保持|延续).{0,30}(?:相应|施工)?资质")],
    "contractor_license_attachment": [element("license_documents", "承包人资质证照提供或附件", r"(?:提供|提交|附件|附后).{0,100}(?:资质证书|安全生产许可证|建造师证书)", r"(?:资质证书|安全生产许可证).{0,100}(?:提供|提交|附件|复印件)")],
    "valid_bid_award_document": [element("award_documents", "中标文件纳入合同文件", DOCUMENT + r".{0,1000}中标通知书")],
    "bid_contract_consistency": [element("bid_consistency", "合同实质内容不得背离中标合同", *CONSISTENCY)],
    "construction_license_and_approval": [element("approval_duties", "施工许可办理责任", r"(?:发包人|承包人)(?:(?!发包人|承包人).){0,35}(?:应|负责|须)(?:(?!发包人|承包人).){0,60}(?:办理|取得|申办)(?:(?!发包人|承包人).){0,40}(?:施工许可证|施工许可|开工批准)")],
    "employer_permit_assistance": [element("permit_assistance", "发包人审批及开工协助", r"发包人(?:应|须|负责|承诺)(?:(?!承包人).){0,40}(?:办理|履行|提供|协助|完成)(?:(?!承包人).){0,60}(?:审批|施工许可|手续|授权|开工|场地)", r"发包人负责办理.{0,40}(?:审批|手续|许可)")],
    "subcontract_to_qualified_party": [
        element("qualified_subcontractor", "分包对象具备相应资质", r"分包.{0,60}(?:相应|具备|合格).{0,15}资质|资质.{0,20}(?:单位|企业).{0,35}分包"),
        element("subcontract_consent", "分包经发包人同意或专用条款许可", r"分包事项.{0,100}发包人.{0,60}(?:批准|同意)", r"专用条款.{0,30}列出.{0,100}分包", r"(?:经|须经)发包人(?:书面)?同意.{0,30}(?:可以|方可)?分包"),
    ],
    "labor_subcontract_qualification": [element("labor_management", "劳务工资及实名管理", r"(?:承包人|劳务分包|分包企业).{0,100}(?:实名|工资.{0,20}(?:支付|发放)|支付.{0,20}工资)")],
    "substantive_terms_consistency": [element("substantive_consistency", "双方不得另签背离实质内容的协议", *CONSISTENCY)],
    "supplementary_agreement_boundary": [element("change_boundary", "补充协议或变更的范围和程序", r"(?:补充协议|工程变更|设计变更)(?:仅|应|须|不得).{0,80}", r"(?:双方|发包人).{0,30}(?:应|须).{0,30}书面.{0,40}(?:变更|补充协议)", r"(?:变更指令|补充协议).{0,20}以书面形式.{0,10}(?:发出|签订)")],
    "bid_contract_archive": [element("bid_archive", "招投标文件组成或归档", DOCUMENT + r".{0,1000}(?:中标通知书|投标文件|招标文件)", r"(?:招标文件|投标文件|中标通知书).{0,80}(?:归档|保存|合同附件)")],
    "start_date_identification": [element("start", "开工日期或开工通知依据", r"(?:实际)?开工日期以.{0,60}(?:起算|为准|确定)", r"以.{0,60}开工通知.{0,30}(?:为|起算).{0,15}(?:开工|日期)")],
    "completion_date_identification": [element("completion", "实际竣工日期的认定依据", r"以.{2,100}(?:之日|日期).{0,12}为(?:实际)?竣工日期", r"(?:实际)?竣工日期(?:应|须)?以.{2,100}(?:为准|确定)")],
    "period_extension_conditions": [element("extension", "非承包人原因的工期顺延", r"(?:发包人原因|不可抗力|非承包人原因).{0,150}(?:工期|竣工日期).{0,40}(?:顺延|延长|延后)")],
    "delay_liability": [element("delay", "承包人延误工期责任", r"(?:逾期竣工|工期延误|误期).{0,120}(?:违约金|赔偿|承担|扣减)")],
    "quality_standard_acceptance": [
        element("standard", "工程质量适用标准", r"(?:工程|质量).{0,70}(?:必须符合|应符合|应达到|应执行).{0,70}(?:标准|规范)", r"工程质量标准[：:].{2,80}"),
        element("acceptance", "竣工验收程序", r"(?:承包人|发包人|监理人).{0,40}(?:应|须).{0,35}(?:组织|申请|提交|通知).{0,50}竣工验收"),
    ],
    "hidden_work_inspection": [element("hidden_inspection", "隐蔽工程检查通知及验收", r"隐蔽.{0,120}(?:通知|检查|验收).{0,100}(?:监理|发包人)|(?:发包人|监理).{0,100}(?:检查|验收).{0,60}隐蔽")],
    "quality_deposit_return_period": [element("deposit_return", "质量保证金返还条件及期限", r"(?:期满|届满|\d+日内).{0,60}(?:返还|退还).{0,20}(?:质量保证金|质保金)", r"(?:质量保证金|质保金)(?:应|须|于|在|的返还期限).{0,60}(?:期|日).{0,40}(?:返还|退还)")],
    "unauthorized_use_consequence": [element("use_consequence", "未验收使用的后果", r"(?:擅自使用|未经.{0,8}验收.{0,12}使用).{0,160}(?:责任|竣工日期|质量|视为)")],
    "project_price_pricing_method": [element("pricing", "工程价款计价方法", r"(?:合同价格|合同价款|工程价款|合同总价).{0,100}(?:固定|总价|单价|计价|清单)", r"本合同采用.{0,30}(?:总价|单价|清单计价).{0,20}(?:合同|形式|方式)")],
    "settlement_procedure": [element("settlement", "竣工结算提交审核程序", r"(?:竣工结算资料|结算文件|结算报告).{0,80}(?:审核|审查|日内)", r"(?:提交|审核).{0,30}(?:竣工结算(?:报告|书|资料)|结算文件)")],
    "project_price_interest": [element("interest", "欠付工程款的利息", r"(?:逾期|拖欠|延误|未支付|未能支付).{0,160}(?:利息|LPR)|(?:LPR|利息).{0,100}(?:拖欠|逾期|应付|支付)")],
    "add_subcontractor_party": [
        element("subcontract_chain", "分包合同链条资料提交留存", r"(?:提供|提交|移交|保存|留存|归档).{0,60}(?:全部|所有|相关)?分包合同.{0,100}(?:执行情况|结算|付款|资料|说明)", r"分包合同.{0,80}(?:归档|保存|留存)"),
    ],
    "stoppage_loss_claim": [
        element("employer_stoppage_cost", "发包人原因暂停的费用责任", r"(?:发包人原因|发包人通知).{0,160}(?:暂停|停工).{0,180}(?:费用|损失).{0,80}发包人.{0,30}(?:承担|负责|支付)"),
        element("idle_cost", "进场延误或窝工损失责任", r"(?:发包人原因|非承包人原因).{0,60}(?:进场|窝工).{0,160}发包人.{0,60}(?:费用|承担|负责)", r"发包人.{0,30}承担.{0,80}窝工费用"),
    ],
    "employer_assistance_breach_termination": [element("contractor_termination", "发包人不履约时承包人解除权", r"承包人有权.{0,60}解除合同.{0,350}发包人.{0,60}(?:延误付款|未能|不履行)", r"发包人.{0,120}(?:不履行|未履行|未能|延误付款).{0,180}承包人.{0,30}(?:可|有权).{0,35}解除")],
    "contract_termination_settlement": [
        element("termination_account", "解除日期的结算资料及款项", r"(?:解除合同|合同解除|解除日期).{0,120}(?:商定|确认|提交).{0,100}(?:工程款项|合同款项|结算资料|已完工程)", r"解除.{0,20}(?:结算资料|结算依据).{0,100}(?:商定|包括|确认)"),
        element("termination_payment", "解除后的结算支付", r"(?:双方|发包人).{0,120}解除.{0,60}结算资料.{0,100}(?:结清|支付|应收应付)", r"合同解除后.{0,100}(?:已完工程|工程价款).{0,80}(?:结算|支付)"),
    ],
    "drawing_technical_spec_attachment": [
        element("drawings", "图纸纳入合同文件", DOCUMENT + r".{0,1000}图纸", r"图纸.{0,80}(?:合同附件|组成部分)"),
        element("specifications", "标准规范及技术要求纳入合同", DOCUMENT + r".{0,1000}(?:标准.{0,8}规范|技术要求|技术规范)"),
    ],
    "boq_pricing_attachment": [element("pricing_attachment", "计价清单或预算附件", r"(?:工程量清单|报价清单|预算书|计价表).{0,100}(?:附件|合同文件|组成|确认)|(?:附件|合同文件|组成).{0,160}(?:工程量清单|报价清单|预算书|计价表)")],
    "tender_bid_permit_attachment": [
        element("tender_documents", "招投标文件纳入合同", DOCUMENT + r".{0,1000}(?:中标通知书|投标文件|招标文件)"),
        element("permit_documents", "许可审批文件的附件或提交清单", r"(?:提供|提交)[^。\n]{0,30}(?:规划许可证|施工许可证|开工批准文件)", DOCUMENT + r".{0,1000}(?:规划许可证|施工许可证)", r"(?:规划许可证|施工许可证)[^。\n]{0,60}(?:作为附件|附件清单|合同组成部分)"),
    ],
    "change_visa_settlement_attachment": [
        element("change_records", "变更签证书面资料", r"(?:变更|签证|洽商).{0,120}(?:书面|记录|资料|提交|确认)", r"(?:书面|提交|确认).{0,70}(?:变更|签证|洽商)"),
        element("settlement_records", "竣工结算资料提交留存", r"(?:提交|移交|保存|归档).{0,100}(?:竣工资料|竣工结算|结算资料)|(?:竣工资料|结算资料).{0,100}(?:提交|移交|保存|归档)"),
    ],
}


_CROSS_CLAUSE_CONTEXT = {"contract_termination_settlement", "employer_assistance_breach_termination",
                       "stoppage_loss_claim", "drawing_technical_spec_attachment", "tender_bid_permit_attachment",
                       "bid_contract_archive", "valid_bid_award_document"}
for _node, _requirements in PROFILES.items():
    for _requirement in _requirements:
        if _node not in _CROSS_CLAUSE_CONTEXT:
            _requirement["construction_patterns"] = tuple(p.replace(".{", "[^。\\n]{") for p in _requirement["construction_patterns"])


def supports(requirement, text):
    return any((m := re.search(p, text, re.S)) and not re.search(r"_{2,}", m.group()) for p in requirement["construction_patterns"])


def permit_attachment_assessment(clauses):
    """Separate document housekeeping from missing operative safeguards."""
    from review_v2.adverse_evidence import direct_evidence
    duties = extract("construction_license_and_approval", clauses)
    conditions, _ = direct_evidence(clauses, (
        r"(?:取得|具备|完成).{0,45}(?:施工许可|开工许可|开工条件).{0,45}(?:开工|施工)",
        r"(?:开工|施工).{0,30}(?:前|条件).{0,50}(?:许可|批准|审批)",
    ), require_assertion=False)
    abnormalities, _ = direct_evidence(clauses, (
        r"(?:施工许可证|规划许可证|开工批准文件).{0,15}(?:已被撤销|已被吊销|已失效|系伪造)",
        r"(?:本工程|本项目|发包人).{0,20}(?:尚未|未能)取得.{0,12}(?:施工许可证|规划许可证)",
        r"(?:无需|不必)办理.{0,12}(?:施工许可|规划许可)",
    ), require_assertion=False)
    return {"responsibility_evidence": duties, "start_condition_evidence": conditions,
            "abnormality_evidence": abnormalities,
            "specific_exposure": bool(abnormalities) or not duties or not conditions,
            "external_fact_verified": False}


def extract(node_id, clauses):
    rows = []
    for requirement in PROFILES.get(node_id, []):
        hits = []
        for clause in clauses:
            if clause.section_type not in {"正式合同条款", "附件"}:
                continue
            for pattern in requirement["construction_patterns"]:
                match = re.search(pattern, clause.text, re.S)
                if not match:
                    continue
                # Include complete surrounding sentences, without manufacturing
                # a heading or truncating away the actual supporting predicate.
                start = max(clause.text.rfind("。", 0, match.start()), clause.text.rfind("\n", 0, match.start())) + 1
                ends = [value + 1 for delimiter in ("。", "\n") if (value := clause.text.find(delimiter, match.end())) >= 0]
                end = min(ends) if ends else len(clause.text)
                text = clause.text[start:end].strip()
                if len(text) < 18 and not re.search(r"应|须|双方|发包人|承包人", text):
                    # A subsection label such as "提交竣工结算资料" alone is
                    # not an operative duty. Expand to its actual paragraph.
                    next_end = clause.text.find("。", end)
                    if next_end >= 0:
                        end = next_end + 1
                        text = clause.text[start:end].strip()
                if not text:
                    continue
                hits.append({"clause_id": clause.clause_id, "location": clause.location,
                             "title": clause.title, "text": text, "original_excerpt": text,
                             "section_type": clause.section_type, "block_type": clause.block_type,
                             "construction_element_ids": [requirement["element_id"]],
                             "construction_blank": bool(re.search(r"_{2,}", match.group())),
                             "source_start": start, "source_end": end})
                break
        operative = [r for r in hits if not re.search(r"(?:是指|：指|按照第.{0,20}约定确定)", r["text"])]
        if operative:
            hits = operative
        # Operative relationships outrank blank forms, definitions and bare
        # references. Source identifiers are never inferred from cross-references.
        rows.extend(sorted(hits, key=lambda r: (
            r["construction_blank"],
            bool(re.search(r"(?:是指|：指|按照第.{0,20}约定确定)", r["text"])),
            bool(re.search(r"重新组织|重新验收", r["text"])) if node_id == "quality_standard_acceptance" else False,
            -len(re.findall(r"以.{2,100}?为(?:实际)?竣工日期", r["text"])) if node_id == "completion_date_identification" else 0,
            len(r["text"]),
        ))[:3])
    unique = {}
    for row in rows:
        key = row["clause_id"], row["text"]
        if key in unique:
            unique[key]["construction_element_ids"].extend(row["construction_element_ids"])
        else:
            unique[key] = row
    return list(unique.values())


def coverage_failures(items):
    failures = []
    for item in items:
        from review_v2.construction_evidence import EXTERNAL_NODES
        if item.node_id in EXTERNAL_NODES and item.coverage_status == "通过":
            failures.append({"requirement": "CONSTRUCTION_EXTERNAL_FACT_NOT_PROVEN_BY_ABSENCE", "root_cause": item.item_id + "：合同未出现不利约定不能证明外部事实合规。", "current_status": "FAIL"})
        if item.item_id.startswith("CE-") and item.coverage_status == "通过" and item.node_id not in PROFILES:
            from review_v2.construction_evidence import ADVERSE_PREDICATES
            if item.node_id in ADVERSE_PREDICATES:
                continue  # Negative checks prove absence, not a positive duty.
            trace = item.decision_trace or {}
            source_rows = trace.get("construction_nature_evidence", []) or [
                r for rows in trace.get("cross_clause_coverage", {}).get("covered", {}).values() for r in rows]
            if not item.evidence_clauses or not all(any(
                r.get("clause_id") == s.get("clause_id") and
                re.sub(r"\s+", "", r.get("text", "")) == re.sub(r"\s+", "", s.get("text", "")) and
                re.sub(r"\s+", "", r.get("location", "")) == re.sub(r"\s+", "", s.get("location", ""))
                for s in source_rows) for r in item.evidence_clauses):
                failures.append({"requirement": "CONSTRUCTION_PASS_SOURCE_BINDING", "root_cause": item.item_id + "：通过证据未绑定已验证原文。", "current_status": "FAIL"})
        if item.node_id not in PROFILES or item.coverage_status not in {"通过", "部分覆盖"}:
            continue
        rows = item.evidence_clauses or []
        source = (item.decision_trace or {}).get("construction_coverage_search", {}).get("evidence", [])
        matched = {e["element_id"] for e in PROFILES[item.node_id]
                   if any(supports(e, row.get("text", "")) for row in rows)}
        for row in rows:
            bound = any(row.get("clause_id") == s["clause_id"]
                        and re.sub(r"\s+", "", row.get("text", "")) == re.sub(r"\s+", "", s["text"])
                        and re.sub(r"\s+", "", row.get("location", "")) == re.sub(r"\s+", "", s["location"])
                        for s in source)
            if not bound or not any(supports(e, row.get("text", "")) or (row.get("construction_blank") and any(re.search(p, row.get("text", ""), re.S) for p in e["construction_patterns"])) for e in PROFILES[item.node_id]):
                failures.append({"requirement": "CONSTRUCTION_PASS_EVIDENCE_INTENT", "root_cause": item.item_id + "：覆盖证据与规则语义或原文定位不一致。", "current_status": "FAIL"})
        if not rows or (item.coverage_status == "通过" and len(matched) != len(PROFILES[item.node_id])):
            failures.append({"requirement": "CONSTRUCTION_PASS_EVIDENCE_COMPLETE", "root_cause": item.item_id + "：通过结论未覆盖必要语义要素。", "current_status": "FAIL"})
    return failures
