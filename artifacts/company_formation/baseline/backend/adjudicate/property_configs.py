"""Property-management adjudication configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from adjudicate.lease_configs import MOUNT_POST, MOUNT_REPLACE, PatchMount


Terms = Tuple[str, ...]
PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class PropertyManagementConfig:
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


PROPERTY_MANAGEMENT_CONFIG = PropertyManagementConfig(
    key="property_management",
    display_name="物业服务合同",
    fact_mapping={
        "合同签订主体": "建设单位/业主委员会",
        "履约主体": "全体业主",
        "核心争议": "物业费是否应缴及金额",
        "瑕疵标准": "轻微/一般/严重",
    },
    reused_modules=("管辖", "适格被告", "合同效力", "违约金调减"),
    patch_mounts=(
        PatchMount(
            "M1",
            "limitation_period",
            MOUNT_REPLACE,
            "诉讼时效逐期计算",
            "物业费欠费纠纷",
            "物业费属于定期缴纳的独立债务，每期分别适用三年诉讼时效",
            "逐期检查欠费期间是否超过三年，超期不支持，未超期支持",
            "物业费诉讼时效逐期计算：XX年X月—XX年X月已超时效，不支持；XX年X月—XX年X月未超时效，支持。",
        ),
        PatchMount(
            "M2",
            "collection_method",
            MOUNT_POST,
            "催收方式合法性审查",
            "业主主张物业以停水、停电、停门禁、停电梯等方式催缴物业费",
            "物业不得采取停止供水、供电、供热、供燃气等方式催交物业费",
            "违法催收不消灭物业费债务，但业主可另行主张损害赔偿",
            "催收方式违法，物业不得以该方式催费，但物业费本体仍需缴纳。",
        ),
        PatchMount(
            "M3",
            "dismissal_procedure",
            MOUNT_POST,
            "解聘程序合法性审查",
            "业主主张已解聘物业，或物业主张解聘无效",
            "《民法典》第278条、第946条",
            "审查是否经业主大会依法定程序共同决定，并提前六十日书面通知",
            "解聘程序合法/不合法，解聘有效/无效。",
        ),
        PatchMount(
            "M4",
            "public_income",
            MOUNT_POST,
            "公共收益归属",
            "涉及电梯广告、地面停车费、公共场地出租等公共区域经营收益",
            "公共区域经营收益归全体业主共有，物业无权占有",
            "物业应返还业主或抵扣物业费，可扣除其举证证明的合理管理成本",
            "公共收益归全体业主共有，物业应返还 [金额] 元或抵扣物业费。",
        ),
        PatchMount(
            "M5",
            "contract_effect",
            MOUNT_POST,
            "事实物业服务关系",
            "未签书面物业服务合同，但物业公司已实际提供主要物业服务，业主长期接受且未提出异议",
            "《民法典》第939条、第944条及事实合同关系规则",
            "实际提供主要服务且业主长期接受未异议的，形成事实物业服务合同关系，业主仍应缴纳物业费",
            "双方形成事实上的物业服务合同关系，业主仍应支付物业费。",
        ),
        PatchMount(
            "M6",
            "dismissal_procedure",
            MOUNT_POST,
            "合同终止后交接僵局",
            "物业服务合同已依法终止，原物业公司拒绝退出或拒绝移交资料",
            "《民法典》第949条",
            "原物业公司拒不退场的，合同终止后的物业费不予支持；拒不移交资料造成损失的，应赔偿",
            "原物业公司拒不退场，合同终止后的物业费不予支持。",
        ),
        PatchMount(
            "M7",
            "dismissal_procedure",
            MOUNT_POST,
            "物业公司对业主大会解聘决定无诉权",
            "业主大会依法作出解聘物业公司的决定，物业公司起诉要求撤销该决定",
            "《民法典》第278条、第946条",
            "物业服务人并非小区业主，无权请求法院就业主大会解聘决定效力作出裁判",
            "物业公司无权起诉要求撤销业主大会解聘决定，法院驳回起诉。",
        ),
    ),
    terms={
        "jurisdiction_question": ("哪里起诉", "去哪起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
        "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "告对人"),
        "property_fee_dispute": ("物业费", "物业欠费", "欠物业费", "欠费", "催缴", "追缴", "拖欠物业费", "物业起诉"),
        "owner": ("业主", "房屋所有权人", "业主本人"),
        "developer_contract": ("前期物业服务合同", "建设单位签", "开发商签", "建设单位选聘", "前期物业合同"),
        "owners_committee_contract": ("业委会签", "业主委员会签", "业主委员会选聘", "业委会选聘"),
        "owner_not_signed_defense": ("不是我签", "我没签", "没有签合同", "不是业主本人签", "业主没签", "合同不是我签"),
        "illegal_collection": ("停水", "停电", "停水停电", "停用门禁", "禁用门禁", "门禁卡停用", "停用电梯", "停电梯", "停梯", "不让刷门禁"),
        "dismissal_dispute": ("解聘物业", "解聘物业公司", "解除物业合同", "更换物业", "物业撤离", "新物业", "选聘新物业"),
        "owners_meeting_valid": ("业主大会表决通过", "业主大会依法表决", "合法表决", "依法定程序", "双过半通过", "共同决定"),
        "owners_meeting_invalid": ("未经业主大会", "没有业主大会表决", "程序违法", "未表决", "业委会擅自", "部分业主决定"),
        "notice_60_days": ("提前60日", "提前六十日", "六十日前", "60日前书面通知", "提前两个月"),
        "service_provided": ("已按约定提供服务", "按约提供服务", "正常提供服务", "服务达标", "物业服务正常"),
        "service_defect": ("服务不达标", "服务不到位", "物业服务差", "服务有瑕疵", "管理混乱", "未按约服务"),
        "minor_defect": ("轻微瑕疵", "个别角落", "局部清洁不到位", "维修响应稍慢", "偶尔不到位"),
        "general_defect": ("一般瑕疵", "多处服务不达标", "多项服务不到位", "经常保洁不到位", "多处公共区域脏乱"),
        "serious_defect": ("严重瑕疵", "严重缺失", "长期无人保洁", "垃圾长期无人清理", "电梯长期停运", "安保长期缺失", "严重影响正常生活"),
        "property_responsibility": ("保洁", "保安", "安保", "绿化", "公共设施维修", "电梯维护", "秩序维护", "公共区域维修", "物业职责"),
        "building_structure_issue": ("外墙漏水", "主体结构", "房屋质量", "结构问题", "屋面漏水"),
        "third_party_tort": ("邻居侵权", "第三方侵权", "他人损害", "邻居造成", "外人造成"),
        "owner_no_living_defense": ("没住", "未入住", "房屋空置", "空置", "没有居住"),
        "owner_no_accept_defense": ("未接受服务", "没有接受服务", "无需接受服务", "不需要物业服务"),
        "public_income": ("公共收益", "电梯广告", "广告收益", "地面停车费", "公共停车费", "公共场地出租", "公共区域经营", "快递柜收益"),
        "management_cost": ("管理成本", "合理成本", "管理费用"),
        "no_written_contract": ("未签订书面物业服务合同", "没有书面物业合同", "未签物业合同", "没有签物业合同", "无书面合同", "没签物业服务合同"),
        "actual_property_service": ("实际提供保洁", "实际提供安保", "实际提供设施维护", "实际提供物业服务", "提供保洁安保", "保洁安保设施维护", "物业实际服务"),
        "long_accept_no_objection": ("长期接受服务未提出异议", "长期接受未异议", "一直接受服务", "未提出异议", "长期未提异议", "长期接受物业服务"),
        "contract_terminated": ("物业合同已终止", "物业服务合同已终止", "合同到期", "服务合同到期", "依法终止", "解聘已经生效", "合同终止后"),
        "original_property_refuses_exit": ("拒不退场", "拒绝退场", "拒绝退出", "不退出物业服务区域", "赖在小区", "拒不撤离"),
        "original_property_refuses_handover": ("拒绝移交资料", "拒不移交资料", "拒绝交接", "不移交档案", "不移交设施资料", "拒绝移交相关资料"),
        "original_property_exited": ("已经退场", "已退场", "已经退出", "已退出物业服务区域", "完成交接"),
        "post_termination_fee": ("终止后的物业费", "合同终止后的物业费", "退场后的物业费", "解聘后的物业费", "到期后的物业费"),
        "property_company_challenges_dismissal": ("物业公司起诉撤销解聘决定", "物业起诉要求撤销业主大会决定", "物业公司要求撤销解聘", "物业公司挑战解聘决定", "物业请求确认解聘决定无效"),
    },
)


PROPERTY_CONFIGS: Dict[str, PropertyManagementConfig] = {
    PROPERTY_MANAGEMENT_CONFIG.key: PROPERTY_MANAGEMENT_CONFIG,
}


def get_property_config(contract_type: str | None = None) -> PropertyManagementConfig:
    key = (contract_type or "property_management").strip().lower()
    aliases = {
        "property": "property_management",
        "物业": "property_management",
        "物业服务": "property_management",
        "property_service": "property_management",
    }
    return PROPERTY_CONFIGS.get(aliases.get(key, key), PROPERTY_MANAGEMENT_CONFIG)
