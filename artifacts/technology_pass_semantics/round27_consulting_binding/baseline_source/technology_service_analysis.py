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
SCALED_CNY_PATTERN = r"(?P<amount>[0-9][0-9,]*(?:\.\d+)?)\s*(?P<unit>万)?\s*元"
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


def _scaled_cny(amount: str, unit: Optional[str] = None) -> Decimal:
    """Return a CNY amount while preserving source-level ``万元`` notation."""
    value = _decimal(amount)
    return value * Decimal("10000") if unit == "万" else value


def _iso(match: re.Match[str]) -> str:
    return date(int(match.group(1)), int(match.group(2)), int(match.group(3))).isoformat()


def _without_negated_rights_disposals(text: str) -> str:
    """Remove prohibitions/disclaimers before detecting affirmative transfers."""

    return re.sub(
        r"(?:无权|不得|禁止|不可|不应|不能|未经[^。；]{0,20}(?:同意|许可)[^。；]{0,8}不得)"
        r"[^。；]{0,45}(?:转让|让与|转移|处分)"
        r"[^。；]{0,35}(?:专利权|专利申请权|技术成果所有权|技术权利)",
        "",
        text or "",
    )


def _structured_entrusted_development(text: str) -> Dict[str, Any]:
    """Recognize a research commission expressed across form-contract articles.

    A client/developer relationship, a funded research programme, its developer's
    performance and delivery of research results must all be present. Ordinary
    deployment, model-training and support vocabulary is not enough.
    """
    compact = re.sub(r"\s+", "", text or "")
    articles = re.split(r"(?=第[一二三四五六七八九十百\d]+条)", compact)
    roles = bool(
        re.search(r"(?:委托方|委托人)[（(]?甲方|甲方[（(]?(?:委托方|委托人)", compact)
        and re.search(
            r"(?:受托方|研究开发人|开发方)[（(]?乙方|乙方[（(]?(?:受托方|研究开发人|开发方)",
            compact,
        )
    )
    objectives = any(
        re.search(r"(?:研究开发要求|研究开发目标|研发目标|开发目标|技术目标)[：:]?", article)
        and re.search(r"(?:研发|研究开发|开发)(?:一[套种项个])?[^。；]{2,100}(?:系统|算法|技术|产品|工艺|装置|材料)", article)
        for article in articles
    )
    funding = any(
        re.search(r"(?:研究开发经费|研发经费|研发费用|开发费用|开发费)(?:和|及|与)?(?:报酬)?", article)
        and re.search(r"(?:总额|总价|费用|经费|报酬)[：:]?(?:人民币)?[\d,]+(?:\.\d+)?(?:万)?元", article)
        and any(term in article for term in ("支付", "付款", "结算"))
        for article in articles
    )
    # Do not interpret a prohibition on outsourcing as the developer's positive
    # undertaking; this check stays within the same sentence and party.
    performance = bool(re.search(
        r"(?:乙方|受托方|研究开发人|开发方)(?:(?!甲方|不得|禁止|无须|不承担)[^。；]){0,65}"
        r"(?:负责|承担|开展|实施|完成|提交)[^。；]{0,35}(?:研究开发|研发|开发工作)",
        compact,
    ))
    schedule = bool(
        re.search(r"研究开发计划|研发计划|研发进度|开发进度|开发里程碑", compact)
    )
    results = bool(re.search(
        r"(?:提交|交付)[^。；]{0,35}(?:研究开发成果|研发成果|开发成果)|"
        r"(?:研究开发成果|研发成果|开发成果)[^。；]{0,45}(?:交付|提交|形成并向甲方)",
        compact,
    ))
    bilateral_tasks = all(bool(re.search(
        rf"{party}(?:(?!{'乙方' if party == '甲方' else '甲方'})[^。；]){{0,65}}"
        r"(?:负责|承担)[^。；]{0,30}(?:研发|研究开发|开发)",
        compact,
    )) for party in ("甲方", "乙方"))
    facts = {
        "client_and_developer_roles": roles,
        "research_objectives": bool(objectives),
        "research_consideration": bool(funding),
        "developer_research_performance": performance,
        "research_schedule": schedule,
        "research_result_delivery": results,
    }
    return {
        **facts,
        "is_primary_commission": all(facts.values()) and not bilateral_tasks,
    }


