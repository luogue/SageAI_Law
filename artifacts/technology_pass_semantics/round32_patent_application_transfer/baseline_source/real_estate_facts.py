"""Source-backed fact schemas for real-estate sale review packs."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Sequence

from review_v2.clause_parser import ParsedClause
from review_v2.contract_facts import ContractFactGraph


@dataclass
class RealEstateSubject:
    certificate_number: str = ""
    registered_owner: str = ""
    ownership_type: str = ""
    address: str = ""
    property_type: str = ""
    structure: str = ""
    usage: str = ""
    building_area_sqm: Optional[float] = None
    land_ownership: str = ""
    land_acquisition_method: str = ""
    land_usage: str = ""
    land_term_start: str = ""
    land_term_end: str = ""


@dataclass
class MortgageStatus:
    exists: Optional[bool] = None
    mortgagee: str = ""
    outstanding_principal: Optional[float] = None
    release_deadline: str = ""
    payment_suspension_trigger: str = ""
    termination_grace_days: Optional[int] = None


@dataclass
class PurchaseFinancing:
    total_price: Optional[float] = None
    deposit: Optional[float] = None
    first_payment: Optional[float] = None
    cumulative_payment: Optional[float] = None
    loan_amount: Optional[float] = None
    balance: Optional[float] = None
    household_holdback: Optional[float] = None


@dataclass
class RegistrationArrangement:
    transfer_date: str = ""
    institution: str = ""
    advance_notice_registration: Optional[bool] = None
    advance_notice_deadline: str = ""


@dataclass
class PropertyDelivery:
    delivery_date: str = ""
    inspection_deadline: str = ""
    possession_trigger: str = ""
    risk_transfer_trigger: str = ""


@dataclass
class ResidentialAttributes:
    spouse_name: str = ""
    spouse_consent: Optional[bool] = None
    existing_lease: Optional[bool] = None
    household_count: Optional[int] = None
    household_moveout_deadline: str = ""
    maintenance_fund_transfer: Optional[bool] = None
    pre_delivery_arrears_borne_by: str = ""


@dataclass
class RealEstateSaleFacts:
    seller_name: str = ""
    buyer_name: str = ""
    subject: RealEstateSubject = field(default_factory=RealEstateSubject)
    mortgage: MortgageStatus = field(default_factory=MortgageStatus)
    financing: PurchaseFinancing = field(default_factory=PurchaseFinancing)
    registration: RegistrationArrangement = field(default_factory=RegistrationArrangement)
    delivery: PropertyDelivery = field(default_factory=PropertyDelivery)
    residential: ResidentialAttributes = field(default_factory=ResidentialAttributes)
    source_clause_ids: Dict[str, List[str]] = field(default_factory=dict)

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _amount(value: str) -> Optional[float]:
    try:
        return float(value.replace(",", ""))
    except (AttributeError, ValueError):
        return None


def _date(value: str) -> str:
    match = re.search(r"(20\d{2})年(\d{1,2})月(\d{1,2})日", value or "")
    return f"{int(match.group(1)):04d}-{int(match.group(2)):02d}-{int(match.group(3)):02d}" if match else value


def _after(text: str, label: str, pattern: str = r"([^\n|。；;]+)", window: int = 180) -> str:
    pos = 0
    while True:
        pos = text.find(label, pos)
        if pos < 0:
            return ""
        chunk = text[pos + len(label):pos + len(label) + window].lstrip("：: \n|")
        match = re.search(pattern, chunk)
        value = match.group(1).strip() if match else ""
        if value and not value.startswith(label):
            return value
        pos += len(label)


def _amount_after(text: str, label: str, window: int = 240) -> Optional[float]:
    raw = _after(text, label, r"(?:人民币)?\s*([\d,]+(?:\.\d+)?)\s*元", window)
    return _amount(raw)


def _date_after(text: str, label: str, window: int = 220) -> str:
    raw = _after(text, label, r"(20\d{2}年\d{1,2}月\d{1,2}日)", window)
    return _date(raw)


def _source(clauses: Sequence[ParsedClause], *signals: object) -> Optional[ParsedClause]:
    values = [str(value) for value in signals if value not in (None, "")]
    for clause in clauses:
        if any(value in clause.text for value in values):
            return clause
    return clauses[0] if clauses else None


def _record(graph: ContractFactGraph, sources: Dict[str, List[str]], clauses: Sequence[ParsedClause], fact_type: str, value: Any, *signals: object) -> None:
    if value in (None, "", []):
        return
    source_signals = {
        "real_estate.price.total": ("房地产转让价款", "房地产总价"),
        "real_estate.payment.deposit": ("第一笔：定金",),
        "real_estate.payment.first_payment": ("第二笔：首期房款",),
        "real_estate.payment.cumulative": ("累计已支付",),
        "real_estate.payment.loan": ("第三笔：银行贷款", "个人住房贷款"),
        "real_estate.payment.balance": ("第四笔：尾款",),
        "real_estate.payment.household_holdback": ("户口迁出及物业",),
        "real_estate.mortgage.outstanding_principal": ("剩余贷款本金",),
        "real_estate.mortgage.release_deadline": ("结清全部抵押贷款", "完成还贷"),
        "real_estate.land.term_start": ("土地使用权使用年限",),
        "real_estate.land.term_end": ("土地使用权使用年限",),
        "real_estate.delivery.date": ("腾空该房屋",),
        "real_estate.delivery.possession_trigger": ("钥匙", "转移占有"),
        "real_estate.delivery.risk_transfer": ("毁损、灭失风险",),
        "real_estate.household.count": ("登记户口",),
    }.get(fact_type, ())
    clause = _source(clauses, *source_signals, value, *signals)
    if clause is None:
        return
    graph.add(fact_type, value, clause, value)
    sources[fact_type] = [clause.clause_id]


def extract_real_estate_sale_facts(text: str, clauses: Sequence[ParsedClause], graph: ContractFactGraph) -> RealEstateSaleFacts:
    subject = RealEstateSubject(
        certificate_number=_after(text, "房地产权证号为", r"([\u4e00-\u9fff（）()0-9]+不动产权第\d+号)") or (re.search(r"[\u4e00-\u9fff（）()0-9]+不动产权第\d+号", text).group(0) if re.search(r"[\u4e00-\u9fff（）()0-9]+不动产权第\d+号", text) else ""),
        registered_owner=_after(text, "登记权利人为"), ownership_type=_after(text, "登记共有情况"),
        address=_after(text, "房地产坐落"), property_type=_after(text, "房屋类型"),
        structure=_after(text, "房屋结构"), usage=_after(text, "房屋用途"),
        building_area_sqm=_amount(_after(text, "房屋建筑面积", r"([\d.]+)\s*平方米")),
        land_ownership=_after(text, "土地所有权为"), land_acquisition_method=_after(text, "国有土地使用权以"),
        land_usage=_after(text, "土地用途"),
        land_term_start=_date_after(text, "国有土地使用权使用年限从"),
    )
    land_end_match = re.search(r"国有土地使用权使用年限从[\s\S]{0,100}?起至[：:\s\n|]*(20\d{2}年\d{1,2}月\d{1,2}日)", text)
    subject.land_term_end = _date(land_end_match.group(1)) if land_end_match else ""
    mortgage_block_pos = text.find("抵押登记仍未注销")
    mortgage_grace_match = re.search(r"逾期超过[：:\s\n|]*(\d+)\s*日", text[mortgage_block_pos:mortgage_block_pos + 400]) if mortgage_block_pos >= 0 else None
    mortgage = MortgageStatus(
        exists=True if "存在抵押" in text or "存在如下抵押" in text else False if "无抵押" in text else None,
        mortgagee=_after(text, "抵押权人"), outstanding_principal=_amount_after(text, "剩余贷款本金约"),
        release_deadline=_date_after(text, "甲方承诺于"),
        payment_suspension_trigger=_date_after(text, "如截至"),
        termination_grace_days=int(mortgage_grace_match.group(1)) if mortgage_grace_match else None,
    )
    financing = PurchaseFinancing(
        total_price=_amount_after(text, "房地产总价") or _amount_after(text, "房地产转让价款共计"),
        deposit=_amount_after(text, "第一笔：定金"), first_payment=_amount_after(text, "第二笔：首期房款"),
        cumulative_payment=_amount_after(text, "累计已支付"), loan_amount=_amount_after(text, "第三笔：银行贷款"),
        balance=_amount_after(text, "第四笔：尾款"), household_holdback=_amount_after(text, "其中"),
    )
    registration = RegistrationArrangement(
        transfer_date=_date_after(text, "房地产过户"),
        institution="上海市浦东新区房地产交易中心" if "上海市浦东新区房地产交易中心" in text else "",
        advance_notice_registration=True if "预告登记" in text else False,
        advance_notice_deadline=_after(text, "支付第一期房款后", r"[\s\S]{0,60}?(\d+\s*个工作日内)"),
    )
    delivery = PropertyDelivery(
        delivery_date=_date_after(text, "甲方应于"),
        inspection_deadline=_after(text, "收到甲方书面交房通知之日起", r"(\d+\s*日内)"),
        possession_trigger="handover_and_keys" if "钥匙" in text and ("转移占有" in text or "验收交接" in text) else "handover",
        risk_transfer_trigger="possession_handover" if "毁损、灭失风险" in text and "实际交付" in text else "",
    )
    spouse = _after(text, "甲方配偶")
    household_match = re.search(r"目前该房地产内登记户口[：:\s\n|]*(\d+)\s*人", text)
    household = household_match.group(1) if household_match else ""
    residential = ResidentialAttributes(
        spouse_name=spouse, spouse_consent=True if spouse and ("同意出售" in text or "无异议" in text) else None,
        existing_lease=False if "无租赁" in text or "不存在出租情况" in text else True if "存在租赁" in text else None,
        household_count=int(household) if household else None,
        household_moveout_deadline=_after(text, "户口迁移", r"[\s\S]{0,300}?(\d+\s*日内)"),
        maintenance_fund_transfer=True if "维修资金账户户名变更" in text else None,
        pre_delivery_arrears_borne_by="seller" if "欠缴" in text and "甲方负责补足" in text else "",
    )
    facts = RealEstateSaleFacts(
        seller_name=_after(text, "卖售人（甲方）") or _after(text, "出卖人（甲方）"),
        buyer_name=_after(text, "买受人（乙方）"), subject=subject, mortgage=mortgage,
        financing=financing, registration=registration, delivery=delivery, residential=residential,
    )
    mappings = {
        "party.seller.name": facts.seller_name, "party.buyer.name": facts.buyer_name,
        "real_estate.certificate.number": subject.certificate_number, "real_estate.owner.name": subject.registered_owner,
        "real_estate.ownership.type": subject.ownership_type, "real_estate.address": subject.address,
        "real_estate.property.type": subject.property_type, "real_estate.property.usage": subject.usage,
        "real_estate.area.building_sqm": subject.building_area_sqm, "real_estate.land.ownership": subject.land_ownership,
        "real_estate.land.acquisition_method": subject.land_acquisition_method, "real_estate.land.usage": subject.land_usage,
        "real_estate.land.term_start": subject.land_term_start, "real_estate.land.term_end": subject.land_term_end,
        "real_estate.mortgage.exists": mortgage.exists, "real_estate.mortgage.mortgagee": mortgage.mortgagee,
        "real_estate.mortgage.outstanding_principal": mortgage.outstanding_principal,
        "real_estate.mortgage.release_deadline": mortgage.release_deadline,
        "real_estate.price.total": financing.total_price, "real_estate.payment.deposit": financing.deposit,
        "real_estate.payment.first_payment": financing.first_payment, "real_estate.payment.cumulative": financing.cumulative_payment,
        "real_estate.payment.loan": financing.loan_amount, "real_estate.payment.balance": financing.balance,
        "real_estate.payment.household_holdback": financing.household_holdback,
        "real_estate.registration.institution": registration.institution,
        "real_estate.registration.advance_notice": registration.advance_notice_registration,
        "real_estate.registration.advance_notice_deadline": registration.advance_notice_deadline,
        "real_estate.delivery.date": delivery.delivery_date, "real_estate.delivery.inspection_deadline": delivery.inspection_deadline,
        "real_estate.delivery.possession_trigger": delivery.possession_trigger, "real_estate.delivery.risk_transfer": delivery.risk_transfer_trigger,
        "real_estate.spouse.name": residential.spouse_name, "real_estate.spouse.consent": residential.spouse_consent,
        "real_estate.lease.exists": residential.existing_lease, "real_estate.household.count": residential.household_count,
        "real_estate.maintenance_fund.transfer": residential.maintenance_fund_transfer,
        "real_estate.fees.pre_delivery_borne_by": residential.pre_delivery_arrears_borne_by,
    }
    for fact_type, value in mappings.items():
        _record(graph, facts.source_clause_ids, clauses, fact_type, value, fact_type.rsplit(".", 1)[-1])
    return facts
