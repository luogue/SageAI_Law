"""Resolve conflicts between a user-selected contract type and document evidence."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Sequence, Tuple

from review_v2.clause_parser import ParsedClause
from review_v2.domain_resolution import DomainResolution, resolve_contract_domain
from review_v2.technology_service_analysis import classify_technology_transaction
from review_v2.priority_contract_types import PRIORITY_TYPES, classify_priority_contract
from review_v2.primary_purpose import analyze as analyze_primary_purpose


@dataclass(frozen=True)
class DomainSelectionEvidence:
    signal_type: str
    signal: str
    target_family: str
    weight: int
    source_clause_ids: List[str]


@dataclass(frozen=True)
class DomainSelectionResolution:
    selected_contract_type: str
    document_domain: Dict[str, Any]
    compatibility: str
    resolution: str
    selected_domain: str
    rejected_domain: str
    confidence: str
    reasons: List[str]
    classification_evidence: List[DomainSelectionEvidence] = field(default_factory=list)
    classification_context: Dict[str, Any] = field(default_factory=dict)

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


_LEASE_SIGNALS: Tuple[Tuple[str, Tuple[str, ...], int], ...] = (
    ("lease_title", ("房屋租赁合同", "住宅租赁合同", "租赁合同"), 8),
    ("lease_parties", ("出租人", "承租人"), 5),
    ("rent_obligation", ("月租金", "租金支付", "支付租金"), 3),
    ("lease_term", ("租赁期限", "租期", "退租"), 3),
    ("lease_deposit", ("租赁押金", "押金退还", "退还押金"), 2),
)

_SALE_SIGNALS: Tuple[Tuple[str, Tuple[str, ...], int], ...] = (
    ("sale_title", ("买卖合同", "供货合同", "采购合同", "框架采购"), 8),
    ("sale_parties", ("出卖人", "买受人", "供方", "需方", "供应商", "采购方"), 5),
    ("framework_structure", ("长期供货", "采购订单", "框架协议", "分批供货"), 5),
    ("goods_identity", ("产品名称", "货物名称", "设备", "材料", "规格型号", "供货数量"), 4),
    ("goods_purchase_obligation", ("购买", "采购", "销售", "供货"), 4),
    ("goods_performance", ("交货地点", "交货期限", "交货", "货款", "支付货款", "验收合格", "对账结算"), 3),
)

_SERVICE_SIGNALS: Tuple[Tuple[str, Tuple[str, ...], int], ...] = (
    ("service_obligation", ("提供服务", "服务内容", "服务范围", "委托乙方服务", "乙方提供"), 5),
    ("service_fee", ("服务费", "服务费用", "咨询费", "技术服务费", "服务报酬"), 5),
    ("service_scope", ("工作范围", "服务项目", "服务清单", "服务标准"), 3),
    ("service_term", ("服务期限", "服务期间", "服务周期", "服务时间"), 2),
    ("service_acceptance", ("服务成果", "成果验收", "验收标准", "验收期限"), 2),
    ("service_title_hint", ("服务合同", "咨询服务", "技术服务"), 1),
)

_TECHNOLOGY_SUBTYPES = {
    "COOPERATIVE_DEVELOPMENT",
    "ENTRUSTED_DEVELOPMENT",
    "TECHNOLOGY_TRANSFER",
    "TECHNOLOGY_LICENSE",
    "TECHNICAL_CONSULTING",
    "TECHNICAL_SERVICE",
}


def consumer_service_context(text: str, technology_classification: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Classify consumer/prepaid service context independently from incidental service words."""
    compact = re.sub(r"\s+", "", text or "")
    technology = technology_classification or classify_technology_transaction(text)
    primary_type = str(technology.get("primary_contract_type") or "")
    technology_subtype = str(technology.get("primary_subtype") or "")
    technology_primary = (
        technology_subtype in _TECHNOLOGY_SUBTYPES
        and primary_type not in {"", "general_technology"}
    )
    training_signals = [term for term in ("培训", "课程", "课时", "授课", "学员", "上课") if term in compact]
    prepaid_signals = [term for term in ("预付费", "预付款", "会员卡", "储值", "充值", "课包", "剩余课时") if term in compact]
    consumer_signals = [term for term in ("消费者", "学员", "会员", "家长", "个人客户") if term in compact]
    training_economic_signals = [
        term for term in ("培训费", "课程费", "课时费", "课程包", "培训项目", "服务费")
        if term in compact
    ]
    consumer_training_structure = bool(
        consumer_signals
        or any(term in compact for term in ("课程", "课时", "授课", "上课", "培训中心"))
    )
    is_training_primary = bool(
        training_signals
        and training_economic_signals
        and consumer_training_structure
        and not technology_primary
    )
    is_prepaid_service = bool(
        prepaid_signals
        and consumer_training_structure
        and (training_signals or "服务" in compact)
        and not technology_primary
    )
    is_consumer_transaction = bool(
        consumer_signals
        and (training_signals or "服务" in compact)
        and not technology_primary
    )
    return {
        "is_consumer_transaction": is_consumer_transaction,
        "is_prepaid_service": is_prepaid_service,
        "is_training_primary_transaction": is_training_primary,
        "consumer_signals": consumer_signals,
        "prepaid_signals": prepaid_signals,
        "training_signals": training_signals,
        "gate_status": "APPLICABLE" if any((is_consumer_transaction, is_prepaid_service, is_training_primary)) else "NOT_APPLICABLE",
    }


