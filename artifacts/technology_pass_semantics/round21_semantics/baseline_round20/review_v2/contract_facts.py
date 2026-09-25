"""Generic, source-backed facts used by evidence retrieval.

This module does not decide review outcomes. It extracts explicit contract
facts and preserves the clause IDs that support each value.
"""

from __future__ import annotations

import re
import hashlib
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
    "major_decision_process": "technology.governance.major_decision",
    "body_development_scope": "technology.development.scope",
    "body_research_work_allocation": "technology.development.work_allocation",
    "creator_attribution": "technology.creator.attribution",
    "creator_named_identity": "technology.creator.named_identity",
    "creator_list_determination": "technology.creator.list_determination",
    "creator_reward_arrangement": "technology.creator.reward_arrangement",
    "body_acceptance_metrics": "technology.acceptance.quantitative_metrics",
    "test_method": "technology.acceptance.test_method",
    "test_report": "technology.acceptance.test_report",
    "acceptance_dispute_retest": "technology.acceptance.retest",
}


def canonical_fact_key(fact_type: str) -> str:
    key = str(fact_type or "").strip()
    from review_v2.technology_fact_ontology import FACT_KEY_ALIASES
    aliases = {**CANONICAL_FACT_ALIASES, **FACT_KEY_ALIASES}
    # Fact namespaces are not flat report-element identifiers. Resolve known
    # spellings/aliases to the registry address without replacing its dots.
    spellings = {re.sub(r"[\s_.-]+", "_", value).casefold(): value
                 for value in sorted(set(aliases) | set(aliases.values()))}
    key = spellings.get(re.sub(r"[\s_.-]+", "_", key).casefold(), key)
    seen = set()
    while key in aliases and key not in seen:
        seen.add(key)
        key = aliases[key]
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]*", key):
        key = key.casefold().replace('-', '_')
    return key


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

    def add(self, fact_type: str, value: Any, clause: ParsedClause, normalized_value: Any = None, *, source_span: Optional[str] = None) -> None:
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
                fact_id=("f_penalty_" + hashlib.sha256((str(getattr(clause, 'document_id', '') or '') + '|' + clause.clause_id + '|' + str(normalized)).encode()).hexdigest()[:20]
                         if fact_type == "liability.penalty" else f"F-{fact_type.upper().replace('.', '-')}-{len(existing) + 1:03d}"),
                fact_type=fact_type,
                value=value,
                normalized_value=normalized,
                source_clause_ids=[clause.clause_id],
                source_spans=[source_span if source_span and source_span in clause.text else clause.text],
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


def resolve_patent_subject_identity(graph: ContractFactGraph) -> Dict[str, Any]:
    """Join source-backed names and identifiers, without inferring title/proof.

    A sole named asset can be identified across the cover and definitions. For
    multiple identifiers, require an unambiguous name/number pair in each source
    record; a bag of unrelated names and numbers is not sufficient evidence.
    """
    name_facts = graph.facts.get("technology.patent.name", [])
    project_facts = graph.facts.get("technology.project.name", [])
    number_facts = [*graph.facts.get("technology.patent.application_number", []),
                    *graph.facts.get("technology.patent.number", [])]
    by_number: Dict[str, List[ContractFact]] = {}
    for fact in number_facts:
        key = re.sub(r"^(?:ZL|CN)", "", str(fact.value).upper())
        by_number.setdefault(key, []).append(fact)
    if not by_number or not (name_facts or project_facts):
        return {"satisfied": False, "facts": [], "reason": "NAME_OR_IDENTIFIER_NOT_ESTABLISHED"}
    selected: List[ContractFact] = []
    names = name_facts or project_facts
    if len(by_number) == 1 and len({fact.value for fact in names}) == 1:
        selected = [*names, *number_facts]
    else:
        for records in by_number.values():
            pair = []
            for record in records:
                source_ids = set(record.source_clause_ids)
                local_names = [fact for fact in names if source_ids & set(fact.source_clause_ids)]
                local_numbers = {key for key, rows in by_number.items()
                                 if any(source_ids & set(fact.source_clause_ids) for fact in rows)}
                if len({fact.value for fact in local_names}) == 1 and len(local_numbers) == 1:
                    pair = [*local_names, record]
                    break
            if not pair:
                return {"satisfied": False, "facts": [], "reason": "AMBIGUOUS_NAME_IDENTIFIER_ASSOCIATION"}
            selected.extend(pair)
    # Optional identification context does not impose granted-patent proof
    # requirements (owner, grant date, annual fees) on application rights.
    for key in ("technology.patent.applicant", "technology.patent.owner",
                "technology.patent.application_date", "technology.patent.authorization_date"):
        rows = graph.facts.get(key, [])
        if len(by_number) == 1 and len({fact.value for fact in rows}) == 1:
            selected.extend(rows)
    return {"satisfied": True, "facts": list({fact.fact_id: fact for fact in selected}.values()),
            "reason": "SOURCE_BOUND_NAME_AND_UNIQUE_IDENTIFIER", "asset_count": len(by_number)}


