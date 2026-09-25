"""Service-contract adjudication configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from adjudicate.lease_configs import MOUNT_POST, PatchMount


Terms = Tuple[str, ...]
PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class ServiceConfig:
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


SERVICE_CONFIG = ServiceConfig(
    key="service",
    display_name="服务合同",
    fact_mapping={
        "合同主体": "服务提供方/服务接受方",
        "核心义务": "按约定提供服务（服务方）/ 支付服务费（接受方）",
        "归责原则": "过错责任（服务方对服务质量瑕疵承担责任）",
        "核心争议": "服务是否提供 → 服务质量是否达标 → 合同能否解除 → 如何退款",
    },
    reused_modules=("管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"),
    patch_mounts=(
        PatchMount("SVC1", "contract_nature", MOUNT_POST, "服务合同性质认定", "合同名称或内容模糊，双方对服务、承揽、委托性质存在争议", "《民法典》第509条及合同编通则", "按实质认定：注重服务过程为服务合同，注重成果交付为承揽合同，注重事务处理为委托合同", "合同性质认定为 [服务合同/承揽合同/委托合同]，适用 [相应] 裁判规则。"),
        PatchMount("SVC2", "contract_subtype", MOUNT_POST, "预付式消费特殊规则", "服务接受方预先支付全部或部分费用，服务提供方多次或持续提供服务", "《消费者权益保护法》第53条、预付式消费司法解释", "经营者未按约定提供服务或终止营业的，应履行约定或退还预付款；恶意逃避退款的支持惩罚性赔偿", "本案为预付式消费，经营者 [已/未] 按约定提供服务，[应/不应] 退还预付款 [金额] 元，[适用/不适用] 惩罚性赔偿。"),
        PatchMount("SVC3", "termination_basis", MOUNT_POST, "身体健康原因解除", "服务接受方因身体健康原因无法继续接受服务", "预付式消费司法解释第13条、《民法典》第533条", "身体健康基础条件发生无法预见重大变化，继续履行明显不公的，消费者可解除且不承担违约金", "消费者因身体健康原因解除合同，[构成/不构成] 违约，[应/不应] 承担违约金，应退还款项 [金额] 元。"),
        PatchMount("SVC4", "contract_effect", MOUNT_POST, "不退不换格式条款效力", "服务合同中存在不退不换、概不退款等格式条款", "《民法典》第496条、第497条、第498条", "不合理免除经营者责任、加重消费者责任、限制消费者主要权利的格式条款无效", "‘不退不换’格式条款 [有效/无效]，消费者 [可以/不可以] 主张退款。"),
        PatchMount("SVC5", "service_quality_standard", MOUNT_POST, "服务质量标准认定", "双方对服务质量是否达标存在争议", "《民法典》第509条、第577条、第582条", "有约定按约定，无约定按行业标准或通常标准，结果难以量化时结合合同目的和交易习惯", "服务质量 [符合/不符合] 约定/行业标准，服务提供方 [构成/不构成] 违约。"),
        PatchMount("SVC6", "service_content_standard", MOUNT_POST, "服务方单方变更服务内容", "服务提供方单方面调整服务内容、方式、标准", "《民法典》第509条、第577条", "未经对方同意单方变更服务内容构成违约，接受方可请求继续履行或解除并赔偿", "服务提供方单方变更服务内容 [构成/不构成] 违约，服务接受方 [可以/不可以] 要求继续履行或解除合同。"),
        PatchMount("SVC7", "provider_obligation", MOUNT_POST, "服务方资质缺失或人员不符", "服务方不具备法定资质，或实际服务人员与约定不符", "《民法典》第509条、第577条", "服务方应具备法定资质，服务人员应符合约定；资质缺失或人员不符构成违约", "服务方 [具备/不具备] 法定资质，实际服务人员 [符合/不符合] 约定，[构成/不构成] 违约。"),
        PatchMount("SVC8", "termination_basis", MOUNT_POST, "不定期继续性服务合同任意解除", "服务合同未约定期限或为长期持续服务", "《民法典》第563条第2款", "持续履行的不定期合同可随时解除，但应在合理期限前通知", "不定期继续性服务合同，当事人 [可以/不可以] 随时解除，[已/未] 在合理期限前通知，解除 [有效/无效]。"),
        PatchMount("SVC9", "nonperformance_reason", MOUNT_POST, "服务接受方原因解除损失赔偿", "服务接受方因不再需要、搬家等自身原因单方解除合同", "《民法典》第509条、第577条、第584条", "经营者无违约过错的，消费者按公平诚信原则承担合理损失，余额退还", "服务接受方因自身原因解除合同，[应/不应] 承担违约责任，可扣除合理损失 [金额] 元后退还余额。"),
        PatchMount("SVC10", "punitive_damages", MOUNT_POST, "恶意逃避退款惩罚性赔偿", "经营者收取预付款后终止营业，恶意逃避消费者退款", "《消费者权益保护法》第55条、预付式消费司法解释第23条", "终止营业且恶意逃避退款构成欺诈的，退还预付款并承担三倍惩罚性赔偿", "经营者 [构成/不构成] 恶意逃避退款，[应/不应] 承担惩罚性赔偿，赔偿金额为 [三倍服务费用] 元。"),
        PatchMount("SVC11", "service_content_standard", MOUNT_POST, "互联网平台服务条款变更", "互联网服务平台单方变更服务条款", "《民法典》第496条、第509条", "涉及重大权益的单方变更应提示说明并取得用户同意，否则对用户不发生效力", "平台服务条款变更 [有效/无效]，对用户 [发生/不发生] 效力。"),
        PatchMount("SVC12", "provider_obligation", MOUNT_POST, "预付式消费合同转让责任", "服务提供方将经营业务转让给第三方", "预付式消费司法解释及合同编通则", "受让方应继续履行预付式消费合同；转让方未告知消费者或受让方不履行的，消费者可主张相应责任", "经营者转让后，受让方 [应/不应] 继续履行合同，转让方 [承担/不承担] 相应责任。"),
        PatchMount("SVC13", "service_quality", MOUNT_POST, "保过包过承诺", "服务合同包含保过、包过、不过全退等承诺", "《民法典》第509条、第577条、第582条", "保过承诺构成合同义务，目标未实现且不可归责于接受方的，服务方承担违约责任", "‘保过’承诺 [构成/不构成] 合同义务，目标 [已/未] 实现，服务方 [应/不应] 承担违约责任。"),
    ),
    terms={
        "jurisdiction_question": ("哪里起诉", "去哪里起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
        "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "告对人"),
        "service_contract": ("服务合同", "服务费", "服务提供方", "服务接受方", "培训", "健身", "美容", "旅游", "咨询", "摄影", "婚庆", "养老", "互联网服务"),
        "contract_date": ("签订合同", "服务开始", "办卡", "充值", "付款", "应提供服务", "停业", "解除合同"),
        "third_party_tort": ("第三人侵权", "路人侵权", "外人造成损害", "他人侵权"),
        "nature_dispute": ("合同性质争议", "到底是什么合同", "名为", "实为", "性质不一致", "定性争议"),
        "service_process": ("提供服务", "接受服务过程", "服务行为", "课程服务", "健身服务", "美容服务", "咨询服务"),
        "work_result": ("完成工作成果", "交付成果", "交付照片", "交付报告", "加工", "定作", "承揽"),
        "entrusted_affair": ("处理事务", "代办事务", "受托人", "委托事务", "按指示处理"),
        "contract_invalid": ("合同无效", "无效合同", "违法无效", "违反强制性规定"),
        "fraud_or_coercion": ("欺诈", "胁迫", "虚假宣传", "诱导消费"),
        "prepaid_consumption": ("预付式消费", "预付款", "预付费", "办卡", "充值", "会员卡", "储值卡", "课包", "私教课"),
        "consumer": ("消费者", "生活消费", "个人消费", "会员", "学员", "顾客"),
        "operator_closed": ("停业", "关店", "跑路", "闭店", "停止营业", "门店关闭", "机构停业"),
        "malicious_refund_evasion": ("恶意逃避退款", "失联", "联系不上", "更换联系方式", "拒不退款", "卷款跑路"),
        "prepaid_amount": ("预付款", "充值", "办卡", "课包", "服务费", "预付费用", "会员费"),
        "service_full_provided": ("全部提供", "服务完成", "课程上完", "已经提供完", "全部履行"),
        "service_not_provided": ("未提供服务", "完全未提供", "没有提供服务", "一节没上", "未履行"),
        "service_partly_provided": ("部分提供", "只提供部分", "剩余服务", "未完成服务", "只上了部分课程", "剩余课时"),
        "unused_amount": ("未消费金额", "剩余金额", "未提供服务金额", "未使用余额", "剩余课时金额"),
        "provider_unilateral_change": ("单方变更服务内容", "擅自变更课程", "更换服务内容", "降低服务标准", "调整服务方式", "单方调整"),
        "accepted_change": ("协商一致", "消费者同意", "用户同意", "双方同意", "已同意变更"),
        "health_change": ("身体健康原因", "医嘱不宜继续", "医生建议停止", "怀孕", "受伤", "疾病", "健康状况变化"),
        "medical_advice": ("医疗机构建议", "医院证明", "医生证明", "医嘱"),
        "unforeseeable": ("无法预见", "订约时无法预见", "不能预见"),
        "unfair_to_continue": ("继续履行明显不公平", "继续履行显失公平", "无法继续接受服务"),
        "format_no_refund": ("不退不换", "概不退款", "一经售出不退", "费用不退", "不予退费", "不退费"),
        "format_clause": ("格式条款", "预先拟定", "模板合同", "不能协商", "霸王条款"),
        "service_quality_dispute": ("服务质量不达标", "服务不达标", "服务质量差", "效果不满意", "质量争议", "未达到标准"),
        "quality_standard_agreed": ("合同约定标准", "明确约定标准", "服务标准", "质量标准"),
        "industry_standard": ("行业标准", "通常标准", "交易习惯"),
        "quality_conform": ("质量达标", "符合约定", "符合标准", "服务合格"),
        "quality_nonconform": ("质量不达标", "不符合约定", "不符合标准", "服务瑕疵"),
        "provider_no_qualification": ("无资质", "没有资质", "无证", "不具备法定资质", "没有执业资格", "无证执教", "无证医师"),
        "staff_mismatch": ("服务人员不符", "私教更换", "老师更换", "师资不符", "不是约定人员", "实际服务人员与约定不符"),
        "service_receiver_fault": ("消费者自身原因", "不再需要", "搬家", "个人原因", "自己不去了", "自身原因解除"),
        "reasonable_loss": ("合理损失", "准备成本", "已支出成本", "违约金"),
        "indefinite_service": ("未约定服务期限", "不定期服务", "长期持续服务", "持续服务", "月付服务"),
        "reasonable_notice": ("提前通知", "合理期限前通知", "提前一个月通知", "已通知"),
        "platform_terms_change": ("平台单方变更服务条款", "互联网平台变更规则", "修改用户协议", "平台服务变更", "账号权益变更"),
        "major_rights_change": ("重大权益", "限制账号功能", "减少权益", "影响主要权利"),
        "prompt_explain": ("提示说明", "明确提示", "通知用户", "公告通知"),
        "user_consent": ("用户同意", "点击同意", "明确同意"),
        "business_transfer": ("经营业务转让", "门店转让", "转让给第三方", "换老板", "受让方"),
        "transfer_notified": ("已通知消费者", "告知消费者", "通知会员"),
        "transferee_refuses_service": ("受让方拒绝服务", "新店不认卡", "不继续提供服务"),
        "guaranteed_result": ("保过", "包过", "不过全退", "保证通过", "保证录用", "保证效果"),
        "goal_not_achieved": ("没有通过", "未通过", "目标未实现", "未录用", "没有达到承诺效果"),
        "receiver_fault_goal": ("学员原因未通过", "消费者不配合", "缺课导致未通过", "接受方原因"),
        "force_majeure": ("不可抗力", "疫情封控", "自然灾害", "政府原因"),
        "termination_request": ("解除合同", "要求解除", "退卡", "退费", "退款", "终止合同"),
        "actual_loss": ("损失", "赔偿", "合理损失", "费用"),
    },
)


SERVICE_CONFIGS: Dict[str, ServiceConfig] = {SERVICE_CONFIG.key: SERVICE_CONFIG}


def get_service_config(contract_type: str | None = None) -> ServiceConfig:
    key = (contract_type or "service").strip().lower()
    aliases = {
        "services": "service",
        "consumer_service": "service",
        "training": "service",
        "fitness": "service",
        "服务": "service",
        "服务合同": "service",
        "培训": "service",
        "健身": "service",
        "美容": "service",
    }
    return SERVICE_CONFIGS.get(aliases.get(key, key), SERVICE_CONFIG)
