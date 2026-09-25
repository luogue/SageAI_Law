"""Utility-supply-contract adjudication configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from adjudicate.lease_configs import MOUNT_POST, PatchMount


Terms = Tuple[str, ...]
PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class UtilitySupplyConfig:
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


UTILITY_SUPPLY_CONFIG = UtilitySupplyConfig(
    key="utility_supply",
    display_name="供用电、水、气、热力合同",
    fact_mapping={
        "合同主体": "供应方（供电/水/气/热力企业）/ 用户",
        "核心义务": "安全、持续供应（供应方）/ 支付使用费并安全使用（用户）",
        "归责原则": "过错责任（各方对自身违约/过错行为承担责任）",
        "核心争议": "供应质量是否达标 → 使用费是否支付 → 中止供应程序是否合法 → 设施维护责任归属",
    },
    reused_modules=("管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"),
    patch_mounts=(
        PatchMount("U1", "contract_type", MOUNT_POST, "合同类型的识别与参照适用", "需要确定适用何种供用合同规则", "《民法典》第648条、第656条", "供用电直接适用供用电合同规则；供用水、气、热力参照适用", "本案为 [供用电/供用水/供用气/供用热力] 合同，[直接适用/参照适用] 供用电合同的有关规定。"),
        PatchMount("U2", "contract_effect", MOUNT_POST, "强制缔约义务", "用户主张供应方拒绝订立合同", "《民法典》第648条", "向社会公众供电的供电人不得拒绝用电人合理的订立合同要求", "供应方 [违反/未违反] 强制缔约义务。"),
        PatchMount("U3", "supply_quality", MOUNT_POST, "供应质量不达标的处理", "用户主张供应质量不符合国家标准或合同约定", "《民法典》第651条", "未按国家规定质量标准和约定安全供应造成损失的，供应方赔偿并可相应减费", "供应方 [已/未] 达到国家规定的供应质量标准。"),
        PatchMount("U4", "interruption_reason", MOUNT_POST, "中断供应的通知义务", "供应方中断供应，用户主张未收到事先通知", "《民法典》第652条", "计划检修、临时检修、依法限供或用户违法使用等中断供应，应事先通知", "供应方 [已/未] 履行中断供应的事先通知义务。"),
        PatchMount("U5", "interruption_reason", MOUNT_POST, "自然灾害断电后的抢修义务", "因自然灾害等原因断电，用户主张供应方未及时抢修", "《民法典》第653条", "自然灾害等原因断电后，供应方应及时抢修", "供应方 [已/未] 及时抢修。"),
        PatchMount("U6", "payment_dispute", MOUNT_POST, "欠费中止供应的法定程序", "供应方因用户欠费而中止供应", "《民法典》第654条", "逾期不付费经催告并给予合理期限后仍不支付的，方可按国家规定程序中止供应", "供应方中止供应程序 [合法/不合法]。"),
        PatchMount("U7", "user_obligation", MOUNT_POST, "用户违规使用的责任", "用户未按国家规定和约定使用，造成供应方损失", "《民法典》第655条", "用户违规使用造成供应方损失的，应承担赔偿责任", "用户 [存在/不存在] 违规使用行为。"),
        PatchMount("U8", "user_obligation", MOUNT_POST, "转供的处理", "用户未经供应方同意向第三方转供", "供用合同安全使用与合同相对性规则", "未经供应方同意向第三方转供的，供应方可要求停止并赔偿损失", "用户 [存在/不存在] 违规转供行为。"),
        PatchMount("U9", "metering_dispute", MOUNT_POST, "计量误差的处理", "计量装置存在误差，双方对使用量有争议", "计量结算规则", "按实际用量重新计算，差额多退少补", "计量装置存在误差，应按实际用量重新计算。"),
        PatchMount("U10", "facility_maintenance", MOUNT_POST, "设施维护责任的认定", "供用设施损坏，双方对维修责任有争议", "《民法典》第650条", "以产权分界处为界确定履行地点和维护责任", "设施维护责任由 [供应方/用户] 承担。"),
        PatchMount("U11", "contract_effect", MOUNT_POST, "未签订书面合同的供用关系认定", "双方未签订书面供用合同，但已形成事实供应关系", "供用合同成立规则", "实际供应、实际使用并支付费用的，供用合同关系成立", "供用合同关系 [成立/不成立]。"),
        PatchMount("U12", "suspension_procedure", MOUNT_POST, "物业公司无权对用户断水断电", "物业公司以用户未交物业费为由断水断电", "供用合同相对性规则", "供水、供电合同当事人为用户和供应企业，物业企业无权断水断电", "物业公司断水断电 [合法/不合法]。"),
        PatchMount("U13", "heating_temperature", MOUNT_POST, "供暖温度不达标的举证责任", "用户主张供暖温度不达标，拒绝缴纳供暖费", "供热质量举证规则", "用户应及时保留投诉、维修、测温或第三方检测记录", "供暖温度不达标主张 [成立/不成立]。"),
        PatchMount("U14", "payment_dispute", MOUNT_POST, "违约金过高的调整", "供应方主张的违约金过高，用户请求调整", "《民法典》第585条", "违约金过分高于损失的，可予以调减", "违约金 [过高/不过高]，[应/不应] 予以调减。"),
        PatchMount("U15", "interruption_notice", MOUNT_POST, "供应方的承诺效力", "供应方在停供公告中明确恢复供应时间", "《民法典》第577条", "停供公告明确恢复时间构成承诺，违反承诺造成损失的承担违约责任", "供应方 [已/未] 作出承诺，[已/未] 违反承诺。"),
    ),
    terms={
        "jurisdiction_question": ("哪里起诉", "去哪里起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
        "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "适格被告"),
        "utility_supply_contract": ("供用合同", "供用电", "供用水", "供用气", "供用热力", "供电合同", "供水合同", "供气合同", "供热合同", "水电气热"),
        "electricity_contract": ("供用电", "供电", "用电", "电费", "断电", "停电", "恢复供电"),
        "water_contract": ("供用水", "供水", "用水", "水费", "断水", "停水", "水压"),
        "gas_contract": ("供用气", "供气", "用气", "气费", "断气", "停气", "燃气", "气压"),
        "heat_contract": ("供用热力", "供热", "供暖", "暖气", "热力", "供暖费", "室温"),
        "contract_date": ("签订供用合同", "合同签订", "开始供电", "开始供水", "开始供气", "开始供热", "催告", "中止供应", "断水断电"),
        "third_party_tort": ("第三人侵权", "外人破坏", "他人侵权", "第三方施工挖断"),
        "no_written_contract": ("未签书面合同", "没有书面合同", "没签合同", "口头约定"),
        "actual_supply": ("实际供电", "实际供水", "实际供气", "实际供热", "已经供应", "持续供应"),
        "user_used": ("实际使用", "一直使用", "用户使用", "已经用电", "已经用水", "已经用气", "已经供暖"),
        "paid_fee": ("支付电费", "支付水费", "支付气费", "支付供暖费", "交费", "缴费", "付费"),
        "refuse_contract": ("拒绝订立合同", "拒绝签约", "拒绝开户", "不给开户", "拒绝接入", "不同意供电"),
        "public_supplier": ("向社会公众供电", "公用事业", "供电公司", "自来水公司", "燃气公司", "供热公司"),
        "reasonable_request": ("合理订立合同要求", "符合接入条件", "符合开户条件", "合理要求", "资料齐全"),
        "format_clause": ("格式条款", "模板合同", "预先拟定", "不能协商", "霸王条款"),
        "unreasonable_clause": ("免除供应方责任", "加重用户责任", "排除用户主要权利", "不合理免责"),
        "supply_quality_dispute": ("供应质量不达标", "质量不达标", "不符合国家标准", "不符合约定", "电压不稳", "水压不足", "气压不足", "温度不达标"),
        "supply_quality_conform": ("质量达标", "符合国家标准", "符合约定", "供应正常"),
        "supply_quality_nonconform": ("质量不达标", "不符合国家标准", "电压不稳", "水压不足", "气压不足", "温度不达标"),
        "supply_interruption": ("中断供应", "中断供电", "中断供水", "中断供气", "中断供热", "停供", "断电", "停电", "断水", "停水", "断气", "停气", "停暖"),
        "supplier_fault": ("供应方原因", "设备故障", "管理不善", "供应企业过错", "供电公司过错", "自来水公司过错", "燃气公司过错", "供热公司过错"),
        "maintenance_interruption": ("计划检修", "临时检修", "检修", "维修"),
        "legal_power_limit": ("依法限电", "依法限水", "依法限气", "限电", "限供"),
        "prior_notice": ("事先通知", "提前通知", "已通知", "公告通知", "短信通知"),
        "natural_disaster": ("自然灾害", "台风", "洪水", "地震", "暴雨", "暴雪"),
        "timely_repair": ("及时抢修", "马上抢修", "及时维修", "已抢修"),
        "user_cause": ("用户原因", "用户违法用电", "用户违法用水", "用户违法用气", "违规使用", "窃电", "窃水", "窃气"),
        "unpaid_fee": ("拖欠电费", "拖欠水费", "拖欠气费", "拖欠供暖费", "欠费", "逾期不支付", "未支付使用费"),
        "liquidated_damage_claim": ("违约金", "滞纳金", "逾期违约金"),
        "urged": ("催告", "经催告", "书面催告", "发送催缴通知"),
        "reasonable_period_given": ("合理期限", "宽限期", "限期缴纳", "限期支付"),
        "supply_suspended": ("中止供电", "中止供水", "中止供气", "中止供热", "中止供应", "停止供应", "停供", "断电", "停电", "断水", "停水", "断气", "停气", "停暖", "断水断电"),
        "statutory_procedure": ("国家规定程序", "按程序", "程序合法", "依法中止"),
        "property_company_cutoff": ("物业断水", "物业断电", "物业停水", "物业停电", "物业公司断水断电", "物业公司", "物业停门禁"),
        "property_fee_unpaid": ("未交物业费", "拖欠物业费", "物业费欠费"),
        "illegal_use": ("违规使用", "违法用电", "违法用水", "违法用气", "窃电", "窃水", "窃气", "擅自改变用电类别"),
        "supplier_loss": ("供应方损失", "造成供电人损失", "造成供应方损失", "损坏供用设施"),
        "sub_supply": ("转供", "向第三方转供", "转供给第三人", "私自接给他人", "给邻居用"),
        "supplier_consent": ("经供应方同意", "供电公司同意", "自来水公司同意", "燃气公司同意", "供热公司同意"),
        "metering_dispute": ("计量争议", "计量装置", "电表", "水表", "燃气表", "热量表", "读数争议", "用量争议"),
        "meter_error": ("计量误差", "读数错误", "表计不准", "电表故障", "水表故障", "燃气表故障", "热量表故障"),
        "meter_fault": ("计量装置故障", "表具老化", "表计故障"),
        "user_modified_meter": ("私自改动计量装置", "私改电表", "私改水表", "私改燃气表", "偷改表"),
        "supplier_install_fault": ("安装不当", "维护不当", "供应方安装错误", "供应方维护不当"),
        "overcharged": ("多计", "多收", "多收费用", "多算"),
        "undercharged": ("少计", "少收", "漏计", "补收"),
        "maintenance_dispute": ("设施维护责任", "维修责任", "设施损坏", "管线损坏", "供用设施损坏"),
        "boundary_supplier_side": ("产权分界处供应方侧", "表前", "用户表前", "供应方侧"),
        "boundary_user_side": ("产权分界处用户侧", "表后", "用户表后", "用户侧"),
        "boundary_unclear": ("产权分界处不明确", "分界处不明", "没有约定分界"),
        "fault_damage": ("过错造成", "人为损坏", "一方过错"),
        "heating_temp_dispute": ("供暖温度不达标", "室温不达标", "暖气不热", "供热温度不足", "拒交供暖费"),
        "heating_temp_not_standard": ("温度不达标", "室温低于标准", "暖气不热", "供热不达标"),
        "heating_evidence": ("测温单", "第三方检测", "投诉记录", "维修记录", "上门测温", "检测报告"),
        "no_heating_evidence": ("没有测温证据", "无测温记录", "没有投诉记录", "没有检测报告"),
        "commitment_restore_time": ("承诺恢复供电时间", "公告恢复时间", "明确恢复供电时间", "承诺恢复供应时间"),
        "commitment_breached": ("未按承诺恢复", "超过承诺时间", "违反承诺", "逾期恢复"),
        "actual_loss": ("损失", "赔偿", "损失金额", "维修费", "差额", "使用费"),
        "fee_amount": ("电费", "水费", "气费", "供暖费", "使用费", "欠费", "费用"),
        "liquidated_damage_amount": ("违约金", "滞纳金", "逾期违约金"),
    },
)


UTILITY_SUPPLY_CONFIGS: Dict[str, UtilitySupplyConfig] = {
    UTILITY_SUPPLY_CONFIG.key: UTILITY_SUPPLY_CONFIG,
}


def get_utility_supply_config(contract_type: str | None = None) -> UtilitySupplyConfig:
    key = (contract_type or "utility_supply").strip().lower()
    aliases = {
        "utility": "utility_supply",
        "utilities": "utility_supply",
        "power_supply": "utility_supply",
        "water_supply": "utility_supply",
        "gas_supply": "utility_supply",
        "heat_supply": "utility_supply",
        "供用": "utility_supply",
        "供用电": "utility_supply",
        "供用水": "utility_supply",
        "供用气": "utility_supply",
        "供用热力": "utility_supply",
        "供水供电": "utility_supply",
    }
    return UTILITY_SUPPLY_CONFIGS.get(aliases.get(key, key), UTILITY_SUPPLY_CONFIG)
