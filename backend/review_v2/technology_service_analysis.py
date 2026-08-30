"""Deterministic classification and relationship analysis for technology contracts."""

from __future__ import annotations

import re
import hashlib
import inspect
from contextvars import ContextVar
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional


DATE_PATTERN = re.compile(r"(20\d{2})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日")
MONEY_PATTERN = r"([0-9][0-9,]*(?:\.\d+)?)\s*元"
TECHNOLOGY_CLASSIFIER_VERSION = "technical-transaction-classifier-v3-single-source"

_classification_session: ContextVar[Optional[Dict[str, Any]]] = ContextVar(
    "technology_classification_session",
    default=None,
)
_payment_analysis_session: ContextVar[Optional[Dict[str, Any]]] = ContextVar(
    "technology_payment_analysis_session",
    default=None,
)


def _classification_document_hash(text: str) -> str:
    normalized = re.sub(r"\s+", "", text or "")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def begin_technology_classification_session(text: str) -> None:
    """Start one request-scoped classification session.

    Every downstream consumer uses the first classification result for the same
    normalized document. Repeated classifier calls become observable cache hits
    instead of independent opportunities to overwrite the canonical subtype.
    """
    _classification_session.set({
        "classifier_version": TECHNOLOGY_CLASSIFIER_VERSION,
        "document_hash": _classification_document_hash(text),
        "cache_key": f"{TECHNOLOGY_CLASSIFIER_VERSION}:{_classification_document_hash(text)}",
        "invocation_count": 0,
        "actual_execution_count": 0,
        "cache_hit_count": 0,
        "calls": [],
        "result": None,
    })


def technology_classification_runtime_trace() -> Dict[str, Any]:
    state = _classification_session.get() or {}
    result = dict(state.get("result") or {})
    call_sites: Dict[tuple[str, str, int], Dict[str, Any]] = {}
    for call in state.get("calls") or []:
        key = (str(call.get("module") or ""), str(call.get("function") or ""), int(call.get("line") or 0))
        row = call_sites.setdefault(key, {
            "module": key[0],
            "function": key[1],
            "line": key[2],
            "invocation_count": 0,
            "cache_hit_count": 0,
        })
        row["invocation_count"] += 1
        row["cache_hit_count"] += int(bool(call.get("cache_hit")))
    return {
        "classifier_version": state.get("classifier_version", TECHNOLOGY_CLASSIFIER_VERSION),
        "document_hash": state.get("document_hash", ""),
        "cache_key": state.get("cache_key", ""),
        "invocation_count": int(state.get("invocation_count") or 0),
        "actual_execution_count": int(state.get("actual_execution_count") or 0),
        "cache_hit_count": int(state.get("cache_hit_count") or 0),
        "call_sites": list(call_sites.values()),
        "raw_classification": {
            "family": result.get("family"),
            "primary_subtype": result.get("primary_subtype"),
            "tertiary_subtype": result.get("tertiary_subtype"),
            "transaction_structure": result.get("transaction_structure"),
            "scenario": result.get("scenario"),
            "scenario_label": result.get("scenario_label"),
            "confidence": result.get("confidence"),
            "classification_score": result.get("classification_score"),
        },
    }


def end_technology_classification_session() -> Dict[str, Any]:
    trace = technology_classification_runtime_trace()
    _classification_session.set(None)
    return trace


def begin_payment_analysis_session(text: str) -> None:
    """Start request-scoped instrumentation for payment arithmetic analysis."""

    _payment_analysis_session.set({
        "document_hash": _classification_document_hash(text),
        "invocation_count": 0,
        "calls": [],
        "last_output": {},
    })


def payment_analysis_runtime_trace() -> Dict[str, Any]:
    state = _payment_analysis_session.get() or {}
    call_sites: Dict[tuple[str, str, int], Dict[str, Any]] = {}
    for call in state.get("calls") or []:
        key = (str(call.get("module") or ""), str(call.get("function") or ""), int(call.get("line") or 0))
        row = call_sites.setdefault(key, {
            "module": key[0],
            "function": key[1],
            "line": key[2],
            "invocation_count": 0,
        })
        row["invocation_count"] += 1
    return {
        "document_hash": str(state.get("document_hash") or ""),
        "invocation_count": int(state.get("invocation_count") or 0),
        "call_sites": list(call_sites.values()),
        "last_output": dict(state.get("last_output") or {}),
    }


def _decimal(value: str) -> Decimal:
    try:
        return Decimal(value.replace(",", ""))
    except (InvalidOperation, AttributeError):
        return Decimal("0")


def _number(value: Decimal) -> int | float:
    integral = value.to_integral_value()
    return int(integral) if value == integral else float(value)


def _iso(match: re.Match[str]) -> str:
    return date(int(match.group(1)), int(match.group(2)), int(match.group(3))).isoformat()


def analyze_primary_transaction(text: str) -> Dict[str, Any]:
    """Classify the exchanged legal/economic performance, not word frequency."""
    source = text or ""
    compact = re.sub(r"\s+", "", source)
    sentences = [row for row in re.split(r"[。；;\n]+", source) if row.strip()]
    operative_sentences = [row for row in sentences if not any(term in row for term in ("另行购买", "另行采购", "另行签署", "另行订立", "具体供货另行"))]
    operative = re.sub(r"\s+", "", "。".join(operative_sentences))

    license_grant = bool(re.search(
        r"(?:许可|授予)[^。；]{0,45}(?:技术|技术资料|制造工艺|源程序|软件|专利)[^。；]{0,45}(?:使用|实施|设计|制造|销售|出口)?|"
        r"(?:技术|技术资料|制造工艺|源程序|软件|专利)[^。；]{0,45}(?:许可|授予)[^。；]{0,30}(?:使用|实施)",
        operative,
    ))
    license_roles = (
        ("许可方" in compact and "被许可方" in compact)
        or ("出让方" in compact and "受让方" in compact and license_grant)
    )
    license_boundaries = {
        "license_mode": any(term in compact for term in ("非独占", "独占许可", "排他许可", "普通许可")),
        "non_transferable": any(term in compact for term in ("不可转让", "不得转让", "不得再许可")),
        "territory": any(term in compact for term in ("许可地域", "约定区域", "中华人民共和国境内", "地域范围")),
        "use_scope": bool(re.search(r"(?:有权|许可)[^。；]{0,80}(?:设计|制造|使用|销售|出口|实施)", operative)),
        "post_termination_use": any(term in compact for term in ("终止后继续使用", "合同终止后技术使用", "永久继续使用")),
    }
    license_scope_count = sum(bool(value) for value in license_boundaries.values())
    royalty = bool(
        any(term in compact for term in ("提成费", "销售提成", "royalty", "许可使用费"))
        or re.search(r"(?:净销售额|销售额)[^。；]{0,40}\d+(?:\.\d+)?%", compact, re.IGNORECASE)
    )
    entry_fee = any(term in compact for term in ("入门费", "技术许可费", "许可费总额", "基础技术许可"))
    technical_delivery = sum(
        term in compact for term in ("技术资料", "PLC源程序", "制造工艺", "故障诊断技术", "设计资料", "技术指导", "人员培训")
    ) >= 2
    independent_license_value = license_grant and (royalty or entry_fee or "许可使用费" in compact) and license_scope_count >= 1
    # A project-result ownership allocation (for example, “成果归甲方所有”)
    # is not itself a transaction transferring pre-existing technology.  Require
    # an operative disposal verb so service/development ownership clauses do not
    # get promoted to a technology-transfer primary transaction.
    technology_disposal = bool(re.search(
        r"(?:专利权|专利申请权|技术成果所有权)[^。；]{0,40}(?:转让给|转移至)|"
        r"(?:转让|让与)[^。；]{0,30}(?:专利权|专利申请权|技术成果所有权)",
        operative,
    ))
    technology_ownership_transfer = bool(
        technology_disposal
        and (
            any(term in compact[:300] for term in ("技术转让合同", "专利权转让合同", "专利申请权转让合同"))
            or ("让与方" in compact and "受让方" in compact)
            or any(term in compact for term in ("技术转让价款", "专利权转让价款", "专利申请权转让价款", "转让总价"))
            or any(term in compact for term in ("本合同转让的技术", "本合同转让的专利权", "转让标的"))
        )
    )

    ownership_transfer = bool(re.search(
        r"(?:货物|设备|产品)[^。；]{0,50}(?:所有权转移|所有权归|产权转移)|"
        r"(?:所有权|产权)[^。；]{0,35}(?:交付后|验收后)[^。；]{0,20}(?:转移|归买方|归买受人)",
        operative,
    ))
    goods_quantity_price = bool(re.search(
        r"\d+\s*(?:台|套|件|吨|批)[^。；]{0,80}(?:每台|每套|每件|单价|总价|货款)|"
        r"(?:每台|每套|每件|单价)[^。；]{0,40}(?:元|美元|USD|人民币)",
        operative,
        re.IGNORECASE,
    ))
    sale_roles = (
        ("出卖人" in operative and "买受人" in operative)
        or ("卖方" in operative and "买方" in operative)
        or ("供方" in operative and "需方" in operative)
    )
    goods_purchase = bool(re.search(
        r"(?:购买|采购)[^。；]{0,30}(?:货物|设备|产品|材料)|"
        r"(?:出售|销售|供应|交付)[^。；]{0,30}\d+\s*(?:台|套|件|吨|批)",
        operative,
    ))
    purchase_price = bool(re.search(
        r"(?:设备|货物|产品)[^。；]{0,60}(?:购买价款|采购价款|总价|货款|单价)|"
        r"(?:购买价款|采购价款|货款|单价)[^。；]{0,60}(?:设备|货物|产品|\d+\s*(?:台|套|件|吨|批))",
        operative,
    ))
    independent_sale_value = (ownership_transfer or goods_purchase) and (goods_quantity_price or purchase_price)
    ancillary_goods_supply = bool(
        re.search(r"(?:另行[^。；]{0,45}(?:购买|采购|供应)|(?:购买|采购|供应)[^。；]{0,45}另行)[^。；]{0,60}(?:零部件|原材料|标准件|备件)|"
                  r"(?:零部件|原材料|标准件|备件)[^。；]{0,80}另行[^。；]{0,30}(?:购买|采购|供应|签署)", compact)
        and any(term in compact for term in ("另行签署", "另行订立", "具体供货另行", "另行确定的价格"))
    )
    software_is_ancillary = bool(
        independent_sale_value
        and any(term in compact for term in ("设备配套软件", "设备使用所必需的软件", "仅为设备运行所需", "随设备许可"))
        and not (royalty or entry_fee or "独立许可费" in compact)
    )

    license_score = (
        10 * int(license_grant)
        + 4 * int(license_roles)
        + min(8, license_scope_count * 2)
        + 7 * int(royalty)
        + 5 * int(entry_fee)
        + 3 * int(technical_delivery)
    )
    sale_score = (
        10 * int(ownership_transfer)
        + 7 * int(goods_quantity_price)
        + 4 * int(sale_roles)
        + 4 * int(goods_purchase)
        + 5 * int(purchase_price)
    )
    if software_is_ancillary:
        independent_license_value = False
    if technology_ownership_transfer:
        transaction_type = "TECHNOLOGY_TRANSFER"
        dominant_family = "TECHNOLOGY"
        confidence = "high"
    elif independent_license_value and independent_sale_value:
        transaction_type = "MIXED_SALE_TECHNOLOGY_LICENSE"
        dominant_family = "TECHNOLOGY"
        confidence = "high"
    elif independent_license_value and license_score >= 16:
        transaction_type = "TECHNOLOGY_LICENSE"
        dominant_family = "TECHNOLOGY"
        confidence = "high"
    elif independent_sale_value and sale_score >= 14:
        transaction_type = "GOODS_SALE"
        dominant_family = "SALE"
        confidence = "high"
    else:
        transaction_type = "UNKNOWN"
        dominant_family = "UNKNOWN"
        confidence = "medium" if max(license_score, sale_score) >= 10 else "low"

    license_obligations = []
    if license_grant:
        license_obligations.append("grant technology use right")
    if technical_delivery:
        license_obligations.extend(["deliver technical materials", "provide technical assistance or training"])
    grantee_obligations = []
    if entry_fee:
        grantee_obligations.append("pay entry fee")
    if royalty:
        grantee_obligations.append("pay royalty")
    sale_obligations = ["deliver goods and transfer ownership"] if independent_sale_value else []
    sale_buyer_obligations = ["pay goods purchase price"] if independent_sale_value else []
    return {
        "type": transaction_type,
        "dominant_family": dominant_family,
        "confidence": confidence,
        "primary_subject": (
            "patent or technical-result ownership"
            if transaction_type == "TECHNOLOGY_TRANSFER"
            else "technology / know-how / technical materials" if transaction_type == "TECHNOLOGY_LICENSE"
            else "goods and technology license" if transaction_type.startswith("MIXED_")
            else "goods" if transaction_type == "GOODS_SALE" else "undetermined"
        ),
        "rights_change": (
            (["ownership of patent or technical result transfers"] if technology_ownership_transfer else [])
            + (["license to use technology"] if independent_license_value and not technology_ownership_transfer else [])
        ) + (["ownership of goods transfers to buyer"] if independent_sale_value else []),
        "primary_obligation_grantor": license_obligations + sale_obligations,
        "primary_obligation_grantee": grantee_obligations + sale_buyer_obligations,
        "primary_consideration": (
            (["entry fee"] if entry_fee else [])
            + (["sales royalty"] if royalty else [])
            + (["goods purchase price"] if independent_sale_value else [])
        ),
        "transaction_purpose": (
            "acquire ownership of patent or technical result"
            if technology_ownership_transfer
            else "use licensed technology to manufacture or operate products" if independent_license_value
            else "acquire ownership of goods" if independent_sale_value else "undetermined"
        ),
        "secondary_transactions": ["ANCILLARY_FUTURE_GOODS_SUPPLY"] if ancillary_goods_supply else [],
        "license_semantics": {
            "grant": license_grant,
            "roles": license_roles,
            "boundaries": license_boundaries,
            "entry_fee": entry_fee,
            "royalty": royalty,
            "technical_delivery": technical_delivery,
            "independent_economic_value": independent_license_value,
        },
        "technology_transfer_semantics": {"ownership_transfer": technology_ownership_transfer},
        "sale_semantics": {
            "ownership_transfer": ownership_transfer,
            "roles": sale_roles,
            "quantity_unit_price": goods_quantity_price,
            "goods_purchase_obligation": goods_purchase,
            "purchase_price": purchase_price,
            "independent_economic_value": independent_sale_value,
            "ancillary_future_supply": ancillary_goods_supply,
        },
        "family_scores": {"TECHNOLOGY": license_score, "SALE": sale_score},
        "decision_basis": "operative rights change + primary obligations + consideration + economic independence",
    }