def _family_for_contract_type(contract_type: str) -> str:
    value = (contract_type or "").strip().lower()
    if value in {"sale", "买卖合同"}:
        return "SALE"
    if value in {"lease", "house_lease", "房屋租赁合同"}:
        return "HOUSE_LEASE"
    if value in {"service", "服务合同"}:
        return "SERVICE"
    if value in {"technology", "技术合同"}:
        return "TECHNOLOGY"
    return value.upper()


def _collect_family_evidence(
    text: str,
    clauses: Sequence[ParsedClause],
    family: str,
    definitions: Sequence[Tuple[str, Tuple[str, ...], int]],
) -> tuple[int, List[DomainSelectionEvidence]]:
    from review_v2.transaction_scope import operative_text
    if family == 'SALE':
        text = operative_text(text)
    score = 0
    evidence: List[DomainSelectionEvidence] = []
    for signal_type, terms, weight in definitions:
        hits = [term for term in terms if term in text]
        if family == 'SALE' and hits:
            operative_hits = []
            for term in hits:
                valid = False
                for match in re.finditer(re.escape(term), text):
                    sentence = re.split(r'[。；\n]', text[:match.start()])[-1] + re.split(r'[。；\n]', text[match.end():])[0]
                    # A product named as an analysis object or expressly
                    # excluded performance is not a goods-sale undertaking.
                    if re.search(r'(?:不承担|不负责|不包含|不涉及)[^。；]{0,80}(?:采购|销售|供货|交货|设备|材料)', sentence):
                        continue
                    if re.search(r'(?:不得|禁止)[^。；]{0,45}(?:购买|采购|销售|供货|交货)', sentence):
                        continue
                    if re.search(r'(?:拟采购|设备|产品)[^。；]{0,35}(?:分析|评价|评估|论证|建议)', sentence) and not re.search(r'(?:应|须|负责)[^。；]{0,20}(?:采购|购买|销售|供货|交货)', sentence):
                        continue
                    if signal_type == 'goods_identity' and not re.search(r'(?:采购|购买|销售|供货|交货|价款|数量|规格型号)', sentence):
                        continue
                    valid = True
                    break
                if valid:
                    operative_hits.append(term)
            hits = operative_hits
        if signal_type.endswith('_title') or signal_type == 'service_title_hint':
            # An analysed contract type in a software feature list is not the
            # title of this transaction. Title signals must have title sources.
            title_rows = [c for c in clauses if getattr(c, 'block_type', '') in {'TITLE', 'HEADING'}
                          or (len(c.text.strip()) < 80 and c.text.strip().endswith(('合同', '协议')))]
            hits = [term for term in hits if any(term in c.text for c in title_rows)]
        if signal_type in {"lease_parties", "sale_parties"}:
            # Roles of third parties or substrings of 信息提供方 are not the
            # parties to this transaction. Require an actual party declaration.
            hits = [term for term in hits if re.search(
                rf'(?:^|[\n（(])\s*{re.escape(term)}\s*[：:（）()]|[甲乙丙丁]方(?:[（(:：]{{1,2}}|为|作为)\s*{re.escape(term)}', text)]
            distinct_roles = {term for term in hits}
            if len(distinct_roles) < 2:
                continue
        if not hits:
            continue
        source_ids = [clause.clause_id for clause in clauses if any(term in (operative_text(clause.text) if family == 'SALE' else clause.text) for term in hits)][:8]
        if signal_type.endswith('_title') or signal_type == 'service_title_hint':
            source_ids = [c.clause_id for c in title_rows if any(t in c.text for t in hits)][:8]
        evidence.append(DomainSelectionEvidence(signal_type, "、".join(hits[:3]), family, weight, source_ids))
        score += weight
    return score, evidence


