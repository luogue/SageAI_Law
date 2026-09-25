"""Transportation-contract adjudication configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from adjudicate.lease_configs import MOUNT_POST, PatchMount


Terms = Tuple[str, ...]
PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class TransportationConfig:
    key: str
    display_name: str
    fact_mapping: Dict[str, str]
    reused_modules: Terms
    patch_mounts: PatchMounts = field(default_factory=tuple)
    terms: Dict[str, Terms] = field(default_factory=dict)

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


TRANSPORTATION_CONFIG = TransportationConfig(
    key="transportation",
    display_name="运输合同",
    fact_mapping={
        "合同主体": "承运人/托运人/收货人",
        "核心义务": "安全、按时运输货物",
        "归责原则": "严格责任（举证责任倒置）",
        "核心争议": "货物是否毁损/灭失/延迟 → 承运人能否证明免责事由 → 赔偿多少",
    },
    reused_modules=("管辖", "适格被告", "合同效力", "违约金调减"),
    patch_mounts=(
        PatchMount(
            "T4",
            "shipper_change_or_cancel",
            MOUNT_POST,
            "托运人变更/解除的赔偿",
            "托运人在货物交付前要求中止运输、返还货物、变更到达地或变更收货人",
            "《民法典》第829条",
            "交付收货人前可以变更或解除，但应赔偿承运人因此受到的损失",
            "托运人变更/解除有效，应赔偿承运人损失 [具体金额]。",
        ),
        PatchMount(
            "T5",
            "carrier_lien",
            MOUNT_POST,
            "承运人留置权",
            "托运人或收货人未支付运费、保管费及其他运输费用",
            "承运人对相应运输货物依法享有留置权",
            "费用到期未支付时可留置相应货物，留置明显超额或行使不当造成损失的应赔偿",
            "承运人留置权成立/不成立。",
        ),
        PatchMount(
            "T6",
            "carrier_lien",
            MOUNT_POST,
            "留置权的同一法律关系限制",
            "承运人因托运人拖欠此前运费，扣押当前批次货物",
            "《民法典》第448条",
            "留置权行使须以债权与动产属于同一法律关系为前提；多笔独立业务不得相互留置",
            "欠付运费与当前货物属于/不属于同一法律关系，留置权成立/不成立。",
        ),
        PatchMount(
            "T7",
            "carrier_lien",
            MOUNT_POST,
            "合同排除留置权的效力",
            "运输合同明确约定承运人不得留置货物，承运人仍以欠付运费为由扣货",
            "《民法典》第836条但书",
            "合同明确排除留置权的，约定优先；承运人扣货构成违约，造成损失的应赔偿",
            "合同明确排除留置权，承运人扣货构成违约。",
        ),
        PatchMount(
            "T3",
            "continuous_transport",
            MOUNT_POST,
            "连续运输/多式联运责任划分",
            "运输涉及多个承运人、转包、分段运输或多式联运",
            "与托运人订立合同的承运人对全程运输承担责任",
            "签约承运人先对托运人或收货人承担全程责任，赔偿后可向责任区段承运人追偿",
            "签约承运人承担全程责任，可向区段承运人追偿。",
        ),
        PatchMount(
            "T1",
            "carrier_exemption",
            MOUNT_POST,
            "承运人严格责任 + 举证责任倒置",
            "货物在运输过程中毁损、灭失",
            "《民法典》第832条",
            "承运人承担严格责任；承运人须证明法定免责事由及其与货损之间的因果关系",
            "承运人未能证明免责事由（或因果关系不成立），应承担赔偿责任。",
        ),
        PatchMount(
            "T2",
            "compensation_amount",
            MOUNT_POST,
            "保价条款效力审查",
            "合同中有保价条款、声明价值条款或限额赔偿条款",
            "《民法典》第833条及格式条款提示说明规则",
            "承运人已提示说明的按保价或限额约定；未提示说明或故意、重大过失时不适用限额",
            "保价条款有效/无效，赔偿金额为 [具体金额]。",
        ),
        PatchMount(
            "T8",
            "carrier_exemption",
            MOUNT_POST,
            "多式联运区段不明时的责任",
            "多式联运货物毁损、灭失，但无法查明发生在哪一运输区段",
            "《海商法》及《民法典》第832条、第833条",
            "区段不明或发生在海运区段的，适用海商法赔偿责任限额；能查明为陆运区段的，按实际损失赔偿",
            "货损区段无法查明，适用海商法赔偿责任限额。",
        ),
    ),
    terms={
        "jurisdiction_question": ("哪里起诉", "去哪起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
        "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "告对人"),
        "transport_contract": ("运输合同", "货运合同", "物流合同", "托运", "承运", "运费", "货物运输"),
        "contract_invalid": ("合同无效", "无效合同", "违法无效", "合同未成立"),
        "cargo_delivered_to_carrier": ("交给承运人", "交付承运人", "承运人收货", "物流已收货", "已揽收", "已装车", "承运人接收货物"),
        "cargo_damage": ("毁损", "损坏", "破损", "货损", "压坏", "摔坏", "受潮", "变质"),
        "cargo_loss": ("灭失", "丢失", "遗失", "少货", "货物不见", "整票丢失", "未送达"),
        "cargo_delay": ("延迟交付", "逾期送达", "未按时送达", "迟延送达", "晚到", "超过约定期限", "超过合理期限"),
        "in_transit": ("运输过程中", "运输途中", "承运期间", "从起运地到目的地途中", "运输期间", "在途"),
        "before_loading": ("装货前", "交货前", "承运人接收前", "揽收前", "运输前"),
        "after_unloading": ("卸货后", "交付后", "签收后", "收货后", "目的地交付后"),
        "force_majeure": ("不可抗力", "洪水", "地震", "台风", "泥石流", "战争", "政府封控"),
        "natural_property": ("自然性质", "自然属性", "自身性质", "易腐", "自燃", "自然变质", "挥发"),
        "reasonable_wear": ("合理损耗", "自然损耗", "正常损耗", "合理短少"),
        "shipper_fault": ("托运人过错", "包装不当", "包装破损", "瞒报", "错报", "瞒报危险品", "未告知危险品", "托运人原因"),
        "consignee_fault": ("收货人过错", "收货人原因", "拒收导致", "收货人迟延提货"),
        "carrier_proves": ("承运人证明", "能够证明", "有证据证明", "已证明", "提交证据证明"),
        "causation": ("导致货损", "造成货损", "与货损有因果关系", "因此损坏", "因此灭失"),
        "valuation_clause": ("保价", "保价条款", "声明价值", "限额赔偿", "未保价", "赔偿限额"),
        "carrier_explained_clause": ("已提示说明", "已明确提示", "已加粗提示", "已向托运人说明", "托运人确认保价"),
        "carrier_no_explanation": ("未提示说明", "没有提示说明", "未尽提示义务", "未说明保价", "格式条款未提示"),
        "carrier_intent_gross_negligence": ("故意", "重大过失", "明知会损坏", "严重违规", "野蛮装卸"),
        "agreed_compensation": ("保价金额", "声明价值", "约定赔偿", "赔偿限额", "限额"),
        "market_price": ("市场价格", "到达地市场价格", "货值", "实际价值", "实际损失"),
        "delay_loss": ("延迟损失", "迟延损失", "停工损失", "违约损失", "逾期损失"),
        "shipper_info_accurate": ("准确告知", "如实告知", "准确表明", "如实申报", "信息准确"),
        "shipper_info_inaccurate": ("未准确告知", "未如实告知", "瞒报", "错报", "谎报", "少报重量", "隐瞒性质", "瞒报危险品"),
        "change_request": ("中止运输", "返还货物", "变更到达地", "改送", "改派", "变更收货人", "解除运输合同"),
        "before_delivery": ("交付收货人之前", "尚未交付", "未交付收货人", "签收前", "到达前"),
        "after_delivery": ("已交付收货人", "已经签收", "签收后", "收货后"),
        "carrier_loss": ("空驶费", "仓储费", "保管费", "改派费", "变更费用", "承运人损失"),
        "unpaid_freight": ("未支付运费", "欠运费", "拖欠运费", "未付保管费", "欠保管费", "运输费用未付"),
        "lien": ("留置", "扣货", "扣留货物", "留置权"),
        "improper_lien": ("留置价值远超", "超额留置", "留置全部货物", "不当留置", "违法扣货"),
        "prior_freight_debt": ("此前运费", "之前运费", "上一票运费", "历史欠费", "旧运费", "前一批运费", "其他业务欠款"),
        "current_cargo_lien": ("扣押当前货物", "扣押当前批次货物", "扣当前这批货", "扣留本批货物", "留置当前货物", "扣押本票货物"),
        "same_legal_relationship": ("同一合同项下", "同一运输合同", "同一法律关系", "同一笔业务", "连续履行同一合同"),
        "different_legal_relationship": ("不同合同", "独立业务", "多笔独立业务", "不是同一法律关系", "另一笔业务", "其他业务"),
        "lien_excluded_by_contract": ("不得留置货物", "禁止留置", "承运人不得留置", "不得扣货", "禁止扣押货物", "合同排除留置权"),
        "mitigation_failure": ("未及时减损", "未采取减损措施", "未防止损失扩大", "放任损失扩大"),
        "freight_amount": ("运费", "保管费", "运输费用", "欠费"),
        "continuous_transport": ("多式联运", "连续运输", "分段运输", "多个承运人", "转包", "区段承运人", "实际承运人"),
        "unknown_transport_segment": ("无法查明区段", "区段无法查明", "不能确定区段", "无法确定发生在哪个区段", "查不清发生在哪段", "运输区段不能确定"),
        "sea_segment": ("海运区段", "海上运输", "海运途中", "船运区段"),
        "land_segment": ("陆运区段", "公路运输", "铁路运输", "陆路运输", "卡车运输"),
        "third_party_tort": ("路人侵权", "第三方侵权", "外人抢货", "陌生人破坏"),
        "delivery_date": ("交付", "应交付", "到达", "签收", "送达"),
    },
)


TRANSPORT_CONFIGS: Dict[str, TransportationConfig] = {
    TRANSPORTATION_CONFIG.key: TRANSPORTATION_CONFIG,
}


def get_transport_config(contract_type: str | None = None) -> TransportationConfig:
    key = (contract_type or "transportation").strip().lower()
    aliases = {
        "transport": "transportation",
        "freight": "transportation",
        "运输": "transportation",
        "货运": "transportation",
        "物流": "transportation",
    }
    return TRANSPORT_CONFIGS.get(aliases.get(key, key), TRANSPORTATION_CONFIG)