def _classify_technology_transaction_uncached(text: str) -> Dict[str, Any]:
    source_text = text or ""
    compact = re.sub(r"\s+", "", source_text)
    primary_transaction_model = analyze_primary_transaction(source_text)
    source_lines = [line.strip() for line in source_text.splitlines() if line.strip()]
    document_title = source_lines[0] if source_lines else ""
    title_compact = re.sub(r"\s+", "", document_title)
    service_signals = (
        "技术服务合同",
        "解决特定技术问题",
        "技术服务内容",
        "技术服务费用",
        "提供技术服务",
    )
    cooperative_signals = ("合作开发", "共同研发", "共同研究开发", "共同投资")
    entrusted_signals = ("委托开发合同", "委托研究开发", "研究开发人")
    transfer_signals = (
        "技术转让合同", "技术转让（专利权）合同", "技术转让(专利权)合同",
        "专利权转让", "转让技术成果所有权", "让与人", "让与方", "受让方",
    )
    license_signals = ("技术许可合同", "被许可人", "许可使用专利", "许可使用技术秘密")
    consulting_signals = ("技术咨询合同", "技术咨询报告", "咨询意见")

    heading = compact[:600]
    scores = {
        "COOPERATIVE_DEVELOPMENT": 0,
        "ENTRUSTED_DEVELOPMENT": 0,
        "TECHNOLOGY_TRANSFER": 0,
        "TECHNOLOGY_LICENSE": 0,
        "TECHNICAL_CONSULTING": 0,
        "TECHNICAL_SERVICE": 0,
    }
    evidence: Dict[str, List[str]] = {key: [] for key in scores}

    def add(subtype_name: str, weight: int, reason: str, present: bool) -> None:
        if present:
            scores[subtype_name] += weight
            evidence[subtype_name].append(reason)

    patent_transfer_title = (
        "合同" in title_compact
        and any(term in title_compact for term in ("专利权转让", "技术转让（专利权）", "技术转让(专利权)"))
    )
    technology_transfer_title = "合同" in title_compact and "技术转让" in title_compact
    patent_license_title = (
        "合同" in title_compact
        and any(term in title_compact for term in ("专利实施许可", "技术许可（专利实施）", "技术许可(专利实施)"))
    )
    technology_license_title = "合同" in title_compact and "技术许可" in title_compact
    consulting_title = "合同" in title_compact and "技术咨询" in title_compact
    service_title = "合同" in title_compact and "技术服务" in title_compact

    patent_license_grant = bool(re.search(
        r"(?:许可人|卖方|乙方).{0,60}(?:许可|授予).{0,80}(?:被许可人|买方|甲方).{0,80}(?:实施|使用).{0,30}专利"
        r"|(?:许可|授予).{0,50}(?:专利实施许可|实施其所拥有的.{0,40}专利)",
        compact,
    ))
    license_consideration = any(term in compact for term in (
        "专利许可费", "实施许可使用费", "许可使用费", "许可费总额", "许可使用费总额",
    ))
    license_scope = any(term in compact for term in (
        "排他许可", "独占许可", "普通许可", "许可范围", "许可期限", "许可地域", "再许可",
    ))
    patent_ownership_transfer = bool(re.search(
        r"(?:转让|让与).{0,30}(?:专利权|专利申请权)|(?:专利权|专利申请权).{0,30}(?:转让|让与|转移至|归受让方所有)",
        compact,
    ))
    transfer_registration = bool(re.search(
        r"(?:专利权.{0,30}(?:转让登记|变更登记|登记至受让方|登记转移)|(?:申请人|专利申请权).{0,30}(?:变更登记|变更))",
        compact,
    ))
    transfer_consideration = any(term in compact for term in (
        "专利权转让价款", "专利权转让总价", "专利权转让费", "技术转让价款", "转让总价",
    ))
    granted_patent_asset = (
        "专利权" in compact
        and any(term in compact for term in ("已取得授权", "当前专利权人", "授权日", "授权公告号"))
    )
    patent_application_asset = any(term in compact for term in (
        "专利申请权", "尚未授权", "当前申请人", "专利申请人",
    ))
    if patent_application_asset and "转让价款" in compact:
        transfer_consideration = True

    add("TECHNOLOGY_TRANSFER", 12, "title:patent_right_transfer", patent_transfer_title)
    add("TECHNOLOGY_TRANSFER", 8, "title:technology_transfer", technology_transfer_title and not patent_transfer_title)
    add("TECHNOLOGY_TRANSFER", 8, "roles:transferee_transferor", "受让方" in compact and ("让与方" in compact or "让与人" in compact))
    add("TECHNOLOGY_TRANSFER", 6, "effect:registration_transfers_patent_right", bool(re.search(r"专利权.{0,18}登记.{0,12}(?:转移|转让)", compact)))
    add("TECHNOLOGY_TRANSFER", 5, "consideration:transfer_price", "专利权转让价款" in compact)
    add("TECHNOLOGY_TRANSFER", 3, "transfer_terms", any(signal in compact for signal in transfer_signals))
    add("TECHNOLOGY_TRANSFER", 10, "core_obligation:patent_ownership_transfer", patent_ownership_transfer and (transfer_registration or transfer_consideration))

    add("TECHNICAL_SERVICE", 12, "title:technical_service", service_title)
    add("TECHNICAL_SERVICE", 6, "service_obligation", any(signal in compact for signal in service_signals[1:]))
    # Titles are supporting signals only. Development mode is resolved primarily
    # from who funds and performs the research and who owns its outcome/risk.
    party_a_invests = bool(re.search(r"甲方(?:(?!乙方).){0,500}(?:计划投入|投入研发|研发人员|研发费用|研发资源)", compact))
    party_b_invests = bool(re.search(r"乙方(?:(?!甲方).){0,500}(?:计划投入|投入研发|研发人员|研发费用|研发资源)", compact))
    party_a_develops = bool(re.search(r"甲方(?:(?!乙方).){0,120}(?:主要负责|负责).{0,100}(?:开发|研发|架构|模块|算法)", compact))
    party_b_develops = bool(re.search(r"乙方(?:(?!甲方).){0,120}(?:主要负责|负责).{0,100}(?:开发|研发|模块|接口|系统)", compact))
    joint_work = any(term in compact for term in (
        "双方共同参与项目研发", "双方共同开发", "共同研究开发", "共同研发",
        "共同进行系统集成", "共同组织验收", "相互提供技术协作",
    ))
    joint_results = any(term in compact for term in (
        "共同开发成果", "共同形成的", "共同享有开发成果", "共同享有",
        "各享有50%的权利", "共同著作权人",
    ))
    joint_risk = any(term in compact for term in (
        "双方各自承担自己已经发生的研发费用", "共同承担开发风险", "各自承担研发费用",
        "正常技术风险", "共同承担项目责任",
    ))
    directed_commission = bool(re.search(
        r"(?:甲方|委托方|委托人).{0,30}(?:委托|提出研发需求).{0,30}(?:乙方|受托方|研究开发人).{0,30}(?:开发|研究开发|研发)",
        compact,
    )) or any(term in compact for term in ("委托乙方研究开发", "甲方委托乙方", "委托研究开发"))
    one_party_funds = bool(re.search(
        r"(?:甲方|委托方|被许可方).{0,80}(?:支付|承担).{0,30}(?:研究开发经费|研发费用|开发费)",
        compact,
    ))
    one_party_develops = bool(re.search(
        r"(?:乙方|受托方|研究开发人|许可方).{0,80}(?:负责|承担).{0,30}(?:研究开发|研发|开发工作)",
        compact,
    ))

    add("COOPERATIVE_DEVELOPMENT", 3, "title:cooperative_development", "合作开发" in heading)
    add("COOPERATIVE_DEVELOPMENT", 6, "bilateral_research_investment", party_a_invests and party_b_invests)
    add("COOPERATIVE_DEVELOPMENT", 8, "bilateral_research_tasks", party_a_develops and party_b_develops)
    add("COOPERATIVE_DEVELOPMENT", 5, "joint_research_and_coordination", joint_work)
    add("COOPERATIVE_DEVELOPMENT", 4, "joint_development_results", joint_results)
    add("COOPERATIVE_DEVELOPMENT", 3, "joint_development_risk", joint_risk)
    add("COOPERATIVE_DEVELOPMENT", 2, "cooperative_wording", any(signal in compact for signal in cooperative_signals))
    add("ENTRUSTED_DEVELOPMENT", 4, "title:entrusted_development", "委托开发" in heading)
    add("ENTRUSTED_DEVELOPMENT", 8, "directed_research_commission", directed_commission)
    add("ENTRUSTED_DEVELOPMENT", 6, "asymmetric_development_funding", one_party_funds and not (party_a_invests and party_b_invests))
    add("ENTRUSTED_DEVELOPMENT", 6, "asymmetric_research_performance", one_party_develops and not (party_a_develops and party_b_develops))
    add("ENTRUSTED_DEVELOPMENT", 2, "entrusted_wording", any(signal in compact for signal in entrusted_signals))
    add("TECHNOLOGY_LICENSE", 16, "title:patent_license", patent_license_title)
    add("TECHNOLOGY_LICENSE", 12, "title:technology_license", technology_license_title and not patent_license_title)
    add(
        "TECHNOLOGY_LICENSE",
        6,
        "current_license_transaction",
        "许可方" in compact
        and "被许可方" in compact
        and any(term in compact for term in ("许可方式", "许可范围", "许可期限", "授予", "专利许可费")),
    )
    add("TECHNOLOGY_LICENSE", 12, "core_obligation:patent_license_grant", patent_license_grant and (license_consideration or license_scope))
    add(
        "TECHNOLOGY_LICENSE",
        18,
        "primary_transaction:technology_license",
        primary_transaction_model["type"] in {"TECHNOLOGY_LICENSE", "MIXED_SALE_TECHNOLOGY_LICENSE"},
    )
    add("TECHNICAL_CONSULTING", 12, "title:technical_consulting", consulting_title)
    add("TECHNICAL_CONSULTING", 5, "consulting_obligation", any(signal in compact for signal in consulting_signals))
    consulting_analysis_terms = (
        "可行性分析", "可行性论证", "技术分析", "技术论证", "分析评价",
        "技术评价", "技术预测", "架构评估", "技术风险分析", "提出技术建议",
    )
    consulting_deliverable = bool(re.search(
        r"(?:提交|出具|形成|提供).{0,24}(?:技术)?(?:咨询|分析|论证|评价|可行性).{0,12}(?:报告|意见|建议|方案)",
        compact,
    )) or any(term in compact for term in ("技术咨询报告", "咨询报告验收", "书面咨询报告"))
    consulting_parties = (
        "委托方" in compact
        and any(term in compact for term in ("咨询方", "受托方"))
        and any(term in compact for term in ("技术咨询", "咨询事项", "咨询项目", "咨询报告"))
    )
    consulting_analysis = sum(term in compact for term in consulting_analysis_terms) >= 2
    consulting_consideration = any(term in compact for term in (
        "技术咨询报酬", "咨询报酬", "咨询费用", "咨询服务费",
    ))
    implementation_disclaimer = any(term in compact for term in (
        "不承担软件开发", "不承担技术实施", "不承担成果制造", "仅提供咨询意见",
    ))
    add("TECHNICAL_CONSULTING", 4, "roles:consulting_client_and_consultant", consulting_parties)
    add("TECHNICAL_CONSULTING", 5, "core_obligation:analysis_evaluation_advice", consulting_analysis)
    add("TECHNICAL_CONSULTING", 5, "deliverable:consulting_report_or_opinion", consulting_deliverable)
    add("TECHNICAL_CONSULTING", 3, "consideration:consulting_fee", consulting_consideration)
    add("TECHNICAL_CONSULTING", 2, "boundary:no_direct_implementation", implementation_disclaimer)

    explicit_title_subtype = (
        "TECHNOLOGY_TRANSFER" if technology_transfer_title or patent_transfer_title
        else "TECHNOLOGY_LICENSE" if technology_license_title or patent_license_title
        else "TECHNICAL_CONSULTING" if consulting_title
        else "TECHNICAL_SERVICE" if service_title
        else "COOPERATIVE_DEVELOPMENT" if "合作开发" in title_compact
        else "ENTRUSTED_DEVELOPMENT" if "委托开发" in title_compact
        else ""
    )
    ranked = sorted(scores, key=lambda key: scores[key], reverse=True)
    if patent_ownership_transfer or primary_transaction_model["type"] == "TECHNOLOGY_TRANSFER":
        subtype = "TECHNOLOGY_TRANSFER"
    elif primary_transaction_model["type"] in {"TECHNOLOGY_LICENSE", "MIXED_SALE_TECHNOLOGY_LICENSE"}:
        subtype = "TECHNOLOGY_LICENSE"
    elif primary_transaction_model["type"] == "GOODS_SALE":
        subtype = "GENERAL_TECHNOLOGY"
    else:
        subtype = explicit_title_subtype or (ranked[0] if scores[ranked[0]] >= 6 else "GENERAL_TECHNOLOGY")
    tertiary_subtype = (
        "MIXED_PATENT_RIGHT_AND_APPLICATION_TRANSFER"
        if subtype == "TECHNOLOGY_TRANSFER" and granted_patent_asset and patent_application_asset
        else "PATENT_APPLICATION_RIGHT_TRANSFER"
        if subtype == "TECHNOLOGY_TRANSFER" and patent_application_asset
        else "PATENT_RIGHT_TRANSFER"
        if subtype == "TECHNOLOGY_TRANSFER" and (granted_patent_asset or "专利权" in compact)
        else "PATENT_LICENSE"
        if subtype == "TECHNOLOGY_LICENSE" and patent_license_grant
        else "TECHNICAL_SECRET_LICENSE"
        if subtype == "TECHNOLOGY_LICENSE" and primary_transaction_model["license_semantics"]["technical_delivery"]
        else ""
    )

    commissioned_development_evidence: List[str] = []
    commissioned_checks = (
        ("development_fee", any(term in compact for term in ("后续技术开发费", "研究开发经费", "开发费用"))),
        ("developer_and_funder", bool(re.search(r"(?:开发费用|开发费).{0,30}(?:被许可方|委托方).{0,16}(?:承担|支付)", compact)) and bool(re.search(r"(?:许可方|受托方|研究开发人).{0,16}(?:负责|承担).{0,12}(?:具体)?(?:研究开发|研发)", compact))),
        ("development_objectives", any(term in compact for term in ("研究开发目标", "研发目标", "技术指标", "开发成果的内容"))),
        ("development_schedule", any(term in compact for term in ("研究开发计划", "开发期限", "开发进度", "阶段成果"))),
        ("development_results", "开发成果" in compact and any(term in compact for term in ("成果归属", "专利申请权", "软件著作权", "源代码"))),
        ("development_acceptance", any(term in compact for term in ("开发的验收标准", "开发成果通过验收", "项目验收"))),
    )
    for reason, present in commissioned_checks:
        if present:
            commissioned_development_evidence.append(reason)
    has_commissioned_development = len(commissioned_development_evidence) >= 3 and "开发" in compact

    cooperative_development_evidence: List[str] = []
    if joint_work:
        cooperative_development_evidence.append("joint_research")
    if party_a_invests and party_b_invests:
        cooperative_development_evidence.append("bilateral_research_investment")
    if party_a_develops and party_b_develops:
        cooperative_development_evidence.append("bilateral_research_tasks")
    if joint_results:
        cooperative_development_evidence.append("joint_development_results")
    if joint_risk:
        cooperative_development_evidence.append("joint_development_risk")
    has_cooperative_development = (
        len(cooperative_development_evidence) >= 3
        and "bilateral_research_tasks" in cooperative_development_evidence
    )

    secondary_modules: List[str] = []
    module_evidence: Dict[str, List[str]] = {}
    if has_commissioned_development and subtype != "ENTRUSTED_DEVELOPMENT":
        secondary_modules.append("COMMISSIONED_DEVELOPMENT")
        module_evidence["COMMISSIONED_DEVELOPMENT"] = commissioned_development_evidence
    if has_cooperative_development and subtype != "COOPERATIVE_DEVELOPMENT":
        secondary_modules.append("COOPERATIVE_DEVELOPMENT")
        module_evidence["COOPERATIVE_DEVELOPMENT"] = cooperative_development_evidence
    subtransaction_analysis = analyze_technology_subtransactions(text)
    structured_subfacts = dict(subtransaction_analysis.get("structured_facts") or {})
    if (
        subtype != "TECHNICAL_SERVICE"
        and (structured_subfacts.get("technical_service") or {}).get("content")
    ):
        secondary_modules.append("TECHNICAL_SERVICE")
        module_evidence["TECHNICAL_SERVICE"] = list(
            (structured_subfacts.get("technical_service") or {}).get("activities") or []
        )

    ancillary_obligations: List[str] = []
    ancillary_terms = {
        "TRAINING": ("培训", "人员培训"),
        "INSTALLATION_AND_COMMISSIONING": ("安装调试", "安装和调试", "系统安装和调试"),
        "TECHNICAL_GUIDANCE": ("现场技术指导", "技术指导"),
        "TECHNICAL_SUPPORT": ("技术支持", "咨询支持", "提供技术咨询"),
    }
    for obligation, terms in ancillary_terms.items():
        if any(term in compact for term in terms):
            ancillary_obligations.append(obligation)
    if subtype != "TECHNICAL_SERVICE" and any(term in compact for term in (
        "技术服务内容", "现场技术交底", "技术答疑", "调试指导",
    )):
        ancillary_obligations.append("TECHNICAL_SERVICE")
    ancillary_obligations = list(dict.fromkeys(ancillary_obligations))

    transitional_arrangements: List[str] = []
    if subtype == "TECHNOLOGY_TRANSFER" and (
        any(term in compact for term in ("过渡期许可", "过渡期实施许可"))
        or bool(re.search(r"(?:合同生效|签署).{0,50}(?:转让登记完成|专利权转移).{0,50}(?:普通实施许可|实施许可)", compact))
    ):
        transitional_arrangements.append("TEMPORARY_PATENT_LICENSE")

    factual_triggers: List[str] = []
    fact_terms = {
        "CONFIDENTIAL_INFORMATION": ("保密义务", "技术秘密", "保密信息"),
        "FOLLOW_ON_IMPROVEMENTS": ("后续改进", "改进技术", "后续开发"),
        "THIRD_PARTY_IP_RISK": ("第三方主张", "侵犯其知识产权", "第三方侵权"),
        "DEVELOPMENT_RESULTS": ("开发成果", "源代码", "专利申请权"),
    }
    for trigger, terms in fact_terms.items():
        if any(term in compact for term in terms):
            factual_triggers.append(trigger)
    if bool(re.search(r"(?:课题组|实验室|研究中心)(?:以|作为).{0,16}(?:签约方|合同主体|名义签订)", compact)):
        factual_triggers.append("RESEARCH_ORGANIZATION_AUTHORITY_RISK")
    if any(term in compact for term in ("冒充研发", "现有技术重复收费", "以现有技术作为新研发成果")):
        factual_triggers.append("EXISTING_TECHNOLOGY_AS_DEVELOPMENT_RISK")

    active_transaction_types = {subtype}
    active_transaction_types.update(
        "ENTRUSTED_DEVELOPMENT" if module == "COMMISSIONED_DEVELOPMENT" else module
        for module in secondary_modules
    )
    excluded_subtypes = [key for key in scores if key not in active_transaction_types]

    primary_contract_type = {
        ("TECHNOLOGY_TRANSFER", "PATENT_RIGHT_TRANSFER"): "technology_transfer_patent",
        ("TECHNOLOGY_TRANSFER", "PATENT_APPLICATION_RIGHT_TRANSFER"): "technology_transfer_patent_application_right",
        ("TECHNOLOGY_TRANSFER", "MIXED_PATENT_RIGHT_AND_APPLICATION_TRANSFER"): "technology_transfer_mixed_patent_assets",
        ("TECHNOLOGY_TRANSFER", ""): "technology_transfer_technical_secret" if "技术秘密" in compact else "technology_transfer",
        ("TECHNOLOGY_LICENSE", "PATENT_LICENSE"): "technology_license_patent",
        ("TECHNOLOGY_LICENSE", "TECHNICAL_SECRET_LICENSE"): "technology_license_technical_secret",
        ("TECHNOLOGY_LICENSE", ""): "technology_license_technical_secret" if "技术秘密" in compact else "technology_license",
        ("ENTRUSTED_DEVELOPMENT", ""): "commissioned_development",
        ("COOPERATIVE_DEVELOPMENT", ""): "cooperative_development",
        ("TECHNICAL_CONSULTING", ""): "technology_consulting",
        ("TECHNICAL_SERVICE", ""): "technology_service",
    }.get((subtype, tertiary_subtype), "general_technology")
    secondary_contract_types = [
        "commissioned_development" if module == "COMMISSIONED_DEVELOPMENT"
        else "cooperative_development" if module == "COOPERATIVE_DEVELOPMENT"
        else module.lower()
        for module in secondary_modules
    ]
    if primary_transaction_model["type"] == "MIXED_SALE_TECHNOLOGY_LICENSE":
        secondary_contract_types.append("goods_sale")
    secondary_contract_types.extend(
        value.lower() for value in primary_transaction_model.get("secondary_transactions") or []
        if value.lower() not in secondary_contract_types
    )

    title_transaction_type = explicit_title_subtype
    operative_transaction_type = (
        "TECHNOLOGY_TRANSFER" if patent_ownership_transfer and (transfer_registration or transfer_consideration)
        else "TECHNOLOGY_LICENSE" if (
            patent_license_grant and (license_consideration or license_scope)
            or primary_transaction_model["type"] in {"TECHNOLOGY_LICENSE", "MIXED_SALE_TECHNOLOGY_LICENSE"}
        )
        else ""
    )
    contract_type_conflict = bool(
        title_transaction_type
        and operative_transaction_type
        and title_transaction_type != operative_transaction_type
    )

    def snippets(terms: tuple[str, ...], limit: int = 4) -> List[str]:
        return [line[:240] for line in source_lines if any(term in line for term in terms)][:limit]

    classification_evidence_details = {
        "contract_title": document_title,
        "subject_matter": snippets(("专利名称", "项目名称", "合同标的", "许可实施的专利权", "转让的专利权")),
        "core_performance_obligations": snippets(("许可买方实施", "授予本专利实施许可", "转让给受让方", "转移至受让方", "共同研究开发", "委托研究开发", "解决特定技术问题", "可行性分析", "技术论证", "分析评价", "技术咨询报告")),
        "rights_transfer_method": snippets(("排他许可", "独占许可", "普通许可", "专利权转让", "转让登记", "变更登记")),
        "consideration_nature": snippets(("许可使用费", "实施许可使用费", "专利权转让价款", "技术服务费用", "研发费用", "咨询报酬")),
        "key_clauses": snippets(("许可范围", "许可期限", "专利权登记", "权利瑕疵", "开发成果", "咨询报告", "咨询内容", "咨询要求", "技术服务内容"), 8),
    }

    personal_information_analysis = _personal_information_processing_analysis(text)
    university_data = any(term in compact for term in ("高校", "大学", "科研数据", "科研项目", "科研管理数据"))
    transaction_structure = (
        "B2B_PATENT_LICENSE_WITH_COMMISSIONED_DEVELOPMENT"
        if tertiary_subtype == "PATENT_LICENSE" and "COMMISSIONED_DEVELOPMENT" in secondary_modules
        else "B2B_PATENT_LICENSE"
        if tertiary_subtype == "PATENT_LICENSE"
        else "MIXED_SALE_TECHNOLOGY_LICENSE"
        if primary_transaction_model["type"] == "MIXED_SALE_TECHNOLOGY_LICENSE"
        else "B2B_TECHNOLOGY_LICENSE"
        if subtype == "TECHNOLOGY_LICENSE"
        else "B2B_TECHNICAL_SERVICE"
        if subtype == "TECHNICAL_SERVICE"
        else "B2B_PATENT_RIGHT_TRANSFER"
        if tertiary_subtype == "PATENT_RIGHT_TRANSFER"
        else "B2B_PATENT_APPLICATION_RIGHT_TRANSFER"
        if tertiary_subtype == "PATENT_APPLICATION_RIGHT_TRANSFER"
        else "B2B_MIXED_PATENT_TRANSFER"
        if tertiary_subtype == "MIXED_PATENT_RIGHT_AND_APPLICATION_TRANSFER"
        else "B2B_COOPERATIVE_DEVELOPMENT"
        if subtype == "COOPERATIVE_DEVELOPMENT"
        else "B2B_ENTRUSTED_DEVELOPMENT"
        if subtype == "ENTRUSTED_DEVELOPMENT"
        else "B2B_TECHNICAL_CONSULTING"
        if subtype == "TECHNICAL_CONSULTING"
        else "B2B_TECHNOLOGY"
    )
    scenario = (
        "PATENT_LICENSE_WITH_COMMISSIONED_DEVELOPMENT"
        if tertiary_subtype == "PATENT_LICENSE" and "COMMISSIONED_DEVELOPMENT" in secondary_modules
        else "PATENT_LICENSE"
        if tertiary_subtype == "PATENT_LICENSE"
        else "UNIVERSITY_RESEARCH_DATA_GOVERNANCE_TECHNICAL_SERVICE"
        if subtype == "TECHNICAL_SERVICE" and university_data
        else "UNIVERSITY_TECH_ACHIEVEMENT_AGREEMENT_TRANSFER"
        if tertiary_subtype == "PATENT_RIGHT_TRANSFER" and university_data and "协议定价" in compact
        else "TECHNOLOGY_LICENSE"
        if subtype == "TECHNOLOGY_LICENSE"
        else "TECHNICAL_SERVICE"
        if subtype == "TECHNICAL_SERVICE"
        else "TECHNICAL_CONSULTING"
        if subtype == "TECHNICAL_CONSULTING"
        else subtype
    )
    scenario_label = (
        "专利实施许可（含委托开发模块）"
        if scenario == "PATENT_LICENSE_WITH_COMMISSIONED_DEVELOPMENT"
        else "专利实施许可"
        if scenario == "PATENT_LICENSE"
        else "高校科研数据治理技术服务"
        if subtype == "TECHNICAL_SERVICE" and university_data
        else "高校科技成果向企业协议转让"
        if tertiary_subtype == "PATENT_RIGHT_TRANSFER" and university_data and "协议定价" in compact
        else "技术许可"
        if subtype == "TECHNOLOGY_LICENSE"
        else "技术服务"
        if subtype == "TECHNICAL_SERVICE"
        else "技术咨询"
        if subtype == "TECHNICAL_CONSULTING"
        else "专利权转让"
        if tertiary_subtype == "PATENT_RIGHT_TRANSFER"
        else "专利申请权转让"
        if tertiary_subtype == "PATENT_APPLICATION_RIGHT_TRANSFER"
        else "专利权及专利申请权转让"
        if tertiary_subtype == "MIXED_PATENT_RIGHT_AND_APPLICATION_TRANSFER"
        else "合作开发"
        if subtype == "COOPERATIVE_DEVELOPMENT"
        else "委托开发"
        if subtype == "ENTRUSTED_DEVELOPMENT"
        else "技术合同"
    )
    return {
        "family": "TECHNOLOGY",
        "primary_category": "TECHNICAL_CONTRACT",
        "primary_subtype": subtype,
        "tertiary_subtype": tertiary_subtype,
        "confidence": "high" if scores.get(subtype, 0) >= 12 else "medium" if scores.get(subtype, 0) >= 6 else "low",
        "classification_score": scores.get(subtype, 0),
        "evidence_node_ids": evidence.get(subtype, []),
        "classification_evidence": cooperative_development_evidence if subtype == "COOPERATIVE_DEVELOPMENT" else commissioned_development_evidence if subtype == "ENTRUSTED_DEVELOPMENT" else evidence.get(subtype, []),
        "classification_evidence_details": classification_evidence_details,
        "primary_contract_type": primary_contract_type,
        "secondary_contract_types": secondary_contract_types,
        "primary_transaction": {
            "type": (
                "technology_transfer" if subtype == "TECHNOLOGY_TRANSFER"
                else "mixed_sale_technology_license" if primary_transaction_model["type"] == "MIXED_SALE_TECHNOLOGY_LICENSE"
                else primary_contract_type
            ),
            "subtype": tertiary_subtype.lower() if tertiary_subtype else subtype.lower(),
        },
        "primary_transaction_model": primary_transaction_model,
        "secondary_transactions": list(secondary_contract_types),
        "sub_transactions": list(subtransaction_analysis.get("sub_transactions") or []),
        "structured_facts": structured_subfacts,
        "fact_registry": build_technology_fact_registry(text),
        "active_transaction_types": sorted(active_transaction_types),
        "title_transaction_type": title_transaction_type,
        "operative_transaction_type": operative_transaction_type,
        "contract_type_conflict": {
            "exists": contract_type_conflict,
            "title_transaction_type": title_transaction_type,
            "operative_transaction_type": operative_transaction_type,
            "resolution": "PRIMARY_TITLE_WITH_CONFLICT_FINDING" if contract_type_conflict else "NO_CONFLICT",
            "reason": (
                "合同标题与核心权利处分条款指向不同交易性质，应单独提示合同性质冲突，但不得同时激活两套规则。"
                if contract_type_conflict else "合同标题与核心给付义务不存在实质类型冲突。"
            ),
        },
        "excluded_subtypes": excluded_subtypes,
        "candidate_scores": scores,
        "subtype": subtype,
        "development_mode": subtype if subtype in {"COOPERATIVE_DEVELOPMENT", "ENTRUSTED_DEVELOPMENT"} else "",
        "is_technical_service": subtype == "TECHNICAL_SERVICE",
        "transaction_structure": transaction_structure,
        "scenario": scenario,
        "scenario_label": scenario_label,
        "current_transaction": subtype,
        "secondary_modules": secondary_modules,
        "transaction_module_evidence": module_evidence,
        "ancillary_obligations": ancillary_obligations,
        "transitional_arrangements": transitional_arrangements,
        "factual_triggers": factual_triggers,
        "license_mode": "EXCLUSIVE" if any(term in compact for term in ("排他实施许可", "排他许可")) else "SOLE" if any(term in compact for term in ("独占实施许可", "独占许可")) else "NON_EXCLUSIVE" if any(term in compact for term in ("普通实施许可", "非独占许可", "非独占、不可转让许可")) else "",
        "referenced_contracts": [{"reference_type": "EXISTING_PATENT_LICENSE", "is_current_transaction": False}] if subtype == "TECHNOLOGY_TRANSFER" and any(term in compact for term in ("原专利实施许可合同", "普通实施许可")) else [],
        "involves_personal_information": bool(personal_information_analysis["triggered"]),
        "involves_background_ip": any(term in compact for term in ("已有", "既有", "通用算法库", "规则引擎", "内部技术工具", "背景知识产权")),
        "involves_software_or_data": (
            any(term in compact for term in (
                "软件系统", "软件交付", "软件著作权", "源代码", "开源软件", "开源组件",
                "程序脚本", "验证脚本", "算法库", "代码仓库",
            ))
            or (
                any(term in compact for term in ("数据处理", "数据治理"))
                and any(term in compact for term in ("数据交付", "委托处理", "数据接口", "数据集", "业务数据", "科研数据"))
            )
        ),
    }