REVIEW_FACT_REQUIREMENTS: Dict[str, List[str]] = {
    "technology_subject_description": [
        "technology.patent.name", "technology.project.name", "technology.patent.number",
        "technology.patent.application_number", "technology.patent.owner", "technology.patent.applicant",
    ],
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
    from review_v2.unified_facts.store import CURRENT, fail
    if CURRENT.get() is not None:
        fail('RAW_FACT_REEXTRACTION_FORBIDDEN', 'extract_contract_fact_graph')
    graph = ContractFactGraph()
    for clause in clauses:
        text = clause.text
        compacted = re.sub(r"\s+", "", text)
        for sentence in re.split(r"(?<=[。；;])|\n", text):
            if "违约金" not in sentence:
                continue
            formula = re.search(r"按(?:照)?(?P<base>[^，。；%]{2,30}?)(?:的)?(?P<rate>\d+(?:\.\d+)?[%％])向(?P<beneficiary>甲方|乙方|丙方|委托方|受托方|买方|卖方)支付违约金", sentence)
            period = re.search(r"每(?:逾期|迟延|延期|延迟)?(?:一|1)?(?:个)?(?:天|日)|每日|每天", sentence)
            actors = re.findall(r"甲方|乙方|丙方|委托方|受托方|买方|卖方", sentence[:formula.start()] if formula else "")
            trigger = re.search(
                r"(?:迟延|逾期|延期|延迟)(?:交付|付款|支付)|(?:交付|付款|支付)(?:迟延|逾期|延期|延迟)|"
                r"未按(?:约定的?)?(?:时间|期限).{0,12}?(?:交付|付款|支付)|未按期(?:交付|付款|支付)",
                sentence,
            )
            if formula and period and actors and trigger:
                value = {"trigger": trigger[0], "obligor": actors[-1], "beneficiary": formula['beneficiary'],
                         "period": period[0], "rate": formula['rate'], "base": formula['base'].removesuffix('的'),
                         "consequence": "支付违约金", "raw_clause": sentence.strip()}
                graph.add("liability.penalty", value, clause, source_span=sentence.strip())

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

        # Technology reviews share these source-backed facts across checklist
        # items.  They describe only what the contract expressly says; legal
        # sufficiency and risk remain the responsibility of the consuming rule.
        if clause.section_type in {"正式合同条款", "附件"}:
            # Preserve typed identity fields and their exact spans. An applicant
            # is not a granted owner, and a project title is not a patent title.
            # The consumer decides whether these fields identify the same asset.
            for key, pattern in (
                ("technology.patent.name", r"(?:专利(?:技术)?名称|发明(?:创造)?名称)[：:]\s*([^，,。；;\n|]{2,120})"),
                ("technology.project.name", r"项目名称[：:]\s*([^，,。；;\n|]{2,120})"),
                ("technology.patent.number", r"(?:专利(?:编号|号)|申请号)[：为:]?\s*([A-Za-z]{0,3}\d[\dA-Za-z.\-]{5,40})"),
                ("technology.patent.application_number", r"(?:专利)?申请号[：为:]?\s*([A-Za-z]{0,3}\d[\dA-Za-z.\-]{5,40})"),
                ("technology.patent.owner", r"专利权人[：:]\s*([^，,。；;\n|]{2,120})"),
                ("technology.patent.applicant", r"(?:专利)?申请人[：:]\s*([^，,。；;\n|]{2,120})"),
            ):
                for match in re.finditer(pattern, text):
                    value = match.group(1).strip()
                    if not re.fullmatch(r"[_＿—－\-\s□×xX]+|待填写|待定|另行确定|详见附件", value):
                        graph.add(key, value, clause, source_span=match.group(0))
            # A contractual ownership declaration identifies the stated owner;
            # it does not establish that a certificate was actually supplied.
            for match in re.finditer(
                r"(?P<owner>许可方|转让方|让与方|接受方|被许可方|[甲乙丙丁]方)"
                r"(?:确认|声明|保证|承诺)?(?:其)?(?:为|是)"
                r"[^，,。；;\n]{0,100}?(?:合法)?专利权人", text,
            ):
                if not re.search(r"不是|并非|不属于|不再|尚未|可能|如为|若为", match.group(0)):
                    graph.add("technology.patent.owner", match.group("owner"), clause,
                              source_span=match.group(0))
        application_date = re.search(
            r"(?:专利)?申请日期?[：为:]?\s*(20\d{2}年\d{1,2}月\d{1,2}日)",
            text,
        )
        if application_date:
            graph.add("technology.patent.application_date", application_date.group(1), clause)
        authorization_date = re.search(
            r"(?:授权(?:公告)?日期?|专利批准日期)[：为:]?\s*(20\d{2}年\d{1,2}月\d{1,2}日)|"
            r"(?:已于|于)(20\d{2}年\d{1,2}月\d{1,2}日).{0,24}(?:批准获得专利权|获得专利权|授权)",
            text,
        )
        if authorization_date:
            graph.add(
                "technology.patent.authorization_date",
                authorization_date.group(1) or authorization_date.group(2),
                clause,
                source_span=authorization_date.group(0),
            )
        if any(term in compacted for term in ("共同专利权人", "共有权人", "共同权利人")):
            graph.add("technology.patent.co_owner_disclosure", compacted[:800], clause)
        if any(term in compacted for term in ("既有许可", "在先许可", "此前许可")):
            graph.add("technology.patent.existing_license_disclosure", compacted[:800], clause)
        if "质押" in compacted:
            graph.add("technology.patent.pledge_disclosure", compacted[:800], clause)
        if any(term in compacted for term in ("查封", "保全")):
            graph.add("technology.patent.seizure_disclosure", compacted[:800], clause)
        if re.search(
            r"(?:专利费用|专利年费|年费).{0,30}(?:按时缴纳|已经缴纳|已缴|缴纳凭证)|"
            r"(?:按时缴纳|已经缴纳|已缴).{0,18}(?:专利费用|专利年费|年费)",
            compacted,
        ):
            graph.add("technology.patent.annual_fee_maintenance", compacted[:800], clause)
        if re.search(
            r"(?:专利年费|年费).{0,24}(?:已经缴纳|已缴纳|已缴|缴费正常|缴纳凭证)|"
            r"(?:已经缴纳|已缴纳|已缴).{0,18}(?:专利年费|年费)",
            compacted,
        ):
            graph.add("technology.patent.annual_fee_status", compacted[:800], clause)
        if re.search(r"(?:维持|保持).{0,12}专利(?:权)?有效|维持专利有效", compacted):
            graph.add("technology.patent.validity_maintenance", compacted[:800], clause)
        if (
            "法律状态" in compacted
            and any(term in compacted for term in ("立即", "及时", "书面"))
            and "通知" in compacted
        ):
            graph.add("technology.patent.status_change_notice", compacted[:800], clause)
        if (
            any(term in compacted for term in ("技术服务", "技术指导", "技术支持"))
            and any(term in compacted for term in ("有义务", "应当", "应", "负责", "提供"))
        ):
            graph.add("technology.license.licensor_support", compacted[:800], clause)

        improvement_subject = any(term in compacted for term in (
            "改进和发展的技术", "改进技术", "改进成果", "后续改进", "进一步开发成果",
        ))
        universal_unilateral_improvement = bool(re.search(
            r"(?:无论|不论)由哪一方完成.{0,60}"
            r"(?:知识产权|专利申请权|成果权利).{0,24}(?:均|全部)?归[\u7532\u4e59\u4e19\u4e01\u620a]方所有",
            compacted,
        ))
        if improvement_subject and not universal_unilateral_improvement and re.search(
            r"(?:所有权|知识产权|专利申请权).{0,20}(?:属于|归)(?:实际)?(?:实施|进行|完成|形成)?改进.{0,12}(?:一方|改进方)|"
            r"(?:实际)?(?:实施|进行|完成|形成)?改进.{0,18}(?:一方|改进方).{0,20}(?:所有|享有)",
            compacted,
        ):
            graph.add("technology.improvement.actual_improver_ownership", True, clause)
        if improvement_subject and universal_unilateral_improvement:
            owner_match = re.search(
                r"(?:知识产权|专利申请权|成果权利).{0,24}(?:均|全部)?归([\u7532\u4e59\u4e19\u4e01\u620a])方所有",
                compacted,
            )
            graph.add(
                "technology.improvement.universal_unilateral_assignment",
                f"{owner_match.group(1)}方" if owner_match else True,
                clause,
            )
        if improvement_subject and re.search(
            r"(?:双方|各方).{0,45}(?:相互|互相).{0,12}(?:免费|无偿).{0,35}(?:提供|许可).{0,15}(?:对方|另一方).{0,12}使用",
            compacted,
        ):
            graph.add("technology.improvement.reciprocal_free_use", True, clause)
            graph.add("technology.improvement.material_delivery", True, clause)
        if improvement_subject and re.search(r"(?:另一方|对方).{0,18}不得.{0,18}申请专利", compacted):
            graph.add("technology.improvement.patent_application_restriction", True, clause)
        if improvement_subject and re.search(r"(?:另一方|对方).{0,22}不得.{0,80}(?:向第三方转让|转让给第三方)", compacted):
            graph.add("technology.improvement.third_party_transfer_restriction", True, clause)

        material_type_hits = sum(
            term in compacted
            for term in (
                "专利证书", "专利说明书", "权利要求书", "专利附图", "设计说明",
                "算法接口", "控制模块", "系统集成", "源代码", "参数表", "操作手册",
            )
        )
        if (
            clause.section_type == "附件"
            and material_type_hits >= 2
            and any(term in compacted for term in ("资料清单", "应交付的专利资料", "交付资料"))
        ):
            graph.add("technology.material.attachment_schedule", True, clause)
        if any(term in compacted for term in ("资料交接确认单", "资料交付确认单", "资料签收单")):
            graph.add("technology.material.receipt_confirmation", True, clause)

        technology_terms = (
            "研究开发", "研发", "技术开发", "技术路线", "算法", "模型",
            "源代码", "技术成果", "知识产权", "验收测试", "技术资料",
        )
        if any(term in compacted for term in technology_terms):
            if any(term in compacted for term in (
                "研究开发内容", "研发内容", "开发范围", "技术目标", "项目目标",
                "负责算法", "负责模型", "负责软件", "负责系统", "开发模块",
            )):
                graph.add("technology.development.scope", compacted[:1000], clause)

            party_count = sum(label in compacted for label in ("甲方", "乙方", "丙方", "丁方"))
            explicit_allocation = (
                any(term in compacted for term in ("研发分工", "研究开发分工", "各方分工"))
                and any(term in compacted for term in ("负责", "承担"))
                and "不承担研发" not in compacted
            )
            role_duty_parties = set(re.findall(
                r"([甲乙丙丁])方.{0,70}(?:研究开发内容|研发内容|开发内容)?[：:]?"
                r".{0,24}(?:负责|(?<!不)承担).{0,60}(?:研发|开发|研究|算法|模型|系统|模块)",
                compacted,
            ))
            role_duties = len(role_duty_parties) >= 2
            if party_count >= 2 and (explicit_allocation or role_duties):
                graph.add("technology.development.work_allocation", compacted[:1200], clause)

        if (
            any(term in compacted for term in ("重大事项", "重大研发事项", "技术路线重大调整"))
            and any(term in compacted for term in ("一致同意", "共同同意", "书面同意", "表决决定"))
        ):
            graph.add("technology.governance.major_decision", True, clause)
        if (
            any(term in compacted for term in ("重大事项", "重大技术路线", "技术路线", "预算调整", "成果商业化"))
            and re.search(r"(?:由)?[\u7532\u4e59\u4e19\u4e01\u620a]方.{0,20}(?:最终决定|最终认定|单方决定)", compacted)
        ):
            graph.add("technology.governance.unilateral_major_decision", True, clause)

        clause_body = "\n".join(text.splitlines()[1:]) if "\n" in text else text
        compacted_body = re.sub(r"\s+", "", clause_body)
        named_creator = re.search(
            r"(?:发明人(?:\s*[/／、和]\s*设计人)?|设计人|完成人)(?:姓名)?\s*[：:]\s*([^\n。；;]+)",
            clause_body,
        )
        if named_creator:
            names = named_creator.group(1).strip(" ，,、。")
            if (
                re.fullmatch(r"[\u4e00-\u9fff·]{2,6}(?:\s*[、，,]\s*[\u4e00-\u9fff·]{2,6})*", names)
                and not re.search(r"待定|待填|待补|另行|未明确|不详|无名|姓名|填写|暂无|无权|有权", names)
            ):
                graph.add("technology.creator.named_identity", names, clause)
        if (
            any(term in compacted_body for term in ("完成人", "研发人员", "实际参加项目研发的人员"))
            and "署名" in compacted_body
            and any(term in compacted_body for term in ("有权", "应当", "根据实际贡献", "按照实际贡献"))
        ):
            graph.add("technology.creator.attribution", True, clause)
        if re.search(
            r"完成人(?:员)?名单.{0,50}(?:由.{0,30}(?:确定|确认)|经.{0,30}(?:确定|确认))",
            compacted_body,
        ):
            graph.add("technology.creator.list_determination", True, clause)
        if (
            any(term in compacted_body for term in ("完成人", "研发人员", "实际参加项目研发的人员"))
            and any(term in compacted_body for term in ("奖励", "报酬"))
            and any(term in compacted_body for term in ("给予", "支付", "发放", "标准", "比例", "金额", "时间"))
        ):
            graph.add("technology.creator.reward_arrangement", True, clause)

        if (
            any(term in compacted for term in ("阶段成果", "最终成果", "项目成果", "开发成果", "研究开发成果"))
            and any(term in compacted for term in (
                "共同所有", "共同享有", "归甲方所有", "归乙方所有", "归丙方所有",
                "归完成方所有", "知识产权归属", "专利申请权归", "著作权归",
            ))
        ):
            graph.add("technology.ip.result_ownership", True, clause)
        if (
            any(term in compacted for term in ("研发人员", "员工", "完成人", "职务成果"))
            and any(term in compacted for term in ("成果归集", "权利归属", "知识产权归属", "转让给", "归公司所有"))
        ):
            graph.add("technology.ip.personnel_assignment", True, clause)
        if (
            any(term in compacted for term in ("第三方软件", "第三方组件", "第三方技术", "第三方代码"))
            and any(term in compacted for term in ("授权文件", "许可证文件", "合法授权", "授权清单", "许可清单"))
        ):
            graph.add("technology.ip.third_party_authorization", True, clause)
        if (
            any(term in compacted for term in ("开源软件", "开源组件", "开源代码"))
            and any(term in compacted for term in ("开源许可证", "许可证义务", "开源合规", "许可证清单", "履行开源义务"))
        ):
            graph.add("technology.ip.open_source_compliance", True, clause)

        attachment_reference = bool(
            "附件" in compacted
            and any(term in compacted for term in (
                "附件包括", "附件清单", "作为本合同附件", "作为合同附件", "详见附件",
                "列入附件", "本合同附件", "合同组成部分",
            ))
        )
        attachment_categories = {
            "technical_material": (
                "项目技术需求说明书", "技术需求说明书", "项目研发计划", "研发计划",
                "技术资料清单", "交付文件清单", "接口文档", "源代码清单",
            ),
            "ip_proof": (
                "背景知识产权清单", "知识产权证明", "权属证明", "专利证书",
                "软件著作权登记", "第三方授权清单", "开源组件清单",
            ),
            "acceptance_test": (
                "成果验收测试方案", "验收测试方案", "项目测试及验收方案",
                "验收方案", "验收测试附件", "测试用例清单",
            ),
        }
        for category, markers in attachment_categories.items():
            if attachment_reference and any(marker in compacted for marker in markers):
                graph.add(f"attachment.reference.{category}", True, clause)
            if (
                clause.section_type == "附件"
                and any(marker in compacted for marker in markers)
                and len(compacted_body) >= 40
            ):
                graph.add(f"attachment.content.{category}", True, clause)

        if "承担保密义务" in compacted or re.search(r"(?:应当|应|须)保密", compacted):
            graph.add("technology.confidentiality.obligation", True, clause)
        if re.search(r"未经.{0,30}(?:同意|许可).{0,20}不得.{0,20}(?:向)?第三方披露|不得向第三方披露", compacted):
            graph.add("technology.confidentiality.third_party_disclosure_restriction", True, clause)
        if re.search(r"不得.{0,12}复制|禁止.{0,12}复制", compacted):
            graph.add("technology.confidentiality.copy_restriction", True, clause)
        if re.search(r"不得.{0,20}(?:超出|超范围|合同目的外).{0,12}使用|仅限.{0,30}使用", compacted):
            graph.add("technology.confidentiality.use_restriction", True, clause)

        ip_subject = any(term in compacted for term in (
            "第三方知识产权", "侵犯他人知识产权", "侵犯第三方知识产权",
            "知识产权纠纷", "权利瑕疵", "无权许可", "侵权责任", "第三方指控侵权",
        )) or bool(re.search(r"第三方.{0,24}(?:指控|主张|声称).{0,24}侵权", compacted))
        ip_liability = any(term in compacted for term in (
            "承担侵权责任", "承担全部侵权责任", "承担相应责任", "承担全部责任",
            "承担损失", "承担全部损失", "赔偿损失", "负责处理", "承担50%的损失",
            "承担由此引起的一切法律和经济责任", "承担由此产生的一切法律和经济责任",
        ))
        if ip_subject and ip_liability:
            graph.add("technology.infringement.special_liability", True, clause)

        broad_remedy_scope = bool(
            re.search(
                r"(?:任何一方|任一方|一方|违约方|合作人).{0,35}"
                r"(?:违反|不履行).{0,30}(?:本合同|本协议|上述各条|任何约定|任何义务|合同义务)",
                compacted,
            )
            or re.search(
                r"(?:违反|不履行).{0,30}(?:本合同|本协议|上述各条|任何约定|任何义务|合同义务)"
                r".{0,35}(?:任何一方|任一方|一方|违约方|合作人)",
                compacted,
            )
        )
        general_remedy = any(term in compacted for term in (
            "赔偿损失", "按实际损失赔偿", "违约金", "继续履行", "采取补救措施",
        )) or bool(re.search(r"赔偿.{0,18}(?:实际|直接|全部|相应)?损失", compacted))
        if broad_remedy_scope and general_remedy:
            graph.add("technology.remedy.general_catch_all", True, clause)
        if ip_subject and any(term in compacted for term in (
            "一般损失赔偿", "一般违约责任", "同一损失", "不得重复赔偿",
            "避免重复赔偿", "适用顺序", "累计适用", "抵扣",
        )):
            graph.add("technology.infringement.same_loss_general_remedy", True, clause)
        if any(term in compacted for term in (
            "同一损失不得重复", "不得重复赔偿", "避免重复赔偿",
            "侵权责任与一般", "侵权专项责任与一般", "侵权赔偿与违约金",
        )):
            graph.add("technology.infringement.remedy_coordination", True, clause)

        # Keep acceptance facts atomic. A referenced test exhibit is a
        # different fact from metrics, methods, reports, or retest mechanics
        # already written into the contract body.
        acceptance_subject = any(term in compacted for term in (
            "验收", "验收测试", "测试通过", "测试报告", "技术指标", "性能指标",
        ))
        quantitative_marker = bool(
            re.search(
                r"(?:准确率|召回率|识别率|响应时间|处理时间|并发|稳定运行|可用率|错误率|吞吐量)"
                r".{0,24}(?:\d|百分之|%|％)",
                compacted,
            )
            or re.search(
                r"(?:\d|百分之|%|％).{0,24}"
                r"(?:准确率|召回率|识别率|响应时间|处理时间|并发|稳定运行|可用率|错误率|吞吐量)",
                compacted,
            )
        )
        if acceptance_subject and quantitative_marker:
            graph.add("technology.acceptance.quantitative_metrics", True, clause)
        if acceptance_subject and any(term in compacted for term in (
            "测试方法", "测试步骤", "测试流程", "操作步骤", "统计口径", "测试次数",
        )):
            graph.add("technology.acceptance.test_method", True, clause)
        if "测试报告" in compacted and any(term in compacted for term in (
            "提交", "出具", "形成", "签署", "确认", "交付", "作为验收",
        )):
            graph.add("technology.acceptance.test_report", True, clause)
        if acceptance_subject and any(term in compacted for term in (
            "复测", "重新测试", "再次测试", "第三方检测", "第三方测试", "共同委托检测",
        )):
            graph.add("technology.acceptance.retest", True, clause)

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

    from review_v2.technology_transaction_evidence import register_facts as register_transaction_facts
    register_transaction_facts(graph, clauses)
    from review_v2.technology_fact_ontology import register_ontology_facts
    register_ontology_facts(graph, clauses)
    return graph
