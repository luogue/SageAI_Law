"""Additive leaves in the existing domain -> subtype -> checklist hierarchy."""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class PriorityContractType:
    name: str
    family: str
    subject: str
    titles: tuple[str, ...]
    signals: tuple[str, ...]


PRIORITY_TYPES = {
    "labor": PriorityContractType("劳动合同", "EMPLOYMENT", "LABOR", ("劳动合同", "劳动用工合同"), ("用人单位", "劳动者", "工资", "工作岗位", "社会保险")),
    "non_compete": PriorityContractType("竞业限制协议", "EMPLOYMENT", "LABOR", ("竞业限制协议", "竞业禁止协议"), ("用人单位", "劳动者", "离职", "竞业限制", "经济补偿")),
    "confidentiality": PriorityContractType("保密协议", "EMPLOYMENT", "CONFIDENTIAL_INFORMATION", ("保密协议", "保密合同"), ("披露方", "接收方", "保密信息", "商业秘密", "保密义务")),
    "employment_termination": PriorityContractType("劳动关系解除/终止协议", "EMPLOYMENT", "LABOR", ("劳动关系解除/终止协议", "解除劳动合同协议", "劳动合同解除协议", "劳动关系解除协议", "劳动关系终止协议", "终止劳动合同协议", "解除劳动关系协议", "解除/终止劳动合同协议"), ("用人单位", "劳动者", "解除", "终止", "经济补偿")),
    "mortgage": PriorityContractType("抵押合同", "SECURITY_PROPERTY", "COLLATERAL", ("抵押合同", "最高额抵押合同"), ("抵押人", "抵押权人", "抵押财产", "主债权", "抵押登记")),
    "movable_pledge": PriorityContractType("动产质押合同", "SECURITY_PROPERTY", "MOVABLE", ("动产质押合同", "质押合同"), ("出质人", "质权人", "质物", "交付", "动产")),
    "equity_pledge": PriorityContractType("股权质押合同", "SECURITY_PROPERTY", "EQUITY", ("股权质押合同", "股权质押协议", "股权出质合同"), ("出质人", "质权人", "股权", "出质登记", "目标公司")),
    "rights_pledge": PriorityContractType("应收账款等权利质押合同", "SECURITY_PROPERTY", "RECEIVABLES_OR_RIGHTS", ("应收账款等权利质押合同", "应收账款质押合同", "权利质押合同", "应收账款质押协议"), ("出质人", "质权人", "应收账款", "权利凭证", "质押登记")),
    "equity_transfer": PriorityContractType("股权转让协议", "EQUITY_INVESTMENT", "EQUITY", ("股权转让协议", "股权转让合同"), ("转让方", "受让方", "股权", "目标公司", "转让价款")),
    "capital_increase": PriorityContractType("增资扩股协议", "EQUITY_INVESTMENT", "EQUITY", ("增资扩股协议", "增资协议", "增资扩股合同"), ("投资方", "新增注册资本", "增资", "目标公司", "认缴")),
    "investment": PriorityContractType("投资协议", "EQUITY_INVESTMENT", "EQUITY", ("投资协议", "股权投资协议", "投资合同"), ("投资方", "目标公司", "股权", "估值", "交割")),
    "shareholders": PriorityContractType("股东合作协议", "EQUITY_INVESTMENT", "EQUITY", ("股东协议", "股东合作协议", "入股合作协议", "共同投资设立公司协议", "公司设立协议", "共同出资协议"), ("股东", "表决权", "董事会", "公司治理", "退出")),
}


def classify_priority_contract(text, clauses):
    """A document heading is strong; incidental annex titles never override it.

    Without a title require three distinct transaction signals. Bare generic
    '质押合同' needs asset evidence to distinguish movable and rights pledges.
    """
    heading = next((line.strip() for line in text.splitlines() if line.strip()), "")[:100]
    heading = re.split(r"[。；]", heading)[0]
    # A completed employment relationship, not an incidental future exit clause.
    exit_heading = re.search(r'(?:解除|终止)(?:或|和|及|/)?(?:终止|解除)?劳动(?:合同|关系).*协议|劳动(?:合同|关系).*(?:解除|终止).*协议|离职(?:结算)?协议', heading)
    exit_purpose = re.search(r'(?:现经|现因|双方同意|双方协商)[^。]{0,100}(?:就解除|就终止|协商解除|协商终止)[^。]{0,50}(?:协议|一致)', text[:700])
    if exit_heading or (exit_purpose and sum(s in text for s in ('工作交接', '经济补偿', '离职证明', '解除劳动合同证明')) >= 2):
        return 'employment_termination', 'high', '本协议以结束劳动关系及离职结算为主要目的'
    candidates = []
    for key, meta in PRIORITY_TYPES.items():
        title = max((t for t in meta.titles if t in heading), key=len, default="")
        if title:
            candidates.append((len(title), key, title))
    if candidates:
        _, key, title = max(candidates)
        if title == "质押合同":
            if "股权" in text:
                key = "equity_pledge"
            elif re.search(r"应收账款|权利凭证|知识产权|票据", text):
                key = "rights_pledge"
        return key, "high", title
    # Existing named main transactions win over their ancillary obligations.
    if re.search(r"合同|协议", heading):
        return None
    scored = []
    for key, meta in PRIORITY_TYPES.items():
        # Secrecy topics are common ancillary duties in every transaction.
        # Without an agreement heading, require the disclosure relationship,
        # rather than letting three generic secrecy words replace the main type.
        if key == "confidentiality" and not all(role in text for role in ("披露方", "接收方")):
            continue
        scored.append((sum(s in text for s in meta.signals), key))
    scored.sort(reverse=True)
    if scored[0][0] >= 3 and scored[0][0] - scored[1][0] >= 2:
        return scored[0][1], "high", "、".join(s for s in PRIORITY_TYPES[scored[0][1]].signals if s in text)
    return None