def analyze_technology_subtransactions(text: str) -> Dict[str, Any]:
    """Extract ancillary performance modules without changing the main transaction."""
    compact = re.sub(r"\s+", "", text or "")
    technical_secret_scope = bool(
        re.search(r"(?:第[一二三四五六七八九十\d]+条)?技术秘密", compact)
        and sum(term in compact for term in (
            "未公开", "算法参数", "训练方法", "调优经验", "部署参数", "测试数据",
            "模型训练参数", "数据标注规范", "模型部署优化参数", "图像预处理方法",
        )) >= 2
    )
    technical_secret_use = bool(re.search(
        r"(?:技术秘密).{0,180}(?:仅可|只能|限于).{0,40}(?:实施|生产|合同目的)|"
        r"(?:仅可|只能|限于).{0,40}(?:使用).{0,30}(?:技术秘密)|"
        r"(?:技术秘密).{0,320}实施要求[：:]?(?:仅可|只能|仅限|限于).{0,90}(?:实施|许可专利|合同目的)",
        compact,
    ))
    technical_secret_fee = bool(re.search(r"技术秘密(?:使用费|许可费)[：:]?(?:人民币)?[\d,]+(?:\.\d+)?(?:万|亿)?元", compact))

    service_heading = bool(re.search(
        r"(?:第[一二三四五六七八九十\d]+条)?技术服务(?:和|及|与)?(?:技术)?(?:指导|培训)|"
        r"技术服务[：:](?:需要|包含|提供)",
        compact,
    ))
    service_activities = [
        term for term in (
            "实施说明", "部署指导", "参数配置培训", "故障排查指导", "部署支持",
            "现场技术指导", "技术培训", "安装调试支持", "技术咨询",
            "系统部署", "模型训练", "生产环境调试", "技术人员培训", "远程技术支持",
        ) if term in compact
    ]
    service_content = bool(service_heading and len(service_activities) >= 2)
    service_fee = bool(re.search(r"技术服务(?:和|及|与)?(?:技术)?(?:指导|培训)?费(?:用)?[：:]?(?:人民币)?[\d,]+(?:\.\d+)?(?:万|亿)?元", compact))
    service_fee_included = bool(re.search(
        r"技术服务(?:和|及|与)?(?:技术)?(?:指导|培训)?费(?:用)?.{0,24}(?:已)?包含在.{0,12}(?:转让费|许可费|合同价款|总价).{0,12}(?:不另行收费|不另收费)?",
        compact,
    ))
    technical_guidance = bool(
        any(term in compact for term in (
            "技术指导", "部署指导", "现场培训", "参数配置培训", "安装调试支持",
        ))
        or (service_heading and "指导" in compact)
    )
    acceptance = bool(
        (
            re.search(r"(?:第[一二三四五六七八九十\d]+条)?验收标准", compact)
            or sum(term in compact for term in (
                "书面确认", "准确率", "连续运行", "重大功能故障", "最终验收", "验收合格",
            )) >= 2
        )
        and sum(term in compact for term in (
            "书面确认", "准确率", "稳定运行", "连续运行", "重大功能故障",
            "首次验收", "重新验收", "再次验收", "验收不合格", "补救期限", "整改", "验收合格",
        )) >= 2
    )
    remedy_deadline = bool(re.search(
        r"(?:补救|整改|改正|修复)期限[：:]?(?:不超过)?\d+(?:个)?(?:工作日|日|天)",
        compact,
    ))
    reinspection_procedure = any(term in compact for term in ("再次验收", "重新验收", "复验"))
    reinspection_count_match = re.search(
        r"(?:再次|重新|复)验收次数[：:]?([一二三四五六七八九十\d]+)次",
        compact,
    )
    reinspection_count = reinspection_count_match.group(1) if reinspection_count_match else ""
    final_failure_scope_match = re.search(
        r"(?:第[二三四五六七八九十\d]+次|再次|重新|复验).{0,24}(?:仍|再次)?不合格.{0,160}",
        compact,
    )
    final_failure_scope = final_failure_scope_match.group(0) if final_failure_scope_match else ""
    final_failure_remedy = bool(
        final_failure_scope
        and any(term in final_failure_scope for term in ("解除合同", "终止合同", "拒绝接受"))
    )
    refund_remedy = bool(
        final_failure_scope
        and any(term in final_failure_scope for term in ("返还已支付", "退还已支付", "退款", "返还转让费", "返还价款"))
    )
    damage_remedy = bool(final_failure_scope and any(term in final_failure_scope for term in ("赔偿损失", "损失赔偿")))
    material_delivery = bool(
        "技术资料" in compact
        and any(term in compact for term in ("提交时间", "交付时间", "提交方式", "交付方式", "交付确认单"))
    )

    sub_transactions: List[str] = []
    if technical_secret_scope and (technical_secret_use or technical_secret_fee):
        sub_transactions.append("technical_secret")
    if service_content:
        sub_transactions.append("technical_service")
    if technical_guidance:
        sub_transactions.append("technical_guidance")
    if acceptance:
        sub_transactions.append("acceptance")
    if material_delivery:
        sub_transactions.append("technical_material_delivery")
    return {
        "sub_transactions": sub_transactions,
        "structured_facts": {
            "technical_secret": {
                "scope": technical_secret_scope,
                "restricted_use": technical_secret_use,
                "separate_fee": technical_secret_fee,
            },
            "technical_service": {
                "content": service_content,
                "activities": service_activities,
                "separate_fee": service_fee,
                "included_in_main_price": service_fee_included,
                "technical_guidance": technical_guidance,
            },
            "acceptance": {
                "defined": acceptance,
                "remedy_deadline": remedy_deadline,
                "reinspection_procedure": reinspection_procedure,
                "reinspection_count": reinspection_count,
                "final_failure_remedy": final_failure_remedy,
                "refund_remedy": refund_remedy,
                "damage_remedy": damage_remedy,
            },
            "technical_material_delivery": {"defined": material_delivery},
        },
    }


