"""Deterministic analysis shared by technology-service contract reviews."""

from __future__ import annotations

import re
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional


DATE_PATTERN = re.compile(r"(20\d{2})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日")
MONEY_PATTERN = r"([0-9][0-9,]*(?:\.\d+)?)\s*元"


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


def classify_technology_transaction(text: str) -> Dict[str, Any]:
    source_text = text or ""
    compact = re.sub(r"\s+", "", source_text)
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
        r"(?:许可人|卖方).{0,60}(?:许可|授予).{0,80}(?:被许可人|买方).{0,80}(?:实施|使用).{0,30}专利"
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
    add("TECHNICAL_CONSULTING", 12, "title:technical_consulting", consulting_title)
    add("TECHNICAL_CONSULTING", 5, "consulting_obligation", any(signal in compact for signal in consulting_signals))

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
    subtype = explicit_title_subtype or (ranked[0] if scores[ranked[0]] >= 6 else "GENERAL_TECHNOLOGY")
    tertiary_subtype = (
        "MIXED_PATENT_RIGHT_AND_APPLICATION_TRANSFER"
        if subtype == "TECHNOLOGY_TRANSFER" and granted_patent_asset and patent_application_asset
        else "PATENT_APPLICATION_RIGHT_TRANSFER"
        if subtype == "TECHNOLOGY_TRANSFER" and patent_application_asset
        else "PATENT_RIGHT_TRANSFER"
        if subtype == "TECHNOLOGY_TRANSFER" and (granted_patent_asset or "专利权" in compact)
        else "PATENT_LICENSE"
        if subtype == "TECHNOLOGY_LICENSE" and "专利" in compact
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

    title_transaction_type = explicit_title_subtype
    operative_transaction_type = (
        "TECHNOLOGY_TRANSFER" if patent_ownership_transfer and (transfer_registration or transfer_consideration)
        else "TECHNOLOGY_LICENSE" if patent_license_grant and (license_consideration or license_scope)
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
        "core_performance_obligations": snippets(("许可买方实施", "授予本专利实施许可", "转让给受让方", "转移至受让方", "共同研究开发", "委托研究开发", "解决特定技术问题")),
        "rights_transfer_method": snippets(("排他许可", "独占许可", "普通许可", "专利权转让", "转让登记", "变更登记")),
        "consideration_nature": snippets(("许可使用费", "实施许可使用费", "专利权转让价款", "技术服务费用", "研发费用", "咨询报酬")),
        "key_clauses": snippets(("许可范围", "许可期限", "专利权登记", "权利瑕疵", "开发成果", "咨询报告", "技术服务内容"), 8),
    }

    personal_information_terms = ("姓名", "工号", "电话号码", "电子邮箱", "身份证", "人脸", "操作日志")
    business_data_context = any(term in compact for term in (
        "数据可能包括", "测试数据", "数据源", "业务数据", "科研数据", "数据处理", "数据治理",
        "个人信息委托处理", "处理个人信息",
    ))
    personal_information_explicit = "个人信息" in compact and any(
        term in compact for term in ("处理", "收集", "存储", "使用", "传输", "删除", "委托")
    )
    university_data = any(term in compact for term in ("高校", "大学", "科研数据", "科研项目", "科研管理数据"))
    transaction_structure = (
        "B2B_PATENT_LICENSE_WITH_COMMISSIONED_DEVELOPMENT"
        if tertiary_subtype == "PATENT_LICENSE" and "COMMISSIONED_DEVELOPMENT" in secondary_modules
        else "B2B_PATENT_LICENSE"
        if tertiary_subtype == "PATENT_LICENSE"
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
        else "TECHNICAL_SERVICE"
        if subtype == "TECHNICAL_SERVICE"
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
        else "技术服务"
        if subtype == "TECHNICAL_SERVICE"
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
            "type": "technology_transfer" if subtype == "TECHNOLOGY_TRANSFER" else primary_contract_type,
            "subtype": tertiary_subtype.lower() if tertiary_subtype else subtype.lower(),
        },
        "secondary_transactions": list(secondary_contract_types),
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
        "license_mode": "EXCLUSIVE" if "排他实施许可" in compact else "SOLE" if "独占实施许可" in compact else "NON_EXCLUSIVE" if "普通实施许可" in compact else "",
        "referenced_contracts": [{"reference_type": "EXISTING_PATENT_LICENSE", "is_current_transaction": False}] if subtype == "TECHNOLOGY_TRANSFER" and any(term in compact for term in ("原专利实施许可合同", "普通实施许可")) else [],
        "involves_personal_information": (
            business_data_context and sum(term in compact for term in personal_information_terms) >= 2
        ) or personal_information_explicit,
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


def _contract_total(text: str) -> Optional[Decimal]:
    patterns = (
        rf"(?:合同总价|合同总额|合同价款|技术服务费用|专利权转让价款总额|专利权转让价款合计)[^。；\n]{{0,24}}?(?:为|共计|合计|总计|：|:)?\s*(?:人民币)?\s*{MONEY_PATTERN}",
        rf"(?:合同总价|合同总额|合同价款|技术服务费用|专利权转让价款总额|专利权转让价款合计)[^。；\n]{{0,12}}?人民币\s*{MONEY_PATTERN}",
    )
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return _decimal(match.group(1))
    return None


def analyze_payment_schedule(text: str) -> Dict[str, Any]:
    total = _contract_total(text or "")
    node_pattern = re.compile(
        rf"(?P<context>[^。；\n]{{0,55}}?)(?P<pct>\d+(?:\.\d+)?)\s*%[^。；\n]{{0,35}}?(?:即|为|计)\s*(?:人民币)?\s*{MONEY_PATTERN}",
        re.I,
    )
    nodes: List[Dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for match in node_pattern.finditer(text or ""):
        pct = _decimal(match.group("pct"))
        amount = _decimal(match.group(3))
        key = (str(pct), str(amount))
        if key in seen:
            continue
        seen.add(key)
        context = match.group("context")
        if any(term in context for term in ("上述付款比例合计", "付款比例合计", "金额合计")):
            continue
        included_retention = "包含" in context and any(term in context for term in ("质保", "保证金"))
        nodes.append({
            "percentage": _number(pct),
            "amount": _number(amount),
            "context": context.strip(),
            "retention_included": included_retention,
        })

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
    return {
        "status": "INCONSISTENT" if inconsistent else "CONSISTENT" if nodes and total is not None else "INSUFFICIENT_DATA",
        "contract_total": _number(total) if total is not None else None,
        "percentage_total": _number(percentage_total),
        "amount_total": _number(amount_total),
        "amount_delta": _number(amount_delta) if amount_delta is not None else None,
        "nodes": nodes,
        "node_mismatches": node_mismatches,
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
        r"(?:提供|提交)[^。\n]{0,12}(?:资料|数据)[^。\n]{0,35}",
        r"(?:资料|数据)[^。\n]{0,18}(?:提供|提交)[^。\n]{0,35}",
        r"应在\s*20\d{2}年\d{1,2}月\d{1,2}日前[^。\n]{0,30}(?:资料|数据)",
        r"(?:甲方|委托方|客户)[^。\n]{0,8}应在\s*20\d{2}年\d{1,2}月\d{1,2}日前[^。\n]{0,20}(?:提供|提交)",
    ))
    signature_dates = [_iso(match) for match in DATE_PATTERN.finditer(value) if "签订" in value[max(0, match.start() - 12):match.start()]]
    effective_date = _first_date(value, (r"(?:合同于|本合同于)[^。\n]{0,25}(?:签署|签订|生效)",))
    if not effective_date and "签字" in value and "生效" in value and signature_dates:
        effective_date = max(signature_dates)

    conflicts: List[Dict[str, Any]] = []
    if effective_date and service_start and service_start < effective_date:
        conflicts.append({"type": "SERVICE_BEFORE_EFFECTIVE", "earlier_date": service_start, "effective_date": effective_date})
    if effective_date and data_deadline and data_deadline < effective_date:
        conflicts.append({"type": "DATA_DUE_BEFORE_EFFECTIVE", "earlier_date": data_deadline, "effective_date": effective_date})
    return {
        "effective_date": effective_date,
        "service_start_date": service_start,
        "data_delivery_deadline": data_deadline,
        "conflicts": conflicts,
    }


def analyze_technical_service_risks(text: str) -> Dict[str, Dict[str, Any]]:
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
    unilateral = any(term in compact for term in ("预算调整", "采购计划变更", "项目取消")) and "解除" in compact
    forced_change = any(term in compact for term in ("必须先行执行", "应先行执行", "应当先行配合执行", "继续履行")) and any(term in compact for term in ("需求调整", "需求变更", "服务内容调整", "工作范围"))
    pii_gap = classification["involves_personal_information"] and not all(
        term in compact for term in ("处理目的", "处理期限", "处理方式", "转委托", "安全事件")
    )
    data_retention_conflict = any(term in compact for term in ("3个月内归还或者删除", "3个月内删除")) and any(term in compact for term in ("保证期", "质量保证期")) and "12个月" in compact
    injury_exclusion = "甲方过错" in compact and any(term in compact for term in ("未购买保险", "保险金额不足")) and any(term in compact for term in ("甲方不予赔偿", "甲方不承担责任"))
    short_data_objection = "3个工作日" in compact and any(term in compact for term in ("视为甲方提供的全部资料", "视为全部资料"))
    external_change_free = any(term in compact for term in ("调整业务规则", "修改测试环境", "更新第三方系统", "变更数据结构")) and any(term in compact for term in ("先行完成修正", "无偿修正"))
    return {
        "acceptance_payment_control": signal(subjective_acceptance or no_deemed_acceptance or unlimited_rectification, ("实际使用效果", "业务部门认可", "不视为验收合格", "直至甲方验收合格"), "量化验收标准受到主观决定、沉默不通过或无限整改安排削弱。"),
        "background_ip_overtransfer": signal(background_overtransfer, ("已有", "规则引擎", "通用算法、规则模板、技术框架", "规则引擎相关改进成果", "甲方所有"), "项目成果与服务方背景知识产权未隔离，通用能力可能被一并转让。"),
        "uncapped_cumulative_liability": signal(cumulative_uncapped, ("同时适用", "不设最高限额", "30%的违约金", "0.5%的违约金"), "服务方违约金、退款、赔偿与继续履行可叠加且累计责任无上限。"),
        "unilateral_termination_change": signal(unilateral or forced_change, ("预算调整", "采购计划变更", "项目取消", "必须先行执行", "继续履行"), "委托方可将内部经营变化和未定价需求变更风险转由服务方承担。"),
        "personal_information_processing_gap": signal(pii_gap, ("姓名", "工号", "电话号码", "电子邮箱", "操作日志"), "合同涉及个人信息委托处理，但处理要素、安全事件、监督和终止后处置机制不完整。"),
        "payment_formula_inconsistency": signal(payment["status"] == "INCONSISTENT", tuple(), "付款比例、节点金额或合同总价之间存在确定性计算不一致。"),
        "timeline_conflict": signal(bool(timeline["conflicts"]), tuple(), "合同生效日期晚于服务开始或资料提供期限，签署前履行边界不清。"),
        "data_retention_warranty_conflict": signal(data_retention_conflict, ("3个月内归还或者删除", "保证期", "12个月"), "资料删除期限早于保证期结束，可能妨碍缺陷复现和保证义务履行。"),
        "personal_injury_liability_exclusion": signal(injury_exclusion, ("甲方过错", "未购买保险", "保险金额不足", "甲方不予赔偿"), "甲方对自身过错造成的人身损害排除未投保或保险不足部分责任，可能存在效力风险。"),
        "short_data_objection_deemed_acceptance": signal(short_data_objection, ("3个工作日", "视为甲方提供的全部资料"), "资料异议期限过短且逾期视为全部合格，可能削弱乙方顺延及抗辩权。"),
        "external_change_free_remediation": signal(external_change_free, ("调整业务规则", "修改测试环境", "更新第三方系统", "变更数据结构", "先行完成修正"), "甲方或外部环境变化仍由乙方先行无偿修正，保证责任范围过宽。"),
    }
