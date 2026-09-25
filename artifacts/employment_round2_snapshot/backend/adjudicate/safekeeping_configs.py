"""Safekeeping-contract adjudication configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from adjudicate.lease_configs import MOUNT_POST, PatchMount


Terms = Tuple[str, ...]
PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class SafekeepingConfig:
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

    def patch_ids_at(self, node_id: str, mount_mode: str) -> Terms:
        return tuple(
            mount.patch_id
            for mount in self.patch_mounts
            if mount.node_id == node_id and mount.mount_mode == mount_mode
        )

    def patch_mount(self, patch_id: str) -> PatchMount | None:
        return next((mount for mount in self.patch_mounts if mount.patch_id == patch_id), None)

    def patch_name(self, patch_id: str, fallback: str) -> str:
        mount = self.patch_mount(patch_id)
        return mount.patch_name if mount and mount.patch_name else fallback


SAFEKEEPING_CONFIG = SafekeepingConfig(
    key="deposit",
    display_name="保管合同",
    fact_mapping={
        "合同主体": "保管人/寄存人",
        "核心义务": "保管并返还原物（保管人不得使用）",
        "归责原则": "有偿=一般过失；无偿=故意或重大过失",
        "核心争议": "保管物是否毁损/灭失/未返还 → 原因 → 责任标准 → 赔偿多少",
    },
    reused_modules=("管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"),
    patch_mounts=(
        PatchMount(
            "S1",
            "contract_nature",
            MOUNT_POST,
            "保管合同与租赁合同/场地租赁合同的定性",
            "合同名称或内容模糊，双方对合同性质存在争议",
            "《民法典》第888条",
            "根据合同目的、保管人是否实际控制保管物、是否只提供场地，认定为保管合同、租赁合同或场地租赁合同",
            "合同性质认定为 [保管合同/租赁合同/场地租赁合同]，适用相应裁判规则。",
        ),
        PatchMount(
            "S2",
            "liability_standard",
            MOUNT_POST,
            "有偿保管与无偿保管的责任标准",
            "保管物在保管期间毁损或灭失",
            "《民法典》第889条、第897条",
            "有偿保管适用一般过失责任；无偿保管仅在保管人故意或重大过失时承担责任",
            "保管合同为 [有偿/无偿]，保管人责任标准为 [一般过失/故意或重大过失]。",
        ),
        PatchMount(
            "S3",
            "custodian_obligation",
            MOUNT_POST,
            "保管人擅自转保管",
            "保管人将保管物转交第三人保管",
            "《民法典》第894条",
            "未经约定擅自转交第三人保管并造成损失的，保管人应赔偿",
            "转保管 [经约定/未经约定]，保管人 [不承担/承担] 赔偿责任。",
        ),
        PatchMount(
            "S4",
            "custodian_obligation",
            MOUNT_POST,
            "保管人擅自使用保管物",
            "保管人使用或许可第三人使用保管物",
            "《民法典》第895条",
            "未经约定使用或许可第三人使用保管物，造成损耗或损坏的应赔偿",
            "保管人 [经约定/未经约定] 使用保管物，[不承担/承担] 赔偿责任。",
        ),
        PatchMount(
            "S5",
            "compensation_amount",
            MOUNT_POST,
            "贵重物品未声明",
            "寄存人寄存货币、有价证券或其他贵重物品，未向保管人声明",
            "《民法典》第898条",
            "未声明贵重物品的，毁损灭失后按一般物品价值赔偿",
            "寄存人 [已/未] 声明贵重物品，赔偿按 [实际价值/一般物品价值] 计算。",
        ),
        PatchMount(
            "S6",
            "compensation_amount",
            MOUNT_POST,
            "消费保管",
            "保管物为货币或其他可替代物",
            "《民法典》第901条",
            "消费保管返还相同种类、品质、数量的货币或物品，而非必须返还原物",
            "属于消费保管，保管人应返还相同种类、数量、品质的货币或物品。",
        ),
        PatchMount(
            "S7",
            "custodian_lien",
            MOUNT_POST,
            "保管人留置权",
            "寄存人未按约定支付保管费或其他费用",
            "《民法典》第903条",
            "费用到期未付的，保管人可以留置保管物；另有约定排除或行使不当的除外",
            "保管人留置权 [成立/不成立]。",
        ),
        PatchMount(
            "S8",
            "return_item",
            MOUNT_POST,
            "寄存人随时领取权",
            "寄存人要求提前领取保管物",
            "《民法典》第899条、第900条",
            "寄存人可以随时领取保管物，保管人应返还保管物及孳息，保管费按实际保管期间计算",
            "寄存人有权随时领取，保管人应返还保管物及孳息。",
        ),
        PatchMount(
            "S9",
            "loss_cause",
            MOUNT_POST,
            "保管物自身性质导致的损失",
            "保管物因自身性质、瑕疵或特殊保管需求导致毁损灭失",
            "《民法典》第893条",
            "寄存人未告知保管物瑕疵或特殊保管需求导致损失的，保管人不承担赔偿责任",
            "保管物自身性质导致损失，寄存人 [已/未] 履行告知义务，保管人 [承担/不承担] 赔偿责任。",
        ),
        PatchMount(
            "S10",
            "return_item",
            MOUNT_POST,
            "保管合同终止后的逾期领取",
            "保管期限届满后，寄存人逾期未领取保管物",
            "《民法典》第899条、第900条、第902条",
            "保管人可催告寄存人在合理期限内领取；逾期产生的额外保管费用由寄存人承担",
            "保管期限已届满，寄存人应在合理期限内领取，逾期费用由寄存人承担。",
        ),
    ),
    terms={
        "jurisdiction_question": ("哪里起诉", "去哪里起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
        "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "告对人"),
        "safekeeping_contract": ("保管合同", "寄存合同", "寄存", "保管物", "保管人", "寄存人", "仓储保管"),
        "contract_invalid": ("合同无效", "无效合同", "违法无效", "合同不成立"),
        "delivery_date": ("交付", "交给", "寄存", "保管开始", "应返还", "领取", "保管期满"),
        "third_party_tort": ("路人侵权", "第三方侵权", "他人损害", "外人造成", "陌生人破坏"),
        "contract_nature_dispute": ("合同性质争议", "性质有争议", "到底是保管还是租赁", "名为保管", "名为租赁", "名为场地租赁", "实为保管", "实为租赁"),
        "purpose_keep_return": ("保管并返还原物", "代为保管", "负责看管", "专人看管", "上锁保管", "返还原物", "保管人实际控制"),
        "transfer_use_right": ("转移使用权", "租用", "租赁", "借用", "自行使用", "使用权"),
        "venue_only": ("仅提供场地", "只提供场地", "场地租赁", "租用仓位", "自行存放", "不负责看管", "自助存放"),
        "custodian_actual_control": ("保管人实际控制", "交给保管人", "保管人收取保管物", "专人看管", "统一保管", "存放在指定柜台", "指定场所"),
        "designated_place_activity": ("购物", "就餐", "住宿", "饭店", "酒店", "商场", "指定柜台", "指定场所", "前台寄存"),
        "item_delivered": ("已交付保管物", "交给保管人", "交付给保管人", "寄存给保管人", "保管人接收", "保管开始"),
        "item_not_delivered": ("尚未交付", "未交付保管物", "交付前", "还没交给保管人", "未实际交付"),
        "before_delivery": ("交付前已经损坏", "交付前丢失", "交给保管人前", "保管开始前", "尚未交付时损坏"),
        "after_retrieval": ("领取后损坏", "取回后丢失", "返还后损坏", "保管结束后", "领取以后"),
        "during_safekeeping": ("保管期间", "寄存期间", "保管过程中", "保管期内", "交给保管人后"),
        "paid_safekeeping": ("有偿保管", "约定保管费", "收取保管费", "付费保管", "收费保管"),
        "unpaid_safekeeping": ("无偿保管", "免费保管", "没有保管费", "未约定保管费", "保管费约定不明", "无保管费约定"),
        "fee_unclear": ("保管费约定不明", "费用约定不明", "没有约定费用", "未约定保管费"),
        "unpaid_fee": ("未支付保管费", "欠保管费", "拖欠保管费", "拒付保管费", "保管费未付", "未支付其他费用"),
        "fee_amount": ("保管费", "费用", "欠费", "拖欠"),
        "lien": ("留置", "扣留保管物", "拒绝返还并要求付费", "行使留置权"),
        "lien_excluded_by_contract": ("不得留置", "禁止留置", "排除留置权", "合同约定不能留置"),
        "improper_lien": ("超额留置", "不当留置", "留置全部物品", "留置价值明显超过欠费"),
        "item_damage": ("损坏", "毁损", "破损", "损毁", "受损", "变坏", "变质"),
        "item_loss": ("丢失", "灭失", "遗失", "不见", "找不到", "被盗"),
        "non_return": ("未返还", "拒绝返还", "无法返还", "不返还", "不归还"),
        "force_majeure": ("不可抗力", "洪水", "地震", "台风", "自然灾害", "火灾不可抗力"),
        "item_nature_defect": ("自身性质", "自身瑕疵", "易腐", "变质", "易挥发", "易自燃", "特殊保管需求", "冷藏要求", "恒温要求"),
        "depositor_disclosed": ("已经告知", "已声明", "已说明", "提前告知", "交付时告知", "告知特殊保管需求"),
        "depositor_not_disclosed": ("未告知", "没有告知", "未声明", "没有声明", "隐瞒", "未说明"),
        "depositor_fault": ("寄存人过错", "寄存人原因", "寄存人包装不当", "寄存人操作不当"),
        "third_party_fault": ("第三人过错", "第三人原因", "他人过错", "被第三人破坏"),
        "proper_custody": ("妥善保管", "尽到保管义务", "合理保管", "按约定保管", "保管措施合理"),
        "improper_custody": ("保管不善", "未妥善保管", "未尽保管义务", "未尽妥善保管义务", "未按约定保管", "看管不善", "管理不善", "未上锁"),
        "custodian_general_negligence": ("一般过失", "疏忽", "注意义务不足", "未尽善良管理人注意义务"),
        "custodian_intent_gross": ("故意", "重大过失", "明显疏忽", "严重疏忽", "放任损失"),
        "custodian_proves_no_intent_gross": ("证明没有故意或重大过失", "证明自己没有故意或重大过失", "证明无故意或重大过失", "无故意或重大过失", "没有重大过失"),
        "changed_place_method": ("擅自改变保管场所", "擅自改变保管方法", "换地方保管", "改变保管方式"),
        "emergency_or_depositor_interest": ("紧急情况", "维护寄存人利益", "为保护寄存人利益"),
        "transfer_to_third": ("转交第三人保管", "转保管", "交给第三人保管", "委托第三人保管", "转给别人保管"),
        "transfer_agreed": ("约定可以转保管", "经约定转保管", "同意转保管", "经寄存人同意", "合同允许转交第三人"),
        "custodian_used_item": ("擅自使用保管物", "使用保管物", "拿去使用", "开走保管车辆", "佩戴保管物", "动用保管物"),
        "third_party_use": ("许可第三人使用", "让第三人使用", "借给第三人使用"),
        "use_agreed": ("约定可以使用", "经约定使用", "同意使用", "寄存人同意使用"),
        "third_party_claim": ("第三人主张权利", "第三人要求返还", "权利人主张", "他人主张所有权"),
        "third_party_lawsuit_or_seizure": ("第三人起诉", "申请扣押", "法院扣押", "保全", "执行扣押"),
        "custodian_notified_depositor": ("已通知寄存人", "及时通知寄存人", "通知寄存人"),
        "valuable_item": ("贵重物品", "名表", "珠宝", "黄金", "有价证券", "高档手表", "奢侈品", "现金", "货币"),
        "declared_valuable": ("声明贵重物品", "已声明价值", "已声明贵重", "验收", "封存", "保管人验收"),
        "undeclared_valuable": ("未声明贵重物品", "没有声明贵重", "未声明价值", "未向保管人声明", "未验收", "未封存"),
        "consumptive_safekeeping": ("消费保管", "货币保管", "可替代物保管", "保管货币", "保管粮食", "保管燃料", "返还同种类"),
        "currency_item": ("货币", "现金", "钱款", "人民币"),
        "fungible_item": ("可替代物", "粮食", "燃料", "同种类物", "同品质物"),
        "depositor_requests_return": ("要求领取", "提前领取", "随时领取", "要求返还", "取回保管物", "要求归还"),
        "custodian_refuses_return": ("拒绝返还", "拒绝归还", "拒绝领取", "不让取回", "不返还"),
        "fruits_interest": ("孳息", "利息", "收益"),
        "fixed_period": ("约定保管期限", "有保管期限", "固定期限", "保管期"),
        "no_fixed_period": ("无保管期限", "未约定期限", "没有保管期限"),
        "period_expired": ("保管期限届满", "保管期满", "期限届满", "到期后", "保管合同终止"),
        "depositor_overdue_retrieval": ("逾期未领取", "过期不取", "到期不领取", "长期不取", "逾期仍不领取"),
        "custodian_urged_retrieval": ("催告领取", "通知领取", "要求限期领取", "催促寄存人领取"),
        "extra_fee": ("额外保管费", "新增保管费", "逾期费用", "额外费用"),
        "actual_loss": ("损失", "实际损失", "价值", "市值", "市场价值", "物品价值"),
    },
)


SAFEKEEPING_CONFIGS: Dict[str, SafekeepingConfig] = {
    SAFEKEEPING_CONFIG.key: SAFEKEEPING_CONFIG,
}


def get_safekeeping_config(contract_type: str | None = None) -> SafekeepingConfig:
    key = (contract_type or "deposit").strip().lower()
    aliases = {
        "safekeeping": "deposit",
        "custody": "deposit",
        "bailment": "deposit",
        "deposit_contract": "deposit",
        "保管": "deposit",
        "保管合同": "deposit",
        "寄存": "deposit",
    }
    return SAFEKEEPING_CONFIGS.get(aliases.get(key, key), SAFEKEEPING_CONFIG)