def build_technology_fact_registry(text: str) -> Dict[str, Any]:
    """Create source-neutral facts shared by every third-party claim review."""
    compact = re.sub(r"\s+", "", text or "")
    # Contract-defined party aliases must survive section-level extraction.  A claim
    # clause often says only "乙方负责应诉", while the role declaration identifying
    # 乙方 as licensor appears elsewhere in the contract.
    # ``许可方`` must not match the suffix of ``被许可方``.
    licensor_aliases = {r"(?<!被)许可方", "卖方", "出让方", "让与方"}
    for match in re.finditer(
        r"(?P<party>甲方|乙方)(?:[（(](?:许可方|卖方|出让方|让与方)[）)]|.{0,8}(?:为|作为|系)(?:许可方|卖方|出让方|让与方))",
        compact,
    ):
        licensor_aliases.add(re.escape(match.group("party")))
    for match in re.finditer(
        r"(?:许可方|卖方|出让方|让与方)(?:[（(](?P<party1>甲方|乙方)[）)]|.{0,8}(?:为|是|即)(?P<party2>甲方|乙方))",
        compact,
    ):
        licensor_aliases.add(re.escape(match.group("party1") or match.group("party2")))
    licensor = r"(?:" + "|".join(sorted(licensor_aliases)) + r")"
    claim_section_match = re.search(
        r"第[一二三四五六七八九十\d]+条(?:第三方权利责任|第三方权利主张处理|第三人侵权责任|侵权的处理)(?P<body>.*?)(?=第[一二三四五六七八九十\d]+条|$)",
        compact,
    )
    claim_scope = claim_section_match.group(0) if claim_section_match else compact

    def licensor_bears(term_pattern: str) -> bool:
        return bool(
            re.search(rf"{licensor}[^。；;]{{0,90}}(?:承担|负担|赔偿)[^。；;]{{0,80}}(?:{term_pattern})", claim_scope)
            or re.search(rf"(?:{term_pattern})[^。；;]{{0,80}}(?:由|均由){licensor}(?:承担|负担|赔偿)", claim_scope)
        )

    party_name_pattern = r"[^\n；;，,。]{2,80}"
    licensor_name_match = re.search(
        rf"(?:许可方|出让方|让与方|卖方)(?:[（(](?:甲方|乙方)[）)])?[：:]\s*(?P<name>{party_name_pattern})",
        text or "",
    )
    patent_owner_match = re.search(rf"专利权人[：:]\s*(?P<name>{party_name_pattern})", text or "")

    def normalized_entity(value: str) -> str:
        return re.sub(r"[\s（）()《》<>：:，,。；;]", "", value or "")

    named_entity_match = bool(
        licensor_name_match and patent_owner_match
        and normalized_entity(licensor_name_match.group("name")) == normalized_entity(patent_owner_match.group("name"))
    )
    role_owner_match = bool(
        patent_owner_match
        and normalized_entity(patent_owner_match.group("name")) in {"许可方", "出让方", "让与方", "乙方"}
        and re.search(r"(?:乙方[（(](?:许可方|出让方|让与方)[）)]|(?:许可方|出让方|让与方)[（(]乙方[）)])", text or "")
    )
    licensor_is_patent_owner = named_entity_match or role_owner_match
    authority = bool(
        licensor_is_patent_owner
        or re.search(rf"{licensor}.{{0,45}}(?:合法权利人|合法授权主体|有权许可|有权授予|完整权利)", compact)
    )
    claim_trigger = bool(
        re.search(r"(?:第三方|第三人).{0,55}(?:权利主张|指控|侵犯|侵权|侵权责任).{0,65}(?:被许可方|买方|受让方|甲方|许可权瑕疵)", compact)
        or re.search(r"(?:第三方|第三人).{0,30}(?:权利主张|主张|指控|侵权责任).{0,55}(?:被许可方|买方|受让方|甲方|许可权瑕疵|交涉|应诉)", compact)
        or re.search(r"(?:被许可方|买方|受让方).{0,45}(?:按约|依约|按照本合同|授权范围).{0,45}(?:第三方|第三人).{0,35}(?:权利主张|指控|侵犯|侵权)", compact)
        or re.search(r"(?:第三方|第三人).{0,55}(?:被许可方|买方|受让方).{0,45}(?:按约|依约|按照本合同|授权范围).{0,35}(?:权利主张|指控|侵犯|侵权)", compact)
        or bool(re.search(r"第三人侵权责任.{0,120}(?:负责与第三方交涉|负责交涉|应诉)", claim_scope))
    )
    claim_handling = bool(re.search(rf"{licensor}.{{0,45}}(?:负责|应|须).{{0,30}}(?:交涉|处理)", claim_scope))
    litigation_handling = bool(re.search(
        rf"{licensor}.{{0,25}}(?:负责|应|须).{{0,16}}(?:应诉|提起诉讼|处理诉讼|进行抗辩|负责抗辩)",
        claim_scope,
    ))
    notification_requirement = bool(
        re.search(r"(?:收到|获悉).{0,35}第三方.{0,45}(?:应|须).{0,20}通知", claim_scope)
        or re.search(r"(?:被许可方|买方|受让方|甲方).{0,15}(?:应|须).{0,20}(?:收到|获悉).{0,35}第三方.{0,45}通知", claim_scope)
    )
    notification_deadline = bool(re.search(
        r"第三方.{0,80}\d+个?(?:工作日|日|天).{0,25}通知|"
        r"\d+个?(?:工作日|日|天).{0,55}通知.{0,35}第三方",
        claim_scope,
    ))
    explicit_process_gap = bool(re.search(
        r"(?:未对|未约定|未明确|未另行约定).{0,150}(?:通知期限|抗辩控制|律师选择|和解决策|费用承担)",
        claim_scope,
    ))
    defense_control = bool(re.search(r"(?:抗辩控制权|控制抗辩).{0,30}(?:归|由|属于)?(?:许可方|卖方|出让方)", claim_scope)) and not explicit_process_gap
    lawyer_selection = bool(re.search(r"律师选择(?:权|机制).{0,30}(?:归|由|属于)?(?:许可方|卖方|出让方)", claim_scope)) and not explicit_process_gap
    settlement_authority = bool(re.search(r"(?:和解决策权限|和解权限|决定是否和解).{0,30}(?:归|由|属于)?(?:许可方|卖方|出让方)", claim_scope)) and not explicit_process_gap
    attorney_fee = licensor_bears(r"(?:合理)?律师费")
    litigation_cost = licensor_bears(r"(?:诉讼费|诉讼费用|仲裁费|程序费用)")
    direct_damage = licensor_bears(r"(?:直接经济损失|合理直接损失|直接损失)")
    general_liability = licensor_bears(r"(?:法律和经济责任|法律责任|经济责任|赔偿责任|损失)")
    replacement_remedy = bool(re.search(rf"{licensor}.{{0,90}}(?:提供|采取|负责).{{0,35}}(?:替代技术|替代方案|绕开侵权方案)", compact))
    license_cure = bool(re.search(rf"{licensor}.{{0,90}}(?:取得|补办|恢复).{{0,30}}(?:第三方许可|许可权|授权)", compact))
    refund_remedy = bool(re.search(rf"{licensor}.{{0,100}}(?:退还|返还).{{0,25}}(?:许可费|许可费用|使用费|价款)", compact))
    third_party_claim = {
        "authority_warranty": authority,
        "licensor_is_patent_owner": licensor_is_patent_owner,
        "claim_trigger": claim_trigger,
        "claim_handling": claim_handling,
        "litigation_handling": litigation_handling,
        "attorney_fee": attorney_fee,
        "litigation_cost": litigation_cost,
        "direct_damage": direct_damage,
        "notification_requirement": notification_requirement,
        "notification_deadline": notification_deadline,
        "defense_control": defense_control,
        "lawyer_selection": lawyer_selection,
        "settlement_authority": settlement_authority,
        "replacement_remedy": replacement_remedy,
        "license_cure": license_cure,
        "refund_remedy": refund_remedy,
        "general_liability": general_liability,
        "explicit_process_gap": explicit_process_gap,
        "responsible_party": "LICENSOR" if any((claim_handling, litigation_handling, attorney_fee, litigation_cost, direct_damage, general_liability)) else "UNKNOWN",
    }
    return {"third_party_claim": third_party_claim}


def classify_technology_transaction(text: str) -> Dict[str, Any]:
    """Return the canonical technology classification for the active request."""
    state = _classification_session.get()
    if state is None:
        return _classify_technology_transaction_uncached(text)

    caller = inspect.currentframe().f_back
    caller_module = str(caller.f_globals.get("__name__") or "") if caller else ""
    caller_function = caller.f_code.co_name if caller else ""
    caller_line = caller.f_lineno if caller else 0
    document_hash = _classification_document_hash(text)
    state["invocation_count"] += 1
    cache_hit = bool(state.get("result") is not None and document_hash == state.get("document_hash"))
    state["calls"].append({
        "call_number": state["invocation_count"],
        "module": caller_module,
        "function": caller_function,
        "line": caller_line,
        "cache_hit": cache_hit,
    })
    if cache_hit:
        state["cache_hit_count"] += 1
        return state["result"]

    result = _classify_technology_transaction_uncached(text)
    state["actual_execution_count"] += 1
    if document_hash == state.get("document_hash"):
        state["result"] = result
    return result


