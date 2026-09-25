"""Deterministic facts for patent-right transfer contracts."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from review_v2.technology_service_analysis import analyze_payment_schedule
from review_v2.clause_parser import parse_contract_clauses


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


def analyze_dispute_resolution_options(text: str) -> Dict[str, Any]:
    """Resolve mutually exclusive dispute options from their operative polarity."""
    fragments = [row.strip() for row in re.split(r"[\n。；;]", text or "") if row.strip()]
    inactive = re.compile(r"(?:不适用|不选择|未选择|不采用|已删除|删除|未勾选|否|[×✕])")

    def option_state(keyword: str, operative: re.Pattern[str]) -> tuple[bool, List[str], List[str]]:
        active_rows: List[str] = []
        inactive_rows: List[str] = []
        for row in fragments:
            if keyword not in row:
                continue
            compact_row = _compact(row)
            if inactive.search(compact_row) or re.search(rf"(?:□|○)\s*[^。；]*{keyword}", row):
                inactive_rows.append(row)
            elif operative.search(compact_row):
                active_rows.append(row)
        return bool(active_rows), active_rows, inactive_rows

    arbitration, arbitration_evidence, arbitration_inactive = option_state(
        "仲裁", re.compile(r"(?:提交|申请|争议由|争议应由).{0,30}仲裁(?:委员会)?(?:仲裁)?"),
    )
    litigation, litigation_evidence, litigation_inactive = option_state(
        "法院", re.compile(r"(?:向|由).{0,20}(?:人民法院|法院).{0,15}(?:提起诉讼|诉讼|管辖)"),
    )
    return {
        "arbitration_selected": arbitration,
        "litigation_selected": litigation,
        "arbitration_evidence": arbitration_evidence,
        "litigation_evidence": litigation_evidence,
        "arbitration_inactive_evidence": arbitration_inactive,
        "litigation_inactive_evidence": litigation_inactive,
    }


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
    pledgee_consent_required: bool = False
    pledgee_consent_obtained: bool = False
    pledge_released: bool = False
    registration_feasibility_blocked: bool = False

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
    consent_required = exists and bool(re.search(
        r"(?:质权人.{0,12}(?:同意|书面同意)|(?:取得|办理).{0,16}质权人.{0,8}(?:同意|书面同意))",
        compact,
    ))
    consent_not_obtained = bool(re.search(
        r"(?:尚未|未|没有|未能)取得.{0,24}质权人.{0,8}(?:同意|书面文件)|"
        r"质权人.{0,12}(?:同意|书面文件).{0,8}(?:尚未|未)取得",
        compact,
    ))
    consent_obtained = not consent_not_obtained and bool(re.search(
        r"(?:已取得|已经取得).{0,24}质权人.{0,8}(?:同意|书面文件)|"
        r"质权人.{0,12}(?:已|已经)(?:书面)?同意",
        compact,
    ))
    release_negated = bool(re.search(r"(?:尚未|未|没有|未能)(?:办理|完成)?(?:质押注销|解除质押)|(?:质押|质押登记).{0,10}(?:尚未|未)(?:注销|解除)", compact))
    released = not release_negated and bool(re.search(
        r"(?:质押|质押登记)(?:已|已经)(?:办理|完成)?(?:注销|解除)|"
        r"(?:已|已经)(?:办理|完成)?(?:质押注销|解除质押)",
        compact,
    ))
    feasibility_blocked = bool(exists and consent_required and not consent_obtained and not released)
    return PatentPledgeFact(
        exists=exists,
        pledged_patent=_first_match(compact, (r"(第[一二三四五六七八九十\d]+项[^，。；]{0,12}专利).{0,30}质押",)),
        pledgee=_first_match(compact, (r"质权人为([^，。；]{2,40})", r"质权人[:：]([^，。；]{2,40})")),
        registration_no=_first_match(compact, (r"质押登记编号为([^，。；]{3,50})", r"质押登记号[:：]?([^，。；]{3,50})")),
        release_required=exists and any(term in compact for term in ("质押注销", "解除质押")),
        release_deadline=_first_match(compact, (r"收到.{0,18}(?:第一期|首期).{0,12}(?:价款|款项)后([^，。；]{0,16}(?:工作日|日))",)),
        release_after_first_payment=bool(re.search(r"收到.{0,18}(?:第一期|首期).{0,12}(?:价款|款项).{0,25}(?:解除|完成).{0,8}质押", compact)),
        registration_blocked_until_release=bool(
            re.search(r"(?:登记申请|提交.{0,8}登记).{0,80}质押.{0,12}(?:注销|解除)", compact)
            or feasibility_blocked
        ),
        pledgee_consent_required=consent_required,
        pledgee_consent_obtained=consent_obtained,
        pledge_released=released,
        registration_feasibility_blocked=feasibility_blocked,
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


def extract_transfer_authority_facts(clauses: List[Any]) -> List[Dict[str, str]]:
    """Resolve the warranting party and its disposition assertion separately.

    A/B labels have no inherent transaction role. Use contract declarations
    where available; a standalone self-representation can identify its own
    actor, but a declared recipient's statement is not the transferor's warranty.
    This is contractual representation only, never independent title proof.
    """
    provider_roles = r"(?:让与方|让与人|转让方|转让人|出让方|卖方)"
    recipient_roles = r"(?:受让方|受让人|买方)"
    text = "\n".join(clause.text for clause in clauses)

    def declared_aliases(roles: str) -> set[str]:
        patterns = (
            rf"(?P<party>[甲乙丙丁]方)\s*[（(][^）)\n]{{0,20}}{roles}[^）)\n]{{0,20}}[）)]",
            rf"{roles}\s*[（(][^）)\n]{{0,20}}(?P<party>[甲乙丙丁]方)[^）)\n]{{0,20}}[）)]",
            rf"(?P<party>[甲乙丙丁]方)(?:为|系|作为){roles}",
            rf"{roles}(?:为|是|即)(?P<party>[甲乙丙丁]方)",
        )
        return {match.group("party") for pattern in patterns for match in re.finditer(pattern, text)}

    providers = declared_aliases(provider_roles)
    recipients = declared_aliases(recipient_roles)
    actor_pattern = re.compile(provider_roles + r"|[甲乙丙丁]方")
    authority = re.compile(
        r"有权(?:依法)?(?:转让|处分)|"
        r"(?:具有|享有|拥有)(?:合法[、，,]?)?(?:完整)?(?:的)?处分权|"
        r"(?:合法[、，,]?)?完整处分权"
    )
    asset = re.compile(r"专利申请权|专利权")
    result: List[Dict[str, str]] = []
    for clause in clauses:
        if getattr(clause, "party_obligation", True) is False:
            continue
        for sentence in re.split(r"[。；;\n]", clause.text):
            compact = _compact(sentence)
            for actor_match in actor_pattern.finditer(compact):
                actor = actor_match.group()
                if actor in recipients or (providers and re.fullmatch(r"[甲乙丙丁]方", actor) and actor not in providers):
                    continue
                # Stop at the next explicit party, not at an arbitrary keyword
                # window that may accidentally borrow another actor's warranty.
                next_actor = re.search(r"[甲乙丙丁]方|受让[方人]|让与[方人]|转让[方人]|出让方|买方|卖方", compact[actor_match.end():])
                end = actor_match.end() + next_actor.start() if next_actor else len(compact)
                statement = compact[actor_match.start():end]
                assertion = authority.search(statement)
                asset_match = asset.search(statement)
                if not assertion or not asset_match:
                    continue
                between = (statement[asset_match.end():assertion.start()] if asset_match.end() <= assertion.start()
                           else statement[assertion.end():asset_match.start()])
                if re.search(r"[，,]", between) and not re.fullmatch(r"[，,](?:并|且|同时|包括)(?:其)?", between):
                    continue
                prefix = statement[:assertion.end()]
                if re.search(r"不保证|未保证|无法保证|不能保证|未能保证|不确认|是否|无权|无(?:合法)?(?:完整)?处分权|(?:不|未)(?:具有|享有|拥有)|待核实", prefix):
                    continue
                if re.search(r"(?:如果|假如|若|假设|如)(?:其|该方|[甲乙丙丁]方)?(?:保证其|确认其)?(?:有权|具有|享有|拥有)", compact[:actor_match.start()] + prefix):
                    continue
                result.append({
                    "clause_id": clause.clause_id, "quote": sentence.strip(), "location": clause.location,
                    "actor": actor, "evidence_level": "CONTRACTUAL_REPRESENTATION",
                    "asset_type": "PATENT_APPLICATION_RIGHT" if asset_match.group() == "专利申请权" else "PATENT_RIGHT",
                })
                break
    return result


def extract_application_rejection_facts(clauses: List[Any]) -> Dict[str, Any]:
    """Application rejection is not granted-patent invalidity or delivery rejection.

    Keep event scope and exact sentence quotes, including conditional remedies.
    Naming a remedy under a narrow fault exception does not make it general.
    """
    facts: Dict[str, Any] = {}
    specs = (
        ("rejection_paid_fees_nonrefundable", r"(?:已.{0,10}(?:支付|收取)|已付).{0,25}(?:价款|费|款).{0,12}(?:不予退还|不退|不予返还)", "ADVERSE"),
        ("rejection_unpaid_fees_continue", r"(?:尚未|未付|未支付).{0,45}(?:仍|继续).{0,35}支付", "ADVERSE"),
        ("rejection_termination_prohibited", r"(?:不得|无权|不允许).{0,40}解除", "ADVERSE"),
        ("rejection_termination_right", r"(?:有权|可以|可).{0,16}解除", "COVERED"),
        ("rejection_future_price_adjustment", r"(?:停止支付|无需继续支付|调减.{0,8}(?:价款|费用)|按.{0,15}(?:比例|价值).{0,15}结算)", "COVERED"),
        ("rejection_independent_value_settlement", r"(?:技术秘密|技术资料|独立价值).{0,45}(?:分项|单独|分别).{0,15}(?:结算|计价)|(?:分项|单独)结算.{0,25}(?:技术秘密|技术资料)", "COVERED"),
        ("rejection_concealment_refund", r"(?:隐瞒|未披露).{0,90}(?:退还|返还|退款)", "COVERED"),
        ("rejection_concealment_damages", r"(?:隐瞒|未披露).{0,90}(?:赔偿|承担损失)", "COVERED"),
    )
    active_article = None
    for clause in clauses:
        article = re.match(r"第[一二三四五六七八九十百\d]+条", str(clause.location))
        article_id = article.group(0) if article else clause.clause_id
        text = clause.text
        trigger = any(
            re.search(r"专利申请.{0,65}(?:被|遭|受到).{0,30}驳回", re.sub(r"\s+", "", sentence))
            and not re.search(r"(?:未|尚未|不会|并未).{0,4}被.{0,20}驳回", sentence)
            for sentence in re.split(r"[。；;\n]", text)
        )
        if trigger:
            active_article = article_id
        if active_article != article_id:
            continue
        for sentence in re.split(r"[。；;\n]", text):
            value = re.sub(r"\s+", "", sentence)
            if not value:
                continue
            def add(key, status):
                facts.setdefault(key, []).append({"clause_id": clause.clause_id, "quote": sentence.strip(),
                                                   "location": clause.location, "status": status})
            if re.search(r"专利申请.{0,65}(?:被|遭).{0,30}驳回", value) and not re.search(r"(?:未|尚未|不会|并未).{0,4}被.{0,20}驳回", value):
                add("application_rejection_trigger", "COVERED")
            for key, pattern, status in specs:
                if re.search(pattern, value):
                    if key == "rejection_unpaid_fees_continue" and re.search(r"无需|无须|不再|停止", value):
                        continue
                    add(key, status)
            if re.search(r"(?:只有|仅在|仅当).{0,100}(?:证明|证实).{0,70}(?:明知|知道).{0,50}隐瞒", value):
                add("rejection_narrow_fault_exception", "ADVERSE")
            # Explicit distinct consequences, not the phrase "全部或部分".
            if re.search(r"(?:全部|部分)驳回.{0,30}(?:应|可|按|则).{0,35}(?:结算|调减|停止支付|解除|比例)", value):
                add("rejection_differentiated_outcomes", "COVERED")
    return facts


def extract_transfer_registration_facts(clauses: List[Any]) -> Dict[str, Any]:
    """Registration duties are actor-neutral and bound to the registration event.

    Either contracting party may submit the application. Material cooperation
    may follow the registration sentence, but unrelated delivery/cooperation
    clauses cannot supply it. Keep responsibility and timing independently true.
    """
    facts: Dict[str, List[Dict[str, str]]] = {}
    event = re.compile(r"(?:专利(?:申请)?权转让|申请人变更|专利权人变更).{0,8}登记")
    actor = r"(?:[甲乙丙丁]方|受让[方人]|让与[方人]|转让[方人]|出让方|[买卖]方)"

    def add(key: str, clause: Any, sentence: str) -> None:
        facts.setdefault(key, []).append({
            "clause_id": clause.clause_id, "quote": sentence.strip(), "location": clause.location,
        })

    for clause in clauses:
        if getattr(clause, "party_obligation", True) is False or not event.search(_compact(clause.text)):
            continue
        registration_context = False
        for sentence in re.split(r"[。；;\n]", clause.text):
            s = _compact(sentence)
            explicit_event = bool(event.search(s))
            if explicit_event:
                registration_context = True
            elif re.search(r"资料交付|交付技术资料|验收|侵权|保密|缴纳年费", s):
                registration_context = False
            if not registration_context:
                continue
            negative = bool(re.search(r"(?:未约定|未明确|无需|无须|不负责|另行协商)", s))
            submission_action = bool(re.search(
                r"(?:办理|提交).{0,25}(?:申请权转让|专利权转让|申请人变更|专利权人变更|转让登记)|"
                r"(?:申请权转让|专利权转让|申请人变更|转让登记).{0,20}(?:由|应|须).{0,18}(?:办理|提交)", s,
            ))
            if submission_action and not negative:
                if re.search(actor + r".{0,18}(?:负责|应当|应|须).{0,65}(?:办理|提交)|(?:办理|提交).{0,30}由" + actor + r"负责", s):
                    add("registration_responsible_party", clause, sentence)
                if re.search(r"(?:\d+|[一二三四五六七八九十百]+)(?:个)?(?:工作日|日|天|月)内", s):
                    add("registration_deadline", clause, sentence)
            if not negative and re.search(actor + r".{0,12}(?:应当|应|须|负责|提供|配合|协助)", s):
                if re.search(r"(?:提供|提交|准备).{0,25}(?:资料|文件|材料)|(?:资料|文件|材料).{0,25}(?:提供|配合|协助)", s):
                    add("registration_cooperation", clause, sentence)
    return facts


def extract_third_party_claim_protection_facts(clauses: List[Any]) -> Dict[str, Any]:
    """Bind each claim-response duty to its own event, actor and polarity.

    Registration assistance, invalidity consequences and general remedies are
    not third-party-claim protection.  Negotiating liability is recorded, but
    never promoted to a handling, damages, termination or refund obligation.
    """
    facts: Dict[str, List[Dict[str, str]]] = {}
    provider = r"(?:转让方|让与方|出让方|卖方|让与人|转让人|许可方|许可人)"
    recipient = r"(?:受让方|受让人|买方|被许可方|被许可人)"
    claim_event = re.compile(
        r"(?:第三方|第三人|他人).{0,45}(?:侵权|侵害|知识产权|权利主张|索赔)|"
        r"(?:侵权|侵害).{0,25}(?:第三方|第三人|他人)|权利(?:来源)?瑕疵|无权处分"
    )
    other_event = re.compile(
        r"专利(?:权)?.{0,15}(?:宣告无效|无效程序)|资料验收|登记失败|转让登记|办理.{0,12}登记|"
        r"不可抗力|逾期付款|保密义务|本合同履行|履行本合同|违反本合同|任何义务|任一义务"
    )

    def add(key: str, clause: Any, sentence: str) -> None:
        row = {"clause_id": clause.clause_id, "quote": sentence.strip(), "location": clause.location}
        if row not in facts.setdefault(key, []):
            facts[key].append(row)

    for clause in clauses:
        if getattr(clause, "party_obligation", True) is False:
            continue
        claim_context = False
        actor = ""
        for sentence in re.split(r"[。；;\n]", clause.text):
            s = _compact(sentence)
            if not s or s == _compact(getattr(clause, "title", "")):
                continue
            explicit_event = bool(claim_event.search(s))
            if other_event.search(s) and not explicit_event:
                claim_context = False
                actor = ""
            if explicit_event:
                claim_context = True
                add("claim_trigger", clause, sentence)
            if not claim_context:
                continue
            if re.search(r"(?:另行|另行再|届时|双方).{0,8}协商.{0,15}责任|责任.{0,12}(?:另行协商|另议|待定)", s):
                add("claim_allocation_negotiation", clause, sentence)
            if re.search(r"(?:应当|应|须|及时).{0,16}(?:通知|告知)", s):
                if not re.search(r"(?:无需|无须|不必|未约定).{0,12}(?:通知|告知)", s):
                    add("claim_notice", clause, sentence)
                    if re.search(r"(?:\d+|[一二三四五六七八九十]+)(?:个)?(?:工作日|日|天)内.{0,15}(?:通知|告知)", s):
                        add("claim_notice_deadline", clause, sentence)
            # Rights belonging to the recipient need their own affirmative text.
            if re.search(recipient + r".{0,15}(?:有权|可以|可|得)解除", s) and not re.search(r"(?:无权|不得|不能|不可)解除", s):
                add("claim_termination", clause, sentence)
            if re.search(r"(?:受让方|受让人|买方).{0,18}(?:擅自修改|超范围实施|擅自再许可).{0,45}(?:承担|负责)", s):
                add("claim_recipient_fault_boundary", clause, sentence)
            if "和解" in s and re.search(r"(?:应|须|需|不得|有权|负责|决定).{0,35}(?:协商|同意|和解)|和解.{0,20}(?:应|须|需|同意)", s):
                add("claim_settlement", clause, sentence)
            for part in re.split(r"[，,]", s):
                provider_match = re.search(provider, part)
                recipient_match = re.search(recipient, part)
                if provider_match or recipient_match:
                    actor = "provider" if provider_match and (not recipient_match or provider_match.start() < recipient_match.start()) else "recipient"
                assigned_provider = bool(re.search(r"由" + provider + r".{0,10}(?:承担|负责|赔偿)", part))
                if actor != "provider" and not assigned_provider:
                    continue
                # The action, not a distant keyword, must be affirmative.
                positive = part.replace("不得拒绝", "应")
                if re.search(r"不保证|(?:不|无需|无须|不必|未约定).{0,6}(?:承担|负责|协助|参与|提供|赔偿|退还|返还|退款)|另行协商|待定", positive):
                    continue
                if re.search(r"(?:应|须|负责|参与|协助).{0,20}(?:处理|交涉|抗辩)|(?:提供|给予).{0,8}(?:必要)?协助", positive):
                    add("claim_participation", clause, sentence)
                if re.search(r"(?:提供|提交).{0,25}(?:权属|技术来源|授权链|证明|证据).{0,8}(?:文件|材料)", positive):
                    add("claim_document_assistance", clause, sentence)
                if re.search(r"抗辩控制权|主导抗辩|负责抗辩", positive):
                    add("claim_defense_control", clause, sentence)
                if re.search(r"(?:选择|选聘|委托).{0,6}律师|律师选择权", positive):
                    add("claim_lawyer_selection", clause, sentence)
                if re.search(r"(?:承担|负担|支付).{0,25}(?:抗辩费用|法律费用|律师费|诉讼费)|(?:抗辩费用|法律费用|律师费|诉讼费).{0,25}(?:承担|负担|支付)", positive):
                    add("claim_defense_cost", clause, sentence)
                if re.search(r"(?:赔偿.{0,18}(?:损失|损害)|承担.{0,15}(?:赔偿责任|侵权责任|全部责任|全部损失)|责任.{0,15}由" + provider + r"承担)", positive):
                    add("claim_damages", clause, sentence)
                if re.search(r"(?:退还|返还|退回).{0,20}(?:款|费)|(?:应|须|负责)退款", positive):
                    add("claim_refund", clause, sentence)
                if re.search(r"(?:提供|采取).{0,20}(?:替代技术|替代方案|绕开侵权)", positive):
                    add("claim_replacement", clause, sentence)
                if re.search(r"取得第三方授权|排除权利瑕疵|修复权利瑕疵|补办授权", positive):
                    add("claim_rights_cure", clause, sentence)
    return facts


def extract_patent_transfer_protection_facts(clauses: List[Any]) -> Dict[str, Any]:
    """Keep acquisition, invalidity and delivery remedies as separate source claims."""
    facts = extract_third_party_claim_protection_facts(clauses)

    def add(key: str, clause: Any, quote: str) -> None:
        fact = {"clause_id": clause.clause_id, "quote": quote, "location": clause.location}
        if fact not in facts.setdefault(key, []):
            facts[key].append(fact)

    for clause in clauses:
        body = _compact(clause.text)
        sentences = [s for s in re.split(r"[。；;\n]", clause.text) if s.strip()]
        invalidity_context = bool(re.search(r"专利(?:权)?.{0,30}(?:全部|整体).{0,12}(?:无效|失效)", body))
        delivery_context = bool(re.search(r"(?:资料|文件).{0,20}(?:交付|验收)|(?:交付|验收).{0,20}(?:资料|文件)", body))
        for sentence in sentences:
            s = _compact(sentence)
            title_statement = re.sub(r"专利(?:申请)?权转让合同", "合同", s)
            ownership = bool(re.search(r"专利(?:申请)?权.{0,65}(?:归.{0,15}所有|转移|转让.{0,8}生效)", title_statement))
            if ownership:
                # A contract's own effectiveness or an interim implementation licence
                # is not an assertion that patent title has already transferred.
                event = re.search(r"(?:自|于|在).{0,18}(签署|签订|签字|付款|支付|交付).{0,25}(?:之日|当日|之时|时|后|日起)", s)
                negated = bool(re.search(r"(?:不|并非|不得|不能|并不)(?:自|于|因|在)|不发生转移|不归.{0,10}所有", s))
                if event and not negated and "登记" not in event.group(0):
                    add("nonregistration_title_transfer", clause, sentence)
                if re.search(r"(?:自|于).{0,16}登记.{0,14}(?:生效|转移|归)", s) and not negated:
                    add("registration_title_transfer", clause, sentence)
            if invalidity_context:
                if re.search(r"(?:仍(?:应|须|需)?|继续|必须).{0,8}(?:支付|付清).{0,15}(?:尚未|未付|剩余|剩下).{0,15}(?:转让费|价款|费用)", s) and not re.search(r"(?:无需|不再|不必|免于).{0,6}(?:继续)?支付", s):
                    add("invalidity_unpaid_fees_continue", clause, sentence)
                if re.search(r"(?:全部|所有)(?:费用|损失|责任|风险).{0,10}由(?:受让方|受让人|买方|甲方).{0,8}承担", s) and not re.search(r"因(?:受让方|受让人|买方|甲方).{0,12}(?:过错|恶意|故意)", s):
                    add("invalidity_costs_shifted", clause, sentence)
                if re.search(r"(?:不退|无需退还|不予退还).{0,25}(?:已|已经).{0,12}(?:转让费|价款)", s):
                    add("invalidity_paid_fees_nonrefund", clause, sentence)
                if re.search(r"专利(?:权)?.{0,30}(?:全部|整体).{0,12}(?:无效|失效)", s):
                    add("total_invalidity_trigger", clause, sentence)
            if re.search(r"(?:转让方|让与方|出让方|卖方|乙方).{0,18}(?:可以|有权|保留).{0,12}(?:继续|无偿|免费).{0,10}(?:使用|实施).{0,12}专利", s):
                add("transferor_retained_implementation", clause, sentence)
            if re.search(r"(?:此前|既有|已有|原有|曾于|已经).{0,65}(?:许可|授权).{0,55}(?:使用|实施|期限)", s):
                add("existing_implementation_license", clause, sentence)
            if re.search(r"(?:签订|签署|生效)后.{0,15}(?:日|天)内.{0,30}支付", s) and re.search(r"(?:占总价|占合同总价|比例为).{0,3}\d+(?:\.\d+)?%", s) and "登记" not in s:
                add("payment_due_without_registration", clause, sentence)
            if not delivery_context:
                continue
            for key, pattern in (
                ("delivery_document_list", r"专利证书|专利说明书|权利要求书|专利申请文件|技术图纸"),
                ("delivery_time", r"(?:生效|签订|收到|签署)后.{0,12}(?:日|天)内.{0,35}交付|交付时间[：:]"),
                ("delivery_method", r"(?:通过|采用|以).{0,12}(?:电子邮件|电子文件|纸质|快递)|交付方式[：:]"),
                ("delivery_acceptance", r"(?:收到资料|交付)后.{0,10}(?:日|天)内.{0,8}验收|验收标准[：:]"),
                ("nonconforming_delivery_remedy", r"(?:不合格|不符合|未通过|缺漏).{0,25}(?:负责|应当|应|须).{0,12}(?:补充|补救|补正|整改|重新交付)"),
                ("delivery_remedy_deadline", r"(?:应|须|负责).{0,8}(?:在)?(?:\d+|[一二三四五六七八九十]+)(?:个工作)?(?:日|天)内.{0,10}(?:补充|补救|补正|整改)|(?:补充|补救|整改)期限(?:为|[：:])(?:\d+|[一二三四五六七八九十]+)(?:个工作)?(?:日|天)"),
                ("delivery_failed_cure_termination", r"(?:未|不|无法|不能).{0,20}(?:补救|补充|补正|合格|目的).{0,40}(?:有权|可以|可|得)解除"),
                ("delivery_failed_cure_refund", r"(?:补救|补充|补正|不合格|解除).{0,50}(?:应当|应|须|负责).{0,10}(?:退还|返还|退回).{0,15}(?:款|费)"),
            ):
                if re.search(pattern, s) and not re.search(r"(?:未约定|不约定|无需|无须|不得|无权).{0,10}(?:补充|补救|解除|退还|退款)", s[:s.find("，") if "，" in s else len(s)]):
                    add(key, clause, sentence)
    return facts


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
        "protection_facts": extract_patent_transfer_protection_facts(parse_contract_clauses(text)),
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
            "infringement_shift_to_transferee": bool(re.search(
                r"(?:受让方|甲方).{0,24}(?:按约|按照?.{0,8}(?:合同|约定)).{0,8}实施专利"
                r".{0,30}侵犯.{0,35}(?:全部责任|责任).{0,8}(?:受让方|甲方).{0,6}承担",
                compact,
            )),
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
        "dispute_resolution": analyze_dispute_resolution_options(text),
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
    by_id = {clause.clause_id: clause for clause in clauses}
    for key, rows in (analysis.get("protection_facts") or {}).items():
        for row in rows:
            if row["clause_id"] in by_id:
                graph.add("patent.protection." + key, row["quote"], by_id[row["clause_id"]])
    mappings = (
        ("patent.count", analysis.get("patent_count"), ("专利类型", "专利号", "专利名称")),
        ("patent.total_transfer_price", analysis.get("total_transfer_price"), ("专利权转让价款",)),
        ("patent.pledge.exists", (analysis.get("patent_pledge") or {}).get("exists"), ("质押登记", "专利权质押")),
        ("patent.pledge.pledgee", (analysis.get("patent_pledge") or {}).get("pledgee"), ("质权人",)),
        ("patent.pledge.registration_no", (analysis.get("patent_pledge") or {}).get("registration_no"), ("质押登记编号", "质押登记号")),
        ("patent.pledge.release_after_first_payment", (analysis.get("patent_pledge") or {}).get("release_after_first_payment"), ("第一期", "质押注销", "解除质押")),
        ("patent.pledge.pledgee_consent_required", (analysis.get("patent_pledge") or {}).get("pledgee_consent_required"), ("质权人同意", "书面同意")),
        ("patent.pledge.pledgee_consent_obtained", (analysis.get("patent_pledge") or {}).get("pledgee_consent_obtained"), ("已取得质权人同意", "质权人已书面同意")),
        ("patent.pledge.released", (analysis.get("patent_pledge") or {}).get("pledge_released"), ("质押已解除", "质押登记已注销")),
        ("patent.registration.feasibility_blocked", (analysis.get("patent_pledge") or {}).get("registration_feasibility_blocked"), ("尚未取得质权人", "解除质押或取得质权人")),
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
