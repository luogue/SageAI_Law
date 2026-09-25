"""Warehouse-contract adjudication configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from adjudicate.lease_configs import MOUNT_POST, PatchMount


Terms = Tuple[str, ...]
PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class WarehouseConfig:
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


WAREHOUSE_CONFIG = WarehouseConfig(
    key="warehouse",
    display_name="仓储合同",
    fact_mapping={
        "合同主体": "保管人（仓储营业人）/存货人",
        "核心义务": "储存保管仓储物（保管人）/ 支付仓储费并按时提取（存货人）",
        "归责原则": "过错责任（保管不善承担赔偿责任；自然性质/包装不符/超期免责）",
        "核心争议": "仓储物是否毁损灭失 → 原因是否为保管不善 → 是否属于免责事由 → 赔偿多少",
    },
    reused_modules=("管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"),
    patch_mounts=(
        PatchMount("W1", "contract_nature", MOUNT_POST, "仓储合同与保管合同的区分认定", "合同名称或内容模糊，双方对合同性质存在争议", "《民法典》第904条、第905条", "以仓储为业、诺成合同、仓单制度指向仓储合同；非商事仓储指向保管合同", "合同性质认定为 [仓储合同/保管合同]，适用 [相应] 裁判规则。"),
        PatchMount("W2", "warehouse_receipt_effect", MOUNT_POST, "仓单的转让与质押效力", "涉及仓单转让或质押", "《民法典》第910条", "背书并经保管人签名或盖章的，转让提货权有效；仓单可设立权利质押", "仓单转让 [有效/无效]，受让人 [取得/未取得] 提货权。"),
        PatchMount("W3", "acceptance_check", MOUNT_POST, "保管人验收义务与责任", "仓储物品种、数量、质量与约定不符", "《民法典》第907条", "保管人应按约验收，发现不符应及时通知；验收后发生不符的承担赔偿责任", "保管人 [已/未] 履行验收义务，[已/未] 及时通知，[应/不应] 承担赔偿责任。"),
        PatchMount("W4", "damage_cause", MOUNT_POST, "保管人免责事由", "仓储物储存期内毁损灭失，保管人主张免责", "《民法典》第917条", "自然性质、包装不符、超过有效储存期造成损失的免责；保管不善的赔偿", "仓储物毁损灭失 [属于/不属于] 保管人免责事由，保管人 [不承担/承担] 赔偿责任。"),
        PatchMount("W5", "overdue_retrieval", MOUNT_POST, "逾期提取的加收费与提存规则", "储存期限届满后未提取仓储物", "《民法典》第915条、第916条", "逾期提取加收仓储费；催告后仍不提取的可提存", "储存期限已届满，存货人逾期未提取，应加收仓储费 [金额] 元。保管人可催告提取，逾期不提取的可提存仓储物。"),
        PatchMount("W6", "dangerous_goods", MOUNT_POST, "危险物品/易变质物品的说明义务", "仓储物为危险物品或易变质物品", "《民法典》第906条", "存货人应说明性质并提供资料；违反说明义务的，保管人可拒收或采取措施，费用由存货人负担", "存货人 [已/未] 履行危险物品说明义务，保管人 [可以/不可以] 拒收仓储物，费用由 [存货人/保管人] 承担。"),
        PatchMount("W7", "emergency_disposal", MOUNT_POST, "保管人紧急处置权", "仓储物变质或损坏危及其他仓储物", "《民法典》第913条", "非紧急先催告；紧急时可必要处置并事后通知", "保管人紧急处置权 [成立/不成立]，处置费用由 [存货人/保管人] 承担。"),
        PatchMount("W8", "early_retrieval", MOUNT_POST, "提前提取不减收仓储费", "存货人期限届满前提取仓储物", "《民法典》第915条", "提前提取的，不减收仓储费", "存货人提前提取仓储物，仓储费不减收，应按原约定支付 [金额] 元。"),
        PatchMount("W9", "unclear_storage_period", MOUNT_POST, "储存期限约定不明的处理", "储存期限没有约定或约定不明确", "《民法典》第914条", "双方均可随时主张提取，但应给予必要准备时间", "储存期限约定不明，双方均可随时主张提取，但应给予必要的准备时间。"),
        PatchMount("W10", "contract_termination", MOUNT_POST, "仓储合同解除", "一方主张解除仓储合同", "《民法典》第563条", "审查不可抗力、拒绝履行、迟延履行经催告仍不履行、违约致合同目的不能实现", "仓储合同解除 [成立/不成立]，解除后果为 [恢复原状/赔偿损失]。"),
        PatchMount("W11", "receipt_holder_identity", MOUNT_POST, "仓单持有人身份的认定", "多人主张仓储物提取权", "《民法典》第910条", "合法持有仓单的人有权提取仓储物", "仓单持有人为 [姓名/名称]，有权提取仓储物。"),
        PatchMount("W12", "partial_damage", MOUNT_POST, "仓储物部分毁损/灭失的处理", "仓储物仅部分毁损或灭失", "《民法典》第917条、第584条", "仅赔偿毁损灭失部分，未毁损部分继续返还", "仓储物部分毁损/灭失，保管人应赔偿毁损部分损失 [金额] 元，未毁损部分应予返还。"),
        PatchMount("W13", "notice_failure", MOUNT_POST, "保管人未尽通知义务的责任", "发现仓储物变质或损坏后未及时通知", "《民法典》第912条", "未及时通知导致损失扩大的，对扩大部分承担赔偿责任", "保管人 [已/未] 及时履行通知义务，对扩大损失 [承担/不承担] 赔偿责任。"),
        PatchMount("W14", "depositor_assignment", MOUNT_POST, "存货人变更/转让后的权利义务", "存货人将仓储物转让给第三人", "《民法典》第910条及合同转让规则", "有效转让后，受让人承继提货权和仓储费等义务", "仓储物已转让，受让人 [承继/不承继] 存货人的权利义务。"),
        PatchMount("W15", "value_depreciation", MOUNT_POST, "仓储物价值减损的认定", "仓储物未毁损但价值减损", "《民法典》第917条、第584条", "因保管不善造成价值减损的，按减损价值赔偿", "仓储物因保管不善价值减损 [金额] 元，保管人应赔偿。"),
    ),
    terms={
        "jurisdiction_question": ("哪里起诉", "去哪里起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
        "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "告对人"),
        "warehouse_contract": ("仓储合同", "仓储物", "仓储费", "仓单", "入库单", "保管人", "存货人", "仓库储存", "商事仓储"),
        "contract_date": ("签订仓储合同", "合同签订", "入库", "仓储费到期", "储存期限届满", "提取仓储物"),
        "third_party_tort": ("第三人侵权", "外人造成损害", "他人侵权", "路人侵权"),
        "nature_dispute": ("合同性质争议", "仓储还是保管", "名为仓储", "实为保管", "不构成仓储合同"),
        "warehouse_business": ("以仓储为业", "仓储营业", "仓储营业资质", "仓储公司", "专业仓储", "仓储经营"),
        "general_safekeeping": ("一般保管", "亲友保管", "临时保管", "无仓储资质", "不是仓储营业人", "非仓储营业"),
        "consensual_contract": ("意思表示一致", "未交付也成立", "签订即成立", "诺成合同"),
        "contract_invalid": ("仓储合同无效", "违禁品储存", "非法仓储物", "违法储存"),
        "qualification_issue": ("无仓储资质", "未取得仓储资质", "不是仓储营业人"),
        "goods_delivered": ("交付仓储物", "货物入库", "已入库", "入库"),
        "receipt_issued": ("出具仓单", "出具入库单", "仓单", "入库单"),
        "receipt_transfer": ("仓单转让", "转让仓单", "背书转让", "受让仓单"),
        "receipt_pledge": ("仓单质押", "质押仓单", "权利质押"),
        "receipt_endorsed": ("背书", "已背书", "仓单上背书"),
        "keeper_signed_receipt": ("保管人签名", "保管人盖章", "经保管人签名", "经保管人盖章"),
        "multiple_claimants": ("多人主张提取", "多个仓单持有人", "多人争提货权", "多方主张提货"),
        "receipt_holder": ("合法持有仓单", "仓单持有人", "持有仓单"),
        "acceptance_dispute": ("验收", "入库验收", "未验收", "未按约验收"),
        "goods_nonconform": ("品种不符", "数量不符", "质量不符", "与约定不符", "不符合约定"),
        "timely_notice": ("及时通知", "已通知", "马上通知", "发现后通知"),
        "no_timely_notice": ("未及时通知", "没有通知", "未通知", "迟延通知"),
        "after_acceptance_nonconform": ("验收后发现不符", "验收后发生不符合约定", "验收后数量不符", "验收后质量不符"),
        "dangerous_goods": ("易燃", "易爆", "有毒", "腐蚀性", "放射性", "危险物品", "危险品", "易变质"),
        "hazard_explained": ("说明物品性质", "提供有关资料", "告知危险性质", "已说明危险"),
        "hazard_not_explained": ("未说明物品性质", "隐瞒危险性质", "未提供资料", "未告知危险"),
        "damage_or_loss": ("毁损灭失", "毁损", "灭失", "损坏", "丢失", "变质"),
        "in_storage_period": ("储存期内", "仓储期间", "保管期间", "入库后出库前"),
        "before_or_after_storage": ("入库前", "出库后", "提货后"),
        "improper_custody": ("保管不善", "未尽善良管理义务", "仓库漏水", "温控失效", "保管人过错", "管理不善"),
        "natural_property": ("自然性质", "自然损耗", "自身性质", "自然变质"),
        "bad_packaging": ("包装不符合约定", "包装不当", "包装破损", "包装不合格"),
        "expired_storage": ("超过有效储存期", "超过保质期", "超期储存", "有效储存期届满"),
        "force_majeure": ("不可抗力", "自然灾害", "洪水", "地震", "台风"),
        "actual_loss": ("损失", "价值", "货值", "损失价值", "实际损失"),
        "partial_damage": ("部分毁损", "部分灭失", "部分损坏", "一部分货物"),
        "undamaged_return": ("未毁损部分", "剩余部分", "完好部分"),
        "value_depreciation": ("价值减损", "贬值", "价值降低", "未毁损但贬值"),
        "inspection_request": ("检查仓储物", "提取样品", "要求检查", "要求取样"),
        "deterioration_found": ("发现变质", "发现损坏", "发现仓储物变质", "仓储物有变质"),
        "loss_expanded": ("损失扩大", "扩大损失", "导致损失扩大"),
        "danger_to_others": ("危及其他仓储物", "影响其他货物安全", "危及正常保管"),
        "emergency": ("情况紧急", "紧急", "来不及催告"),
        "disposed": ("处置", "紧急处置", "必要处置", "处理变质货物"),
        "period_due": ("储存期限届满", "到期", "期限已届满", "仓储期满"),
        "retrieved": ("已提取", "已经提货", "取走仓储物"),
        "overdue_retrieval": ("逾期提取", "逾期未提取", "到期未提货", "未按期提取"),
        "keeper_urged": ("催告提取", "已催告", "催告存货人"),
        "deposit_goods": ("提存", "提存仓储物"),
        "early_retrieval": ("提前提取", "提前提货", "期限届满前提取"),
        "unclear_storage_period": ("储存期限不明", "未约定储存期限", "期限约定不明", "没有约定储存期限"),
        "unpaid_storage_fee": ("欠付仓储费", "拖欠仓储费", "仓储费未付", "未支付仓储费"),
        "lien_claim": ("留置", "留置权", "留置仓储物"),
        "fee_amount": ("仓储费", "加收仓储费", "费用"),
        "termination_request": ("解除仓储合同", "解除合同", "要求解除", "主张解除"),
        "statutory_termination_reason": ("不可抗力", "拒绝履行", "经催告仍未履行", "合同目的不能实现", "根本违约"),
        "depositor_assignment": ("转让仓储物", "存货人变更", "存货人将仓储物转让", "受让人提货"),
        "valid_assignment": ("有效转让", "背书转让", "通知保管人", "转让手续齐备"),
    },
)


WAREHOUSE_CONFIGS: Dict[str, WarehouseConfig] = {WAREHOUSE_CONFIG.key: WAREHOUSE_CONFIG}


def get_warehouse_config(contract_type: str | None = None) -> WarehouseConfig:
    key = (contract_type or "warehouse").strip().lower()
    aliases = {
        "storage": "warehouse",
        "warehousing": "warehouse",
        "warehouse_contract": "warehouse",
        "仓储": "warehouse",
        "仓储合同": "warehouse",
    }
    return WAREHOUSE_CONFIGS.get(aliases.get(key, key), WAREHOUSE_CONFIG)
