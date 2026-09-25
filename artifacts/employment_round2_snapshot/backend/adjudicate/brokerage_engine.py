"""Brokerage-contract adjudication engine."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from adjudicate.brokerage_configs import get_brokerage_config
from adjudicate.engine_v2 import _extract_money_near, _format_output, _mentions, _parse_date, _years_between


@dataclass
class BrokerageFacts:
    raw_text: str
    contract_type: str = "brokerage"
    contract_type_name: str = "中介合同"
    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    brokerage_contract: bool = False
    contract_date: Optional[date] = None
    third_party_tort: bool = False
    nature_dispute: bool = False
    intro_or_media_service: bool = False
    not_party_to_deal: bool = False
    own_name_trade: bool = False
    principal_name_affair: bool = False
    sale_own_obligation: bool = False
    oral_contract: bool = False
    evidence_exists: bool = False
    standard_clause_dispute: bool = False
    unreasonable_standard_clause: bool = False
    report_brokerage: bool = False
    media_brokerage: bool = False
    exclusive_entrustment: bool = False
    non_exclusive_entrustment: bool = False
    truthful_report_dispute: bool = False
    important_fact_hidden: bool = False
    false_information: bool = False
    principal_loss: bool = False
    best_efforts_dispute: bool = False
    best_efforts_done: bool = False
    staff_act_dispute: bool = False
    staff_scope_act: bool = False
    principal_wrong_info: bool = False
    broker_knew_wrong_info: bool = False
    bypass_claim: bool = False
    accepted_service: bool = False
    used_opportunity: bool = False
    bypassed_direct_contract: bool = False
    other_broker_legitimate: bool = False
    original_broker_not_cause: bool = False
    contract_concluded: bool = False
    contract_not_concluded: bool = False
    remuneration_claim: bool = False
    remuneration_agreed: bool = False
    remuneration_unclear: bool = False
    both_parties_bear: bool = False
    necessary_expense_claim: bool = False
    expense_agreed: bool = False
    policy_failure: bool = False
    termination_request: bool = False
    paid_brokerage: bool = False
    unpaid_brokerage: bool = False
    termination_loss: bool = False
    post_contract_obligation: bool = False
    post_contract_breach: bool = False
    burden_proof_dispute: bool = False
    broker_claim_completed: bool = False
    principal_claim_not_completed: bool = False
    proof_completed: bool = False
    actual_loss: float = 0.0
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "brokerage_contract": self.brokerage_contract,
            "contract_date": self.contract_date.isoformat() if self.contract_date else None,
            "third_party_tort": self.third_party_tort,
            "nature_dispute": self.nature_dispute,
            "intro_or_media_service": self.intro_or_media_service,
            "not_party_to_deal": self.not_party_to_deal,
            "own_name_trade": self.own_name_trade,
            "principal_name_affair": self.principal_name_affair,
            "sale_own_obligation": self.sale_own_obligation,
            "oral_contract": self.oral_contract,
            "evidence_exists": self.evidence_exists,
            "standard_clause_dispute": self.standard_clause_dispute,
            "unreasonable_standard_clause": self.unreasonable_standard_clause,
            "report_brokerage": self.report_brokerage,
            "media_brokerage": self.media_brokerage,
            "exclusive_entrustment": self.exclusive_entrustment,
            "non_exclusive_entrustment": self.non_exclusive_entrustment,
            "truthful_report_dispute": self.truthful_report_dispute,
            "important_fact_hidden": self.important_fact_hidden,
            "false_information": self.false_information,
            "principal_loss": self.principal_loss,
            "best_efforts_dispute": self.best_efforts_dispute,
            "best_efforts_done": self.best_efforts_done,
            "staff_act_dispute": self.staff_act_dispute,
            "staff_scope_act": self.staff_scope_act,
            "principal_wrong_info": self.principal_wrong_info,
            "broker_knew_wrong_info": self.broker_knew_wrong_info,
            "bypass_claim": self.bypass_claim,
            "accepted_service": self.accepted_service,
            "used_opportunity": self.used_opportunity,
            "bypassed_direct_contract": self.bypassed_direct_contract,
            "other_broker_legitimate": self.other_broker_legitimate,
            "original_broker_not_cause": self.original_broker_not_cause,
            "contract_concluded": self.contract_concluded,
            "contract_not_concluded": self.contract_not_concluded,
            "remuneration_claim": self.remuneration_claim,
            "remuneration_agreed": self.remuneration_agreed,
            "remuneration_unclear": self.remuneration_unclear,
            "both_parties_bear": self.both_parties_bear,
            "necessary_expense_claim": self.necessary_expense_claim,
            "expense_agreed": self.expense_agreed,
            "policy_failure": self.policy_failure,
            "termination_request": self.termination_request,
            "paid_brokerage": self.paid_brokerage,
            "unpaid_brokerage": self.unpaid_brokerage,
            "termination_loss": self.termination_loss,
            "post_contract_obligation": self.post_contract_obligation,
            "post_contract_breach": self.post_contract_breach,
            "burden_proof_dispute": self.burden_proof_dispute,
            "broker_claim_completed": self.broker_claim_completed,
            "principal_claim_not_completed": self.principal_claim_not_completed,
            "proof_completed": self.proof_completed,
            "actual_loss": self.actual_loss,
            "notes": self.notes,
        }


def _format_brokerage_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: BrokerageFacts,
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


def extract_brokerage_facts(case_text: str) -> BrokerageFacts:
    config = get_brokerage_config()
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = BrokerageFacts(raw_text=raw_text)

    for field_name in (
        "brokerage_contract", "third_party_tort", "nature_dispute",
        "intro_or_media_service", "not_party_to_deal", "own_name_trade",
        "principal_name_affair", "sale_own_obligation", "oral_contract",
        "evidence_exists", "standard_clause_dispute", "unreasonable_standard_clause",
        "report_brokerage", "media_brokerage", "exclusive_entrustment",
        "non_exclusive_entrustment", "truthful_report_dispute",
        "important_fact_hidden", "false_information", "principal_loss",
        "best_efforts_dispute", "best_efforts_done", "staff_act_dispute",
        "staff_scope_act", "principal_wrong_info", "broker_knew_wrong_info",
        "bypass_claim", "accepted_service", "used_opportunity",
        "bypassed_direct_contract", "other_broker_legitimate",
        "original_broker_not_cause", "contract_concluded", "contract_not_concluded",
        "remuneration_claim", "remuneration_agreed", "remuneration_unclear",
        "both_parties_bear", "necessary_expense_claim", "expense_agreed",
        "policy_failure", "termination_request", "paid_brokerage",
        "unpaid_brokerage", "termination_loss", "post_contract_obligation",
        "post_contract_breach", "burden_proof_dispute", "broker_claim_completed",
        "principal_claim_not_completed", "proof_completed",
    ):
        setattr(facts, field_name, _mentions(text, config.get_terms(field_name)))

    facts.asks_jurisdiction = _mentions(text, config.get_terms("jurisdiction_question")) or (
        ("起诉" in text or "法院" in text) and any(word in text for word in ("哪里", "去哪", "哪个", "管辖", "地点"))
    )
    facts.asks_defendant = _mentions(text, config.get_terms("defendant_question"))
    facts.contract_date = _parse_date(text, config.get_terms("contract_date"))
    facts.actual_loss = _extract_money_near(text, config.get_terms("actual_loss"))

    if any(
        (
            facts.intro_or_media_service, facts.report_brokerage, facts.media_brokerage,
            facts.bypass_claim, facts.remuneration_claim, facts.necessary_expense_claim,
            facts.truthful_report_dispute, facts.contract_concluded, facts.contract_not_concluded,
        )
    ):
        facts.brokerage_contract = True
    if facts.accepted_service and (facts.used_opportunity or facts.bypassed_direct_contract):
        facts.brokerage_contract = True
    return facts


def _procedure_findings(facts: BrokerageFacts) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append("中介合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理。")
    if facts.asks_defendant:
        findings.append("适格被告按请求确定：中介人请求报酬的，通常列委托人为被告；委托人主张中介人违约或赔偿的，通常列中介人为被告。")
    return findings


def _only_procedure_question(facts: BrokerageFacts) -> bool:
    substantive = any(
        (
            facts.nature_dispute, facts.oral_contract, facts.standard_clause_dispute,
            facts.truthful_report_dispute, facts.best_efforts_dispute,
            facts.staff_act_dispute, facts.principal_wrong_info, facts.bypass_claim,
            facts.contract_concluded, facts.contract_not_concluded, facts.remuneration_claim,
            facts.necessary_expense_claim, facts.policy_failure, facts.termination_request,
            facts.post_contract_obligation, facts.burden_proof_dispute,
        )
    )
    return (facts.asks_jurisdiction or facts.asks_defendant) and not substantive


def adjudicate_brokerage(case_text: str, today: Optional[date] = None) -> Dict[str, Any]:
    config = get_brokerage_config()
    facts = extract_brokerage_facts(case_text)
    today = today or date.today()
    triggered: List[str] = []
    path: List[str] = ["入口程序校验"]
    procedure_findings = _procedure_findings(facts)

    if _only_procedure_question(facts):
        major = "中介合同纠纷的程序事项应先确认管辖法院和适格被告。"
        minor = "用户提出的是起诉地点或被告确定问题，未提出报酬、跳单、如实报告、解除等实体争议事实。"
        conclusion = "；".join(procedure_findings)
        return _format_brokerage_output(major, minor, conclusion, ["管辖程序"] if procedure_findings else [], facts, path, procedure_findings)

    if facts.contract_date and _years_between(facts.contract_date, today) > 3:
        major = "中介合同纠纷适用三年一般诉讼时效。"
        minor = f"识别到相关合同签订、服务履行或催告日期为{facts.contract_date.isoformat()}，截至{today.isoformat()}已经超过三年。"
        conclusion = "诉讼时效已过，驳回请求。"
        return _format_brokerage_output(major, minor, conclusion, [], facts, [*path, "诉讼时效"], procedure_findings)

    if facts.burden_proof_dispute:
        triggered.append(config.patch_name("M14", "中介合同纠纷的举证责任"))
        major = "主张中介合同关系存在、主张中介义务已经完成，或者主张对方未履行义务的一方，应对其主张承担举证责任；举证不能的，承担不利后果。"
        minor = "识别到双方对中介合同关系或中介义务履行存在争议。"
        if facts.broker_claim_completed:
            subject = "中介人"
        elif facts.principal_claim_not_completed:
            subject = "委托人"
        else:
            subject = "提出具体主张的一方"
        result = "已完成举证，不承担举证不能的不利后果" if facts.proof_completed else "未完成举证，应承担不利后果"
        conclusion = f"{subject}承担举证责任，{result}。"
        return _format_brokerage_output(major, minor, conclusion, triggered, facts, [*path, "举证责任"], procedure_findings)

    if facts.third_party_tort and not facts.brokerage_contract:
        major = "中介合同裁判引擎处理中介人与委托人之间因报告订约机会、提供媒介服务、报酬或如实报告义务产生的合同争议；单纯合同外第三人侵权应按侵权责任处理。"
        minor = "识别到争议核心是合同外第三人侵权，未识别到中介合同履行争议。"
        conclusion = "本案涉及侵权责任，非中介合同纠纷，不适用本中介合同裁判引擎。"
        return _format_brokerage_output(major, minor, conclusion, [], facts, path, procedure_findings)

    path.append("前置实体判断")
    if any((facts.nature_dispute, facts.own_name_trade, facts.principal_name_affair, facts.sale_own_obligation)):
        triggered.append(config.patch_name("M1", "中介合同的性质认定"))
        major = "《民法典》第961条规定，中介合同是中介人向委托人报告订立合同的机会或者提供订立合同的媒介服务，委托人支付报酬的合同。合同性质应按实质内容认定。"
        if facts.intro_or_media_service and (facts.not_party_to_deal or not (facts.own_name_trade or facts.principal_name_affair or facts.sale_own_obligation)):
            minor = "识别到一方处于介绍人或撮合人地位，向委托人报告订约机会或提供媒介服务，且未直接参与委托人与第三人的交易合同。"
            conclusion = "合同性质认定为中介合同，适用中介合同裁判规则。"
        elif facts.own_name_trade:
            minor = "识别到一方以自己名义与第三人从事代购、代销、寄售等贸易活动。"
            conclusion = "合同性质更接近行纪合同，不适用中介合同裁判规则。"
        elif facts.principal_name_affair:
            minor = "识别到受托人以委托人名义处理事务，而非仅报告订约机会或提供媒介服务。"
            conclusion = "合同性质更接近委托合同，不适用中介合同裁判规则。"
        elif facts.sale_own_obligation:
            minor = "识别到一方直接参与交易并承担买卖合同权利义务。"
            conclusion = "合同性质更接近买卖合同或其他交易合同，不适用中介合同裁判规则。"
        else:
            minor = "现有事实不足以确认一方是否仅处于介绍人地位并提供订约机会或媒介服务。"
            conclusion = "合同性质暂不能稳定认定，需补充中介人的服务内容、签约名义和是否参与交易合同后再裁判。"
        return _format_brokerage_output(major, minor, conclusion, triggered, facts, [*path, "合同性质认定"], procedure_findings)

    if facts.oral_contract:
        triggered.append(config.patch_name("M8", "口头中介协议的效力"))
        major = "《民法典》第961条未要求中介合同必须采用书面形式；能够证明双方存在中介合意并已提供中介服务的，口头中介协议可以成立。"
        minor = "识别到双方未签订书面中介合同，但主张存在口头中介合意。"
        conclusion = "口头中介协议成立，中介合同关系存在。" if facts.evidence_exists else "口头中介协议证据不足，中介合同关系暂不能认定存在。"
        return _format_brokerage_output(major, minor, conclusion, triggered, facts, [*path, "合同成立与效力审查"], procedure_findings)

    if facts.standard_clause_dispute:
        triggered.append(config.patch_name("M12", "中介合同格式条款的效力"))
        major = "《民法典》第496条、第497条规定，提供格式条款的一方应履行提示说明义务；不合理免除或减轻其责任、加重对方责任、限制对方主要权利的格式条款无效。"
        minor = "识别到中介合同中的格式条款被主张无效。"
        conclusion = "该格式条款不合理地免除或减轻中介责任、加重委托人责任或限制主要权利，应认定无效。" if facts.unreasonable_standard_clause else "暂未识别到格式条款存在不合理免责、加重责任或限制主要权利情形，不能直接认定无效。"
        return _format_brokerage_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查"], procedure_findings)

    if facts.staff_act_dispute:
        triggered.append(config.patch_name("M9", "中介人工作人员行为的责任归属"))
        major = "中介人工作人员在履行职务过程中作出的行为，其后果通常由中介人承担；非职务行为由行为人自行承担责任。"
        minor = "识别到中介人工作人员行为引发争议。"
        conclusion = "工作人员行为属于职务行为，责任由中介人承担。" if facts.staff_scope_act else "工作人员行为暂不能认定属于职务行为，责任应由工作人员自行承担或另行查明。"
        return _format_brokerage_output(major, minor, conclusion, triggered, facts, [*path, "中介人义务审查"], procedure_findings)

    if facts.principal_wrong_info:
        triggered.append(config.patch_name("M11", "委托人提供信息有误导致中介服务瑕疵"))
        major = "中介合同履行中，各方应遵循诚信原则。委托人提供信息有误导致中介服务瑕疵的，委托人承担相应责任；中介人明知或应知信息有误仍继续服务的，也应承担相应责任。"
        minor = "识别到中介服务瑕疵来源于委托人提供的信息错误。"
        conclusion = "中介人明知或应知信息有误仍继续服务，中介人也应承担相应责任。" if facts.broker_knew_wrong_info else "委托人提供信息有误，委托人承担相应责任。"
        return _format_brokerage_output(major, minor, conclusion, triggered, facts, [*path, "中介人义务审查"], procedure_findings)

    if facts.best_efforts_dispute:
        triggered.append(config.patch_name("M6", "中介人的尽力义务"))
        major = "中介人应依据中介合同内容和诚信原则履行促成交易的合理努力义务。"
        minor = "识别到委托人主张中介人未尽力促成交易。"
        conclusion = "中介人已履行尽力义务，不构成违约。" if facts.best_efforts_done else "中介人未履行尽力义务，构成违约。"
        return _format_brokerage_output(major, minor, conclusion, triggered, facts, [*path, "中介人义务审查"], procedure_findings)

    path.append("跳单认定与责任")
    if facts.bypass_claim:
        triggered.append(config.patch_name("M2", "“跳单”的认定标准"))
        major = "《民法典》第965条规定，委托人在接受中介人的服务后，利用中介人提供的交易机会或者媒介服务，绕开中介人直接订立合同的，应当向中介人支付报酬。"
        minor = "识别到委托人绕开中介人直接订立合同，中介人主张报酬。"
        if facts.non_exclusive_entrustment and facts.other_broker_legitimate:
            triggered.append(config.patch_name("M13", "独家委托 vs 非独家委托对“跳单”认定的影响"))
            conclusion = "本案属于非独家委托，委托人通过其他中介人正当途径获取相同信息并完成交易，不构成“跳单”，委托人不应向原中介人支付报酬。"
        elif facts.original_broker_not_cause:
            conclusion = "原中介人未能促成合同成立，委托人后续成交与原中介服务之间缺乏充分关联，不构成“跳单”，委托人不应向原中介人支付报酬。"
        elif facts.accepted_service and facts.used_opportunity and facts.bypassed_direct_contract:
            conclusion = "构成“跳单”的三个要件全部满足，构成“跳单”，委托人应向中介人支付报酬。"
        else:
            conclusion = "构成“跳单”的三个要件未全部满足，不构成“跳单”，委托人不应向中介人支付报酬。"
        return _format_brokerage_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("报酬支付")
    if facts.policy_failure:
        triggered.append(config.patch_name("M10", "政策原因导致交易不成的责任"))
        major = "《民法典》第964条规定，中介人未促成合同成立的，不得请求支付报酬；但是可以按照约定请求委托人支付从事中介活动支出的必要费用。"
        minor = "识别到交易因限购、贷款政策变化等政策原因未能成立。"
        conclusion = "因政策原因导致交易不成，中介人不得请求报酬；如双方对必要费用有约定，中介人可以请求必要费用。"
        return _format_brokerage_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.contract_not_concluded and (facts.remuneration_claim or facts.necessary_expense_claim):
        triggered.append(config.patch_name("M4", "未促成合同成立时的必要费用"))
        major = "《民法典》第964条规定，中介人未促成合同成立的，不得请求支付报酬；但是可以按照约定请求委托人支付从事中介活动支出的必要费用。"
        minor = "识别到中介人未促成合同成立，但仍主张报酬或必要费用。"
        if facts.expense_agreed or facts.necessary_expense_claim:
            conclusion = f"中介人未促成合同成立，不得请求支付报酬；有必要费用约定或必要费用事实的，可以请求支付必要费用，金额为{_money(facts.actual_loss)}。"
        else:
            conclusion = "中介人未促成合同成立，不得请求支付报酬；未识别必要费用约定，必要费用由中介人自行承担。"
        return _format_brokerage_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.contract_concluded and facts.remuneration_claim:
        triggered.append(config.patch_name("M3", "报酬的计算与负担"))
        major = "《民法典》第963条规定，中介人促成合同成立的，委托人应按约定支付报酬；没有约定或约定不明确的，根据中介人的劳务合理确定。因中介人提供媒介服务而促成合同成立的，由该合同的当事人平均负担中介人的报酬；中介活动费用由中介人负担。"
        minor = "识别到中介人已经促成合同成立，并请求支付中介报酬。"
        amount = _money(facts.actual_loss)
        if facts.remuneration_agreed:
            conclusion = f"报酬按约定确定为{amount}，由委托人支付；中介活动费用由中介人自行负担。"
        elif facts.both_parties_bear or facts.media_brokerage:
            conclusion = f"报酬根据中介人的劳务合理确定为{amount}，由交易合同当事人平均负担；中介活动费用由中介人自行负担。"
        else:
            conclusion = f"报酬没有约定或约定不明，应根据中介人的劳务合理确定，暂按{amount}处理；中介活动费用由中介人自行负担。"
        return _format_brokerage_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("如实报告义务")
    if facts.truthful_report_dispute:
        triggered.append(config.patch_name("M5", "中介人如实报告义务的违反"))
        major = "《民法典》第962条规定，中介人应当就有关订立合同的事项向委托人如实报告。中介人故意隐瞒与订立合同有关的重要事实或者提供虚假情况，损害委托人利益的，不得请求支付报酬并应当承担赔偿责任。"
        minor = "识别到委托人主张中介人未如实报告或提供虚假信息。"
        if (facts.important_fact_hidden or facts.false_information) and facts.principal_loss:
            conclusion = f"中介人违反如实报告义务，不可以请求支付报酬，并应承担赔偿责任；已识别损失为{_money(facts.actual_loss)}。"
        elif facts.important_fact_hidden or facts.false_information:
            conclusion = "中介人存在未如实报告或提供虚假情况，但尚需证明该行为损害委托人利益；损害成立后，中介人不得请求报酬并应赔偿。"
        else:
            conclusion = "暂未识别中介人故意隐瞒重要事实或提供虚假情况，中介人不当然丧失报酬请求权。"
        return _format_brokerage_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("中介合同解除")
    if facts.termination_request:
        triggered.append(config.patch_name("M7", "中介合同解除"))
        major = "《民法典》第966条规定，中介合同章没有规定的，参照适用委托合同的有关规定；第933条规定，委托人或者受托人可以随时解除委托合同。中介合同可参照适用随时解除规则，但造成损失的应按有偿或无偿情形赔偿。"
        minor = "识别到委托人或中介人主张解除中介合同。"
        if facts.termination_loss and facts.paid_brokerage:
            conclusion = f"中介合同解除有效；有偿中介解除造成损失的，赔偿范围包括直接损失和可得利益，已识别金额为{_money(facts.actual_loss)}。"
        elif facts.termination_loss:
            conclusion = f"中介合同解除有效；解除时间不当造成损失的，赔偿范围为直接损失，已识别金额为{_money(facts.actual_loss)}。"
        else:
            conclusion = "中介合同解除有效；未识别解除造成损失，暂不支持损失赔偿。"
        return _format_brokerage_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("后合同义务")
    if facts.post_contract_obligation:
        triggered.append(config.patch_name("M15", "中介合同终止后的后合同义务"))
        major = "《民法典》第558条规定，合同的权利义务关系终止后，当事人应当遵循诚信等原则，根据交易习惯履行通知、协助、保密、旧物回收等义务。"
        minor = "识别到中介合同终止后，一方主张另一方违反通知、协助、保密等后合同义务。"
        conclusion = "一方已违反后合同义务，应承担相应责任。" if facts.post_contract_breach else "暂未识别违反后合同义务的具体行为，不应直接承担责任。"
        return _format_brokerage_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.brokerage_contract:
        major = "《民法典》第961条至第966条规定，中介合同裁判应围绕中介人是否报告订约机会或提供媒介服务、是否促成合同成立、是否构成“跳单”、是否违反如实报告义务以及报酬和必要费用如何处理进行审查。"
        minor = "已识别中介合同关系，但未稳定识别足以触发报酬、跳单、如实报告、必要费用、解除或后合同义务的具体争议事实。"
        conclusion = "事实要素不足，需要补充中介人提供了哪些服务、是否促成合同成立、是否绕开中介成交、是否存在隐瞒或虚假信息、报酬和费用如何约定后再裁判。"
        return _format_brokerage_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    major = "中介合同纠纷应围绕中介人报告订约机会或提供媒介服务、委托人支付报酬、促成合同成立、跳单、如实报告义务和解除后果进行审查。"
    minor = "自然语言事实未能稳定识别出中介合同关系和关键争议节点。"
    conclusion = "事实要素不足，需要补充是否存在中介服务、委托人是否接受服务、合同是否成立、中介是否主张报酬或是否存在跳单、隐瞒事实等情形后再裁判。"
    return _format_brokerage_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
