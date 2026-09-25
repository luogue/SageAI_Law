"""用户风险画像模块。

画像维度由用户在启动审查前填写，引擎根据画像动态调整审查输出：
- 风险等级个性化（保守/标准/激进）
- 修改建议语气动态调整
- 审查点激活/过滤
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from review_v2.profile_catalog import NEUTRAL_IDENTITY, NEUTRAL_SCENARIO, PROFILE_OPTIONS, ROLE_ALIASES, profile_options

# ---------------------------------------------------------------------------
# 画像维度定义
# ---------------------------------------------------------------------------

USER_IDENTITIES = (NEUTRAL_IDENTITY,)
CONTRACT_SCENARIOS = (NEUTRAL_SCENARIO,)
RISK_APPETITES = ("保守", "标准", "激进")
BARGAINING_POSITIONS = ("强势方", "均衡方", "弱势方")


@dataclass
class UserRiskProfile:
    """用户风险画像——在启动审查前填写。"""

    user_identity: str = NEUTRAL_IDENTITY
    contract_scenario: str = NEUTRAL_SCENARIO
    risk_appetite: str = "标准"
    bargaining_position: str = "均衡方"
    # 跨地域裁判预判用：案件管辖地/用户所在地
    jurisdiction: str = "北京"  # 如：北京、上海、广州、深圳、杭州、成都 等
    contract_type: str = ""

    # ---------- 快速工厂方法 ----------

    @classmethod
    def default(cls) -> UserRiskProfile:
        """无上下文时保持中性，识别合同类型后再生成具体画像。"""
        return cls()

    @classmethod
    def conservative_individual_tenant(cls) -> UserRiskProfile:
        """保守个人租客——任何风险都要求修改。"""
        return cls(
            user_identity="承租人",
            contract_scenario="居住用途",
            risk_appetite="保守",
            bargaining_position="弱势方",
            contract_type="house_lease",
        )

    @classmethod
    def aggressive_investor(cls) -> UserRiskProfile:
        """激进投资者——仅高风险才要求修改。"""
        return cls(
            user_identity="投资方",
            contract_scenario="股权投资",
            risk_appetite="激进",
            bargaining_position="强势方",
            contract_type="investment",
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            "user_identity": self.user_identity,
            "contract_scenario": self.contract_scenario,
            "risk_appetite": self.risk_appetite,
            "bargaining_position": self.bargaining_position,
            "jurisdiction": self.jurisdiction,
            "contract_type": self.contract_type,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, str]) -> UserRiskProfile:
        # An explicit task review role is authoritative.  Some callers also carry
        # a generic user_identity inferred from the contract subtype; it must not
        # overwrite the party perspective selected for the review.
        d = d if isinstance(d, dict) else {}
        user_identity = d.get("review_role") or d.get("user_identity") or NEUTRAL_IDENTITY
        return cls(
            user_identity=user_identity,
            contract_scenario=d.get("contract_scenario") or NEUTRAL_SCENARIO,
            risk_appetite=d.get("risk_appetite") if d.get("risk_appetite") in RISK_APPETITES else "标准",
            bargaining_position=d.get("bargaining_position") if d.get("bargaining_position") in BARGAINING_POSITIONS else "均衡方",
            jurisdiction=d.get("jurisdiction") or "北京",
            contract_type=d.get("contract_type") or "",
        )


def normalize_profile(profile: Optional[UserRiskProfile], contract_type: str,
                      previous_type: str = "") -> UserRiskProfile:
    """Copy and scope contextual fields after classification; retain preferences.

    Old clients may omit ownership. Validate their roles and discard rental
    defaults outside rental contracts instead of trusting unscoped strings.
    """
    key = "house_lease" if contract_type == "lease" else contract_type
    source = (profile or UserRiskProfile.default()).to_dict()
    options = profile_options(key)
    owner = source.get("contract_type") or previous_type
    owner = "house_lease" if owner == "lease" else owner
    changed = bool(owner and owner != key)
    identity = str(source.get("user_identity") or "")
    scenario = str(source.get("contract_scenario") or "")
    legacy = {"个人租客/买方", "个人租客", "小微企业（≤50人）", "中型企业（50-500人）", "大型企业/投资者"}
    if key not in PROFILE_OPTIONS:
        identity, scenario = NEUTRAL_IDENTITY, NEUTRAL_SCENARIO
    else:
        if identity not in legacy and identity not in options["identities"]:
            identity = next((identity.replace(alias, role) for alias, role in ROLE_ALIASES.get(key, {}).items() if alias in identity), identity)
        valid_role = identity in options["identities"] or any(
            role in identity for role in options["identities"] if role != NEUTRAL_IDENTITY
        )
        # Technical subtypes resolve party labels against the document later.
        if key == "technology" and identity not in legacy and not any(s in identity for s in ("租客", "承租", "出租")):
            valid_role = True
        if changed or identity in legacy or not valid_role or (identity == NEUTRAL_IDENTITY and not source.get("contract_type")):
            identity = options["identities"][0]
        rental_scenario = (any(s in scenario for s in ("居住用途", "投资/转租"))
                           or ("租赁" in scenario and key != "finance_lease"))
        foreign_scenario = any(scenario in values[1] for t, values in PROFILE_OPTIONS.items() if t != key)
        if (changed or not scenario or scenario == NEUTRAL_SCENARIO
                or (key != "house_lease" and rental_scenario)
                or (not owner and key != "technology" and scenario not in options["scenarios"])
                or (foreign_scenario and scenario not in options["scenarios"])):
            scenario = options["scenarios"][0]
    return UserRiskProfile.from_dict({**source, "user_identity": identity,
                                     "contract_scenario": scenario, "contract_type": key})


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
    "承租人": (
        # 押金、维修、提前解约、隐私安全
        "HL-003", "HL-006", "HL-007", "HL-014", "HL-015", "HL-016",
        "HL-017", "HL-018", "HL-019", "HL-024", "HL-025", "HL-026",
        "HL-029", "HL-030", "HL-031", "HL-032", "HL-034", "HL-036",
        "HL-037",
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
    if profile.contract_type not in {"house_lease", "lease"}:
        return priorities
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
