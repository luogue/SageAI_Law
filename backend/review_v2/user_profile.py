"""用户风险画像模块。

画像维度由用户在启动审查前填写，引擎根据画像动态调整审查输出：
- 风险等级个性化（保守/标准/激进）
- 修改建议语气动态调整
- 审查点激活/过滤
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# 画像维度定义
# ---------------------------------------------------------------------------

USER_IDENTITIES = ("个人租客/买方", "小微企业（≤50人）", "中型企业（50-500人）", "大型企业/投资者")
CONTRACT_SCENARIOS = ("居住用途", "商业经营", "投资/转租")
RISK_APPETITES = ("保守", "标准", "激进")
BARGAINING_POSITIONS = ("强势方", "均衡方", "弱势方")


@dataclass
class UserRiskProfile:
    """用户风险画像——在启动审查前填写。"""

    user_identity: str = "个人租客/买方"
    contract_scenario: str = "居住用途"
    risk_appetite: str = "标准"
    bargaining_position: str = "均衡方"
    # 跨地域裁判预判用：案件管辖地/用户所在地
    jurisdiction: str = "北京"  # 如：北京、上海、广州、深圳、杭州、成都 等

    # ---------- 快速工厂方法 ----------

    @classmethod
    def default(cls) -> UserRiskProfile:
        """默认画像（标准用户，与旧版行为一致）。"""
        return cls()

    @classmethod
    def conservative_individual_tenant(cls) -> UserRiskProfile:
        """保守个人租客——任何风险都要求修改。"""
        return cls(
            user_identity="个人租客/买方",
            contract_scenario="居住用途",
            risk_appetite="保守",
            bargaining_position="弱势方",
        )

    @classmethod
    def aggressive_investor(cls) -> UserRiskProfile:
        """激进投资者——仅高风险才要求修改。"""
        return cls(
            user_identity="大型企业/投资者",
            contract_scenario="投资/转租",
            risk_appetite="激进",
            bargaining_position="强势方",
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            "user_identity": self.user_identity,
            "contract_scenario": self.contract_scenario,
            "risk_appetite": self.risk_appetite,
            "bargaining_position": self.bargaining_position,
            "jurisdiction": self.jurisdiction,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, str]) -> UserRiskProfile:
        # An explicit task review role is authoritative.  Some callers also carry
        # a generic user_identity inferred from the contract subtype; it must not
        # overwrite the party perspective selected for the review.
        user_identity = d.get("review_role") or d.get("user_identity") or "个人租客/买方"
        return cls(
            user_identity=user_identity,
            contract_scenario=d.get("contract_scenario", "居住用途"),
            risk_appetite=d.get("risk_appetite", "标准"),
            bargaining_position=d.get("bargaining_position", "均衡方"),
            jurisdiction=d.get("jurisdiction", "北京"),
        )


# ---------------------------------------------------------------------------
# 语气映射
# ---------------------------------------------------------------------------

# 高风险语气
TONE_HIGH: Dict[str, str] = {
    "保守": "必须修改",
    "标准": "建议修改",
    "激进": "可考虑修改",
}

# 中风险语气
TONE_MEDIUM: Dict[str, str] = {
    "保守": "建议重点完善",
    "标准": "建议重点完善",
    "激进": "提示注意",
}

# 低风险语气
TONE_LOW: Dict[str, str] = {
    "保守": "建议完善",
    "标准": "可优化",
    "激进": "仅供参考",
}


def get_action_label(risk_level: str, risk_appetite: str) -> str:
    """根据风险等级和用户偏好，返回行动标签（必须改/建议改/可考虑改）。"""
    mapping = {
        "高": TONE_HIGH,
        "中": TONE_MEDIUM,
        "低": TONE_LOW,
    }
    return mapping.get(risk_level, TONE_MEDIUM).get(risk_appetite, "需关注")


def get_risk_remap(risk_level: str, risk_appetite: str) -> str:
    """根据风险偏好重映射风险等级。

    风险等级只表达客观法律严重性，不再由用户画像机械抬高。
    保守型用户通过行动标签和提示语体现“建议优先修改”，但高风险仍仅保留
    合同效力、重大财产损失、人身安全等法律底线类事项。
    """
    if risk_appetite == "保守":
        return risk_level
    if risk_appetite == "激进":
        # 中降为低，低保持不变（不隐藏）
        if risk_level == "中":
            return "低"
        return risk_level
    # 标准：不调整
    return risk_level


def get_modification_tone(risk_level: str, risk_appetite: str) -> str:
    """获取修改建议语气文本。"""
    mapping = {
        "高": TONE_HIGH,
        "中": TONE_MEDIUM,
        "低": TONE_LOW,
    }
    return mapping.get(risk_level, TONE_MEDIUM).get(risk_appetite, "需关注")


# ---------------------------------------------------------------------------
# 审查点激活/过滤规则
# ---------------------------------------------------------------------------

# 按用户身份优先激活的审查点 ID 集合
PRIORITY_CHECKPOINTS: Dict[str, Tuple[str, ...]] = {
    "个人租客/买方": (
        # 押金、维修、提前解约、隐私安全
        "HL-003", "HL-006", "HL-007", "HL-014", "HL-015", "HL-016",
        "HL-017", "HL-018", "HL-019", "HL-024", "HL-025", "HL-026",
        "HL-029", "HL-030", "HL-031", "HL-032", "HL-034", "HL-036",
        "HL-037",
    ),
    "大型企业/投资者": (
        # 转租限制、租金调整、续租权、违约责任上限
        "HL-004", "HL-005", "HL-008", "HL-009", "HL-010", "HL-011",
        "HL-012", "HL-013", "HL-020", "HL-021", "HL-022", "HL-023",
        "HL-027", "HL-028", "HL-033", "HL-035", "HL-038", "HL-039",
    ),
}

# 按合同场景优先激活的审查点
SCENARIO_CHECKPOINTS: Dict[str, Tuple[str, ...]] = {
    "居住用途": (
        "HL-003", "HL-006", "HL-007", "HL-014", "HL-017", "HL-024", "HL-034",
    ),
    "商业经营": (
        "HL-005", "HL-008", "HL-009", "HL-010", "HL-011", "HL-012",
        "HL-020", "HL-021", "HL-022", "HL-023",
    ),
    "投资/转租": (
        "HL-004", "HL-027", "HL-028", "HL-033", "HL-035", "HL-038", "HL-039",
    ),
}


def get_priority_checkpoints(profile: UserRiskProfile) -> set:
    """获取需要优先激活的审查点 ID 集合。"""
    priorities: set = set()
    if profile.user_identity in PRIORITY_CHECKPOINTS:
        priorities.update(PRIORITY_CHECKPOINTS[profile.user_identity])
    if profile.contract_scenario in SCENARIO_CHECKPOINTS:
        priorities.update(SCENARIO_CHECKPOINTS[profile.contract_scenario])
    return priorities


def is_priority_checkpoint(item_id: str, profile: UserRiskProfile) -> bool:
    """判断某审查点是否为当前画像的优先审查点。"""
    return item_id in get_priority_checkpoints(profile)


# ---------------------------------------------------------------------------
# 画像摘要生成
# ---------------------------------------------------------------------------

def format_profile_summary(profile: UserRiskProfile) -> str:
    """生成用户画像摘要文本。"""
    lines = [
        f"- **用户身份**：{profile.user_identity}",
        f"- **合同场景**：{profile.contract_scenario}",
        f"- **风险偏好**：{profile.risk_appetite}",
        f"- **交易地位**：{profile.bargaining_position}",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 审查报告语气适配
# ---------------------------------------------------------------------------

def adapt_report_header(profile: UserRiskProfile) -> str:
    """根据画像生成报告头部语气适配说明。"""
    if profile.risk_appetite == "保守":
        return (
            "> **审查策略**：保守模式。本报告对所有可能的法律风险均标注修改建议，"
            "力求最大程度保护您作为{identity}的合法权益。"
        ).format(identity=profile.user_identity)
    if profile.risk_appetite == "激进":
        return (
            "> **审查策略**：激进模式。本报告仅对违反强制性规定或可能导致合同无效的条款"
            "给出修改建议，其他条款仅作提示。"
        )
    return (
        "> **审查策略**：标准模式。高风险和中风险条款给出修改建议，"
        "低风险条款仅作优化提示。"
    )
