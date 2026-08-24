"""Deterministic facts for patent-right transfer contracts."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from review_v2.technology_service_analysis import analyze_payment_schedule


DATE_RE = re.compile(r"(20\d{2})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日")


def _compact(value: str) -> str:
    return re.sub(r"\s+", "", value or "")


def _amount(value: str) -> Optional[int]:
    match = re.search(r"([\d,]+(?:\.\d+)?)\s*元", value or "")
    return int(float(match.group(1).replace(",", ""))) if match else None


def _date_value(value: str) -> str:
    match = DATE_RE.search(value or "")
    return date(int(match.group(1)), int(match.group(2)), int(match.group(3))).isoformat() if match else ""


def _first_match(text: str, patterns: tuple[str, ...], group: int = 1) -> str:
    for pattern in patterns:
        match = re.search(pattern, text or "", re.S)
        if match:
            return match.group(group).strip("：:；;，,。 \n\t")
    return ""


@dataclass(frozen=True)
class PatentAsset:
    sequence_no: str
    patent_type: str
    patent_number: str
    patent_name: str
    inventors: str
    application_date: str
    grant_date: str
    legal_status: str
    transfer_price: Optional[int]

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PatentPledgeFact:
    exists: bool = False
    pledged_patent: str = ""
    pledgee: str = ""
    registration_no: str = ""
    release_required: bool = False
    release_deadline: str = ""
    release_after_first_payment: bool = False
    registration_blocked_until_release: bool = False

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExistingLicenseFact:
    exists: bool = False
    is_current_transaction: bool = False
    licensed_patent: str = ""
    license_type: str = ""
    licensee: str = ""
    start_date: str = ""
    end_date: str = ""
    scope: str = ""
    region: str = ""
    sublicense_allowed: Optional[bool] = None
    fee_already_received: bool = False
    fee_retained_by_transferor: bool = False
    obligations_assumed_by_transferee: bool = False

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TransferRegistrationFact:
    contract_effective_event: str = ""
    patent_transfer_registration_event: str = ""
    patent_right_transfer_effective_event: str = ""
    responsible_party: str = ""
    conditions: List[str] = field(default_factory=list)
    deadline: str = ""

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


def extract_patent_assets(text: str) -> List[PatentAsset]:
    rows = [line.split("\t") for line in (text or "").splitlines() if "\t" in line]
    header_index = next((index for index, row in enumerate(rows) if {"专利类型", "专利号", "专利名称", "当前法律状态"} <= {cell.strip() for cell in row}), None)
    if header_index is None:
        return []
    header = [cell.strip() for cell in rows[header_index]]
    aliases = {
        "sequence_no": ("序号",), "patent_type": ("专利类型",), "patent_number": ("专利号",),
        "patent_name": ("专利名称",), "inventors": ("发明人或设计人", "发明人", "设计人"),
        "application_date": ("申请日",), "grant_date": ("授权公告日", "授权日"),
        "legal_status": ("当前法律状态", "法律状态"), "transfer_price": ("转让单价", "价格"),
    }

    def column(name: str) -> int:
        return next((header.index(alias) for alias in aliases[name] if alias in header), -1)

    indexes = {name: column(name) for name in aliases}
    assets: List[PatentAsset] = []
    for row in rows[header_index + 1:]:
        number_index = indexes["patent_number"]
        if number_index < 0 or len(row) <= number_index:
            continue
        number = row[number_index].strip()
        if not number or not re.search(r"[A-Z]{0,3}\d{6,}", number, re.I):
            continue

        def value(name: str) -> str:
            index = indexes[name]
            return row[index].strip() if 0 <= index < len(row) else ""

        assets.append(PatentAsset(
            sequence_no=value("sequence_no"), patent_type=value("patent_type"), patent_number=number,
            patent_name=value("patent_name"), inventors=value("inventors"),
            application_date=_date_value(value("application_date")), grant_date=_date_value(value("grant_date")),
            legal_status=value("legal_status"), transfer_price=_amount(value("transfer_price")),
        ))
    return assets


def extract_patent_pledge(text: str) -> PatentPledgeFact:
    compact = _compact(text)
    exists = bool(re.search(r"专利.{0,35}(?:已经|已|存在).{0,12}(?:质押|专利权质押)", compact))
    return PatentPledgeFact(
        exists=exists,
        pledged_patent=_first_match(compact, (r"(第[一二三四五六七八九十\d]+项[^，。；]{0,12}专利).{0,30}质押",)),
        pledgee=_first_match(compact, (r"质权人为([^，。；]{2,40})", r"质权人[:：]([^，。；]{2,40})")),
        registration_no=_first_match(compact, (r"质押登记编号为([^，。；]{3,50})", r"质押登记号[:：]?([^，。；]{3,50})")),
        release_required=exists and any(term in compact for term in ("质押注销", "解除质押")),
        release_deadline=_first_match(compact, (r"收到.{0,18}(?:第一期|首期).{0,12}(?:价款|款项)后([^，。；]{0,16}(?:工作日|日))",)),
        release_after_first_payment=bool(re.search(r"收到.{0,18}(?:第一期|首期).{0,12}(?:价款|款项).{0,25}(?:解除|完成).{0,8}质押", compact)),
        registration_blocked_until_release=bool(re.search(r"(?:登记申请|提交.{0,8}登记).{0,80}质押.{0,12}(?:注销|解除)", compact)),
    )


def extract_existing_license(text: str) -> ExistingLicenseFact:
    compact = _compact(text)
    exists = bool(re.search(r"(?:签订|转让|生效|登记).{0,40}(?:前|既有|原).{0,30}(?:普通|排他|独占)?实施许可", compact)) or "原专利实施许可合同" in compact
    license_type = next((term for term in ("独占实施许可", "排他实施许可", "普通实施许可") if term in compact), "")
    period = re.search(r"许可期限[:：]?(20\d{2}年\d{1,2}月\d{1,2}日)(?:至|到|—|-)(20\d{2}年\d{1,2}月\d{1,2}日)", compact)
    return ExistingLicenseFact(
        exists=exists,
        is_current_transaction=False,
        licensed_patent=_first_match(compact, (r"(第[一二三四五六七八九十\d]+项[^，。；]{0,12}专利).{0,30}(?:普通|排他|独占)实施许可",)),
        license_type=license_type,
        licensee=_first_match(compact, (r"(?:许可给|被许可人为|被许可人[:：])([^，。；]{2,45})",)),
        start_date=_date_value(period.group(1)) if period else "",
        end_date=_date_value(period.group(2)) if period else "",
        scope=_first_match(compact, (r"许可范围[:：]?([^。；]{2,100})",)),
        region=_first_match(compact, (r"许可地域[:：]?([^，。；]{2,30})",)),
        sublicense_allowed=False if re.search(r"(?:是否允许再许可|是否允许转许可)[:：]?(?:不允许|否)", compact) else None,
        fee_already_received=bool(re.search(r"(?:许可费|使用费).{0,16}(?:已经|已).{0,8}(?:收取|支付完毕)|(?:已经|已).{0,8}(?:收取|支付).{0,14}(?:许可费|使用费)", compact)),
        fee_retained_by_transferor=bool(re.search(r"(?:已经|已).{0,8}(?:收取|支付).{0,14}(?:许可费|使用费).{0,18}(?:不向|不再向|无需向).{0,8}(?:受让方|甲方).{0,6}(?:分配|支付)", compact)),
        obligations_assumed_by_transferee=bool(re.search(r"(?:权利|义务).{0,20}(?:受让方|甲方).{0,8}(?:承接|承担)", compact)),
    )


def extract_transfer_registration(text: str) -> TransferRegistrationFact:
    compact = _compact(text)
    conditions = [label for label, pattern in (
        ("TRANSFER_DOCUMENTS_COMPLETE", r"转让合同.{0,8}(?:资料|文件).{0,8}(?:齐备|符合|要求)"),
        ("PLEDGE_RELEASED", r"质押登记.{0,8}(?:已经|已).{0,4}(?:注销|解除)"),
        ("APPLICATION_SIGNED", r"双方.{0,6}签署.{0,12}登记.{0,8}(?:申请|文件)"),
    ) if re.search(pattern, compact)]
    return TransferRegistrationFact(
        contract_effective_event="SIGNATURE_AND_SEAL" if re.search(r"签字.{0,10}(?:盖章|公章).{0,8}生效", compact) else "",
        patent_transfer_registration_event="PATENT_TRANSFER_REGISTRATION" if "专利权转让登记" in compact else "",
        patent_right_transfer_effective_event="REGISTRATION_COMPLETED" if re.search(r"专利权.{0,12}(?:自|于).{0,14}登记.{0,10}(?:转移|转让)", compact) else "",
        responsible_party="PATENT_TRANSFEREE" if re.search(r"(?:受让方|甲方).{0,20}(?:办理|提交).{0,12}专利权转让登记", compact) else "",
        conditions=conditions,
        deadline=_first_match(compact, (r"应在.{0,35}同时满足.{0,12}条件后([^，。；]{0,16}(?:工作日|日))",)),
    )


def analyze_patent_transfer(text: str) -> Dict[str, Any]:
    compact = _compact(text)
    assets = extract_patent_assets(text)
    pledge = extract_patent_pledge(text)
    existing_license = extract_existing_license(text)
    registration = extract_transfer_registration(text)
    payment = analyze_payment_schedule(text)
    total = payment.get("contract_total") or sum(asset.transfer_price or 0 for asset in assets) or None
    publicity_dates = re.search(r"公示期间[:：]?(20\d{2}年\d{1,2}月\d{1,2}日)(?:至|到|—|-)(20\d{2}年\d{1,2}月\d{1,2}日)", compact)
    signing = _first_match(compact, (r"签订时间[:：]?(20\d{2}年\d{1,2}月\d{1,2}日)",))
    publicity_end = _date_value(publicity_dates.group(2)) if publicity_dates else ""
    signing_date = _date_value(signing)
    timeline_conflicts: List[Dict[str, str]] = []
    if publicity_end and signing_date and signing_date < publicity_end:
        timeline_conflicts.append({"type": "SIGNING_BEFORE_PUBLICITY_END", "signing_date": signing_date, "publicity_end_date": publicity_end})
    return {
        "patent_assets": [asset.to_public_dict() for asset in assets],
        "patent_count": len(assets),
        "patent_types": list(dict.fromkeys(asset.patent_type for asset in assets if asset.patent_type)),
        "total_transfer_price": total,
        "patent_pledge": pledge.to_public_dict(),
        "existing_license": existing_license.to_public_dict(),
        "transfer_registration": registration.to_public_dict(),
        "payment": payment,
        "ancillary_transactions": {
            "existing_patent_license": existing_license.exists,
            "patent_pledge": pledge.exists,
            "university_transfer": any(term in compact for term in ("高校", "大学", "校内科技成果", "校内公示")),
            "agreement_pricing": "协议定价" in compact,
            "publicity_completed": bool(publicity_end and signing_date and signing_date >= publicity_end),
            "technical_document_delivery": bool(re.search(r"技术资料.{0,100}(?:提交|交付)", compact)),
        },
        "rights_warranty": {
            "registered_owner_warranty": bool(re.search(r"(?:让与方|乙方).{0,16}保证.{0,30}登记专利权人", compact)),
            "encumbrance_disclosure": pledge.exists and existing_license.exists,
            "invalidity_broad_disclaimer": bool(re.search(r"专利权.{0,24}(?:全部|部分).{0,8}无效.{0,45}(?:不承担|不退|不赔)", compact)),
            "infringement_shift_to_transferee": bool(re.search(r"(?:受让方|甲方).{0,24}按.{0,8}(?:合同|约定).{0,8}实施专利.{0,30}侵犯.{0,35}(?:全部责任|责任).{0,8}(?:受让方|甲方).{0,6}承担", compact)),
        },
        "continuing_obligations": {
            "confidentiality_survives": bool(re.search(r"保密.{0,100}(?:终止|期限届满).{0,18}(?:继续|仍然|不受影响|有效)", compact)),
            "payment_due_after_registration": bool(re.search(r"登记.{0,12}(?:完成|至.{0,8}名下)后.{0,12}(?:支付|付款)", compact)),
            "license_transition_assistance": bool(re.search(r"登记完成后.{0,35}协助.{0,20}(?:被许可人|许可)", compact)),
            "improvement_rights_survive": "后续改进成果" in compact,
            "deemed_fully_performed_on_registration": bool(re.search(r"登记.{0,12}(?:完成|至.{0,8}名下).{0,12}视为.{0,10}(?:全部履行|履行完毕)", compact)),
        },
        "retained_use": {
            "commercial_use_prohibited": bool(re.search(r"(?:让与方|乙方).{0,20}(?:不得|禁止).{0,30}(?:生产经营|商业)", compact)),
            "research_use_reserved": bool(re.search(r"(?:教学|科学研究|科研)", compact)),
            "paid_service_reserved": bool(re.search(r"(?:对外|有偿).{0,8}(?:技术服务|服务)", compact)),
        },
        "dispute_resolution": {
            "arbitration_selected": bool(re.search(r"提交.{0,20}仲裁委员会仲裁", compact)),
            "litigation_selected": bool(re.search(r"(?:人民法院|法院).{0,8}(?:诉讼|管辖)", compact)),
        },
        "breach_liability": {
            "transferee_daily_penalty": bool(re.search(r"(?:受让方|甲方).{0,24}(?:逾期付款|未按.{0,12}付款).{0,30}(?:每日|每逾期一日)", compact)),
            "transferee_additional_penalty": bool(re.search(r"(?:受让方|甲方).{0,18}逾期付款.{0,60}(?:另行|另付|额外).{0,10}违约金", compact)),
            "transfer_failure_refund": bool(re.search(r"登记.{0,16}无法完成.{0,30}(?:退还|返还).{0,12}(?:价款|款项)", compact)),
            "transferor_liability_cap_or_exclusion": bool(re.search(r"(?:退款|退还|返还).{0,35}(?:违约金).{0,45}(?:全部责任|不承担|排除)", compact)),
        },
        "timeline": {
            "publicity_end_date": publicity_end,
            "contract_signing_date": signing_date,
            "contract_effective_event": registration.contract_effective_event,
            "patent_right_transfer_effective_event": registration.patent_right_transfer_effective_event,
            "conflicts": timeline_conflicts,
        },
        "registration_authority_section_present": "以下内容由技术合同登记机构填写" in compact,
        "technical_secret_transfer_included": not bool(re.search(r"(?:不包含|不涉及).{0,12}技术秘密.{0,12}转让|技术秘密转让价款为0元", compact)),
    }


def add_patent_transfer_facts_to_graph(analysis: Dict[str, Any], clauses: List[Any], graph: Any) -> None:
    """Publish source-backed patent facts before the request snapshot freezes."""
    mappings = (
        ("patent.count", analysis.get("patent_count"), ("专利类型", "专利号", "专利名称")),
        ("patent.total_transfer_price", analysis.get("total_transfer_price"), ("专利权转让价款",)),
        ("patent.pledge.exists", (analysis.get("patent_pledge") or {}).get("exists"), ("质押登记", "专利权质押")),
        ("patent.pledge.pledgee", (analysis.get("patent_pledge") or {}).get("pledgee"), ("质权人",)),
        ("patent.pledge.registration_no", (analysis.get("patent_pledge") or {}).get("registration_no"), ("质押登记编号", "质押登记号")),
        ("patent.pledge.release_after_first_payment", (analysis.get("patent_pledge") or {}).get("release_after_first_payment"), ("第一期", "质押注销", "解除质押")),
        ("patent.existing_license.exists", (analysis.get("existing_license") or {}).get("exists"), ("普通实施许可", "原专利实施许可合同")),
        ("patent.existing_license.type", (analysis.get("existing_license") or {}).get("license_type"), ("普通实施许可", "排他实施许可", "独占实施许可")),
        ("patent.existing_license.licensee", (analysis.get("existing_license") or {}).get("licensee"), ("许可给", "被许可人")),
        ("patent.existing_license.current_transaction", False, ("原专利实施许可合同", "签订前")),
        ("patent.registration.responsible_party", (analysis.get("transfer_registration") or {}).get("responsible_party"), ("办理专利权转让登记", "提交专利权转让登记")),
        ("patent.registration.right_effective_event", (analysis.get("transfer_registration") or {}).get("patent_right_transfer_effective_event"), ("专利权转让登记之日起转移", "专利权自登记")),
        ("patent.technical_documents.delivery", (analysis.get("ancillary_transactions") or {}).get("technical_document_delivery"), ("技术资料", "提交时间", "提交方式")),
        ("patent.university.publicity_completed", (analysis.get("ancillary_transactions") or {}).get("publicity_completed"), ("公示期间", "科技成果转化公示")),
    )
    for fact_type, value, terms in mappings:
        if value in (None, "", []):
            continue
        clause = next((row for row in clauses if all(term in _compact(row.text) for term in terms[:2])), None)
        if clause is None:
            clause = next((row for row in clauses if any(term in _compact(row.text) for term in terms)), None)
        if clause is not None:
            graph.add(fact_type, value, clause, value)
    for asset in analysis.get("patent_assets") or []:
        clause = next((row for row in clauses if asset.get("patent_number") and asset["patent_number"] in row.text), None)
        if clause is None:
            continue
        identity = asset.get("patent_number")
        graph.add("patent.asset", asset, clause, identity)