def analyze_primary_transaction(text: str) -> Dict[str, Any]:
    """Classify the exchanged legal/economic performance, not word frequency."""
    source = text or ""
    compact = re.sub(r"\s+", "", source)
    sentences = [row for row in re.split(r"[。；;\n]+", source) if row.strip()]
    operative_sentences = [row for row in sentences if not any(term in row for term in ("另行购买", "另行采购", "另行签署", "另行订立", "具体供货另行"))]
    operative = re.sub(r"\s+", "", "。".join(operative_sentences))
    affirmative_operative = _without_negated_rights_disposals(operative)
    development_semantics = _structured_entrusted_development(source)

    license_grant = bool(re.search(
        r"(?:许可|授予)[^。；]{0,45}(?:技术|技术资料|制造工艺|源程序|软件|专利)[^。；]{0,45}(?:使用|实施|设计|制造|销售|出口)?|"
        r"(?:技术|技术资料|制造工艺|源程序|软件|专利)[^。；]{0,45}(?:许可|授予)[^。；]{0,30}(?:使用|实施)|"
        r"许可方式[：:]?(?:普通|排他|独占|非独占)(?:实施)?许可.{0,120}(?:技术秘密名称|专有技术名称|非专利技术名称)|"
        r"(?:技术秘密名称|专有技术名称|非专利技术名称).{0,120}许可方式[：:]?(?:普通|排他|独占|非独占)(?:实施)?许可",
        operative,
    ))
    licensee_role_present = any(term in compact for term in (
        "被许可方", "被许可人", "接受方", "受许可方",
    ))
    license_roles = (
        (any(term in compact for term in ("许可方", "许可人")) and licensee_role_present)
        or ("出让方" in compact and "受让方" in compact and license_grant)
    )
    license_boundaries = {
        "license_mode": any(term in compact for term in ("非独占", "独占许可", "排他许可", "普通许可")),
        "non_transferable": any(term in compact for term in ("不可转让", "不得转让", "不得再许可")),
        "territory": any(term in compact for term in (
            "许可地域", "约定区域", "中华人民共和国境内", "中华人民共和国大陆地区", "地域范围",
        )),
        "use_scope": bool(re.search(
            r"(?:有权|许可|仅可|可以)[^。；]{0,80}(?:设计|研发|生产|制造|使用|销售|出口|实施|复制|编译)",
            operative,
        )),
        "post_termination_use": any(term in compact for term in ("终止后继续使用", "合同终止后技术使用", "永久继续使用")),
    }
    license_scope_count = sum(bool(value) for value in license_boundaries.values())
    royalty = bool(
        any(term in compact for term in (
            "提成费", "销售提成", "royalty", "许可使用费", "技术秘密使用费", "技术秘密许可费",
        ))
        or re.search(r"(?:净销售额|销售额)[^。；]{0,40}\d+(?:\.\d+)?%", compact, re.IGNORECASE)
    )
    entry_fee = any(term in compact for term in (
        "入门费", "技术许可费", "许可费总额", "基础技术许可", "技术秘密使用费总额", "技术秘密许可费总额",
    ))
    technical_delivery = sum(
        term in compact for term in (
            "技术资料", "技术秘密资料清单", "PLC源程序", "源代码", "算法",
            "控制参数", "测试数据", "接口说明", "制造工艺", "故障诊断技术",
            "设计资料", "技术指导", "人员培训",
        )
    ) >= 2
    independent_license_value = bool(
        license_grant
        and (royalty or entry_fee or "许可使用费" in compact)
        and (license_scope_count >= 1 or license_roles)
    )
    # A project-result ownership allocation (for example, “成果归甲方所有”)
    # is not itself a transaction transferring pre-existing technology.  Require
    # an operative disposal verb so service/development ownership clauses do not
    # get promoted to a technology-transfer primary transaction.
    explicit_technology_rights_transfer = bool(re.search(
        r"(?:完整|全部|整体)(?:的)?(?:非专利)?技术(?:成果)?(?:权利)?转让|"
        r"(?:受让方|甲方)[^。；]{0,45}(?:取得|受让|承接)[^。；]{0,35}(?:本合同|标的)?(?:非专利)?技术(?:相关)?(?:全部)?权利|"
        r"(?:本合同|标的)(?:价款)?支付完成后[^。；]{0,35}(?:受让方|甲方)[^。；]{0,20}取得[^。；]{0,30}技术(?:相关)?权利|"
        r"(?:非专利技术|技术秘密|专有技术)[^。；]{0,45}(?:全部权利|整体权利)[^。；]{0,25}(?:转移|转让|归属)",
        affirmative_operative,
    ))
    technology_disposal = bool(explicit_technology_rights_transfer or re.search(
        r"(?:专利权|专利申请权|技术成果所有权)[^。；]{0,40}(?:转让给|转移至)|"
        r"(?:转让|让与)[^。；]{0,30}(?:专利权|专利申请权|技术成果所有权)",
        affirmative_operative,
    ))
    technical_secret_disposal = bool(
        (
            any(term in compact[:300] for term in (
                "技术转让（技术秘密）合同", "技术转让(技术秘密)合同", "技术秘密转让合同",
                "非专利技术转让合同",
            ))
            or re.search(
                r"(?:转让方|让与方|乙方)[^。；]{0,60}(?:向|给)(?:受让方|甲方)[^。；]{0,60}"
                r"(?:转让|交付|提供)[^。；]{0,45}(?:技术秘密|非公开技术|专有技术)|"
                r"(?:本合同|转让标的|标的技术)[^。；]{0,60}(?:为|包括|系)[^。；]{0,45}技术秘密",
                operative,
            )
        )
        and any(term in compact for term in (
            "固定技术转让费", "技术转让费", "技术转让价款", "转让总价", "技术交易额", "成交总额",
        ))
    ) or bool(
        explicit_technology_rights_transfer
        and ("非专利技术" in compact or "技术秘密" in compact or "专有技术" in compact)
        and any(term in compact for term in ("技术转让价款", "技术转让费", "技术交易额", "成交总额"))
    )
    technology_ownership_transfer = bool(
        (technology_disposal or technical_secret_disposal)
        and (
            any(term in compact[:300] for term in (
                "技术转让合同", "技术转让（技术秘密）合同", "技术转让(技术秘密)合同",
                "技术秘密转让合同", "非专利技术转让合同", "专利权转让合同", "专利申请权转让合同",
            ))
            or (("让与方" in compact or "转让方" in compact) and "受让方" in compact)
            or any(term in compact for term in (
                "技术转让价款", "固定技术转让费", "技术转让费", "专利权转让价款",
                "专利申请权转让价款", "转让总价", "技术交易额", "成交总额",
            ))
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
    elif development_semantics["is_primary_commission"]:
        transaction_type = "ENTRUSTED_DEVELOPMENT"
        dominant_family = "TECHNOLOGY"
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
            "technical secret / know-how"
            if transaction_type == "TECHNOLOGY_TRANSFER" and technical_secret_disposal
            else "patent or technical-result ownership" if transaction_type == "TECHNOLOGY_TRANSFER"
            else "technology / know-how / technical materials" if transaction_type == "TECHNOLOGY_LICENSE"
            else "goods and technology license" if transaction_type.startswith("MIXED_")
            else "new research and development results" if transaction_type == "ENTRUSTED_DEVELOPMENT"
            else "goods" if transaction_type == "GOODS_SALE" else "undetermined"
        ),
        "rights_change": (
            (["ownership/control of technical secret transfers"] if technical_secret_disposal else
             ["ownership of patent or technical result transfers"] if technology_ownership_transfer else [])
            + (["license to use technology"] if independent_license_value and not technology_ownership_transfer else [])
        ) + (["ownership of goods transfers to buyer"] if independent_sale_value else []),
        "primary_obligation_grantor": (
            ["perform commissioned research and deliver development results"]
            if transaction_type == "ENTRUSTED_DEVELOPMENT" else license_obligations + sale_obligations
        ),
        "primary_obligation_grantee": (
            ["fund research and pay development remuneration"]
            if transaction_type == "ENTRUSTED_DEVELOPMENT" else grantee_obligations + sale_buyer_obligations
        ),
        "primary_consideration": (
            (["entry fee"] if entry_fee else [])
            + (["sales royalty"] if royalty else [])
            + (["goods purchase price"] if independent_sale_value else [])
            + (["research funding and development remuneration"] if transaction_type == "ENTRUSTED_DEVELOPMENT" else [])
        ),
        "transaction_purpose": (
            "acquire ownership or control of technical secret/non-patent technology"
            if technology_ownership_transfer and technical_secret_disposal
            else "acquire ownership of patent or technical result"
            if technology_ownership_transfer
            else "use licensed technology to manufacture or operate products" if independent_license_value
            else "commission research and obtain new development results" if transaction_type == "ENTRUSTED_DEVELOPMENT"
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
        "technology_transfer_semantics": {
            "ownership_transfer": technology_ownership_transfer,
            "technical_secret_transfer": technical_secret_disposal,
            "explicit_technology_rights_transfer": explicit_technology_rights_transfer,
        },
        "sale_semantics": {
            "ownership_transfer": ownership_transfer,
            "roles": sale_roles,
            "quantity_unit_price": goods_quantity_price,
            "goods_purchase_obligation": goods_purchase,
            "purchase_price": purchase_price,
            "independent_economic_value": independent_sale_value,
            "ancillary_future_supply": ancillary_goods_supply,
        },
        "development_semantics": development_semantics,
        "family_scores": {
            "TECHNOLOGY": license_score + (18 if transaction_type == "ENTRUSTED_DEVELOPMENT" else 0),
            "SALE": sale_score,
        },
        "decision_basis": "operative rights change + primary obligations + consideration + economic independence",
    }


def _classify_technology_transaction_uncached(text: str) -> Dict[str, Any]:
    source_text = text or ""
    compact = re.sub(r"\s+", "", source_text)
    affirmative_compact = _without_negated_rights_disposals(compact)
    primary_transaction_model = analyze_primary_transaction(source_text)
    source_lines = [line.strip() for line in source_text.splitlines() if line.strip()]
    # Cover-page fields often precede the actual title.  Search the opening
    # block for a concise title instead of assuming the first non-empty line is
    # always the title.
    document_title = next(
        (
            line for line in source_lines[:30]
            if len(re.sub(r"\s+", "", line)) <= 60
            and re.search(r"(?:合同|协议)$", re.sub(r"\s+", "", line))
            and not re.match(r"^(?:第.+条|\d+(?:\.\d+)*)", line)
        ),
        source_lines[0] if source_lines else "",
    )
    title_compact = re.sub(r"\s+", "", document_title)
    service_signals = (
        "技术服务合同",
        "解决特定技术问题",
        "技术服务内容",
        "技术服务费用",
        "技术服务报酬",
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
    technical_secret_transfer_title = (
        technology_transfer_title
        and any(term in title_compact for term in ("技术秘密", "专有技术", "非公开技术", "非专利技术"))
    )
    patent_license_title = (
        "合同" in title_compact
        and any(term in title_compact for term in (
            "专利实施许可", "专利技术许可", "技术许可（专利实施）", "技术许可(专利实施)",
        ))
    )
    technology_license_title = "合同" in title_compact and any(
        term in title_compact for term in ("技术许可", "技术秘密许可", "专有技术许可", "非专利技术许可")
    )
    technical_secret_license_fields = bool(
        re.search(r"许可方式[：:]?(?:普通|排他|独占|非独占)(?:实施)?许可", compact)
        and any(term in compact for term in ("技术秘密名称", "专有技术名称", "非专利技术名称"))
        and any(term in compact for term in ("许可人", "许可方"))
        and any(term in compact for term in ("被许可人", "被许可方"))
    )
    technical_secret_license_title = (
        "合同" in title_compact
        and any(term in title_compact for term in ("技术秘密许可", "专有技术许可", "非专利技术许可"))
    ) or technical_secret_license_fields
    consulting_title = "合同" in title_compact and "技术咨询" in title_compact
    service_title = "合同" in title_compact and "技术服务" in title_compact
    entrusted_title = bool(re.search(
        r"委托(?:研究)?开发|技术开发[（(]委托[）)]|技术开发(?:合同|协议)[（(]委托[）)]",
        title_compact,
    ))

    # A grant is an operative proposition, never text assembled across
    # warranty/remedy/third-party-claim sentences or article boundaries.
    from review_v2.proposition_scope import arrangement_matches
    patent_grant_pattern = (
        r"(?:许可人|许可方|卖方|乙方)[^。；;\n]{0,60}(?:许可|授予)[^。；;\n]{0,80}"
        r"(?:被许可人|被许可方|接受方|受许可方|买方|甲方)[^。；;\n]{0,80}"
        r"(?:实施|使用|制造|销售)[^。；;\n]{0,30}专利|"
        r"(?:许可|授予)[^。；;\n]{0,50}(?:专利实施许可|实施其所拥有的[^。；;\n]{0,40}专利)"
    )
    patent_license_grant = any(
        not re.search(r"第三方.{0,12}(?:主张|声称)|无权许可|未获授权", row['quote'])
        for row in arrangement_matches(patent_grant_pattern, re.sub(r'[^\S\n]+', '', source_text))
    )
    license_consideration = any(term in compact for term in (
        "专利许可费", "实施许可使用费", "许可使用费", "许可费总额", "许可使用费总额",
    ))
    license_scope = any(term in compact for term in (
        "排他许可", "独占许可", "普通许可", "许可范围", "许可期限", "许可地域", "再许可",
    ))
    patent_ownership_transfer = bool(re.search(
        r"(?:转让|让与).{0,30}(?:专利权|专利申请权)|(?:专利权|专利申请权).{0,30}(?:转让|让与|转移至|归受让方所有)",
        affirmative_compact,
    ))
    transfer_registration = bool(re.search(
        r"(?:专利权.{0,30}(?:转让登记|变更登记|登记至受让方|登记转移)|(?:申请人|专利申请权).{0,30}(?:变更登记|变更))",
        compact,
    ))
    transfer_consideration = any(term in compact for term in (
        "专利权转让价款", "专利权转让总价", "专利权转让费", "技术转让价款",
        "固定技术转让费", "技术转让费", "转让总价", "技术交易额", "成交总额",
    ))
    explicit_technology_rights_transfer = bool(re.search(
        r"(?:完整|全部|整体)(?:的)?(?:非专利)?技术(?:成果)?(?:权利)?转让|"
        r"(?:受让方|甲方).{0,45}(?:取得|受让|承接).{0,35}(?:本合同|标的)?(?:非专利)?技术(?:相关)?(?:全部)?权利|"
        r"(?:本合同|标的)(?:价款)?支付完成后.{0,35}(?:受让方|甲方).{0,20}取得.{0,30}技术(?:相关)?权利|"
        r"(?:非专利技术|技术秘密|专有技术).{0,45}(?:全部权利|整体权利).{0,25}(?:转移|转让|归属)",
        affirmative_compact,
    ))
    granted_patent_asset = (
        "专利权" in compact
        and any(term in compact for term in ("已取得授权", "当前专利权人", "授权日", "授权公告号"))
    )
    # A reference to a future improvement's patent application right does not
    # make the current transaction a patent-application-right transfer. The
    # application right must itself be the operative transfer subject.
    patent_application_asset = bool(
        "专利申请权转让" in title_compact
        or re.search(
            r"(?:本合同|转让标的|标的资产)[^。；]{0,70}(?:专利申请权|尚未授权专利申请)|"
            r"(?:转让方|让与方|乙方)[^。；]{0,50}(?:转让|让与)[^。；]{0,30}专利申请权|"
            r"专利申请权[^.。；]{0,35}(?:一并)?转让(?:给|至)?(?:受让方|甲方)?|"
            r"专利申请权[^.。；]{0,35}(?:转让登记|变更登记|变更至受让方)",
            compact,
        )
        or (
            any(term in compact for term in ("当前申请人", "专利申请人"))
            and any(term in compact for term in ("专利申请权转让价款", "专利申请权转让总价"))
        )
    )
    from review_v2.technology_asset_identity import transfer_assets
    transfer_asset_facts = transfer_assets(text)
    registered_patent_transfer = bool(patent_ownership_transfer
        and transfer_asset_facts['patent_identifier']
        and (transfer_asset_facts['patent_grant'] or transfer_asset_facts['patent_registration']))
    granted_patent_asset = granted_patent_asset or registered_patent_transfer
    if patent_application_asset and "转让价款" in compact:
        transfer_consideration = True

    technical_secret_transfer = bool(
        technical_secret_transfer_title
        or (
            explicit_technology_rights_transfer
            and ("非专利技术" in compact or "技术秘密" in compact or "专有技术" in compact)
            and transfer_consideration
        )
        or (
            any(term in compact for term in (
                "技术秘密的内容和范围", "转让技术秘密的内容", "技术秘密交付",
                "非公开技术资料", "专有技术资料",
            ))
            and (("转让方" in compact or "让与方" in compact) and "受让方" in compact)
            and transfer_consideration
        )
        or re.search(
            r"(?:转让方|让与方|乙方).{0,60}(?:向|给)(?:受让方|甲方).{0,60}"
            r"(?:转让|交付|提供).{0,45}(?:技术秘密|非公开技术|专有技术)",
            compact,
        )
    )

    if registered_patent_transfer:
        # Confidential supporting documents cannot displace an operative,
        # identified registered patent. A distinct secret grant remains a module.
        technical_secret_transfer = bool(transfer_asset_facts['secret_transaction'])

    add("TECHNOLOGY_TRANSFER", 12, "title:patent_right_transfer", patent_transfer_title)
    add("TECHNOLOGY_TRANSFER", 8, "title:technology_transfer", technology_transfer_title and not patent_transfer_title)
    add("TECHNOLOGY_TRANSFER", 8, "roles:transferee_transferor", "受让方" in compact and ("让与方" in compact or "让与人" in compact))
    add("TECHNOLOGY_TRANSFER", 8, "roles:transferee_transferor", "受让方" in compact and "转让方" in compact)
    add("TECHNOLOGY_TRANSFER", 6, "effect:registration_transfers_patent_right", bool(re.search(r"专利权.{0,18}登记.{0,12}(?:转移|转让)", compact)))
    add("TECHNOLOGY_TRANSFER", 5, "consideration:transfer_price", "专利权转让价款" in compact)
    add("TECHNOLOGY_TRANSFER", 3, "transfer_terms", any(signal in compact for signal in transfer_signals))
    add("TECHNOLOGY_TRANSFER", 10, "core_obligation:patent_ownership_transfer", patent_ownership_transfer and (transfer_registration or transfer_consideration))
    add("TECHNOLOGY_TRANSFER", 16, "title:technical_secret_transfer", technical_secret_transfer_title)
    add("TECHNOLOGY_TRANSFER", 12, "core_obligation:technical_secret_transfer", bool(technical_secret_transfer and transfer_consideration))
    add("TECHNOLOGY_TRANSFER", 14, "core_effect:technology_rights_transfer", explicit_technology_rights_transfer and transfer_consideration)

    add("TECHNICAL_SERVICE", 12, "title:technical_service", service_title)
    add("TECHNICAL_SERVICE", 6, "service_obligation", any(signal in compact for signal in service_signals[1:]))
    technical_service_activity_terms = (
        "系统部署", "系统调试", "技术调试", "参数调试", "参数优化", "算法优化",
        "设备维护", "设备监测", "状态监测", "故障诊断", "故障排查", "预测性维护",
        "运行维护", "技术支持", "技术优化", "数据建模", "模型训练", "性能优化",
    )
    technical_service_activity_hits = [
        term for term in technical_service_activity_terms if term in compact
    ]
    technical_service_deliverable = bool(re.search(
        r"(?:提交|交付|形成|提供).{0,35}(?:技术|系统|项目|实施|优化|测试|诊断)?"
        r"(?:报告|模型|算法|参数文件|测试记录|操作手册|系统手册)",
        compact,
    ))
    add(
        "TECHNICAL_SERVICE", 8, "core_obligation:technical_operation_and_problem_solving",
        len(technical_service_activity_hits) >= 2,
    )
    add(
        "TECHNICAL_SERVICE", 4, "deliverable:technical_service_result",
        technical_service_deliverable and bool(technical_service_activity_hits),
    )
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
    add("ENTRUSTED_DEVELOPMENT", 4, "title:entrusted_development", entrusted_title or "委托开发" in heading)
    add(
        "ENTRUSTED_DEVELOPMENT", 18, "primary_transaction:funded_research_and_result_delivery",
        primary_transaction_model["type"] == "ENTRUSTED_DEVELOPMENT",
    )
    add("ENTRUSTED_DEVELOPMENT", 8, "directed_research_commission", directed_commission)
    add("ENTRUSTED_DEVELOPMENT", 6, "asymmetric_development_funding", one_party_funds and not (party_a_invests and party_b_invests))
    add("ENTRUSTED_DEVELOPMENT", 6, "asymmetric_research_performance", one_party_develops and not (party_a_develops and party_b_develops))
    add("ENTRUSTED_DEVELOPMENT", 2, "entrusted_wording", any(signal in compact for signal in entrusted_signals))
    add("TECHNOLOGY_LICENSE", 16, "title:patent_license", patent_license_title)
    add("TECHNOLOGY_LICENSE", 12, "title:technology_license", technology_license_title and not patent_license_title)
    add(
        "TECHNOLOGY_LICENSE", 12, "cover_fields:technical_secret_license",
        technical_secret_license_fields and not patent_license_title,
    )
    add(
        "TECHNOLOGY_LICENSE",
        6,
        "current_license_transaction",
        any(term in compact for term in ("许可方", "许可人"))
        and any(term in compact for term in ("被许可方", "被许可人", "接受方", "受许可方"))
        and any(term in compact for term in (
            "许可方式", "许可范围", "许可期限", "授予", "专利许可费", "技术秘密使用费",
        )),
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
        else "ENTRUSTED_DEVELOPMENT" if entrusted_title
        else ""
    )
    ranked = sorted(scores, key=lambda key: scores[key], reverse=True)
    if patent_ownership_transfer or explicit_technology_rights_transfer or primary_transaction_model["type"] == "TECHNOLOGY_TRANSFER":
        subtype = "TECHNOLOGY_TRANSFER"
    elif primary_transaction_model["type"] in {"TECHNOLOGY_LICENSE", "MIXED_SALE_TECHNOLOGY_LICENSE"}:
        subtype = "TECHNOLOGY_LICENSE"
    elif primary_transaction_model["type"] == "GOODS_SALE":
        subtype = "GENERAL_TECHNOLOGY"
    elif primary_transaction_model["type"] == "ENTRUSTED_DEVELOPMENT":
        subtype = "ENTRUSTED_DEVELOPMENT"
    else:
        subtype = explicit_title_subtype or (ranked[0] if scores[ranked[0]] >= 6 else "GENERAL_TECHNOLOGY")
    tertiary_subtype = (
        "PATENT_RIGHT_TRANSFER"
        if subtype == "TECHNOLOGY_TRANSFER" and registered_patent_transfer and not patent_application_asset
        else
        "TECHNICAL_SECRET_TRANSFER"
        if subtype == "TECHNOLOGY_TRANSFER" and technical_secret_transfer
        else "MIXED_PATENT_RIGHT_AND_APPLICATION_TRANSFER"
        if subtype == "TECHNOLOGY_TRANSFER" and granted_patent_asset and patent_application_asset
        else "PATENT_APPLICATION_RIGHT_TRANSFER"
        if subtype == "TECHNOLOGY_TRANSFER" and patent_application_asset
        else "PATENT_RIGHT_TRANSFER"
        if subtype == "TECHNOLOGY_TRANSFER" and (patent_transfer_title or patent_ownership_transfer or granted_patent_asset) and not technical_secret_transfer
        else "PATENT_LICENSE"
        if subtype == "TECHNOLOGY_LICENSE" and (
            patent_license_title
            or patent_license_grant
            or (
                bool(re.search(r"专利号[：:]?(?:ZL|CN)", compact, re.I))
                and any(term in compact for term in ("专利许可费", "排他实施许可", "独占实施许可"))
            )
            or (
                primary_transaction_model["type"] in {"TECHNOLOGY_LICENSE", "MIXED_SALE_TECHNOLOGY_LICENSE"}
                and any(term in compact for term in ("专利技术", "专利编号", "专利实施"))
                and not any(term in compact for term in ("技术秘密许可", "专有技术许可", "非专利技术许可"))
            )
        )
        else "TECHNICAL_SECRET_LICENSE"
        if subtype == "TECHNOLOGY_LICENSE" and (
            technical_secret_license_title
            or bool(re.search(
                r"(?:许可|授予)[^。；]{0,50}(?:技术秘密|专有技术|非专利技术)|"
                r"(?:技术秘密|专有技术|非专利技术)[^。；]{0,50}(?:许可|使用权)",
                compact,
            ))
        )
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
    # Incidental words such as "技术指标", "项目验收" or a prohibition on
    # later development do not create a commissioned-development subtransaction.
    # A secondary development module needs an operative development performance:
    # either the developer/funder relationship itself, or a separately priced
    # development deliverable.  This keeps the primary service route exclusive
    # unless the contract really contains a mixed transaction.
    commissioned_core = (
        "developer_and_funder" in commissioned_development_evidence
        or {
            "development_fee", "development_results",
        }.issubset(set(commissioned_development_evidence))
    )
    has_commissioned_development = (
        len(commissioned_development_evidence) >= 3
        and commissioned_core
        and "开发" in compact
    )

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
    sub_transactions = list(subtransaction_analysis.get("sub_transactions") or [])
    if tertiary_subtype in {"TECHNICAL_SECRET_TRANSFER", "TECHNICAL_SECRET_LICENSE"}:
        if "technical_secret" not in sub_transactions:
            sub_transactions.append("technical_secret")
        secret_facts = dict(structured_subfacts.get("technical_secret") or {})
        secret_facts.update({
            "scope": True,
            "transfer_transaction": tertiary_subtype == "TECHNICAL_SECRET_TRANSFER",
            "license_transaction": tertiary_subtype == "TECHNICAL_SECRET_LICENSE",
            "separate_fee": bool(
                transfer_consideration
                or re.search(r"技术秘密(?:许可)?使用费", compact)
            ),
        })
        structured_subfacts["technical_secret"] = secret_facts
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
        ("TECHNOLOGY_TRANSFER", "TECHNICAL_SECRET_TRANSFER"): "technology_transfer_technical_secret",
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
        "TECHNOLOGY_TRANSFER" if (
            (patent_ownership_transfer and (transfer_registration or transfer_consideration))
            or (explicit_technology_rights_transfer and transfer_consideration)
            or (
                primary_transaction_model["type"] == "TECHNOLOGY_TRANSFER"
                and transfer_consideration
                and not (
                    patent_license_grant
                    and license_consideration
                    and not transfer_registration
                )
            )
        )
        else "TECHNOLOGY_LICENSE" if (
            patent_license_grant and (license_consideration or license_scope)
            or primary_transaction_model["type"] in {"TECHNOLOGY_LICENSE", "MIXED_SALE_TECHNOLOGY_LICENSE"}
        )
        else "ENTRUSTED_DEVELOPMENT" if primary_transaction_model["type"] == "ENTRUSTED_DEVELOPMENT"
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
        "subject_matter": snippets(("专利名称", "项目名称", "合同标的", "许可实施的专利权", "转让的专利权", "技术秘密", "非公开技术", "专有技术", "非专利技术")),
        "core_performance_obligations": snippets(("许可买方实施", "授予本专利实施许可", "转让给受让方", "向受让方提供", "技术秘密交付", "转移至受让方", "完整技术转让", "取得本合同技术相关权利", "共同研究开发", "委托研究开发", "研究开发要求", "提交研究开发计划", "研究开发成果", "解决特定技术问题", "可行性分析", "技术论证", "分析评价", "技术咨询报告")),
        "rights_transfer_method": snippets(("排他许可", "独占许可", "普通实施许可", "专利权转让", "技术秘密转让", "非专利技术转让", "完整技术转让", "取得本合同技术相关权利", "技术秘密交付", "转让登记", "变更登记")),
        "consideration_nature": snippets(("许可使用费", "实施许可使用费", "专利权转让价款", "固定技术转让费", "技术转让费", "技术转让价款", "技术交易额", "成交总额", "技术服务费用", "研究开发经费", "研发经费", "研发费用", "咨询报酬")),
        "key_clauses": snippets(("许可范围", "许可期限", "专利权登记", "权利瑕疵", "开发成果", "咨询报告", "咨询内容", "咨询要求", "技术服务内容"), 8),
    }

    personal_information_analysis = _personal_information_processing_analysis(text)
    university_data = any(term in compact for term in ("高校", "大学", "科研数据", "科研项目", "科研管理数据"))
    research_data_governance_service = (
        subtype == "TECHNICAL_SERVICE"
        and any(term in compact for term in ("科研数据", "科研管理数据", "科研项目数据"))
        and any(term in compact for term in ("数据治理", "数据标准", "字段映射", "数据质量", "敏感字段"))
    )
    enterprise_system_performance_service = (
        subtype == "TECHNICAL_SERVICE"
        and any(term in compact for term in ("ERP系统", "企业信息系统", "业务系统"))
        and sum(term in compact for term in (
            "性能诊断", "数据库分析", "数据库优化", "SQL优化", "参数优化", "性能测试",
        )) >= 2
    )
    transaction_structure = (
        "B2B_PATENT_LICENSE_WITH_COMMISSIONED_DEVELOPMENT"
        if tertiary_subtype == "PATENT_LICENSE" and "COMMISSIONED_DEVELOPMENT" in secondary_modules
        else "B2B_PATENT_LICENSE"
        if tertiary_subtype == "PATENT_LICENSE"
        else "MIXED_SALE_TECHNOLOGY_LICENSE"
        if primary_transaction_model["type"] == "MIXED_SALE_TECHNOLOGY_LICENSE"
        else "B2B_TECHNICAL_SECRET_LICENSE"
        if tertiary_subtype == "TECHNICAL_SECRET_LICENSE"
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
        else "B2B_TECHNICAL_SECRET_TRANSFER"
        if tertiary_subtype == "TECHNICAL_SECRET_TRANSFER"
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
        if research_data_governance_service
        else "ENTERPRISE_INFORMATION_SYSTEM_PERFORMANCE_OPTIMIZATION_SERVICE"
        if enterprise_system_performance_service
        else "UNIVERSITY_TECH_ACHIEVEMENT_AGREEMENT_TRANSFER"
        if tertiary_subtype == "PATENT_RIGHT_TRANSFER" and university_data and "协议定价" in compact
        else "TECHNICAL_SECRET_LICENSE"
        if tertiary_subtype == "TECHNICAL_SECRET_LICENSE"
        else "TECHNOLOGY_LICENSE"
        if subtype == "TECHNOLOGY_LICENSE"
        else "TECHNICAL_SECRET_TRANSFER"
        if tertiary_subtype == "TECHNICAL_SECRET_TRANSFER"
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
        if research_data_governance_service
        else "ERP系统性能诊断与数据库优化技术服务"
        if enterprise_system_performance_service
        else "高校科技成果向企业协议转让"
        if tertiary_subtype == "PATENT_RIGHT_TRANSFER" and university_data and "协议定价" in compact
        else "技术秘密许可"
        if tertiary_subtype == "TECHNICAL_SECRET_LICENSE"
        else "技术许可"
        if subtype == "TECHNOLOGY_LICENSE"
        else "技术秘密转让"
        if tertiary_subtype == "TECHNICAL_SECRET_TRANSFER"
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
        "transfer_asset_facts": transfer_asset_facts,
        "independent_secret_transaction": bool(transfer_asset_facts['secret_transaction']),
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
        "sub_transactions": sub_transactions,
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
    technical_secret_fee = bool(re.search(
        r"技术秘密(?:许可)?(?:使用费|许可费)(?:总额)?[：:]?(?:人民币)?[\d,]+(?:\.\d+)?(?:万|亿)?元",
        compact,
    ))

    service_heading = bool(re.search(
        r"(?:第[一二三四五六七八九十\d]+条)?技术服务(?:和|及|与)?(?:技术)?(?:指导|培训)|"
        r"第[一二三四五六七八九十\d]+条技术(?:指导(?:和|及|与)?培训|支持)|"
        r"技术服务[：:](?:需要|包含|提供)",
        compact,
    ))
    service_articles = [
        article for article in re.split(r"(?=第[一二三四五六七八九十百\d]+条)", compact)
        if re.match(
            r"第[一二三四五六七八九十百\d]+条技术(?:服务|指导|支持|培训)",
            article,
        )
    ]
    service_scope = "。".join(service_articles) if service_articles else compact
    service_activities = [
        term for term in (
            "实施说明", "部署指导", "参数配置培训", "故障排查指导", "部署支持",
            "现场技术指导", "技术培训", "安装调试支持", "技术咨询",
            "系统部署", "模型训练", "生产环境调试", "技术人员培训", "远程技术支持",
            "软件部署", "参数标定", "系统调试", "现场技术支持", "人员培训",
        ) if term in service_scope
    ]
    service_content = bool(service_heading and len(service_activities) >= 2)
    structured_training = bool(
        re.search(r"培训(?:人员|人数)[：:]?\d+人", compact)
        and re.search(r"培训(?:时间|期限)[：:]?\d+个?(?:工作日|日|天)", compact)
        and re.search(r"技术服务期限[：:]?[^。；]{0,35}\d+个?(?:工作日|日|天)", compact)
    )
    service_content = service_content or structured_training
    if structured_training:
        service_activities.append("约定人数、培训时长及服务期限的技术培训")
    service_fee = bool(re.search(r"技术服务(?:和|及|与)?(?:技术)?(?:指导|培训)?费(?:用)?[：:]?(?:人民币)?[\d,]+(?:\.\d+)?(?:万|亿)?元", compact))
    service_fee_included = bool(re.search(
        r"技术服务(?:和|及|与)?(?:技术)?(?:指导|培训)?费(?:用)?.{0,24}(?:已)?包含在.{0,12}(?:转让费|许可费|合同价款|总价).{0,12}(?:不另行收费|不另收费)?",
        compact,
    )) or bool(re.search(
        r"(?:合同总价|合同价款|转让费|许可费)[^。；]{0,12}(?:已)?包含[^。；]{0,20}"
        r"(?:技术服务|技术支持|技术指导|培训)(?:费|费用)",
        service_scope,
    ))
    # A scoped service allowance followed by an express charge only for work
    # beyond that allowance is strong evidence that the baseline service is
    # already absorbed by the main transaction price.  Keep the separately
    # charged excess service as its own pricing question instead of turning the
    # whole service-fee arrangement into a missing fact.
    included_service_scope = bool(
        service_content
        and re.search(
            r"(?:技术服务|现场技术服务).{0,24}(?:不超过|限于|累计不超过)\d+(?:个)?(?:工作日|日|天|小时|次)",
            compact,
        )
        and re.search(
            r"(?:超过|超出).{0,36}(?:服务|工作量|工时).{0,24}(?:另行协商收费|另行收费|另行计费|协商计费)",
            compact,
        )
    )
    extra_service_charge_trigger = bool(re.search(
        r"(?:超过|超出).{0,36}(?:服务|工作量|工时).{0,24}(?:另行协商收费|另行收费|另行计费|协商计费)",
        compact,
    ))
    extra_service_pricing_standard = bool(
        extra_service_charge_trigger
        and re.search(
            r"(?:超过|超出).{0,80}(?:每(?:人)?日|每小时|每次|单价|费率|计价标准|计算公式)[：:]?(?:人民币)?[\d,.]+",
            compact,
        )
    )
    extra_service_billing_method = bool(
        extra_service_charge_trigger
        and re.search(r"(?:工时确认单|服务记录|工作量确认|按实际工时|按人日|按小时|按次计费)", compact)
    )
    extra_service_payment_node = bool(
        extra_service_charge_trigger
        and re.search(r"(?:额外|超出|超过).{0,60}(?:支付|付款|结算).{0,30}(?:日内|完成后|确认后|按月|按季)", compact)
    )
    technical_guidance = bool(
        any(term in compact for term in (
            "技术指导", "部署指导", "现场培训", "参数配置培训", "安装调试支持",
        ))
        or (service_heading and "指导" in compact)
    )
    technical_secret_transfer_context = bool(
        re.search(r"技术秘密.{0,16}转让|转让.{0,16}技术秘密", compact)
        and ("转让方" in compact or "让与方" in compact)
        and "受让方" in compact
    )
    secret_transfer_acceptance = bool(
        technical_secret_transfer_context
        and re.search(r"(?:第[一二三四五六七八九十\d]+条)?验收", compact)
        and sum(term in compact for term in (
            "按照以下标准验收", "书面异议", "验收合格",
            "能够在", "能够输出", "视为全部验收合格",
        )) >= 2
    )
    acceptance_heading_with_criteria = bool(
        re.search(r"第[一二三四五六七八九十\d]+条验收", compact)
        and sum(term in compact for term in (
            "技术资料交付", "正常部署", "正常运行", "平均误差", "重复定位误差",
            "验收指标", "测试条件", "验收合格",
        )) >= 2
    )
    structured_acceptance = bool(
        re.search(r"技术指标[：:]?[^。；]{0,70}(?:\d+(?:\.\d+)?%|\d+(?:\.\d+)?(?:mm|毫米))", compact)
        and re.search(r"首次验收期限[：:]?[^。；]{0,35}\d+日", compact)
        and re.search(r"第[二三]次验收期限[：:]?[^。；]{0,35}\d+日", compact)
    )
    acceptance = structured_acceptance or secret_transfer_acceptance or acceptance_heading_with_criteria or bool(
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
    from review_v2.technology_fact_ontology import matches_action
    refund_remedy = bool(
        final_failure_scope
        and matches_action('payment_refund', final_failure_scope)
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
                "included_service_scope": included_service_scope,
                "extra_service_charge_trigger": extra_service_charge_trigger,
                "extra_service_pricing_standard": extra_service_pricing_standard,
                "extra_service_billing_method": extra_service_billing_method,
                "extra_service_payment_node": extra_service_payment_node,
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


def analyze_technical_secret_loss_arrangement(text: str) -> Dict[str, Any]:
    """Resolve the substance of secret-loss clauses, not only their presence.

    The bounded clause window prevents an unrelated payment or termination
    clause from being combined with a technical-secret disclosure provision.
    """
    source = str(text or "")
    compact = re.sub(r"\s+", "", source)
    trigger_pattern = re.compile(
        r"(?:核心技术|许可技术|技术秘密|秘密性|秘密信息|know-?how).{0,50}(?:进入公开领域|成为公知|丧失秘密性|"
        r"被(?:第三方|他人)公开|第三方(?:合法)?公开|主动公开|申请专利.{0,20}公开)|"
        r"(?:进入公开领域|成为公知|丧失秘密性).{0,50}(?:技术秘密|秘密信息|know-?how)",
        re.I,
    )
    secret_loss_heading_pattern = re.compile(
        r"^(?:第[一二三四五六七八九十百\d]+条)?"
        r"(?:(?:技术秘密|秘密信息).{0,12}(?:公开|丧失秘密性)|秘密性.{0,8}丧失)",
        re.I,
    )

    # Never fall back to the entire contract.  That fallback combined an
    # unrelated secrecy sentence with unrelated payment/termination clauses
    # and manufactured an adverse arrangement that did not exist in the text.
    section_parts = re.split(
        r"(?m)(?=^\s*(?:第[一二三四五六七八九十百\d]+条|[一二三四五六七八九十百\d]+[、.．]))",
        source,
    )
    candidate_scopes = [
        part
        for part in section_parts
        if part.strip()
        and (
            trigger_pattern.search(re.sub(r"\s+", "", part))
            or secret_loss_heading_pattern.search(re.sub(r"\s+", "", part))
        )
    ]
    if not candidate_scopes:
        sentences = [
            re.sub(r"\s+", "", part)
            for part in re.split(r"(?<=[。；;！？!?])|\r?\n+", source)
            if re.sub(r"\s+", "", part)
        ]
        for index, sentence in enumerate(sentences):
            if trigger_pattern.search(sentence):
                candidate_scopes.append("".join(sentences[index:index + 5]))

    def _scope_score(value: str) -> tuple[int, int]:
        value = re.sub(r"\s+", "", value)
        consequence_hits = sum(
            bool(re.search(pattern, value, re.I))
            for pattern in (
                r"继续(?:履行|有效|支付|缴纳)",
                r"(?:未到期|未来|后续).{0,24}(?:许可费|使用费|转让费|服务费|提成)",
                r"(?:已支付|已付).{0,18}(?:不退|不予返还|不予退还)",
                r"(?:不得|无权|不能).{0,12}(?:解除|终止)",
                r"(?:调减|停止支付|分项结算|费用调整)",
                r"(?:有权|可以).{0,18}(?:解除|终止)",
                r"(?:公开|丧失秘密性).{0,80}(?:通知|告知)",
                r"(?:迟延|延迟|未及时|未履行).{0,18}(?:通知|告知).{0,45}(?:赔偿|损失)",
            )
        )
        return consequence_hits, -len(value)

    scope = max(candidate_scopes, key=_scope_score) if candidate_scopes else ""
    from review_v2.proposition_scope import arrangement_matches, component_states
    patterns = {
        "third_party_disclosure": r"(?:第三方|他人)[^。；;\n]{0,80}(?:公开|披露)",
        "public_domain_entry": r"(?:进入|成为)[^。；;\n]{0,16}(?:公共领域|公开领域|公知技术)",
        "licensor_patent_disclosure": r"(?:许可方|卖方|出让方|转让方|甲方|乙方)[^。；;\n]{0,35}(?:申请专利|公开)[^。；;\n]{0,35}(?:导致|使)[^。；;\n]{0,20}(?:公开|丧失秘密性)",
        "licensor_active_disclosure": r"(?:许可方|卖方|出让方|转让方|甲方)[^。；;\n]{0,20}主动(?:向[^，。；;\n]{0,15})?公开",
        "independent_research_disclosure": r"(?:第三方|他人)[^。；;\n]{0,12}独立(?:研究|研发|开发)[^。；;\n]{0,70}(?:公开|丧失秘密性)",
        "reverse_engineering_disclosure": r"反向工程[^。；;\n]{0,70}(?:公开|丧失秘密性)",
        "partial_disclosure": r"(?:全部或者部分|全部或部分|部分)[^。；;\n]{0,20}(?:公开|丧失秘密性)",
        "secret_disclosure": r"(?:技术秘密|秘密信息).{0,35}(?:公开|丧失秘密性)|(?:核心技术|许可技术).{0,35}丧失秘密性",
        "future_license_fee_continues": r"(?:不得.{0,35}停止支付|(?:仍须|仍应|仍需|继续).{0,35}支付).{0,35}(?:尚未到期的?)?(?:技术秘密)?(?:许可使用费|许可费|使用费|转让费)",
        "future_service_fee_continues": r"(?:不得.{0,45}停止支付|(?:仍须|仍应|仍需|继续).{0,45}支付).{0,35}技术服务费",
        "royalty_continues": r"(?:不得.{0,45}停止支付|(?:仍须|仍应|仍需|继续).{0,45}支付).{0,35}(?:提成费用|提成费)|(?:提成费用|提成费).{0,30}(?:仍须|继续)支付",
        "termination_restricted": r"(?:不得|无权).{0,45}(?:以技术秘密.{0,25}(?:公开|丧失秘密性).{0,20}为由)?(?:单方面|单方)?解除合同",
        "paid_fee_nonrefundable": r"(?:已经|已)支付.{0,25}(?:不予退还|不退)|(?:无需|无须|不予|不得).{0,12}(?:退还|返还).{0,25}(?:已经|已)(?:支付|收取)",
        "fee_stop_or_reduction": r"(?:停止支付|不再支付|调减|减少|调整).{0,35}(?:未到期|未来|尚未履行)?.{0,20}(?:许可使用费|许可费|使用费|技术服务费|提成)",
        "termination_available": r"(?:被许可方|买方|受让方).{0,30}(?:有权|可以).{0,20}解除合同|(?:公开|丧失秘密性).{0,40}(?:可以|有权)解除合同",
        "secret_loss_notification": r"(?:技术秘密|秘密性|秘密信息).{0,80}(?:公开|丧失秘密性).{0,80}(?:通知|告知)|(?:通知|告知).{0,80}(?:技术秘密|秘密性|秘密信息).{0,80}(?:公开|丧失秘密性)|通知期限|通知义务|应.{0,16}(?:通知|告知)|须.{0,16}(?:通知|告知)|未履行.{0,12}(?:通知|告知)",
        "secret_loss_notification_deadline": r"(?:\d+|[一二三四五六七八九十]+)个?(?:工作日|日|天)(?:内)?(?:通知|告知)|通知期限[:：]?(?:\d+|[一二三四五六七八九十]+)个?(?:工作日|日|天)",
        "late_notification_damage": r"(?:未履行|迟延|延迟|未及时).{0,18}(?:通知|告知).{0,45}(?:赔偿|损失)|(?:通知|告知).{0,28}(?:迟延|延迟|未履行).{0,35}(?:赔偿|损失)",
        "separate_value_settlement": r"(?:技术服务|其他独立价值|已履行部分).{0,35}(?:分项结算|单独结算|据实结算)",
    }
    # Every consumer receives the same bounded proposition and condition.
    # Neither a retrieval hit nor a word in an unspecified question is proof.
    fact_sources = {key: list(arrangement_matches(pattern, scope)) for key, pattern in patterns.items()}
    third_party_disclosure = bool(fact_sources['third_party_disclosure'])
    public_domain_entry = bool(fact_sources['public_domain_entry'])
    licensor_patent_disclosure = bool(fact_sources['licensor_patent_disclosure'])
    partial_disclosure = bool(fact_sources['partial_disclosure'])
    trigger_keys = list(patterns)[:8]
    secret_loss_trigger = any(fact_sources[key] for key in trigger_keys)
    future_license_fee_continues = bool(fact_sources['future_license_fee_continues'])
    future_service_fee_continues = bool(fact_sources['future_service_fee_continues'])
    royalty_continues = bool(fact_sources['royalty_continues'])
    termination_restricted = bool(fact_sources['termination_restricted'])
    paid_fee_nonrefundable = bool(fact_sources['paid_fee_nonrefundable'])
    fee_stop_or_reduction = bool(fact_sources['fee_stop_or_reduction'])
    termination_available = bool(fact_sources['termination_available'])
    secret_loss_notification = bool(fact_sources['secret_loss_notification'])
    secret_loss_notification_deadline = secret_loss_notification and bool(fact_sources['secret_loss_notification_deadline'])
    late_notification_damage = bool(fact_sources['late_notification_damage'])
    separate_value_settlement = bool(fact_sources['separate_value_settlement'])
    trigger_components = component_states([
        (key, label, fact_sources[key]) for key, label in zip(trigger_keys,
            ('第三方公开', '进入公共领域', '许可方申请专利导致公开', '许可方主动公开',
             '第三方独立研究导致公开', '反向工程导致公开', '部分技术信息公开', '技术秘密公开或丧失秘密性'))])
    unconditional_future_payment = any((
        future_license_fee_continues,
        future_service_fee_continues,
        royalty_continues,
    ))
    adverse = bool(
        secret_loss_trigger
        and unconditional_future_payment
        and not fee_stop_or_reduction
    )
    reasonable = bool(
        secret_loss_trigger
        and fee_stop_or_reduction
        and termination_available
        and not unconditional_future_payment
    )
    return {
        "evidence_scope": scope,
        "fact_sources": fact_sources,
        "trigger_components": trigger_components,
        "secret_loss_trigger": secret_loss_trigger,
        "third_party_disclosure": third_party_disclosure,
        "public_domain_entry": public_domain_entry,
        "licensor_patent_disclosure": licensor_patent_disclosure,
        "partial_disclosure": partial_disclosure,
        "future_license_fee_continues": future_license_fee_continues,
        "future_service_fee_continues": future_service_fee_continues,
        "royalty_continues": royalty_continues,
        "termination_restricted": termination_restricted,
        "paid_fee_nonrefundable": paid_fee_nonrefundable,
        "fee_stop_or_reduction": fee_stop_or_reduction,
        "termination_available": termination_available,
        "secret_loss_notification": secret_loss_notification,
        "secret_loss_notification_deadline": secret_loss_notification_deadline,
        "late_notification_damage": late_notification_damage,
        "separate_value_settlement": separate_value_settlement,
        "unconditional_future_payment": unconditional_future_payment,
        "adverse": adverse,
        "reasonable": reasonable,
    }


EXPENSE_ITEM_PATTERN = re.compile(
    r"律师费|诉讼费|鉴定费|仲裁费|和解费|赔偿费|召回费用|召回损失|停产损失|"
    r"业务中断损失|客户索赔|直接经济损失|间接损失|可得利益损失"
)


def explicit_expense_items(text: str) -> List[str]:
    """Only enumerate expense heads actually written in the source allocation."""
    return list(dict.fromkeys(EXPENSE_ITEM_PATTERN.findall(text)))


def extract_material_delivery_method_facts(clauses: List[Any]) -> List[Dict[str, Any]]:
    facts = []
    methods = r"电子邮件|电子文件|电子版|电子技术资料|加密网盘|网盘|移动存储设备|存储介质|纸质|光盘|安全文件服务器|现场交付|可编辑格式"
    for clause in clauses:
        context = " ".join([clause.title, clause.text, *getattr(clause, "heading_path", [])])
        if not re.search(r"资料|文件|交付方式|提交方式", context):
            continue
        for sentence in re.split(r"[。；;\n]", clause.text):
            if re.search(methods, sentence) and re.search(r"交付|提交|提供|资料|文件", sentence):
                if not re.search(r"(?:不得|不采用|未明确|未约定).{0,20}(?:交付|提交|电子|方式)", sentence):
                    facts.append({"clause_id": clause.clause_id, "location": clause.location, "quote": sentence.strip()})
    return facts


def extract_material_disposition_facts(clauses: List[Any]) -> Dict[str, Any]:
    """Keep disposal/retention objects and actors separate, including anaphora.

    '相关数据' can refer back to explicitly enumerated data in the same clause;
    it cannot introduce a copy/backup or turn that data into technical files.
    """
    facts: Dict[str, Any] = {}
    objects = {
        "technical_secret_material": r"技术秘密资料|保密(?:资料|文件|材料)",
        "technical_material": r"(?<!秘密)技术资料|技术文件",
        "original_material": r"原始资料|原件",
        "copy": r"复制件|副本",
        "backup": r"备份",
        "counterparty_data": r"生产数据|销售数据|测试数据|客户资料|技术反馈",
    }
    for clause in clauses:
        previous_data = ""
        for sentence in re.split(r"[。；;\n]", clause.text):
            s = re.sub(r"\s+", "", sentence)
            if not s:
                continue
            if re.search(objects["counterparty_data"], s):
                previous_data = sentence.strip()
            disposal = bool(re.search(r"返还|删除|销毁|清除", s))
            retention = bool(re.search(r"(?:终止|解除|届满|履行完毕|项目结束).{0,80}(?:保存|保留|留存)", s))
            if not disposal and not retention:
                continue
            if re.search(r"(?:无需|无须|不必|不得|不予).{0,10}(?:返还|删除|销毁)", s):
                disposal = False
            if re.search(r"(?:不得|无需|无须|不必|不再|不予|不能).{0,8}(?:保存|保留|留存)", s):
                retention = False
            actor_match = re.search(r"被许可[方人]|(?<!被)许可[方人]|受让方|让与方|出让方|卖方|买方|甲方|乙方|各方", s)
            actor = actor_match.group(0) if actor_match else "未明确主体"
            for object_id, pattern in objects.items():
                direct = bool(re.search(pattern, s))
                antecedent = object_id == "counterparty_data" and previous_data and bool(re.search(r"相关数据|上述数据|该等数据", s))
                if not direct and not antecedent:
                    continue
                for action, present in (("disposal", disposal), ("retention", retention)):
                    if not present:
                        continue
                    # A sentence with both verbs must name this object on the
                    # same side of the conjunction, not borrow its sibling.
                    parts = re.split(r"[；;，,]|但|而", s)
                    verb = r"返还|删除|销毁|清除" if action == "disposal" else r"保存|保留|留存"
                    if direct and not any(re.search(pattern, part) and re.search(verb, part) for part in parts):
                        continue
                    row = {"clause_id": clause.clause_id, "location": clause.location,
                           "quote": sentence.strip(), "actor": actor, "object_type": object_id,
                           "action": action}
                    if antecedent and not direct:
                        row["antecedent_quote"] = previous_data
                    facts.setdefault(object_id + "_" + action, []).append(row)
    by_id = {clause.clause_id: clause for clause in clauses}
    for key, retained in list(facts.items()):
        if not key.endswith("_retention"):
            continue
        object_id = key.removesuffix("_retention")
        for source in retained:
            clause = by_id[source["clause_id"]]
            tail = clause.text[clause.text.find(source["quote"]):]
            same_object_context = True
            same_actor_context = True
            for sentence in re.split(r"[。；;\n]", tail):
                named_objects = {name for name, pattern in objects.items() if re.search(pattern, sentence)}
                subject = re.search(
                    r"(被许可[方人]|(?<!被)许可[方人]|受让方|让与方|出让方|卖方|买方|甲方|乙方|各方)"
                    r"(?=应当|应|须|可以|可|仅|不得|负责)", sentence,
                )
                if named_objects:
                    same_object_context = object_id in named_objects
                if subject:
                    same_actor_context = subject.group(1) == source["actor"]
                if not same_object_context or not same_actor_context:
                    continue
                for suffix, pattern in (
                    ("period", r"(?:保存|留存|保留|期限).{0,12}(?:\d+|[一二三四五六七八九十]+)(?:年|月|日|天)"),
                    ("access_control", r"(?:访问|接触|读取).{0,12}(?:权限|控制|限制)|最小权限|授权人员"),
                    ("deletion_or_destroy", r"(?:到期|届满|期限届满).{0,18}(?:删除|销毁|清除)"),
                    ("confirmation", r"(?:删除|销毁|处置).{0,18}(?:确认|证明)|(?:确认|证明).{0,12}(?:删除|销毁|处置)"),
                ):
                    if re.search(pattern, sentence) and not re.search(r"未约定|未明确|无需|不必", sentence):
                        facts.setdefault(object_id + "_" + suffix, []).append({
                            **source, "quote": sentence.strip(), "action": suffix,
                            "antecedent_quote": source["quote"],
                        })
    return facts


CLAIM_RESPONSE_ELEMENT_FACT_KEYS = {
    "claim_trigger": "claim_trigger", "notification_requirement": "notification_requirement",
    "notification_deadline": "notification_deadline", "claim_handling": "claim_handling",
    "administrative_handling": "administrative_handling", "litigation_handling": "litigation_handling",
    "licensor_participation": "claim_handling", "licensee_claim_handling": "licensee_claim_handling",
    "licensor_assistance": "claim_assistance", "liability_responsible_party": "liability_responsible_party",
    "legal_cost_allocation": "legal_cost_allocation", "attorney_fee": "attorney_fee",
    "litigation_cost": "litigation_cost", "direct_damage": "direct_damage",
    "defense_cost_allocation": "defense_cost_scope", "damages_allocation": "damages_allocation",
    "damages_scope": "damages_scope", "settlement_non_prejudice": "settlement_non_prejudice",
    "settlement_consultation": "settlement_consultation", "defense_control": "defense_control",
    "lawyer_selection": "lawyer_selection", "settlement_authority": "settlement_authority",
    "replacement_remedy": "replacement_remedy", "replacement_or_workaround": "replacement_remedy",
    "license_cure": "license_cure", "refund_or_termination_remedy": "refund_remedy",
}

# A duty to lead handling supports the basic component of control, not the
# separate right to decide the defence. Only PARTIAL consumers may use it.
CLAIM_RESPONSE_PARTIAL_FACT_KEYS = {'defense_control': 'claim_handling'}


_CLAIM_EXPENSE_ITEMS = {
    "legal_cost_allocation": r"(?:合理)?法律(?:服务)?费用",
    "attorney_fee": r"律师费(?:用)?", "litigation_cost": r"诉讼费(?:用)?",
    "defense_fee": r"抗辩费(?:用)?", "arbitration_cost": r"仲裁费(?:用)?",
    "administrative_cost": r"行政处理费(?:用)?",
}
_CLAIM_DAMAGE_ITEMS = r"直接经济损失|合理直接损失|直接损失|可得利益(?:损失)?|停产损失|召回损失|业务中断损失|全部损失"


def extract_claim_response_facts(clauses: List[Any], provider: str, recipient: str) -> Dict[str, Any]:
    """Extract affirmative duties within the same inbound-claim event and actor.

    Outbound patent enforcement, improvement notices and invalidity remedies
    are different events. Each fact retains its own source quotation; a duty
    to assist never entails a duty to take charge of the claim.
    """
    facts: Dict[str, Any] = {}
    inbound = re.compile(
        r"(?:第三方|第三人|他人).{0,40}(?:主张|指控|索赔|提出.{0,12}(?:权利|侵权))|"
        r"(?:侵犯|侵害|侵权).{0,18}(?:第三方|第三人|他人)|第三方(?:侵权)?索赔|"
        r"(?:受到|遭到|收到|遭受).{0,15}(?:第三方|第三人|他人).{0,15}(?:警告|投诉|诉讼)|"
        r"权属瑕疵.{0,35}(?:无法|不能)取得.{0,12}(?:专利|权利)"
    )
    outbound = re.compile(r"(?:第三方|第三人|他人)(?:侵犯|侵害).{0,20}(?:合同专利|本专利|本合同|许可专利)")
    unrelated = re.compile(r"不可抗力|保密义务|改进成果|分许可|资料验收|宣告无效|逾期付款|转让登记")

    def add(key: str, clause: Any, quote: str, actor: str = "", **values: Any) -> None:
        # Retain a fault/knowledge restriction as a condition of the source
        # obligation, never broaden it into unconditional provider liability.
        from review_v2.proposition_scope import scoped_propositions
        restriction = next((row['condition'] for row in scoped_propositions(quote) if row['condition']), '')
        row = {"clause_id": clause.clause_id, "quote": quote.strip(), "location": clause.location,
               "actor": actor, **values}
        if restriction:
            limited = bool(row.get("limited") or re.search(r"故意隐瞒|明知|已知|明确知(?:道|悉)|故意未披露", restriction))
            row.update(condition=restriction, limited=limited, polarity="CONDITIONAL")
            if limited and key == "damages_allocation":
                condition_row = dict(row)
                if condition_row not in facts.setdefault("claim_fault_condition", []):
                    facts["claim_fault_condition"].append(condition_row)
        if row not in facts.setdefault(key, []):
            facts[key].append(row)

    for clause in clauses:
        if getattr(clause, "party_obligation", True) is False:
            continue
        context = False
        actor = ""
        from review_v2.proposition_scope import scoped_propositions
        for scoped in scoped_propositions(clause.text):
            sentence = scoped['quote'].rstrip('。；;！？')
            if scoped['polarity'] == 'MISSING' and not scoped['affirmative_tail']:
                actor = ""
                continue
            s = re.sub(r"\s+", "", sentence)
            if not s:
                continue
            without_number = re.sub(r"^(?:第[一二三四五六七八九十百\d]+条|\d+[.、])", "", s)
            if without_number == re.sub(r"\s+", "", str(getattr(clause, "title", ""))) or s == re.sub(r"\s+", "", str(getattr(clause, "title", ""))):
                continue
            if re.search(r"(?:不保证|保证).{0,45}(?:不|不会)侵犯", s) and not re.search(r"权利主张|索赔|指控", s):
                continue
            if outbound.search(s):
                context, actor = False, ""
                continue
            explicit = bool(inbound.search(s))
            if unrelated.search(s) and not explicit:
                context, actor = False, ""
            if explicit:
                context = True
                add("claim_trigger", clause, sentence)
            if not context:
                continue
            if scoped['polarity'] == 'MISSING':
                # A contrast closes only the preceding absence proposition.
                # Keep the full exact quote/trigger, but extract duties solely
                # from the independently affirmed tail.
                s = re.sub(r"\s+", "", scoped['affirmative_tail'])
            if re.search(r"(?:另行|届时).{0,12}协商.{0,12}(?:承担|责任)|(?:责任|费用|损失).{0,20}(?:另行|届时).{0,8}协商", s):
                # An enumerated cost followed by future negotiation names a
                # topic, not a present allocation to the preceding actor.
                actor = ""
                continue
            # Notification must identify the recipient of the notice, not just
            # contain a notice verb or a nearby delivery/payment deadline.
            field_source = sentence.strip()
            if field_source.endswith(("：", ":")):
                field_value = re.search(re.escape(field_source) + r"\s*(?:\d+|[一二三四五六七八九十]+)个?(?:工作日|日|天|小时)内?", clause.text)
                field_source = field_value[0] if field_value else ""
            field_notice = re.search(
                rf"{recipient}.{{0,25}}(?:收到|获悉).{{0,35}}第三方.{{0,20}}(?:主张|索赔).{{0,15}}通知期限[：:]\s*"
                r"((?:\d+|[一二三四五六七八九十]+)个?(?:工作日|日|天|小时)内?)",
                re.sub(r"\s+", "", field_source),
            )
            if field_notice and not re.search(r"未约定|未明确|待定|无需", field_notice[0]):
                # Keep the label and its value together as one direct source.
                add("notification_requirement", clause, field_source, "LICENSEE")
                add("notification_deadline", clause, field_source, "LICENSEE", value=field_notice[1])
            notice = re.search(rf"(?:应当|应|须|必须|及时).{{0,45}}(?:通知|告知|通知给){provider}", s)
            if notice and not re.search(r"(?:无需|无须|不必|未约定|未明确).{0,20}(?:通知|告知)", s):
                notice_actor = re.search(recipient, s[:notice.start()])
                if notice_actor or actor == "LICENSEE":
                    add("notification_requirement", clause, sentence, "LICENSEE")
                    deadline = re.search(r"(?:\d+|[一二三四五六七八九十]+)个?(?:工作日|日|天|小时)内", notice.group(0))
                    if deadline:
                        add("notification_deadline", clause, sentence, "LICENSEE", value=deadline.group(0))
            if "和解" in s and not re.search(r"未约定|未明确|另行协商责任", s):
                if re.search(rf"(?:不得|不应).{{0,15}}损害.{{0,10}}{recipient}|未经{recipient}.{{0,15}}同意.{{0,20}}不得.{{0,10}}和解|未经{recipient}.{{0,15}}同意.{{0,20}}不得以[^。；]{{0,90}}(?:承认侵权|停止[^。；]{{0,10}}生产|额外付款)[^。；]{{0,60}}为条件(?:达成)?和解", s):
                    add("settlement_non_prejudice", clause, sentence)
                if re.search(r"和解.{0,18}(?:应|须|必须).{0,12}(?:事先)?协商|双方.{0,15}和解.{0,15}事先协商", s):
                    add("settlement_consultation", clause, sentence)
            allocation_text = s
            protected_terms = re.search(r'不得以[^。；]+为条件(?:达成)?和解', s)
            if protected_terms:
                # Obligations forbidden as settlement conditions are not
                # present allocations to the protected party.
                allocation_text = s[:protected_terms.start()] + s[protected_terms.end():]
            for part in re.split(r"[，,：:]|但(?:是)?(?=不|无|未)", allocation_text):
                if re.search(r'(?:导致|致使|造成).{0,55}(?:承担|支付|赔偿).{0,30}(?:的|时)$', part):
                    # A recipient suffering third-party liability is the
                    # premise for reimbursement, not the operative allocation.
                    continue
                roles = sorted([(m.start(), role) for role, pattern in (("LICENSOR", provider), ("LICENSEE", recipient))
                                for m in re.finditer(pattern, part)])
                subjects = [(pos, role) for pos, role in roles if
                            re.fullmatch(r"(?:并|且|同时)?", part[:pos]) or
                            re.match(rf"(?:{provider}|{recipient})(?:应当|应|须|负责|自行|仅|承担)", part[pos:])]
                if subjects:
                    actor = subjects[0][1]
                # An explicit passive allocation takes precedence over the
                # party merely mentioned as the victim or fee basis.
                assigned = re.search(rf"由(?P<party>{provider}|{recipient}).{{0,8}}(?:承担|负责|处理|负担)", part)
                if assigned:
                    actor = "LICENSEE" if re.fullmatch(recipient, assigned.group("party")) else "LICENSOR"
                requested = re.search(rf"(?:{provider}|{recipient})(?:有权|可以)要求(?P<obligor>{provider}|{recipient})", part)
                if requested:
                    actor = "LICENSEE" if re.fullmatch(recipient, requested['obligor']) else "LICENSOR"
                if not actor:
                    continue
                positive = part.replace("不得拒绝", "应")
                if re.search(r"未(?:明确)?约定", positive):
                    # Negation scopes this atom, not a later affirmative duty.
                    continue
                if re.search(r"不保证|(?:不|无需|无须|不必|未约定|未明确).{0,8}(?:承担|负责|协助|通知|参与|提供|赔偿|退还|返还|选择|决定)|另行协商|待定", positive):
                    continue
                # Stop at a new actor. '被许可方...许可方负责' cannot
                # attribute the provider's action to the first party.
                if len(roles) > 1 and not assigned:
                    action_roles = [(pos, role) for pos, role in roles if re.match(
                        rf"(?:{provider}|{recipient})(?:应当|应|须|负责|自行|根据|仅|承担)", part[pos:])]
                    if action_roles:
                        pos, actor = action_roles[-1]
                        positive = part[pos:]
                from review_v2.technology_fact_ontology import claim_action
                handling = claim_action('handling', positive)
                if handling and not re.search(r"协助|配合", handling.group(0)):
                    add("claim_handling" if actor == "LICENSOR" else "licensee_claim_handling", clause, sentence, actor)
                    if actor == "LICENSOR":
                        for key, pattern in (
                            ("administrative_handling", r"(?:负责|应当|应|须|自行).{0,18}(?:行政处理|行政程序|行政应对)(?!费|成本)"),
                            ("litigation_handling", r"(?:负责|应当|应|须|自行).{0,18}(?:应诉|诉讼|司法程序)(?!费|成本)"),
                        ):
                            if re.search(pattern, positive):
                                add(key, clause, sentence, actor)
                if actor == "LICENSOR" and re.search(r"(?:提供|给予|予以).{0,18}(?:协助|帮助)|(?:应|须).{0,10}(?:协助|配合)", positive):
                    add("claim_assistance", clause, sentence, actor,
                        limited=bool(re.search(r"仅|根据实际情况|技术协助|技术帮助", positive)))
                # Legal liability and damages liability identify the same actor;
                # identifying that actor does not prove any specific cost scope.
                cap_only = bool(re.search(r"承担的.{0,16}(?:责任|赔偿).{0,12}(?:不超过|限于|为限|上限)", positive))
                if claim_action('liability_party', positive) and not cap_only:
                    add("liability_responsible_party", clause, sentence, actor)
                for key, pattern in (
                    ("defense_control", r"抗辩控制权|主导抗辩|控制抗辩|负责抗辩"),
                    ("lawyer_selection", r"(?:选择|选聘|委托).{0,6}律师|律师选择权"),
                    ("settlement_authority", r"和解决策权|和解权限|和解审批权|和解审批机制|决定是否和解"),
                    ("claim_cost_allocation", r"(?:承担|负担|支付).{0,40}(?:律师费|诉讼费|法律费用|抗辩费用)|(?:律师费|诉讼费|法律费用|抗辩费用).{0,70}(?:承担|负担|支付)"),
                    ("third_party_compensation_allocation", r"(?:赔偿费|赔偿责任|全部损失|全部责任|法律和经济责任).{0,45}(?:承担|负担)|承担.{0,25}(?:赔偿责任|侵权责任|全部责任|损失|法律和经济责任)|赔偿(?:全部|直接|相应|合理)?损失"),
                ):
                    if re.search(pattern, positive):
                        add(key, clause, sentence, actor)
                # General legal expenses and statutory damages identify an
                # allocation, not the concrete expense or loss categories.
                # Require each category inside the same actor/action span.
                expense_items = []
                excluded_scope = " ".join(re.findall(r"(?:不包括|不含|排除)([^的。；，,]{1,50})", positive))
                for key, pattern in _CLAIM_EXPENSE_ITEMS.items():
                    if re.search(pattern, excluded_scope):
                        continue
                    allocation = re.search(
                        rf"(?:承担|负担|支付).{{0,40}}(?:{pattern})|(?:{pattern}).{{0,70}}(?:承担|负担|支付)", positive,
                    )
                    if allocation:
                        values = list(dict.fromkeys(re.findall(pattern, allocation[0])))
                        add(key, clause, sentence, actor, scope_items=values, allocation_quote=positive)
                        if key != "legal_cost_allocation":
                            expense_items.extend(values)
                if expense_items:
                    add("defense_cost_scope", clause, sentence, actor,
                        scope_items=list(dict.fromkeys(expense_items)), allocation_quote=positive)
                damages_distribution = re.search(
                    rf"(?:承担|负担|支付|赔偿).{{0,40}}(?:赔偿费(?:用)?|{_CLAIM_DAMAGE_ITEMS})|"
                    rf"(?:赔偿费(?:用)?|{_CLAIM_DAMAGE_ITEMS}).{{0,70}}(?:承担|负担|支付|赔偿)", positive,
                )
                if damages_distribution:
                    add("damages_allocation", clause, sentence, actor, allocation_quote=positive)
                damage_allocation = re.search(
                    rf"(?:承担|负担|赔偿).{{0,40}}(?:{_CLAIM_DAMAGE_ITEMS})|"
                    rf"(?:{_CLAIM_DAMAGE_ITEMS}).{{0,70}}(?:承担|负担|赔偿)", positive,
                )
                if damage_allocation:
                    values = list(dict.fromkeys(re.findall(_CLAIM_DAMAGE_ITEMS, damage_allocation[0])))
                    add("damages_scope", clause, sentence, actor, scope_items=values, allocation_quote=positive)
                    direct = [value for value in values if "直接" in value]
                    if direct:
                        add("direct_damage", clause, sentence, actor, scope_items=direct, allocation_quote=positive)
                if actor == "LICENSOR":
                    for key, pattern in (
                        ("replacement_remedy", r"(?:提供|采取).{0,20}(?:替代技术|替代方案|绕开侵权)"),
                        ("license_cure", r"(?:取得|补办|恢复).{0,15}(?:第三方许可|第三方授权|许可权|授权)|修复权利瑕疵"),
                        ("refund_remedy", r"(?:退还|返还|退回).{0,20}(?:款|费)"),
                    ):
                        if re.search(pattern, positive):
                            add(key, clause, sentence, actor)
    return facts


def claim_requirement_entailment(
    element_id: str, quote: str, context_text: str = "", provider: Optional[str] = None,
    recipient: Optional[str] = None, support_status: str = "COVERED",
) -> Optional[bool]:
    """Recompute one declared evidence edge from source text and a fixed schema.

    Unknown element IDs return None so callers can dispatch other domains.
    Context supplies the inbound event, but the quoted text itself must contain
    the actor/action span proving this exact requirement.
    """
    fact_key = CLAIM_RESPONSE_ELEMENT_FACT_KEYS.get(str(element_id).lower())
    if fact_key is None:
        return None
    from review_v2.clause_parser import parse_contract_clauses

    text = context_text or quote
    if provider is None or recipient is None:
        patterns = build_technology_fact_registry(text)["third_party_claim"]["response_party_patterns"]
        provider, recipient = provider or patterns["provider"], recipient or patterns["recipient"]
    facts = extract_claim_response_facts(parse_contract_clauses(text), provider, recipient)
    compact_quote = re.sub(r"\s+", "", quote or "")
    compact_source = re.sub(r"\s+", "", text)
    if not compact_quote or compact_quote not in compact_source:
        return False
    candidates = list(facts.get(fact_key, []))
    if support_status == 'PARTIALLY_COVERED':
        candidates += facts.get(CLAIM_RESPONSE_PARTIAL_FACT_KEYS.get(element_id), [])
    return any(
        re.sub(r"\s+", "", row.get("allocation_quote") or row["quote"]) in compact_quote
        for row in candidates
    )


def claim_response_entailment_failures(
    elements: List[Dict[str, Any]], clauses: List[Any], *, provider: Optional[str] = None,
    recipient: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Validate covered elements using source clauses, never asserted bindings."""
    from types import SimpleNamespace

    sources = []
    for row in clauses:
        if isinstance(row, dict):
            if row.get("source_type") == "SEARCH_AUDIT":
                continue
            row = SimpleNamespace(
                clause_id=row.get("clause_id") or row.get("evidence_id"),
                text=row.get("raw_text") or row.get("text") or row.get("quote") or row.get("quoted_text") or "",
                location=row.get("location") or "", title="", party_obligation=True,
            )
        sources.append(row)
    text = "\n".join(row.text for row in sources)
    if provider is None or recipient is None:
        patterns = build_technology_fact_registry(text)["third_party_claim"]["response_party_patterns"]
        provider, recipient = provider or patterns["provider"], recipient or patterns["recipient"]
    facts = extract_claim_response_facts(sources, provider, recipient)
    failures = []
    for element in elements:
        key = element.get("element_id")
        fact_key = CLAIM_RESPONSE_ELEMENT_FACT_KEYS.get(key)
        partial_key = CLAIM_RESPONSE_PARTIAL_FACT_KEYS.get(key)
        if element.get('status') == 'PARTIALLY_COVERED' and partial_key == element.get('source_fact_key'):
            fact_key = partial_key
        if fact_key is None or element.get("status") not in {"COVERED", "PARTIALLY_COVERED", "ADVERSE"}:
            continue
        if element.get("source_fact_key") != fact_key:
            failures.append({"element_id": key, "reason": "CLAIM_RESPONSE_FACT_KEY_MISMATCH"})
        actual = facts.get(fact_key, [])
        if not actual:
            failures.append({"element_id": key, "reason": "CLAIM_RESPONSE_FACT_NOT_ENTAILED"})
            continue
        declared_sources = element.get("supporting_evidence") or []
        if not declared_sources:
            failures.append({"element_id": key, "reason": "CLAIM_RESPONSE_SOURCE_BINDING_MISMATCH"})
        for declared in declared_sources:
            if not any(
                declared.get("clause_id") == source.get("clause_id")
                and declared.get("actor") == source.get("actor")
                and re.sub(r"\s+", "", declared.get("quote") or "") == re.sub(r"\s+", "", source["quote"])
                and declared.get("scope_items") == source.get("scope_items")
                for source in actual
            ):
                failures.append({"element_id": key, "reason": "CLAIM_RESPONSE_SOURCE_BINDING_MISMATCH"})
    return failures


def build_technology_fact_registry(text: str) -> Dict[str, Any]:
    """Create source-neutral facts shared by every third-party claim review."""
    compact = re.sub(r"\s+", "", text or "")
    # Contract-defined party aliases must survive section-level extraction.  A claim
    # clause often says only "乙方负责应诉", while the role declaration identifying
    # 乙方 as licensor appears elsewhere in the contract.
    # ``许可方`` must not match the suffix of ``被许可方``.
    licensor_aliases = {r"(?<!被)许可方", r"(?<!被)许可人", "卖方", "出让方", "让与方", "转让方"}
    licensee_aliases = {"被许可方", "被许可人", "接受方", "买方", "受让方"}
    for match in re.finditer(
        r"(?P<party>甲方|乙方)(?:[（(](?:许可方|卖方|出让方|让与方|转让方)[）)]|.{0,8}(?:为|作为|系)(?:许可方|卖方|出让方|让与方|转让方))",
        compact,
    ):
        licensor_aliases.add(re.escape(match.group("party")))
    for match in re.finditer(
        r"(?<!被)(?:许可方|卖方|出让方|让与方|转让方)(?:[（(](?P<party1>甲方|乙方)[）)]|.{0,8}(?:为|是|即)(?P<party2>甲方|乙方))",
        compact,
    ):
        licensor_aliases.add(re.escape(match.group("party1") or match.group("party2")))
    for match in re.finditer(
        r"(?P<party>甲方|乙方)(?:[（(](?:被许可方|买方|受让方)[）)]|.{0,8}(?:为|作为|系)(?:被许可方|买方|受让方))",
        compact,
    ):
        licensee_aliases.add(re.escape(match.group("party")))
    for match in re.finditer(
        r"(?:被许可方|买方|受让方)(?:[（(](?P<party1>甲方|乙方)[）)]|.{0,8}(?:为|是|即)(?P<party2>甲方|乙方))",
        compact,
    ):
        licensee_aliases.add(re.escape(match.group("party1") or match.group("party2")))
    licensor = r"(?:" + "|".join(sorted(licensor_aliases)) + r")"
    licensee = r"(?:" + "|".join(sorted(licensee_aliases)) + r")"
    claim_section_match = re.search(
        r"第[一二三四五六七八九十\d]+条(?:权利保证(?:及|与)第三方权利|第三方权利(?:责任|主张处理)?|第三人侵权责任|侵权的处理)(?P<body>.*?)(?=第[一二三四五六七八九十\d]+条|$)",
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
        rf"(?:许可方|出让方|让与方|转让方|卖方)(?:[（(](?:甲方|乙方)[）)])?[：:]\s*(?P<name>{party_name_pattern})",
        text or "",
    ) or re.search(
        rf"(?:甲方|乙方)[（(](?:许可方|出让方|让与方|转让方|卖方)[）)][：:]\s*(?P<name>{party_name_pattern})",
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
        and re.fullmatch(licensor, normalized_entity(patent_owner_match.group("name")))
    )
    licensor_direct_owner = bool(re.search(
        rf"{licensor}(?:是|系|为)(?:本合同|合同项下|标的|该|本)?(?:专利的)?专利权人|"
        rf"{licensor}(?:合法)?拥有(?:本合同|合同项下|标的|该|本)专利权",
        compact,
        re.I,
    ))
    licensor_is_patent_owner = named_entity_match or role_owner_match or licensor_direct_owner
    explicit_non_owner = bool(re.search(
        rf"{licensor}(?:并非|不是|非|并不是)(?:本合同|合同项下|标的|该|本)?(?:专利的)?专利权人", compact,
    ))
    named_entities_differ = bool(
        licensor_name_match and patent_owner_match
        and not named_entity_match and not role_owner_match
        and not re.search(r"待定|未知|未提供|未明确|__|许可方|甲方|乙方", patent_owner_match.group("name"))
    )
    owner_identity = (
        True if licensor_is_patent_owner and not explicit_non_owner
        else False if (explicit_non_owner or named_entities_differ) and not licensor_is_patent_owner
        else None
    )
    # A restriction on improvements is not evidence about sublicensing the
    # licensed patent. Keep the object and sentence boundary in this prerequisite.
    sublicense_permissions = set()
    from review_v2.clause_parser import parse_contract_clauses
    for clause in parse_contract_clauses(text or ""):
        if "改进" in str(clause.location or "") and not re.search(r"本专利|合同专利", clause.text):
            continue
        for sentence in re.split(r"[。；;\n]", clause.text):
            sentence = re.sub(r"\s+", "", sentence)
            if not re.search(r"分许可|再许可|转许可", sentence) or "改进" in sentence:
                continue
            if re.search(r"不得|禁止|不允许|无权|未经.{0,12}同意", sentence):
                sublicense_permissions.add(False)
            elif re.search(r"允许|可以|有权|可向|享有|同意", sentence):
                sublicense_permissions.add(True)
    sublicense_permission = next(iter(sublicense_permissions)) if len(sublicense_permissions) == 1 else None
    authority = bool(
        licensor_is_patent_owner
        or re.search(rf"{licensor}.{{0,65}}(?:合法权利人|合法授权主体|有权许可|有权授予|有权转让|有权签订本合同|有权签署本合同|有权提供本项技术|合法持有|完整权利)", compact)
    )
    claim_trigger = bool(
        re.search(r"(?:第三方|第三人).{0,55}(?:权利主张|指控|侵犯|侵权|侵权责任).{0,65}(?:被许可方|买方|受让方|甲方|许可权瑕疵)", compact)
        or re.search(r"(?:第三方|第三人).{0,30}(?:权利主张|主张|指控|侵权责任).{0,55}(?:被许可方|买方|受让方|甲方|许可权瑕疵|交涉|应诉)", compact)
        or re.search(r"(?:被许可方|买方|受让方).{0,45}(?:按约|依约|按照本合同|授权范围).{0,45}(?:第三方|第三人).{0,35}(?:权利主张|指控|侵犯|侵权)", compact)
        or re.search(r"(?:第三方|第三人).{0,55}(?:被许可方|买方|受让方).{0,45}(?:按约|依约|按照本合同|授权范围).{0,35}(?:权利主张|指控|侵犯|侵权)", compact)
        or bool(re.search(r"第三人侵权责任.{0,120}(?:负责与第三方交涉|负责交涉|应诉)", claim_scope))
    )
    claim_handling = bool(re.search(
        rf"{licensor}[^。；;]{{0,45}}(?:负责|应|须)[^。；;]{{0,30}}(?:交涉|处理|抗辩|应诉)",
        claim_scope,
    ))
    licensee_claim_handling = bool(re.search(
        # Do not cross an intervening licensor reference.  Without this
        # directional boundary, "被许可方遭索赔时，由许可方负责处理"
        # was incorrectly read as both parties handling the claim merely
        # because the licensee appeared earlier in the same sentence.
        rf"{licensee}(?:(?!{licensor})[^。；;]){{0,45}}(?:负责|应|须|自行)[^。；;]{{0,35}}(?:交涉|处理|抗辩|应诉)|"
        rf"(?:由|均由){licensee}[^。；;]{{0,15}}(?:自行)?(?:交涉|处理|抗辩|应诉)",
        claim_scope,
    ))
    claim_assistance = bool(re.search(
        rf"{licensor}[^。；;]{{0,55}}(?:提供|提交)[^。；;]{{0,35}}(?:专利|权属|技术来源|证明|资料|文件|协助)"
        rf"|{licensor}[^。；;]{{0,45}}(?:提供必要协助|协助|配合)[^。；;]{{0,30}}(?:抗辩|应诉|处理|交涉)?",
        claim_scope,
    ))
    litigation_handling = bool(re.search(
        rf"{licensor}[^。；;]{{0,25}}(?:负责|应|须)[^。；;]{{0,16}}(?:应诉|提起诉讼|处理诉讼|进行抗辩|负责抗辩)",
        claim_scope,
    ))
    licensee_litigation_handling = bool(re.search(
        rf"{licensee}[^。；;]{{0,25}}(?:负责|应|须|自行)[^。；;]{{0,20}}(?:应诉|提起诉讼|处理诉讼|进行抗辩|负责抗辩)",
        claim_scope,
    ))
    notification_requirement = bool(
        re.search(r"(?:收到|获悉).{0,35}第三方.{0,45}(?:应|须).{0,20}通知", claim_scope)
        or re.search(r"(?:被许可方|买方|受让方|甲方).{0,15}(?:应|须).{0,20}(?:收到|获悉).{0,35}第三方.{0,45}通知", claim_scope)
        or re.search(
            rf"(?:第三方|第三人).{{0,90}}{licensee}.{{0,70}}(?:应|须|必须).{{0,55}}通知{licensor}|"
            rf"{licensee}.{{0,120}}(?:第三方|第三人).{{0,80}}(?:应|须|必须).{{0,55}}通知{licensor}",
            claim_scope,
        )
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
    settlement_consultation = bool(re.search(
        r"(?:双方|许可方与被许可方|卖方与买方).{0,35}(?:和解).{0,25}(?:事先)?(?:协商|书面同意)|"
        r"(?:和解).{0,25}(?:应|须|必须).{0,12}(?:事先)?(?:协商|取得.{0,10}同意)",
        claim_scope,
    ))
    attorney_fee = licensor_bears(r"(?:合理)?律师费")
    litigation_cost = licensor_bears(r"(?:诉讼费|诉讼费用|仲裁费|程序费用)")
    legal_cost = licensor_bears(r"(?:合理)?(?:法律费用|法律服务费用)")
    direct_damage = licensor_bears(r"(?:直接经济损失|合理直接损失|直接损失)")
    general_liability = licensor_bears(r"(?:法律和经济责任|法律责任|经济责任|赔偿责任|损失)")
    # Coverage and direction are separate.  A clause allocating fees to the
    # licensee is adverse to that party, but it is not an absent allocation.
    attorney_fee_allocation = bool(re.search(r"律师费.{0,90}(?:由|均由).{0,25}(?:承担|负担)", claim_scope))
    litigation_cost_allocation = bool(re.search(
        r"(?:诉讼费|诉讼费用|行政处理费用|和解费用).{0,100}(?:由|均由).{0,25}(?:承担|负担)",
        claim_scope,
    ))
    third_party_compensation_allocation = bool(re.search(
        r"(?:赔偿费|赔偿费用|第三方赔偿|其他损失).{0,100}(?:由|均由).{0,25}(?:承担|负担)",
        claim_scope,
    )) or licensor_bears(r"(?:依法应承担的)?赔偿责任")
    claim_cost_bearer = (
        "LICENSEE" if re.search(
            r"(?:律师费|诉讼费|行政处理费用|和解费用|赔偿费|赔偿费用|停产损失|其他损失).{0,160}(?:由|均由)(?:被许可方|受让方|买方|甲方)(?:承担|负担)",
            claim_scope,
        ) else
        "LICENSOR" if attorney_fee or litigation_cost or legal_cost or third_party_compensation_allocation else
        "UNKNOWN"
    )
    licensee_broad_business_loss_allocation = bool(re.search(
        r"(?:停产损失|召回损失|业务中断损失|客户索赔)[^。；;]{0,100}"
        r"(?:由|均由)(?:被许可方|受让方|买方|甲方)(?:承担|负担)",
        claim_scope,
    ))
    def extract_party_liability_cap(party_pattern: str) -> tuple[Optional[float], str]:
        """Extract a cap only when the named party is the subject of liability.

        The counterparty may appear later merely as the fee/payment basis.  By
        requiring the party token before the liability phrase, that reference
        cannot be mistaken for a cap protecting the counterparty.
        """
        responsibility = (
            r"(?:累计承担的全部|累计承担的|承担的全部|全部)?"
            r"(?:赔偿|侵权|法律|经济)?责任"
        )
        for match in re.finditer(
            rf"{party_pattern}[^。；;]{{0,50}}?{responsibility}(?P<tail>[^。；;]{{0,160}})",
            claim_scope,
        ):
            tail = match.group("tail")
            percentage = re.search(
                r"(?:最高(?:也)?(?:不得)?超过|累计(?:最高)?不超过|(?:亦)?不得超过|不超过|"
                r"上限(?:为|是)?).{0,90}?(\d+(?:\.\d+)?)\s*%",
                tail,
            )
            if not percentage:
                percentage = re.search(
                    r"(\d+(?:\.\d+)?)\s*%.{0,24}?(?:为上限|以内|以下)",
                    tail,
                )
            if percentage:
                return _number(_decimal(percentage.group(1))), match.group(0)
        return None, ""

    licensor_cap_percentage, licensor_cap_text = extract_party_liability_cap(licensor)
    licensee_cap_percentage, licensee_cap_text = extract_party_liability_cap(licensee)
    if licensor_cap_percentage is None and licensee_cap_percentage is None:
        liability_cap_balance = "NO_CAPS"
    elif licensor_cap_percentage is not None and licensee_cap_percentage is None:
        liability_cap_balance = "LICENSOR_ONLY"
    elif licensor_cap_percentage is None and licensee_cap_percentage is not None:
        liability_cap_balance = "LICENSEE_ONLY"
    else:
        higher_cap = max(float(licensor_cap_percentage), float(licensee_cap_percentage))
        lower_cap = min(float(licensor_cap_percentage), float(licensee_cap_percentage))
        liability_cap_balance = (
            "BOTH_BALANCED"
            if higher_cap == 0 or lower_cap / higher_cap >= 0.8
            else "BOTH_ASYMMETRIC"
        )
    liability_cap_imbalance = bool(
        (
            licensor_cap_percentage is not None
            and licensee_cap_percentage is None
            and claim_cost_bearer == "LICENSEE"
        )
        or (
            licensor_cap_percentage is not None
            and licensee_cap_percentage is not None
            and float(licensor_cap_percentage) < float(licensee_cap_percentage) * 0.8
        )
    )
    liability_cap_exceptions = bool(re.search(
        r"(?:故意|重大过失|未披露.{0,20}权利瑕疵).{0,45}"
        r"(?:不适用|不受).{0,20}(?:责任上限|责任限制|赔偿上限)"
        r"|(?:责任上限|责任限制|赔偿上限).{0,45}"
        r"(?:不适用|不包括).{0,25}(?:故意|重大过失|未披露.{0,20}权利瑕疵)",
        claim_scope,
    ))
    replacement_remedy = bool(re.search(rf"{licensor}.{{0,90}}(?:提供|采取|负责).{{0,35}}(?:替代技术|替代方案|绕开侵权方案)", compact))
    license_cure = bool(re.search(rf"{licensor}.{{0,90}}(?:取得|补办|恢复).{{0,30}}(?:第三方许可|许可权|授权)", compact))
    refund_remedy = bool(re.search(rf"{licensor}.{{0,100}}(?:退还|返还).{{0,25}}(?:许可费|许可费用|使用费|价款)", compact))
    third_party_claim = {
        "authority_warranty": authority,
        "licensor_is_patent_owner": licensor_is_patent_owner,
        "licensor_owner_identity": owner_identity,
        "sublicense_permission": sublicense_permission,
        "claim_trigger": claim_trigger,
        "claim_handling": claim_handling,
        "licensee_claim_handling": licensee_claim_handling,
        "claim_assistance": claim_assistance,
        "litigation_handling": litigation_handling,
        "licensee_litigation_handling": licensee_litigation_handling,
        "attorney_fee": attorney_fee,
        "litigation_cost": litigation_cost,
        "legal_cost": legal_cost,
        "attorney_fee_allocation": attorney_fee_allocation or attorney_fee,
        "litigation_cost_allocation": litigation_cost_allocation or litigation_cost,
        "third_party_compensation_allocation": third_party_compensation_allocation,
        "claim_cost_allocation": attorney_fee_allocation or litigation_cost_allocation or third_party_compensation_allocation or attorney_fee or litigation_cost or legal_cost,
        "claim_cost_bearer": claim_cost_bearer,
        "licensee_broad_business_loss_allocation": licensee_broad_business_loss_allocation,
        "direct_damage": direct_damage,
        "notification_requirement": notification_requirement,
        "notification_deadline": notification_deadline,
        "defense_control": defense_control,
        "lawyer_selection": lawyer_selection,
        "settlement_authority": settlement_authority,
        "settlement_consultation": settlement_consultation,
        "replacement_remedy": replacement_remedy,
        "license_cure": license_cure,
        "refund_remedy": refund_remedy,
        "general_liability": general_liability,
        "licensor_liability_cap": licensor_cap_percentage is not None,
        "licensor_liability_cap_percentage": licensor_cap_percentage,
        "licensor_liability_cap_text": licensor_cap_text,
        "licensee_liability_cap": licensee_cap_percentage is not None,
        "licensee_liability_cap_percentage": licensee_cap_percentage,
        "licensee_liability_cap_text": licensee_cap_text,
        "liability_cap_balance": liability_cap_balance,
        "liability_cap_imbalance": liability_cap_imbalance,
        "liability_cap_exceptions": liability_cap_exceptions,
        "licensee_open_ended_infringement_liability": bool(
            claim_cost_bearer == "LICENSEE" and licensee_cap_percentage is None
        ),
        "explicit_process_gap": explicit_process_gap,
        "responsible_party": (
            "LICENSEE" if any((licensee_claim_handling, licensee_litigation_handling)) or claim_cost_bearer == "LICENSEE"
            else "LICENSOR" if any((claim_handling, litigation_handling, attorney_fee, litigation_cost, direct_damage, general_liability))
            else "UNKNOWN"
        ),
    }
    from review_v2.clause_parser import parse_contract_clauses
    response_facts = extract_claim_response_facts(parse_contract_clauses(text), licensor, licensee)
    for key in (
        "claim_trigger", "claim_handling", "licensee_claim_handling", "claim_assistance",
        "notification_requirement", "notification_deadline", "defense_control", "lawyer_selection",
        "settlement_authority", "settlement_consultation", "settlement_non_prejudice",
        "claim_cost_allocation", "liability_responsible_party",
        "replacement_remedy", "license_cure", "refund_remedy",
    ):
        third_party_claim[key] = bool(response_facts.get(key))
    third_party_claim["response_element_evidence"] = response_facts
    third_party_claim["response_party_patterns"] = {"provider": licensor, "recipient": licensee}
    # Keep specific registry fields at the same granularity as their source
    # predicates. The independent broad responsibility model remains intact.
    for key in ("administrative_handling", "litigation_handling", "attorney_fee", "litigation_cost", "direct_damage"):
        third_party_claim[key] = any(row.get("actor") == "LICENSOR" for row in response_facts.get(key, []))
    third_party_claim["attorney_fee_allocation"] = bool(response_facts.get("attorney_fee"))
    third_party_claim["litigation_cost_allocation"] = bool(response_facts.get("litigation_cost"))
    third_party_claim["third_party_compensation_allocation"] = bool(response_facts.get("third_party_compensation_allocation"))
    # Actor-sensitive consumers must use the same scoped response facts. A
    # recipient in the trigger cannot own the provider's later response verb.
    third_party_claim["licensee_litigation_handling"] = any(
        row.get("actor") == "LICENSEE" for row in response_facts.get("litigation_handling", []))
    responsible_actors = {row["actor"] for row in response_facts.get("liability_responsible_party", [])
                          if row.get("actor")}
    if not responsible_actors:
        responsible_actors = {row["actor"] for key in ("claim_handling", "licensee_claim_handling", "litigation_handling")
                              for row in response_facts.get(key, []) if row.get("actor")}
    third_party_claim["responsible_party"] = (
        next(iter(responsible_actors)) if len(responsible_actors) == 1
        else "MIXED" if responsible_actors else "UNKNOWN")
    third_party_claim["general_liability"] = any(
        row.get("actor") == "LICENSOR" for row in response_facts.get("liability_responsible_party", []))
    cost_actors = {row.get("actor") for row in response_facts.get("claim_cost_allocation", []) if row.get("actor")}
    if cost_actors:
        # A capped provider damages clause cannot reverse the actor of a
        # separate clause assigning claim-handling costs to the recipient.
        third_party_claim["claim_cost_bearer"] = next(iter(cost_actors)) if len(cost_actors) == 1 else "MIXED"
        third_party_claim["licensee_open_ended_infringement_liability"] = bool(
            "LICENSEE" in cost_actors and licensee_cap_percentage is None
        )
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
        r"合同总价款|合同总价|合同总额|合同价款|成交总额|"
        r"项目总预算|研发预算总额|项目研发预算总额|投资总额|投入总额|"
        r"(?:研发|开发|技术开发)?费用(?:总价|总额)|"
        r"技术服务费总额|技术服务费用|技术服务费|技术咨询费用|技术咨询报酬|服务报酬|专利(?:申请)?权转让价款(?:总额|总价)?|"
        r"入门费总额|本合同入门费|"
        r"固定许可费总额|固定许可费|许可使用费总额|专利实施许可费总额|"
        r"专利许可费|专利实施许可费|后续技术开发费|技术开发费|"
        r"固定技术转让费总额|固定技术转让费|技术转让费总额|技术转让费|"
        r"分项[一二三四五六七八九十\d]+(?:的)?合同价"
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
        rf"(?P<label>{label})(?P<context>[^。；\n]{{0,35}}?)(?:为|共计|合计|总计|：|:)\s*(?:人民币)?\s*{SCALED_CNY_PATTERN}",
        re.I,
    )
    for match in plain_pattern.finditer(text or ""):
        if "%" in match.group(0) or any(row["start_offset"] == match.start() for row in candidates):
            continue
        candidates.append({
            "value": _number(_scaled_cny(match.group("amount"), match.group("unit"))),
            "label": match.group("label"),
            "currency": "CNY",
            "certainty": "provisional" if any(term in match.group(0) for term in ("暂定", "暂估", "预估")) else "explicit",
            "raw_text": match.group(0).strip(),
            "start_offset": match.start(),
            "end_offset": match.end(),
        })
    foreign_pattern = re.compile(
        rf"(?P<label>{label})(?P<context>[\s\S]{{0,60}}?)(?:为|共计|合计|总计|：|:)?\s*"
        r"(?:(?P<prefix_currency>EUR|USD|欧元|美元)\s*)?"
        r"(?P<amount>[0-9][0-9,]*(?:\.\d+)?)\s*(?P<suffix_currency>EUR|USD|欧元|美元)?",
        re.I,
    )
    for match in foreign_pattern.finditer(text or ""):
        currency_token = match.group("prefix_currency") or match.group("suffix_currency")
        if not currency_token or "%" in match.group(0) or any(row["start_offset"] == match.start() for row in candidates):
            continue
        currency = "EUR" if str(currency_token).upper() == "EUR" or currency_token == "欧元" else "USD"
        candidates.append({
            "value": _number(_decimal(match.group("amount"))),
            "label": match.group("label"),
            "currency": currency,
            "certainty": "provisional" if any(term in match.group(0) for term in ("暂定", "暂估", "预估")) else "explicit",
            "raw_text": match.group(0).strip(),
            "start_offset": match.start(),
            "end_offset": match.end(),
        })
    document_hash = _classification_document_hash(text or "")
    for candidate in candidates:
        candidate.setdefault("source_document", document_hash)
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
    elif any(term in stage_source for term in ("最终验收", "验收合格", "尾款", "末期")):
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
    paired_node_pattern = re.compile(
        rf"(?P<context>[^。；\n]{{0,55}}?)(?P<pct>\d+(?:\.\d+)?)\s*%[^。；\n]{{0,35}}?(?:即|为|计)\s*(?:人民币)?\s*{SCALED_CNY_PATTERN}",
        re.I,
    )
    nodes: List[Dict[str, Any]] = []
    seen: set[tuple[int, int, str, str, str]] = set()
    occupied_ranges: List[tuple[int, int]] = []
    facts_before_dedup: List[Dict[str, Any]] = []

    def overlaps_existing(start: int, end: int) -> bool:
        return any(start < existing_end and end > existing_start for existing_start, existing_end in occupied_ranges)

    def add_node(
        *,
        start: int,
        end: int,
        raw_text: str,
        context: str,
        percentage: Optional[Decimal],
        amount: Optional[Decimal],
        currency: str,
        retention_included: bool = False,
    ) -> None:
        source = _source_context(value, start, context)
        sequence = len(facts_before_dedup) + 1
        fact = {
            "fact_id": f"PAY-{sequence:03d}-{hashlib.sha256(f'{start}:{end}:{raw_text}'.encode('utf-8')).hexdigest()[:10]}",
            "source_document": _classification_document_hash(value),
            "source_clause": source["trigger"],
            "source_location": source["source_location"],
            "sequence": sequence,
            "stage": source["stage"],
            "trigger": source["trigger"],
            "condition": source["trigger"],
            "percentage": _number(percentage) if percentage is not None else None,
            "amount": _number(amount) if amount is not None else None,
            "currency": currency,
            "payment_type": source["stage"],
            "is_deposit": source["stage"] == "initial",
            "is_stage_payment": source["stage"] == "milestone",
            "is_final_payment": source["stage"] == "final",
            "is_retention": source["stage"] == "retention",
            "raw_text": raw_text,
            "start_offset": start,
            "end_offset": end,
            "context": context.strip(),
            "retention_included": retention_included,
            "percentage_inferred": False,
            "amount_inferred": False,
        }
        facts_before_dedup.append(dict(fact))
        key = (start, end, source["trigger"], str(percentage), str(amount))
        if key in seen:
            return
        seen.add(key)
        nodes.append(fact)
        occupied_ranges.append((start, end))

    for match in paired_node_pattern.finditer(value):
        pct = _decimal(match.group("pct"))
        amount = _scaled_cny(match.group("amount"), match.group("unit"))
        context = match.group("context")
        if any(term in context for term in ("上述付款比例合计", "付款比例合计", "金额合计")):
            continue
        source = _source_context(value, match.start(), context)
        included_retention = "包含" in f"{context}{source['trigger']}" and any(term in f"{context}{source['trigger']}" for term in ("质保", "保证金"))
        add_node(
            start=match.start(), end=match.end(), raw_text=match.group(0).strip(),
            context=context, percentage=pct, amount=amount, currency="CNY",
            retention_included=included_retention,
        )

    paired_foreign_pattern = re.compile(
        r"(?P<context>[^。；\n]{0,80}?)(?P<pct>\d+(?:\.\d+)?)\s*%[^。；\n]{0,35}?(?:即|为|计)?\s*"
        r"(?:(?P<prefix_currency>EUR|USD|欧元|美元)\s*)"
        r"(?P<amount>[0-9][0-9,]*(?:\.\d+)?)\s*(?P<suffix_currency>EUR|USD|欧元|美元)?",
        re.I,
    )
    for match in paired_foreign_pattern.finditer(value):
        if overlaps_existing(match.start(), match.end()):
            continue
        currency_token = match.group("prefix_currency") or match.group("suffix_currency")
        currency = "EUR" if str(currency_token).upper() == "EUR" or currency_token == "欧元" else "USD"
        context = match.group("context")
        if any(term in context for term in ("上述付款比例合计", "付款比例合计", "金额合计")):
            continue
        add_node(
            start=match.start(), end=match.end(), raw_text=match.group(0).strip(),
            context=context, percentage=_decimal(match.group("pct")),
            amount=_decimal(match.group("amount")), currency=currency,
        )

    cross_line_pattern = re.compile(
        r"(?P<pct>\d+(?:\.\d+)?)\s*%\s*(?:\r?\n|\s)*(?:即|为|计)\s*[：:]?\s*"
        r"(?:\r?\n|\s)*(?:(?P<prefix_currency>EUR|USD|欧元|美元)\s*)?"
        r"(?P<amount>[0-9][0-9,]*(?:\.\d+)?)\s*(?P<unit>万)?\s*(?P<currency>EUR|欧元|美元|USD|元)?",
        re.I,
    )
    for match in cross_line_pattern.finditer(value):
        if overlaps_existing(match.start(), match.end()):
            continue
        pct = _decimal(match.group("pct"))
        currency_token = match.group("prefix_currency") or match.group("currency")
        if not currency_token:
            continue
        amount = _scaled_cny(match.group("amount"), match.group("unit")) if currency_token == "元" else _decimal(match.group("amount"))
        context_start = max(0, match.start() - 100)
        context = value[context_start:match.start()]
        if any(term in context[-60:] for term in ("提成率", "计算示例", "应付提成费", "净销售额")):
            continue
        source = _source_context(value, match.start(), context[-55:])
        currency = (
            "EUR" if str(currency_token).upper() == "EUR" or currency_token == "欧元"
            else "USD" if str(currency_token).upper() == "USD" or currency_token == "美元"
            else "CNY"
        )
        add_node(
            start=match.start(), end=match.end(), raw_text=match.group(0).strip(),
            context=context[-55:], percentage=pct, amount=amount, currency=currency,
        )

    # A payment obligation may state only an amount (for example a fixed tail
    # payment or retention).  Such a node remains a first-class fact and must
    # not disappear merely because the clause omits a percentage.
    amount_only_pattern = re.compile(
        r"(?P<context>[^。；\n]{0,100}?(?:首期|首笔|第[一二三四五六七八九十\d]+(?:期|笔|阶段)|尾款|余款|剩余款项|质保金|保证金|验收|交付|支付条件|合同(?:签订|签署|生效)|协议生效|双方(?:签字|盖章)|项目启动|开发项目启动|完成首次量产|首次量产|(?:提交|交付|完成)[^。；\n]{0,40})[^。；\n]{0,80}?)"
        r"(?:应|须|将|再|予以|向[^。；\n]{0,12})?(?:支付|付清|给付)\s*(?:剩余|尾款|余款|质保金|保证金|款项)?\s*"
        r"(?:(?P<prefix_currency>EUR|USD|欧元|美元)\s*)?"
        r"(?:人民币)?\s*(?P<amount>[0-9][0-9,]*(?:\.\d+)?)\s*(?P<unit>万)?\s*(?P<currency>EUR|欧元|美元|USD|元)?",
        re.I,
    )
    excluded_amount_context = (
        "违约金", "赔偿", "罚息", "滞纳金", "逾期", "应付未付",
        "损失", "返还", "退还", "退款", "违反", "未达到", "免费整改", "泄密",
    )
    for match in amount_only_pattern.finditer(value):
        if overlaps_existing(match.start(), match.end()):
            continue
        context = match.group("context")
        compact_context = re.sub(r"\s+", "", context)
        if (
            any(term in compact_context for term in excluded_amount_context)
            or re.search(r"收到.{0,35}(?:支付|给付)", compact_context)
        ):
            continue
        currency_token = match.group("prefix_currency") or match.group("currency")
        if not currency_token:
            continue
        currency = (
            "EUR" if str(currency_token).upper() == "EUR" or currency_token == "欧元"
            else "USD" if str(currency_token).upper() == "USD" or currency_token == "美元"
            else "CNY"
        )
        add_node(
            start=match.start(), end=match.end(), raw_text=match.group(0).strip(),
            context=context, percentage=None,
            amount=(
                _scaled_cny(match.group("amount"), match.group("unit"))
                if currency == "CNY" else _decimal(match.group("amount"))
            ),
            currency=currency,
        )

    # Percentage-only nodes are also retained.  Their amount can be derived
    # from an explicit contract total without changing the source fact.
    percentage_only_pattern = re.compile(
        r"(?P<context>[^。；\n]{0,100}?(?:首期|首笔|第[一二三四五六七八九十\d]+(?:期|笔|阶段)|尾款|余款|剩余款项|质保金|保证金|验收|交付|支付条件)[^。；\n]{0,80}?)"
        r"(?:应|须|将|再|予以|向[^。；\n]{0,12})?(?:支付|扣留|保留)[^。；\n]{0,20}?(?P<pct>\d+(?:\.\d+)?)\s*%",
        re.I,
    )
    for match in percentage_only_pattern.finditer(value):
        if overlaps_existing(match.start(), match.end()):
            continue
        context = match.group("context")
        if any(term in re.sub(r"\s+", "", context) for term in excluded_amount_context):
            continue
        add_node(
            start=match.start(), end=match.end(), raw_text=match.group(0).strip(),
            context=context, percentage=_decimal(match.group("pct")), amount=None, currency="CNY",
        )

    dynamic_remainder_pattern = re.compile(
        r"(?P<context>[^。；\n]{0,100}?(?:验收|交付|尾款|末期|最后一笔|支付条件)[^。；\n]{0,80}?)"
        r"(?:应|须|将|再|予以|向[^。；\n]{0,12})?(?:支付|付清)\s*(?P<dynamic>剩余款项|剩余价款|剩余合同价款|余款|尾款)",
        re.I,
    )
    for match in dynamic_remainder_pattern.finditer(value):
        if overlaps_existing(match.start(), match.end()):
            continue
        context = match.group("context")
        if any(term in re.sub(r"\s+", "", context) for term in excluded_amount_context):
            continue
        add_node(
            start=match.start(), end=match.end(), raw_text=match.group(0).strip(),
            context=context, percentage=None, amount=None, currency="CNY",
        )
        nodes[-1]["dynamic_expression"] = "REMAINDER"

    # R&D investment and budget are another parent/child amount relationship.
    # Treat explicit party contributions as amount nodes so the shared
    # deterministic consistency rule can compare them with an explicit project
    # or R&D budget.  This is intentionally independent from payment wording:
    # a contribution is not a payment instalment, but the arithmetic invariant
    # (sum(children) == declared parent amount) is the same.
    budget_candidates = [
        row for row in total_candidates
        if any(term in str(row.get("label") or "") for term in (
            "项目总预算", "研发预算", "项目研发预算", "投资总额", "投入总额",
        ))
    ]
    investment_node_pattern = re.compile(
        rf"(?P<context>(?:甲方|乙方|丙方|丁方|一方|另一方)[^。；\n]{{0,90}}?)"
        rf"(?:投入|计划投入|预计投入)(?:研发)?(?:资金|费用|经费)?\s*(?:为|共计|合计|：|:)?\s*"
        rf"(?:人民币)?\s*{SCALED_CNY_PATTERN}",
        re.I,
    )
    if budget_candidates:
        for match in investment_node_pattern.finditer(value):
            if overlaps_existing(match.start(), match.end()):
                continue
            compact_context = re.sub(r"\s+", "", match.group("context"))
            if any(term in compact_context for term in ("违约金", "损失", "返还", "退款")):
                continue
            add_node(
                start=match.start(), end=match.end(), raw_text=match.group(0).strip(),
                context=match.group("context"), percentage=None,
                amount=_scaled_cny(match.group("amount"), match.group("unit")),
                currency="CNY",
            )
            nodes[-1]["consistency_context"] = "BUDGET_INVESTMENT"
            nodes[-1]["payment_type"] = "research_investment"
            nodes[-1]["stage"] = "investment"

    nodes.sort(key=lambda row: (int(row.get("start_offset") or 0), int(row.get("end_offset") or 0)))

    # A contract can contain several independently priced components.  A
    # percentage only has meaning against its own component price, so bind each
    # payment node to the nearest preceding explicit price fact before doing
    # any inference or arithmetic.  The overall contract total remains a
    # separate amount-only reconciliation base.
    global_total_candidates = [
        row for row in total_candidates
        if any(term in str(row.get("label") or "") for term in ("合同总价", "合同总额", "合同价款"))
    ]
    global_total_candidate = global_total_candidates[0] if global_total_candidates else (
        total_candidates[0] if len(total_candidates) == 1 else None
    )
    component_total_candidates = [
        row for row in total_candidates
        if row is not global_total_candidate
        and not any(term in str(row.get("label") or "") for term in ("合同总价", "合同总额", "合同价款"))
    ]
    component_total_sum: Optional[Decimal] = None
    component_total_delta: Optional[Decimal] = None
    if global_total_candidate and len(component_total_candidates) >= 2:
        component_currencies = {str(row.get("currency") or "CNY") for row in component_total_candidates}
        global_currency = str(global_total_candidate.get("currency") or "CNY")
        if component_currencies == {global_currency}:
            component_total_sum = sum(
                (_decimal(str(row.get("value"))) for row in component_total_candidates),
                Decimal("0"),
            )
            component_total_delta = component_total_sum - _decimal(str(global_total_candidate.get("value")))

    def node_base_candidate(node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if node.get("consistency_context") == "BUDGET_INVESTMENT" and budget_candidates:
            return min(
                budget_candidates,
                key=lambda row: abs(int(row.get("start_offset") or 0) - int(node.get("start_offset") or 0)),
            )
        node_start = int(node.get("start_offset") or 0)
        node_language = re.sub(
            r"\s+",
            "",
            " ".join((
                str(node.get("raw_text") or ""),
                str(node.get("context") or ""),
                str(node.get("source_clause") or ""),
            )),
        )
        # An instalment explicitly expressed against the whole contract price
        # must not inherit the nearest preceding component price.
        if any(term in node_language for term in ("合同总价", "合同总额", "合同价款", "成交总额")):
            return global_total_candidate
        node_component = re.search(
            r"分项(?P<key>[一二三四五六七八九十\d]+)",
            node_language,
        )
        if node_component:
            component_key = node_component.group("key")
            exact_components = [
                candidate for candidate in component_total_candidates
                if re.search(
                    rf"分项{re.escape(component_key)}(?:的)?合同价",
                    re.sub(r"\s+", "", str(candidate.get("raw_text") or candidate.get("label") or "")),
                )
            ]
            if exact_components:
                return min(
                    exact_components,
                    key=lambda row: abs(int(row.get("start_offset") or 0) - node_start),
                )
        preceding = [
            candidate for candidate in component_total_candidates
            if int(candidate.get("end_offset") or 0) <= node_start
        ]
        if preceding:
            return max(preceding, key=lambda row: int(row.get("end_offset") or 0))
        return global_total_candidate

    for sequence, node in enumerate(nodes, start=1):
        node["sequence"] = sequence
        base_candidate = node_base_candidate(node)
        base_amount = _decimal(str(base_candidate["value"])) if base_candidate else total
        group_key = (
            "budget_investment"
            if node.get("consistency_context") == "BUDGET_INVESTMENT" else
            f"component:{base_candidate.get('start_offset')}"
            if base_candidate and base_candidate in component_total_candidates
            else "contract_total"
        )
        node["payment_group_id"] = group_key
        node["payment_group_label"] = str((base_candidate or {}).get("label") or "合同总价")
        node["payment_base_amount"] = _number(base_amount) if base_amount is not None else None
        node["payment_base_fact_offset"] = (base_candidate or {}).get("start_offset")
        percentage = node.get("percentage")
        amount = node.get("amount")
        if base_amount is not None and amount is None and percentage is not None:
            inferred_amount = base_amount * _decimal(str(percentage)) / Decimal("100")
            node["effective_amount"] = _number(inferred_amount)
            node["amount_inferred"] = True
        else:
            node["effective_amount"] = amount

    grouped_nodes: Dict[str, List[Dict[str, Any]]] = {}
    for node in nodes:
        grouped_nodes.setdefault(str(node.get("payment_group_id") or "contract_total"), []).append(node)

    for group_nodes in grouped_nodes.values():
        base_amount_value = group_nodes[0].get("payment_base_amount")
        base_amount = _decimal(str(base_amount_value)) if base_amount_value is not None else None
        dynamic_nodes = [node for node in group_nodes if node.get("dynamic_expression") == "REMAINDER"]
        if base_amount is not None and len(dynamic_nodes) == 1:
            dynamic_node = dynamic_nodes[0]
            other_amounts = [
                _decimal(str(node.get("effective_amount")))
                for node in group_nodes if node is not dynamic_node and node.get("effective_amount") is not None
            ]
            if len(other_amounts) == len(group_nodes) - 1:
                inferred_remainder = base_amount - sum(other_amounts, Decimal("0"))
                if inferred_remainder >= 0:
                    dynamic_node["effective_amount"] = _number(inferred_remainder)
                    dynamic_node["amount_inferred"] = True

        for node in group_nodes:
            percentage = node.get("percentage")
            amount = node.get("effective_amount")
            if base_amount is not None and percentage is None and amount is not None and base_amount != 0:
                inferred_percentage = _decimal(str(amount)) / base_amount * Decimal("100")
                node["effective_percentage"] = _number(inferred_percentage)
                node["percentage_inferred"] = True
            else:
                node["effective_percentage"] = percentage

    payment_groups: List[Dict[str, Any]] = []
    node_mismatches: List[Dict[str, Any]] = []
    for group_id, group_nodes in grouped_nodes.items():
        effective_group_nodes = [node for node in group_nodes if not node["retention_included"]]
        known_percentages = [node.get("effective_percentage") for node in effective_group_nodes if node.get("effective_percentage") is not None]
        known_amounts = [node.get("effective_amount") for node in effective_group_nodes if node.get("effective_amount") is not None]
        group_percentage_total = sum((_decimal(str(value)) for value in known_percentages), Decimal("0"))
        group_amount_total = sum((_decimal(str(value)) for value in known_amounts), Decimal("0"))
        group_percentage_complete = bool(effective_group_nodes) and len(known_percentages) == len(effective_group_nodes)
        group_amount_complete = bool(effective_group_nodes) and len(known_amounts) == len(effective_group_nodes)
        base_amount_value = group_nodes[0].get("payment_base_amount")
        base_amount = _decimal(str(base_amount_value)) if base_amount_value is not None else None
        if base_amount and group_percentage_complete:
            # Aggregate inferred amounts before division. Summing serialized
            # float thirds invents a percentage discrepancy on exact amounts.
            inferred_amounts = sum((_decimal(str(n['effective_amount'])) for n in effective_group_nodes
                                    if n.get('percentage_inferred')), Decimal('0'))
            declared_percentages = sum((_decimal(str(n['percentage'])) for n in effective_group_nodes
                                        if not n.get('percentage_inferred') and n.get('percentage') is not None), Decimal('0'))
            group_percentage_total = declared_percentages + inferred_amounts / base_amount * Decimal('100')
        group_delta = group_amount_total - base_amount if base_amount is not None and group_amount_complete else None
        group_mismatches: List[Dict[str, Any]] = []
        if base_amount is not None:
            for node in group_nodes:
                if node.get("percentage") is None or node.get("amount") is None:
                    continue
                expected = base_amount * _decimal(str(node["percentage"])) / Decimal("100")
                actual = _decimal(str(node["amount"]))
                if abs(expected - actual) > Decimal("0.01"):
                    mismatch = {
                        "node": node.get("sequence"),
                        "payment_group_id": group_id,
                        "payment_group_label": node.get("payment_group_label"),
                        "base_amount": _number(base_amount),
                        "percentage": node["percentage"],
                        "expected_amount": _number(expected),
                        "actual_amount": node["amount"],
                        "delta": _number(actual - expected),
                    }
                    group_mismatches.append(mismatch)
                    node_mismatches.append(mismatch)
        group_has_complete_schedule = len(effective_group_nodes) >= 2
        group_inconsistent = bool(effective_group_nodes) and (
            (group_percentage_complete and len(effective_group_nodes) >= 2 and group_percentage_total != Decimal("100"))
            or (group_has_complete_schedule and group_delta is not None and abs(group_delta) > Decimal("0.01"))
            or bool(group_mismatches)
        )
        payment_groups.append({
            "group_id": group_id,
            "label": group_nodes[0].get("payment_group_label"),
            "base_amount": _number(base_amount) if base_amount is not None else None,
            "base_fact_offset": group_nodes[0].get("payment_base_fact_offset"),
            "node_fact_ids": [str(node.get("fact_id") or "") for node in group_nodes],
            "percentages": [node.get("effective_percentage") for node in effective_group_nodes],
            "amounts": [node.get("effective_amount") for node in effective_group_nodes],
            "percentage_total": _number(group_percentage_total),
            "amount_total": _number(group_amount_total),
            "amount_delta": _number(group_delta) if group_delta is not None else None,
            "percentage_total_complete": group_percentage_complete,
            "percentage_total_inferred": bool(effective_group_nodes) and all(
                node.get("percentage") is None and node.get("effective_percentage") is not None
                for node in effective_group_nodes
            ),
            "amount_total_complete": group_amount_complete,
            "node_mismatches": group_mismatches,
            "status": "INCONSISTENT" if group_inconsistent else "CONSISTENT" if base_amount is not None else "INSUFFICIENT_DATA",
        })

    effective_nodes = [node for node in nodes if not node["retention_included"]]
    known_amounts = [node.get("effective_amount") for node in effective_nodes if node.get("effective_amount") is not None]
    amount_total = sum((_decimal(str(value)) for value in known_amounts), Decimal("0"))
    complete_amount_total = bool(effective_nodes) and len(known_amounts) == len(effective_nodes)
    if len(payment_groups) == 1:
        percentage_total = _decimal(str(payment_groups[0]["percentage_total"]))
        complete_percentage_total = bool(payment_groups[0]["percentage_total_complete"])
    elif total is not None and complete_amount_total and total != 0:
        percentage_total = amount_total / total * Decimal("100")
        complete_percentage_total = True
    else:
        percentage_total = None
        complete_percentage_total = False
    amount_delta = amount_total - total if total is not None and complete_amount_total else None
    direction_rows: List[Dict[str, Any]] = []
    for node in nodes:
        start = int(node.get("start_offset") or 0)
        end = int(node.get("end_offset") or start)
        line_start = value.rfind("\n", 0, start) + 1
        line_end = value.find("\n", end)
        if line_end < 0:
            line_end = len(value)
        source_segment = value[line_start:line_end].strip()
        payee_match = re.search(
            r"支付给(?P<party>委托方|咨询方|甲方|乙方|服务方|服务提供方|服务接受方|受托方|许可方|被许可方|转让方|受让方)",
            re.sub(r"\s+", "", source_segment),
        )
        payer_match = re.search(
            r"由(?P<party>委托方|咨询方|甲方|乙方|服务方|服务提供方|服务接受方|受托方|许可方|被许可方|转让方|受让方).{0,80}支付给",
            re.sub(r"\s+", "", source_segment),
        )
        node["payment_direction"] = {
            "payer": payer_match.group("party") if payer_match else "",
            "payee": payee_match.group("party") if payee_match else "",
            "source_text": source_segment,
        }
        if payee_match:
            direction_rows.append({
                "fact_id": node.get("fact_id"),
                "payer": payer_match.group("party") if payer_match else "",
                "payee": payee_match.group("party"),
                "source_text": source_segment,
                "start_offset": line_start,
                "end_offset": line_end,
            })
    payee_counts: Dict[str, int] = {}
    for row in direction_rows:
        payee_counts[row["payee"]] = payee_counts.get(row["payee"], 0) + 1
    dominant_payee = max(payee_counts, key=payee_counts.get) if payee_counts else ""
    direction_outliers = [row for row in direction_rows if dominant_payee and row["payee"] != dominant_payee]

    inconsistent = bool(nodes) and (
        any(group.get("status") == "INCONSISTENT" for group in payment_groups)
        or (amount_delta is not None and abs(amount_delta) > Decimal("0.01"))
        or (component_total_delta is not None and abs(component_total_delta) > Decimal("0.01"))
        or bool(node_mismatches)
        or bool(direction_outliers)
    )
    result = {
        "status": "INCONSISTENT" if inconsistent else "CONSISTENT" if nodes and total is not None else "INSUFFICIENT_DATA",
        "contract_total": _number(total) if total is not None else None,
        "contract_total_candidates": total_candidates,
        "percentage_total": _number(percentage_total) if percentage_total is not None else None,
        "amount_total": _number(amount_total),
        "amount_delta": _number(amount_delta) if amount_delta is not None else None,
        "percentage_total_complete": complete_percentage_total,
        "amount_total_complete": complete_amount_total,
        "nodes": nodes,
        "payment_groups": payment_groups,
        "global_total_candidate": global_total_candidate,
        "component_total_candidates": component_total_candidates,
        "component_total_sum": _number(component_total_sum) if component_total_sum is not None else None,
        "component_total_delta": _number(component_total_delta) if component_total_delta is not None else None,
        "payment_fact_count": len(nodes),
        "facts_before_dedup": facts_before_dedup,
        "facts_after_dedup": [dict(node) for node in nodes],
        "node_mismatches": node_mismatches,
        "payment_direction_facts": direction_rows,
        "dominant_payee": dominant_payee,
        "payment_direction_outliers": direction_outliers,
        "overall_percentage_inferred_from_amounts": bool(len(payment_groups) > 1 and percentage_total is not None),
        "currency": next((row.get("currency") for row in nodes if row.get("currency")), next((row.get("currency") for row in total_candidates if row.get("currency")), "CNY")),
        "consistency_context": (
            "BUDGET_INVESTMENT"
            if nodes and all(node.get("consistency_context") == "BUDGET_INVESTMENT" for node in nodes)
            else "PAYMENT_SCHEDULE"
        ),
        "input_document_hash": _classification_document_hash(value),
        "input_fact_ids": [
            *[f"TOTAL-{index}" for index, _ in enumerate(total_candidates, start=1)],
            *[str(node.get("fact_id") or "") for node in nodes if node.get("fact_id")],
        ],
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
    compact_value = re.sub(r"\s+", "", value)
    service_start = _first_date(value, (
        r"服务期限[\s\S]{0,45}",
        r"服务开始[^。\n]{0,20}",
        r"履行期限[^。\n]{0,35}",
        r"合作期限[^。\n]{0,55}",
        r"开发周期[^。\n]{0,55}",
        r"开发期限[^。\n]{0,80}",
    ))
    service_end: Optional[str] = None
    for period_label in ("服务期限", "履行期限", "合作期限", "开发周期", "开发期限"):
        service_period_match = re.search(
            re.escape(period_label)
            + r"[^。\n]{0,25}?(20\d{2}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)\s*(?:至|到|[-—~～])\s*"
            r"(20\d{2}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)",
            value,
        )
        if not service_period_match:
            continue
        end_match = DATE_PATTERN.search(service_period_match.group(2))
        service_end = _iso(end_match) if end_match else None
        break
    if not service_end:
        # Development contracts commonly state a start date plus a duration and
        # then repeat only the calculated end date ("即至……").  The end date is
        # still an explicit contractual boundary and must participate in the
        # same timeline graph as service/consulting periods.
        development_end_match = re.search(
            r"(?:开发期限|开发周期|研发期限|项目期限)[^。\n]{0,100}?"
            r"(?:即)?至\s*(20\d{2}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)",
            value,
        )
        if development_end_match:
            end_match = DATE_PATTERN.search(development_end_match.group(1))
            service_end = _iso(end_match) if end_match else None
    # A licence can begin before the agreement is signed just as a service or
    # development phase can.  Keep the licence start as its own fact so the
    # shared TECH-SHARED-03 comparison is transaction-neutral.
    license_start = _first_date(value, (
        r"(?:专利)?(?:实施)?许可期限\s*[：:]?\s*(?:自)?\s*20\d{2}年\d{1,2}月\d{1,2}日",
        r"(?:专利)?(?:实施)?许可(?:开始|起始)(?:日期|时间)?[^。\n]{0,25}",
        r"(?:许可权|实施权)[^。\n]{0,18}(?:自|从)\s*20\d{2}年\d{1,2}月\d{1,2}日(?:起|开始)",
    ))
    transfer_start = _first_date(value, (
        r"(?:技术)?转让期限[^。\n]{0,45}(?:自|从)\s*20\d{2}年\d{1,2}月\d{1,2}日(?:起|开始|计算)?",
        r"(?:受让方|甲方)(?:的)?(?:技术)?使用权[^。\n]{0,35}(?:自|从)\s*20\d{2}年\d{1,2}月\d{1,2}日(?:起|开始|计算)?",
        r"(?:技术转让期限|受让方使用权|甲方使用权)[^。\n]{0,45}20\d{2}年\d{1,2}月\d{1,2}日",
    ))
    data_deadline = _first_date(value, (
        r"(?:第一批|首批)[^。\n]{0,12}技术资料[\s\S]{0,45}?(?:应于|应在|交付时间)[\s\S]{0,30}",
        r"技术资料交付时间[\s\S]{0,35}",
        r"(?:提供|提交)[^。\n]{0,12}(?:资料|数据)[^。\n]{0,35}",
        r"(?:资料|数据)[^。\n]{0,18}(?:提供|提交)[^。\n]{0,35}",
        r"应在\s*20\d{2}年\d{1,2}月\d{1,2}日前[^。\n]{0,30}(?:资料|数据)",
        r"(?:甲方|委托方|客户)[^。\n]{0,8}应在\s*20\d{2}年\d{1,2}月\d{1,2}日前[^。\n]{0,20}(?:提供|提交)",
    ))
    # A date merely appearing shortly after the word "签订" is not necessarily
    # the signing date (the next field may be a performance/effective period).
    # Bind the date to its own signing label instead of using a proximity scan.
    signature_dates: List[str] = []
    signature_date_pattern = re.compile(
        r"(?:合同)?(?:签订|签署|签约|签名|盖章)(?:时间|日期|日)?\s*[：:]?\s*"
        r"(20\d{2})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日",
    )
    for match in signature_date_pattern.finditer(value):
        signature_dates.append(
            date(int(match.group(1)), int(match.group(2)), int(match.group(3))).isoformat()
        )
    contract_sign_date = max(signature_dates) if signature_dates else None
    effective_date = _first_date(value, (
        r"(?:合同生效日期|本合同生效日期|生效日期为|生效时间为|双方最后批准日期)[^。\n]{0,45}",
        # "有效期限" may describe a service/performance period and must not be
        # promoted to an effective date.  Only the explicit legal label
        # "生效期限" establishes this fact here.
        r"(?:合同)?生效期限\s*[：:]?\s*20\d{2}年\d{1,2}月\d{1,2}日",
        r"(?:批准与生效)[\s\S]{0,100}?20\d{2}年\d{1,2}月\d{1,2}日",
        r"(?:本合同|合同|本协议|协议)(?:自)?双方于\s*20\d{2}年\d{1,2}月\d{1,2}日(?:签字|签名|盖章|签字盖章)[^。\n]{0,12}生效",
        r"(?:本合同|合同|本协议|协议)[^。\n]{0,20}(?:自|于)\s*20\d{2}年\d{1,2}月\d{1,2}日(?:起|之日起)?生效",
        r"(?:本合同|合同|本协议|协议)[^。\n]{0,20}(?:自|于)?\s*20\d{2}年\d{1,2}月\d{1,2}日[^。\n]{0,20}(?:签署|签订|签字盖章)[^。\n]{0,12}生效",
    ))
    validity_start = _first_date(value, (r"(?:合同有效期|有效期限|合同期限)(?!至)[^。\n]{0,45}",))
    validity_period = re.search(r"(?:合同有效期|有效期限|合同期限)[^。\n]*", value)
    validity_dates = list(DATE_PATTERN.finditer(validity_period[0])) if validity_period else []
    validity_end = _iso(validity_dates[-1]) if validity_dates and (len(validity_dates) > 1 or "至" in validity_period[0]) else None
    registration_condition = re.search(
        r"(?:本合同|本协议)[^。\n]{0,80}?(?:登记|注册)[^。\n]{0,15}生效", value,
    )
    # A registration condition has no calendar value merely because a dated
    # signature block follows it. Contract effect and title transfer also differ.
    if registration_condition:
        effective_date = None
    effective_date_basis = "REGISTRATION_CONDITION" if registration_condition else "EXPLICIT_EFFECTIVE_DATE" if effective_date else ""
    signature_effective_condition = bool(re.search(
        r"(?:本合同|合同|本协议|协议)[^。；\n]{0,30}(?:经|自)?(?:双方)?"
        r"(?:签字(?:盖章)?|签名(?:盖章)?|盖章)[^。；\n]{0,20}(?:后|之日起)?生效",
        value,
    ))
    if not registration_condition and not effective_date and signature_effective_condition and signature_dates:
        effective_date = contract_sign_date
        effective_date_basis = "SIGNATURE_DATE_PLUS_EFFECTIVE_CONDITION"

    performance_facts: List[Dict[str, Any]] = []
    performance_markers = (
        "需求分析", "开发进度", "研发进度", "项目进度", "开发开始", "研发开始",
        "第一阶段", "第一期", "项目启动", "实施开始", "履行开始",
        "合作期限", "合作开始", "开发周期",
        "开发期限",
        "第一批技术资料", "首批技术资料", "技术资料交付时间", "技术资料交付期限",
        "许可期限", "许可开始", "许可起始", "实施许可期限",
        "技术转让期限", "受让方使用权", "甲方使用权", "权利起始",
    )
    for match in DATE_PATTERN.finditer(value):
        line_prefix = value[value.rfind("\n", 0, match.start()) + 1:match.start()]
        if re.search(r"(?:签订|签署|签约)(?:日期|时间)?[：:]?\s*$|(?:有效期限|合同有效期|合同期限)[^。\n]*$", line_prefix):
            continue
        context = value[max(0, match.start() - 80):min(len(value), match.end() + 40)]
        matched = [term for term in performance_markers if term in context]
        if not matched:
            continue
        compact_context = re.sub(r"\s+", "", context)
        if (
            any(term in compact_context for term in ("既有许可", "此前已", "已于"))
            and any(term in compact_context for term in ("第三方", "合作企业", "许可期限"))
            and not any(term in compact_context for term in ("本合同项下", "甲方使用权", "受让方使用权", "技术转让期限"))
        ):
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
    performance_candidates = [row for row in (earliest_performance, service_start, license_start, transfer_start) if row]
    earliest_performance = min(performance_candidates) if performance_candidates else None

    comparison_date = effective_date or contract_sign_date
    comparison_basis = "EFFECTIVE_DATE" if effective_date else "SIGNING_DATE" if contract_sign_date else ""
    conflict_suffix = "EFFECTIVE" if effective_date else "SIGNING"
    conflicts: List[Dict[str, Any]] = []
    if validity_start and contract_sign_date and validity_start < contract_sign_date:
        conflicts.append({"type": "VALIDITY_BEFORE_SIGNING", "earlier_date": validity_start,
                          "comparison_date": contract_sign_date, "comparison_basis": "SIGNING_DATE"})
    if comparison_date and service_start and service_start < comparison_date:
        conflicts.append({
            "type": f"SERVICE_BEFORE_{conflict_suffix}",
            "earlier_date": service_start,
            "comparison_date": comparison_date,
            "comparison_basis": comparison_basis,
        })
    if comparison_date and license_start and license_start < comparison_date:
        conflicts.append({
            "type": f"LICENSE_BEFORE_{conflict_suffix}",
            "earlier_date": license_start,
            "comparison_date": comparison_date,
            "comparison_basis": comparison_basis,
        })
    if comparison_date and transfer_start and transfer_start < comparison_date:
        conflicts.append({
            "type": f"TRANSFER_BEFORE_{conflict_suffix}",
            "earlier_date": transfer_start,
            "comparison_date": comparison_date,
            "comparison_basis": comparison_basis,
        })
    if comparison_date and data_deadline and data_deadline < comparison_date:
        conflicts.append({
            "type": f"DATA_DUE_BEFORE_{conflict_suffix}",
            "earlier_date": data_deadline,
            "comparison_date": comparison_date,
            "comparison_basis": comparison_basis,
        })
    if comparison_date and earliest_performance and earliest_performance < comparison_date and not any(
        row["type"] == f"SERVICE_BEFORE_{conflict_suffix}" and row["earlier_date"] == earliest_performance for row in conflicts
    ):
        conflicts.append({
            "type": f"PERFORMANCE_BEFORE_{conflict_suffix}",
            "earlier_date": earliest_performance,
            "comparison_date": comparison_date,
            "comparison_basis": comparison_basis,
        })
    milestone_facts: List[Dict[str, Any]] = []
    milestone_terms = (
        "最终技术服务报告", "最终报告", "最终交付", "项目验收", "最终验收",
        "阶段交付", "交付节点", "验收节点",
    )
    post_performance_terms = ("质保期", "保修期", "质量保证期", "维保期", "售后支持期")
    for match in DATE_PATTERN.finditer(value):
        context = value[max(0, match.start() - 80):min(len(value), match.end() + 80)]
        matched_terms = [term for term in milestone_terms if term in context]
        if not matched_terms or any(term in context for term in post_performance_terms):
            continue
        milestone = {
            "fact_id": f"DATE-MILESTONE-{len(milestone_facts) + 1:03d}",
            "type": "DELIVERY_OR_ACCEPTANCE_MILESTONE",
            "date": _iso(match),
            "matched_terms": matched_terms,
            "source_location": f"line {value.count(chr(10), 0, match.start()) + 1}",
            "raw_text": re.sub(r"\s+", " ", context).strip(),
        }
        if not any(row["date"] == milestone["date"] and row["matched_terms"] == milestone["matched_terms"] for row in milestone_facts):
            milestone_facts.append(milestone)
    if service_end:
        for milestone in milestone_facts:
            if milestone["date"] > service_end:
                conflicts.append({
                    "type": "MILESTONE_AFTER_PERFORMANCE_END",
                    "milestone_date": milestone["date"],
                    "performance_end_date": service_end,
                    "milestone_terms": list(milestone["matched_terms"]),
                    "source_location": milestone["source_location"],
                    "raw_text": milestone["raw_text"],
                })

    # A development deadline may be followed by go-live, a trial-operation
    # period and final acceptance.  These are a single chained milestone, not
    # unrelated post-performance support duties.  Preserve the explicit chain
    # so the report can explain why final acceptance falls outside the stated
    # development term without pretending a calendar date was written for it.
    chained_acceptance_facts: List[Dict[str, Any]] = []
    chained_pattern = re.compile(
        r"(?P<text>[^。；;\n]{0,100}?(?P<base_date>20\d{2}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)"
        r"[^。；;\n]{0,35}?(?:上线|交付)[^。；;\n]{0,50}[。；;\n\s]*"
        r"(?:上线|交付)后(?:进入)?(?P<trial_months>\d+(?:\.\d+)?)\s*个?月(?:的)?试运行期"
        r"[\s\S]{0,100}?试运行(?:期)?结束后(?P<acceptance_days>\d+)\s*个?工作日内(?:进行|完成)?最终验收)",
        re.I,
    )
    for match in chained_pattern.finditer(value):
        base_match = DATE_PATTERN.search(match.group("base_date"))
        if not base_match:
            continue
        base_date = _iso(base_match)
        trial_months = _number(_decimal(match.group("trial_months")))
        acceptance_days = int(match.group("acceptance_days"))
        fact = {
            "fact_id": f"CHAINED-MILESTONE-{len(chained_acceptance_facts) + 1:03d}",
            "type": "GO_LIVE_TRIAL_FINAL_ACCEPTANCE_CHAIN",
            "base_date": base_date,
            "trial_months": trial_months,
            "acceptance_working_days": acceptance_days,
            "source_location": f"line {value.count(chr(10), 0, match.start()) + 1}",
            "raw_text": re.sub(r"\s+", " ", match.group("text")).strip(),
        }
        chained_acceptance_facts.append(fact)
        if service_end and base_date >= service_end and (Decimal(str(trial_months)) > 0 or acceptance_days > 0):
            conflicts.append({
                "type": "MILESTONE_AFTER_PERFORMANCE_END_RELATIVE_CHAIN",
                "performance_end_date": service_end,
                "milestone_base_date": base_date,
                "trial_months": trial_months,
                "acceptance_working_days": acceptance_days,
                "milestone_terms": ["上线", "试运行", "最终验收"],
                "source_location": fact["source_location"],
                "raw_text": fact["raw_text"],
            })

    # Relative durations are first-class timeline constraints as well.  A
    # statement such as "服务在8个月内完成" is the performance boundary; a
    # report or acceptance due in month 9/10/11 must be compared against that
    # boundary even though neither side contains a calendar date.
    performance_duration_candidates: List[Dict[str, Any]] = []
    relative_duration_pattern = re.compile(
        r"(?P<text>[^。；;\n]{0,90}(?:服务|咨询|开发|合作|项目|履行)[^。；;\n]{0,60}?"
        r"(?P<months>\d+(?:\.\d+)?)\s*个?月(?:内|以内)[^。；;\n]{0,35}?(?:完成|结束|届满))",
        re.I,
    )
    for match in relative_duration_pattern.finditer(value):
        context = re.sub(r"\s+", " ", match.group("text")).strip()
        if any(term in re.sub(r"\s+", "", context) for term in ("提交", "交付", "验收")):
            continue
        performance_duration_candidates.append({
            "fact_id": f"DURATION-PERF-{len(performance_duration_candidates) + 1:03d}",
            "type": "PERFORMANCE_DURATION_MONTHS",
            "months": _number(_decimal(match.group("months"))),
            "source_location": f"line {value.count(chr(10), 0, match.start()) + 1}",
            "raw_text": context,
        })
    # Also support the common "自生效之日起8个月内完成" form where the word
    # 服务 appears farther to the left in the same sentence.
    for sentence_match in re.finditer(r"[^。；;\n]+", value):
        sentence = sentence_match.group(0).strip()
        compact_sentence = re.sub(r"\s+", "", sentence)
        if not any(term in compact_sentence for term in ("服务", "咨询", "开发", "合作", "项目", "履行")):
            continue
        for match in re.finditer(r"(?P<months>\d+(?:\.\d+)?)\s*个?月(?:内|以内)(?:完成|结束|届满)", sentence):
            if any(term in compact_sentence[max(0, match.start() - 20):match.end() + 20] for term in ("提交", "交付", "验收")):
                continue
            months = _number(_decimal(match.group("months")))
            if any(row["months"] == months and row["raw_text"] == sentence for row in performance_duration_candidates):
                continue
            performance_duration_candidates.append({
                "fact_id": f"DURATION-PERF-{len(performance_duration_candidates) + 1:03d}",
                "type": "PERFORMANCE_DURATION_MONTHS",
                "months": months,
                "source_location": f"line {value.count(chr(10), 0, sentence_match.start()) + 1}",
                "raw_text": sentence,
            })
    performance_duration_months = min(
        (Decimal(str(row["months"])) for row in performance_duration_candidates),
        default=None,
    )

    relative_milestone_facts: List[Dict[str, Any]] = []
    for sentence_match in re.finditer(r"[^。；;\n]+", value):
        sentence = sentence_match.group(0).strip()
        compact_sentence = re.sub(r"\s+", "", sentence)
        if not any(term in compact_sentence for term in (
            "提交", "交付", "最终报告", "咨询报告", "技术报告", "验收", "分项",
        )):
            continue
        for month_match in re.finditer(r"(?P<months>\d+(?:\.\d+)?)\s*个?月(?:内|以内)", sentence):
            months = _number(_decimal(month_match.group("months")))
            nearby = compact_sentence[max(0, month_match.start() - 40):month_match.end() + 80]
            matched_terms = [term for term in (
                "提交", "交付", "最终报告", "最终技术咨询报告", "咨询报告", "技术报告", "验收", "最终验收", "分项",
            ) if term in nearby or term in compact_sentence]
            if not matched_terms:
                continue
            fact = {
                "fact_id": f"DURATION-MILESTONE-{len(relative_milestone_facts) + 1:03d}",
                "type": "RELATIVE_DELIVERY_OR_ACCEPTANCE_MILESTONE",
                "months": months,
                "matched_terms": matched_terms,
                "source_location": f"line {value.count(chr(10), 0, sentence_match.start()) + 1}",
                "raw_text": sentence,
            }
            if not any(row["months"] == months and row["raw_text"] == sentence for row in relative_milestone_facts):
                relative_milestone_facts.append(fact)
    if performance_duration_months is not None:
        for milestone in relative_milestone_facts:
            milestone_months = Decimal(str(milestone["months"]))
            if milestone_months <= performance_duration_months:
                continue
            conflicts.append({
                "type": "MILESTONE_AFTER_PERFORMANCE_DURATION",
                "milestone_offset_months": _number(milestone_months),
                "performance_duration_months": _number(performance_duration_months),
                "milestone_terms": list(milestone["matched_terms"]),
                "source_location": milestone["source_location"],
                "raw_text": milestone["raw_text"],
            })
    conflict_types = [row["type"] for row in conflicts]
    if any(value.startswith("DATA_DUE_BEFORE_") for value in conflict_types):
        primary_conflict_subject = "TECHNICAL_MATERIAL_DELIVERY"
    elif any(value.startswith("TRANSFER_BEFORE_") for value in conflict_types):
        primary_conflict_subject = "TRANSFER_START"
    elif any(value.startswith("LICENSE_BEFORE_") for value in conflict_types):
        primary_conflict_subject = "LICENSE_START"
    elif any(value.startswith("SERVICE_BEFORE_") for value in conflict_types):
        primary_conflict_subject = "SERVICE_START"
    elif any(value.startswith("PERFORMANCE_BEFORE_") for value in conflict_types):
        primary_conflict_subject = "PERFORMANCE_START"
    elif "VALIDITY_BEFORE_SIGNING" in conflict_types:
        primary_conflict_subject = "VALIDITY_START"
        comparison_date, comparison_basis = contract_sign_date, "SIGNING_DATE"
    else:
        primary_conflict_subject = ""
    return {
        "validity_start_date": validity_start,
        "validity_end_date": validity_end,
        "signing_date": contract_sign_date,
        "performance_start_date": earliest_performance,
        "effective_date_condition": registration_condition.group(0) if registration_condition else "",
        "effective_date": effective_date,
        "contract_sign_date": contract_sign_date,
        "contract_effective_date": effective_date,
        "effective_date_basis": effective_date_basis,
        "signature_effective_condition": signature_effective_condition,
        "comparison_date": comparison_date,
        "comparison_basis": comparison_basis,
        "service_start_date": service_start,
        "service_end_date": service_end,
        "license_start_date": license_start,
        "transfer_start_date": transfer_start,
        "earliest_performance_date": earliest_performance,
        "performance_before_effective_date": bool(effective_date and earliest_performance and earliest_performance < effective_date),
        "performance_before_signing_date": bool(contract_sign_date and earliest_performance and earliest_performance < contract_sign_date),
        "date_facts": performance_facts,
        "milestone_facts": milestone_facts,
        "performance_duration_months": _number(performance_duration_months) if performance_duration_months is not None else None,
        "performance_duration_facts": performance_duration_candidates,
        "relative_milestone_facts": relative_milestone_facts,
        "chained_acceptance_facts": chained_acceptance_facts,
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

    # Reciprocal clauses often use the neutral subject “双方” rather than
    # restating licensor/licensee in each direction.  Treat that wording as
    # two objective grant facts, while preserving any unspecified licence
    # dimensions for the rule layer to assess later.
    reciprocal_free_match = re.search(
        r"(?:双方|各方).{0,65}(?:改进和发展(?:的)?(?:技术)?|改进技术|改进成果|后续改进)"
        r".{0,45}(?:相互|互相).{0,18}(?:免费|无偿).{0,35}"
        r"(?:提供|许可|开放).{0,20}(?:对方|另一方).{0,12}使用",
        compact,
    )
    if not reciprocal_free_match:
        reciprocal_free_match = re.search(
            r"(?:一般改进|改进成果|后续改进|改进技术)[：:]?.{0,20}(?:双方|各方)(?:可|可以)?(?:相互|互相)(?:免费|无偿)使用",
            compact,
        )

    # A compulsory assignment of independently created improvements is more
    # restrictive than a grant-back licence.  It must remain visible as a
    # directional, zero-consideration fact instead of being reduced to
    # "ownership has been addressed".
    forced_transfer_match = re.search(
        r"(?:受让方|被许可方|买方|甲方).{0,80}(?:独立(?:完成|形成)|自行(?:完成|形成)|形成的任何)?"
        r".{0,25}(?:改进成果|改进方案|改进技术).{0,100}"
        r"(?:知识产权|专利申请权|专利权|软件著作权).{0,35}(?:均|全部)?归(?:出让方|让与方|转让方|许可方|卖方|乙方)所有"
        r".{0,100}(?:无偿|免费).{0,30}(?:办理|配合).{0,35}(?:转移|转让)",
        compact,
    )
    if not forced_transfer_match:
        forced_transfer_match = re.search(
            r"(?:受让方|被许可方|买方|甲方).{0,45}(?:独立(?:完成|形成)|自行(?:完成|形成))"
            r".{0,30}(?:改进成果|改进方案|改进技术).{0,45}(?:知识产权.{0,20})?"
            r"(?:无偿|免费).{0,18}归(?:出让方|让与方|转让方|许可方|卖方|乙方)所有",
            compact,
        )
    if not forced_transfer_match:
        forced_transfer_match = re.search(
            r"(?:受让方|被许可方|买方|甲方).{0,55}(?:独立|自行)(?:进一步)?(?:完成|形成)?"
            r".{0,45}(?:改进|优化|算法|软件|其他成果).{0,100}(?:知识产权|专利申请权|专利权|软件著作权)"
            r".{0,25}(?:亦|均|全部)?(?:无偿|免费).{0,12}归(?:出让方|让与方|转让方|许可方|卖方|乙方)所有",
            compact,
        )
    if forced_transfer_match:
        forced_source = forced_transfer_match.group(0)
        forced_fact = _improvement_license_fact("LICENSEE", "LICENSOR", forced_source)
        forced_fact.update({
            "license_fee": "ZERO",
            "transfer_mode": "OWNERSHIP_TRANSFER",
            "independent_improvement": True,
            "mandatory": True,
        })
        facts.append(forced_fact)

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
    )) or bool(reciprocal_free_match)
    if symmetric_shortcut and len(facts) < 2:
        reciprocal_source = (
            compact[max(0, reciprocal_free_match.start() - 32):reciprocal_free_match.end()]
            if reciprocal_free_match else compact
        )
        common = {
            "license_fee": "ZERO",
            "license_duration": "CONTRACT_TERM" if "合同有效期内" in reciprocal_source else "SAME_DEFINED",
            "territory": "UNSPECIFIED" if reciprocal_free_match else "SAME_DEFINED",
            "revocability": "UNSPECIFIED" if reciprocal_free_match else "SAME_DEFINED",
            "exclusivity": "UNSPECIFIED" if reciprocal_free_match else "SAME_DEFINED",
            "commercial_use": None,
            "reciprocal_obligation": True, "source_text": reciprocal_source,
        }
        facts = [
            {"improving_party": "PARTY_A", "grantor": "PARTY_A", "grantee": "PARTY_B", **common},
            {"improving_party": "PARTY_B", "grantor": "PARTY_B", "grantee": "PARTY_A", **common},
        ]

    comparison_fields = ("license_fee", "license_duration", "territory", "revocability", "exclusivity", "commercial_use")
    signatures = [tuple(row.get(field) for field in comparison_fields) for row in facts]
    has_mandatory_free_grant = any(row.get("license_fee") == "ZERO" for row in facts)
    forced_free_transfer = bool(forced_transfer_match)
    asymmetric = bool(
        facts
        and not symmetric_shortcut
        and (
            forced_free_transfer
            or
            len(facts) == 1 and has_mandatory_free_grant
            or len(facts) >= 2 and len(set(signatures)) > 1
        )
    )
    for row in facts:
        row["reciprocal_obligation"] = not asymmetric and len(facts) >= 2
    licensee_owns_improvement = bool(re.search(
        r"(?:受让方|被许可方|买方|甲方).{0,45}(?:后续改进|改进成果|改进技术|新的技术成果).{0,180}(?:归其所有|归(?:受让方|被许可方|买方|甲方)(?:所有)?|归属[：:]?(?:受让方|被许可方|买方|甲方)(?:所有)?)",
        compact,
    ))
    licensor_owns_improvement = bool(re.search(
        r"(?:出让方|让与方|许可方|卖方|乙方).{0,45}(?:后续改进|改进成果|改进技术|新的技术成果).{0,180}(?:归其所有|归(?:出让方|让与方|许可方|卖方|乙方)(?:所有)?|归属[：:]?(?:出让方|让与方|许可方|卖方|乙方)(?:所有)?)",
        compact,
    ))
    actual_improver_owns = bool(re.search(
        r"(?:改进和发展(?:的)?技术|改进技术|改进成果).{0,35}"
        r"(?:所有权|知识产权).{0,15}(?:属于|归)(?:实际)?(?:实施|进行|完成|形成)?"
        r"(?:改进和发展|改进).{0,12}(?:的一方|一方|改进方)",
        compact,
    ))
    licensee_priority_license = bool(re.search(
        r"(?:受让方|被许可方|买方|甲方).{0,25}(?:优先许可权|优先获得许可|优先被许可)", compact,
    ))
    licensor_use_negotiated = bool(re.search(
        r"(?:出让方|许可方|卖方|乙方).{0,40}(?:使用|许可).{0,45}(?:另行协商|协商确定|另行约定)", compact,
    ))
    ownership_arrangement = bool(
        licensee_owns_improvement or licensor_owns_improvement or actual_improver_owns
    )
    partial_arrangement = bool(
        ownership_arrangement
        and (
            licensee_priority_license or licensor_use_negotiated
            or (licensee_owns_improvement and licensor_owns_improvement)
            or "无义务将各自独立完成的后续改进成果无偿许可给另一方" in compact
        )
    )
    arrangement_status = (
        "ASYMMETRIC" if asymmetric
        else "SYMMETRIC" if facts
        else "PARTIAL" if partial_arrangement
        else "MISSING"
    )
    reciprocal_material_delivery = bool(
        reciprocal_free_match
        and any(term in reciprocal_free_match.group(0) for term in ("技术资料", "资料", "提供"))
    )
    patent_application_restriction = bool(re.search(
        r"(?:另一方|对方).{0,18}不得.{0,20}(?:利用|使用).{0,18}(?:该等)?技术资料.{0,12}申请专利|"
        r"(?:另一方|对方).{0,18}不得.{0,25}申请专利",
        compact,
    ))
    third_party_transfer_restriction = bool(re.search(
        r"(?:另一方|对方).{0,22}不得.{0,80}(?:向第三方转让|转让给第三方)",
        compact,
    ))
    license_terms_complete = bool(
        facts
        and all(
            row.get("license_fee") not in {None, "UNSPECIFIED"}
            and row.get("license_duration") not in {None, "UNSPECIFIED"}
            and row.get("territory") not in {None, "UNSPECIFIED"}
            and row.get("commercial_use") is not None
            for row in facts
        )
    )
    return {
        "arrangement_status": arrangement_status,
        "facts": facts,
        "asymmetric_improvement_license": asymmetric,
        "forced_free_improvement_transfer": forced_free_transfer,
        "unreasonable_improvement_restriction": forced_free_transfer,
        "actual_improver_owns": actual_improver_owns,
        "reciprocal_free_use": bool(reciprocal_free_match),
        "reciprocal_material_delivery": reciprocal_material_delivery,
        "patent_application_restriction": patent_application_restriction,
        "third_party_transfer_restriction": third_party_transfer_restriction,
        "license_terms_complete": license_terms_complete,
        "ownership_and_priority_arrangement": {
            "licensee_owns_improvement": licensee_owns_improvement,
            "licensor_owns_improvement": licensor_owns_improvement,
            "actual_improver_owns": actual_improver_owns,
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


def analyze_patent_license_consistency(text: str) -> Dict[str, Any]:
    """Analyze patent-license facts whose risk only appears across clauses.

    The function deliberately separates presence from correctness: a licence
    type, term, territory or fee clause can be present while contradicting the
    patent right or another operative clause.
    """
    value = text or ""
    compact = re.sub(r"\s+", "", value)

    # Compare operative clauses, not the whole document as one string.  Patent
    # templates often define both ordinary and exclusive licences in a glossary;
    # scanning across paragraph boundaries can incorrectly combine those two
    # definitions into an operative permission for the licensor.
    permission_segments = [
        re.sub(r"\s+", "", segment)
        for segment in re.split(r"[\n\r。；;]+", value)
        if segment.strip()
    ]
    declared_license_type = "UNKNOWN"
    declared_license_type_label = ""
    declared_license_type_source = ""
    license_type_labels = {
        "独占": ("SOLE_EXCLUSIVE", "独占实施许可"),
        "排他": ("EXCLUSIVE", "排他实施许可"),
        "普通": ("NON_EXCLUSIVE", "普通实施许可"),
        "非独占": ("NON_EXCLUSIVE", "非独占实施许可"),
    }
    from review_v2.license_terms import LICENSE_TYPE_PATTERN, declared_license_type as is_declared_license_type
    license_type_term = '(' + LICENSE_TYPE_PATTERN + ')'

    def license_type_for_term(term: str) -> tuple[str, str]:
        for prefix, resolved in license_type_labels.items():
            if term.startswith(prefix):
                return resolved
        return "UNKNOWN", ""
    for segment in permission_segments:
        if not is_declared_license_type(segment):
            continue
        if re.match(r"^(?:普通实施许可|排他实施许可|独占实施许可)[—－-]{1,2}(?:指|是指)", segment):
            continue
        match = re.search(
            r"(?:本合同(?:项下)?(?:专利|技术)?(?:采用|约定为|许可方式为)|"
            r"(?:本合同)?(?:专利|技术)?许可方式(?:为|采用)|"
            r"许可方.{0,12}授予(?:被许可方|接受方|受许可方).{0,30})"
            rf".{{0,12}}?{license_type_term}(?:方式)?",
            segment,
        )
        if not match:
            match = re.search(
                rf"本合同(?:项下)?(?:专利|技术)?.{{0,16}}{license_type_term}(?:方式)?",
                segment,
            )
        if match:
            matched_term = match.group(1)
            declared_license_type, declared_license_type_label = license_type_for_term(matched_term)
            declared_license_type_source = segment
            break
    if declared_license_type == "UNKNOWN":
        for segment in permission_segments:
            if not is_declared_license_type(segment):
                continue
            if re.match(r"^(?:普通实施许可|排他实施许可|独占实施许可)[—－-]{1,2}(?:指|是指)", segment):
                continue
            match = re.search(rf"{license_type_term}(?:合同|方式|。|$)", segment)
            if not match:
                continue
            matched_term = match.group(1)
            declared_license_type, declared_license_type_label = license_type_for_term(matched_term)
            declared_license_type_source = segment
            break
    exclusive_declared = declared_license_type in {"SOLE_EXCLUSIVE", "EXCLUSIVE"}
    licensor_role = r"(?:许可方|许可人|出让方|让与方|卖方)"
    licensor_permission_patterns = (
        rf"{licensor_role}.{{0,60}}(?:有权|可以|仍可|可同时|可(?=向|对)).{{0,30}}(?:向|对)?(?:该)?(?:第三方|其他企业|其他主体).{{0,30}}(?:授予|给予|进行|提供).{{0,15}}(?:普通)?(?:实施)?许可",
        rf"{licensor_role}.{{0,25}}(?:认为)?(?:该)?第三方.{{0,35}}(?:不存在直接竞争关系|非竞争).{{0,35}}(?:可以|可|有权).{{0,20}}(?:向)?(?:该)?第三方.{{0,15}}(?:授予|给予).{{0,12}}(?:普通)?实施许可",
        rf"{licensor_role}.{{0,30}}(?:向|对).{{0,30}}(?:不存在直接竞争关系|非竞争).{{0,30}}(?:第三方|企业).{{0,25}}(?:授予|给予|许可).{{0,12}}(?:普通)?实施许可",
    )
    licensor_third_party_permission = any(
        not re.match(r"^(?:普通实施许可|排他实施许可|独占实施许可)[—－-]{1,2}(?:指|是指)", segment)
        and not re.search(r"(?:不再|不得|禁止).{0,30}(?:第三方|其他企业|其他主体).{0,30}(?:授予|给予|许可)", segment)
        and any(re.search(pattern, segment) for pattern in licensor_permission_patterns)
        for segment in permission_segments
    )
    # Operative exception lists are often split into a lead-in sentence and
    # several bullet paragraphs.  Evaluate that bounded clause window without
    # treating glossary definitions as operative permissions.
    operative_exception_block = bool(re.search(
        r"(?:虽然|尽管)?(?:本合同)?(?:为)?排他(?:实施)?许可.{0,60}"
        r"(?:许可方|许可人|出让方|让与方|卖方)(?:仍|仍然)?(?:可以|有权).{0,260}"
        r"(?:许可其他科研机构实施|向.{0,30}科研合作.{0,30}企业提供.{0,20}专利技术|"
        r"向.{0,30}(?:第三方|其他机构|合作企业).{0,25}(?:许可|提供).{0,20}(?:实施|专利技术))",
        compact,
    ))
    existing_third_party_license = any(
        bool(re.search(
            rf"{licensor_role}.{{0,45}}(?:已于|此前|已经).{{0,80}}(?:普通|非独占)(?:实施)?许可"
            r".{0,60}(?:许可给|授予|允许).{0,50}(?:公司|企业|机构)",
            segment,
        ))
        or bool(re.search(
            rf"{licensor_role}.{{0,45}}(?:已于|此前|已经).{{0,120}}以(?:普通|非独占)许可方式"
            r".{0,40}(?:许可给|授予).{0,50}(?:公司|企业|机构)",
            segment,
        ))
        or bool(re.search(
            rf"{licensor_role}.{{0,45}}(?:已于|此前|已经|已).{{0,35}}(?:向|对)?"
            r"(?:第三方|[^,，。；;]{1,30}(?:公司|企业|机构))"
            r".{0,25}(?:授予|给予|签订|存在).{0,18}(?:普通|非独占)(?:实施)?许可",
            segment,
        ))
        for segment in permission_segments
    )
    reserved_collaboration_permission = bool(re.search(
        rf"{licensor_role}.{{0,80}}(?:保留|仍保留).{{0,30}}(?:向|对).{{0,55}}"
        r"(?:科研|教学|合作).{0,40}(?:企业|机构|主体).{0,35}(?:提供|许可).{0,30}(?:相关)?技术",
        compact,
    )) or bool(re.search(
        rf"{licensor_role}.{{0,70}}(?:可以|有权|仍可).{{0,30}}(?:因科研|向).{{0,80}}"
        r"(?:合作关系|科研合作).{0,30}(?:企业|机构).{0,30}(?:提供|许可).{0,25}(?:相关)?技术",
        compact,
    ))
    licensor_self_implementation = any(
        not re.match(r"^(?:普通实施许可|排他实施许可|独占实施许可)[—－-]{1,2}(?:指|是指)", segment)
        and bool(re.search(
            rf"{licensor_role}.{{0,35}}(?:仍)?(?:有权|可以|可|保留).{{0,20}}(?:自行|自己)(?:继续)?实施",
            segment,
        ))
        for segment in permission_segments
    )
    licensor_third_party_permission = (
        licensor_third_party_permission
        or operative_exception_block
        or existing_third_party_license
        or reserved_collaboration_permission
    )
    third_party_permission_conflict = exclusive_declared and licensor_third_party_permission
    self_implementation_conflict = declared_license_type == "SOLE_EXCLUSIVE" and licensor_self_implementation
    exclusive_conflict = third_party_permission_conflict or self_implementation_conflict

    downgrade_block = re.search(
        r"(?:排他|独占)(?:实施)?许可.{0,180}(?:许可方|出让方|让与方).{0,40}"
        r"(?:有权|可以).{0,40}(?:变更|调整|降级)为(?:普通|非独占)(?:实施)?许可",
        compact,
    )
    unilateral_downgrade = bool(downgrade_block) and bool(re.search(
        r"(?:无需|不需|无须).{0,15}(?:被许可方|受让方).{0,10}(?:同意|确认)|"
        r"(?:许可方|出让方|让与方).{0,35}(?:单方|自行|直接).{0,30}(?:变更|调整|降级)",
        downgrade_block.group(0) if downgrade_block else "",
    ))
    downgrade_text = downgrade_block.group(0) if downgrade_block else ""
    downgrade_trigger_defined = bool(re.search(
        r"(?:连续)?(?:\d+|[一二三四五六七八九十]+)个?月.{0,35}"
        r"(?:未|没有|未能).{0,30}(?:实际实施|商业化实施|实现销售|投产)",
        downgrade_text,
    ))
    downgrade_notice = bool(re.search(r"(?:书面)?通知", downgrade_text))
    downgrade_cure_period = bool(re.search(r"(?:宽限期|整改期|补救期|限期整改|限期实施)", downgrade_text))
    downgrade_licensee_consent = bool(re.search(
        r"(?:经|取得).{0,8}(?:被许可方|受让方).{0,8}(?:书面)?(?:同意|确认)",
        downgrade_text,
    ))
    downgrade_consideration_adjustment = bool(re.search(
        r"(?:调减|调整|返还|退还).{0,30}(?:排他|独占)?(?:许可费|对价)|"
        r"(?:排他|独占)(?:许可)?(?:对价|许可费).{0,30}(?:调减|调整|返还|退还)",
        downgrade_text,
    ))

    patent_type = (
        "INVENTION" if "发明专利" in compact else
        "UTILITY_MODEL" if "实用新型" in compact else
        "DESIGN" if "外观设计" in compact else
        "UNKNOWN"
    )
    application_date = _first_date(value, (
        r"(?:专利)?申请日(?:期)?\s*(?:为)?\s*[：:]?\s*20\d{2}年\d{1,2}月\d{1,2}日",
    ))
    explicit_expiry_date = _first_date(value, (
        r"(?:专利(?:权)?的?)?(?:法定|基础)?(?:保护期限)?届满日\s*(?:为)?\s*[：:]?\s*20\d{2}年\d{1,2}月\d{1,2}日",
        r"专利权期限届满日\s*(?:为)?\s*[：:]?\s*20\d{2}年\d{1,2}月\d{1,2}日",
    ))

    licence_period_match = re.search(
        r"(?:专利)?(?:实施)?许可期限\s*[：:]?\s*(?:为)?\s*(?:自)?\s*"
        r"(?P<start>20\d{2}年\d{1,2}月\d{1,2}日)\s*(?:起|开始)?\s*(?:至|到)\s*"
        r"(?P<end>20\d{2}年\d{1,2}月\d{1,2}日)",
        compact,
    )

    def iso_from_text(date_text: str) -> Optional[str]:
        match = DATE_PATTERN.search(date_text or "")
        return _iso(match) if match else None

    licence_start = iso_from_text(licence_period_match.group("start")) if licence_period_match else None
    licence_end = iso_from_text(licence_period_match.group("end")) if licence_period_match else None
    basic_term_years: Optional[int] = None
    if patent_type == "INVENTION":
        basic_term_years = 20
    elif patent_type == "UTILITY_MODEL":
        basic_term_years = 10
    elif patent_type == "DESIGN" and application_date:
        basic_term_years = 15 if application_date >= "2021-06-01" else 10

    calculated_basic_expiry: Optional[str] = None
    if application_date and basic_term_years:
        applied = date.fromisoformat(application_date)
        try:
            calculated_basic_expiry = applied.replace(year=applied.year + basic_term_years).isoformat()
        except ValueError:
            calculated_basic_expiry = applied.replace(month=2, day=28, year=applied.year + basic_term_years).isoformat()
    basic_expiry = explicit_expiry_date or calculated_basic_expiry
    term_compensation_present = bool(re.search(
        r"(?:专利权|专利)?期限(?:补偿|延长)|药品专利期限补偿|专利期限补偿决定",
        compact,
    ))
    term_exceeds_basic_expiry = bool(
        licence_end and basic_expiry and licence_end > basic_expiry and not term_compensation_present
    )

    china_patent_only = bool(
        re.search(r"专利号[：:]?(?:ZL|CN)", compact, re.I)
        or "国家知识产权局" in compact
        or "中华人民共和国发明专利" in compact
    ) and not bool(re.search(r"(?:美国|欧洲|日本|PCT|国际专利|境外专利).{0,30}(?:专利号|申请号)", compact, re.I))
    foreign_territory = bool(re.search(
        r"许可区域[^。；]{0,160}(?:其他国家和地区|未来.{0,12}国家和地区|全球|世界范围|境外)",
        compact,
    )) or bool(re.search(r"许可区域[^。；]{0,120}(?:香港|澳门|台湾)", compact))
    territory_exceeds_patent_protection = china_patent_only and foreign_territory

    invalidity_terminates = bool(re.search(
        r"(?:专利|许可专利).{0,30}(?:全部无效|宣告全部无效).{0,80}(?:合同|本合同).{0,20}(?:终止|解除)",
        compact,
    ))
    invalidity_occurs = bool(re.search(
        r"(?:专利|合同专利).{0,35}(?:全部|部分)?(?:被)?(?:宣告)?(?:无效|失效)",
        compact,
    ))
    contract_continues_after_invalidity = bool(re.search(
        r"(?:专利|合同专利).{0,35}(?:全部|部分)?(?:被)?(?:宣告)?无效.{0,60}"
        r"(?:本合同|合同).{0,20}(?:原则上)?继续履行",
        compact,
    ))
    future_fixed_fee_continues = bool(re.search(
        r"(?:全部无效|部分无效|宣告无效|无效决定).{0,220}(?:尚未到期|未到期|未来|剩余).{0,30}"
        r"(?:固定许可费|许可费).{0,35}(?:(?:仍应|继续).{0,15}(?:支付|缴纳)|不得.{0,12}停止支付)",
        compact,
    )) or bool(re.search(
        r"(?:不得|无权).{0,20}(?:以)?专利(?:被)?(?:宣告)?无效.{0,25}(?:为由)?停止支付.{0,30}"
        r"(?:尚未到期|未到期).{0,12}(?:固定许可费|许可费)",
        compact,
    ))
    royalty_continues_after_invalidity = bool(re.search(
        r"(?:全部无效|部分无效|宣告无效).{0,220}(?:销售提成|提成).{0,35}"
        r"(?:(?:仍应|继续).{0,15}(?:支付|缴纳)|不得.{0,12}停止支付)",
        compact,
    )) or bool(re.search(
        r"(?:不得|无权).{0,20}(?:以)?专利(?:被)?(?:宣告)?无效.{0,25}(?:为由)?停止支付.{0,60}(?:销售提成|提成)",
        compact,
    ))
    paid_fee_nonrefundable_after_invalidity = bool(re.search(
        r"(?:全部无效|部分无效|宣告无效).{0,240}(?:已经支付|已付).{0,80}(?:不退还|不予退还)",
        compact,
    ))
    termination_prohibited_after_invalidity = bool(re.search(
        r"(?:全部无效|部分无效|宣告无效).{0,260}(?:不得|无权).{0,35}(?:解除|终止)(?:本)?合同|"
        r"(?:不得|无权).{0,35}(?:以)?专利(?:被)?(?:宣告)?无效.{0,25}(?:解除|终止)合同",
        compact,
    ))
    invalidity_fee_conflict = bool(
        invalidity_occurs
        and (future_fixed_fee_continues or royalty_continues_after_invalidity)
        and (invalidity_terminates or contract_continues_after_invalidity or termination_prohibited_after_invalidity)
    )
    continued_use_after_invalidity = bool(re.search(
        r"专利(?:权)?(?:无效|失效).{0,180}(?:可以|有权|继续).{0,30}"
        r"(?:使用|实施).{0,45}(?:技术|专利|公有领域)",
        compact,
    )) or bool(re.search(
        r"专利(?:权)?(?:无效|失效).{0,220}(?:技术|专利).{0,35}"
        r"(?:进入公有领域|可以继续使用|可继续实施)",
        compact,
    ))
    royalty_stops_after_invalidity = bool(re.search(
        r"(?:专利(?:权)?(?:无效|失效)|失效日).{0,160}"
        r"(?:不再|停止|无需).{0,24}(?:支付|缴纳).{0,24}(?:提成费|许可费)",
        compact,
    ))
    paid_fee_refunded_after_invalidity = bool(re.search(
        r"(?:专利(?:权)?(?:无效|失效)|失效日).{0,180}"
        r"(?:返还|退还).{0,40}(?:已收取|已收|已支付|已付).{0,24}(?:费用|提成费|许可费)",
        compact,
    )) or bool(re.search(
        r"(?:返还|退还).{0,50}(?:专利(?:权)?(?:无效|失效)|失效日)"
        r".{0,50}(?:费用|提成费|许可费)",
        compact,
    ))

    return {
        "license_type": declared_license_type,
        "license_type_label": declared_license_type_label,
        "license_type_source_text": declared_license_type_source,
        "exclusive_license_declared": exclusive_declared,
        "licensor_self_implementation": licensor_self_implementation,
        "license_type_self_implementation_conflict": self_implementation_conflict,
        "license_type_third_party_permission_conflict": third_party_permission_conflict,
        "licensor_third_party_license_permission": licensor_third_party_permission,
        "existing_third_party_license": existing_third_party_license,
        "reserved_collaboration_permission": reserved_collaboration_permission,
        "exclusive_license_conflict": exclusive_conflict,
        "exclusive_license_downgrade_present": bool(downgrade_block),
        "exclusive_license_unilateral_downgrade": unilateral_downgrade,
        "downgrade_trigger_defined": downgrade_trigger_defined,
        "downgrade_notice_present": downgrade_notice,
        "downgrade_cure_period_present": downgrade_cure_period,
        "downgrade_licensee_consent_required": downgrade_licensee_consent,
        "downgrade_consideration_adjustment_present": downgrade_consideration_adjustment,
        "patent_type": patent_type,
        "application_date": application_date,
        "basic_patent_term_years": basic_term_years,
        "basic_patent_expiry_date": basic_expiry,
        "explicit_patent_expiry_date": explicit_expiry_date,
        "calculated_basic_patent_expiry_date": calculated_basic_expiry,
        "patent_expiry_source": "CONTRACT_EXPLICIT" if explicit_expiry_date else "APPLICATION_DATE_CALCULATION" if calculated_basic_expiry else "UNKNOWN",
        "license_start_date": licence_start,
        "license_end_date": licence_end,
        "patent_term_compensation_present": term_compensation_present,
        "license_term_exceeds_basic_patent_term": term_exceeds_basic_expiry,
        "patent_protection_territories": ["CN_MAINLAND"] if china_patent_only else [],
        "license_contains_foreign_territory": foreign_territory,
        "license_territory_exceeds_patent_protection": territory_exceeds_patent_protection,
        "patent_invalidity_terminates_contract": invalidity_terminates,
        "patent_invalidity_occurs": invalidity_occurs,
        "contract_continues_after_patent_invalidity": contract_continues_after_invalidity,
        "future_fixed_fee_continues_after_invalidity": future_fixed_fee_continues,
        "royalty_continues_after_invalidity": royalty_continues_after_invalidity,
        "paid_fee_nonrefundable_after_invalidity": paid_fee_nonrefundable_after_invalidity,
        "termination_prohibited_after_invalidity": termination_prohibited_after_invalidity,
        "patent_invalidity_fee_conflict": invalidity_fee_conflict,
        "continued_use_after_patent_invalidity": continued_use_after_invalidity,
        "royalty_stops_after_patent_invalidity": royalty_stops_after_invalidity,
        "paid_fee_refunded_after_patent_invalidity": paid_fee_refunded_after_invalidity,
    }


def analyze_third_party_infringement_allocation(text: str) -> Dict[str, Any]:
    """Return the canonical third-party claim facts used by TC-12-01/02/04."""
    registry = build_technology_fact_registry(text)
    claim = dict(registry["third_party_claim"])
    licensor_handles_claim = bool(claim["claim_handling"] or claim["litigation_handling"])
    licensee_handles_claim = bool(claim.get("licensee_claim_handling") or claim.get("licensee_litigation_handling"))
    licensor_legal_economic_liability = bool(
        claim.get("responsible_party") == "LICENSOR"
        and (
            claim["general_liability"] or claim["direct_damage"]
            or claim["attorney_fee"] or claim["litigation_cost"] or claim.get("legal_cost")
            or claim.get("third_party_compensation_allocation")
        )
    )
    licensee_legal_economic_liability = bool(
        claim.get("claim_cost_bearer") == "LICENSEE"
        or claim.get("licensee_broad_business_loss_allocation")
        or (
            claim.get("responsible_party") == "LICENSEE"
            and claim.get("third_party_compensation_allocation")
        )
    )
    return {
        "licensor_authority_warranty": claim["authority_warranty"],
        "third_party_claim_trigger": claim["claim_trigger"],
        "responsible_party": claim.get("responsible_party") or "UNKNOWN",
        "claim_cost_bearer": claim.get("claim_cost_bearer") or "UNKNOWN",
        "licensor_handles_claim": licensor_handles_claim,
        "licensee_handles_claim": licensee_handles_claim,
        "licensor_assistance_only": bool(claim.get("claim_assistance") and licensee_handles_claim and not licensor_handles_claim),
        "licensor_legal_economic_liability": licensor_legal_economic_liability,
        "licensee_legal_economic_liability": licensee_legal_economic_liability,
        "basic_liability_allocation": bool(
            claim["claim_trigger"]
            and (licensor_handles_claim or licensee_handles_claim)
            and (licensor_legal_economic_liability or licensee_legal_economic_liability)
        ),
        "claim_process": {
            "explicit_gap": claim["explicit_process_gap"],
            "notification_requirement": claim["notification_requirement"],
            "notification_deadline": claim["notification_deadline"],
            "defense_control": claim["defense_control"],
            "lawyer_selection": claim["lawyer_selection"],
            "settlement_authority": claim["settlement_authority"],
            "settlement_consultation": bool(claim.get("settlement_consultation")),
            "defense_cost_allocation": bool(
                claim.get("claim_cost_allocation")
                or claim["attorney_fee"] or claim["litigation_cost"] or claim.get("legal_cost")
            ),
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
    quantitative_subject = (
        r"(?:SOC估算平均误差|误差|异常报警率|连续稳定运行|"
        r"响应时间|执行时间|使用率|准确率|可用率|并发量|性能指标)"
    )
    quantitative_pattern = re.compile(
        quantitative_subject
        + r"[^。；]{0,50}(?:\d+(?:\.\d+)?\s*(?:秒|毫秒|小时|%|个百分点)|"
        r"降低\d+(?:\.\d+)?%|不高于|不低于|以内|以上)"
    )
    quantitative_target_matches = [match.group(0) for match in quantitative_pattern.finditer(compact)]
    standard_concrete = any(term in acceptance_text for term in (
        "准确率", "响应时间", "并发量", "可用率", "功能清单", "缺陷等级", "测试用例", "性能指标",
    )) or bool(quantitative_target_matches)
    performance_target_weakening = any(term in compact for term in (
        "原则上", "最终优化效果以实际运行结果为准", "最终以实际运行结果为准", "以实际运行结果为准",
    ))
    payment_tied_to_acceptance = bool(re.search(
        r"验收(?:合格|通过)[^。；]{0,35}(?:支付|付款|结算)|"
        r"(?:支付|付款|结算)[^。；]{0,35}验收(?:合格|通过)",
        compact,
    ))
    target_as_acceptance_condition = bool(
        quantitative_target_matches
        and (
            any(term in acceptance_text for term in (
                "响应时间", "执行时间", "使用率", "降低30%", "降低20%", "性能指标作为验收",
            ))
            or bool(re.search(
                r"按照第[\u4e00-\u9fa5\d]+条[^。；]{0,20}(?:技术服务)?质量要求[^。；]{0,16}(?:验收|进行验收)",
                compact,
            ))
        )
    )
    performance_acceptance_disconnect = bool(
        quantitative_target_matches
        and payment_tied_to_acceptance
        and not target_as_acceptance_condition
        and (performance_target_weakening or standard_deferred)
    )
    remedy_deadline_specific = bool(re.search(
        r"(?:应|须)(?:在)?\d+(?:个)?(?:工作日|日|小时)内(?:完成)?(?:修改|整改|修复)|"
        r"(?:修改|整改|修复)期限(?:为|：|:)\d+",
        acceptance_text,
    ))

    result_scope_terms = (
        "项目成果", "软件功能", "程序代码", "技术文档", "新技术成果", "服务成果",
        "诊断方法", "优化方法", "技术经验", "技术方案", "诊断报告", "优化建议书",
        "咨询报告", "测试结果", "方法成果",
    )
    result_segments = [
        segment for segment in compact_segments
        if any(term in segment for term in result_scope_terms)
        and any(term in segment for term in ("知识产权", "归属", "归甲方", "归乙方", "归双方", "属于甲方", "属于乙方", "内部使用", "内部经营", "内部管理", "用于其他客户"))
    ]
    result_text = "".join(result_segments)
    ownership_deferred = any(
        term in result_text for term in ("另行协商确定", "另行协商", "另行约定", "后续确定", "另行确认")
    )
    ownership_finalized = bool(re.search(
        r"(?:项目成果|软件功能|程序代码|技术文档|新技术成果|服务成果|诊断方法|优化方法|技术经验|技术方案|诊断报告|优化建议书|咨询报告|测试结果)[^。；]{0,140}"
        r"(?:知识产权)?(?:归|属于)(?:甲方|乙方|双方)(?:所有|共有)?",
        result_text,
    )) and not ownership_deferred
    owner_match = re.search(
        r"(?:项目成果|软件功能|程序代码|技术文档|新技术成果|服务成果|诊断方法|优化方法|技术经验|技术方案|诊断报告|优化建议书|咨询报告|测试结果)[^。；]{0,140}"
        r"(?:知识产权)?(?:归|属于)(甲方|乙方|双方)(?:所有|共有)?",
        result_text,
    )
    ownership_party = owner_match.group(1) if owner_match and ownership_finalized else ""
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
    # A nearby second party's role declaration must not become the first
    # party's role after whitespace compaction joins two header lines.
    role_text = re.sub(r'[^\S\r\n]+', '', text or '')
    provider_party = (
        "甲方" if re.search(r"甲方(?:(?!乙方)[^。；\n]){0,15}(?:服务提供方|技术服务提供方|服务方)", role_text)
        else "乙方" if re.search(r"乙方(?:(?!甲方)[^。；\n]){0,15}(?:服务提供方|技术服务提供方|服务方)", role_text)
        else "甲方" if re.search(r"(?:受托人|受托方)[：:]?[^。；\n]{0,60}[（(]?甲方[）)]?", role_text)
        else "乙方" if re.search(r"(?:受托人|受托方)[：:]?[^。；\n]{0,60}[（(]?乙方[）)]?", role_text)
        else ""
    )
    recipient_party = "乙方" if provider_party == "甲方" else "甲方" if provider_party == "乙方" else ""
    deliverable_terms = (
        "诊断报告", "优化建议书", "技术方案", "技术优化报告", "算法参数文件",
        "测试结果记录", "测试记录", "测试报告", "服务记录", "现场技术服务",
        "现场技术培训", "技术培训", "技术咨询支持", "咨询报告", "分析报告", "评估报告",
        "培训材料", "操作手册", "接口文档",
    )
    deliverable_segments: List[str] = []
    for segment in compact_segments:
        matched_terms = [term for term in deliverable_terms if term in segment]
        if not matched_terms:
            continue
        if any(term in segment for term in (
            "不得", "禁止", "无偿归", "知识产权归属", "许可", "转让",
            "第三方主张", "第三方授权", "侵权", "替代方案",
        )):
            continue
        recipient_is_supplier = bool(
            recipient_party
            and re.search(rf"{re.escape(recipient_party)}[^。；\n]{{0,12}}(?:提交|交付|提供)", segment)
        )
        has_delivery_language = any(term in segment for term in ("交付", "提交", "提供", "成果", "包括"))
        standalone_deliverable_line = (
            len(segment) <= 36
            and not any(party in segment for party in ("甲方", "乙方", "丙方", "丁方"))
            and not any(term in segment for term in ("源代码", "现有系统", "技术资料", "测试数据"))
            and any(segment.rstrip("。；;，,").endswith(term) for term in matched_terms)
        )
        # A compact enumerated deliverable list (two or more concrete terms) is
        # also evidence even if the list line itself omits the delivery verb.
        if (has_delivery_language and not recipient_is_supplier) or len(matched_terms) >= 2 or standalone_deliverable_line:
            deliverable_segments.append(segment)
    actual_deliverables = [
        term for term in deliverable_terms
        if any(term in segment for segment in deliverable_segments)
        and not any(term != longer and term in longer and any(longer in segment for segment in deliverable_segments)
                    for longer in deliverable_terms)
    ]

    def deliverable_type(name: str) -> str:
        if any(term in name for term in ("测试记录", "测试报告", "测试结果")):
            return "TEST_RECORD"
        if any(term in name for term in ("参数文件", "数据集", "数据文件")):
            return "DATA_OR_PARAMETER_FILE"
        if "现场" in name and "服务" in name:
            return "ONSITE_SERVICE"
        if "培训" in name:
            return "TRAINING"
        if any(term in name for term in ("咨询", "支持")):
            return "SUPPORT_OR_CONSULTING"
        if any(term in name for term in ("软件", "源代码", "算法", "模型", "模块")) and "报告" not in name:
            return "SOFTWARE_OR_TECHNICAL_ARTIFACT"
        return "DOCUMENT_OR_REPORT"

    deliverable_facts: List[Dict[str, Any]] = []
    service_location_match = re.search(
        r"技术服务地点[：:]?([^\n。；;]+)",
        text,
    )
    service_location = service_location_match.group(1).strip() if service_location_match else ""
    for name in actual_deliverables:
        source_segments = [segment for segment in deliverable_segments if name in segment]
        source_text = "；".join(source_segments)
        quantity_token = r"(?:\d+(?:\.\d+)?|[一二两三四五六七八九十百]+)\s*(?:份|套|次|场|小时|工作日|人次)"
        quantity_match = (
            re.search(rf"{re.escape(name)}[^。；]{{0,24}}({quantity_token})", source_text)
            or re.search(rf"({quantity_token})[^。；]{{0,24}}{re.escape(name)}", source_text)
        )
        version_match = re.search(
            rf"(?:{re.escape(name)}[^。；]{{0,24}}|[^。；]{{0,24}}{re.escape(name)})"
            r"((?:V|v)?\d+(?:\.\d+)+(?:版|版本)?|最终版|定稿版)",
            source_text,
        )
        title_candidates = re.findall(
            r"《([^ 》]*(?:报告|建议书|方案|清单|记录)[^》]*)》",
            source_text,
        )
        document_title_value = next(
            (candidate.strip() for candidate in title_candidates if name in candidate),
            title_candidates[0].strip() if len(title_candidates) == 1 else None,
        )
        support_duration_match = re.search(
            r"((?:项目结束|合同终止|最终验收)(?:之)?后?"
            r"(?:\d+(?:\.\d+)?|[一二三四五六七八九十百]+)"
            r"(?:个)?(?:工作日|日|月|年))",
            source_text,
        )
        acceptance_basis = ""
        if any(term in source_text for term in ("验收标准", "验收基线", "确认单", "签字确认", "验收合格")):
            acceptance_basis = source_text
        deliverable_kind = deliverable_type(name)
        covered_fields = ["name"]
        if quantity_match:
            covered_fields.append("quantity")
        if version_match:
            covered_fields.append("version")
        if acceptance_basis:
            covered_fields.append("acceptance_basis")
        if document_title_value:
            covered_fields.append("document_title")
        if support_duration_match:
            covered_fields.append("support_duration")
        if deliverable_kind == "ONSITE_SERVICE" and service_location:
            covered_fields.append("service_location")
        deliverable_facts.append({
            "name": name,
            "type": deliverable_kind,
            "document_title": document_title_value,
            "quantity": quantity_match.group(1) if quantity_match else None,
            "version": version_match.group(1) if version_match else None,
            "acceptance_basis": acceptance_basis or None,
            "support_duration": support_duration_match.group(1) if support_duration_match else None,
            "service_location": service_location if deliverable_kind == "ONSITE_SERVICE" and service_location else None,
            "covered_fields": covered_fields,
            "partial_fields": [],
            "source_segments": source_segments,
        })

    test_control_match = re.search(
        r"(测试数据|测试数据集|样本数据|测试设备|测试环境|测试方法)"
        r"[^。；]{0,80}由(甲方|乙方|双方)(?:单方)?(?:确定|决定|指定|制定)",
        compact,
    )

    def concrete_test_detail(subject_pattern: str, value_pattern: str) -> bool:
        """A control-right statement is not a concrete test parameter."""
        for segment in compact_segments:
            if not re.search(subject_pattern, segment):
                continue
            if re.search(
                rf"{subject_pattern}[^。；]{{0,80}}由(?:甲方|乙方|双方)(?:单方)?"
                r"(?:确定|决定|指定|制定|另行确定)",
                segment,
            ):
                continue
            if re.search(value_pattern, segment):
                return True
        return False

    test_data_scope_defined = concrete_test_detail(
        r"(?:测试数据集|测试数据|样本数据)",
        r"(?:测试数据集|测试数据|样本数据)[^。；]{0,20}"
        r"(?:为|包括|采用|使用|范围|来源|数量|不少于|具体)",
    )
    test_equipment_defined = concrete_test_detail(
        r"(?:测试设备|硬件设备)",
        r"(?:测试设备|硬件设备)[^。；]{0,20}(?:为|包括|采用|型号|配置|数量|具体)",
    )
    test_environment_defined = concrete_test_detail(
        r"(?:测试环境|运行环境|硬件条件)",
        r"(?:测试环境|运行环境|硬件条件)[^。；]{0,24}(?:为|包括|采用|配置|具体|应满足)",
    )
    test_method_defined = concrete_test_detail(
        r"(?:测试方法|测试步骤|测试工具|统计方法|统计口径)",
        r"(?:测试方法|测试步骤|测试工具|统计方法|统计口径)"
        r"[^。；]{0,24}(?:为|包括|采用|按照|具体|计算)",
    )
    liability_cap_match = re.search(
        r"(甲方|乙方)[^。；]{0,30}(?:承担的)?(?:全部|累计)?赔偿责任[^。；]{0,35}"
        r"(?:最高不超过|不超过)[^。；]{0,45}(?:已经|实际)?支付[^。；]{0,25}(?:技术服务费用|服务费用|服务费)",
        compact,
    )
    cap_party = liability_cap_match.group(1) if liability_cap_match else ""
    excluded_loss_aliases = {
        "profit_loss": ("利润损失", "可得利益", "预期利益"),
        "business_interruption": ("业务中断损失", "业务中断"),
        "third_party_claim": ("第三方索赔", "第三方权利主张"),
        "data_loss": ("数据损失", "数据丢失"),
        "indirect_loss": ("间接损失", "附带损失"),
    }
    excluded_loss_types = [
        key for key, aliases in excluded_loss_aliases.items()
        if any(alias in compact for alias in aliases)
        and any(term in compact for term in ("不承担责任", "不予赔偿", "免责", "不负责"))
    ]
    operational_exposure_facts = {
        "production_system_access": any(term in compact for term in ("生产数据库", "生产环境", "ERP系统")),
        "database_access": any(term in compact for term in ("访问甲方测试数据库", "访问甲方生产数据库", "访问生产数据库")),
        "configuration_or_parameter_change": any(term in compact for term in ("参数调整", "参数修改", "SQL优化", "系统优化")),
        "provider_data_processing": any(term in compact for term in ("订单数据", "员工账号信息", "数据库备份", "复制至乙方测试服务器")),
        "business_interruption_exposure": any(term in compact for term in ("无法正常运行", "业务中断", "系统恢复")),
    }
    provider_cap_and_broad_exclusion_risk = bool(
        liability_cap_match
        and provider_party
        and cap_party == provider_party
        and len(excluded_loss_types) >= 2
        and sum(bool(value) for value in operational_exposure_facts.values()) >= 2
    )

    return {
        "acceptance": {
            "mechanism_present": any(term in acceptance_text for term in (
                "验收通知", "通知乙方进行验收", "提交验收申请", "提出验收申请",
            )),
            "standard_referenced": "验收标准" in compact,
            "standard_deferred": standard_deferred,
            "standard_concrete": standard_concrete,
            "quantitative_targets_present": bool(quantitative_target_matches),
            "quantitative_target_evidence": quantitative_target_matches,
            "performance_target_weakening": performance_target_weakening,
            "payment_tied_to_acceptance": payment_tied_to_acceptance,
            "target_as_acceptance_condition": target_as_acceptance_condition,
            "performance_acceptance_disconnect": performance_acceptance_disconnect,
            "test_determination_authority": test_control_match.group(2) if test_control_match else "",
            "test_parameters_controlled_but_not_fixed": bool(test_control_match),
            "test_environment_defined": test_environment_defined,
            "test_equipment_defined": test_equipment_defined,
            "test_dataset_defined": test_data_scope_defined,
            "test_method_defined": test_method_defined,
            "retest_mechanism_defined": any(term in compact for term in ("复测", "重新测试", "第三方检测", "第三方复核")),
            "deadline_defined": bool(re.search(r"收到验收(?:通知|申请)后\d+(?:个)?工作日内", acceptance_text)),
            "written_objection": "书面异议" in acceptance_text,
            "deemed_acceptance": bool(re.search(
                r"未[^。；]{0,24}提出书面异议[^。；]{0,40}视为[^。；]{0,30}验收合格",
                acceptance_text,
            )),
            "remedy_present": any(term in acceptance_text for term in ("问题清单", "完成修改", "整改", "修复")),
            "remedy_deadline_specific": remedy_deadline_specific,
            "remedy_deadline_vague": "合理期限" in acceptance_text and not remedy_deadline_specific,
        },
        "service_generated_result": {
            "scope_defined": bool(result_segments),
            "ownership_deferred": ownership_deferred,
            "ownership_finalized": ownership_finalized,
            "ownership_party": ownership_party,
            "interim_use_arranged": interim_use,
            "recipient_internal_use_only": bool(re.search(
                r"(?:甲方|乙方)[^。；]{0,25}(?:企业|公司|集团)?内部[^。；]{0,12}(?:使用|管理)|"
                r"(?:仅限|可供)(?:甲方|乙方)[^。；]{0,20}内部[^。；]{0,12}(?:使用|管理)",
                compact,
            )),
            "third_party_sharing_restricted": bool(re.search(r"未经[^。；]{0,30}(?:书面)?同意[^。；]{0,40}不得[^。；]{0,30}(?:第三方|对外提供)|不得[^。；]{0,40}(?:提供给|披露给)第三方", compact)),
            "provider_reuse_allowed": bool(re.search(r"乙方[^。；]{0,30}(?:可以|有权)[^。；]{0,80}(?:用于其他客户|其他客户项目|继续使用|继续利用)", compact)),
            "evidence_segments": result_segments,
        },
        "liability": {
            "third_party_platform_exception": any(term in compact for term in ("第三方云服务", "第三方平台接口", "电商平台接口故障"))
            and any(term in compact for term in ("不承担责任", "免责")),
            "indirect_loss_exclusion": any(term in compact for term in ("间接", "附带", "惩罚性损失"))
            and any(term in compact for term in ("不负责", "不承担责任", "概不负责")),
            "service_provider_party": provider_party,
            "service_recipient_party": recipient_party,
            "provider_liability_cap": bool(liability_cap_match and cap_party == provider_party),
            "liability_cap_party": cap_party,
            "liability_cap_basis": "PAID_SERVICE_FEES" if liability_cap_match else "",
            "excluded_loss_types": excluded_loss_types,
            "broad_loss_exclusion": len(excluded_loss_types) >= 2,
            "operational_exposure_facts": operational_exposure_facts,
            "high_operational_exposure": sum(bool(value) for value in operational_exposure_facts.values()) >= 2,
            "provider_cap_and_broad_exclusion_risk": provider_cap_and_broad_exclusion_risk,
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
        "technical_materials": {
            "actual_deliverables": actual_deliverables,
            "deliverable_facts": deliverable_facts,
            "evidence_segments": deliverable_segments,
            "source_code_delivery_excluded": bool(re.search(
                r"(?:不负责|无需|不向)[^。；]{0,50}(?:交付|提供)[^。；]{0,40}(?:源代码|新的ERP软件|独立软件产品)|"
                r"(?:不交付|无需交付)[^。；]{0,30}(?:源代码|软件产品)",
                compact,
            )),
        },
    }


def _personal_information_processing_analysis(text: str) -> Dict[str, Any]:
    compact = re.sub(r"\s+", "", text or "")
    strong_category_markers = (
        "姓名", "工号", "身份证", "电话号码", "手机号", "电子邮箱", "定位信息",
        "企业邮箱", "生物识别", "收货地址", "联系地址", "员工数据", "员工信息", "员工账号信息",
        "用户数据", "消费者数据", "订单数据",
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
    strong_fact_evidence: Dict[str, List[str]] = {
        "production_database_access": [],
        "personal_data_access": [],
        "data_transfer_to_provider": [],
        "data_copy_to_provider_server": [],
        "data_storage_by_provider": [],
        "data_analysis_by_provider": [],
        "real_data_processing": [],
    }
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
            r"(?:个人信息|个人数据|员工信息|员工账号信息|用户信息|客户信息|消费者信息|订单数据|数据库备份|数据可能包括|数据包括)",
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
        copy_to_provider_server = bool(re.search(
            r"(?:乙方|服务方|开发方|受托方)[^。；]{0,35}(?:复制|传输|转移|保存|存储)"
            r"[^。；]{0,45}(?:乙方|服务方|开发方|受托方)[^。；]{0,20}(?:服务器|测试服务器|环境)",
            segment_compact,
        ))
        provider_analysis = bool(re.search(
            r"(?:乙方|服务方|开发方|受托方)[^。；]{0,30}(?:对|将)"
            r"[^。；]{0,25}(?:甲方|委托方|客户)?[^。；]{0,15}"
            r"(?:数据|数据库备份|订单数据|员工账号信息)[^。；]{0,20}(?:进行)?(?:分析|诊断|测试|优化)",
            segment_compact,
        )) or bool(re.search(
            r"(?:复制|传输|转移)[^。；]{0,60}(?:服务器|测试服务器)[^。；]{0,30}(?:分析|诊断|测试|优化)",
            segment_compact,
        ))
        if not administrative_contact and (
            explicit_delegation or actual_data_delivery or production_access
            or managed_processing or continuing_processing or copy_to_provider_server or provider_analysis
        ):
            delegated_processing_segments.append(segment_compact)
            if production_access:
                strong_fact_evidence["production_database_access"].append(segment_compact)
            if actual_data_delivery:
                strong_fact_evidence["data_transfer_to_provider"].append(segment_compact)
            if copy_to_provider_server:
                strong_fact_evidence["data_copy_to_provider_server"].append(segment_compact)
                strong_fact_evidence["data_storage_by_provider"].append(segment_compact)
            if provider_analysis or continuing_processing:
                strong_fact_evidence["data_analysis_by_provider"].append(segment_compact)
            if explicit_personal_data or segment_categories:
                strong_fact_evidence["personal_data_access"].append(segment_compact)
            if actual_data_delivery or production_access or managed_processing or continuing_processing or copy_to_provider_server:
                strong_fact_evidence["real_data_processing"].append(segment_compact)
        if active_list_heading and segment != active_list_heading:
            active_list_remaining -= 1
            if not segment_categories and not any(marker in segment for marker in ("包括", "如下", "字段")):
                active_list_heading = ""
                active_list_remaining = 0
        if active_list_remaining <= 0:
            active_list_heading = ""
    feature_text = "".join(feature_segments)
    matched_categories = [marker for marker in category_markers if marker in feature_text]
    # Actual access/analysis of non-personal operational data is not by itself
    # a personal-information delegation.  Require both a real provider-side
    # processing act and an affirmative personal-data/category signal.
    triggered = bool(delegated_processing_segments) and bool(
        feature_segments or strong_fact_evidence["personal_data_access"]
    )
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
    explicit_scope_definition = any(marker in compact for marker in control_groups["scope"])
    # Concrete categories already extracted from operative processing clauses
    # are affirmative scope evidence.  They may be incomplete, but an absence
    # search must not report the information categories as wholly missing.
    if matched_categories:
        controls["scope"] = True
    control_coverage = {
        key: (
            "COVERED"
            if present and (key != "scope" or explicit_scope_definition)
            else "PARTIALLY_COVERED"
            if key == "scope" and bool(matched_categories)
            else "MISSING"
        )
        for key, present in controls.items()
    }
    missing = [key for key, present in controls.items() if not present]
    strong_facts = {key: bool(rows) for key, rows in strong_fact_evidence.items()}
    return {
        "triggered": triggered,
        "feature_scope_present": bool(feature_segments),
        "delegated_processing_present": triggered,
        "trigger_strength": "STRONG" if triggered else "WEAK" if feature_segments else "NONE",
        "feature_segments": feature_segments,
        "delegated_processing_segments": delegated_processing_segments,
        "matched_categories": matched_categories,
        "personal_data_categories": matched_categories,
        "strong_facts": strong_facts,
        "strong_fact_evidence": strong_fact_evidence,
        "controls": controls,
        "control_coverage": control_coverage,
        "missing_controls": missing,
        "gap": triggered and bool(missing),
    }


def analyze_personal_information_processing(text: str) -> Dict[str, Any]:
    """Public structured view used by evidence and absence-search layers."""
    return _personal_information_processing_analysis(text)


def analyze_technology_relationship_risks(text: str) -> Dict[str, Dict[str, Any]]:
    compact = re.sub(r"\s+", "", text or "")
    classification = classify_technology_transaction(text)
    payment = analyze_payment_schedule(text)
    timeline = analyze_timeline(text)
    timeline_conflict_present = bool(timeline["conflicts"])
    if (
        timeline.get("primary_conflict_subject") == "LICENSE_START"
        and classification.get("primary_subtype") != "TECHNOLOGY_LICENSE"
    ):
        # A transfer contract may disclose a pre-existing licence as an
        # encumbrance.  Its historical licence period is not the start of the
        # current transfer contract's performance.
        timeline_conflict_present = False

    def signal(present: bool, terms: tuple[str, ...], reason: str) -> Dict[str, Any]:
        evidence = [term for term in terms if term in compact]
        return {"present": bool(present), "evidence_terms": evidence, "reason": reason}

    subjective_acceptance = any(term in compact for term in (
        "实际使用效果", "实际使用要求", "业务部门认可", "业务部门意见决定是否通过",
        "直至甲方满意", "甲方满意",
    ))
    no_deemed_acceptance = any(term in compact for term in ("不视为验收合格", "不视为通过"))
    unlimited_rectification = any(term in compact for term in ("直至甲方验收合格", "整改直至验收通过"))
    background_overtransfer = classification["involves_background_ip"] and any(
        term in compact for term in ("通用算法、规则模板、技术框架", "既有工具相关改进成果", "规则引擎相关改进成果")
    ) and "甲方所有" in compact
    cumulative_uncapped = "不设最高限额" in compact and any(term in compact for term in ("同时适用", "累计适用"))
    liability_remedies = {
        "daily_fixed": bool(re.search(r"每(?:逾期|超过)?(?:一|1)天[^。；]{0,35}(?:违约金|支付)[^。；]{0,20}(?:元|￥|¥)", compact)),
        "daily_percentage": bool(re.search(
            r"每(?:逾期|迟延|延迟|超过)?(?:一|1)(?:天|日)[^。；]{0,40}"
            r"\d+(?:\.\d+)?%[^。；]{0,20}违约金",
            compact,
        )),
        "termination_percentage": bool(re.search(r"(?:解除|终止)[^。；]{0,100}\d+(?:\.\d+)?%[^。；]{0,20}违约金|\d+(?:\.\d+)?%[^。；]{0,35}违约金[^。；]{0,35}(?:解除|终止)", compact)),
        "all_losses": "全部损失" in compact,
        "lost_profit": "可得利益" in compact,
        "third_party": any(term in compact for term in ("第三方的赔偿", "第三方赔偿", "支付给第三方")),
        "enforcement_costs": any(term in compact for term in ("律师费", "诉讼费用", "公证费", "调查取证费用")),
    }
    liability_overlap = sum(bool(value) for value in liability_remedies.values()) >= 4 and any(
        term in compact for term in ("同时仍应", "全部损失", "包括但不限于")
    )
    liability_cap_validity_segments = [
        segment.strip()
        for segment in re.split(r"[。；;\n]", text or "")
        if segment.strip()
        and any(term in re.sub(r"\s+", "", segment) for term in ("责任上限", "责任限制", "累计不超过", "最高不超过", "上述责任限制"))
        and any(term in re.sub(r"\s+", "", segment) for term in ("仍然适用", "仍适用", "继续适用", "不受影响", "适用于"))
        and not any(term in re.sub(r"\s+", "", segment) for term in ("不适用于", "不再适用", "排除适用"))
        and any(term in re.sub(r"\s+", "", segment) for term in ("故意", "重大过失"))
    ]
    broad_liability_cap_segments = [
        segment.strip()
        for segment in re.split(r"[。；;\n]", text or "")
        if segment.strip()
        and any(term in re.sub(r"\s+", "", segment) for term in (
            "任何和所有责任", "任何及所有责任", "全部责任", "全部赔偿责任", "所有责任", "累计责任", "累计赔偿责任",
        ))
        and any(term in re.sub(r"\s+", "", segment) for term in (
            "限制在", "限定在", "限于", "不超过", "责任上限", "责任限制",
        ))
    ]
    personal_or_property_damage_segments = [
        segment.strip()
        for segment in re.split(r"[。；;\n]", text or "")
        if segment.strip()
        and any(term in re.sub(r"\s+", "", segment) for term in (
            "人身损害", "人身伤害", "人员伤亡", "财产损失", "财产损害",
        ))
        and any(term in re.sub(r"\s+", "", segment) for term in (
            "承担责任", "赔偿", "负责", "过失", "疏忽", "损害责任", "伤害责任",
        ))
        and not any(term in re.sub(r"\s+", "", segment) for term in (
            "不适用责任上限", "责任上限不适用", "不受责任上限限制", "排除责任上限",
        ))
    ]
    cap_scope_segments = [
        segment.strip()
        for segment in re.split(r"[。；;\n]", text or "")
        if segment.strip()
        and any(term in re.sub(r"\s+", "", segment) for term in ("责任上限", "责任限制", "前述上限"))
        and any(term in re.sub(r"\s+", "", segment) for term in ("适用于", "包括", "覆盖"))
        and any(term in re.sub(r"\s+", "", segment) for term in (
            "人身损害", "人身伤害", "人员伤亡", "故意", "重大过失",
        ))
        and not any(term in re.sub(r"\s+", "", segment) for term in ("不适用于", "排除适用"))
    ]
    for segment in cap_scope_segments:
        if segment not in liability_cap_validity_segments:
            liability_cap_validity_segments.append(segment)
    if broad_liability_cap_segments and personal_or_property_damage_segments:
        for segment in broad_liability_cap_segments:
            if segment not in liability_cap_validity_segments:
                liability_cap_validity_segments.append(segment)
    liability_cap_validity = bool(liability_cap_validity_segments)
    cap_fault_categories = [
        label for label in ("故意", "重大过失")
        if any(
            label in segment
            and not bool(re.search(rf"(?:除|不包括|排除)[^。；]{{0,30}}{label}", segment))
            for segment in liability_cap_validity_segments
        )
    ]
    cap_damage_categories = [
        label for label, aliases in (
            ("人身损害", ("人身损害", "人身伤害", "人员伤亡")),
            ("财产损失", ("财产损失", "财产损害")),
        )
        if any(any(alias in segment for alias in aliases) for segment in liability_cap_validity_segments)
    ]
    cap_fact_sources = list(liability_cap_validity_segments[:2])
    if broad_liability_cap_segments and personal_or_property_damage_segments:
        cap_fact_sources = [personal_or_property_damage_segments[0], broad_liability_cap_segments[0]]
    cap_fact_text = "；".join(dict.fromkeys(cap_fact_sources))
    liability_cap_contract_fact = (
        f"合同明确约定{cap_fact_text.rstrip('。')}。"
        if cap_fact_text else ""
    )

    daily_penalties: List[Dict[str, Any]] = []
    def penalty_parties_and_trigger(source_text: str) -> Dict[str, str]:
        normalized = re.sub(r"\s+", "", source_text or "")
        party_pattern = r"甲方|乙方|委托方|受托方|咨询方|服务方|服务提供方|服务接受方|许可方|被许可方|转让方|受让方|买方|卖方"
        # Resolve the party nearest to the obligation verb.  A leading
        # obligee mentioned in the same local context must not be inherited
        # as the obligor of a staged payment/penalty subparagraph.
        direct_obligor_matches = list(re.finditer(
            rf"(?P<party>{party_pattern})(?:(?!(?:{party_pattern})).){{0,70}}?"
            rf"(?:应当|应|须).{{0,55}}?(?:支付|承担)",
            normalized,
        ))
        breach_obligor_matches = list(re.finditer(
            rf"(?P<party>{party_pattern})(?:(?!(?:{party_pattern})).){{0,45}}?"
            rf"(?:违反|违约|逾期|未按|未履行|泄露|泄密).{{0,90}}?(?:支付|承担)",
            normalized,
        ))
        obligor_match = (
            direct_obligor_matches[-1]
            if direct_obligor_matches else
            breach_obligor_matches[-1]
            if breach_obligor_matches else None
        )
        obligee_match = re.search(rf"向(?P<party>{party_pattern})支付", normalized)
        obligor = obligor_match.group("party") if obligor_match else ""
        obligee = obligee_match.group("party") if obligee_match else ""
        if not obligee and obligor == "甲方":
            obligee = "乙方"
        elif not obligee and obligor == "乙方":
            obligee = "甲方"
        trigger = re.split(r"(?:，?应(?:当)?向|，?应(?:当)?支付|，?每逾期|，?按)", source_text, maxsplit=1)[0].strip(" ，；;。")
        return {"obligor": obligor, "obligee": obligee, "trigger": trigger}

    for match in re.finditer(
        r"(?P<text>[^。；;\n]{0,45}每(?:逾期|迟延|延迟|超过)(?:一|1)(?:日|天)[^。；;\n]{0,70}?"
        r"(?P<rate>\d+(?:\.\d+)?)%[^。；;\n]{0,35}(?:违约金|支付))",
        text or "",
    ):
        rate = _decimal(match.group("rate"))
        source_text = match.group("text").strip()
        daily_penalties.append({
            "rate_percent_per_day": _number(rate),
            "source_text": source_text,
            "potentially_excessive": rate >= Decimal("0.1"),
            "calculation_method": "DAILY_PERCENTAGE",
            **penalty_parties_and_trigger(source_text),
        })

    weekly_penalties: List[Dict[str, Any]] = []
    for segment_match in re.finditer(r"[^。；;\n]+", text or ""):
        segment = segment_match.group(0).strip()
        compact_segment = re.sub(r"\s+", "", segment)
        if "每周" not in compact_segment or "%" not in compact_segment:
            continue
        rates = [
            _decimal(rate)
            for rate in re.findall(r"(?:每周(?:支付|按|计收)?|按每周)\D{0,18}(\d+(?:\.\d+)?)\s*%", compact_segment)
        ]
        if not rates:
            rates = [_decimal(rate) for rate in re.findall(r"(\d+(?:\.\d+)?)\s*%", compact_segment)]
        if not rates:
            continue
        party_context = penalty_parties_and_trigger(segment)
        if not party_context.get("obligor"):
            # Staged rates are often listed on separate subparagraphs below a
            # lead-in that identifies the obligor and obligee.  Inherit only
            # the immediately preceding local clause context, never another
            # contract or a process-level fallback.
            context_start = max(0, segment_match.start() - 240)
            local_context = (text or "")[context_start:segment_match.start()]
            contextual_parties = penalty_parties_and_trigger(local_context + segment)
            if contextual_parties.get("obligor"):
                party_context = {
                    **party_context,
                    "obligor": contextual_parties.get("obligor") or "",
                    "obligee": contextual_parties.get("obligee") or "",
                    "party_context_source": "IMMEDIATE_PRECEDING_CLAUSE",
                }
        weekly_penalties.append({
            "rates_percent_per_week": [_number(rate) for rate in rates],
            "max_rate_percent_per_week": _number(max(rates)),
            "source_text": segment,
            "potentially_excessive": max(rates) >= Decimal("2"),
            "calculation_method": "WEEKLY_SEGMENTED_PERCENTAGE" if len(rates) > 1 else "WEEKLY_PERCENTAGE",
            **party_context,
        })
    cumulative_penalty_caps: List[Dict[str, Any]] = []
    for segment in [row.strip() for row in re.split(r"[。；;\n]+", text or "") if row.strip()]:
        normalized = re.sub(r"\s+", "", segment)
        if not (
            any(term in normalized for term in ("违约金", "延迟赔偿", "迟延赔偿"))
            and any(term in normalized for term in ("累计", "总额", "最高"))
            and any(term in normalized for term in ("不超过", "不得超过", "上限为", "最高为"))
        ):
            continue
        percentage_values = re.findall(r"(\d+(?:\.\d+)?)\s*%", normalized)
        if not percentage_values:
            continue
        # A cap clause can also repeat an earlier staged rate.  The cap is the
        # percentage nearest the end of this same clause, not a digit suffix
        # accidentally left after a greedy regex (for example 30% -> 0%).
        cap = _decimal(percentage_values[-1])
        cumulative_penalty_caps.append({
            "cap_percent": _number(cap),
            "source_text": segment,
            "potentially_excessive": cap >= Decimal("30"),
        })

    fixed_penalties: List[Dict[str, Any]] = []
    contract_total = payment.get("contract_total")
    total_decimal = Decimal(str(contract_total)) if contract_total else None
    for match in re.finditer(
        r"(?P<text>[^。；;\n]{0,90}(?:支付|承担)(?:人民币)?\s*"
        r"(?P<amount>[0-9][0-9,]*(?:\.\d+)?)\s*(?P<unit>万)?元违约金[^。；;\n]{0,45})",
        text or "",
    ):
        amount = _scaled_cny(match.group("amount"), match.group("unit"))
        ratio = (amount / total_decimal * Decimal("100")) if total_decimal else None
        source_text = match.group("text").strip()
        fixed_penalties.append({
            "amount": _number(amount),
            "contract_total_ratio_percent": _number(ratio) if ratio is not None else None,
            "source_text": source_text,
            "potentially_excessive": bool(ratio is not None and ratio >= Decimal("100")),
            "calculation_method": "FIXED_AMOUNT",
            **penalty_parties_and_trigger(source_text),
        })

    high_daily_penalties = [row for row in daily_penalties if row["potentially_excessive"]]
    high_weekly_penalties = [row for row in weekly_penalties if row["potentially_excessive"]]
    high_fixed_penalties = [row for row in fixed_penalties if row["potentially_excessive"]]
    high_cumulative_caps = [row for row in cumulative_penalty_caps if row["potentially_excessive"]]
    potential_excessive_liquidated_damages = bool(
        high_daily_penalties or high_weekly_penalties or high_fixed_penalties or high_cumulative_caps
    )
    def display_number(value: Any, digits: int = 2) -> str:
        numeric = Decimal(str(value))
        rendered = f"{numeric:.{digits}f}".rstrip("0").rstrip(".")
        return rendered or "0"

    def display_cny(value: Any) -> str:
        numeric = Decimal(str(value))
        if numeric % Decimal("10000") == 0:
            return f"{display_number(numeric / Decimal('10000'))}万元"
        return f"{display_number(numeric)}元"

    penalty_parts: List[str] = []
    if high_daily_penalties:
        rates = "、".join(
            f"每日{display_number(row['rate_percent_per_day'])}%" for row in high_daily_penalties
        )
        penalty_parts.append(f"按日违约金达到{rates}")
    if high_weekly_penalties:
        rate_groups = "、".join(
            "/".join(f"每周{display_number(rate)}%" for rate in row["rates_percent_per_week"])
            for row in high_weekly_penalties
        )
        penalty_parts.append(f"按周分段违约金达到{rate_groups}")
    if high_cumulative_caps:
        caps = "、".join(f"累计最高{display_number(row['cap_percent'])}%" for row in high_cumulative_caps)
        penalty_parts.append(f"累计上限达到{caps}")
    if high_fixed_penalties:
        amounts = "、".join(
            f"{display_cny(row['amount'])}（约为合同总价{display_number(row['contract_total_ratio_percent'])}%）"
            for row in high_fixed_penalties
        )
        penalty_parts.append(f"固定违约金包括{amounts}")
    excessive_penalty_reason = (
        "合同" + "，且".join(penalty_parts)
        + "；该比例仅用于识别异常计价标准，不等同于实际损失比例，发生争议时存在司法调减风险。"
        if penalty_parts else "未识别到明显异常的违约金金额或按日计收比例。"
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
    timeline_basis_label = "合同签订日期" if timeline.get("comparison_basis") == "SIGNING_DATE" else "合同生效日"
    timeline_boundary_label = "签订前" if timeline.get("comparison_basis") == "SIGNING_DATE" else "生效前"
    return {
        "acceptance_payment_control": signal(subjective_acceptance or no_deemed_acceptance or unlimited_rectification, ("实际使用效果", "实际使用要求", "业务部门认可", "甲方满意", "不视为验收合格", "直至甲方验收合格"), "量化验收标准受到主观决定、沉默不通过或无限整改安排削弱。"),
        "background_ip_overtransfer": signal(background_overtransfer, ("已有", "规则引擎", "通用算法、规则模板、技术框架", "规则引擎相关改进成果", "甲方所有"), "项目成果与服务方背景知识产权未隔离，通用能力可能被一并转让。"),
        "uncapped_cumulative_liability": signal(cumulative_uncapped, ("同时适用", "不设最高限额", "30%的违约金", "0.5%的违约金"), "服务方违约金、退款、赔偿与继续履行可叠加且累计责任无上限。"),
        "cumulative_liability_overlap": {
            **signal(liability_overlap, tuple(key for key, present in liability_remedies.items() if present), "多种违约金、全部损失和实现权利费用可能由同一违约链条触发，并用和抵扣关系不清。"),
            "analysis": liability_remedies,
        },
        "liability_cap_validity": {
            **signal(
                liability_cap_validity,
                (
                    "责任上限", "责任限制", "累计不超过", "最高不超过", "重大过失",
                    "仍然适用", "仍适用", "任何和所有责任", "人身损害", "财产损失",
                ),
                (
                    f"{liability_cap_contract_fact}重大过失仍受责任上限保护的约定存在效力风险。"
                    if cap_fault_categories and liability_cap_contract_fact
                    else f"{liability_cap_contract_fact}责任上限明确覆盖人身损害时，相关限责范围存在效力风险。"
                    if liability_cap_contract_fact and broad_liability_cap_segments and personal_or_property_damage_segments
                    else "合同将责任上限扩展至依法可能不得限责的责任情形，相关约定存在效力风险。"
                ),
            ),
            "analysis": {
                "contract_fact": liability_cap_contract_fact,
                "factual_fault_categories": cap_fault_categories,
                "factual_damage_categories": cap_damage_categories,
                "source_segments": liability_cap_validity_segments,
                "broad_cap_segments": broad_liability_cap_segments,
                "personal_or_property_damage_segments": personal_or_property_damage_segments,
                "personal_injury_within_broad_cap": bool(
                    broad_liability_cap_segments and personal_or_property_damage_segments
                ),
                "gross_negligence_within_cap": "重大过失" in cap_fault_categories,
                "intent_within_cap": "故意" in cap_fault_categories,
                "legal_effect_is_not_deterministically_invalid": True,
                "legal_rule": "民法典第506条对人身损害以及故意或者重大过失造成财产损失的免责条款设置效力限制。",
                "legal_consequence": "合同实际约定覆盖的过错或损害情形可能不受责任上限保护，但不当然影响整份合同效力。",
            },
        },
        "potential_excessive_liquidated_damages": {
            "present": potential_excessive_liquidated_damages,
            "evidence_terms": [
                term for term in ("每逾期一日", "违约金", "合同总额", "不足以弥补", "继续赔偿")
                if term in compact
            ],
            "reason": excessive_penalty_reason,
            "analysis": {
                "contract_total": contract_total,
                "daily_penalties": daily_penalties,
                "weekly_penalties": weekly_penalties,
                "cumulative_penalty_caps": cumulative_penalty_caps,
                "fixed_penalties": fixed_penalties,
                "high_daily_penalties": high_daily_penalties,
                "high_weekly_penalties": high_weekly_penalties,
                "high_cumulative_penalty_caps": high_cumulative_caps,
                "high_fixed_penalties": high_fixed_penalties,
                "contract_price_ratio_is_not_actual_loss_ratio": True,
            },
        },
        "unilateral_termination_change": signal(unilateral or forced_change, ("预算调整", "采购计划变更", "项目取消", "必须先行执行", "继续履行"), "委托方可将内部经营变化和未定价需求变更风险转由服务方承担。"),
        "demand_reduction_exit_cost": signal(demand_reduction_exit_cost, ("减少需求", "下降数额", "另外向", "补贴", "不得低于", "重新协商", "有权解除"), "减少采购内容仍触发额外补偿、最低价款和解除压力，形成需求调整及退出成本。"),
        "personal_information_processing_gap": {
            **signal(pii_gap, tuple(pii_analysis["matched_categories"]), "合同涉及个人信息委托处理，但处理要素、安全事件、监督和终止后处置机制不完整。"),
            "analysis": pii_analysis,
        },
        "payment_formula_inconsistency": signal(payment["status"] == "INCONSISTENT", tuple(), "付款比例、节点金额或合同总价之间存在确定性计算不一致。"),
        "timeline_conflict": signal(
            timeline_conflict_present,
            tuple(),
            f"技术资料交付义务早于{timeline_basis_label}，{timeline_boundary_label}履行边界不清。"
            if timeline.get("primary_conflict_subject") == "TECHNICAL_MATERIAL_DELIVERY"
            else f"许可开始日期早于{timeline_basis_label}，{timeline_boundary_label}许可实施边界不清。"
            if timeline.get("primary_conflict_subject") == "LICENSE_START"
            else f"服务开始义务早于{timeline_basis_label}，{timeline_boundary_label}履行边界不清。"
            if timeline.get("primary_conflict_subject") == "SERVICE_START"
            else f"履行义务早于{timeline_basis_label}，{timeline_boundary_label}履行边界不清。",
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