def _technology_family_evidence(
    text: str,
    clauses: Sequence[ParsedClause],
    technology_classification: Dict[str, Any] | None = None,
) -> tuple[int, List[DomainSelectionEvidence], Dict[str, Any]]:
    classification = technology_classification or classify_technology_transaction(text)
    subtype = str(classification.get("primary_subtype") or "")
    confidence = str(classification.get("confidence") or "low")
    raw_score = int(classification.get("classification_score") or 0)
    primary_model = dict(classification.get("primary_transaction_model") or {})
    model_type = str(primary_model.get("type") or "")
    model_score = int(((primary_model.get("family_scores") or {}).get("TECHNOLOGY") or 0))
    model_proves_technology = model_type in {
        "TECHNOLOGY_LICENSE", "MIXED_SALE_TECHNOLOGY_LICENSE", "TECHNOLOGY_TRANSFER", "COOPERATIVE_DEVELOPMENT", "ENTRUSTED_DEVELOPMENT",
    }
    if (
        subtype not in _TECHNOLOGY_SUBTYPES
        or (confidence == "low" and not model_proves_technology)
    ):
        return 0, [], classification

    reasons = [str(value) for value in classification.get("classification_evidence") or []]
    if not reasons:
        reasons = [str(value) for value in classification.get("evidence_node_ids") or []]
    source_ids = [clause.clause_id for clause in clauses if any(
        term in clause.text
        for term in ("委托", "开发", "研发", "源代码", "API", "专利", "许可", "技术服务", "技术咨询")
    )][:12]
    if model_type == "GOODS_SALE":
        return 0, [], classification
    score = max(6, raw_score, model_score)
    evidence = [DomainSelectionEvidence(
        signal_type=f"technology_{subtype.lower()}",
        signal="、".join(reasons[:8]) or subtype,
        target_family="TECHNOLOGY",
        weight=score,
        source_clause_ids=source_ids,
    )]
    return score, evidence, classification


