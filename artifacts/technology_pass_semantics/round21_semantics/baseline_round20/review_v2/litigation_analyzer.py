"""诉讼策略分析模块。

对审查报告中标记为高风险和中风险的条款，输出三层分析：
1. 证据缺口清单（红色=缺了几乎必输，黄色=建议补充，绿色=证据充分）
2. 法院裁量预测（合同约定 vs 法院大概率支持，附法律依据）
3. 成本收益评估（诉讼费估算、时间成本、综合建议）

约束：
- 不输出绝对胜诉/败诉结论，使用概率性表述
- 所有裁量预测必须引用具体法律条文
- 保留免责声明
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from review_v2.user_profile import UserRiskProfile

# ---------------------------------------------------------------------------
# 免责声明
# ---------------------------------------------------------------------------

LITIGATION_DISCLAIMER = (
    "本分析基于合同文本和通用法律规则生成，不构成法律意见，不替代律师的专业判断。"
    "实际诉讼结果受证据、法官自由裁量、地方司法实践等多重因素影响，仅供参考。"
)

# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------


@dataclass
class EvidenceGap:
    evidence_name: str
    severity: str  # critical / recommended / sufficient
    description: str
    source_hint: str = ""


@dataclass
class CourtPrediction:
    contract_terms: str
    likely_court_view: str
    legal_basis: str
    amount_range: str = ""
    reference_cases: str = ""


@dataclass
class CostBenefit:
    dispute_amount: float = 0.0
    litigation_fee: float = 0.0
    time_cost: str = ""
    enforcement_risk: str = ""
    recommendation: str = ""
    recommendation_reason: str = ""


@dataclass
class LitigationAnalysisItem:
    item_id: str
    title: str
    risk_level: str
    evidence_gaps: List[EvidenceGap] = field(default_factory=list)
    court_prediction: Optional[CourtPrediction] = None
    cost_benefit: Optional[CostBenefit] = None

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "title": self.title,
            "risk_level": self.risk_level,
            "evidence_gaps": [
                {
                    "evidence_name": e.evidence_name,
                    "severity": e.severity,
                    "description": e.description,
                    "source_hint": e.source_hint,
                }
                for e in self.evidence_gaps
            ],
            "court_prediction": {
                "contract_terms": self.court_prediction.contract_terms,
                "likely_court_view": self.court_prediction.likely_court_view,
                "legal_basis": self.court_prediction.legal_basis,
                "amount_range": self.court_prediction.amount_range,
                "reference_cases": self.court_prediction.reference_cases,
            } if self.court_prediction else None,
            "cost_benefit": {
                "dispute_amount": self.cost_benefit.dispute_amount,
                "litigation_fee": self.cost_benefit.litigation_fee,
                "time_cost": self.cost_benefit.time_cost,
                "enforcement_risk": self.cost_benefit.enforcement_risk,
                "recommendation": self.cost_benefit.recommendation,
                "recommendation_reason": self.cost_benefit.recommendation_reason,
            } if self.cost_benefit else None,
        }


@dataclass
class LitigationReport:
    disclaimer: str
    items: List[LitigationAnalysisItem]
    summary: Dict[str, int]

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "disclaimer": self.disclaimer,
            "items": [item.to_public_dict() for item in self.items],
            "summary": self.summary,
        }


# ---------------------------------------------------------------------------
# 证据缺口分析
# ---------------------------------------------------------------------------

CRITICAL_EVIDENCE_MAP = {
    "违约金": [
        EvidenceGap("合同原件/复印件", "critical", "无合同则无法证明违约金约定存在", "保存签约原件，拍照或扫描备份"),
        EvidenceGap("违约事实证明材料", "critical", "需证明对方确实存在违约行为", "催告函、违约通知、聊天记录、录音录像"),
        EvidenceGap("实际损失计算凭证", "recommended", "违约金过高时对方可能主张调减，需证明实际损失", "付款凭证、评估报告、市场比价"),
        EvidenceGap("催告履行通知", "recommended", "证明已给予对方合理履行期限", "挂号信回执、快递单、微信/邮件催告记录"),
    ],
    "押金": [
        EvidenceGap("押金支付凭证", "critical", "无凭证则无法证明押金金额和支付事实", "银行转账记录、微信/支付宝转账截图、收据"),
        EvidenceGap("房屋/物品交接清单", "recommended", "需证明入住/交付时的原始状态", "交接清单、照片、视频、第三方验房报告"),
        EvidenceGap("损坏/欠费证据", "critical", "如主张扣除押金，需证明损坏或欠费事实", "维修报价单、维修发票、物业费/水电费欠费单"),
        EvidenceGap("退还催告记录", "recommended", "证明已催告对方退还押金", "微信/短信/邮件催告记录、律师函"),
    ],
    "租金": [
        EvidenceGap("租金支付凭证", "critical", "需证明已支付租金或对方未支付租金", "银行流水、转账记录、收据"),
        EvidenceGap("欠租催告通知", "recommended", "证明已催告支付，触发解除权或违约责任", "挂号信回执、快递单、微信/邮件通知"),
    ],
    "解除": [
        EvidenceGap("解除通知及送达证明", "critical", "解除合同需通知对方，无法证明送达则解除不生效", "挂号信回执、快递单、微信/邮件、律师函"),
        EvidenceGap("解除事由证据", "critical", "需证明符合约定或法定解除条件", "违约证据、不可抗力证明、协商记录"),
    ],
    "赔偿": [
        EvidenceGap("损失计算明细", "critical", "无损失证据则法院难以支持赔偿请求", "发票、付款凭证、评估报告、市场价证明"),
        EvidenceGap("因果关系证明", "recommended", "需证明损失由对方违约/侵权直接造成", "专家意见、鉴定报告、证人证言"),
    ],
    "退费": [
        EvidenceGap("付款凭证", "critical", "无凭证则无法证明付款金额和时间", "转账记录、收据、刷卡单"),
        EvidenceGap("未提供服务证明", "critical", "需证明对方未按约提供服务", "服务记录、签到表、课程记录、聊天记录"),
        EvidenceGap("退费申请记录", "recommended", "证明已按合同约定提出退费申请", "微信/邮件/书面申请记录"),
    ],
    "服务": [
        EvidenceGap("服务合同/协议原件", "critical", "无合同则无法确定服务内容、标准和费用", "保存签约原件"),
        EvidenceGap("服务履行记录", "recommended", "需证明服务是否按约提供", "签到表、服务报告、照片、视频、微信记录"),
        EvidenceGap("沟通记录", "recommended", "证明双方就服务质量、变更、投诉的沟通过程", "微信/邮件/短信/书面函件"),
    ],
}


def _match_evidence_category(title: str) -> Optional[str]:
    for category in ("违约金", "押金", "租金", "解除", "赔偿", "退费", "服务"):
        if category in title:
            return category
    return None


def _build_evidence_gaps(title: str, coverage_status: str, issue_type: str) -> List[EvidenceGap]:
    category = _match_evidence_category(title)
    if category is None:
        return [
            EvidenceGap("合同原件/复印件", "critical", "诉讼的基本依据，缺失则无法证明权利义务关系", "保存签约原件并扫描备份"),
            EvidenceGap("履约过程记录", "recommended", "证明双方履约情况的关键证据", "微信记录、邮件往来、付款凭证、照片视频"),
            EvidenceGap("身份信息", "recommended", "需明确被告姓名/名称、住所、联系方式", "合同签署栏、营业执照查询、身份证复印件"),
        ]

    template = CRITICAL_EVIDENCE_MAP.get(category, [])
    result: List[EvidenceGap] = []

    for gap in template:
        if coverage_status in ("通过", "已覆盖") and gap.severity == "recommended":
            result.append(EvidenceGap(
                evidence_name=gap.evidence_name,
                severity="sufficient",
                description=f"合同已覆盖相关内容，{gap.description}",
                source_hint=gap.source_hint,
            ))
        else:
            result.append(gap)

    if coverage_status == "缺失" and not any(g.evidence_name == "合同原件/复印件" for g in result):
        result.insert(0, EvidenceGap(
            "合同原件/复印件",
            "critical",
            "条款完全缺失，如无法提供完整合同文本，诉讼基础将极为薄弱",
            "查找并保存签约时所有文件",
        ))

    return result


# ---------------------------------------------------------------------------
# 法院裁量预测
# ---------------------------------------------------------------------------

COURT_PREDICTION_RULES = {
    "HL-039": {
        "legal_basis": "《民法典》第585条（违约金调整）、《民法典合同编司法解释》第65条",
        "prediction": (
            "合同约定的违约金为{contract_terms}。法院在审理违约金争议时，以实际损失为基础，"
            "兼顾合同履行情况、当事人过错程度和预期利益等综合因素，根据公平原则和诚实信用原则衡量。"
            "如违约金过分高于实际损失（通常超过损失的30%），法院大概率会调减。"
        ),
        "amount": "调减后的违约金一般在实际损失的100%-130%之间。如合同约定违约金为{amount}元，在损失为{loss}元的情况下，法院大概率支持{range_low}-{range_high}元。",
        "reference": "参考《民法典合同编司法解释》第65条：当事人主张约定的违约金过高请求适当减少的，应当以实际损失为基础，兼顾合同的履行情况、当事人的过错程度以及预期利益等综合因素，根据公平原则和诚实信用原则予以衡量。",
    },
    "HL-014": {
        "legal_basis": "《民法典》第714条（承租人妥善保管义务）、第711条（按约定使用）",
        "prediction": (
            "押金返还争议的核心在于：承租人是否存在损坏、欠费或违约行为。"
            "出租人主张扣除押金的，需承担举证责任。如无法证明损坏系承租人造成或无法证明维修费用的合理性，"
            "法院大概率支持全额退还押金。"
        ),
        "amount": "如押金为{amount}元，出租人主张扣除{deduct}元维修费但仅有报价单无发票的，法院大概率支持退还押金{range_low}-{range_high}元。",
        "reference": "参考《民法典》第714条：承租人应当妥善保管租赁物，因保管不善造成租赁物毁损、灭失的，应当承担赔偿责任。举证责任由主张损害赔偿的一方承担。",
    },
    "HL-015": {
        "legal_basis": "《民法典》第563条（合同解除）、第722条（承租人逾期支付租金）",
        "prediction": (
            "承租人逾期不支付租金的，出租人可催告后在合理期限内解除合同。"
            "如合同明确约定逾期天数（如1个月）即构成解除事由，且出租人已履行催告义务，"
            "法院大概率支持解除合同。"
        ),
        "amount": "",
        "reference": "参考《民法典》第722条：承租人无正当理由未支付或者迟延支付租金的，出租人可以请求承租人在合理期限内支付；承租人逾期不支付的，出租人可以解除合同。",
    },
    "HL-016": {
        "legal_basis": "《民法典》第712条（出租人维修义务）、第713条（维修费用承担）",
        "prediction": (
            "出租人应履行租赁物的维修义务。如出租人未在合理期限内维修，承租人自行维修的，"
            "维修费用由出租人承担。但承租人需保留维修通知、维修必要性和费用合理性证明。"
        ),
        "amount": "",
        "reference": "参考《民法典》第713条：承租人在租赁物需要维修时可以请求出租人在合理期限内维修。出租人未履行维修义务的，承租人可以自行维修，费用由出租人负担。",
    },
    "S-06-03": {
        "legal_basis": "《民法典》第582条（质量瑕疵救济）、第610条（根本违约）",
        "prediction": (
            "出卖人交付的标的物不符合质量要求的，买受人可合理选择请求修理、更换、重作、退货或减少价款。"
            "如质量问题严重影响合同目的实现，买受人可解除合同。"
        ),
        "amount": "",
        "reference": "参考《民法典》第582条：履行不符合约定的，应当按照当事人的约定承担违约责任。对违约责任没有约定或约定不明确的，受损害方根据标的的性质以及损失的大小，可以合理选择请求对方承担修理、重作、更换、退货、减少价款或者报酬等违约责任。",
    },
    "S-08-02": {
        "legal_basis": "《民法典》第585条（违约金调整）",
        "prediction": "买卖合同中的违约金条款受《民法典》第585条调整。如约定违约金明显超出实际损失，法院大概率支持调减。",
        "amount": "如合同约定违约金为{amount}元，在未证明实际损失超过{loss}元的情况下，法院大概率支持违约金{range_low}-{range_high}元。",
        "reference": "参考《民法典合同编司法解释》第65条。",
    },
    "SVC-04-03": {
        "legal_basis": "《消费者权益保护法》第53条（预付式消费退款）、《预付式消费司法解释》第13条",
        "prediction": (
            "预付式消费中，经营者未按约提供服务或停业的，消费者有权要求退还预付款余额。"
            "如合同约定的退费条件明显不合理（如概不退款），法院大概率认定该格式条款无效，"
            "支持按未消费比例退费。"
        ),
        "amount": "预付款为{amount}元，已消费{used}元，剩余{remain}元。如经营者违约停业，法院大概率支持全额退还剩余{remain}元。",
        "reference": "参考《消费者权益保护法》第53条：经营者以预收款方式提供商品或者服务的，应当按照约定提供。未按照约定提供的，应当按照消费者的要求履行约定或者退回预付款。",
    },
}


def _build_court_prediction(
    item_id: str, title: str, risk_point: str, suggested_clause: str, legal_basis: str
) -> CourtPrediction:
    rule = COURT_PREDICTION_RULES.get(item_id)
    if rule is None:
        for pid, r in COURT_PREDICTION_RULES.items():
            kw = r.get("title_keyword", "")
            if kw and kw in title:
                rule = r
                break

    if rule is None:
        return CourtPrediction(
            contract_terms=f"合同约定的{title}相关条款",
            likely_court_view=(
                f"关于{title}的争议，法院将根据《民法典》合同编的相关规定，"
                "结合合同约定、履约情况、双方过错和实际损失综合判断。"
                "如条款约定不明确，法院将按照通常交易习惯和诚信原则填补合同漏洞。"
            ),
            legal_basis=legal_basis or "《民法典》第509条（合同履行）、第577条（违约责任）",
        )

    prediction = rule["prediction"].format(
        contract_terms=suggested_clause or f"合同约定的{title}相关条款",
        amount="[争议金额]",
        loss="[实际损失]",
        range_low="[下限]",
        range_high="[上限]",
        deduct="[扣除金额]",
        used="[已消费金额]",
        remain="[剩余金额]",
    )
    amount_range = ""
    if rule.get("amount"):
        amount_range = rule["amount"].format(
            amount="[争议金额]",
            loss="[实际损失]",
            range_low="[下限]",
            range_high="[上限]",
            deduct="[扣除金额]",
            used="[已消费金额]",
            remain="[剩余金额]",
        )

    return CourtPrediction(
        contract_terms=suggested_clause or f"合同约定的{title}相关条款",
        likely_court_view=prediction,
        legal_basis=rule["legal_basis"],
        amount_range=amount_range,
        reference_cases=rule.get("reference", ""),
    )


# ---------------------------------------------------------------------------
# 成本收益评估
# ---------------------------------------------------------------------------

def _estimate_litigation_fee(dispute_amount: float) -> float:
    if dispute_amount <= 0:
        return 50.0
    if dispute_amount <= 10000:
        return 50.0
    if dispute_amount <= 100000:
        return dispute_amount * 0.025
    if dispute_amount <= 200000:
        return dispute_amount * 0.02
    if dispute_amount <= 500000:
        return dispute_amount * 0.015
    if dispute_amount <= 1000000:
        return dispute_amount * 0.01
    if dispute_amount <= 2000000:
        return dispute_amount * 0.009
    if dispute_amount <= 5000000:
        return dispute_amount * 0.008
    return dispute_amount * 0.007


def _extract_dispute_amount(title: str, risk_point: str) -> float:
    patterns = [
        r"(\d[\d,.]*)\s*元",
        r"(\d[\d,.]*)\s*万",
    ]
    for pattern in patterns:
        match = re.search(pattern, risk_point)
        if match:
            try:
                amount = float(match.group(1).replace(",", ""))
                if "万" in risk_point[match.start():match.end()]:
                    amount *= 10000
                return amount
            except ValueError:
                pass

    amount_map = {
        "押金": 10000.0,
        "租金": 30000.0,
        "违约金": 50000.0,
        "赔偿": 80000.0,
        "退费": 15000.0,
        "解除": 50000.0,
    }
    for keyword, amount in amount_map.items():
        if keyword in title:
            return amount

    return 30000.0


def _build_cost_benefit(title: str, risk_point: str, profile: UserRiskProfile) -> CostBenefit:
    dispute_amount = _extract_dispute_amount(title, risk_point)
    fee = _estimate_litigation_fee(dispute_amount)

    if dispute_amount <= 50000:
        time_cost = f"争议金额较小（约{dispute_amount:.0f}元），法院大概率适用简易程序，审理期限约3个月。"
    else:
        time_cost = f"争议金额约{dispute_amount:.0f}元，可能适用普通程序，审理期限约6个月，含举证期、答辩期和可能的鉴定期间。"

    if profile.bargaining_position == "弱势方":
        enforcement_risk = "对方为强势方，可能存在转移资产、拖延执行风险。建议申请财产保全。"
    elif profile.bargaining_position == "强势方":
        enforcement_risk = "己方为强势方，胜诉后执行难度相对较低。"
    else:
        enforcement_risk = "执行风险中等，建议关注对方经营状况和资产情况。"

    fee_ratio = fee / dispute_amount if dispute_amount > 0 else 1.0
    # 保守用户：倾向于诉讼维权，门槛低
    if profile.risk_appetite == "保守":
        if dispute_amount >= 20000 and fee_ratio < 0.10:
            recommendation = "建议起诉"
            reason = f"争议金额{dispute_amount:.0f}元，诉讼费约{fee:.0f}元（{fee_ratio:.1%}），金额较大值得通过诉讼维护权益。"
        elif dispute_amount >= 10000:
            recommendation = "建议协商"
            reason = f"争议金额{dispute_amount:.0f}元，建议先发律师函协商，协商不成可考虑起诉（诉讼费约{fee:.0f}元）。"
        else:
            recommendation = "建议协商"
            reason = f"争议金额较小（{dispute_amount:.0f}元），建议协商解决以节约时间和精力。"
    # 激进用户：更关注性价比，门槛高
    elif profile.risk_appetite == "激进":
        if dispute_amount >= 80000 and fee_ratio < 0.05:
            recommendation = "建议起诉"
            reason = f"争议金额{dispute_amount:.0f}元，诉讼费约{fee:.0f}元（{fee_ratio:.1%}），预期收益远超成本，建议起诉。"
        elif dispute_amount >= 30000:
            recommendation = "建议协商"
            reason = f"争议金额{dispute_amount:.0f}元，诉讼费约{fee:.0f}元，建议通过协商或调解解决以节约时间和费用。"
        else:
            recommendation = "不建议起诉"
            reason = f"争议金额较小（{dispute_amount:.0f}元），投入产出比不佳，建议优先协商解决。"
    # 标准用户
    else:
        if dispute_amount >= 50000 and fee_ratio < 0.08:
            recommendation = "建议起诉"
            reason = f"争议金额{dispute_amount:.0f}元，诉讼费约{fee:.0f}元（{fee_ratio:.1%}），合同约定较明确，胜诉概率较高。"
        elif dispute_amount >= 15000:
            recommendation = "建议协商"
            reason = f"争议金额{dispute_amount:.0f}元，诉讼费约{fee:.0f}元，建议在律师函或调解阶段解决。"
        else:
            recommendation = "不建议起诉"
            reason = f"争议金额较小（{dispute_amount:.0f}元），通过协商或调解解决更为经济。"

    return CostBenefit(
        dispute_amount=dispute_amount,
        litigation_fee=fee,
        time_cost=time_cost,
        enforcement_risk=enforcement_risk,
        recommendation=recommendation,
        recommendation_reason=reason,
    )


# ---------------------------------------------------------------------------
# 主分析函数
# ---------------------------------------------------------------------------


def analyze_litigation_strategy(
    review_items: List[Dict[str, Any]],
    profile: UserRiskProfile,
) -> LitigationReport:
    target_items = [item for item in review_items if item.get("risk_level") in ("高", "中")]
    results: List[LitigationAnalysisItem] = []

    for item in target_items:
        title = item.get("title", "")
        item_id = item.get("item_id", "")
        risk_level = item.get("risk_level", "中")
        risk_point = item.get("risk_point_description", "")
        suggested_clause = item.get("suggested_clause_example", "")
        legal_basis = item.get("legal_basis_index", "")
        coverage_status = item.get("coverage_status", "")
        issue_type = item.get("issue_type", "")

        evidence_gaps = _build_evidence_gaps(title, coverage_status, issue_type)
        court_prediction = _build_court_prediction(item_id, title, risk_point, suggested_clause, legal_basis)
        cost_benefit = _build_cost_benefit(title, risk_point, profile)

        results.append(LitigationAnalysisItem(
            item_id=item_id, title=title, risk_level=risk_level,
            evidence_gaps=evidence_gaps, court_prediction=court_prediction, cost_benefit=cost_benefit,
        ))

    summary = {
        "建议起诉": sum(1 for r in results if r.cost_benefit and r.cost_benefit.recommendation == "建议起诉"),
        "建议协商": sum(1 for r in results if r.cost_benefit and r.cost_benefit.recommendation == "建议协商"),
        "不建议起诉": sum(1 for r in results if r.cost_benefit and r.cost_benefit.recommendation == "不建议起诉"),
    }
    return LitigationReport(disclaimer=LITIGATION_DISCLAIMER, items=results, summary=summary)


def format_litigation_markdown(report: LitigationReport) -> str:
    lines = [
        "# 诉讼策略分析",
        "",
        f"> {report.disclaimer}",
        "",
        "---",
        "",
        "## 综合建议总览",
        "",
        f"- **建议起诉**：{report.summary['建议起诉']} 项",
        f"- **建议协商**：{report.summary['建议协商']} 项",
        f"- **不建议起诉**：{report.summary['不建议起诉']} 项",
        "",
        "---",
        "",
    ]

    for index, item in enumerate(report.items, start=1):
        lines.append(f"## {index}. {item.title}（{item.item_id}）")
        lines.append(f"风险等级：{item.risk_level}")
        lines.append("")

        lines.append("### 证据缺口清单")
        critical_gaps = [g for g in item.evidence_gaps if g.severity == "critical"]
        recommended_gaps = [g for g in item.evidence_gaps if g.severity == "recommended"]
        sufficient_gaps = [g for g in item.evidence_gaps if g.severity == "sufficient"]

        if critical_gaps:
            lines.append("")
            lines.append("#### 缺了几乎必输")
            for gap in critical_gaps:
                lines.append(f"- **{gap.evidence_name}**：{gap.description}")
                if gap.source_hint:
                    lines.append(f"  > 获取方式：{gap.source_hint}")

        if recommended_gaps:
            lines.append("")
            lines.append("#### 建议补充")
            for gap in recommended_gaps:
                lines.append(f"- **{gap.evidence_name}**：{gap.description}")
                if gap.source_hint:
                    lines.append(f"  > 获取方式：{gap.source_hint}")

        if sufficient_gaps:
            lines.append("")
            lines.append("#### 证据充分")
            for gap in sufficient_gaps:
                lines.append(f"- {gap.evidence_name}：{gap.description}")

        lines.append("")

        if item.court_prediction:
            lines.append("### 法院裁量预测")
            lines.append(f"- **合同约定**：{item.court_prediction.contract_terms}")
            lines.append(f"- **法院大概率支持**：{item.court_prediction.likely_court_view}")
            lines.append(f"- **法律依据**：{item.court_prediction.legal_basis}")
            if item.court_prediction.amount_range:
                lines.append(f"- **可执行金额范围**：{item.court_prediction.amount_range}")
            if item.court_prediction.reference_cases:
                lines.append(f"- **参考判例/解释**：{item.court_prediction.reference_cases}")
            lines.append("")

        if item.cost_benefit:
            lines.append("### 成本收益评估")
            cb = item.cost_benefit
            lines.append(f"- **争议金额**：约{cb.dispute_amount:.0f}元")
            lines.append(f"- **预估诉讼费**：约{cb.litigation_fee:.0f}元")
            lines.append(f"- **时间成本**：{cb.time_cost}")
            lines.append(f"- **执行风险**：{cb.enforcement_risk}")
            lines.append(f"- **综合建议**：**{cb.recommendation}**")
            lines.append(f"  > {cb.recommendation_reason}")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)
