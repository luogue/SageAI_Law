"""Gift-contract adjudication configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from adjudicate.lease_configs import MOUNT_POST, PatchMount


Terms = Tuple[str, ...]
PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class GiftConfig:
    key: str
    display_name: str
    fact_mapping: Dict[str, str]
    reused_modules: Terms
    patch_mounts: PatchMounts = field(default_factory=tuple)
    terms: Dict[str, Terms] = field(default_factory=dict)

    @property
    def enabled_patches(self) -> Terms:
        return tuple(mount.patch_id for mount in self.patch_mounts)

    def get_terms(self, key: str) -> Terms:
        return self.terms.get(key, ())

    def patch_mount(self, patch_id: str) -> PatchMount | None:
        return next((mount for mount in self.patch_mounts if mount.patch_id == patch_id), None)

    def patch_name(self, patch_id: str, fallback: str) -> str:
        mount = self.patch_mount(patch_id)
        return mount.patch_name if mount and mount.patch_name else fallback


GIFT_CONFIG = GiftConfig(
    key="gift",
    display_name="赠与合同",
    fact_mapping={
        "合同主体": "赠与人/受赠人/赠与人的继承人或法定代理人",
        "核心义务": "无偿给予财产（赠与人）/ 表示接受（受赠人）",
        "归责原则": "赠与人一般不承担瑕疵担保责任；附义务赠与、故意不告知或保证无瑕疵等情形除外",
        "核心争议": "合同性质认定 → 赠与类型识别 → 撤销权是否成立（任意/法定/继承人撤销）→ 是否应交付或赔偿",
    },
    reused_modules=("管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"),
    patch_mounts=(
        PatchMount("G1", "contract_nature", MOUNT_POST, "赠与合同的性质认定", "合同名称或内容模糊，双方对合同性质存在争议", "《民法典》第657条", "按是否存在无偿给予和受赠人接受认定赠与合同性质", "合同性质认定为 [赠与合同/买卖合同/其他合同]。"),
        PatchMount("G2", "arbitrary_revocation", MOUNT_POST, "任意撤销权的行使条件", "赠与人主张撤销赠与", "《民法典》第658条", "财产权利转移前可撤销；公证、公益、道德义务性质赠与除外", "赠与人任意撤销权 [成立/不成立]。"),
        PatchMount("G3", "statutory_revocation", MOUNT_POST, "法定撤销权的行使条件", "赠与人主张法定撤销权", "《民法典》第663条", "有严重侵害、不履行扶养义务或不履行约定义务，且一年内行使的，可撤销并请求返还", "法定撤销权 [成立/不成立]。"),
        PatchMount("G4", "heir_revocation", MOUNT_POST, "继承人/法定代理人的撤销权", "赠与人的继承人或法定代理人主张撤销赠与", "《民法典》第664条", "受赠人违法行为致赠与人死亡或丧失民事行为能力，六个月内行使的，可撤销", "继承人/法定代理人撤销权 [成立/不成立]。"),
        PatchMount("G5", "compulsory_delivery", MOUNT_POST, "公证/公益赠与的强制履行与赔偿责任", "公证赠与或公益/道德义务赠与的受赠人请求交付", "《民法典》第660条", "赠与人不交付的，受赠人可请求交付；故意或重大过失致毁损灭失的，赠与人赔偿", "赠与人 [应/不应] 交付赠与财产。"),
        PatchMount("G6", "obligation_attached", MOUNT_POST, "附义务赠与的履行与责任", "赠与附有义务，受赠人未履行或赠与财产有瑕疵", "《民法典》第661条、第662条", "受赠人应履行约定义务；财产瑕疵时赠与人在附义务限度内承担出卖人同等责任", "受赠人 [已/未] 履行约定义务。"),
        PatchMount("G7", "defect_warranty", MOUNT_POST, "赠与人瑕疵担保责任的免除与例外", "赠与财产有瑕疵，受赠人主张赔偿", "《民法典》第662条", "一般赠与瑕疵赠与人不担责；附义务、故意不告知或保证无瑕疵除外", "赠与人 [不承担/承担] 瑕疵担保责任。"),
        PatchMount("G8", "poverty_defense", MOUNT_POST, "穷困抗辩权", "赠与人主张不再履行赠与义务", "《民法典》第666条", "赠与人经济状况显著恶化且严重影响生产经营或家庭生活的，可以不再履行", "穷困抗辩权 [成立/不成立]。"),
        PatchMount("G9", "return_after_revocation", MOUNT_POST, "赠与合同撤销后的财产返还", "撤销权人已行使撤销权", "《民法典》第665条", "撤销权成立后，受赠人应返还赠与财产；不能返还的折价赔偿", "撤销权成立，受赠人应返还赠与财产。"),
        PatchMount("G10", "registration", MOUNT_POST, "赠与财产需办理登记手续的处理", "赠与财产依法需要办理登记或者其他手续", "《民法典》第659条", "不动产等财产赠与以登记办理判断权利是否转移", "赠与财产 [已/未] 办理登记手续。"),
        PatchMount("G11", "termination_vs_revocation", MOUNT_POST, "赠与合同的任意解除 vs 撤销", "赠与人主张解除赠与合同", "赠与合同撤销权规则", "赠与人的反悔应定性为撤销，而非解除", "赠与人主张的‘解除’应定性为‘撤销’。"),
        PatchMount("G12", "donee_predeceased", MOUNT_POST, "受赠人先于赠与人死亡的处理", "受赠人在赠与人交付财产前死亡", "赠与合同人身属性规则", "受赠人先于赠与人死亡的，赠与合同终止，赠与人无需继续履行", "受赠人先于赠与人死亡，赠与合同终止。"),
        PatchMount("G13", "waiver_revocation", MOUNT_POST, "赠与人与受赠人约定不得撤销的效力", "赠与合同约定赠与人不得撤销", "赠与合同意思自治规则", "约定放弃任意撤销权有效，但不影响法定撤销权", "赠与人已放弃任意撤销权，不得行使任意撤销权。"),
        PatchMount("G14", "heir_performance", MOUNT_POST, "赠与人的继承人是否应继续履行赠与义务", "赠与人死亡，受赠人请求继承人继续履行", "赠与合同人身属性及第660条", "一般赠与继承人无需履行；公证、公益、道德义务赠与的继承人在遗产范围内履行", "继承人 [应/不应] 继续履行赠与义务。"),
        PatchMount("G15", "limitation_period", MOUNT_POST, "赠与合同纠纷的诉讼时效与除斥期间区分", "需要确定权利行使期限", "《民法典》第663条、第664条及诉讼时效规则", "撤销权适用1年或6个月除斥期间；其他请求权适用3年诉讼时效", "撤销权行使期限为除斥期间 [1年/6个月]。"),
    ),
    terms={
        "jurisdiction_question": ("哪里起诉", "去哪里起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
        "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "适格被告"),
        "gift_contract": ("赠与合同", "赠与", "赠送", "无偿给予", "无偿赠与", "受赠人", "赠与人"),
        "contract_date": ("签订赠与合同", "合同签订", "承诺赠与", "表示赠与", "知道撤销事由", "请求交付", "撤销赠与"),
        "third_party_tort": ("第三人侵权", "外人侵权", "他人侵权"),
        "deadline_question": ("期限", "除斥期间", "诉讼时效", "超过一年", "超过6个月", "超过六个月", "撤销期限"),
        "nature_dispute": ("合同性质争议", "到底是赠与还是买卖", "名为赠与", "实为买卖", "性质不明", "合同性质"),
        "gratuitous_intent": ("无偿给予", "无偿赠与", "免费赠送", "不要对价", "不收钱", "赠送"),
        "donee_accepts": ("受赠人表示接受", "受赠人接受", "接受赠与", "同意接受"),
        "no_acceptance": ("未表示接受", "拒绝接受", "没有接受赠与"),
        "consideration": ("支付价款", "有偿转让", "对价", "买卖", "付款购买"),
        "betrothal_or_romance": ("彩礼", "恋爱期间", "恋爱赠与", "以结婚为目的", "大额赠与"),
        "equity_incentive": ("股权激励", "激励协议", "赠与股权"),
        "contract_invalid": ("合同无效", "无效合同", "违反强制性规定"),
        "notarized_gift": ("公证赠与", "经过公证", "赠与合同公证", "公证的赠与"),
        "public_welfare_gift": ("救灾", "扶贫", "助残", "公益赠与", "慈善捐赠", "公益性质"),
        "moral_obligation_gift": ("道德义务", "赡养补偿", "抚养补偿", "报恩"),
        "obligation_attached": ("附义务赠与", "附条件赠与", "约定义务", "附有义务", "要求受赠人履行义务"),
        "registration_required": ("不动产", "房屋", "房产", "车辆过户", "股权登记", "需要登记", "办理登记"),
        "registration_done": ("已经过户", "已办理登记", "完成登记", "已登记"),
        "right_transferred": ("权利已转移", "已经交付", "已经过户", "已办理登记", "动产已交付"),
        "not_transferred": ("尚未交付", "未交付", "未过户", "未办理登记", "权利未转移"),
        "arbitrary_revocation_claim": ("任意撤销", "撤销赠与", "反悔", "不想赠与", "收回赠与"),
        "termination_word": ("解除赠与合同", "解除合同", "要求解除赠与"),
        "waiver_revocation_agreement": ("不得撤销", "放弃任意撤销权", "约定不得撤销", "不可撤销约定"),
        "statutory_revocation_claim": ("法定撤销", "依法撤销", "因受赠人行为撤销"),
        "serious_infringement": ("严重侵害赠与人", "严重侵害近亲属", "殴打赠与人", "虐待赠与人", "侵害合法权益"),
        "support_duty_unfulfilled": ("不履行扶养义务", "不赡养", "拒绝扶养", "有扶养义务而不履行"),
        "agreed_obligation_unfulfilled": ("不履行约定义务", "未履行约定义务", "没有履行附义务", "违反约定义务"),
        "within_one_year": ("一年内", "未超过一年", "在一年内"),
        "over_one_year": ("超过一年", "超过1年", "一年后", "已过一年"),
        "heir_or_agent_revocation": ("继承人撤销", "法定代理人撤销", "继承人主张撤销", "法定代理人主张撤销"),
        "donee_illegal_act": ("受赠人违法行为", "违法行为", "犯罪行为"),
        "donor_dead": ("赠与人死亡", "致赠与人死亡"),
        "donor_incapacitated": ("丧失民事行为能力", "致赠与人丧失行为能力"),
        "within_six_months": ("六个月内", "6个月内", "未超过六个月", "未超过6个月"),
        "over_six_months": ("超过六个月", "超过6个月", "六个月后", "6个月后"),
        "delivery_claim": ("请求交付", "要求交付", "要求履行赠与", "继续履行赠与"),
        "property_not_delivered": ("不交付", "拒绝交付", "未交付赠与财产"),
        "property_destroyed": ("毁损", "灭失", "财产损坏", "财产灭失"),
        "donor_intent_gross": ("故意", "重大过失", "故意或者重大过失"),
        "force_majeure": ("不可抗力", "自然灾害"),
        "donee_obligation_performed": ("已履行约定义务", "完成约定义务", "履行了义务"),
        "gift_property_defect": ("瑕疵", "质量问题", "有缺陷", "赠与财产有瑕疵"),
        "deliberate_non_disclosure": ("故意不告知瑕疵", "隐瞒瑕疵", "明知瑕疵未告知"),
        "guaranteed_no_defect": ("保证无瑕疵", "承诺没有瑕疵", "保证质量没问题"),
        "poverty_defense": ("穷困抗辩", "不再履行赠与义务", "经济状况恶化", "无力赠与"),
        "economic_deteriorated": ("经济状况显著恶化", "破产", "负债严重", "收入骤降"),
        "serious_life_impact": ("严重影响家庭生活", "严重影响生产经营", "生活困难", "经营困难"),
        "revocation_exercised": ("已经撤销赠与", "撤销权成立", "已行使撤销权"),
        "return_claim": ("请求返还", "要求返还赠与财产", "返还财产", "返还赠与物"),
        "property_unreturnable": ("无法返还", "不能返还", "已经处分", "已经灭失"),
        "donee_predeceased": ("受赠人先于赠与人死亡", "受赠人先死亡", "交付前受赠人死亡"),
        "donor_dead_inheritance_request": ("赠与人死亡后", "赠与人去世后", "请求继承人继续履行", "继承人继续履行"),
        "actual_loss": ("损失", "赔偿", "损失金额", "折价赔偿", "财产价值"),
        "property_value": ("财产价值", "赠与财产价值", "价值", "折价赔偿"),
    },
)


GIFT_CONFIGS: Dict[str, GiftConfig] = {GIFT_CONFIG.key: GIFT_CONFIG}


def get_gift_config(contract_type: str | None = None) -> GiftConfig:
    key = (contract_type or "gift").strip().lower()
    aliases = {
        "donation": "gift",
        "gift_contract": "gift",
        "赠与": "gift",
        "赠与合同": "gift",
        "捐赠": "gift",
    }
    return GIFT_CONFIGS.get(aliases.get(key, key), GIFT_CONFIG)