def _contract_total_candidates(text: str) -> List[Dict[str, Any]]:
    """Extract explicit contract-price facts without discarding provisional values."""
    label = (
        r"合同总价款|合同总价|合同总额|合同价款|"
        r"(?:研发|开发|技术开发)?费用(?:总价|总额)|"
        r"技术服务费用|技术咨询费用|技术咨询报酬|服务报酬|专利权转让价款|"
        r"入门费总额|本合同入门费"
    )
    pattern = re.compile(
        rf"(?P<label>{label})(?P<context>[\s\S]{{0,100}}?)(?:￥|¥)\s*(?P<amount>[0-9][0-9,]*(?:\.\d+)?)\s*元",
        re.I,
    )
    candidates: List[Dict[str, Any]] = []
    for match in pattern.finditer(text or ""):
        raw = match.group(0)
        if "%" in raw:
            continue
        amount = _decimal(match.group("amount"))
        candidates.append({
            "value": _number(amount),
            "label": match.group("label"),
            "certainty": "provisional" if any(term in raw for term in ("暂定", "暂估", "预估")) else "explicit",
            "raw_text": raw.strip(),
            "start_offset": match.start(),
            "end_offset": match.end(),
        })
    # Plain Arabic amount remains supported for contracts that do not use a currency symbol.
    plain_pattern = re.compile(
        rf"(?P<label>{label})(?P<context>[^。；\n]{{0,35}}?)(?:为|共计|合计|总计|：|:)\s*(?:人民币)?\s*{MONEY_PATTERN}",
        re.I,
    )
    for match in plain_pattern.finditer(text or ""):
        if "%" in match.group(0) or any(row["start_offset"] == match.start() for row in candidates):
            continue
        candidates.append({
            "value": _number(_decimal(match.group(3))),
            "label": match.group("label"),
            "certainty": "provisional" if any(term in match.group(0) for term in ("暂定", "暂估", "预估")) else "explicit",
            "raw_text": match.group(0).strip(),
            "start_offset": match.start(),
            "end_offset": match.end(),
        })
    foreign_pattern = re.compile(
        rf"(?P<label>{label})(?P<context>[\s\S]{{0,60}}?)(?:为|共计|合计|总计|：|:)?\s*"
        r"(?P<amount>[0-9][0-9,]*(?:\.\d+)?)\s*(?P<currency>美元|USD)",
        re.I,
    )
    for match in foreign_pattern.finditer(text or ""):
        if "%" in match.group(0) or any(row["start_offset"] == match.start() for row in candidates):
            continue
        candidates.append({
            "value": _number(_decimal(match.group("amount"))),
            "label": match.group("label"),
            "currency": "USD",
            "certainty": "provisional" if any(term in match.group(0) for term in ("暂定", "暂估", "预估")) else "explicit",
            "raw_text": match.group(0).strip(),
            "start_offset": match.start(),
            "end_offset": match.end(),
        })
    return sorted(candidates, key=lambda row: (row["start_offset"], row["end_offset"]))


def _contract_total(text: str) -> Optional[Decimal]:
    candidates = _contract_total_candidates(text)
    return _decimal(str(candidates[0]["value"])) if candidates else None


def _source_context(text: str, start: int, raw_context: str) -> Dict[str, Any]:
    line_no = text.count("\n", 0, start) + 1
    prefix_lines = text[:start].splitlines()
    previous = next((line.strip() for line in reversed(prefix_lines) if line.strip()), "")
    trigger = re.sub(r"\s+", "", raw_context).strip("：:") or previous
    if previous and (len(trigger) < 4 or re.fullmatch(r"(?:支付|应支付)?(?:合同)?(?:总)?价款的?", trigger)):
        trigger = previous
    stage_source = f"{previous}{trigger}"
    if any(term in stage_source for term in ("合同签订", "合同生效", "首笔", "首期")):
        stage = "initial"
    elif any(term in stage_source for term in ("最终验收", "尾款", "末期")):
        stage = "final"
    elif any(term in stage_source for term in ("质保", "保证金")):
        stage = "retention"
    else:
        stage = "milestone"
    return {"line_no": line_no, "source_location": f"line {line_no}", "trigger": trigger, "stage": stage}


def analyze_payment_schedule(text: str) -> Dict[str, Any]:
    state = _payment_analysis_session.get()
    if state is not None:
        caller = inspect.currentframe().f_back
        state["invocation_count"] += 1
        state["calls"].append({
            "module": str(caller.f_globals.get("__name__") or "") if caller else "",
            "function": caller.f_code.co_name if caller else "",
            "line": caller.f_lineno if caller else 0,
        })
    value = text or ""
    total_candidates = _contract_total_candidates(value)
    total = _contract_total(value)
    node_pattern = re.compile(
        rf"(?P<context>[^。；\n]{{0,55}}?)(?P<pct>\d+(?:\.\d+)?)\s*%[^。；\n]{{0,35}}?(?:即|为|计)\s*(?:人民币)?\s*{MONEY_PATTERN}",
        re.I,
    )
    nodes: List[Dict[str, Any]] = []
    seen: set[tuple[int, int, str, str, str]] = set()
    facts_before_dedup: List[Dict[str, Any]] = []
    for sequence, match in enumerate(node_pattern.finditer(value), start=1):
        pct = _decimal(match.group("pct"))
        amount = _decimal(match.group(3))
        context = match.group("context")
        if any(term in context for term in ("上述付款比例合计", "付款比例合计", "金额合计")):
            continue
        source = _source_context(value, match.start(), context)
        included_retention = "包含" in f"{context}{source['trigger']}" and any(term in f"{context}{source['trigger']}" for term in ("质保", "保证金"))
        raw_text = match.group(0).strip()
        fact = {
            "fact_id": f"PAY-{sequence:03d}-{hashlib.sha256(f'{match.start()}:{match.end()}:{raw_text}'.encode('utf-8')).hexdigest()[:10]}",
            "source_document": _classification_document_hash(value),
            "source_clause": source["trigger"],
            "source_location": source["source_location"],
            "sequence": sequence,
            "stage": source["stage"],
            "trigger": source["trigger"],
            "condition": source["trigger"],
            "percentage": _number(pct),
            "amount": _number(amount),
            "currency": "CNY",
            "payment_type": source["stage"],
            "is_deposit": source["stage"] == "initial",
            "is_stage_payment": source["stage"] == "milestone",
            "is_final_payment": source["stage"] == "final",
            "is_retention": source["stage"] == "retention",
            "raw_text": raw_text,
            "start_offset": match.start(),
            "end_offset": match.end(),
            "context": context.strip(),
            "retention_included": included_retention,
        }
        facts_before_dedup.append(dict(fact))
        # Identity is source-bound. Equal values at distinct stages/locations are separate obligations.
        key = (match.start(), match.end(), source["trigger"], str(pct), str(amount))
        if key not in seen:
            seen.add(key)
            nodes.append(fact)

    cross_line_pattern = re.compile(
        r"(?P<pct>\d+(?:\.\d+)?)\s*%\s*(?:\r?\n|\s)*(?:即|为|计)\s*[：:]?\s*"
        r"(?:\r?\n|\s)*(?P<amount>[0-9][0-9,]*(?:\.\d+)?)\s*(?P<currency>美元|USD|元)",
        re.I,
    )
    for match in cross_line_pattern.finditer(value):
        if any(node["start_offset"] == match.start() for node in nodes):
            continue
        pct = _decimal(match.group("pct"))
        amount = _decimal(match.group("amount"))
        context_start = max(0, match.start() - 100)
        context = value[context_start:match.start()]
        if any(term in context[-60:] for term in ("提成率", "计算示例", "应付提成费", "净销售额")):
            continue
        source = _source_context(value, match.start(), context[-55:])
        sequence = len(facts_before_dedup) + 1
        raw_text = match.group(0).strip()
        currency = "USD" if match.group("currency").upper() == "USD" or match.group("currency") == "美元" else "CNY"
        fact = {
            "fact_id": f"PAY-{sequence:03d}-{hashlib.sha256(f'{match.start()}:{match.end()}:{raw_text}'.encode('utf-8')).hexdigest()[:10]}",
            "source_document": _classification_document_hash(value),
            "source_clause": source["trigger"], "source_location": source["source_location"],
            "sequence": sequence, "stage": source["stage"], "trigger": source["trigger"], "condition": source["trigger"],
            "percentage": _number(pct), "amount": _number(amount), "currency": currency,
            "payment_type": source["stage"], "is_deposit": source["stage"] == "initial",
            "is_stage_payment": source["stage"] == "milestone", "is_final_payment": source["stage"] == "final",
            "is_retention": source["stage"] == "retention", "raw_text": raw_text,
            "start_offset": match.start(), "end_offset": match.end(), "context": context[-55:].strip(),
            "retention_included": False,
        }
        facts_before_dedup.append(dict(fact))
        nodes.append(fact)

    effective_nodes = [node for node in nodes if not node["retention_included"]]
    percentage_total = sum((_decimal(str(node["percentage"])) for node in effective_nodes), Decimal("0"))
    amount_total = sum((_decimal(str(node["amount"])) for node in effective_nodes), Decimal("0"))
    node_mismatches: List[Dict[str, Any]] = []
    if total is not None:
        for index, node in enumerate(nodes, start=1):
            expected = total * _decimal(str(node["percentage"])) / Decimal("100")
            actual = _decimal(str(node["amount"]))
            if abs(expected - actual) > Decimal("0.01"):
                node_mismatches.append({
                    "node": index,
                    "percentage": node["percentage"],
                    "expected_amount": _number(expected),
                    "actual_amount": node["amount"],
                    "delta": _number(actual - expected),
                })
    amount_delta = amount_total - total if total is not None else None
    inconsistent = bool(nodes) and (
        percentage_total != Decimal("100")
        or (amount_delta is not None and abs(amount_delta) > Decimal("0.01"))
        or bool(node_mismatches)
    )
    result = {
        "status": "INCONSISTENT" if inconsistent else "CONSISTENT" if nodes and total is not None else "INSUFFICIENT_DATA",
        "contract_total": _number(total) if total is not None else None,
        "contract_total_candidates": total_candidates,
        "percentage_total": _number(percentage_total),
        "amount_total": _number(amount_total),
        "amount_delta": _number(amount_delta) if amount_delta is not None else None,
        "nodes": nodes,
        "payment_fact_count": len(nodes),
        "facts_before_dedup": facts_before_dedup,
        "facts_after_dedup": [dict(node) for node in nodes],
        "node_mismatches": node_mismatches,
        "currency": next((row.get("currency") for row in nodes if row.get("currency")), next((row.get("currency") for row in total_candidates if row.get("currency")), "CNY")),
    }
    if state is not None:
        state["last_output"] = result
    return result


def analyze_royalty_calculation(text: str) -> Dict[str, Any]:
    """Validate an explicit sales-royalty example independently from staged fees."""
    value = text or ""

    def money(label: str) -> Optional[Decimal]:
        match = re.search(
            rf"(?:{label})\s*[：:]?\s*(?:\r?\n|\s)*([0-9][0-9,]*(?:\.\d+)?)\s*(?:美元|USD|元)",
            value,
            re.I,
        )
        return _decimal(match.group(1)) if match else None

    sales = money(r"合同产品销售收入|销售收入|销售额")
    deduction_labels = ("包装费", "运输费", "保险费", "商业折扣", "税金", "外购件费用")
    deductions = {label: money(label) for label in deduction_labels}
    net_sales = money(r"净销售额")
    fee = money(r"应付提成费|提成费")
    rate_match = re.search(r"(?:提成率|净销售额的)\s*[：:]?\s*(?:\r?\n|\s)*(\d+(?:\.\d+)?)\s*%", value)
    rate = _decimal(rate_match.group(1)) if rate_match else None
    known_deductions = [amount for amount in deductions.values() if amount is not None]
    expected_net = sales - sum(known_deductions, Decimal("0")) if sales is not None and known_deductions else None
    expected_fee = net_sales * rate / Decimal("100") if net_sales is not None and rate is not None else None
    net_delta = net_sales - expected_net if net_sales is not None and expected_net is not None else None
    fee_delta = fee - expected_fee if fee is not None and expected_fee is not None else None
    complete = all(row is not None for row in (sales, net_sales, rate, fee)) and bool(known_deductions)
    consistent = bool(complete and abs(net_delta or Decimal("0")) <= Decimal("0.01") and abs(fee_delta or Decimal("0")) <= Decimal("0.01"))
    return {
        "status": "CONSISTENT" if consistent else "INCONSISTENT" if complete else "INSUFFICIENT_DATA",
        "sales": _number(sales) if sales is not None else None,
        "deductions": {label: _number(amount) for label, amount in deductions.items() if amount is not None},
        "deduction_total": _number(sum(known_deductions, Decimal("0"))) if known_deductions else None,
        "net_sales": _number(net_sales) if net_sales is not None else None,
        "expected_net_sales": _number(expected_net) if expected_net is not None else None,
        "royalty_rate": _number(rate) if rate is not None else None,
        "royalty_fee": _number(fee) if fee is not None else None,
        "expected_royalty_fee": _number(expected_fee) if expected_fee is not None else None,
        "net_sales_delta": _number(net_delta) if net_delta is not None else None,
        "royalty_fee_delta": _number(fee_delta) if fee_delta is not None else None,
        "currency": "USD" if "美元" in value or "USD" in value.upper() else "CNY",
    }


def _first_date(text: str, patterns: tuple[str, ...]) -> Optional[str]:
    for pattern in patterns:
        match = re.search(pattern, text, re.S)
        if not match:
            continue
        date_match = DATE_PATTERN.search(match.group(0))
        if date_match:
            return _iso(date_match)
    return None