def _classify_document_family(
    text: str,
    clauses: Sequence[ParsedClause],
    technology_classification: Dict[str, Any] | None = None,
) -> tuple[str, str, List[DomainSelectionEvidence], Dict[str, int], Dict[str, Any]]:
    lease_score, lease_evidence = _collect_family_evidence(text, clauses, "HOUSE_LEASE", _LEASE_SIGNALS)
    sale_score, sale_evidence = _collect_family_evidence(text, clauses, "SALE", _SALE_SIGNALS)
    service_score, service_evidence = _collect_family_evidence(text, clauses, "SERVICE", _SERVICE_SIGNALS)
    technology_score, technology_evidence, technology_classification = _technology_family_evidence(
        text,
        clauses,
        technology_classification,
    )
    scores = {
        "SALE": sale_score,
        "HOUSE_LEASE": lease_score,
        "SERVICE": service_score,
        "TECHNOLOGY": technology_score,
    }
    winner = max(scores, key=lambda key: scores[key])
    winner_score = scores[winner]
    runner_up = max((score for key, score in scores.items() if key != winner), default=0)
    margin = winner_score - runner_up
    evidence_by_family = {
        "SALE": sale_evidence,
        "HOUSE_LEASE": lease_evidence,
        "SERVICE": service_evidence,
        "TECHNOLOGY": technology_evidence,
    }
    winner_evidence = evidence_by_family[winner]
    if winner == "TECHNOLOGY" and technology_classification.get("confidence") == "high" and margin >= 4:
        confidence = "high"
    elif winner_score >= 8 and margin >= 4 and len(winner_evidence) >= 2:
        confidence = "high"
    elif winner_score >= 5 and margin >= 2:
        confidence = "medium"
    else:
        return "UNCERTAIN", "low", lease_evidence + sale_evidence + service_evidence + technology_evidence, scores, technology_classification
    return winner, confidence, lease_evidence + sale_evidence + service_evidence + technology_evidence, scores, technology_classification


