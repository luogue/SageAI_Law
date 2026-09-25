"""Commission-agency-contract adjudication configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from adjudicate.lease_configs import MOUNT_POST, PatchMount


Terms = Tuple[str, ...]
PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class CommissionAgencyConfig:
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


COMMISSION_AGENCY_CONFIG = CommissionAgencyConfig(
    key="commission_agency",
    display_name="行纪合同",
    fact_mapping={
        "合同主体": "行纪人/委托人",
        "核心义务": "行纪人以自己名义为委托人从事贸易活动；委托人支付报酬并受领委托物",
        "归责原则": "行纪人对第三人违约承担赔偿责任，另有约定的除外",
        "核心争议": "合同性质认定 → 行纪人是否按指示行事 → 第三人是否履行义务 → 报酬是否支付",
    },
    reused_modules=("管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"),
    patch_mounts=(
        PatchMount("J1", "contract_nature", MOUNT_POST, "行纪合同的性质认定", "合同名称或内容模糊，双方对合同性质存在争议", "《民法典》第951条", "按是否以自己名义为委托人从事贸易活动认定合同性质", "合同性质认定为 [行纪合同/委托合同/中介合同/买卖合同]。"),
        PatchMount("J2", "price_instruction", MOUNT_POST, "行纪人违反价格指示的处理", "行纪人未按委托人指定价格交易", "《民法典》第955条", "低卖高买须经同意或补差；高卖低买利益无约定归委托人；特别指示不得违反", "行纪人 [已/未] 遵守价格指示，差价利益归 [委托人/按约定]。"),
        PatchMount("J3", "intervention_right", MOUNT_POST, "行纪人介入权的行使条件", "行纪人主张自己作为买受人或者出卖人", "《民法典》第956条", "市场定价商品且委托人无相反意思表示的，行纪人可以介入并请求报酬", "行纪人介入权 [成立/不成立]。"),
        PatchMount("J4", "third_party_default", MOUNT_POST, "行纪人对第三人违约的责任承担", "第三人不履行义务致使委托人受损", "《民法典》第958条", "行纪人与第三人合同由行纪人直接享权担责；第三人违约造成委托人损失的，行纪人赔偿，另有约定除外", "第三人不履行义务，行纪人 [应/不应] 承担赔偿责任。"),
        PatchMount("J5", "lien_right", MOUNT_POST, "行纪人留置权的行使", "委托人逾期不支付报酬", "《民法典》第959条", "行纪人完成或部分完成事务后，委托人逾期不付报酬的，行纪人对委托物享有留置权，另有约定除外", "行纪人留置权 [成立/不成立]。"),
        PatchMount("J6", "deposit_right", MOUNT_POST, "行纪人提存权的行使", "委托人无正当理由拒绝受领或取回委托物", "《民法典》第957条", "催告后无正当理由拒绝受领、取回或处分委托物的，行纪人可以提存", "行纪人提存权 [成立/不成立]。"),
        PatchMount("J7", "defective_goods_disposal", MOUNT_POST, "委托物瑕疵/易变质时的处分权", "委托物交付时有瑕疵或容易腐烂变质", "《民法典》第954条", "经委托人同意可处分；不能及时联系的可合理处分，所得转交委托人", "行纪人处分委托物 [合规/不合规]。"),
        PatchMount("J8", "custody_duty", MOUNT_POST, "行纪人妥善保管义务", "委托物在行纪人占有期间毁损灭失", "《民法典》第953条", "行纪人占有委托物的，应妥善保管；未尽义务的赔偿", "行纪人 [已/未] 尽到妥善保管义务。"),
        PatchMount("J9", "expense_burden", MOUNT_POST, "行纪人费用负担", "行纪人主张委托人承担处理事务费用", "《民法典》第952条", "处理委托事务支出的费用由行纪人负担，另有约定除外", "处理委托事务费用由 [行纪人/按约定] 负担。"),
        PatchMount("J10", "malicious_collusion", MOUNT_POST, "行纪人与第三人恶意串通", "行纪人与第三人恶意串通损害委托人利益", "《民法典》第577条及诚信义务", "恶意串通损害委托人利益的，行纪人承担全部赔偿责任", "行纪人与第三人存在恶意串通，行纪人承担全部赔偿责任。"),
        PatchMount("J11", "remuneration", MOUNT_POST, "行纪合同报酬的确定", "当事人未约定报酬或约定不明", "《民法典》第959条", "完成或部分完成委托事务的，应支付报酬；无约定可按交易习惯或公平原则确定", "报酬 [按约定/酌情确定]。"),
        PatchMount("J12", "sub_entrustment", MOUNT_POST, "行纪合同与转委托", "行纪人将委托事务转交第三人处理", "《民法典》第960条、第923条", "经同意转委托的仅就选任和指示负责；未经同意的对第三人行为承担全部责任", "转委托 [经同意/未经同意]，行纪人 [有限/全部] 负责。"),
        PatchMount("J13", "termination", MOUNT_POST, "行纪合同的任意解除权", "委托人或行纪人主张解除合同", "《民法典》第960条、第933条", "参照委托合同任意解除；有偿行纪赔偿直接损失和可得利益，无偿或时间不当解除赔偿直接损失", "行纪合同解除有效，赔偿范围为 [直接损失/直接损失+可得利益]。"),
        PatchMount("J14", "identity_confusion", MOUNT_POST, "行纪人身份混同的处理", "行纪人身份混同，无法证明委托物属于行纪事务", "行纪合同证明责任规则", "身份混同且无法证明货物为行纪事务项下委托物的，行纪人主张不成立", "行纪人身份 [明确/混同]，主张 [成立/不成立]。"),
        PatchMount("J15", "oral_contract", MOUNT_POST, "行纪合同未采用书面形式", "行纪合同未采用书面形式", "《民法典》第951条", "行纪合同不强制书面形式；有证据证明行纪关系存在的，合同成立", "行纪合同 [成立/不成立]。"),
    ),
    terms={
        "jurisdiction_question": ("哪里起诉", "去哪里起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
        "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "适格被告"),
        "commission_agency_contract": ("行纪合同", "行纪人", "委托人", "行纪事务", "寄售", "代购", "代销", "贸易活动"),
        "contract_date": ("签订行纪合同", "合同签订", "交付委托物", "完成委托事务", "支付报酬", "催告"),
        "third_party_tort": ("第三人侵权", "外人侵权", "他人侵权"),
        "nature_dispute": ("合同性质争议", "行纪还是委托", "名为委托实为行纪", "合同性质不明", "名为买卖实为行纪"),
        "own_name_trade": ("以自己名义", "行纪人自己名义", "自己名义与第三人交易", "以行纪人名义"),
        "principal_name": ("以委托人名义", "代理委托人", "受托人以委托人名义"),
        "intermediary_service": ("报告订约机会", "媒介服务", "中介合同", "居间"),
        "sale_contract": ("买卖合同", "转移所有权", "自己买卖", "标准买卖"),
        "trade_activity": ("贸易活动", "购销", "代购", "代销", "寄售", "买入卖出"),
        "oral_contract": ("口头约定", "未签书面合同", "没有书面合同", "口头行纪"),
        "evidence_exists": ("有聊天记录", "有交易记录", "有证据证明", "有委托凭证", "有转账记录"),
        "identity_confusion": ("身份混同", "职务身份混同", "无法区分身份", "不能证明委托物"),
        "custody_damage": ("委托物毁损", "委托物灭失", "委托物损坏", "保管不善", "占有期间毁损"),
        "proper_custody": ("妥善保管", "已尽保管义务", "无保管过错"),
        "improper_custody": ("未妥善保管", "保管不善", "行纪人过错"),
        "expense_claim": ("费用", "支出费用", "处理事务费用", "要求报销费用"),
        "expense_agreed": ("费用另有约定", "约定费用由委托人承担", "按约定负担费用"),
        "third_party_contract": ("与第三人订立合同", "和第三人签合同", "第三人交易"),
        "third_party_default": ("第三人不履行", "第三人违约", "第三人未付款", "第三人不交货"),
        "principal_loss": ("委托人受损", "委托人受到损害", "造成委托人损失", "损失"),
        "liability_excluded_agreed": ("另有约定免责", "约定第三人风险由委托人承担", "免责约定"),
        "malicious_collusion": ("恶意串通", "串通第三人", "与第三人串通", "损害委托人利益"),
        "price_instruction": ("指定价格", "价格指示", "最低价", "最高价", "特别指示"),
        "low_sell": ("低于指定价格卖出", "低价卖出", "低于最低价卖出"),
        "high_buy": ("高于指定价格买入", "高价买入", "高于最高价买入"),
        "high_sell": ("高于指定价格卖出", "高价卖出", "高于最低价卖出"),
        "low_buy": ("低于指定价格买入", "低价买入", "低于最高价买入"),
        "principal_consent": ("经委托人同意", "委托人同意", "事后追认"),
        "difference_compensated": ("补偿差额", "补足差额", "赔偿差价"),
        "special_instruction": ("特别指示", "不得低于", "不得高于", "严格价格"),
        "market_priced_goods": ("市场定价", "有市场价格", "交易所定价", "公开市场价格"),
        "intervention_claim": ("介入权", "自己作为买受人", "自己作为出卖人", "自行买入", "自行卖出"),
        "contrary_expression": ("相反意思表示", "明确反对介入", "不同意自行买卖"),
        "defective_or_perishable": ("有瑕疵", "容易腐烂", "容易变质", "易腐", "易变质"),
        "disposal_claim": ("处分委托物", "合理处分", "卖掉变质货物", "处置委托物"),
        "cannot_contact": ("无法联系委托人", "不能及时取得联系", "联系不上"),
        "proceeds_transfer": ("处分所得转交", "所得转交委托人"),
        "buy_in": ("按约定买入委托物", "买入委托物", "代购完成"),
        "refuse_accept": ("拒绝受领", "不受领", "无正当理由拒收"),
        "cannot_sell": ("不能卖出", "卖不出去"),
        "withdraw_sale": ("撤回出售", "撤销出售", "不卖了"),
        "refuse_take_back": ("不取回", "拒绝取回", "不处分委托物"),
        "urged": ("催告", "经催告", "书面催告"),
        "deposit_claim": ("提存", "提存委托物"),
        "remuneration_claim": ("报酬", "佣金", "行纪报酬", "服务费"),
        "remuneration_unpaid": ("未支付报酬", "拖欠报酬", "逾期不支付报酬", "拒付报酬"),
        "matter_completed": ("完成委托事务", "部分完成委托事务", "交易完成", "已经完成"),
        "remuneration_agreed": ("约定报酬", "报酬有约定", "约定佣金"),
        "remuneration_unclear": ("未约定报酬", "报酬约定不明", "佣金不明"),
        "lien_claim": ("留置", "留置权", "留置委托物"),
        "lien_excluded": ("排除留置权", "不得留置", "另有约定不得留置"),
        "sub_entrustment": ("转委托", "转交第三人处理", "交给第三人处理"),
        "sub_entrustment_consent": ("经委托人同意转委托", "同意转委托", "授权转委托"),
        "termination_request": ("解除行纪合同", "解除合同", "任意解除", "随时解除"),
        "paid_commission": ("有偿行纪", "有偿合同", "约定报酬"),
        "unpaid_commission": ("无偿行纪", "无偿"),
        "termination_loss": ("解除造成损失", "直接损失", "可得利益损失"),
        "actual_loss": ("损失", "赔偿", "损失金额", "差额", "差价"),
    },
)


COMMISSION_AGENCY_CONFIGS: Dict[str, CommissionAgencyConfig] = {
    COMMISSION_AGENCY_CONFIG.key: COMMISSION_AGENCY_CONFIG,
}


def get_commission_agency_config(contract_type: str | None = None) -> CommissionAgencyConfig:
    key = (contract_type or "commission_agency").strip().lower()
    aliases = {
        "commission": "commission_agency",
        "commission_contract": "commission_agency",
        "commission_agency_contract": "commission_agency",
        "行纪": "commission_agency",
        "行纪合同": "commission_agency",
    }
    return COMMISSION_AGENCY_CONFIGS.get(aliases.get(key, key), COMMISSION_AGENCY_CONFIG)