def analyze_timeline(text: str) -> Dict[str, Any]:
    value = text or ""
    service_start = _first_date(value, (
        r"服务期限[\s\S]{0,45}",
        r"服务开始[^。\n]{0,20}",
        r"履行期限[^。\n]{0,35}",
    ))
    data_deadline = _first_date(value, (
        r"(?:第一批|首批)[^。\n]{0,12}技术资料[\s\S]{0,45}?(?:应于|应在|交付时间)[\s\S]{0,30}",
        r"技术资料交付时间[\s\S]{0,35}",
        r"(?:提供|提交)[^。\n]{0,12}(?:资料|数据)[^。\n]{0,35}",
        r"(?:资料|数据)[^。\n]{0,18}(?:提供|提交)[^。\n]{0,35}",
        r"应在\s*20\d{2}年\d{1,2}月\d{1,2}日前[^。\n]{0,30}(?:资料|数据)",
        r"(?:甲方|委托方|客户)[^。\n]{0,8}应在\s*20\d{2}年\d{1,2}月\d{1,2}日前[^。\n]{0,20}(?:提供|提交)",
    ))
    signature_dates = [
        _iso(match) for match in DATE_PATTERN.finditer(value)
        if any(term in value[max(0, match.start() - 30):match.start()] for term in ("签订", "签署", "签名", "盖章"))
    ]
    effective_date = _first_date(value, (
        r"(?:合同生效日期|本合同生效日期|生效日期为|双方最后批准日期)[^。\n]{0,45}",
        r"(?:批准与生效)[\s\S]{0,100}?20\d{2}年\d{1,2}月\d{1,2}日",
        r"(?:合同于|本合同于)[^。\n]{0,35}(?:签署|签订|生效)",
        r"(?:签订时间|签署日期|签订日期|生效日期)[：:\s]*20\d{2}年\d{1,2}月\d{1,2}日",
    ))
    if not effective_date and any(term in value for term in ("签字", "签名", "盖章")) and "生效" in value and signature_dates:
        effective_date = max(signature_dates)

    performance_facts: List[Dict[str, Any]] = []
    performance_markers = (
        "需求分析", "开发进度", "研发进度", "项目进度", "开发开始", "研发开始",
        "第一阶段", "第一期", "项目启动", "实施开始", "履行开始",
        "第一批技术资料", "首批技术资料", "技术资料交付时间", "技术资料交付期限",
    )
    for match in DATE_PATTERN.finditer(value):
        context = value[max(0, match.start() - 80):min(len(value), match.end() + 40)]
        matched = [term for term in performance_markers if term in context]
        if not matched:
            continue
        performance_facts.append({
            "fact_id": f"DATE-PERF-{len(performance_facts) + 1:03d}",
            "type": "PERFORMANCE_DATE",
            "date": _iso(match),
            "matched_terms": matched,
            "source_location": f"line {value.count(chr(10), 0, match.start()) + 1}",
            "raw_text": re.sub(r"\s+", " ", context).strip(),
        })
    earliest_performance = min((row["date"] for row in performance_facts), default=service_start)

    conflicts: List[Dict[str, Any]] = []
    if effective_date and service_start and service_start < effective_date:
        conflicts.append({"type": "SERVICE_BEFORE_EFFECTIVE", "earlier_date": service_start, "effective_date": effective_date})
    if effective_date and data_deadline and data_deadline < effective_date:
        conflicts.append({"type": "DATA_DUE_BEFORE_EFFECTIVE", "earlier_date": data_deadline, "effective_date": effective_date})
    if effective_date and earliest_performance and earliest_performance < effective_date and not any(
        row["type"] == "SERVICE_BEFORE_EFFECTIVE" and row["earlier_date"] == earliest_performance for row in conflicts
    ):
        conflicts.append({"type": "PERFORMANCE_BEFORE_EFFECTIVE", "earlier_date": earliest_performance, "effective_date": effective_date})
    conflict_types = [row["type"] for row in conflicts]
    if "DATA_DUE_BEFORE_EFFECTIVE" in conflict_types:
        primary_conflict_subject = "TECHNICAL_MATERIAL_DELIVERY"
    elif "SERVICE_BEFORE_EFFECTIVE" in conflict_types:
        primary_conflict_subject = "SERVICE_START"
    elif "PERFORMANCE_BEFORE_EFFECTIVE" in conflict_types:
        primary_conflict_subject = "PERFORMANCE_START"
    else:
        primary_conflict_subject = ""
    return {
        "effective_date": effective_date,
        "service_start_date": service_start,
        "earliest_performance_date": earliest_performance,
        "performance_before_effective_date": bool(effective_date and earliest_performance and earliest_performance < effective_date),
        "date_facts": performance_facts,
        "data_delivery_deadline": data_deadline,
        "conflicts": conflicts,
        "conflict_types": conflict_types,
        "primary_conflict_subject": primary_conflict_subject,
    }


def analyze_proposition_polarity(
    text: str,
    proposition_terms: tuple[str, ...] = tuple(),
) -> Dict[str, Any]:
    """Resolve whether a clause affirms, negates, or prohibits a proposition.

    A prohibition such as ``未经许可不得披露`` affirmatively creates an
    obligation.  An absence declaration such as ``未约定删除机制`` negates
    the existence of the tracked contractual mechanism.  Keeping those two
    forms separate prevents target keywords inside an explicit gap statement
    from becoming positive coverage evidence.
    """
    source = text or ""
    compact = re.sub(r"\s+", "", source)
    matched_terms = [term for term in proposition_terms if term and term in compact]
    absence_patterns = (
        r"(?:双方|各方|当事人)?(?:尚未|未曾|未|没有|并未|并没有)(?:另行)?(?:约定|明确|规定|设置|建立|提供|提交)[^。；]{0,140}",
        r"(?:双方|各方|当事人)?(?:尚未|未曾|未|没有|并未|并没有)(?:对|就)[^。；]{0,140}(?:作[^。；]{0,12}约定|约定|明确|规定|设置|建立)",
        r"(?:双方|各方|当事人)?(?:无|不存在)[^。；]{0,80}(?:约定|机制|义务|责任|安排|条款)",
        r"(?:不承担|无需承担|无须承担)[^。；]{0,80}(?:义务|责任|费用|赔偿)",
        r"(?:不适用|未发现|未提供)[^。；]{0,80}",
    )
    prohibition_patterns = (
        r"未经[^。；]{0,60}(?:不得|禁止|严禁)[^。；]{0,100}",
        r"(?:不得|禁止|严禁)[^。；]{0,100}(?:披露|泄露|使用|复制|转让|许可|收取|研发|开发|销售)",
    )
    def proposition_match(patterns: tuple[str, ...]) -> Optional[re.Match[str]]:
        for pattern in patterns:
            for match in re.finditer(pattern, compact):
                if not proposition_terms or any(term in match.group(0) for term in proposition_terms):
                    return match
        return None

    absence_match = proposition_match(absence_patterns)
    prohibition_match = proposition_match(prohibition_patterns)
    if absence_match:
        polarity = "NEGATED"
        fact_value: Optional[bool] = False
        cue = absence_match.group(0)
        semantic_role = "EXPLICIT_GAP"
    elif prohibition_match:
        polarity = "PROHIBITIVE_OBLIGATION"
        fact_value = True
        cue = prohibition_match.group(0)
        semantic_role = "AFFIRMATIVE_DUTY"
    else:
        polarity = "AFFIRMATIVE"
        fact_value = True if matched_terms else None
        cue = ""
        semantic_role = "POSITIVE_ASSERTION" if matched_terms else "UNRESOLVED"
    return {
        "polarity": polarity,
        "fact_value": fact_value,
        "semantic_role": semantic_role,
        "negation_cue": cue,
        "matched_terms": matched_terms,
        "source_text": source,
    }


def _improvement_party(value: str) -> str:
    return {
        "受让方": "LICENSEE", "被许可方": "LICENSEE", "买方": "LICENSEE", "甲方": "PARTY_A", "A方": "PARTY_A", "A": "PARTY_A",
        "出让方": "LICENSOR", "许可方": "LICENSOR", "卖方": "LICENSOR", "乙方": "PARTY_B", "B方": "PARTY_B", "B": "PARTY_B",
    }.get(value, value or "UNKNOWN")


def _improvement_license_fact(
    improving_party: str,
    grantee: str,
    window: str,
    *,
    negotiated: bool = False,
) -> Dict[str, Any]:
    fee = "NEGOTIATED" if negotiated else "ZERO" if any(term in window for term in ("无偿", "免费", "不收取任何费用", "不得收取任何费用")) else "UNSPECIFIED"
    duration = "NEGOTIATED" if negotiated else "PERPETUAL" if "永久" in window else "UNSPECIFIED"
    territory = "NEGOTIATED" if negotiated else "WORLDWIDE" if any(term in window for term in ("全球范围", "全球")) else "UNSPECIFIED"
    revocability = "NEGOTIATED" if negotiated else "IRREVOCABLE" if "不可撤销" in window else "UNSPECIFIED"
    exclusivity = "NEGOTIATED" if negotiated else "NON_EXCLUSIVE" if "非独占" in window else "EXCLUSIVE" if "独占" in window else "UNSPECIFIED"
    return {
        "improving_party": improving_party,
        "grantor": improving_party,
        "grantee": grantee,
        "license_fee": fee,
        "license_duration": duration,
        "territory": territory,
        "revocability": revocability,
        "exclusivity": exclusivity,
        "commercial_use": True if any(term in window for term in ("商业目的", "商业使用", "商业化")) else None,
        "reciprocal_obligation": None,
        "source_text": window,
    }


def _improvement_fact_window(compact: str, start: int, limit: int = 240) -> str:
    """Keep a directional fact inside its own numbered clause or sentence."""
    window = compact[start:start + limit]
    next_clause = re.search(r"\d+\.\d+", window[8:])
    if next_clause:
        return window[:8 + next_clause.start()]
    sentence_end = window.find("。")
    return window[:sentence_end + 1] if sentence_end >= 0 else window


def analyze_improvement_license_facts(text: str) -> Dict[str, Any]:
    """Extract directional improvement grant-backs and compare their terms."""
    compact = re.sub(r"\s+", "", text or "")
    facts: List[Dict[str, Any]] = []

    licensee_match = re.search(
        r"(?:受让方|被许可方|买方).{0,45}(?:改进成果|改进技术).{0,25}(?:应|须|必须).{0,8}(?:无偿|免费).{0,12}(?:授予|许可|提供)(?:给)?(?:出让方|许可方|卖方)",
        compact,
    )
    if licensee_match:
        start = licensee_match.start()
        facts.append(_improvement_license_fact("LICENSEE", "LICENSOR", _improvement_fact_window(compact, start)))

    licensor_match = re.search(
        r"(?:出让方|许可方|卖方)(?:的)?(?:改进成果|改进技术|新的改进技术).{0,70}(?:受让方|被许可方|买方).{0,30}(?:使用|取得).{0,45}(?:另行协商|重新协商|协商)(?:许可条件|许可费用|费用|许可范围)?",
        compact,
    )
    if licensor_match:
        start = licensor_match.start()
        facts.append(_improvement_license_fact(
            "LICENSOR", "LICENSEE", _improvement_fact_window(compact, start, 220), negotiated=True,
        ))

    # General directional language used by mutation and non-template contracts.
    party_token = r"受让方|被许可方|出让方|许可方|甲方|乙方|A方|B方|A|B"
    for match in re.finditer(
        rf"(?P<grantor>{party_token})(?:形成的|形成|的)?(?:任何)?(?:改进成果|改进技术|改进)[^。；;]{{0,25}}(?:无偿|免费)[^。；;]{{0,15}}(?:授予|许可|提供|给)(?P<grantee>{party_token})",
        compact,
    ):
        grantor = _improvement_party(match.group("grantor"))
        grantee = _improvement_party(match.group("grantee"))
        if not any(row["grantor"] == grantor and row["grantee"] == grantee for row in facts):
            facts.append(_improvement_license_fact(
                grantor, grantee, _improvement_fact_window(compact, match.start(), 180),
            ))

    for match in re.finditer(
        rf"(?P<grantor>{party_token})(?:形成的|形成|的)?(?:任何)?(?:改进成果|改进技术|改进)[^。；;]{{0,35}}(?P<grantee>{party_token})[^。；;]{{0,35}}(?:必须付费|另行付费|有偿许可|协商费用|另行协商费用|另行支付许可费|支付许可费)",
        compact,
    ):
        grantor = _improvement_party(match.group("grantor"))
        grantee = _improvement_party(match.group("grantee"))
        if not any(row["grantor"] == grantor and row["grantee"] == grantee for row in facts):
            facts.append(_improvement_license_fact(
                grantor, grantee, _improvement_fact_window(compact, match.start(), 180), negotiated=True,
            ))

    symmetric_shortcut = bool(re.search(
        r"双方.{0,30}(?:改进成果|改进技术).{0,30}(?:均|互相|相互).{0,20}(?:无偿|免费).{0,40}(?:同等|相同|同期限|同地域|期限均|地域均)",
        compact,
    ))
    if symmetric_shortcut and len(facts) < 2:
        common = {
            "license_fee": "ZERO", "license_duration": "SAME_DEFINED", "territory": "SAME_DEFINED",
            "revocability": "SAME_DEFINED", "exclusivity": "SAME_DEFINED", "commercial_use": None,
            "reciprocal_obligation": True, "source_text": compact,
        }
        facts = [
            {"improving_party": "PARTY_A", "grantor": "PARTY_A", "grantee": "PARTY_B", **common},
            {"improving_party": "PARTY_B", "grantor": "PARTY_B", "grantee": "PARTY_A", **common},
        ]

    comparison_fields = ("license_fee", "license_duration", "territory", "revocability", "exclusivity", "commercial_use")
    signatures = [tuple(row.get(field) for field in comparison_fields) for row in facts]
    has_mandatory_free_grant = any(row.get("license_fee") == "ZERO" for row in facts)
    asymmetric = bool(
        facts
        and not symmetric_shortcut
        and (
            len(facts) == 1 and has_mandatory_free_grant
            or len(facts) >= 2 and len(set(signatures)) > 1
        )
    )
    for row in facts:
        row["reciprocal_obligation"] = not asymmetric and len(facts) >= 2
    licensee_owns_improvement = bool(re.search(
        r"(?:受让方|被许可方|买方|甲方).{0,45}(?:改进成果|改进技术).{0,180}(?:归其所有|归(?:受让方|被许可方|买方|甲方)(?:所有)?|归属[：:]?(?:受让方|被许可方|买方|甲方)(?:所有)?)",
        compact,
    ))
    licensor_owns_improvement = bool(re.search(
        r"(?:出让方|让与方|许可方|卖方|乙方).{0,45}(?:改进成果|改进技术).{0,180}(?:归其所有|归(?:出让方|让与方|许可方|卖方|乙方)(?:所有)?|归属[：:]?(?:出让方|让与方|许可方|卖方|乙方)(?:所有)?)",
        compact,
    ))
    licensee_priority_license = bool(re.search(
        r"(?:受让方|被许可方|买方|甲方).{0,25}(?:优先许可权|优先获得许可|优先被许可)", compact,
    ))
    licensor_use_negotiated = bool(re.search(
        r"(?:出让方|许可方|卖方|乙方).{0,40}(?:使用|许可).{0,45}(?:另行协商|协商确定|另行约定)", compact,
    ))
    ownership_arrangement = bool(licensee_owns_improvement or licensor_owns_improvement)
    partial_arrangement = bool(
        ownership_arrangement
        and (
            licensee_priority_license or licensor_use_negotiated
            or "无义务将各自独立完成的后续改进成果无偿许可给另一方" in compact
        )
    )
    arrangement_status = (
        "ASYMMETRIC" if asymmetric
        else "SYMMETRIC" if facts
        else "PARTIAL" if partial_arrangement
        else "MISSING"
    )
    return {
        "arrangement_status": arrangement_status,
        "facts": facts,
        "asymmetric_improvement_license": asymmetric,
        "ownership_and_priority_arrangement": {
            "licensee_owns_improvement": licensee_owns_improvement,
            "licensor_owns_improvement": licensor_owns_improvement,
            "licensee_priority_license": licensee_priority_license,
            "licensor_use_negotiated": licensor_use_negotiated,
            "partial_arrangement": partial_arrangement,
        },
        "comparison_fields": list(comparison_fields),
        "comparison": {
            "fact_count": len(facts),
            "signatures": [list(signature) for signature in signatures],
            "reason": (
                "Directional improvement licences impose materially different fee, duration, territory, revocability, exclusivity or commercial-use terms."
                if asymmetric else "Reciprocal improvement licence terms are materially aligned."
                if len(facts) >= 2 else "Ownership or priority-licence terms exist, but detailed licence conditions remain incomplete."
                if partial_arrangement else "No directional improvement licence allocation was found."
            ),
        },
    }


