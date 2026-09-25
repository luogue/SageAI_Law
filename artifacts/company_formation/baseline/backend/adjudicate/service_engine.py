"""Service-contract adjudication engine."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from adjudicate.engine_v2 import _format_output, _mentions, _parse_date, _years_between
from adjudicate.service_configs import get_service_config


@dataclass
class ServiceFacts:
    raw_text: str
    contract_type: str = "service"
    contract_type_name: str = "服务合同"
    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    service_contract: bool = False
    contract_date: Optional[date] = None
    third_party_tort: bool = False
    nature_dispute: bool = False
    service_process: bool = False
    work_result: bool = False
    entrusted_affair: bool = False
    contract_invalid: bool = False
    fraud_or_coercion: bool = False
    prepaid_consumption: bool = False
    consumer: bool = False
    operator_closed: bool = False
    malicious_refund_evasion: bool = False
    prepaid_amount: float = 0.0
    service_full_provided: bool = False
    service_not_provided: bool = False
    service_partly_provided: bool = False
    unused_amount: float = 0.0
    provider_unilateral_change: bool = False
    accepted_change: bool = False
    health_change: bool = False
    medical_advice: bool = False
    unforeseeable: bool = False
    unfair_to_continue: bool = False
    format_no_refund: bool = False
    format_clause: bool = False
    service_quality_dispute: bool = False
    quality_standard_agreed: bool = False
    industry_standard: bool = False
    quality_conform: bool = False
    quality_nonconform: bool = False
    provider_no_qualification: bool = False
    staff_mismatch: bool = False
    service_receiver_fault: bool = False
    reasonable_loss: float = 0.0
    indefinite_service: bool = False
    reasonable_notice: bool = False
    platform_terms_change: bool = False
    major_rights_change: bool = False
    prompt_explain: bool = False
    user_consent: bool = False
    business_transfer: bool = False
    transfer_notified: bool = False
    transferee_refuses_service: bool = False
    guaranteed_result: bool = False
    goal_not_achieved: bool = False
    receiver_fault_goal: bool = False
    force_majeure: bool = False
    termination_request: bool = False
    actual_loss: float = 0.0
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "service_contract": self.service_contract,
            "contract_date": self.contract_date.isoformat() if self.contract_date else None,
            "third_party_tort": self.third_party_tort,
            "nature_dispute": self.nature_dispute,
            "service_process": self.service_process,
            "work_result": self.work_result,
            "entrusted_affair": self.entrusted_affair,
            "contract_invalid": self.contract_invalid,
            "fraud_or_coercion": self.fraud_or_coercion,
            "prepaid_consumption": self.prepaid_consumption,
            "consumer": self.consumer,
            "operator_closed": self.operator_closed,
            "malicious_refund_evasion": self.malicious_refund_evasion,
            "prepaid_amount": self.prepaid_amount,
            "service_full_provided": self.service_full_provided,
            "service_not_provided": self.service_not_provided,
            "service_partly_provided": self.service_partly_provided,
            "unused_amount": self.unused_amount,
            "provider_unilateral_change": self.provider_unilateral_change,
            "accepted_change": self.accepted_change,
            "health_change": self.health_change,
            "medical_advice": self.medical_advice,
            "unforeseeable": self.unforeseeable,
            "unfair_to_continue": self.unfair_to_continue,
            "format_no_refund": self.format_no_refund,
            "format_clause": self.format_clause,
            "service_quality_dispute": self.service_quality_dispute,
            "quality_standard_agreed": self.quality_standard_agreed,
            "industry_standard": self.industry_standard,
            "quality_conform": self.quality_conform,
            "quality_nonconform": self.quality_nonconform,
            "provider_no_qualification": self.provider_no_qualification,
            "staff_mismatch": self.staff_mismatch,
            "service_receiver_fault": self.service_receiver_fault,
            "reasonable_loss": self.reasonable_loss,
            "indefinite_service": self.indefinite_service,
            "reasonable_notice": self.reasonable_notice,
            "platform_terms_change": self.platform_terms_change,
            "major_rights_change": self.major_rights_change,
            "prompt_explain": self.prompt_explain,
            "user_consent": self.user_consent,
            "business_transfer": self.business_transfer,
            "transfer_notified": self.transfer_notified,
            "transferee_refuses_service": self.transferee_refuses_service,
            "guaranteed_result": self.guaranteed_result,
            "goal_not_achieved": self.goal_not_achieved,
            "receiver_fault_goal": self.receiver_fault_goal,
            "force_majeure": self.force_majeure,
            "termination_request": self.termination_request,
            "actual_loss": self.actual_loss,
            "notes": self.notes,
        }


def _format_service_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: ServiceFacts,
    path: List[str],
    procedure_findings: Optional[List[str]] = None,
) -> Dict[str, Any]:
    return _format_output(
        major=major,
        minor=minor,
        conclusion=conclusion,
        triggered_items=triggered_items,
        facts=facts,
        path=path,
        procedure_findings=procedure_findings,
        footer_label="触发补丁清单",
    )


def _money(value: float) -> str:
    return f"{value:.2f} 元" if value > 0 else "待核定"


def _extract_money_near(text: str, labels: tuple[str, ...]) -> float:
    money_pattern = r"(\d+(?:\.\d+)?)\s*(万|万元|元|块|人民币)?"

    def normalize(match: re.Match[str]) -> float:
        value = float(match.group(1))
        unit = match.group(2) or ""
        if unit in {"万", "万元"}:
            value *= 10000
        return value

    for label in labels:
        for match in re.finditer(re.escape(label), text):
            after = text[match.end():min(len(text), match.end() + 18)]
            after_match = re.search(money_pattern, after)
            if after_match:
                value = normalize(after_match)
                if value > 0:
                    return value
            before = text[max(0, match.start() - 12):match.start()]
            before_matches = list(re.finditer(money_pattern, before))
            if before_matches:
                value = normalize(before_matches[-1])
                if value > 0:
                    return value
    return 0.0


def extract_service_facts(case_text: str) -> ServiceFacts:
    config = get_service_config()
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = ServiceFacts(raw_text=raw_text)

    for field_name in (
        "service_contract", "third_party_tort", "nature_dispute", "service_process",
        "work_result", "entrusted_affair", "contract_invalid", "fraud_or_coercion",
        "prepaid_consumption", "consumer", "operator_closed", "malicious_refund_evasion",
        "service_full_provided", "service_not_provided", "service_partly_provided",
        "provider_unilateral_change", "accepted_change", "health_change", "medical_advice",
        "unforeseeable", "unfair_to_continue", "format_no_refund", "format_clause",
        "service_quality_dispute", "quality_standard_agreed", "industry_standard",
        "quality_conform", "quality_nonconform", "provider_no_qualification", "staff_mismatch",
        "service_receiver_fault", "indefinite_service", "reasonable_notice",
        "platform_terms_change", "major_rights_change", "prompt_explain", "user_consent",
        "business_transfer", "transfer_notified", "transferee_refuses_service",
        "guaranteed_result", "goal_not_achieved", "receiver_fault_goal", "force_majeure",
        "termination_request",
    ):
        setattr(facts, field_name, _mentions(text, config.get_terms(field_name)))

    facts.asks_jurisdiction = _mentions(text, config.get_terms("jurisdiction_question")) or (
        ("起诉" in text or "法院" in text) and any(word in text for word in ("哪里", "去哪", "哪个", "管辖", "地点"))
    )
    facts.asks_defendant = _mentions(text, config.get_terms("defendant_question"))
    facts.contract_date = _parse_date(text, config.get_terms("contract_date"))
    facts.prepaid_amount = _extract_money_near(text, config.get_terms("prepaid_amount"))
    facts.unused_amount = _extract_money_near(text, config.get_terms("unused_amount"))
    facts.reasonable_loss = _extract_money_near(text, config.get_terms("reasonable_loss"))
    facts.actual_loss = _extract_money_near(text, config.get_terms("actual_loss"))

    if facts.format_no_refund:
        facts.format_clause = True
    if facts.prepaid_consumption or facts.operator_closed or facts.service_partly_provided:
        facts.service_contract = True
    return facts


def _procedure_findings(facts: ServiceFacts) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append("服务合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理")
    if facts.asks_defendant:
        findings.append("适格被告通常为服务提供方或服务接受方；预付式消费经营业务转让的，可结合转让方、受让方履行情况确定责任主体")
    return findings


def _only_procedure_question(facts: ServiceFacts) -> bool:
    substantive = any(
        (
            facts.nature_dispute, facts.work_result, facts.entrusted_affair, facts.contract_invalid,
            facts.prepaid_consumption, facts.operator_closed, facts.format_no_refund,
            facts.service_quality_dispute, facts.quality_nonconform, facts.provider_unilateral_change,
            facts.provider_no_qualification, facts.staff_mismatch, facts.health_change,
            facts.indefinite_service, facts.platform_terms_change, facts.business_transfer,
            facts.guaranteed_result, facts.termination_request,
        )
    )
    return (facts.asks_jurisdiction or facts.asks_defendant) and not substantive


def adjudicate_service(case_text: str, today: Optional[date] = None) -> Dict[str, Any]:
    config = get_service_config()
    facts = extract_service_facts(case_text)
    today = today or date.today()
    triggered: List[str] = []
    path: List[str] = ["入口程序校验"]
    procedure_findings = _procedure_findings(facts)

    if _only_procedure_question(facts):
        major = "服务合同纠纷的程序事项应先确认管辖法院和适格被告。"
        minor = "用户提出的是起诉地点或被告确定问题，未提出服务是否提供、服务质量、预付款退款、合同解除或格式条款争议事实。"
        conclusion = "；".join(procedure_findings)
        return _format_service_output(major, minor, conclusion, ["管辖程序"] if procedure_findings else [], facts, path, procedure_findings)

    if facts.contract_date and _years_between(facts.contract_date, today) > 3:
        major = "服务合同纠纷适用三年一般诉讼时效。"
        minor = f"识别到相关服务开始、付款、停业或应履行日期为{facts.contract_date.isoformat()}，截至{today.isoformat()}已经超过三年。"
        conclusion = "诉讼时效已过，驳回请求。"
        return _format_service_output(major, minor, conclusion, [], facts, [*path, "诉讼时效"], procedure_findings)

    if facts.third_party_tort and not facts.service_contract:
        major = "服务合同裁判引擎处理服务提供方与服务接受方之间围绕服务履行、服务质量、服务费用和解除退款产生的合同争议；单纯合同外第三人侵权应按侵权责任处理。"
        minor = "识别到争议核心是合同外第三人侵权，未识别到服务合同履行争议。"
        conclusion = "本案涉及侵权责任，非服务合同纠纷，不适用本服务合同裁判引擎。"
        return _format_service_output(major, minor, conclusion, [], facts, path, procedure_findings)

    path.append("前置实体判断")
    if facts.nature_dispute or facts.work_result or facts.entrusted_affair:
        triggered.append(config.patch_name("SVC1", "服务合同性质认定"))
        major = "服务合同属于无名合同，应适用合同编通则，并按合同实质确定性质：核心为提供服务行为的，认定为服务合同；核心为完成工作并交付成果的，认定为承揽合同；核心为按指示处理事务的，认定为委托合同。"
        if facts.service_process and not (facts.work_result or facts.entrusted_affair):
            minor = "识别到合同核心是提供服务行为，接受方重在接受服务过程。"
            conclusion = "合同性质认定为服务合同，适用服务合同裁判规则。"
        elif facts.work_result:
            minor = "识别到合同核心是完成特定工作并交付成果。"
            conclusion = "合同性质认定为承揽合同，适用承揽合同裁判规则。"
        else:
            minor = "识别到合同核心是处理事务并按委托人指示行事。"
            conclusion = "合同性质认定为委托合同，适用委托合同裁判规则。"
        return _format_service_output(major, minor, conclusion, triggered, facts, [*path, "合同性质认定"], procedure_findings)

    if facts.contract_invalid or facts.fraud_or_coercion:
        major = "服务合同违反法律、行政法规强制性规定，或存在欺诈、胁迫等影响真实意思表示的情形，应按合同无效、撤销或违约责任规则处理。"
        minor = "识别到合同效力争议，可能存在违法无效、欺诈、胁迫或虚假宣传。"
        conclusion = "合同无效或被撤销后，服务方应返还取得的服务费；有过错的一方赔偿对方因此受到的损失。"
        return _format_service_output(major, minor, conclusion, [], facts, [*path, "合同效力审查"], procedure_findings)

    if facts.format_no_refund:
        triggered.append(config.patch_name("SVC4", "不退不换格式条款效力"))
        major = "《民法典》第496条、第497条规定，格式条款不得不合理免除或者减轻提供方责任、加重对方责任、限制对方主要权利。服务合同中的不退不换、概不退款条款如排除消费者依法退款权利，应认定无效。"
        minor = "识别到服务合同中存在不退不换、概不退款或费用不退的格式条款。"
        conclusion = "‘不退不换’格式条款无效，消费者可以依法主张退款。"
        return _format_service_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查"], procedure_findings)

    if facts.platform_terms_change:
        triggered.append(config.patch_name("SVC11", "互联网平台服务条款变更"))
        major = "互联网平台单方变更服务条款，应遵循诚信原则并尽到合理提示说明义务；涉及用户重大权益的变更，应取得用户同意。"
        minor = "识别到互联网平台单方变更服务条款或用户协议。"
        if facts.major_rights_change and not (facts.prompt_explain and facts.user_consent):
            conclusion = "平台服务条款变更无效，对用户不发生效力。"
        else:
            conclusion = "平台已提示说明且用户明确同意，或变更未涉及重大权益的，平台服务条款变更对用户发生效力。"
        return _format_service_output(major, minor, conclusion, triggered, facts, [*path, "服务内容与标准确定"], procedure_findings)

    if facts.business_transfer:
        triggered.append(config.patch_name("SVC12", "预付式消费合同转让责任"))
        major = "预付式消费经营业务转让后，受让方应继续履行服务合同；转让方未告知消费者或受让方不继续履行的，消费者可以依法向相关责任主体主张权利。"
        minor = "识别到服务提供方将经营业务转让给第三方。"
        if facts.transferee_refuses_service:
            conclusion = "经营者转让后，受让方应继续履行合同；受让方拒绝服务的，消费者可向转让方和受让方主张相应责任。"
        elif facts.transfer_notified:
            conclusion = "经营者转让后，受让方应继续履行合同；转让方已通知消费者的，是否继续承担责任需结合转让协议和消费者权益受影响情况判断。"
        else:
            conclusion = "经营者转让后，受让方应继续履行合同；转让方未告知消费者的，仍应承担相应责任。"
        return _format_service_output(major, minor, conclusion, triggered, facts, [*path, "服务提供方义务审查"], procedure_findings)

    if facts.prepaid_consumption:
        triggered.append(config.patch_name("SVC2", "预付式消费特殊规则"))
        major = "《消费者权益保护法》第53条规定，经营者以预收款方式提供服务的，应按约定提供；未按约定提供的，应按消费者要求履行约定或者退回预付款。预付式消费司法解释支持经营者终止营业且恶意逃避退款时的惩罚性赔偿。"
        minor = "识别到服务接受方预先支付费用，服务提供方多次或持续提供服务，属于预付式消费场景。"
        refund = facts.unused_amount or facts.prepaid_amount
        if facts.operator_closed and facts.malicious_refund_evasion:
            triggered.append(config.patch_name("SVC10", "恶意逃避退款惩罚性赔偿"))
            punitive = refund * 3 if refund > 0 else 0.0
            conclusion = f"本案为预付式消费，经营者未按约定提供服务，应退还预付款 {_money(refund)}，并适用惩罚性赔偿；赔偿金额为 {_money(punitive)}。"
        elif facts.operator_closed or facts.service_not_provided:
            conclusion = f"本案为预付式消费，经营者未按约定提供服务，应退还预付款 {_money(refund)}，不适用惩罚性赔偿。"
        elif facts.service_partly_provided:
            conclusion = f"本案为预付式消费，经营者已部分提供服务，应按未提供服务比例退还预付款 {_money(refund)}；赠送服务不纳入已提供服务价值计算。"
        else:
            conclusion = "本案为预付式消费；经营者仍可按约提供服务的，消费者可要求继续履行，未按约提供的可请求退还相应预付款。"
        return _format_service_output(major, minor, conclusion, triggered, facts, [*path, "合同类型细分"], procedure_findings)

    if facts.provider_unilateral_change:
        triggered.append(config.patch_name("SVC6", "服务方单方变更服务内容"))
        major = "《民法典》第509条规定，当事人应按约定全面履行义务。服务提供方未经协商一致单方变更服务内容、方式或标准的，构成违约。"
        minor = "识别到服务提供方单方面调整服务内容、方式或标准。"
        if facts.accepted_change:
            conclusion = "服务提供方变更服务内容已经服务接受方同意，不构成违约；双方应按变更后的约定履行。"
        else:
            conclusion = "服务提供方单方变更服务内容构成违约，服务接受方可以要求继续履行原约定或解除合同并赔偿损失。"
        return _format_service_output(major, minor, conclusion, triggered, facts, [*path, "服务内容与标准确定"], procedure_findings)

    if facts.provider_no_qualification or facts.staff_mismatch:
        triggered.append(config.patch_name("SVC7", "服务方资质缺失或人员不符"))
        major = "服务提供方应具备法定资质或执业资格，实际提供服务的人员也应符合合同约定。资质缺失或人员不符导致合同目的受影响的，服务方应承担违约责任。"
        minor = "识别到服务方不具备资质、执业资格，或实际服务人员与约定不符。"
        conclusion = "服务方不具备法定资质或实际服务人员不符合约定，构成违约；服务接受方可以解除合同并要求退款、赔偿损失。"
        return _format_service_output(major, minor, conclusion, triggered, facts, [*path, "服务提供方义务审查"], procedure_findings)

    path.append("服务未提供或未完全提供")
    if facts.service_receiver_fault:
        triggered.append(config.patch_name("SVC9", "服务接受方原因解除损失赔偿"))
        major = "服务接受方因自身原因单方解除合同，而经营者不存在违约或过错的，应根据公平原则和诚实信用原则承担经营者合理损失，剩余预付款应予退还。"
        minor = "识别到服务接受方因搬家、不再需要等自身原因要求解除或退款。"
        refund_base = facts.unused_amount or facts.prepaid_amount
        balance = max(0.0, refund_base - facts.reasonable_loss) if refund_base > 0 else 0.0
        conclusion = f"服务接受方因自身原因解除合同，应承担合理损失 {_money(facts.reasonable_loss)}，扣除后退还余额 {_money(balance)}。"
        return _format_service_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.service_not_provided or facts.service_partly_provided or facts.operator_closed:
        major = "《民法典》第577条、第582条规定，一方未履行或履行不符合约定的，应承担继续履行、采取补救措施、减少价款或者赔偿损失等违约责任。"
        minor = "识别到服务方未提供或未完全提供约定服务。"
        refund = facts.unused_amount or facts.prepaid_amount
        if facts.operator_closed:
            conclusion = f"服务方停业或停止营业构成根本违约，服务接受方可以解除合同并要求退还未提供服务对应款项 {_money(refund)}。"
        elif facts.service_not_provided:
            conclusion = f"服务方完全未提供服务，服务接受方可以解除合同并要求全额退款 {_money(refund)}。"
        else:
            conclusion = f"服务方部分提供服务，应按未提供服务比例退款 {_money(refund)}；已提供服务部分按合同价格或通常价格结算。"
        return _format_service_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("服务质量")
    if facts.guaranteed_result:
        triggered.append(config.patch_name("SVC13", "保过包过承诺"))
        major = "服务合同中的保过、包过、不过全退等承诺，若构成合同内容，服务方未实现承诺目标且不可归责于服务接受方的，应承担违约责任。"
        minor = "识别到服务合同包含保过、包过或不过全退等承诺。"
        if facts.goal_not_achieved and not facts.receiver_fault_goal:
            conclusion = "‘保过’承诺构成合同义务，目标未实现，服务方应承担违约责任，服务接受方可以要求退款或赔偿。"
        elif facts.receiver_fault_goal:
            conclusion = "目标未实现系服务接受方不配合、缺课等自身原因导致的，服务方不当然承担保过违约责任。"
        else:
            conclusion = "‘保过’承诺构成合同义务；是否违约需查明承诺目标是否未实现及原因。"
        return _format_service_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.service_quality_dispute or facts.quality_nonconform or facts.quality_conform:
        triggered.append(config.patch_name("SVC5", "服务质量标准认定"))
        major = "服务质量标准有明确约定的按约定；约定不明的，按行业标准、通常标准、合同目的和交易习惯综合判断。服务质量不符合约定的，服务方应承担继续履行、补救、减少价款或赔偿损失等责任。"
        if facts.quality_conform:
            minor = "识别到服务质量符合合同约定、行业标准或通常标准。"
            conclusion = "服务质量符合约定或行业标准，服务提供方不构成违约，服务接受方应按约支付服务费。"
        else:
            minor = "识别到服务质量不达标或双方对服务质量存在争议。"
            conclusion = "服务质量不符合约定或行业标准，服务提供方构成违约；服务接受方可以要求继续履行、采取补救措施、减少费用或赔偿损失。"
        return _format_service_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("服务合同解除")
    if facts.health_change:
        triggered.append(config.patch_name("SVC3", "身体健康原因解除"))
        major = "预付式消费司法解释第13条规定，消费者身体健康属于预付式消费合同的基础条件；该条件发生无法预见的重大变化，继续履行明显不公平的，消费者可以请求解除合同。"
        minor = "识别到服务接受方因身体健康原因无法继续接受服务。"
        refund = facts.unused_amount or facts.prepaid_amount
        if facts.medical_advice and (facts.unforeseeable or facts.unfair_to_continue):
            conclusion = f"消费者因身体健康原因解除合同，不构成违约，不应承担违约金，应退还款项 {_money(refund)}。"
        else:
            conclusion = "消费者因身体健康原因解除合同，需结合医疗机构建议、健康变化是否无法预见、继续履行是否明显不公平确定是否免除违约责任。"
        return _format_service_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.indefinite_service:
        triggered.append(config.patch_name("SVC8", "不定期继续性服务合同任意解除"))
        major = "《民法典》第563条第2款规定，以持续履行的债务为内容的不定期合同，当事人可以随时解除合同，但是应当在合理期限之前通知对方。"
        minor = "识别到服务合同未约定服务期限，或属于长期持续提供服务的不定期合同。"
        if facts.reasonable_notice:
            conclusion = "不定期继续性服务合同，当事人可以随时解除，已在合理期限前通知，解除有效；退款按实际接受服务情况计算。"
        else:
            conclusion = "不定期继续性服务合同，当事人可以随时解除，但未在合理期限前通知的，应赔偿因此给对方造成的合理损失。"
        return _format_service_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.termination_request or facts.force_majeure:
        major = "《民法典》第563条规定，因不可抗力、一方明确不履行、迟延履行经催告仍不履行，或其他违约行为导致合同目的不能实现的，当事人可以解除合同。"
        minor = "识别到服务合同解除争议。"
        if facts.force_majeure:
            conclusion = "因不可抗力导致合同目的不能实现的，可以解除合同；尚未履行部分终止履行，已履行部分按公平原则结算。"
        else:
            conclusion = "是否可以解除需查明服务方是否根本违约、迟延履行经催告仍未履行，或合同目的是否不能实现；解除后按履行情况退款并由违约方赔偿损失。"
        return _format_service_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.service_contract:
        major = "服务合同的核心是服务提供方按约定提供服务，服务接受方支付服务费；裁判应围绕服务是否提供、质量是否达标、是否可解除和退款金额进行审查。"
        minor = "已识别服务合同关系，但未稳定识别服务未提供、服务质量、预付费、格式条款、解除依据或损失金额等足以输出最终裁判的事实。"
        conclusion = "事实要素不足，需补充服务类型、付款金额、已提供服务比例、质量标准、解除原因、是否预付式消费或是否存在经营者违约后再裁判。"
        return _format_service_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    major = "服务合同纠纷应围绕服务行为是否提供、服务质量是否达标、服务费是否应付、合同能否解除以及如何退款进行审查。"
    minor = "自然语言事实未能稳定识别出足以进入最终结论的服务合同关键事实。"
    conclusion = "事实要素不足，需补充是否存在服务合同关系、服务内容、付款金额、履行情况、质量争议或解除退款事实后再裁判。"
    return _format_service_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
