"""商业谈判分析模块。

对审查报告中标记为高风险和中风险的条款，生成谈判筹码转换方案：
1. 条款谈判属性标记（必争项/核心项/灵活项）
2. 对方真实意图分析（用中性表述，不假设恶意）
3. 替代方案（具体可执行的修改方案）
4. 交换筹码建议（用对方让步换取接受）
5. 谈判话术（口语化、可直接使用）
6. 整体谈判策略（分类清单+让步顺序）

约束：
- 不假设对方恶意，用中性表述
- 所有替代方案必须具体、可执行
- 话术必须口语化、可直接使用
- 保留免责声明
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from review_v2.user_profile import UserRiskProfile

# ---------------------------------------------------------------------------
# 免责声明
# ---------------------------------------------------------------------------

NEGOTIATION_DISCLAIMER = (
    "本分析基于合同文本和通用谈判原则生成，不构成法律意见，不替代律师或专业谈判顾问的判断。"
    "实际谈判结果受双方实力对比、市场环境和具体谈判进程影响，仅供参考。"
)

# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------


@dataclass
class CounterpartyIntent:
    """对方真实意图分析。"""

    likely_concern: str  # 对方可能担心什么
    likely_want: str  # 对方想要什么
    pressure_points: str = ""  # 对方可能让步的压力点


@dataclass
class AlternativeProposal:
    """替代方案。"""

    proposal: str  # 具体替代方案描述
    impact: str  # 对己方的影响评估
    feasibility: str  # 可行性评估（高/中/低）


@dataclass
class TradeoffSuggestion:
    """交换筹码建议。"""

    what_you_give: str  # 你让步的内容
    what_you_ask: str  # 你要求对方回报的内容
    rationale: str  # 交换理由


@dataclass
class NegotiationItem:
    """单条条款的谈判分析。"""

    item_id: str
    title: str
    risk_level: str
    # 谈判属性：必争项/核心项/灵活项
    negotiation_priority: str
    # 对方真实意图
    counterparty_intent: CounterpartyIntent
    # 替代方案（可多个）
    alternatives: List[AlternativeProposal]
    # 交换筹码
    tradeoff: TradeoffSuggestion
    # 谈判话术
    script: str

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "title": self.title,
            "risk_level": self.risk_level,
            "negotiation_priority": self.negotiation_priority,
            "counterparty_intent": {
                "likely_concern": self.counterparty_intent.likely_concern,
                "likely_want": self.counterparty_intent.likely_want,
                "pressure_points": self.counterparty_intent.pressure_points,
            },
            "alternatives": [
                {
                    "proposal": a.proposal,
                    "impact": a.impact,
                    "feasibility": a.feasibility,
                }
                for a in self.alternatives
            ],
            "tradeoff": {
                "what_you_give": self.tradeoff.what_you_give,
                "what_you_ask": self.tradeoff.what_you_ask,
                "rationale": self.tradeoff.rationale,
            },
            "script": self.script,
        }


@dataclass
class NegotiationReport:
    """完整谈判分析报告。"""

    disclaimer: str
    items: List[NegotiationItem]
    # 分类清单
    must_fight: List[str]  # 必争项 ID 列表
    core_negotiate: List[str]  # 核心项 ID 列表
    flexible: List[str]  # 灵活项 ID 列表
    # 让步顺序建议
    concession_order: List[str]
    # 整体策略
    overall_strategy: str

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "disclaimer": self.disclaimer,
            "items": [item.to_public_dict() for item in self.items],
            "must_fight": self.must_fight,
            "core_negotiate": self.core_negotiate,
            "flexible": self.flexible,
            "concession_order": self.concession_order,
            "overall_strategy": self.overall_strategy,
        }


# ---------------------------------------------------------------------------
# 条款谈判属性判定
# ---------------------------------------------------------------------------

# 必争项 ID（涉及合同效力、强制性规定，不能让步）
MUST_FIGHT_ITEMS = {
    "HL-002", "HL-010",  # 主体身份、房屋合法性
    "CE-05-01", "CE-05-02", "CE-05-03",  # 建设工程转包/分包禁止
    "S-02-01", "S-02-02",  # 标的物合法性
    "SVC-02-01", "SVC-02-04",  # 服务方资质
    "G-01-01", "G-01-02",  # 赠与意思表示
}

# 核心项关键词（涉及重大商业利益）
CORE_ITEM_KEYWORDS = {
    "违约金", "赔偿", "押金", "退款", "退费",
    "解除", "租金", "付款", "价格", "期限",
    "质量", "验收", "交付",
}

# 灵活项关键词（一般商业条件）
FLEXIBLE_ITEM_KEYWORDS = {
    "管辖", "送达", "附件", "通知", "不可抗力",
    "争议", "协商", "联系方式", "备案", "记录",
}


def _determine_negotiation_priority(item_id: str, title: str, risk_level: str) -> str:
    """判定条款谈判属性。"""
    if item_id in MUST_FIGHT_ITEMS or risk_level == "高":
        # 涉及强制性规定或已被判定为高风险 -> 必争项
        return "必争项"

    for kw in CORE_ITEM_KEYWORDS:
        if kw in title:
            return "核心项"

    for kw in FLEXIBLE_ITEM_KEYWORDS:
        if kw in title:
            return "灵活项"

    # 默认按风险等级
    if risk_level == "中":
        return "核心项"
    return "灵活项"


# ---------------------------------------------------------------------------
# 对方真实意图分析
# ---------------------------------------------------------------------------

COUNTERPARTY_INTENT_RULES = {
    "违约金": CounterpartyIntent(
        likely_concern="对方可能担心己方中途违约或拖延履行，造成其资金占用和机会损失",
        likely_want="对方希望通过高额违约金形成威慑，确保合同顺利履行",
        pressure_points="可指出违约金过高可能被法院调减，实际执行效果有限，不如约定合理的违约金+损失补足机制",
    ),
    "押金": CounterpartyIntent(
        likely_concern="对方可能担心租赁物损坏、欠费或提前退租造成的空置损失",
        likely_want="对方希望用押金覆盖可能发生的维修费、欠费和提前退租损失",
        pressure_points="可指出押金扣减需要举证，建议约定明确的扣减标准和退还期限，减少争议",
    ),
    "租金": CounterpartyIntent(
        likely_concern="对方可能担心承租人拖欠租金，影响其现金流和收益预期",
        likely_want="对方希望确保租金按时足额收取，并保留欠租时的解除权",
        pressure_points="可建议约定明确的付款节点和逾期通知机制，降低欠租风险",
    ),
    "解除": CounterpartyIntent(
        likely_concern="对方可能担心合同履行中出现变故，希望在特定条件下保留退出渠道",
        likely_want="对方希望在对方违约或出现重大变化时能及时止损",
        pressure_points="可指出解除权需符合法定条件，建议约定明确、合理的解除事由和通知期",
    ),
    "赔偿": CounterpartyIntent(
        likely_concern="对方可能担心违约造成的损失无法通过一般违约金覆盖",
        likely_want="对方希望确保实际损失能得到充分赔偿",
        pressure_points="可指出赔偿需证明损失和因果关系，建议约定明确的损失计算方式",
    ),
    "退费": CounterpartyIntent(
        likely_concern="对方可能担心消费者中途退费影响经营现金流和已投入成本",
        likely_want="对方希望减少退费损失，将已发生成本转嫁给消费者",
        pressure_points="可指出格式退费条款可能无效，建议约定合理的退费计算方式，平衡双方利益",
    ),
    "服务": CounterpartyIntent(
        likely_concern="对方可能担心服务标准不清导致持续争议，或服务成本超出预期",
        likely_want="对方希望在服务内容、标准和价格上有明确的边界",
        pressure_points="可建议细化服务清单和验收标准，减少模糊地带",
    ),
    "管辖": CounterpartyIntent(
        likely_concern="对方可能担心异地诉讼增加其维权成本和时间",
        likely_want="对方希望在己方所在地法院管辖，降低诉讼门槛",
        pressure_points="可指出法定管辖规则通常支持被告住所地或合同履行地，建议选择双方相对便利的中立地点",
    ),
    "期限": CounterpartyIntent(
        likely_concern="对方可能担心长期锁定影响其灵活性，或短期合同频繁续约增加管理成本",
        likely_want="对方希望在合同期限上取得有利安排",
        pressure_points="可建议约定合理的期限+续约条款，平衡稳定性和灵活性",
    ),
    "付款": CounterpartyIntent(
        likely_concern="对方可能担心收款延迟影响其现金流和经营安排",
        likely_want="对方希望确保付款节点明确、逾期有约束力",
        pressure_points="可建议约定明确的付款节点和逾期利息，确保双方利益",
    ),
}


def _build_counterparty_intent(title: str) -> CounterpartyIntent:
    """分析对方真实意图。"""
    for keyword, intent in COUNTERPARTY_INTENT_RULES.items():
        if keyword in title:
            return intent

    # 通用分析
    return CounterpartyIntent(
        likely_concern=f"对方可能担心「{title}」相关安排不明确或不公平，影响其履约安全和预期收益",
        likely_want=f"对方希望在「{title}」上取得对其有利的安排",
        pressure_points="可指出明确的条款约定对双方都有利，建议提供行业惯例或市场参考标准",
    )


# ---------------------------------------------------------------------------
# 替代方案生成
# ---------------------------------------------------------------------------

ALTERNATIVE_TEMPLATES = {
    "违约金": [
        AlternativeProposal(
            proposal="将违约金从固定倍数改为「以实际损失为限，最高不超过月租金的X倍」，避免法院调减风险",
            impact="降低违约金金额上限，但增加可执行性",
            feasibility="高",
        ),
        AlternativeProposal(
            proposal="增加「违约金不足以弥补损失的，违约方应赔偿造成的实际损失」条款",
            impact="保留全额赔偿可能性，对己方更有利",
            feasibility="高",
        ),
    ],
    "押金": [
        AlternativeProposal(
            proposal="约定「押金在租赁期满且无欠费损坏后X日内全额退还」，明确退还期限",
            impact="保障押金及时返还，降低维权成本",
            feasibility="高",
        ),
        AlternativeProposal(
            proposal="增加「出租人扣除押金应提供维修发票或第三方报价单作为凭证」",
            impact="限制对方随意扣减，保护押金安全",
            feasibility="中",
        ),
    ],
    "租金": [
        AlternativeProposal(
            proposal="将租金支付周期从年付/半年付改为季付或月付，降低资金占用",
            impact="增加对方收款频率但降低己方一次性支出",
            feasibility="高",
        ),
        AlternativeProposal(
            proposal="增加「逾期支付租金超过X日，出租人应书面催告后方可主张违约责任」",
            impact="给予缓冲期，避免因短时延迟被认定为违约",
            feasibility="高",
        ),
    ],
    "解除": [
        AlternativeProposal(
            proposal="增加「一方提前解除应提前X日书面通知，并按未履行期限比例承担合理损失」",
            impact="明确解除后果，避免争议",
            feasibility="高",
        ),
        AlternativeProposal(
            proposal="约定「因不可抗力或政策变化导致合同无法履行的，双方互不承担违约责任，按实际履行结算」",
            impact="保护双方在特殊情形下的利益",
            feasibility="高",
        ),
    ],
    "管辖": [
        AlternativeProposal(
            proposal="将管辖法院改为「合同履行地人民法院」，通常对双方都相对公平",
            impact="可能增加己方诉讼成本，但降低对方的抗拒",
            feasibility="高",
        ),
        AlternativeProposal(
            proposal="增加「争议发生后双方应先行协商，协商不成的可选择仲裁或诉讼」",
            impact="增加争议解决灵活性",
            feasibility="中",
        ),
    ],
    "退费": [
        AlternativeProposal(
            proposal="约定「退费金额=已付款-已提供服务价值-合理手续费（不超过已付款的X%）」",
            impact="明确退费公式，减少争议空间",
            feasibility="高",
        ),
        AlternativeProposal(
            proposal="增加「赠送课时/服务不单独计入已提供服务价值」条款",
            impact="保护消费者权益，避免赠送服务被计价抵扣",
            feasibility="中",
        ),
    ],
}


def _build_alternatives(title: str) -> List[AlternativeProposal]:
    """生成替代方案。"""
    for keyword, alternatives in ALTERNATIVE_TEMPLATES.items():
        if keyword in title:
            return alternatives

    # 通用替代方案
    return [
        AlternativeProposal(
            proposal=f"建议明确约定「{title}」的具体标准、范围和例外情形，减少模糊条款",
            impact="增加条款明确性和可执行性",
            feasibility="高",
        ),
        AlternativeProposal(
            proposal=f"可参照行业惯例或市场通行做法，约定「{title}」的合理标准",
            impact="引入客观参考标准，降低争议空间",
            feasibility="中",
        ),
    ]


# ---------------------------------------------------------------------------
# 交换筹码建议
# ---------------------------------------------------------------------------

TRADEOFF_SUGGESTIONS = {
    "违约金": TradeoffSuggestion(
        what_you_give="接受较高的违约金条款",
        what_you_ask="要求对方同步接受更明确的己方解除权和押金退还条款",
        rationale="违约金是对方核心关切，接受后可用此换取其他条款的让步",
    ),
    "押金": TradeoffSuggestion(
        what_you_give="接受押金扣减条款",
        what_you_ask="要求对方同意「扣减需提供凭证」和「明确退还期限」",
        rationale="押金管理是出租方核心利益，接受扣减权但增加透明度限制，是平衡的让步",
    ),
    "租金": TradeoffSuggestion(
        what_you_give="接受较高的租金或较短的支付周期",
        what_you_ask="要求对方在维修责任、设备配置或免租期上让步",
        rationale="租金是核心对价，适当让步可用以换取服务质量的提升",
    ),
    "解除": TradeoffSuggestion(
        what_you_give="接受对方的解除权条款",
        what_you_ask="要求对方同步接受己方在对方违约时的对等解除权和赔偿条款",
        rationale="解除权应对等，接受对方权利的同时应确保己方权益",
    ),
    "管辖": TradeoffSuggestion(
        what_you_give="接受对方所在地管辖",
        what_you_ask="要求对方在违约金、押金或付款条款上做出让步",
        rationale="管辖条款对日常履行影响较小，可作为交换筹码换取实质利益",
    ),
    "退费": TradeoffSuggestion(
        what_you_give="接受对方的退费扣减方案",
        what_you_ask="要求对方提供明确的服务标准、质量保证或优惠价格",
        rationale="退费是消费合同核心条款，适度让步可换取服务质量和价格的提升",
    ),
}


def _build_tradeoff(title: str, profile: UserRiskProfile) -> TradeoffSuggestion:
    """生成交换筹码建议。"""
    for keyword, suggestion in TRADEOFF_SUGGESTIONS.items():
        if keyword in title:
            return suggestion

    if profile.bargaining_position == "弱势方":
        return TradeoffSuggestion(
            what_you_give=f"在「{title}」上做出有限让步",
            what_you_ask="要求对方在己方更关心的核心条款上做出对等让步",
            rationale="作为弱势方，应集中资源争取最核心的利益，在次要条款上适当让步",
        )
    elif profile.bargaining_position == "强势方":
        return TradeoffSuggestion(
            what_you_give=f"在「{title}」上给出合理方案",
            what_you_ask="确保合同的整体公平性和长期合作基础",
            rationale="作为强势方，适度让步有助于建立良好合作关系，降低未来纠纷风险",
        )
    return TradeoffSuggestion(
        what_you_give=f"在「{title}」上寻求双方可接受的中间方案",
        what_you_ask="争取在其他条款上获得对等补偿",
        rationale="均衡谈判中，每一处让步都应对应有价值的回报",
    )


# ---------------------------------------------------------------------------
# 谈判话术生成
# ---------------------------------------------------------------------------

SCRIPT_TEMPLATES = {
    "违约金": (
        "「关于违约金这块，我理解您希望确保合同能顺利履行。不过目前约定的违约金比例确实偏高了，"
        "根据法院的通常做法，超过实际损失30%的部分大概率会被调减。"
        "咱们不如约定一个双方都能接受的标准，再加一条损失补足条款，这样既有约束力，执行起来也更顺畅。」"
    ),
    "押金": (
        "「押金这块我完全理解，您肯定担心房子有损坏或者费用没结清。"
        "咱们可以约定，退租时您来检查，如果有损坏您提供维修报价或发票，从押金里合理扣减。"
        "同时也约定一个退还期限，比如7个工作日内，这样双方都放心。」"
    ),
    "租金": (
        "「关于租金支付方式，您看能不能调整为季付或者月付？一次性付太多确实有点压力。"
        "当然，如果按时付款有任何问题，咱们可以约定逾期利息和催告机制，保证您的收款安全。」"
    ),
    "解除": (
        "「解除条款这块，我希望咱们能约定对等的权利。"
        "如果我这边有违约情况，您当然有权解除；同样，如果您这边出现问题，我也需要有相应的解除权。"
        "这样对双方都公平，也符合合同法的精神。」"
    ),
    "管辖": (
        "「关于管辖法院，我理解您希望在本地处理。咱们能不能折中一下，选择合同履行地法院？"
        "这样对双方都相对公平，万一真有问题，大家都不至于跑太远。」"
    ),
    "退费": (
        "「退费这块，我理解您有成本投入，不希望中途退费影响经营。"
        "咱们可以约定一个合理的退费公式：扣除已消费部分和少量手续费，剩余退还。"
        "这样既保护您的成本，也给我一个合理的退出通道。」"
    ),
    "赔偿": (
        "「赔偿条款这块，我希望咱们能把损失计算方式约定得更清楚一些。"
        "比如直接损失包括哪些、间接损失怎么算、需不需要发票或评估报告来证明。"
        "这样万一真需要赔偿，双方都清楚标准，不用再扯皮。」"
    ),
    "服务": (
        "「关于服务内容和标准，咱们能不能再细化一下？比如服务的具体项目、频次、时长、标准都写清楚。"
        "这样您提供服务时有明确目标，我验收时也有客观标准，对双方都省心。」"
    ),
    "付款": (
        "「付款这块，咱们能不能约定分阶段付款？比如签约付一部分、服务进行到一半付一部分、验收后付尾款。"
        "这样您的收款也有保障，我的资金压力也能分散一些。」"
    ),
    "期限": (
        "「关于合同期限，咱们能不能先签一年，约定到期前X日双方无异议自动续期？"
        "这样既有稳定性，也保留了调整的灵活性。如果合作得好，自然就续下去了。」"
    ),
}


def _build_script(title: str, profile: UserRiskProfile) -> str:
    """生成谈判话术。"""
    for keyword, script in SCRIPT_TEMPLATES.items():
        if keyword in title:
            return script

    # 通用话术
    if profile.bargaining_position == "弱势方":
        return (
            f"「关于「{title}」这一条，我看了一下，目前这个安排对我来说确实有点压力。"
            "咱们能不能商量一个双方都能接受的方案？我这边也可以在其他方面配合您。」"
        )
    elif profile.bargaining_position == "强势方":
        return (
            f"「关于「{title}」，咱们目前这个安排我觉得基本合理，"
            "但为了合作更顺畅，我想听听您的想法，看看有没有更好的方式。」"
        )
    return (
        f"「关于「{title}」这条，咱们各自聊聊想法吧。"
        "您最关心的是什么？我这边也有一些考虑，咱们看看能不能找到折中方案。」"
    )


# ---------------------------------------------------------------------------
# 整体谈判策略
# ---------------------------------------------------------------------------

def _build_overall_strategy(
    items: List[NegotiationItem], profile: UserRiskProfile
) -> str:
    """生成整体谈判策略。"""
    must = [i for i in items if i.negotiation_priority == "必争项"]
    core = [i for i in items if i.negotiation_priority == "核心项"]
    flex = [i for i in items if i.negotiation_priority == "灵活项"]

    lines = ["## 整体谈判策略", ""]

    # 角色定位
    if profile.bargaining_position == "弱势方":
        lines.append(
            "**角色定位**：您在当前交易中处于相对弱势地位。建议采取「防御为主、重点突破」策略："
            "集中精力守住必争项，在核心项上争取合理条款，在灵活项上主动让步以换取对方好感。"
        )
    elif profile.bargaining_position == "强势方":
        lines.append(
            "**角色定位**：您在当前交易中处于相对强势地位。建议采取「主动引导、留有空间」策略："
            "在守住底线的同时，适度让步以建立长期合作关系，避免过度施压导致对方退出。"
        )
    else:
        lines.append(
            "**角色定位**：双方地位相对均衡。建议采取「对等交换、逐项推进」策略："
            "每一项让步都应换取对等回报，避免单方面退让。"
        )

    lines.append("")

    # 分类清单
    lines.append("### 必争项（不能让步）")
    if must:
        for i, item in enumerate(must, 1):
            lines.append(f"{i}. **{item.title}**（{item.item_id}）")
    else:
        lines.append("无")
    lines.append("")

    lines.append("### 核心项（建议坚持，可适度交换）")
    if core:
        for i, item in enumerate(core, 1):
            lines.append(f"{i}. **{item.title}**（{item.item_id}）")
    else:
        lines.append("无")
    lines.append("")

    lines.append("### 灵活项（可让步用于换取对方让步）")
    if flex:
        for i, item in enumerate(flex, 1):
            lines.append(f"{i}. **{item.title}**（{item.item_id}）")
    else:
        lines.append("无")
    lines.append("")

    # 让步顺序建议
    lines.append("### 建议让步顺序")
    if profile.risk_appetite == "保守":
        lines.append(
            "1. 先在灵活项上让步，表达诚意\n"
            "2. 在核心项上坚持，仅在对方对等让步时考虑\n"
            "3. 必争项坚决不让，引用法律规定作为依据\n"
            "4. 如对方坚持必争项，建议暂停谈判，咨询律师后再继续"
        )
    elif profile.risk_appetite == "激进":
        lines.append(
            "1. 在灵活项上主动让步，快速建立谈判氛围\n"
            "2. 在核心项上提出交换条件，推动对方让步\n"
            "3. 必争项保持底线，但可在表述方式上给对方留面子\n"
            "4. 目标是以最小代价达成协议，推动交易落地"
        )
    else:
        lines.append(
            "1. 先讨论灵活项，建立协商基础\n"
            "2. 核心项逐项谈判，每项让步争取对等回报\n"
            "3. 必争项在最后讨论，以法律规定为依据\n"
            "4. 整体让步控制在合理范围内，确保最终方案公平可执行"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 主分析函数
# ---------------------------------------------------------------------------


def analyze_negotiation_strategy(
    review_items: List[Dict[str, Any]],
    profile: UserRiskProfile,
) -> NegotiationReport:
    """对审查报告中的高/中风险条款执行商业谈判分析。"""
    target_items = [item for item in review_items if item.get("risk_level") in ("高", "中")]
    results: List[NegotiationItem] = []

    for item in target_items:
        title = item.get("title", "")
        item_id = item.get("item_id", "")
        risk_level = item.get("risk_level", "中")

        priority = _determine_negotiation_priority(item_id, title, risk_level)
        intent = _build_counterparty_intent(title)
        alternatives = _build_alternatives(title)
        tradeoff = _build_tradeoff(title, profile)
        script = _build_script(title, profile)

        results.append(NegotiationItem(
            item_id=item_id, title=title, risk_level=risk_level,
            negotiation_priority=priority,
            counterparty_intent=intent,
            alternatives=alternatives,
            tradeoff=tradeoff,
            script=script,
        ))

    must_fight = [i.item_id for i in results if i.negotiation_priority == "必争项"]
    core_negotiate = [i.item_id for i in results if i.negotiation_priority == "核心项"]
    flexible = [i.item_id for i in results if i.negotiation_priority == "灵活项"]
    concession_order = flexible + core_negotiate  # 先让灵活项，再让核心项

    overall_strategy = _build_overall_strategy(results, profile)

    return NegotiationReport(
        disclaimer=NEGOTIATION_DISCLAIMER,
        items=results,
        must_fight=must_fight,
        core_negotiate=core_negotiate,
        flexible=flexible,
        concession_order=concession_order,
        overall_strategy=overall_strategy,
    )


def format_negotiation_markdown(report: NegotiationReport) -> str:
    """将谈判分析报告格式化为 Markdown。"""
    lines = [
        "# 商业谈判分析",
        "",
        f"> {report.disclaimer}",
        "",
        "---",
        "",
        report.overall_strategy,
        "",
        "---",
        "",
        "## 逐项谈判指南",
        "",
    ]

    for index, item in enumerate(report.items, start=1):
        priority_icon = {"必争项": "🔴", "核心项": "🟡", "灵活项": "🟢"}
        lines.append(f"## {index}. {item.title}（{item.item_id}）")
        lines.append(f"谈判属性：{priority_icon.get(item.negotiation_priority, '')} **{item.negotiation_priority}**")
        lines.append(f"风险等级：{item.risk_level}")
        lines.append("")

        # 对方真实意图
        lines.append("### 对方真实意图")
        lines.append(f"- **对方可能担心**：{item.counterparty_intent.likely_concern}")
        lines.append(f"- **对方希望**：{item.counterparty_intent.likely_want}")
        if item.counterparty_intent.pressure_points:
            lines.append(f"- **谈判压力点**：{item.counterparty_intent.pressure_points}")
        lines.append("")

        # 替代方案
        lines.append("### 替代方案")
        for alt in item.alternatives:
            lines.append(f"- **方案**：{alt.proposal}")
            lines.append(f"  - 对己方影响：{alt.impact}")
            lines.append(f"  - 可行性：{alt.feasibility}")
        lines.append("")

        # 交换筹码
        lines.append("### 交换筹码建议")
        lines.append(f"- **你可以让步**：{item.tradeoff.what_you_give}")
        lines.append(f"- **要求对方回报**：{item.tradeoff.what_you_ask}")
        lines.append(f"- **交换理由**：{item.tradeoff.rationale}")
        lines.append("")

        # 谈判话术
        lines.append("### 谈判话术")
        lines.append(f"> {item.script}")
        lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)