def analyze_third_party_infringement_allocation(text: str) -> Dict[str, Any]:
    """Return the canonical third-party claim facts used by TC-12-01/02/04."""
    registry = build_technology_fact_registry(text)
    claim = dict(registry["third_party_claim"])
    handles_claim = bool(claim["claim_handling"] or claim["litigation_handling"])
    legal_economic_liability = bool(
        claim["general_liability"] or claim["direct_damage"]
        or claim["attorney_fee"] or claim["litigation_cost"]
    )
    return {
        "licensor_authority_warranty": claim["authority_warranty"],
        "third_party_claim_trigger": claim["claim_trigger"],
        "licensor_handles_claim": handles_claim,
        "licensor_legal_economic_liability": legal_economic_liability,
        "basic_liability_allocation": bool(
            claim["authority_warranty"] and claim["claim_trigger"]
            and handles_claim and legal_economic_liability
        ),
        "claim_process": {
            "explicit_gap": claim["explicit_process_gap"],
            "notification_requirement": claim["notification_requirement"],
            "notification_deadline": claim["notification_deadline"],
            "defense_control": claim["defense_control"],
            "lawyer_selection": claim["lawyer_selection"],
            "settlement_authority": claim["settlement_authority"],
            "defense_cost_allocation": bool(claim["attorney_fee"] or claim["litigation_cost"]),
        },
        "fact_registry": registry,
    }


def analyze_license_lifecycle(text: str) -> Dict[str, Any]:
    """Compare contract, technology, trademark, survival and royalty periods."""
    compact = re.sub(r"\s+", "", text or "")

    def years(patterns: tuple[str, ...]) -> Optional[int]:
        for pattern in patterns:
            match = re.search(pattern, compact)
            if match:
                return int(match.group("years"))
        return None

    contract_duration = years((
        r"合同自生效日起有效期[：:]?(?P<years>\d+)年",
        r"本合同[^。；]{0,18}有效期[：:]?(?P<years>\d+)年",
        r"合同有效期[：:]?(?P<years>\d+)年",
        r"合同期限[：:]?(?:为)?(?P<years>\d+)年",
        r"合同(?P<years>\d+)年",
    ))
    technology_duration = years((
        r"技术许可期限[^。；]{0,12}(?:为|一致，为?)[：:]?(?P<years>\d+)年",
        r"许可技术[^。；]{0,12}期限[：:]?(?P<years>\d+)年",
        r"技术许可期限[：:]?(?:为)?(?P<years>\d+)年",
        r"技术许可(?P<years>\d+)年",
    )) or contract_duration
    trademark_duration = years((
        r"商标许可期限[^。；]{0,30}(?P<years>\d+)年",
        r"商标[^。；]{0,20}(?:仅在|限于)[^。；]{0,15}(?P<years>\d+)年",
    ))
    no_post_technology = bool(re.search(
        r"(?:合同终止|合同解除|期限届满).{0,60}(?:不得|无权|禁止).{0,20}(?:继续)?使用技术",
        compact,
    ))
    post_technology = not no_post_technology and (bool(re.search(
        r"(?:合同终止|合同解除|期限届满).{0,80}(?:仍有权|继续).{0,100}(?:使用技术|使用出让方已交付的技术|使用技术资料)",
        compact,
    )) or bool(re.search(r"技术及技术资料继续使用权.{0,30}不因合同期限届满而终止", compact))
        or bool(re.search(r"技术(?:使用)?(?:权)?永久(?:许可|有效|存续)", compact)))
    perpetual = post_technology and "永久" in compact
    post_sales = post_technology and bool(re.search(r"(?:合同终止|合同解除|期限届满).{0,180}销售合同产品", compact))
    trademark_survives = False if re.search(r"合同终止后.{0,30}不得继续使用.{0,15}商标", compact) else True if re.search(r"合同终止后.{0,30}(?:仍可|有权|继续)使用.{0,15}商标", compact) else None
    royalty_gap_match = re.search(
        r"(?:未另行约定|未约定|尚未明确).{0,80}(?:终止后|继续使用技术).{0,50}(?:提成费|royalty)", compact, re.I,
    ) or re.search(
        r"(?:终止后|继续使用技术).{0,60}(?:提成费|royalty).{0,35}(?:未另行约定|未约定|尚未明确)", compact, re.I,
    )
    royalty_negation = analyze_proposition_polarity(
        royalty_gap_match.group(0) if royalty_gap_match else "",
        ("终止后", "继续使用技术", "支付提成费"),
    )
    royalty_explicit_gap = bool(royalty_gap_match)
    royalty_continues = bool(re.search(
        r"(?:终止后|期限届满后).{0,60}(?:仍|继续).{0,20}(?:支付|按).{0,20}(?:\d+(?:\.\d+)?%|提成费|royalty)",
        compact,
        re.I,
    ))
    royalty_defined = royalty_continues and not royalty_explicit_gap
    risk = bool(post_technology and not royalty_defined)
    post_termination_rights = [
        right for right, present in (
            ("USE_TECHNOLOGY", post_technology and any(term in compact for term in ("使用出让方已交付的技术", "继续使用技术", "技术永久许可"))),
            ("USE_TECHNICAL_MATERIALS", post_technology and "使用技术资料" in compact),
            ("DESIGN_PRODUCTS", post_technology and "设计合同产品" in compact),
            ("MANUFACTURE_PRODUCTS", post_technology and "制造合同产品" in compact),
            ("SELL_PRODUCTS", post_sales),
        ) if present
    ]
    favorable_elements = [
        label for code, label in (
            ("USE_TECHNOLOGY", "终止后继续使用技术"),
            ("USE_TECHNICAL_MATERIALS", "终止后继续使用技术资料"),
            ("DESIGN_PRODUCTS", "终止后继续设计合同产品"),
            ("MANUFACTURE_PRODUCTS", "终止后继续制造合同产品"),
            ("SELL_PRODUCTS", "终止后继续销售合同产品"),
        ) if code in post_termination_rights
    ]
    if perpetual:
        favorable_elements.append("上述许可权利永久存续")
    if post_technology and "不可撤销" in compact:
        favorable_elements.append("上述许可权利不可撤销")
    ambiguous_elements = []
    if risk:
        ambiguous_elements.extend([
            "终止后是否继续支付提成费",
            "终止后提成费率",
            "终止后结算周期",
            "终止后销售审计机制",
            "终止后提成义务的终止时间",
        ])
    return {
        "contract_duration_years": contract_duration,
        "technology_license_duration_years": technology_duration,
        "trademark_license_duration_years": trademark_duration,
        "technology_rights_survive_contract": post_technology,
        "technology_rights_survival_duration": "PERPETUAL" if perpetual else "SURVIVES" if post_technology else "NO_SURVIVAL",
        "post_termination_technology_rights": post_termination_rights,
        "post_termination_sales_rights": post_sales,
        "trademark_rights_survive_contract": trademark_survives,
        "post_termination_royalty_defined": royalty_defined,
        "post_termination_royalty_obligation": "CONTINUES" if royalty_defined else "UNDEFINED" if royalty_explicit_gap or post_technology else "NOT_APPLICABLE",
        "royalty_polarity": royalty_negation,
        "license_lifecycle_risk": risk,
        "favorable_elements": favorable_elements,
        "adverse_elements": [],
        "ambiguous_elements": ambiguous_elements,
        "party_interest": {
            "review_role": "LICENSEE",
            "favorable_elements": favorable_elements,
            "adverse_elements": [],
            "ambiguous_elements": ambiguous_elements,
            "overall": "AMBIGUOUS" if ambiguous_elements else "FAVORABLE" if favorable_elements else "NEUTRAL",
        },
        "major_severity_reason": "",
        "risk_reason": (
            "终止后继续使用和销售权本身对被许可方有利，但终止后是否继续产生提成费及其结算规则未明确。"
            if risk else "许可存续期间、终止后使用范围及提成义务之间未发现确定性缺口。"
        ),
    }


def _duration_days(value: str, unit: str) -> int:
    amount = int(value)
    return amount * {"日": 1, "天": 1, "个月": 30, "月": 30, "年": 365}[unit]


def _retention_warranty_relationship(text: str) -> Dict[str, Any]:
    """Compare independently stated deletion and post-delivery duty periods."""
    compact = re.sub(r"\s+", "", text or "")
    retention_patterns = (
        r"(?P<value>\d+)\s*(?P<unit>日|天|个月|月|年)(?:内|后)?[^。；]{0,28}(?:归还|返还|删除|销毁)",
        r"(?:归还|返还|删除|销毁)[^。；]{0,28}(?P<value>\d+)\s*(?P<unit>日|天|个月|月|年)(?:内|后)?",
    )
    warranty_patterns = (
        r"(?:保证期|质保期|保修期)[^。；]{0,20}(?P<value>\d+)\s*(?P<unit>日|天|个月|月|年)",
        r"(?P<value>\d+)\s*(?P<unit>日|天|个月|月|年)[^。；]{0,12}(?:保证期|质保期|保修期)",
    )

    def durations(patterns: tuple[str, ...]) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for pattern in patterns:
            for match in re.finditer(pattern, compact):
                row = {
                    "value": int(match.group("value")),
                    "unit": match.group("unit"),
                    "days": _duration_days(match.group("value"), match.group("unit")),
                    "text": match.group(0),
                }
                if row not in rows:
                    rows.append(row)
        return rows

    retention = durations(retention_patterns)
    warranty = durations(warranty_patterns)
    conflicts = [
        {"retention": left, "post_delivery_duty": right}
        for left in retention
        for right in warranty
        if left["days"] < right["days"]
    ]
    return {"retention_periods": retention, "post_delivery_duty_periods": warranty, "conflicts": conflicts}


def analyze_technical_service_core_facts(text: str) -> Dict[str, Any]:
    """Extract atomic technical-service facts without deciding every fact is a risk."""
    compact = re.sub(r"\s+", "", text or "")
    segments = [segment.strip() for segment in re.split(r"[。；;\n]", text or "") if segment.strip()]
    compact_segments = [re.sub(r"\s+", "", segment) for segment in segments]

    acceptance_segments = [
        segment for segment in compact_segments
        if any(term in segment for term in ("验收", "书面异议", "问题清单", "完成修改"))
    ]
    acceptance_text = "".join(acceptance_segments)
    standard_deferred = bool(re.search(
        r"(?:技术标准|功能目标|验收标准|交付方式)(?:及|、|等|[^。；]){0,100}"
        r"(?:另行书面确认|另行确认|后续书面确认|另行约定|后续确定)",
        compact,
    ))
    standard_concrete = any(term in acceptance_text for term in (
        "准确率", "响应时间", "并发量", "可用率", "功能清单", "缺陷等级", "测试用例", "性能指标",
    ))
    remedy_deadline_specific = bool(re.search(
        r"(?:应|须)(?:在)?\d+(?:个)?(?:工作日|日|小时)内(?:完成)?(?:修改|整改|修复)|"
        r"(?:修改|整改|修复)期限(?:为|：|:)\d+",
        acceptance_text,
    ))

    result_segments = [
        segment for segment in compact_segments
        if any(term in segment for term in ("项目成果", "软件功能", "程序代码", "技术文档", "新技术成果"))
        and any(term in segment for term in ("知识产权", "归属", "归甲方", "归乙方", "归双方"))
    ]
    result_text = "".join(result_segments)
    ownership_deferred = any(
        term in result_text for term in ("另行协商确定", "另行协商", "另行约定", "后续确定", "另行确认")
    )
    ownership_finalized = bool(re.search(
        r"(?:项目成果|软件功能|程序代码|技术文档|新技术成果)[^。；]{0,100}"
        r"(?:知识产权)?(?:归|属于)(?:甲方|乙方|双方)(?:所有|共有)?",
        result_text,
    )) and not ownership_deferred
    interim_use = bool(re.search(
        r"(?:未就知识产权归属|知识产权归属[^。；]{0,30}前)[^。；]{0,80}"
        r"(?:有权|可以)(?:(?:保留并)?继续|保留)?使用",
        compact,
    ))

    change_present = any(term in compact for term in ("需求调整", "需求变更", "变更需求"))
    complete_change_mechanism = (
        any(term in compact for term in ("变更单", "书面变更确认", "变更申请"))
        and "费用" in compact
        and any(term in compact for term in ("工期", "交付时间", "服务周期"))
    )
    actual_workload_basis = bool(re.search(
        r"(?:提前解除|合同提前解除|解除合同)[^。；]{0,80}(?:实际完成的工作量|实际完成程度)|"
        r"(?:实际完成的工作量|实际完成程度)[^。；]{0,80}(?:费用结算|协商确定对应费用)",
        compact,
    ))
    workload_determination_unclear = actual_workload_basis and not any(
        term in compact for term in ("工时记录", "工作量确认单", "里程碑完成比例", "核算公式", "计价标准")
    )

    return {
        "acceptance": {
            "mechanism_present": "验收通知" in acceptance_text or "通知乙方进行验收" in acceptance_text,
            "standard_referenced": "验收标准" in compact,
            "standard_deferred": standard_deferred,
            "standard_concrete": standard_concrete,
            "deadline_defined": bool(re.search(r"收到验收通知后\d+(?:个)?工作日内", acceptance_text)),
            "written_objection": "书面异议" in acceptance_text,
            "deemed_acceptance": bool(re.search(r"未提出书面异议[^。；]{0,40}视为[^。；]{0,30}验收合格", acceptance_text)),
            "remedy_present": any(term in acceptance_text for term in ("问题清单", "完成修改", "整改", "修复")),
            "remedy_deadline_specific": remedy_deadline_specific,
            "remedy_deadline_vague": "合理期限" in acceptance_text and not remedy_deadline_specific,
        },
        "service_generated_result": {
            "scope_defined": bool(result_segments),
            "ownership_deferred": ownership_deferred,
            "ownership_finalized": ownership_finalized,
            "interim_use_arranged": interim_use,
        },
        "liability": {
            "third_party_platform_exception": any(term in compact for term in ("第三方云服务", "第三方平台接口", "电商平台接口故障"))
            and any(term in compact for term in ("不承担责任", "免责")),
            "indirect_loss_exclusion": any(term in compact for term in ("间接", "附带", "惩罚性损失"))
            and any(term in compact for term in ("不负责", "不承担责任", "概不负责")),
            "provider_liability_cap": bool(re.search(
                r"(?:服务提供方|甲方)[^。；]{0,80}(?:累计赔偿责任|赔偿责任)[^。；]{0,80}"
                r"(?:最高不超过|不超过)[^。；]{0,60}(?:已支付|实际支付)[^。；]{0,30}(?:服务费|费用)",
                compact,
            )),
        },
        "change_control": {
            "change_present": change_present,
            "complete_mechanism": complete_change_mechanism,
            "principle_only": change_present and not complete_change_mechanism,
        },
        "termination_settlement": {
            "actual_workload_basis": actual_workload_basis,
            "workload_determination_unclear": workload_determination_unclear,
        },
    }


