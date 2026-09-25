"""跨地域裁判预判模块。

对审查报告中标记为高风险和中风险的条款，结合用户所在地法院的司法实践，
给出地域裁判倾向分析和起诉建议。

数据来源：
- 各省高院发布的审判指导意见/会议纪要（真实规则）
- 最高人民法院司法解释
- 判例案号为占位标注，待接入真实裁判文书数据库后替换

约束：
- 不输出绝对结论，使用倾向性表述
- 无数据时明确标注
- 保留免责声明
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from review_v2.user_profile import UserRiskProfile

# ---------------------------------------------------------------------------
# 免责声明
# ---------------------------------------------------------------------------

JURISDICTION_DISCLAIMER = (
    "本分析基于各省高院公开的审判指导意见和最高人民法院司法解释生成。"
    "判例案号为占位标注，不代表真实已决案件。实际裁判结果受个案事实、"
    "证据情况和法官自由裁量影响，本分析不构成法律意见，仅供参考。"
)

# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------


@dataclass
class JurisdictionCase:
    """本地判例引用（占位数据，待接入真实数据库）。"""

    case_id: str  # 案号（占位）
    court: str  # 审理法院
    conclusion: str  # 核心结论
    relevance: str  # 与本案的关联说明


@dataclass
class JurisdictionItem:
    """单条条款的地域裁判预判。"""

    item_id: str
    title: str
    risk_level: str
    # 本地法院倾向
    local_court_tendency: str
    # 法律基础（地域裁量差异的来源）
    legal_basis: str
    # 本地判例参考（2-3个）
    local_cases: List[JurisdictionCase]
    # 起诉建议
    litigation_recommendation: str  # 建议起诉/建议协商/不建议起诉
    recommendation_reason: str
    # 管辖策略提示
    jurisdiction_strategy: str = ""
    # 数据来源说明
    data_source_note: str = ""

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "title": self.title,
            "risk_level": self.risk_level,
            "local_court_tendency": self.local_court_tendency,
            "legal_basis": self.legal_basis,
            "local_cases": [
                {
                    "case_id": c.case_id,
                    "court": c.court,
                    "conclusion": c.conclusion,
                    "relevance": c.relevance,
                }
                for c in self.local_cases
            ],
            "litigation_recommendation": self.litigation_recommendation,
            "recommendation_reason": self.recommendation_reason,
            "jurisdiction_strategy": self.jurisdiction_strategy,
            "data_source_note": self.data_source_note,
        }


@dataclass
class JurisdictionReport:
    """完整跨地域裁判预判报告。"""

    disclaimer: str
    jurisdiction: str  # 用户所在地
    items: List[JurisdictionItem]
    # 整体地域环境评估
    environment_assessment: str
    # 管辖策略总结
    jurisdiction_strategy_summary: str

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "disclaimer": self.disclaimer,
            "jurisdiction": self.jurisdiction,
            "items": [item.to_public_dict() for item in self.items],
            "environment_assessment": self.environment_assessment,
            "jurisdiction_strategy_summary": self.jurisdiction_strategy_summary,
        }


# ---------------------------------------------------------------------------
# 地域裁判规则库
# ---------------------------------------------------------------------------

# 各省高院/主要城市法院的通用裁判倾向
# 数据来源：《各省高院关于审理合同纠纷案件的指导意见》、最高人民法院司法解释

REGIONAL_TENDENCIES = {
    "北京": {
        "label": "北京法院",
        "style": "北京法院注重合同文义解释和格式条款的提示说明义务，对格式条款的审查较为严格。",
        "rules": {
            "违约金": "北京法院通常尊重合同约定的违约金条款，但如违约金明显过高（超过实际损失30%），会依据《民法典》第585条予以调减。北京市高级人民法院《关于审理房屋租赁合同纠纷案件若干问题的指导意见》指出，违约金调减以实际损失为基础。",
            "押金": "北京法院对押金返还争议持保护承租人立场，出租人主张扣减押金需承担举证责任。北京法院通常要求出租人提供维修发票或第三方评估报告，仅凭报价单不足以支持扣减。",
            "解除": "北京法院对出租人解除权的审查较严，要求催告程序完整且解除通知有效送达。如出租人未履行催告义务直接解除，法院通常不予支持。",
            "赔偿": "北京法院对损失赔偿的证明标准较高，要求原告提供完整的损失计算依据和因果关系证明。间接损失和预期利益损失的支持率相对较低。",
            "管辖": "北京法院对格式管辖条款的审查趋严。如管辖条款约定在对方所在地且对消费者明显不便，法院可能认定该条款无效，适用法定管辖。",
            "服务": "北京法院对预付式消费的保护力度较强。北京市第三中级人民法院在多个判例中支持消费者按未消费比例退费，并认定概不退款格式条款无效。",
        },
    },
    "上海": {
        "label": "上海法院",
        "style": "上海法院注重合同自由和市场交易效率，倾向于尊重商业主体的自主约定，同时兼顾公平原则。",
        "rules": {
            "违约金": "上海法院在违约金调整上相对克制，对商事主体间的违约金条款通常予以尊重。上海市高级人民法院《关于审理合同纠纷案件若干问题的解答》指出，商事合同中约定的违约金一般不予调整，除非明显违反公平原则。",
            "押金": "上海法院对押金条款倾向于按合同约定处理，但对出租人扣减押金的举证要求与北京类似。上海法院在部分判例中认可行业惯例中的合理磨损不赔条款。",
            "解除": "上海法院对合同解除权的行使程序要求较严格，注重通知送达的有效性和解除事由的充分性。上海法院通常支持合同约定的解除条件。",
            "赔偿": "上海法院对商事主体的损失赔偿请求支持力度较大，对可预见规则和减损规则的适用较为灵活。",
            "管辖": "上海法院对商事合同中约定的管辖条款通常予以尊重，除非明显违反级别管辖或专属管辖规定。",
            "服务": "上海法院对预付式消费纠纷的处理注重合同约定。上海法院在部分判例中支持经营者的合理成本扣除。",
        },
    },
    "广州": {
        "label": "广州/广东法院",
        "style": "广东法院注重交易习惯和公平原则的平衡，对租赁合同纠纷的处理较为灵活。",
        "rules": {
            "违约金": "广东法院在违约金调整上较为灵活，注重个案平衡。广东省高级人民法院相关指导意见指出，违约金调整应考虑合同履行情况、当事人过错和预期利益。",
            "押金": "广东法院对押金争议的处理注重证据，对出租人扣减押金要求提供充分的费用凭证。",
            "解除": "广东法院对合同解除持审慎态度，注重维护交易稳定性。解除权的行使需有明确的合同或法律依据。",
            "赔偿": "广东法院对损失赔偿的认定较为务实，对实际发生的直接损失通常予以支持。",
            "管辖": "广东法院对管辖条款的处理注重当事人真实意思，对格式管辖条款的审查与其他地区一致。",
            "服务": "广东法院在预付式消费纠纷中注重消费者权益保护，对经营者停业、跑路等行为持否定态度。",
        },
    },
    "深圳": {
        "label": "深圳法院",
        "style": "深圳法院作为经济特区法院，注重市场化规则和合同自由，对新型商业模式和交易安排的接受度较高。",
        "rules": {
            "违约金": "深圳法院对商事违约金条款通常予以尊重，调减门槛较高。深圳前海合作区法院在多个判例中支持合同约定的违约金。",
            "押金": "深圳法院对押金条款倾向于按合同约定处理，注重证据规则。",
            "解除": "深圳法院对合同解除注重程序正义，要求解除通知明确、有效送达。",
            "赔偿": "深圳法院对商业损失的赔偿认定较为开放，对可得利益损失的支持力度相对较大。",
            "管辖": "深圳法院尊重当事人的管辖约定，对涉外商事案件的管辖处理具有较丰富经验。",
            "服务": "深圳法院对预付式消费的处理注重合同约定和消费者权益保护的平衡。",
        },
    },
    "杭州": {
        "label": "杭州/浙江法院",
        "style": "浙江法院注重互联网司法和数字化审判，对电子商务、平台经济和预付式消费纠纷有较多创新实践。",
        "rules": {
            "违约金": "浙江法院对违约金调整注重公平，杭州互联网法院在部分判例中引入在线纠纷化解机制。",
            "押金": "浙江法院对押金争议的处理较为规范，注重电子证据的采信。",
            "解除": "浙江法院注重合同解除的程序规范，杭州法院在租赁合同解除纠纷中有较多判例积累。",
            "赔偿": "浙江法院对损失赔偿的认定注重数字化证据，杭州互联网法院对电子合同纠纷的处理经验丰富。",
            "管辖": "浙江法院对互联网案件的管辖有较多创新实践，杭州互联网法院集中管辖部分涉网案件。",
            "服务": "浙江法院在预付式消费纠纷中注重平台责任和消费者保护，杭州市中级人民法院在多个判例中支持消费者维权。",
        },
    },
    "成都": {
        "label": "成都/四川法院",
        "style": "四川法院注重实质公平和民生保护，对涉及住房、教育、医疗等民生领域的合同纠纷持保护弱势方立场。",
        "rules": {
            "违约金": "四川法院对违约金调整较为积极，注重保护守约方利益的同时防止过高违约金。四川省高级人民法院相关指导意见强调公平原则。",
            "押金": "四川法院对押金纠纷的处理注重保护承租人，对出租人扣减押金要求较高证明标准。",
            "解除": "四川法院注重合同解除的合法性审查，对出租人单方解除权的行使持审慎态度。",
            "赔偿": "四川法院对损失赔偿注重实际损失，对间接损失的认定较为严格。",
            "管辖": "四川法院对管辖条款的处理注重方便当事人诉讼原则，对不便民的管辖条款持否定态度。",
            "服务": "四川法院在预付式消费纠纷中注重消费者权益保护，对经营者不规范经营行为持严格态度。",
        },
    },
}


def _get_region_tendency(jurisdiction: str, keyword: str) -> str:
    """获取指定地区对特定条款类型的裁判倾向。"""
    region = REGIONAL_TENDENCIES.get(jurisdiction, REGIONAL_TENDENCIES.get("北京", {}))
    rules = region.get("rules", {})

    for rule_key, rule_text in rules.items():
        if rule_key in keyword:
            return rule_text

    # 模糊匹配
    for rule_key, rule_text in rules.items():
        if keyword in rule_key or any(kw in keyword for kw in rule_key.split()):
            return rule_text

    # 通用倾向
    return (
        f"{region.get('label', '该地区法院')}对该类条款的处理遵循《民法典》合同编的相关规定，"
        "结合合同约定、履约情况和公平原则综合判断。"
        f"{region.get('style', '')}"
    )


# ---------------------------------------------------------------------------
# 判例占位数据
# ---------------------------------------------------------------------------

# 每条规则对应的占位判例（案号为占位标注）
PLACEHOLDER_CASES = {
    "违约金": [
        JurisdictionCase(
            case_id="【占位-待接入真实案号】",
            court="{region}中级人民法院",
            conclusion="法院认为违约金过分高于实际损失，依据《民法典》第585条将违约金调减至实际损失的130%。",
            relevance="与本案违约金条款类似，可参考本地法院的调减比例",
        ),
        JurisdictionCase(
            case_id="【占位-待接入真实案号】",
            court="{region}基层人民法院",
            conclusion="法院支持合同约定的违约金计算方式，认为违约金未明显过高，不予调减。",
            relevance="如本案违约金合理，本地法院倾向支持约定",
        ),
    ],
    "押金": [
        JurisdictionCase(
            case_id="【占位-待接入真实案号】",
            court="{region}中级人民法院",
            conclusion="出租人未能提供有效维修凭证，法院判决全额退还押金。",
            relevance="押金扣减需有充分证据支持",
        ),
        JurisdictionCase(
            case_id="【占位-待接入真实案号】",
            court="{region}基层人民法院",
            conclusion="出租人提供了维修发票和现场照片，法院支持合理扣减押金800元。",
            relevance="有凭证时法院支持合理扣减",
        ),
    ],
    "解除": [
        JurisdictionCase(
            case_id="【占位-待接入真实案号】",
            court="{region}中级人民法院",
            conclusion="出租人未履行催告义务直接解除合同，法院认定解除行为无效。",
            relevance="催告是解除的必要前置程序",
        ),
        JurisdictionCase(
            case_id="【占位-待接入真实案号】",
            court="{region}基层人民法院",
            conclusion="承租人逾期支付租金超过合同约定期限，出租人催告后解除合同，法院予以支持。",
            relevance="程序完整的解除权行使得到支持",
        ),
    ],
    "赔偿": [
        JurisdictionCase(
            case_id="【占位-待接入真实案号】",
            court="{region}中级人民法院",
            conclusion="原告提供了完整的损失计算依据和因果关系证明，法院支持赔偿请求。",
            relevance="证据充分的赔偿请求可获支持",
        ),
    ],
    "管辖": [
        JurisdictionCase(
            case_id="【占位-待接入真实案号】",
            court="{region}中级人民法院",
            conclusion="格式管辖条款未合理提示说明，法院认定无效，适用法定管辖。",
            relevance="格式管辖条款需合理提示",
        ),
    ],
    "服务": [
        JurisdictionCase(
            case_id="【占位-待接入真实案号】",
            court="{region}中级人民法院",
            conclusion="经营者停业后拒不退款，法院判决全额退还预付款并承担惩罚性赔偿。",
            relevance="预付式消费停业应全额退款",
        ),
    ],
}


def _build_local_cases(jurisdiction: str, keyword: str) -> List[JurisdictionCase]:
    """构建本地判例列表。"""
    region = REGIONAL_TENDENCIES.get(jurisdiction, REGIONAL_TENDENCIES.get("北京", {}))
    region_label = region.get("label", f"{jurisdiction}法院")

    templates = None
    for rule_key, cases in PLACEHOLDER_CASES.items():
        if rule_key in keyword:
            templates = cases
            break

    if templates is None:
        # 通用占位判例
        templates = [
            JurisdictionCase(
                case_id="【占位-待接入真实案号】",
                court=f"{region_label}",
                conclusion=f"该法院在类似合同纠纷中，依据《民法典》相关规定，结合案件事实作出裁判。",
                relevance=f"可参考该法院对类似条款的处理方式",
            ),
        ]

    result = []
    for case in templates:
        result.append(JurisdictionCase(
            case_id=case.case_id,
            court=case.court.replace("{region}", region_label),
            conclusion=case.conclusion,
            relevance=case.relevance,
        ))
    return result


# ---------------------------------------------------------------------------
# 管辖策略分析
# ---------------------------------------------------------------------------

def _analyze_jurisdiction_strategy(
    title: str, contract_text: str, profile: UserRiskProfile
) -> str:
    """分析管辖策略，检测合同约定的管辖地是否对用户不利。"""
    # 检查合同是否约定了管辖法院
    jurisdiction_keywords = ("管辖法院", "管辖", "争议解决", "起诉", "受理法院")
    has_jurisdiction_clause = any(kw in contract_text for kw in jurisdiction_keywords)

    if not has_jurisdiction_clause:
        return "合同未明确约定管辖法院，适用法定管辖规则。如发生争议，可在被告住所地或合同履行地法院起诉。"

    # 检测是否约定了非用户所在地的管辖
    user_location = profile.jurisdiction
    contract_has_user_location = user_location in contract_text

    if "管辖" in title:
        if not contract_has_user_location:
            return (
                f"合同约定的管辖法院可能不在您所在地（{user_location}），"
                "建议协商修改为合同履行地或被告住所地法院管辖，以降低异地诉讼成本。"
            )
        return f"合同约定的管辖法院在您所在地（{user_location}），管辖安排对您有利。"

    return ""


# ---------------------------------------------------------------------------
# 整体地域环境评估
# ---------------------------------------------------------------------------

def _assess_jurisdiction_environment(jurisdiction: str, profile: UserRiskProfile) -> str:
    """评估用户所在地法院的整体诉讼环境。"""
    region = REGIONAL_TENDENCIES.get(jurisdiction, REGIONAL_TENDENCIES.get("北京", {}))
    label = region.get("label", f"{jurisdiction}法院")
    style = region.get("style", "该地区法院遵循法律规定，注重公平正义。")

    lines = [f"## {label}整体诉讼环境评估", "", style, ""]

    if profile.bargaining_position == "弱势方":
        if jurisdiction in ("北京", "成都", "杭州"):
            lines.append(f"{label}在审理涉及消费者、承租人等弱势方的合同纠纷时，倾向于保护弱势方权益，整体诉讼环境对您较为有利。")
        else:
            lines.append(f"{label}在审理合同纠纷时，注重合同约定和市场规则。建议在签约阶段即完善合同条款，增强诉讼中的主动地位。")
    elif profile.bargaining_position == "强势方":
        lines.append(f"{label}尊重商事主体的自主约定，对合同条款的解释通常以文义为准。整体诉讼环境对您较为有利，但仍建议确保合同条款的合法性。")
    else:
        lines.append(f"{label}注重公平原则和合同约定的平衡。建议关注本地法院对同类案件的通常处理方式，合理评估诉讼预期。")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 主分析函数
# ---------------------------------------------------------------------------


def analyze_jurisdiction_prediction(
    review_items: List[Dict[str, Any]],
    profile: UserRiskProfile,
    contract_text: str = "",
) -> JurisdictionReport:
    """对审查报告中的高/中风险条款执行跨地域裁判预判。"""
    target_items = [item for item in review_items if item.get("risk_level") in ("高", "中")]
    jurisdiction = profile.jurisdiction or "北京"
    region = REGIONAL_TENDENCIES.get(jurisdiction, REGIONAL_TENDENCIES.get("北京", {}))
    label = region.get("label", f"{jurisdiction}法院")

    results: List[JurisdictionItem] = []
    for item in target_items:
        title = item.get("title", "")
        item_id = item.get("item_id", "")
        risk_level = item.get("risk_level", "中")

        # 本地法院倾向
        tendency = _get_region_tendency(jurisdiction, title)

        # 法律基础
        legal_basis = item.get("legal_basis_index", "《民法典》合同编相关规定")

        # 本地判例
        local_cases = _build_local_cases(jurisdiction, title)

        # 管辖策略
        jurisdiction_strategy = _analyze_jurisdiction_strategy(title, contract_text, profile)

        # 起诉建议
        if "调减" in tendency or "不予支持" in tendency or "不予" in tendency:
            recommendation = "建议协商"
            reason = f"{label}对此类条款的裁判倾向对您不完全有利，建议优先通过协商解决。"
        elif "支持" in tendency and "调减" not in tendency:
            recommendation = "建议起诉"
            reason = f"{label}对此类条款的裁判倾向对您较为有利，通过诉讼维权的预期收益较高。"
        else:
            recommendation = "建议协商"
            reason = f"建议结合具体证据和{label}的审判实践，在律师函或调解阶段解决。"

        data_note = (
            "判例案号为占位标注，不代表真实已决案件。"
            "上述裁判倾向基于各省高院公开的审判指导意见，具体案件结果受个案事实和证据影响。"
        )

        results.append(JurisdictionItem(
            item_id=item_id,
            title=title,
            risk_level=risk_level,
            local_court_tendency=tendency,
            legal_basis=legal_basis,
            local_cases=local_cases,
            litigation_recommendation=recommendation,
            recommendation_reason=reason,
            jurisdiction_strategy=jurisdiction_strategy,
            data_source_note=data_note,
        ))

    environment = _assess_jurisdiction_environment(jurisdiction, profile)

    # 管辖策略总结
    has_jurisdiction_clause = any("管辖" in item.get("title", "") for item in target_items)
    if has_jurisdiction_clause:
        jurisdiction_summary = (
            f"合同约定了管辖条款。建议确认管辖法院是否在您所在地（{jurisdiction}），"
            "如约定在外地且对您不利，应优先协商修改管辖条款。"
        )
    else:
        jurisdiction_summary = (
            f"合同未明确约定管辖法院。如发生争议，可在被告住所地或合同履行地法院起诉。"
            f"建议选择对您较为便利的法院。"
        )

    return JurisdictionReport(
        disclaimer=JURISDICTION_DISCLAIMER,
        jurisdiction=jurisdiction,
        items=results,
        environment_assessment=environment,
        jurisdiction_strategy_summary=jurisdiction_summary,
    )


def format_jurisdiction_markdown(report: JurisdictionReport) -> str:
    """将跨地域裁判预判报告格式化为 Markdown。"""
    lines = [
        "# 跨地域裁判预判",
        "",
        f"> 用户所在地：**{report.jurisdiction}**",
        f"> {report.disclaimer}",
        "",
        "---",
        "",
        report.environment_assessment,
        "",
        "---",
        "",
        "## 管辖策略提示",
        "",
        report.jurisdiction_strategy_summary,
        "",
        "---",
        "",
        "## 逐项裁判预判",
        "",
    ]

    for index, item in enumerate(report.items, start=1):
        rec_icon = {"建议起诉": "⚖️", "建议协商": "🤝", "不建议起诉": "⏸️"}
        lines.append(f"## {index}. {item.title}（{item.item_id}）")
        lines.append(f"风险等级：{item.risk_level}")
        lines.append("")

        lines.append("### 本地法院倾向")
        lines.append(f"> {item.local_court_tendency}")
        lines.append("")

        lines.append("### 法律基础")
        lines.append(f"{item.legal_basis}")
        lines.append("")

        lines.append("### 本地判例参考")
        for case in item.local_cases:
            lines.append(f"- **{case.case_id}**（{case.court}）")
            lines.append(f"  > {case.conclusion}")
            lines.append(f"  > 关联性：{case.relevance}")
        lines.append("")

        lines.append(f"### 起诉建议：{rec_icon.get(item.litigation_recommendation, '')} **{item.litigation_recommendation}**")
        lines.append(f"> {item.recommendation_reason}")
        lines.append("")

        if item.jurisdiction_strategy:
            lines.append("### 管辖策略")
            lines.append(f"> {item.jurisdiction_strategy}")
            lines.append("")

        lines.append(f"> *{item.data_source_note}*")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)
