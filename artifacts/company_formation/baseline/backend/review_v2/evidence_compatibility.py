"""Explicit semantic domains: related subject matter does not establish support.

Bindings with a declared requirement domain must have a matching source domain.
Reclassify the actual quote in the gate instead of trusting a caller's label.
"""
import re

QUALITY_SUBJECT = r"(?:电压|频率|供电可靠性|电能质量|供电质量|供应质量|水质|水压|气压|燃气质量|供热质量|供热温度|热力质量)"
QUALITY_ACTION = r"(?:检测|监测|测量|测温|记录|检验|报告)"
QUALITY_PATTERN = rf"(?:{QUALITY_SUBJECT}[^，,。；\n]{{0,45}}{QUALITY_ACTION}|{QUALITY_ACTION}[^，,。；\n]{{0,45}}{QUALITY_SUBJECT})"
DOMAIN_PATTERNS = {
    "supply_quality_measurement": QUALITY_PATTERN,
    "billing_measurement": r"电能表|计量装置|抄表|计量误差|用电量|电费结算|计费数据",
    "payment_receipt": r"付款凭证|支付凭证|汇款回单|银行回单",
    "acceptance_evidence": r"验收报告|验收单|验收记录|验收确认",
    "ownership_proof": r"权属证书|产权证|专利证书|登记簿副本",
    "quality_proof": r"质量检验报告|质量检测报告|质量合格证",
    "notice_obligation": r"应[^。；\n]{0,20}通知|须[^。；\n]{0,20}通知",
    "notice_record": r"通知送达回执|已送达[^。；\n]{0,20}通知|通知记录",
    "liability": r"违约责任|赔偿责任|承担赔偿|违约金",
    "performance_obligation": r"应[^。；\n]{0,15}(?:交付|提供|完成|履行)",
    "attachment_entity": r"附件[一二三四五六七八九十\d]*[：:]|附件清单",
}


def evidence_domains(text):
    return {domain for domain, pattern in DOMAIN_PATTERNS.items() if re.search(pattern, text)}


def evidence_compatible(text, required_domain):
    return not required_domain or required_domain in evidence_domains(text)


def evidence_compatibility_failures(items):
    failures = []
    for item in items:
        get = item.get if isinstance(item, dict) else lambda k, d=None: getattr(item, k, d)
        elements = {e["element_id"]: e for e in get("coverage_elements", []) or []}
        trace = get("decision_trace", {}) or {}
        declared = trace.get("required_evidence_domains", {})
        for evidence in get("evidence_clauses", []) or []:
            for key in evidence.get("supported_elements", []):
                domain = declared.get(key) or elements.get(key, {}).get("required_evidence_domain")
                if domain and not evidence_compatible(evidence.get("quote") or evidence.get("text", ""), domain):
                    failures.append(dict(requirement="EVIDENCE_TYPE_COMPATIBILITY", current_status="FAIL",
                                         root_cause="引文无法证明目标证据域，主题相关不等于要素覆盖。",
                                         source_rules=[get("item_id")], element_id=key, evidence_id=evidence.get("evidence_id")))
    return failures