def _personal_information_processing_analysis(text: str) -> Dict[str, Any]:
    compact = re.sub(r"\s+", "", text or "")
    strong_category_markers = (
        "姓名", "工号", "身份证", "电话号码", "手机号", "电子邮箱", "定位信息",
        "企业邮箱", "生物识别", "收货地址", "联系地址", "员工数据", "用户数据", "消费者数据",
    )
    contextual_category_markers = (
        "操作日志", "行为日志", "用户账号", "个人账号", "系统账号", "系统账号信息", "设备信息", "认证信息",
    )
    category_markers = (*strong_category_markers, *contextual_category_markers)
    segments = [segment for segment in re.split(r"[。；;\n]", text or "") if segment.strip()]
    # Keep the functional data scope separate from an actual entrusted
    # processing relationship.  A system may be designed to process names,
    # phone numbers or addresses without the developer ever receiving or
    # accessing production personal data.
    feature_segments = []
    delegated_processing_segments = []
    active_list_heading = ""
    active_list_remaining = 0
    list_heading_markers = (
        "个人信息包括", "个人数据包括", "信息种类", "数据字段",
        "系统需处理的数据包括", "需处理的数据包括",
    )
    for index, segment in enumerate(segments):
        # A preceding list heading may define the fields in the next paragraph;
        # unrelated company contact details elsewhere in the document must not.
        if any(marker in segment for marker in list_heading_markers):
            active_list_heading = segment
            active_list_remaining = 16
        previous = active_list_heading if active_list_remaining > 0 else ""
        window = previous + segment
        segment_compact = re.sub(r"\s+", "", window)
        administrative_contact = any(marker in segment_compact for marker in (
            "合同联系方式", "项目联系人", "联系信息", "司法送达地址",
            "通过指定电子邮箱", "指定电子邮箱提供资料", "电子邮箱提供资料", "法定代表人或授权代表",
        ))
        segment_categories = [marker for marker in category_markers if marker in segment_compact]
        strong_categories = [marker for marker in strong_category_markers if marker in segment_compact]
        explicit_personal_data = any(marker in segment_compact for marker in (
            "个人信息", "个人数据", "员工信息", "员工数据", "用户信息", "用户数据", "消费者信息", "消费者数据",
        ))
        processing_context = any(marker in segment_compact for marker in (
            "受托处理", "委托处理", "处理", "收集", "存储", "访问", "使用", "传输", "提供", "返还", "删除", "销毁",
        ))
        list_field = bool(active_list_heading and segment_categories)
        functional_personal_data = not administrative_contact and (
            (processing_context and (explicit_personal_data or bool(strong_categories))) or list_field
        )
        if functional_personal_data:
            feature_segments.append(segment_compact)

        explicit_delegation = bool(re.search(
            r"(?:甲方|委托方|客户)?(?:明确)?(?:委托|授权)(?:乙方|服务方|开发方|受托方)[^。；]{0,45}(?:处理|收集|存储|使用|分析|传输)"
            r"[^。；]{0,45}(?:个人信息|个人数据|员工信息|用户信息|客户信息|消费者信息)",
            segment_compact,
        )) or any(marker in segment_compact for marker in (
            "个人信息委托处理", "受托处理个人信息", "受托处理个人数据", "服务方受托处理", "开发方受托处理",
        )) or bool(segment_categories) and any(marker in segment_compact for marker in (
            "委托乙方处理", "乙方受托处理", "授权乙方处理",
            "服务方受托处理", "开发方受托处理", "受托方处理",
        ))
        actual_data_delivery = bool(re.search(
            r"(?:甲方|委托方|客户)[^。；]{0,25}(?:向|提供给|交付给|传输给)乙方[^。；]{0,35}"
            r"(?:个人信息|个人数据|员工信息|用户信息|客户信息|消费者信息|数据可能包括|数据包括)",
            segment_compact,
        )) or bool(re.search(
            r"(?:乙方|服务方|开发方|受托方)[^。；]{0,20}(?:接收|取得|获取)[^。；]{0,35}"
            r"(?:真实数据|生产数据|个人信息|个人数据|员工信息|用户信息|客户信息|消费者信息)",
            segment_compact,
        ))
        production_access = bool(re.search(
            r"(?:乙方|服务方|开发方|受托方)[^。；]{0,30}(?:可以|可|有权|需要|应当|负责)?(?:访问|接入|操作|维护)"
            r"[^。；]{0,35}(?:生产数据库|生产环境|真实数据|个人信息|个人数据)",
            segment_compact,
        ))
        managed_processing = bool(re.search(
            r"(?:乙方|服务方|开发方|受托方)[^。；]{0,30}(?:负责|承担)[^。；]{0,25}"
            r"(?:云端托管|云托管|生产环境运维|数据迁移|数据备份|真实数据测试|生产数据测试)",
            segment_compact,
        ))
        continuing_processing = bool(re.search(
            r"(?:乙方|服务方|开发方|受托方)[^。；]{0,30}(?:持续|日常|定期)?(?:处理|存储|分析|传输)"
            r"[^。；]{0,35}(?:个人信息|个人数据|真实数据|生产数据)",
            segment_compact,
        ))
        if not administrative_contact and (
            explicit_delegation or actual_data_delivery or production_access
            or managed_processing or continuing_processing
        ):
            delegated_processing_segments.append(segment_compact)
        if active_list_heading and segment != active_list_heading:
            active_list_remaining -= 1
            if not segment_categories and not any(marker in segment for marker in ("包括", "如下", "字段")):
                active_list_heading = ""
                active_list_remaining = 0
        if active_list_remaining <= 0:
            active_list_heading = ""
    feature_text = "".join(feature_segments)
    matched_categories = [marker for marker in category_markers if marker in feature_text]
    triggered = bool(delegated_processing_segments)
    control_groups = {
        "purpose": ("处理目的", "使用目的"),
        "scope": ("处理范围", "信息种类", "数据范围"),
        "duration": ("处理期限", "保存期限"),
        "method": ("处理方式", "处理活动"),
        "security": ("安全措施", "加密", "访问控制", "权限控制"),
        "incident": ("安全事件", "数据泄露", "事件通知"),
        "supervision": ("监督", "审计", "检查权"),
        "subprocessing": ("转委托", "再委托", "分包处理"),
        "return_or_delete": ("返还", "归还", "删除", "销毁"),
    }
    controls = {
        key: any(marker in compact for marker in markers)
        for key, markers in control_groups.items()
    }
    missing = [key for key, present in controls.items() if not present]
    return {
        "triggered": triggered,
        "feature_scope_present": bool(feature_segments),
        "delegated_processing_present": triggered,
        "trigger_strength": "STRONG" if triggered else "WEAK" if feature_segments else "NONE",
        "feature_segments": feature_segments,
        "delegated_processing_segments": delegated_processing_segments,
        "matched_categories": matched_categories,
        "controls": controls,
        "missing_controls": missing,
        "gap": triggered and bool(missing),
    }


def analyze_technology_relationship_risks(text: str) -> Dict[str, Dict[str, Any]]:
    compact = re.sub(r"\s+", "", text or "")
    classification = classify_technology_transaction(text)
    payment = analyze_payment_schedule(text)
    timeline = analyze_timeline(text)

    def signal(present: bool, terms: tuple[str, ...], reason: str) -> Dict[str, Any]:
        evidence = [term for term in terms if term in compact]
        return {"present": bool(present), "evidence_terms": evidence, "reason": reason}

    subjective_acceptance = any(term in compact for term in ("实际使用效果", "业务部门认可", "业务部门意见决定是否通过"))
    no_deemed_acceptance = any(term in compact for term in ("不视为验收合格", "不视为通过"))
    unlimited_rectification = any(term in compact for term in ("直至甲方验收合格", "整改直至验收通过"))
    background_overtransfer = classification["involves_background_ip"] and any(
        term in compact for term in ("通用算法、规则模板、技术框架", "既有工具相关改进成果", "规则引擎相关改进成果")
    ) and "甲方所有" in compact
    cumulative_uncapped = "不设最高限额" in compact and any(term in compact for term in ("同时适用", "累计适用"))
    liability_remedies = {
        "daily_fixed": bool(re.search(r"每(?:逾期|超过)?(?:一|1)天[^。；]{0,35}(?:违约金|支付)[^。；]{0,20}(?:元|￥|¥)", compact)),
        "daily_percentage": bool(re.search(r"每(?:逾期|超过)?(?:一|1)天[^。；]{0,40}\d+(?:\.\d+)?%[^。；]{0,20}违约金", compact)),
        "termination_percentage": bool(re.search(r"(?:解除|终止)[^。；]{0,100}\d+(?:\.\d+)?%[^。；]{0,20}违约金|\d+(?:\.\d+)?%[^。；]{0,35}违约金[^。；]{0,35}(?:解除|终止)", compact)),
        "all_losses": "全部损失" in compact,
        "lost_profit": "可得利益" in compact,
        "third_party": any(term in compact for term in ("第三方的赔偿", "第三方赔偿", "支付给第三方")),
        "enforcement_costs": any(term in compact for term in ("律师费", "诉讼费用", "公证费", "调查取证费用")),
    }
    liability_overlap = sum(bool(value) for value in liability_remedies.values()) >= 4 and any(
        term in compact for term in ("同时仍应", "全部损失", "包括但不限于")
    )
    internal_reason_termination = bool(re.search(
        r"(?:预算调整|采购计划变更|项目取消|内部经营调整)[^。；]{0,80}(?:解除|终止)",
        compact,
    ))
    completed_work_excluded = bool(re.search(
        r"(?:仅|只)[^。；]{0,20}(?:验收合格|已经验收)[^。；]{0,30}(?:结算|支付)|"
        r"(?:已经完成|已完成)[^。；]{0,16}(?:尚未验收|未经最终验收)[^。；]{0,25}(?:不计入|不予|不得)(?:结算|支付)",
        compact,
    ))
    unilateral = internal_reason_termination and completed_work_excluded
    forced_change = bool(re.search(
        r"(?:需求调整|需求变更|服务内容调整|工作范围调整)[^。；]{0,100}"
        r"(?:必须先行执行|应先行执行|应当先行配合执行|未达成一致[^。；]{0,25}继续履行)|"
        r"(?:必须先行执行|应先行执行|应当先行配合执行)[^。；]{0,100}"
        r"(?:需求调整|需求变更|服务内容调整|工作范围调整)",
        compact,
    ))
    demand_reduction_exit_cost = bool(
        (
            re.search(r"(?:减少|缩减|调减)[^。；]{0,60}(?:需求|内容|范围|功能|开发软件)", compact)
            or re.search(r"(?:需求|内容|范围|功能|开发软件)[^。；]{0,60}(?:减少|缩减|调减)", compact)
            or re.search(r"(?:项目变更|需求变更)[^。；]{0,40}(?:费用|价款)[^。；]{0,20}(?:下降|减少)", compact)
        )
        and any(term in compact for term in ("另外向", "另行向", "补贴", "补偿"))
        and any(term in compact for term in ("不得低于", "重新协商", "协商不一致", "协商不成", "有权解除"))
    )
    pii_analysis = _personal_information_processing_analysis(text)
    pii_gap = bool(pii_analysis["gap"])
    retention_warranty = _retention_warranty_relationship(text)
    data_retention_conflict = bool(retention_warranty["conflicts"])
    injury_exclusion = "甲方过错" in compact and any(term in compact for term in ("未购买保险", "保险金额不足")) and any(term in compact for term in ("甲方不予赔偿", "甲方不承担责任"))
    short_data_objection = "3个工作日" in compact and any(term in compact for term in ("视为甲方提供的全部资料", "视为全部资料"))
    external_change_free = any(term in compact for term in ("调整业务规则", "修改测试环境", "更新第三方系统", "变更数据结构")) and any(term in compact for term in ("先行完成修正", "无偿修正"))
    return {
        "acceptance_payment_control": signal(subjective_acceptance or no_deemed_acceptance or unlimited_rectification, ("实际使用效果", "业务部门认可", "不视为验收合格", "直至甲方验收合格"), "量化验收标准受到主观决定、沉默不通过或无限整改安排削弱。"),
        "background_ip_overtransfer": signal(background_overtransfer, ("已有", "规则引擎", "通用算法、规则模板、技术框架", "规则引擎相关改进成果", "甲方所有"), "项目成果与服务方背景知识产权未隔离，通用能力可能被一并转让。"),
        "uncapped_cumulative_liability": signal(cumulative_uncapped, ("同时适用", "不设最高限额", "30%的违约金", "0.5%的违约金"), "服务方违约金、退款、赔偿与继续履行可叠加且累计责任无上限。"),
        "cumulative_liability_overlap": {
            **signal(liability_overlap, tuple(key for key, present in liability_remedies.items() if present), "多种违约金、全部损失和实现权利费用可能由同一违约链条触发，并用和抵扣关系不清。"),
            "analysis": liability_remedies,
        },
        "unilateral_termination_change": signal(unilateral or forced_change, ("预算调整", "采购计划变更", "项目取消", "必须先行执行", "继续履行"), "委托方可将内部经营变化和未定价需求变更风险转由服务方承担。"),
        "demand_reduction_exit_cost": signal(demand_reduction_exit_cost, ("减少需求", "下降数额", "另外向", "补贴", "不得低于", "重新协商", "有权解除"), "减少采购内容仍触发额外补偿、最低价款和解除压力，形成需求调整及退出成本。"),
        "personal_information_processing_gap": {
            **signal(pii_gap, tuple(pii_analysis["matched_categories"]), "合同涉及个人信息委托处理，但处理要素、安全事件、监督和终止后处置机制不完整。"),
            "analysis": pii_analysis,
        },
        "payment_formula_inconsistency": signal(payment["status"] == "INCONSISTENT", tuple(), "付款比例、节点金额或合同总价之间存在确定性计算不一致。"),
        "timeline_conflict": signal(
            bool(timeline["conflicts"]),
            tuple(),
            "技术资料交付义务早于合同生效日，生效前履行边界不清。"
            if timeline.get("primary_conflict_subject") == "TECHNICAL_MATERIAL_DELIVERY"
            else "服务开始义务早于合同生效日，生效前履行边界不清。"
            if timeline.get("primary_conflict_subject") == "SERVICE_START"
            else "履行义务早于合同生效日，生效前履行边界不清。",
        ),
        "data_retention_warranty_conflict": {
            **signal(data_retention_conflict, ("归还", "返还", "删除", "销毁", "保证期", "质保期", "保修期"), "资料删除期限早于保证期结束，可能妨碍缺陷复现和保证义务履行。"),
            "analysis": retention_warranty,
        },
        "personal_injury_liability_exclusion": signal(injury_exclusion, ("甲方过错", "未购买保险", "保险金额不足", "甲方不予赔偿"), "甲方对自身过错造成的人身损害排除未投保或保险不足部分责任，可能存在效力风险。"),
        "short_data_objection_deemed_acceptance": signal(short_data_objection, ("3个工作日", "视为甲方提供的全部资料"), "资料异议期限过短且逾期视为全部合格，可能削弱乙方顺延及抗辩权。"),
        "external_change_free_remediation": signal(external_change_free, ("调整业务规则", "修改测试环境", "更新第三方系统", "变更数据结构", "先行完成修正"), "甲方或外部环境变化仍由乙方先行无偿修正，保证责任范围过宽。"),
    }


def analyze_technical_service_risks(text: str) -> Dict[str, Dict[str, Any]]:
    """Backward-compatible alias for callers that predate the shared relationship layer."""
    return analyze_technology_relationship_risks(text)