def resolve_domain_selection(
    selected_contract_type: str,
    text: str,
    clauses: Sequence[ParsedClause],
    technology_classification: Dict[str, Any] | None = None,
) -> tuple[DomainSelectionResolution, DomainResolution, str]:
    """Return the public resolution, detailed document domain, and routed registry type."""
    selected_family = _family_for_contract_type(selected_contract_type)
    document_family, confidence, evidence, scores, technology_classification = _classify_document_family(
        text,
        clauses,
        technology_classification,
    )

    # A commissioned physical result is not a goods sale merely because its
    # contract also specifies products, prices, delivery and acceptance.
    compact = re.sub(r"\s+", "", text or "")
    work_roles = bool(re.search(r"承揽[人方]", compact) and re.search(r"定[作做人][人方]?", compact))
    work_performance = bool(re.search(r"委托.{0,30}(?:加工|制作|修理)|按照.{0,55}(?:图纸|样品).{0,35}(?:加工|制作|生产)", compact))
    work_primary = work_roles and work_performance
    priority = classify_priority_contract(text, clauses)
    if work_primary:
        document_family, confidence = "WORK_CONTRACT", "high"
        scores[document_family] = 30
        evidence.append(DomainSelectionEvidence("commissioned_result", "承揽人与定作人之间按要求加工交付特定成果", document_family, 30,
            [c.clause_id for c in clauses if re.search(r"承揽[人方]|定作[人方]|加工成品", c.text)][:8]))
    elif priority:
        priority_type, confidence, signal = priority
        document_family = priority_type.upper()
        scores[document_family] = 30
        evidence.append(DomainSelectionEvidence("primary_transaction", signal, document_family, 30,
            [c.clause_id for c in clauses if any(t in c.text for t in PRIORITY_TYPES[priority_type].titles) or any(t in c.text for t in PRIORITY_TYPES[priority_type].signals)][:8]))
    elif selected_contract_type in PRIORITY_TYPES:
        # An unsupported weak alternative cannot displace an explicit new type.
        if confidence != "high":
            document_family = "UNCERTAIN"

    purpose = analyze_primary_purpose(text, clauses)
    # A broad labor-purpose score cannot erase a positively identified labor
    # subtype. It refines other transactions, but is the parent of these leaves.
    labor_subtype = bool(priority and PRIORITY_TYPES[priority[0]].family == 'EMPLOYMENT'
                         and PRIORITY_TYPES[priority[0]].subject == 'LABOR')
    equity_primary = bool(priority and PRIORITY_TYPES[priority[0]].family == 'EQUITY_INVESTMENT')
    # A rights/consideration transaction model is stronger evidence than the
    # broad purpose classifier's buyer/seller, delivery and price vocabulary.
    # Licensees/transferees are often called buyers without buying goods. This
    # protection requires a high-confidence operative model, not a title or
    # the user's selected family.
    technology_model = technology_classification.get('primary_transaction_model') or {}
    technical_rights_primary = (
        document_family == 'TECHNOLOGY' and confidence == 'high'
        and technology_model.get('dominant_family') == 'TECHNOLOGY'
        and technology_model.get('confidence') == 'high'
    )
    technical_consulting_primary = (
        document_family == 'TECHNOLOGY'
        and technology_classification.get('primary_subtype') == 'TECHNICAL_CONSULTING'
        and technology_classification.get('confidence') == 'high'
        and 'boundary:no_direct_implementation' in (technology_classification.get('classification_evidence') or [])
    )
    generic_sale_displaced = (technical_rights_primary or technical_consulting_primary) and purpose['primary_family'] == 'SALE'
    generic_service_displaced = technical_consulting_primary and purpose['primary_family'] == 'SERVICE'
    if purpose['primary_family'] and not generic_sale_displaced and not generic_service_displaced and not (priority and priority[0]=='operating_cooperation') and not equity_primary and not (labor_subtype and purpose['primary_family'] == 'LABOR'):
        document_family, confidence = purpose['primary_family'], purpose['confidence']
        scores.update(purpose['scores'])
        evidence.extend(DomainSelectionEvidence(**row) for row in purpose['classification_evidence'])
    from review_v2.carriage_scope import analyze as carriage_scope
    carriage = carriage_scope(text)
    if carriage['established'] and not priority and not work_primary:
        document_family, confidence = 'TRANSPORTATION', 'high'
    # Once the full-document verifier establishes employment form, the
    # legacy text classifier cannot replace that fact with a different family.
    from review_v2.employment_fact_store import current as employment_store
    verified_employment = employment_store()
    if selected_contract_type == 'labor' and verified_employment is not None and getattr(verified_employment, 'is_verified', False):
        form_facts = verified_employment.get('contract.employment_form', positive=False)
        if form_facts and all(f['assertion'] == 'EXPLICIT' and f['confidence'] >= .75 for f in form_facts):
            document_family, confidence = 'LABOR', 'high'
            scores[document_family] = 30
            evidence.append(DomainSelectionEvidence('verified_employment_form',
                '全文已验证的劳动用工关系', document_family, 30,
                sorted({e['clause_id'] for f in form_facts for e in f['evidence']})))
    comparable = selected_family in {"SALE", "HOUSE_LEASE", "SERVICE", "TECHNOLOGY"} or selected_contract_type in PRIORITY_TYPES or bool(priority) or work_primary or bool(purpose['primary_family']) or carriage['established']
    if document_family == "UNCERTAIN" or not comparable:
        routed_family = selected_family
        resolution = "USER_SELECTION_ACCEPTED"
        compatibility = "UNCERTAIN" if comparable else "NOT_COMPARABLE"
        rejected = ""
    elif document_family == selected_family:
        routed_family = selected_family
        resolution = "AGREE"
        compatibility = "COMPATIBLE"
        rejected = ""
    elif confidence == "high":
        routed_family = document_family
        resolution = "DOCUMENT_OVERRIDE"
        compatibility = "CONFLICT"
        rejected = selected_family
    else:
        routed_family = selected_family
        resolution = "UNCERTAIN_CONFLICT"
        compatibility = "CONFLICT"
        rejected = document_family

    family_types = {"SALE": "sale", "HOUSE_LEASE": "house_lease", "SERVICE": "service", "TECHNOLOGY": "technology", "WORK_CONTRACT": "work_contract", "GUARANTEE": "guarantee"}
    family_types.update({key.upper(): key for key in PRIORITY_TYPES})
    family_types['TRANSPORTATION'] = 'transportation'
    routed_type = family_types.get(routed_family, selected_contract_type)
    document_type = family_types.get(document_family, routed_type)
    document_domain = resolve_contract_domain(
        document_type,
        text,
        clauses,
        technology_classification=technology_classification if document_type == "technology" else None,
    )
    reasons = [
        "document family scores: " + ", ".join(f"{family}={score}" for family, score in scores.items()),
        f"document family={document_family}, confidence={confidence}",
    ]
    # Candidate classification remains diagnostic. Only the accepted route may
    # supply execution context, including when a non-comparable type is retained.
    routed_technology = technology_classification if routed_family == "TECHNOLOGY" else {}
    primary_transaction = dict(routed_technology.get("primary_transaction") or {}) if routed_family == "TECHNOLOGY" else {"type": routed_type}
    primary_transaction_model = dict(routed_technology.get("primary_transaction_model") or {})
    ancillary_obligations = list(routed_technology.get("ancillary_obligations") or [])
    post_delivery_obligations = [
        obligation for obligation in ancillary_obligations
        if obligation in {"TRAINING", "TECHNICAL_SUPPORT", "TECHNICAL_GUIDANCE", "INSTALLATION_AND_COMMISSIONING"}
    ]
    consumer_context = consumer_service_context(text, routed_technology)
    classification_context = {
        'effect_review_ids': [c.item_id for c in __import__('review_v2.contract_effects',fromlist=['active']).active(text)],
        'property_service_structure': __import__('review_v2.service_scenarios',fromlist=['is_property_service']).is_property_service(text),
        'business_overlays': __import__('review_v2.business_overlays',fromlist=['active']).active(text),
        'overlay_review_ids': [c.item_id for c in __import__('review_v2.business_overlays',fromlist=['checkpoints']).checkpoints(text)],
        'settlement_formulas': __import__('review_v2.settlement_formula',fromlist=['analyze']).analyze(text),
        'carriage_scope': carriage,
        'operating_structure': __import__('review_v2.operating_cooperation',fromlist=['structure']).structure(text),
        'incomplete_obligations': __import__('review_v2.clause_completeness',fromlist=['fragments']).fragments(text),
        'business_domain_tags': ['DANGEROUS_GOODS_TRANSPORT'] if routed_type=='operating_cooperation' and '危险品' in text else [],
        'primary_contract_type': routed_family,
        'contract_type_confidence': confidence,
        'secondary_clause_features': purpose['secondary_clause_features'],
        'suppressed_primary_purpose_candidate': (
            {'family': 'SALE', 'scores': purpose['scores'],
             'reason': 'Operative technology rights and consideration outweigh generic goods vocabulary.'}
            if generic_sale_displaced else
            {'family': 'SERVICE', 'scores': purpose['scores'],
             'reason': 'Verified consulting performance and express exclusion of implementation displace generic service vocabulary.'}
            if generic_service_displaced else None
        ),
        'guarantee_features_detected': purpose['guarantee_features_detected'],
        'nda_primary_features_detected': purpose['nda_primary_features_detected'],
        'classification_conflict': {'detected': resolution in {'DOCUMENT_OVERRIDE','UNCERTAIN_CONFLICT'},
            'selected': selected_family, 'document': document_family,
            'resolved': resolution != 'UNCERTAIN_CONFLICT'},
        "primary_transaction": primary_transaction,
        "primary_transaction_model": primary_transaction_model,
        "secondary_transactions": list(routed_technology.get("secondary_transactions") or []),
        "ancillary_obligations": ancillary_obligations,
        "post_delivery_obligations": post_delivery_obligations,
        "consumer_service_context": consumer_context,
        "candidate_scores": scores,
        "technology_candidate_scores": dict(technology_classification.get("candidate_scores") or {}),
        "primary_transaction_reason": (
            "New technical result creation and development-performance facts control; training/support are ancillary obligations."
            if routed_family == "TECHNOLOGY" and str(routed_technology.get("primary_contract_type") or "") in {"commissioned_development", "cooperative_development"}
            else "Operative rights change, primary obligations, consideration and economic independence control before Review Registry loading."
        ),
    }
    if resolution == "DOCUMENT_OVERRIDE":
        reasons.append("High-confidence document evidence overrides the incompatible user selection before Review Registry loading.")
    elif resolution == "UNCERTAIN_CONFLICT":
        reasons.append("Conflicting document evidence is not strong enough for an automatic override.")
    else:
        reasons.append("The user selection remains a compatible or uncontested routing prior.")
    public_document = document_domain.to_public_dict()
    public_document["family"] = document_family
    public_document["classification_confidence"] = confidence
    public_document["classification_scores"] = scores
    public_document["primary_contract_type"] = technology_classification.get("primary_contract_type") if document_family == "TECHNOLOGY" else document_type
    public_document["primary_subtype"] = technology_classification.get("primary_subtype") if document_family == "TECHNOLOGY" else document_domain.contract_subtype
    public_document["primary_transaction_model"] = primary_transaction_model
    resolution_result = DomainSelectionResolution(
        selected_contract_type=selected_contract_type,
        document_domain=public_document,
        compatibility=compatibility,
        resolution=resolution,
        selected_domain=routed_family,
        rejected_domain=rejected,
        confidence=confidence,
        reasons=reasons,
        classification_evidence=evidence,
        classification_context=classification_context,
    )
    routed_domain = resolve_contract_domain(
        routed_type,
        text,
        clauses,
        technology_classification=technology_classification if routed_type == "technology" else None,
    )
    return resolution_result, routed_domain, routed_type


