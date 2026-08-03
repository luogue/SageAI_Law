"""Commission-agency-contract adjudication engine."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from adjudicate.commission_agency_configs import get_commission_agency_config
from adjudicate.engine_v2 import _extract_money_near, _format_output, _mentions, _parse_date, _years_between


@dataclass
class CommissionAgencyFacts:
    raw_text: str
    contract_type: str = "commission_agency"
    contract_type_name: str = "行纪合同"
    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    commission_agency_contract: bool = False
    contract_date: Optional[date] = None
    third_party_tort: bool = False
    nature_dispute: bool = False
    own_name_trade: bool = False
    principal_name: bool = False
    intermediary_service: bool = False
    sale_contract: bool = False
    trade_activity: bool = False
    oral_contract: bool = False
    evidence_exists: bool = False
    identity_confusion: bool = False
    custody_damage: bool = False
    proper_custody: bool = False
    improper_custody: bool = False
    expense_claim: bool = False
    expense_agreed: bool = False
    third_party_contract: bool = False
    third_party_default: bool = False
    principal_loss: bool = False
    liability_excluded_agreed: bool = False
    malicious_collusion: bool = False
    price_instruction: bool = False
    low_sell: bool = False
    high_buy: bool = False
    high_sell: bool = False
    low_buy: bool = False
    principal_consent: bool = False
    difference_compensated: bool = False
    special_instruction: bool = False
    market_priced_goods: bool = False
    intervention_claim: bool = False
    contrary_expression: bool = False
    defective_or_perishable: bool = False
    disposal_claim: bool = False
    cannot_contact: bool = False
    proceeds_transfer: bool = False
    buy_in: bool = False
    refuse_accept: bool = False
    cannot_sell: bool = False
    withdraw_sale: bool = False
    refuse_take_back: bool = False
    urged: bool = False
    deposit_claim: bool = False
    remuneration_claim: bool = False
    remuneration_unpaid: bool = False
    matter_completed: bool = False
    remuneration_agreed: bool = False
    remuneration_unclear: bool = False
    lien_claim: bool = False
    lien_excluded: bool = False
    sub_entrustment: bool = False
    sub_entrustment_consent: bool = False
    termination_request: bool = False
    paid_commission: bool = False
    unpaid_commission: bool = False
    termination_loss: bool = False
    actual_loss: float = 0.0
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "commission_agency_contract": self.commission_agency_contract,
            "contract_date": self.contract_date.isoformat() if self.contract_date else None,
            "third_party_tort": self.third_party_tort,
            "nature_dispute": self.nature_dispute,
            "own_name_trade": self.own_name_trade,
            "principal_name": self.principal_name,
            "intermediary_service": self.intermediary_service,
            "sale_contract": self.sale_contract,
            "trade_activity": self.trade_activity,
            "oral_contract": self.oral_contract,
            "evidence_exists": self.evidence_exists,
            "identity_confusion": self.identity_confusion,
            "custody_damage": self.custody_damage,
            "proper_custody": self.proper_custody,
            "improper_custody": self.improper_custody,
            "expense_claim": self.expense_claim,
            "expense_agreed": self.expense_agreed,
            "third_party_contract": self.third_party_contract,
            "third_party_default": self.third_party_default,
            "principal_loss": self.principal_loss,
            "liability_excluded_agreed": self.liability_excluded_agreed,
            "malicious_collusion": self.malicious_collusion,
            "price_instruction": self.price_instruction,
            "low_sell": self.low_sell,
            "high_buy": self.high_buy,
            "high_sell": self.high_sell,
            "low_buy": self.low_buy,
            "principal_consent": self.principal_consent,
            "difference_compensated": self.difference_compensated,
            "special_instruction": self.special_instruction,
            "market_priced_goods": self.market_priced_goods,
            "intervention_claim": self.intervention_claim,
            "contrary_expression": self.contrary_expression,
            "defective_or_perishable": self.defective_or_perishable,
            "disposal_claim": self.disposal_claim,
            "cannot_contact": self.cannot_contact,
            "proceeds_transfer": self.proceeds_transfer,
            "buy_in": self.buy_in,
            "refuse_accept": self.refuse_accept,
            "cannot_sell": self.cannot_sell,
            "withdraw_sale": self.withdraw_sale,
            "refuse_take_back": self.refuse_take_back,
            "urged": self.urged,
            "deposit_claim": self.deposit_claim,
            "remuneration_claim": self.remuneration_claim,
            "remuneration_unpaid": self.remuneration_unpaid,
            "matter_completed": self.matter_completed,
            "remuneration_agreed": self.remuneration_agreed,
            "remuneration_unclear": self.remuneration_unclear,
            "lien_claim": self.lien_claim,
            "lien_excluded": self.lien_excluded,
            "sub_entrustment": self.sub_entrustment,
            "sub_entrustment_consent": self.sub_entrustment_consent,
            "termination_request": self.termination_request,
            "paid_commission": self.paid_commission,
            "unpaid_commission": self.unpaid_commission,
            "termination_loss": self.termination_loss,
            "actual_loss": self.actual_loss,
            "notes": self.notes,
        }


def _format_commission_agency_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: CommissionAgencyFacts,
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


def extract_commission_agency_facts(case_text: str) -> CommissionAgencyFacts:
    config = get_commission_agency_config()
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = CommissionAgencyFacts(raw_text=raw_text)

    for field_name in (
        "commission_agency_contract", "third_party_tort", "nature_dispute", "own_name_trade",
        "principal_name", "intermediary_service", "sale_contract", "trade_activity",
        "oral_contract", "evidence_exists", "identity_confusion", "custody_damage",
        "proper_custody", "improper_custody", "expense_claim", "expense_agreed",
        "third_party_contract", "third_party_default", "principal_loss",
        "liability_excluded_agreed", "malicious_collusion", "price_instruction",
        "low_sell", "high_buy", "high_sell", "low_buy", "principal_consent",
        "difference_compensated", "special_instruction", "market_priced_goods",
        "intervention_claim", "contrary_expression", "defective_or_perishable",
        "disposal_claim", "cannot_contact", "proceeds_transfer", "buy_in",
        "refuse_accept", "cannot_sell", "withdraw_sale", "refuse_take_back",
        "urged", "deposit_claim", "remuneration_claim", "remuneration_unpaid",
        "matter_completed", "remuneration_agreed", "remuneration_unclear",
        "lien_claim", "lien_excluded", "sub_entrustment", "sub_entrustment_consent",
        "termination_request", "paid_commission", "unpaid_commission", "termination_loss",
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
            facts.own_name_trade, facts.trade_activity, facts.third_party_contract,
            facts.price_instruction, facts.intervention_claim, facts.remuneration_claim,
            facts.lien_claim, facts.deposit_claim, facts.defective_or_perishable,
        )
    ):
        facts.commission_agency_contract = True
    return facts


def _procedure_findings(facts: CommissionAgencyFacts) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append("行纪合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理。")
    if facts.asks_defendant:
        findings.append("适格被告通常为行纪人或委托人；行纪人与第三人订立的合同，由行纪人直接享有权利、承担义务。")
    return findings


def _only_procedure_question(facts: CommissionAgencyFacts) -> bool:
    substantive = any(
        (
            facts.nature_dispute, facts.own_name_trade, facts.principal_name,
            facts.intermediary_service, facts.sale_contract, facts.trade_activity,
            facts.oral_contract, facts.identity_confusion, facts.custody_damage,
            facts.expense_claim, facts.third_party_default, facts.malicious_collusion,
            facts.price_instruction, facts.intervention_claim, facts.defective_or_perishable,
            facts.deposit_claim, facts.remuneration_claim, facts.remuneration_unpaid,
            facts.lien_claim, facts.sub_entrustment, facts.termination_request,
        )
    )
    return (facts.asks_jurisdiction or facts.asks_defendant) and not substantive


def adjudicate_commission_agency(case_text: str, today: Optional[date] = None) -> Dict[str, Any]:
    config = get_commission_agency_config()
    facts = extract_commission_agency_facts(case_text)
    today = today or date.today()
    triggered: List[str] = []
    path: List[str] = ["入口程序校验"]
    procedure_findings = _procedure_findings(facts)

    if _only_procedure_question(facts):
        major = "行纪合同纠纷的程序事项应先确认管辖法院和适格被告。"
        minor = "用户提出的是起诉地点或被告确定问题，未提出行纪事务履行、第三人交易、价格指示、报酬或留置等实体争议事实。"
        conclusion = "；".join(procedure_findings)
        return _format_commission_agency_output(major, minor, conclusion, ["管辖程序"] if procedure_findings else [], facts, path, procedure_findings)

    if facts.third_party_tort and not facts.commission_agency_contract:
        major = "行纪合同裁判引擎处理行纪人与委托人之间因行纪事务产生的合同争议；单纯合同外第三人侵权应按侵权责任处理。"
        minor = "识别到争议核心是合同外第三人侵权，未识别到行纪合同履行争议。"
        conclusion = "本案涉及侵权责任，非行纪合同纠纷，不适用本行纪合同裁判引擎。"
        return _format_commission_agency_output(major, minor, conclusion, [], facts, path, procedure_findings)

    if facts.contract_date and _years_between(facts.contract_date, today) > 3:
        major = "行纪合同纠纷适用三年一般诉讼时效。"
        minor = f"识别到相关合同签订、履行或催告日期为{facts.contract_date.isoformat()}，截至{today.isoformat()}已经超过三年。"
        conclusion = "诉讼时效已过，驳回请求。"
        return _format_commission_agency_output(major, minor, conclusion, [], facts, [*path, "诉讼时效"], procedure_findings)

    path.append("前置实体判断")
    if any((facts.nature_dispute, facts.own_name_trade, facts.principal_name, facts.intermediary_service, facts.sale_contract, facts.trade_activity)):
        triggered.append(config.patch_name("J1", "行纪合同的性质认定"))
        major = "《民法典》第951条规定，行纪合同是行纪人以自己的名义为委托人从事贸易活动，委托人支付报酬的合同。合同性质应按实质内容认定。"
        if facts.own_name_trade and facts.trade_activity:
            minor = "识别到行纪人以自己名义与第三人从事代购、代销、寄售等贸易活动。"
            conclusion = "合同性质认定为行纪合同，适用行纪合同裁判规则。"
        elif facts.principal_name:
            minor = "识别到受托人是以委托人名义处理事务，而非以自己名义交易。"
            conclusion = "合同性质更接近委托合同，不适用行纪合同裁判规则。"
        elif facts.intermediary_service:
            minor = "识别到合同核心是报告订约机会或提供媒介服务。"
            conclusion = "合同性质更接近中介合同，不适用行纪合同裁判规则。"
        elif facts.sale_contract and not facts.own_name_trade:
            minor = "识别到合同核心是标的物所有权转移，而非为委托人从事贸易活动。"
            conclusion = "合同性质更接近买卖合同，不适用行纪合同裁判规则。"
        else:
            minor = "现有事实显示存在贸易活动，但尚不足以确认行纪人是否以自己名义为委托人交易。"
            conclusion = "合同性质暂不能稳定认定，需要补充签约名义、交易相对方和报酬约定后再裁判。"
        return _format_commission_agency_output(major, minor, conclusion, triggered, facts, [*path, "合同性质认定"], procedure_findings)

    if facts.oral_contract:
        triggered.append(config.patch_name("J15", "行纪合同未采用书面形式"))
        major = "《民法典》第951条未要求行纪合同必须采用书面形式；口头约定亦可成立，但需要证据证明行纪关系存在。"
        minor = "识别到双方未签书面行纪合同或仅有口头约定。"
        conclusion = "有证据证明行纪关系存在，行纪合同成立。" if facts.evidence_exists else "缺少证据证明行纪关系存在，行纪合同不成立。"
        return _format_commission_agency_output(major, minor, conclusion, triggered, facts, [*path, "合同形式审查"], procedure_findings)

    if facts.identity_confusion:
        triggered.append(config.patch_name("J14", "行纪人身份混同的处理"))
        major = "行纪人主张行纪合同权利，应能证明其处理的货物或交易属于行纪事务。身份混同且不能证明的，相关主张不成立。"
        minor = "识别到行纪人与其他职务身份或交易身份混同，不能清楚证明涉案货物属于行纪事务项下委托物。"
        conclusion = "行纪人身份混同，主张不成立。"
        return _format_commission_agency_output(major, minor, conclusion, triggered, facts, [*path, "身份混同"], procedure_findings)

    if facts.custody_damage:
        triggered.append(config.patch_name("J8", "行纪人妥善保管义务"))
        major = "《民法典》第953条规定，行纪人占有委托物的，应当妥善保管委托物。"
        minor = "识别到委托物在行纪人占有期间发生毁损、灭失或损坏。"
        if facts.proper_custody and not facts.improper_custody:
            conclusion = "行纪人已尽到妥善保管义务，不承担赔偿责任。"
        elif facts.improper_custody:
            conclusion = f"行纪人未尽到妥善保管义务，应承担赔偿责任，已识别损失为 {_money(facts.actual_loss)}。"
        else:
            conclusion = "需进一步审查行纪人是否尽到妥善保管义务；不能证明已妥善保管的，应承担相应责任。"
        return _format_commission_agency_output(major, minor, conclusion, triggered, facts, [*path, "妥善保管义务"], procedure_findings)

    if facts.expense_claim:
        triggered.append(config.patch_name("J9", "行纪人费用负担"))
        major = "《民法典》第952条规定，行纪人处理委托事务支出的费用，由行纪人负担，但是当事人另有约定的除外。"
        minor = "识别到行纪人要求委托人另行承担处理行纪事务发生的费用。"
        conclusion = "双方对费用负担另有约定，按约定处理。" if facts.expense_agreed else "处理委托事务的费用由行纪人自行负担，委托人无需另行报销。"
        return _format_commission_agency_output(major, minor, conclusion, triggered, facts, [*path, "费用负担"], procedure_findings)

    if facts.sub_entrustment:
        triggered.append(config.patch_name("J12", "行纪合同与转委托"))
        major = "《民法典》第960条规定，行纪合同章没有规定的，参照适用委托合同的有关规定；转委托责任可参照委托合同规则处理。"
        minor = "识别到行纪人将委托事务转交第三人处理。"
        if facts.sub_entrustment_consent:
            conclusion = "转委托经委托人同意，行纪人仅就第三人的选任和指示承担责任。"
        else:
            conclusion = "转委托未经委托人同意，行纪人应对第三人的行为向委托人承担全部责任。"
        return _format_commission_agency_output(major, minor, conclusion, triggered, facts, [*path, "转委托"], procedure_findings)

    path.append("第三人交易责任")
    if facts.malicious_collusion:
        triggered.append(config.patch_name("J10", "行纪人与第三人恶意串通"))
        major = "行纪人履行行纪合同应遵守诚信义务；与第三人恶意串通损害委托人利益的，应承担违约赔偿责任。"
        minor = "识别到行纪人与第三人串通，损害委托人利益。"
        conclusion = f"行纪人与第三人存在恶意串通，行纪人应承担全部赔偿责任，已识别损失为 {_money(facts.actual_loss)}。"
        return _format_commission_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.third_party_default:
        triggered.append(config.patch_name("J4", "行纪人对第三人违约的责任承担"))
        major = "《民法典》第958条规定，行纪人与第三人订立合同的，行纪人对该合同直接享有权利、承担义务；第三人不履行义务致使委托人受损的，行纪人应承担赔偿责任，但行纪人与委托人另有约定的除外。"
        minor = "识别到行纪人与第三人交易后，第三人不付款、不交货或存在其他不履行义务情形，并造成委托人损失。"
        if facts.liability_excluded_agreed:
            conclusion = "双方另有第三人风险承担约定，按该约定处理；行纪人不当然承担全部赔偿责任。"
        else:
            conclusion = f"第三人不履行义务，行纪人应向委托人承担赔偿责任，赔偿后可向第三人追偿；已识别损失为 {_money(facts.actual_loss)}。"
        return _format_commission_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("价格争议")
    if facts.price_instruction:
        triggered.append(config.patch_name("J2", "行纪人违反价格指示的处理"))
        major = "《民法典》第955条规定，行纪人低于委托人指定价格卖出或高于指定价格买入，应经委托人同意；未经同意但补偿差额的，对委托人发生效力。高于指定价格卖出或低于指定价格买入的，差价利益无约定时归委托人。"
        minor = "识别到委托人对交易价格有指定或特别指示，双方对交易价格处理存在争议。"
        if facts.low_sell or facts.high_buy:
            if facts.principal_consent:
                conclusion = "行纪人虽低卖或高买，但已经委托人同意，交易对委托人发生效力。"
            elif facts.difference_compensated:
                conclusion = "行纪人未经同意低卖或高买，但补偿差额的，交易对委托人发生效力，差额由行纪人承担。"
            else:
                conclusion = "行纪人未经同意低卖或高买且未补偿差额，相应损失由行纪人自行承担。"
        elif facts.high_sell or facts.low_buy:
            if facts.special_instruction:
                conclusion = "委托人有特别价格指示，行纪人不得违反；违反的，应承担违约责任。"
            else:
                conclusion = "行纪人高卖或低买产生的有利差价，没有约定或约定不明的，利益归委托人。"
        else:
            conclusion = "需要进一步查明实际成交价格与委托人指定价格的关系，再确定差价归属或赔偿责任。"
        return _format_commission_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("介入权")
    if facts.intervention_claim:
        triggered.append(config.patch_name("J3", "行纪人介入权的行使条件"))
        major = "《民法典》第956条规定，行纪人卖出或者买入具有市场定价的商品，除委托人有相反意思表示外，行纪人自己可以作为买受人或者出卖人，并仍可请求支付报酬。"
        minor = "识别到行纪人主张自己作为买受人或者出卖人介入交易。"
        if facts.market_priced_goods and not facts.contrary_expression:
            conclusion = "行纪人介入权成立，可以自己作为买受人或出卖人，并仍可请求委托人支付报酬。"
        else:
            conclusion = "行纪人介入权不成立，不能自行作为买受人或出卖人处理该交易。"
        return _format_commission_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("委托物处分")
    if facts.defective_or_perishable or facts.disposal_claim:
        triggered.append(config.patch_name("J7", "委托物瑕疵/易变质时的处分权"))
        major = "《民法典》第954条规定，委托物交付给行纪人时有瑕疵或者容易腐烂、变质的，经委托人同意，行纪人可以处分；不能及时联系委托人的，行纪人可以合理处分。"
        minor = "识别到委托物存在瑕疵、容易腐烂变质或行纪人主张处分委托物。"
        if facts.principal_consent or facts.cannot_contact:
            conclusion = "行纪人处分委托物合规，处分所得应转交委托人。"
        else:
            conclusion = "行纪人未取得委托人同意且能够联系委托人时擅自处分委托物，不合规；造成损失的应承担赔偿责任。"
        return _format_commission_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("提存权")
    if facts.deposit_claim or facts.refuse_accept or facts.refuse_take_back:
        triggered.append(config.patch_name("J6", "行纪人提存权的行使"))
        major = "《民法典》第957条规定，行纪人按约定买入委托物后，委托人经催告无正当理由拒绝受领的，行纪人可以提存；委托物不能卖出或委托人撤回出售，经催告后委托人不取回或不处分的，行纪人也可以提存。"
        minor = "识别到委托人拒绝受领、拒绝取回或不处分委托物，行纪人主张提存。"
        can_deposit = facts.urged and ((facts.buy_in and facts.refuse_accept) or ((facts.cannot_sell or facts.withdraw_sale) and facts.refuse_take_back))
        conclusion = "行纪人提存权成立，可以依法提存委托物。" if can_deposit else "行纪人提存权暂不成立，需要先证明已催告且委托人无正当理由拒绝受领、取回或处分。"
        return _format_commission_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("报酬与留置权")
    if (facts.remuneration_claim or facts.remuneration_unclear) and not (facts.remuneration_unpaid or facts.lien_claim):
        triggered.append(config.patch_name("J11", "行纪合同报酬的确定"))
        major = "《民法典》第959条规定，行纪人完成或者部分完成委托事务的，委托人应当向其支付相应报酬。"
        minor = "识别到行纪人请求报酬，或双方对报酬标准约定不明。"
        if facts.matter_completed and facts.remuneration_agreed:
            conclusion = "行纪人已完成或部分完成委托事务，报酬按约定支付。"
        elif facts.matter_completed:
            conclusion = "行纪人已完成或部分完成委托事务，报酬约定不明的，可按交易习惯或公平原则酌情确定。"
        else:
            conclusion = "未识别到行纪人完成或部分完成委托事务，暂不支持报酬请求。"
        return _format_commission_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.remuneration_unpaid or facts.lien_claim:
        triggered.append(config.patch_name("J5", "行纪人留置权的行使"))
        major = "《民法典》第959条规定，委托人逾期不支付报酬的，行纪人对委托物享有留置权，但是当事人另有约定的除外。"
        minor = "识别到委托人逾期未支付报酬，行纪人主张留置委托物。"
        if facts.lien_excluded:
            conclusion = "合同另有约定排除留置权，行纪人不得留置委托物。"
        elif facts.matter_completed:
            conclusion = "行纪人已完成或部分完成委托事务且委托人逾期不支付报酬，行纪人留置权成立。"
        else:
            conclusion = "未识别到行纪人完成或部分完成委托事务，留置权暂不成立。"
        return _format_commission_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("合同解除")
    if facts.termination_request:
        triggered.append(config.patch_name("J13", "行纪合同的任意解除权"))
        major = "《民法典》第960条规定，行纪合同章没有规定的，参照适用委托合同的有关规定；第933条规定，委托人或者受托人可以随时解除委托合同。"
        minor = "识别到委托人或行纪人主张解除行纪合同。"
        if facts.termination_loss and facts.paid_commission:
            conclusion = f"行纪合同解除有效；有偿行纪造成损失的，赔偿范围包括直接损失和合同履行后可以获得的利益，已识别金额为 {_money(facts.actual_loss)}。"
        elif facts.termination_loss:
            conclusion = f"行纪合同解除有效；解除时间不当造成损失的，赔偿范围为直接损失，已识别金额为 {_money(facts.actual_loss)}。"
        else:
            conclusion = "行纪合同解除有效；未识别到解除造成损失，暂不支持损失赔偿。"
        return _format_commission_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.commission_agency_contract:
        major = "《民法典》第951条至第960条规定，行纪合同裁判应围绕行纪人是否以自己名义从事贸易活动、是否遵守委托人指示、第三人是否履行义务、报酬和委托物处理等事实进行审查。"
        minor = "已识别行纪合同关系，但未稳定识别足以触发价格指示、第三人违约、保管、处分、提存、报酬、留置或解除的具体争议事实。"
        conclusion = "事实要素不足，需要补充交易名义、价格指示、第三人履行情况、委托物状态、报酬支付或解除损失后再裁判。"
        return _format_commission_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    major = "行纪合同纠纷应围绕行纪人是否以自己名义为委托人从事贸易活动，以及第三人交易、价格指示、报酬、留置、提存和委托物保管等事项审查。"
    minor = "自然语言事实未能稳定识别出行纪合同关系和关键争议节点。"
    conclusion = "事实要素不足，需要补充是否存在行纪合同关系、交易相对方、交易名义、报酬约定、第三人履行情况和损失金额后再裁判。"
    return _format_commission_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
