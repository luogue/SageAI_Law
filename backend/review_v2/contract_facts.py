"""Generic, source-backed facts used by evidence retrieval.

This module does not decide review outcomes. It extracts explicit contract
facts and preserves the clause IDs that support each value.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Optional

from review_v2.clause_parser import ParsedClause


FACT_GRAPH_VERSION = "contract-fact-graph-1.0"


CANONICAL_FACT_ALIASES: Dict[str, str] = {
    "course_name": "service.course_name",
    "training_course_name": "service.course_name",
    "service_name": "service.course_name",
    "class_id": "service.project_id",
    "class_number": "service.project_id",
    "project_id": "service.project_id",
    "training_project_id": "service.project_id",
    "total_lessons": "service.total_sessions",
    "total_classes": "service.total_sessions",
    "service_count": "service.total_sessions",
    "training_fee": "payment.total_fee",
    "service_fee": "payment.total_fee",
    "prepaid_total": "payment.total_fee",
    "contract_total_fee": "payment.total_fee",
}


def canonical_fact_key(fact_type: str) -> str:
    key = str(fact_type or "").strip()
    return CANONICAL_FACT_ALIASES.get(key, key)


@dataclass(frozen=True)
class ContractFact:
    fact_id: str
    fact_type: str
    value: Any
    normalized_value: Any
    source_clause_ids: List[str]
    source_spans: List[str]
    source_locations: List[str]
    confidence: str = "high"

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ContractFactGraph:
    version: str = FACT_GRAPH_VERSION
    facts: Dict[str, List[ContractFact]] = field(default_factory=dict)
    snapshot_id: str = ""
    frozen: bool = False

    def add(self, fact_type: str, value: Any, clause: ParsedClause, normalized_value: Any = None) -> None:
        if self.frozen:
            raise RuntimeError("ContractFactRegistry snapshot is immutable after freeze().")
        if value in (None, "", []):
            return
        fact_type = canonical_fact_key(fact_type)
        normalized = value if normalized_value is None else normalized_value
        existing = self.facts.setdefault(fact_type, [])
        identity = (str(normalized), clause.clause_id)
        if any((str(item.normalized_value), item.source_clause_ids[0]) == identity for item in existing):
            return
        existing.append(
            ContractFact(
                fact_id=f"F-{fact_type.upper().replace('.', '-')}-{len(existing) + 1:03d}",
                fact_type=fact_type,
                value=value,
                normalized_value=normalized,
                source_clause_ids=[clause.clause_id],
                source_spans=[clause.text],
                source_locations=[clause.location],
            )
        )

    def freeze(self, snapshot_id: str) -> None:
        self.snapshot_id = snapshot_id
        self.frozen = True

    def matching(self, requirements: Iterable[str]) -> List[ContractFact]:
        result: List[ContractFact] = []
        for requirement in requirements:
            requirement = canonical_fact_key(requirement)
            for fact_type, facts in self.facts.items():
                if fact_type == requirement or fact_type.startswith(requirement + ".") or requirement.startswith(fact_type + "."):
                    result.extend(facts)
        return list({fact.fact_id: fact for fact in result}.values())

    def source_clause_ids(self, requirements: Iterable[str]) -> List[str]:
        return list(dict.fromkeys(clause_id for fact in self.matching(requirements) for clause_id in fact.source_clause_ids))

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "snapshot_id": self.snapshot_id,
            "frozen": self.frozen,
            "facts": {
                fact_type: [fact.to_public_dict() for fact in facts]
                for fact_type, facts in self.facts.items()
            },
            "fact_count": sum(len(facts) for facts in self.facts.values()),
        }


REVIEW_FACT_REQUIREMENTS: Dict[str, List[str]] = {
    "common_effective_clause": ["contract.effective_date", "contract.effective_condition"],
    "common_jurisdiction": ["dispute.type", "dispute.institution", "dispute.location"],
    "sale_validity_party_capacity": ["party.buyer", "party.seller", "party.identity", "party.authority"],
    "sale_subject_name_spec": ["goods.name", "goods.model"],
    "sale_subject_quantity_unit": ["quantity.total", "quantity.unit"],
    "sale_subject_quality_standard": ["quality.standard"],
    "sale_delivery_time": ["delivery.date", "delivery.deadline", "delivery.schedule", "delivery.batch"],
    "sale_delivery_place": ["delivery.location"],
    "sale_delivery_method": ["transport.mode", "transport.responsible_party", "delivery.voucher"],
    "sale_price_amount_currency": ["price.total", "price.unit", "currency"],
    "sale_payment_schedule": ["prepayment.ratio", "prepayment.amount", "payment.schedule"],
    "sale_payment_method_account": ["payment.account", "payment.method"],
    "sale_quality_standard_basis": ["quality.standard"],
    "sale_warranty_period": ["warranty.duration", "warranty.response", "warranty.repair_or_replace"],
    "sale_quality_remedy": ["quality_objection.deadline", "quality.remedy", "warranty.repair_or_replace"],
    "sale_inspection_period": ["inspection.deadline", "inspection.sample_ratio", "inspection.institution"],
    "sale_deemed_acceptance": ["deemed_conforming.deadline"],
    "sale_breach_liability_general": ["breach.remedy", "breach.liquidated_damages"],
    "sale_expectation_loss": ["damages.expectation_loss", "damages.foreseeability_limit"],
    "real_estate_seller_identity": ["party.seller"],
    "real_estate_buyer_identity": ["party.buyer"],
    "real_estate_registered_owner": ["real_estate.owner", "real_estate.certificate"],
    "real_estate_coownership": ["real_estate.ownership"],
    "real_estate_spouse_consent": ["real_estate.spouse"],
    "real_estate_certificate": ["real_estate.certificate"],
    "real_estate_mortgage_status": ["real_estate.mortgage"],
    "real_estate_mortgage_release": ["real_estate.mortgage.release_deadline"],
    "real_estate_existing_lease": ["real_estate.lease"],
    "real_estate_property_identity": ["real_estate.address", "real_estate.property"],
    "real_estate_area_usage": ["real_estate.area", "real_estate.property.usage"],
    "real_estate_land_use_right": ["real_estate.land"],
    "real_estate_total_price": ["real_estate.price"],
    "real_estate_deposit_downpayment": ["real_estate.payment.deposit", "real_estate.payment.first_payment"],
    "real_estate_purchase_financing": ["real_estate.payment.loan"],
    "real_estate_balance_holdback": ["real_estate.payment.balance", "real_estate.payment.household_holdback"],
    "real_estate_transfer_deadline": ["real_estate.registration"],
    "real_estate_registration_cooperation": ["real_estate.registration.institution"],
    "real_estate_advance_notice_registration": ["real_estate.registration.advance_notice"],
    "real_estate_delivery_deadline": ["real_estate.delivery.date"],
    "real_estate_inspection": ["real_estate.delivery.inspection_deadline"],
    "real_estate_possession_handover": ["real_estate.delivery.possession_trigger"],
    "real_estate_risk_transfer": ["real_estate.delivery.risk_transfer"],
    "real_estate_household_registration": ["real_estate.household"],
    "real_estate_maintenance_fund": ["real_estate.maintenance_fund"],
    "service_content_standard": [
        "service.course_name",
        "service.project_id",
        "service.total_sessions",
        "service.session_duration",
        "service.location",
        "service.delivery_mode",
    ],
    "service_schedule_and_place": [
        "service.schedule",
        "service.start_date",
        "service.end_date",
        "service.location",
        "service.delivery_mode",
    ],
    "prepaid_amount_and_balance": [
        "payment.total_fee",
        "payment.amount_paid",
        "payment.unit_price",
        "payment.remaining_balance",
        "payment.material_fee",
    ],
    "prepaid_partly_provided_refund": [
        "payment.unit_price",
        "payment.total_sessions",
        "payment.remaining_balance",
        "payment.refund_formula",
        "payment.material_fee",
    ],
    "termination_refund_calculation": [
        "payment.unit_price",
        "payment.total_sessions",
        "payment.remaining_balance",
        "payment.refund_formula",
        "payment.material_fee",
    ],
    "fee_standard_attachment": [
        "payment.total_fee",
        "payment.session_fee_total",
        "payment.unit_price",
        "payment.material_fee",
        "payment.fee_schedule",
    ],
}


def fact_requirements_for_node(node_id: str) -> List[str]:
    return list(REVIEW_FACT_REQUIREMENTS.get(node_id, []))


def _number(value: str) -> Optional[float]:
    try:
        return float(value.replace(",", ""))
    except (TypeError, ValueError):
        return None


def _date(value: str) -> str:
    match = re.search(r"(20\d{2})[年/.-](\d{1,2})[月/.-](\d{1,2})日?", value)
    return f"{int(match.group(1)):04d}-{int(match.group(2)):02d}-{int(match.group(3)):02d}" if match else value


def _add_matches(graph: ContractFactGraph, clause: ParsedClause, fact_type: str, pattern: str, group: int = 1, normalize=None) -> None:
    for match in re.finditer(pattern, clause.text, re.IGNORECASE):
        value = match.group(group).strip()
        graph.add(fact_type, value, clause, normalize(value) if normalize else value)


def _add_first_match(graph: ContractFactGraph, clause: ParsedClause, fact_type: str, pattern: str, group: int = 1, normalize=None) -> None:
    match = re.search(pattern, clause.text, re.IGNORECASE)
    if not match:
        return
    value = match.group(group).strip()
    graph.add(fact_type, value, clause, normalize(value) if normalize else value)


def extract_contract_fact_graph(clauses: List[ParsedClause]) -> ContractFactGraph:
    graph = ContractFactGraph()
    for clause in clauses:
        text = clause.text
        compacted = re.sub(r"\s+", "", text)

        for role, labels in (("buyer", ("购货单位", "买方", "买受人")), ("seller", ("供货单位", "卖方", "出卖人"))):
            for label in labels:
                match = re.search(rf"{label}[：:]?([^，。；;\n|]+)", text)
                if match and len(match.group(1).strip()) >= 2:
                    graph.add(f"party.{role}.name", match.group(1).strip(), clause)
        if any(term in compacted for term in ("法定代表人", "委托代理人", "统一社会信用代码", "地址", "住所", "电话", "开户银行", "账号")):
            graph.add("party.identity", compacted[:300], clause)
        if any(term in compacted for term in ("法定代表人", "委托代理人", "授权代表", "授权书")):
            graph.add("party.authority", compacted[:300], clause)
        for role, marker in (("buyer", "甲方"), ("seller", "乙方")):
            role_segment = compacted.split(marker, 1)[1] if marker in compacted else ""
            if role == "buyer" and "乙方" in role_segment:
                role_segment = role_segment.split("乙方", 1)[0]
            for fact_name, pattern in (
                ("legal_representative", r"法定代表人[：:]?([^委地开账电]{2,40})"),
                ("agent", r"委托代理人[：:]?([^地开账电]{2,40})"),
                ("address", r"地址[：:]?([^开账电]{4,80})"),
            ):
                match = re.search(pattern, role_segment)
                if match:
                    graph.add(f"party.{role}.{fact_name}", match.group(1), clause)

        _add_matches(graph, clause, "goods.name", r"产品名称[：:]?\s*([^。；;\n|]+)")
        for model in re.findall(r"\b[A-Z]{2,}[A-Z0-9.-]*\d[A-Z0-9.-]*\b", text):
            if "BLIND" not in model and "SALE" not in model:
                graph.add("goods.model", model, clause)
        _add_matches(graph, clause, "quantity.total", r"(?:产品总数量|总数量|合计数量)[：:]?\s*([\d,]+(?:\.\d+)?)", normalize=_number)
        unit_match = re.search(r"(?:计量单位(?:和计量方法)?)[^。；;\n|]{0,20}?以\s*(台|吨|件|套|个|公斤|千克|米|平方米)\s*为计量单位", text)
        if unit_match:
            graph.add("quantity.unit", unit_match.group(1), clause)
        for match in re.finditer(r"([\d,]+(?:\.\d+)?)\s*(台|吨|件|套|个|公斤|千克|米|平方米)", text):
            graph.add("quantity.item", match.group(1), clause, _number(match.group(1)))
            graph.add("quantity.unit", match.group(2), clause)

        for match in re.finditer(r"(?:总价款|合同(?:含税)?总价|合同价款总额|价款合计|总计)[^\d]{0,12}([\d,]+(?:\.\d+)?)\s*元", text):
            graph.add("price.total", match.group(1), clause, _number(match.group(1)))
        for match in re.finditer(r"([\d,]+(?:\.\d+)?)\s*元\s*/\s*(台|吨|件|套|个)", text):
            graph.add("price.unit", match.group(1), clause, _number(match.group(1)))
        if "人民币" in text:
            graph.add("currency", "人民币", clause, "CNY")
        for match in re.finditer(r"预付款[^。；;\n]{0,30}?([\d.]+)\s*[%％]", text):
            graph.add("prepayment.ratio", match.group(1) + "%", clause, float(match.group(1)) / 100)
        for match in re.finditer(r"([\d.]+)\s*[%％][^。；;\n]{0,16}(?:作为)?预付款", text):
            graph.add("prepayment.ratio", match.group(1) + "%", clause, float(match.group(1)) / 100)
        for match in re.finditer(r"预付款[^。；;\n]{0,40}?([\d,]+(?:\.\d+)?)\s*元", text):
            graph.add("prepayment.amount", match.group(1), clause, _number(match.group(1)))
        if "预付款" in text:
            amounts = re.findall(r"(?:人民币)?\s*([\d,]+(?:\.\d+)?)\s*元", text)
            if amounts:
                graph.add("prepayment.amount", amounts[-1], clause, _number(amounts[-1]))
        if any(term in text for term in ("预付款", "尾款", "分期付款", "付款节点", "支付货款")):
            graph.add("payment.schedule", compacted[:400], clause)
        if any(term in text for term in ("银行转账", "付款方式", "支付方式")):
            graph.add("payment.method", compacted[:300], clause)
        if any(term in text for term in ("收款账户", "账号", "开户银行", "开户行")):
            graph.add("payment.account", compacted[:300], clause)

        dates = re.findall(r"20\d{2}[年/.-]\d{1,2}[月/.-]\d{1,2}日?", text)
        if dates and any(term in text for term in ("交货", "交付", "供货", "发货")):
            for value in dates:
                graph.add("delivery.date", value, clause, _date(value))
            graph.add("delivery.schedule", compacted[:500], clause)
            if any(term in text for term in ("第一批", "第二批", "分批")):
                graph.add("delivery.batch", compacted[:500], clause)
                for label, fact_type in (("第一批", "delivery.batch1.deadline"), ("第二批", "delivery.batch2.deadline")):
                    match = re.search(rf"{label}[^：:。；;\n]*[：:]?\s*(20\d{{2}}[年/.-]\d{{1,2}}[月/.-]\d{{1,2}}日?)", text)
                    if match:
                        graph.add(fact_type, match.group(1), clause, _date(match.group(1)))
            final_match = re.search(r"(20\d{2}[年/.-]\d{1,2}[月/.-]\d{1,2}日?)前[^。；;\n]{0,20}(?:完成全部|全部产品|全部供货)", text)
            if final_match:
                graph.add("delivery.final_deadline", final_match.group(1), clause, _date(final_match.group(1)))
        if any(term in text for term in ("交货地点", "交付地点", "收货地址", "指定仓库")):
            graph.add("delivery.location", compacted[:300], clause)
        if any(term in text for term in ("汽车运输", "公路运输", "铁路运输", "航空运输", "海运", "物流", "自提")):
            graph.add("transport.mode", compacted[:300], clause)
        if re.search(r"(甲方|乙方|买方|卖方|出卖人|买受人).{0,8}(负责|承担).{0,8}运输", compacted):
            graph.add("transport.responsible_party", compacted[:300], clause)
        if "保险" in text:
            graph.add("transport.insurance", compacted[:300], clause)
            party = re.search(r"(甲方|乙方|买方|卖方|出卖人|买受人)[^。；;\n]{0,8}(?:负责购买|承担)[^。；;\n]{0,8}保险", text)
            if party:
                graph.add("insurance.party", party.group(1), clause, "seller" if party.group(1) in {"乙方", "卖方", "出卖人"} else "buyer")
        if any(term in text for term in ("送货单", "签收单", "物流回执", "实际签收")):
            graph.add("delivery.voucher", compacted[:300], clause)

        if any(term in text for term in ("质量标准", "国家标准", "行业标准", "企业标准", "GB/", "GB ")):
            graph.add("quality.standard", compacted[:500], clause)
        if any(term in text for term in ("验收", "检验")):
            graph.add("inspection.clause", compacted[:500], clause)
            for match in re.finditer(r"(?:收到|收货|到货|验收|检验)[^。；;\n]{0,24}?([\d]+)\s*(个工作日|工作日|日|天)内", text):
                graph.add("inspection.deadline", match.group(1) + match.group(2), clause)
            for match in re.finditer(r"抽检[^。；;\n]{0,20}?([\d.]+)\s*[%％]", text):
                graph.add("inspection.sample_ratio", match.group(1) + "%", clause, float(match.group(1)) / 100)
            if any(term in text for term in ("检验机构", "质量监督检验", "检测机构")):
                graph.add("inspection.institution", compacted[:400], clause)
        if "质量异议" in text or ("提出异议" in text and "质量" in text):
            graph.add("quality.remedy", compacted[:500], clause)
            for match in re.finditer(r"([\d]+)\s*(个工作日|工作日|日|天)内", text):
                graph.add("quality_objection.deadline", match.group(1) + match.group(2), clause)
            response = re.search(r"(?:乙方|卖方|出卖人)[^。；;\n]{0,24}?([\d]+)\s*(个工作日|工作日|日|天)内[^。；;\n]{0,16}(?:处理|响应)", text)
            if response:
                graph.add("seller_response.deadline", response.group(1) + response.group(2), clause)
        if re.search(r"([\d]+)\s*(个工作日|工作日|日|天)内[^。；;]{0,20}(?:未通知|未提出异议)", text):
            match = re.search(r"([\d]+)\s*(个工作日|工作日|日|天)内[^。；;]{0,20}(?:未通知|未提出异议)", text)
            graph.add("deemed_conforming.deadline", match.group(1) + match.group(2), clause)

        if any(term in text for term in ("质保期", "质量保证期", "保修期")):
            for match in re.finditer(r"([\d]+)\s*(个月|月|年)", text):
                graph.add("warranty.duration", match.group(1) + match.group(2), clause)
        if "响应" in text and "工作日" in text:
            _add_matches(graph, clause, "warranty.response", r"([\d]+\s*个工作日)内\s*响应")
        if any(term in text for term in ("维修", "更换", "包修", "包换")):
            graph.add("quality.remedy", compacted[:500], clause)
            if "工作日" in text:
                graph.add("warranty.repair_or_replace", compacted[:500], clause)

        if any(term in text for term in ("违约金", "赔偿损失", "包换", "包修", "退货", "拒收")):
            graph.add("breach.remedy", compacted[:700], clause)
        if "违约金" in text:
            graph.add("breach.liquidated_damages", compacted[:700], clause)
            if "逾期付款" in text:
                graph.add("breach.buyer_late_payment", compacted[:700], clause)
            if "逾期交货" in text:
                graph.add("breach.seller_late_delivery", compacted[:700], clause)
            cannot_deliver = re.search(r"(?:乙方|卖方|出卖人)不能交货[^。；;\n]{0,30}?([\d.]+)\s*[%％]", text)
            if cannot_deliver:
                graph.add("breach.seller_non_delivery_ratio", cannot_deliver.group(1) + "%", clause, float(cannot_deliver.group(1)) / 100)
        if "可得" in text and "利益" in text:
            graph.add("damages.expectation_loss", compacted[:500], clause)
        if any(term in text for term in ("应当预见", "可预见", "预见到")) and "损失" in text:
            graph.add("damages.foreseeability_limit", compacted[:500], clause)

        if "仲裁" in text:
            graph.add("dispute.type", "仲裁", clause, "arbitration")
            institution = re.search(r"提交\s*([^，。；;\n]{2,40}仲裁委员会)", text)
            if institution:
                graph.add("dispute.institution", institution.group(1).strip(), clause)
            location = re.search(r"仲裁地点(?:为|是|：|:)\s*([^，。；;\n]+)", text)
            if location:
                graph.add("dispute.location", location.group(1).strip(), clause)
        effective = re.search(r"(?:本合同)?自\s*(20\d{2}[年/.-]\d{1,2}[月/.-]\d{1,2}日?)\s*(?:起)?生效", text)
        if effective:
            graph.add("contract.effective_date", effective.group(1), clause, _date(effective.group(1)))
        expiry = re.search(r"(?:有效期至|期限至|有效至)\s*(20\d{2}[年/.-]\d{1,2}[月/.-]\d{1,2}日?)", text)
        if expiry:
            graph.add("contract.expiry_date", expiry.group(1), clause, _date(expiry.group(1)))
        if "生效" in text:
            graph.add("contract.effective_condition", compacted[:400], clause)
        if "中华人民共和国合同法" in text:
            graph.add("legal.legacy_reference", "中华人民共和国合同法", clause)

        if any(term in text for term in ("培训", "课程", "课时", "上课", "服务费", "培训费", "课时费")):
            _add_matches(graph, clause, "service.course_name", r"(?:课程名称|服务名称|培训项目)[：:]\s*([^，。；;\n]+)")
            _add_first_match(graph, clause, "service.project_id", r"(?:班级编号|班号|项目编号|服务项目编号)[：:]\s*([A-Za-z0-9][A-Za-z0-9_.\-]{2,40})")
            total_sessions = re.search(
                r"(?:总课时(?:数)?(?:（节）|\(节\))?|课时总数|合计课时|课程共)\s*[：:]?\s*(\d+(?:\.\d+)?)\s*(?:节|课时|次)",
                text,
            )
            if total_sessions:
                graph.add("service.total_sessions", total_sessions.group(1), clause, _number(total_sessions.group(1)))
                graph.add("payment.total_sessions", total_sessions.group(1), clause, _number(total_sessions.group(1)))
            session_match = re.search(r"(?:每次|单次|每节)[^。；;\n]{0,20}?(?:\d+(?:\.\d+)?\s*(?:节|课时|小时|分钟))[^。；;\n]{0,24}?(?:\d+(?:\.\d+)?\s*分钟)?", text)
            if session_match:
                graph.add("service.session_duration", session_match.group(0).strip(), clause)
            _add_first_match(graph, clause, "service.schedule", r"(?:上课时间|服务时间|排课时间)[：:]\s*([^。；;\n]+)")
            _add_first_match(graph, clause, "service.start_date", r"(?:开课日期|服务开始日期|开始日期)[：:为\s]*(20\d{2}[年/.-]\d{1,2}[月/.-]\d{1,2}日?)", normalize=_date)
            _add_first_match(graph, clause, "service.end_date", r"(?:预计结课日期|结课日期|服务结束日期|结束日期)[：:为\s]*(20\d{2}[年/.-]\d{1,2}[月/.-]\d{1,2}日?)", normalize=_date)
            _add_first_match(graph, clause, "service.location", r"(?:培训地点|上课地点|服务地点)[：:]\s*([^。；;\n]+)")
            if any(term in text for term in ("线上", "线下", "面授", "远程", "到店", "预约")):
                graph.add("service.delivery_mode", compacted[:240], clause)

            for match in re.finditer(
                r"(?:培训费用合计|费用合计|培训费合计|服务费合计|培训费用总额|服务费总额|预付款金额|总金额)[^。；;\n]{0,40}?([\d,]+(?:\.\d+)?)\s*元",
                text,
            ):
                graph.add("payment.total_fee", match.group(1), clause, _number(match.group(1)))
            for match in re.finditer(r"(?:课时费|课程费)[^\d]{0,12}([\d,]+(?:\.\d+)?)\s*元", text):
                graph.add("payment.session_fee_total", match.group(1), clause, _number(match.group(1)))
            for match in re.finditer(r"([\d,]+(?:\.\d+)?)\s*元\s*/\s*(?:节|课时|次|小时)", text):
                graph.add("payment.unit_price", match.group(1), clause, _number(match.group(1)))
            for match in re.finditer(r"[×xX*]\s*(\d+(?:\.\d+)?)\s*(?:节|课时|次|小时)", text):
                graph.add("payment.total_sessions", match.group(1), clause, _number(match.group(1)))
            for match in re.finditer(r"(?:资料费|教材费|材料费)[^\d]{0,12}([\d,]+(?:\.\d+)?)\s*元", text):
                graph.add("payment.material_fee", match.group(1), clause, _number(match.group(1)))
            for match in re.finditer(r"(?:已付|已支付|支付|付款)[^\d]{0,16}([\d,]+(?:\.\d+)?)\s*元", text):
                graph.add("payment.amount_paid", match.group(1), clause, _number(match.group(1)))
            if any(term in text for term in ("余额", "剩余课时", "未消耗课时", "剩余费用", "未提供服务")):
                graph.add("payment.remaining_balance", compacted[:300], clause)
            if any(term in text for term in ("退费", "退款", "按实际课时", "实际消耗课时", "未消耗课时", "未提供服务")):
                graph.add("payment.refund_formula", compacted[:400], clause)
            if any(term in text for term in ("收费标准", "费用明细", "价目表", "课时费", "资料费", "教材费")):
                graph.add("payment.fee_schedule", compacted[:400], clause)

    return graph