def domain_selection_consistency_gate(
    resolution: DomainSelectionResolution,
    review_ids: Sequence[str],
    perspective: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    resolved = resolution.selected_domain
    if resolved.lower() in PRIORITY_TYPES or resolved == 'GUARANTEE':
        from review_v2.contract_registry import get_checklist_for_resolution
        from types import SimpleNamespace
        # Validate against the same resolved scenario used by execution.
        domain = SimpleNamespace(**resolution.document_domain)
        allowed = {row.item_id for row in get_checklist_for_resolution(resolved.lower(), domain)}
        from review_v2.penalty_base import CHECKPOINT as common_penalty_checkpoint
        allowed.add(common_penalty_checkpoint.item_id)
        from review_v2.contract_references import CHECKPOINTS as reference_checkpoints
        allowed.update(c.item_id for c in reference_checkpoints)
        from review_v2.clause_completeness import CHECKPOINT as completeness_checkpoint
        allowed.add(completeness_checkpoint.item_id)
        allowed.update(resolution.classification_context.get('overlay_review_ids',[]))
        allowed.update(resolution.classification_context.get('effect_review_ids',[]))
        from review_v2.settlement_formula import CHECKPOINT as formula_checkpoint
        if resolution.classification_context.get('settlement_formulas'):
            allowed.add(formula_checkpoint.item_id)
        wrong_ids = [item_id for item_id in review_ids if item_id not in allowed]
    elif resolved == "SALE":
        wrong_ids = [item_id for item_id in review_ids if item_id.startswith(("HL-", "SVC-"))]
    elif resolved == "HOUSE_LEASE":
        wrong_ids = [item_id for item_id in review_ids if item_id.startswith(("S-", "FS-", "RE-", "SVC-"))]
    elif resolved == "SERVICE":
        wrong_ids = [item_id for item_id in review_ids if item_id.startswith(("S-", "FS-", "RE-", "HL-"))]
    elif resolved == "TECHNOLOGY":
        mixed_sale_license = str(
            ((resolution.classification_context.get("primary_transaction_model") or {}).get("type") or "")
        ) == "MIXED_SALE_TECHNOLOGY_LICENSE"
        forbidden_prefixes = ("FS-", "RE-", "HL-", "SVC-") if mixed_sale_license else ("S-", "FS-", "RE-", "HL-", "SVC-")
        wrong_ids = [item_id for item_id in review_ids if item_id.startswith(forbidden_prefixes)]
    else:
        wrong_ids = []
    failures: List[Dict[str, str]] = []
    if not set(resolution.classification_context.get('effect_review_ids',[])).issubset(review_ids):
        failures.append({'requirement':'UNREVIEWED_ADVERSE_LEGAL_EFFECT','root_cause':'Source waiver, exit imbalance or dispute conflict omitted','current_status':'FAIL'})
    if resolution.classification_context.get('property_service_structure') and resolution.document_domain.get('contract_subtype') != 'PROPERTY_SERVICE':
        failures.append({'requirement':'PROPERTY_SERVICE_SUBTYPE_LOST','root_cause':'Property obligations were reduced to generic service','current_status':'FAIL'})
    expected=set(resolution.classification_context.get('overlay_review_ids',[]))
    if not expected.issubset(review_ids):
        failures.append({'requirement':'BUSINESS_OVERLAY_OMITTED','root_cause':'Identified regulated business has missing verification reviews','current_status':'FAIL'})
    if resolution.classification_context.get('settlement_formulas') and 'COMMON-23-01' not in review_ids:
        failures.append({'requirement':'SETTLEMENT_FORMULA_NOT_REVIEWED','root_cause':'Settlement expression omitted','current_status':'FAIL'})
    if resolution.classification_context.get('operating_structure',{}).get('established') and resolved != 'OPERATING_COOPERATION':
        failures.append({'requirement':'BODY_PRIMARY_TRANSACTION_CONFLICT','root_cause':'Operating delegation facts conflict with the selected review family','current_status':'FAIL'})
    from review_v2.clause_completeness import CHECKPOINT as completeness_checkpoint
    if resolution.classification_context.get('incomplete_obligations') and completeness_checkpoint.item_id not in review_ids:
        failures.append({'requirement':'UNREVIEWED_INCOMPLETE_OBLIGATION','root_cause':'Incomplete operative clause not reviewed','current_status':'FAIL'})
    primary = resolution.classification_context.get('primary_contract_type')
    if primary and primary != resolved:
        failures.append({'requirement':'PRIMARY_TRANSACTION_ROUTE_CONFLICT','failure_stage':'Domain Selection',
            'root_cause':f'Primary transaction {primary} differs from routed domain {resolved}',
            'responsible_function':'resolve_domain_selection','current_status':'FAIL'})
    if resolution.resolution == "UNCERTAIN_CONFLICT":
        failures.append({
            "requirement": "DOMAIN_SELECTION_CONSISTENCY_GATE",
            "failure_stage": "Domain Selection",
            "root_cause": "User selection conflicts with document classification without enough confidence for automatic override.",
            "responsible_function": "resolve_domain_selection",
            "current_status": "FAIL",
        })
    if wrong_ids:
        failures.append({
            "requirement": "DOMAIN_SELECTION_CONSISTENCY_GATE",
            "failure_stage": "Review Registry",
            "root_cause": f"Resolved domain {resolved} loaded incompatible reviews: {', '.join(wrong_ids)}",
            "responsible_function": "get_checklist_for_resolution",
            "current_status": "FAIL",
        })
    primary_type = str(((resolution.classification_context.get("primary_transaction") or {}).get("type") or ""))
    role = str((perspective or {}).get("canonical_role") or "")
    if resolved == "TECHNOLOGY" and primary_type == "commissioned_development" and role and role not in {
        "COMMISSIONING_PARTY", "DEVELOPMENT_CONTRACTOR", "ENTRUSTED_DEVELOPMENT_PARTY",
    }:
        failures.append({
            "requirement": "PRIMARY_ROLE_CONSISTENCY_GATE",
            "failure_stage": "Perspective Resolution",
            "root_cause": f"Primary commissioned-development transaction is incompatible with role {role}.",
            "responsible_function": "resolve_perspective",
            "current_status": "FAIL",
        })
    return {
        "status": "BLOCKED" if failures else "REPORT_READY",
        "gate": "DOMAIN_SELECTION_CONSISTENCY_GATE",
        "gate_status": "FAIL" if failures else "PASS",
        "wrong_domain_review_count": len(wrong_ids),
        "wrong_domain_review_ids": wrong_ids,
        "failures": failures,
    }
