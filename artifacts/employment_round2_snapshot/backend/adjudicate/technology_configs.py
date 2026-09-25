"""Technology-contract adjudication configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from adjudicate.lease_configs import MOUNT_POST, PatchMount


Terms = Tuple[str, ...]
PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class TechnologyConfig:
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


TECHNOLOGY_CONFIG = TechnologyConfig(
    key="technology",
    display_name="技术合同",
    fact_mapping={
        "合同主体": "委托人/研究开发人/让与人/许可人/受让人/被许可人/咨询人/服务人",
        "核心义务": "研发/转让/许可/咨询/服务技术成果",
        "归责原则": "过错责任（各方对自身违约行为承担责任）",
        "核心争议": "合同类型认定 → 合同是否有效 → 技术成果权属 → 违约救济 → 风险承担",
    },
    reused_modules=("管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"),
    patch_mounts=(
        PatchMount("T1", "contract_type", MOUNT_POST, "技术合同类型认定", "合同名称或内容模糊，双方对合同性质存在争议", "《民法典》第843条", "按技术开发、转让、许可、咨询、服务的实质内容认定合同类型", "合同性质认定为 [技术开发合同/技术转让合同/技术许可合同/技术咨询合同/技术服务合同]。"),
        PatchMount("T2", "achievement_ownership", MOUNT_POST, "职务技术成果 vs 非职务技术成果的认定", "当事人对技术成果权属存在争议", "《民法典》第847条、第848条", "执行单位工作任务或主要利用单位物质技术条件的为职务技术成果；否则为非职务技术成果", "该技术成果 [属于/不属于] 职务技术成果，权属归 [单位/个人]。"),
        PatchMount("T3", "contract_effect", MOUNT_POST, "非法垄断技术的认定", "一方主张合同因非法垄断技术无效", "《民法典》第850条", "限制新研发、限制从其他渠道吸收技术、阻碍合理实施专利或使用技术秘密的，合同无效", "合同 [构成/不构成] 非法垄断技术，[无效/有效]。"),
        PatchMount("T4", "development_risk", MOUNT_POST, "技术开发合同的风险分担", "技术开发未能成功，当事人对损失分担有争议", "技术开发合同风险分担规则", "有约定按约定；无约定根据投入、过错等合理分担", "技术开发失败，风险 [按约定/合理分担]。"),
        PatchMount("T5", "development_result", MOUNT_POST, "委托开发成果的专利申请权归属", "委托开发完成的发明创造，双方对专利申请权有争议", "《民法典》第859条", "无约定时申请专利权归研究开发人，委托人可依法实施该专利", "委托开发成果的专利申请权归 [研究开发人/按约定]。"),
        PatchMount("T6", "development_result", MOUNT_POST, "技术秘密成果的使用权/转让权归属", "委托开发或合作开发完成技术秘密成果，权属约定不明", "《民法典》第861条", "没有约定或约定不明的，双方均有使用和转让权", "技术秘密成果的使用权/转让权 [按约定/归双方共有]。"),
        PatchMount("T7", "license_infringement", MOUNT_POST, "技术许可合同侵权责任的承担", "被许可人按约实施专利或使用技术秘密侵害他人合法权益", "《民法典》第874条", "按约实施侵害他人权益的，由让与人或许可人承担责任；超范围使用的被许可人自担", "被许可人按约定实施/使用，侵权责任由 [让与人/许可人] 承担。"),
        PatchMount("T8", "consulting_risk", MOUNT_POST, "技术咨询合同决策风险承担", "委托人按咨询报告决策造成损失", "《民法典》第881条", "报告符合要求的，决策损失由委托人承担；报告不合格的，受托人承担违约责任", "委托人按符合要求的咨询报告作出决策造成损失，由委托人承担。"),
        PatchMount("T9", "consulting_service_result", MOUNT_POST, "技术咨询/服务合同的新技术成果归属", "咨询或服务过程中产生新技术成果", "《民法典》第885条", "受托人利用委托人资料和条件完成的归受托人；委托人利用受托人成果完成的归委托人", "新技术成果归 [受托人/委托人] 所有。"),
        PatchMount("T10", "contract_termination", MOUNT_POST, "技术合同解除的催告期限", "一方迟延履行主要债务，另一方主张解除", "技术合同司法解释第11条", "经催告后30日内仍未履行的，可以解除", "一方迟延履行主要债务，经催告后超过30日仍未履行，另一方 [可以/不可以] 解除合同。"),
        PatchMount("T11", "contract_effect", MOUNT_POST, "侵害技术秘密合同被确认无效后的善意使用", "侵害他人技术秘密的技术合同被确认无效", "技术合同司法解释第12条", "善意取得方可在原范围内继续使用，但应支付合理使用费并承担保密义务", "善意取得方 [可以/不可以] 继续使用技术秘密，应支付合理使用费 [金额] 元。"),
        PatchMount("T12", "followup_improvement", MOUNT_POST, "后续改进成果的归属", "一方后续改进技术成果，另一方主张分享", "《民法典》第875条", "没有约定或约定不明的，其他各方无权分享", "后续改进成果归 [改进方/按约定]，他方 [无权/有权] 分享。"),
        PatchMount("T13", "contract_effect", MOUNT_POST, "欺诈订立技术合同的撤销", "一方以欺诈手段订立技术合同", "技术合同司法解释第12条", "用现有技术冒充委托开发标的或重复收费使对方违背真实意思订约的，可撤销", "存在欺诈订立情形，受损害方 [可以/不可以] 请求撤销合同。"),
        PatchMount("T14", "proper_defendant", MOUNT_POST, "不具有民事主体资格的科研组织订立合同的责任承担", "无民事主体资格科研组织订立技术合同", "技术合同司法解释第7条", "经授权认可的由授权组织承担；未经授权认可的由成员共同承担，受益组织在受益范围内承担责任", "科研组织订立合同，责任由 [授权组织/成员共同] 承担。"),
        PatchMount("T15", "contract_effect", MOUNT_POST, "技术进出口合同的特殊规定", "技术合同涉及技术进出口", "《民法典》第877条", "技术进出口合同优先适用相关法律、行政法规", "本案涉及技术进出口，优先适用技术进出口相关法律法规。"),
    ),
    terms={
        "jurisdiction_question": ("哪里起诉", "去哪里起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
        "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "适格被告"),
        "technology_contract": ("技术合同", "技术开发", "技术转让", "技术许可", "技术咨询", "技术服务", "技术成果", "技术秘密", "专利"),
        "contract_date": ("签订技术合同", "合同签订", "交付技术成果", "支付使用费", "催告", "解除合同"),
        "third_party_tort": ("第三人侵权", "外人侵权", "他人侵权"),
        "nature_dispute": ("合同性质争议", "技术合同类型", "名为技术", "实为承揽", "实为建设工程", "合同类型不明"),
        "development_contract": ("技术开发合同", "委托开发", "合作开发", "研究开发", "研发新技术", "新产品", "新工艺", "新材料"),
        "commissioned_development": ("委托开发", "委托人", "研究开发人"),
        "cooperative_development": ("合作开发", "共同开发", "合作研发"),
        "transfer_contract": ("技术转让", "专利权转让", "专利申请权转让", "技术秘密转让", "权利让与"),
        "license_contract": ("技术许可", "专利实施许可", "技术秘密使用许可", "许可实施", "许可使用", "被许可人"),
        "consulting_contract": ("技术咨询", "可行性论证", "技术预测", "专题技术调查", "分析评价报告", "咨询报告"),
        "service_contract": ("技术服务", "解决特定技术问题", "技术服务合同"),
        "work_or_construction": ("承揽合同", "建设工程合同", "加工定作", "施工"),
        "illegal_monopoly": ("非法垄断技术", "限制新的研究开发", "限制从其他渠道吸收技术", "阻碍合理实施专利", "限制技术竞争", "限制技术发展"),
        "infringe_achievement": ("侵害他人技术成果", "侵犯他人专利", "侵犯技术秘密", "侵害技术秘密", "侵犯他人合法权益"),
        "trade_secret_invalid": ("侵害他人技术秘密的技术合同无效", "侵害技术秘密合同无效", "技术秘密合同无效"),
        "good_faith_acquirer": ("善意取得", "善意取得方", "善意受让"),
        "reasonable_use_fee": ("合理使用费", "使用费"),
        "fraud_contract": ("欺诈订立", "现有技术冒充委托开发", "重复收费", "同一课题分别订立合同", "违背真实意思"),
        "duty_achievement": ("职务技术成果", "执行单位工作任务", "履行岗位职责", "离职后一年内", "利用单位物质技术条件", "单位未公开技术成果"),
        "non_duty_achievement": ("非职务技术成果", "个人完成", "未利用单位条件", "个人技术成果"),
        "ownership_dispute": ("权属争议", "成果归属", "使用权归属", "转让权归属", "专利申请权归属"),
        "termination_request": ("解除技术合同", "解除合同", "主张解除"),
        "delayed_main_obligation": ("迟延履行主要债务", "逾期交付", "逾期付款", "未履行主要债务"),
        "urged": ("催告", "经催告", "书面催告"),
        "over_30_days": ("超过30日", "超过三十日", "30日内仍未履行", "三十日内仍未履行"),
        "technology_import_export": ("技术进出口", "进口技术", "出口技术", "跨境技术转让"),
        "development_failed": ("开发失败", "研发失败", "未能成功", "研究开发失败"),
        "risk_agreed": ("风险分担约定", "约定风险", "按约定分担"),
        "no_risk_agreement": ("未约定风险", "没有风险分担约定", "约定不明"),
        "developer_breach": ("研究开发人违约", "未按期完成", "未交付成果", "经费使用不合理", "研发延误"),
        "client_breach": ("委托人违约", "未支付经费", "未提供资料", "未完成协作", "不接受成果"),
        "stagnation_delay_failure": ("停滞", "延误", "失败"),
        "invention_creation": ("发明创造", "专利申请权", "申请专利"),
        "patent_agreed": ("专利申请权有约定", "约定专利申请权", "按约定归属"),
        "technical_secret_result": ("技术秘密成果", "技术秘密使用权", "技术秘密转让权"),
        "result_agreed": ("成果归属有约定", "约定成果归属", "按约定分配"),
        "licensor_not_owner": ("非合法拥有者", "无权许可", "无权转让", "不是合法拥有者"),
        "technology_defective": ("技术不完整", "技术有误", "技术无效", "不能达到约定目标"),
        "license_not_provided": ("未按约定许可技术", "未交付技术资料", "未提供许可"),
        "license_over_scope": ("超越约定范围许可", "擅自许可第三人", "违反保密义务"),
        "fee_unpaid": ("未支付使用费", "拖欠使用费", "欠付使用费"),
        "licensee_over_scope": ("超越约定范围使用", "擅自许可第三人", "超范围使用"),
        "licensee_as_agreed": ("按约定实施", "按约定使用", "依约实施专利"),
        "third_party_infringement": ("侵害他人合法权益", "侵犯第三人专利", "侵犯第三人技术秘密"),
        "followup_improvement": ("后续改进", "改进成果", "后续改进成果"),
        "share_agreed": ("分享约定", "约定分享", "按约定分享"),
        "consulting_report_conform": ("咨询报告符合约定", "报告符合要求", "符合要求的咨询报告"),
        "consulting_report_nonconform": ("报告不符合约定", "咨询报告不符合要求", "报告不合格"),
        "decision_loss": ("决策造成损失", "按咨询报告决策", "决策损失"),
        "new_result": ("新的技术成果", "新技术成果", "履行过程中产生新成果"),
        "trustee_uses_client_material": ("受托人利用委托人提供的技术资料", "利用委托人工作条件"),
        "client_uses_trustee_result": ("委托人利用受托人的工作成果", "利用受托人成果"),
        "research_org_no_capacity": ("科研组织不具有民事主体资格", "无民事主体资格科研组织", "课题组签订合同"),
        "authorized_or_ratified": ("经授权", "经认可", "授权订立", "事后认可"),
        "unauthorized_org": ("未经授权", "未经认可", "没有授权"),
    },
)


TECHNOLOGY_CONFIGS: Dict[str, TechnologyConfig] = {TECHNOLOGY_CONFIG.key: TECHNOLOGY_CONFIG}


def get_technology_config(contract_type: str | None = None) -> TechnologyConfig:
    key = (contract_type or "technology").strip().lower()
    aliases = {
        "tech": "technology",
        "technology_contract": "technology",
        "技术": "technology",
        "技术合同": "technology",
        "技术开发": "technology",
        "技术转让": "technology",
        "技术许可": "technology",
        "技术咨询": "technology",
        "技术服务": "technology",
    }
    return TECHNOLOGY_CONFIGS.get(aliases.get(key, key), TECHNOLOGY_CONFIG)
