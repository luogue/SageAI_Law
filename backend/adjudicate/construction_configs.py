"""Construction-contract adjudication configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from adjudicate.lease_configs import MOUNT_POST, PatchMount


Terms = Tuple[str, ...]
PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class ConstructionConfig:
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


CONSTRUCTION_CONFIG = ConstructionConfig(
    key="construction",
    display_name="建设工程合同",
    fact_mapping={
        "合同主体": "发包人/承包人/勘察人/设计人/转包人/违法分包人/实际施工人",
        "核心义务": "进行工程建设（承包人）/ 支付价款（发包人）",
        "归责原则": "过错责任（各方对自身违约/过错行为承担责任）",
        "核心争议": "合同是否有效 → 工期是否延误 → 质量是否合格 → 价款如何结算 → 是否享有优先受偿权",
    },
    reused_modules=("管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"),
    patch_mounts=(
        PatchMount("C1", "contract_effect", MOUNT_POST, "合同无效但工程合格的处理", "建设工程施工合同无效但工程验收合格", "《民法典》第793条第1款", "参照合同关于工程价款的约定折价补偿承包人", "合同无效但工程验收合格，应参照合同约定折价补偿承包人 [金额] 元。"),
        PatchMount("C2", "contract_effect", MOUNT_POST, "合同无效且工程不合格的处理", "建设工程施工合同无效且工程验收不合格", "《民法典》第793条第2款", "可修复的由承包人承担修复费用；不可修复的无权请求折价补偿", "合同无效且工程不合格，[可修复/不可修复]，承包人 [可/不可] 主张折价补偿。"),
        PatchMount("C3", "contract_effect", MOUNT_POST, "黑白合同的认定", "另行合同与中标合同实质性内容不一致", "建设工程司法解释（一）第2条", "工程范围、工期、质量、价款等实质性内容不一致的，以中标合同为准", "黑白合同成立，应按中标合同确定权利义务。"),
        PatchMount("C4", "contract_effect", MOUNT_POST, "出借资质（挂靠）的连带责任", "无资质实际施工人借用有资质企业名义", "建设工程司法解释（一）第7条", "出借方与借用方对因出借资质造成的损失承担连带赔偿责任", "出借资质成立，出借方与借用方对损失承担连带赔偿责任。"),
        PatchMount("C5", "priority_payment", MOUNT_POST, "工程价款优先受偿权的行使", "发包人未按约支付工程价款", "《民法典》第807条、建设工程司法解释（一）第35-41条", "质量合格、催告后逾期不付、18个月内行使的，承包人享有优先受偿权", "承包人享有建设工程价款优先受偿权，优先于抵押权和其他债权。"),
        PatchMount("C6", "actual_constructor", MOUNT_POST, "实际施工人直接起诉发包人", "实际施工人主张权利", "建设工程司法解释（一）第43条、第44条", "可向发包人主张权利，发包人在欠付工程款范围内承担责任；可提起代位权诉讼", "实际施工人可向发包人主张权利，发包人在欠付工程款 [金额] 元范围内承担责任。"),
        PatchMount("C7", "period_identification", MOUNT_POST, "开工日期与竣工日期的认定", "当事人对开工或竣工日期有争议", "建设工程司法解释（一）第8条、第9条", "开工按通知、具备条件、实际进场顺序认定；竣工按验收合格、提交报告、擅自使用规则认定", "开工日期认定为 [日期]，竣工日期认定为 [日期]。"),
        PatchMount("C8", "quality_deposit", MOUNT_POST, "工程质量保证金返还", "承包人请求返还工程质量保证金", "建设工程司法解释（一）第17条", "有约定按约定；无约定的竣工验收合格满二年；发包人原因未验收的自提交报告90日后起算", "工程质量保证金 [应/不应] 返还。"),
        PatchMount("C9", "stoppage_loss", MOUNT_POST, "发包人违约造成停工/窝工损失", "发包人未提供材料、设备、场地、资金、技术资料或中途停建缓建", "《民法典》第803条、第804条", "承包人可顺延工期并请求停工、窝工等损失", "发包人违约造成停工/窝工，应赔偿承包人损失 [金额] 元。"),
        PatchMount("C10", "price_interest", MOUNT_POST, "工程款利息的计算", "发包人拖欠工程款，承包人主张利息", "建设工程价款利息规则", "有约定按约定；无约定按同期LPR；起算按交付、提交结算文件、起诉时间确定", "工程款利息按 [LPR/约定利率] 计算，起算时间为 [日期]，利息金额为 [金额] 元。"),
        PatchMount("C11", "contract_type", MOUNT_POST, "勘察、设计合同纠纷的特殊处理", "合同为工程勘察合同或工程设计合同", "《民法典》第794条、第808条", "勘察、设计合同没有特别规定的，适用承揽合同有关规定", "本案为 [勘察/设计] 合同，适用承揽合同相关规定。"),
        PatchMount("C12", "contract_effect", MOUNT_POST, "劳务分包合同的效力", "具有劳务作业法定资质的劳务分包合同", "建设工程司法解释（一）第5条", "具有劳务作业法定资质的承包人与总承包人、分包人签订的劳务分包合同有效", "劳务分包合同有效。"),
        PatchMount("C13", "completion_date", MOUNT_POST, "发包人擅自使用未验收工程的法律后果", "建设工程未经竣工验收，发包人擅自使用", "建设工程司法解释（一）第9条", "以转移占有之日为竣工日期；擅自使用后再主张使用部分质量不符的，不予支持", "发包人擅自使用未验收工程，竣工日期认定为转移占有之日。"),
        PatchMount("C14", "quality_check", MOUNT_POST, "隐蔽工程检查", "隐蔽工程隐蔽前承包人通知检查，发包人未及时检查", "《民法典》第798条", "承包人可顺延工期并请求停工、窝工等损失", "发包人未及时检查隐蔽工程，承包人可顺延工期并索赔损失。"),
        PatchMount("C15", "contract_termination", MOUNT_POST, "建设工程合同解除后的处理", "建设工程合同被解除", "《民法典》第806条", "已完工程质量合格的按约支付工程价款；不合格的参照第793条处理", "合同解除，已完工程质量 [合格/不合格]，[应/不应] 支付工程价款。"),
    ),
    terms={
        "jurisdiction_question": ("哪里起诉", "去哪里起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
        "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "告对人"),
        "construction_contract": ("建设工程合同", "建设工程施工合同", "工程合同", "施工合同", "工程价款", "工程款", "发包人", "承包人"),
        "contract_date": ("签订建设工程合同", "合同签订", "开工", "竣工", "验收合格", "工程款到期", "提交结算"),
        "third_party_tort": ("第三人侵权", "外人造成损害", "他人侵权"),
        "survey_contract": ("勘察合同", "工程勘察", "勘察人"),
        "design_contract": ("设计合同", "工程设计", "设计人"),
        "construction_work_contract": ("施工合同", "建设工程施工", "施工人", "承包施工"),
        "contract_invalid": ("施工合同无效", "建设工程合同无效", "合同无效"),
        "qualification_defect": ("未取得建筑业企业资质", "没有施工资质", "无资质", "超越资质等级", "资质缺陷"),
        "qualification_before_completion": ("竣工前取得相应资质", "竣工前取得资质"),
        "affiliation": ("借用资质", "出借资质", "挂靠", "借用有资质企业名义"),
        "tender_illegal": ("必须招标而未招标", "未招标", "中标无效", "招投标违法"),
        "planning_missing": ("未取得建设工程规划许可证", "没有规划许可证", "规划许可缺失"),
        "planning_obtained_before_suit": ("起诉前取得规划许可证", "起诉前补办规划许可"),
        "illegal_subcontract": ("违法分包", "全部转包", "转包", "支解后分别转包", "分包给无资质单位", "再分包"),
        "black_white_contract": ("黑白合同", "另行签订合同", "阴阳合同", "背离中标合同"),
        "substantive_inconsistency": ("实质性内容不一致", "工程价款不一致", "建设工期不一致", "工程质量不一致", "工程范围不一致"),
        "labor_subcontract": ("劳务分包", "劳务作业分包"),
        "labor_qualification": ("劳务作业法定资质", "具有劳务资质", "劳务资质齐备"),
        "project_accepted": ("验收合格", "工程质量合格", "竣工验收合格", "质量合格"),
        "project_unaccepted": ("验收不合格", "工程验收不合格", "工程质量不合格", "质量不合格", "竣工验收不合格"),
        "repairable": ("可以修复", "可修复", "修复后合格"),
        "unrepairable": ("不可修复", "修复后仍不合格", "无法修复"),
        "developer_fault": ("发包人有过错", "发包人过错"),
        "project_price": ("工程价款", "工程款", "折价补偿", "合同价款"),
        "repair_cost": ("修复费用", "维修费用", "返工费用"),
        "period_dispute": ("工期争议", "开工日期争议", "竣工日期争议", "开工日期", "竣工日期"),
        "start_notice": ("开工通知", "通知载明开工日期"),
        "conditions_missing": ("不具备开工条件", "开工条件不具备"),
        "actual_entry": ("实际进场施工", "实际进场", "进场施工"),
        "completion_accepted": ("竣工验收合格", "验收合格之日"),
        "delay_acceptance": ("拖延验收", "发包人拖延验收"),
        "report_submitted": ("提交竣工验收报告", "提交验收报告"),
        "unauthorized_use": ("擅自使用", "未经竣工验收擅自使用", "未验收即使用", "转移占有"),
        "quality_defect": ("质量不符合约定", "质量问题", "工程质量不合格", "质量瑕疵"),
        "quality_deposit_return": ("返还工程质量保证金", "质量保证金返还", "退还质保金", "工程质量保证金"),
        "deposit_period_due": ("返还期限届满", "质保金期限届满", "满二年", "已满二年"),
        "no_deposit_period": ("未约定返还期限", "没有约定质保金返还期限"),
        "hidden_work": ("隐蔽工程", "隐蔽前", "隐蔽工程检查"),
        "contractor_notified_inspection": ("通知发包人检查", "已通知检查", "通知检查"),
        "developer_no_inspection": ("未及时检查", "没有及时检查", "拒不检查"),
        "unpaid_project_price": ("拖欠工程款", "欠付工程款", "未支付工程价款", "未按约支付价款"),
        "payment_urged": ("催告支付", "经催告", "催告发包人"),
        "priority_claim": ("优先受偿权", "工程价款优先受偿", "拍卖工程", "折价工程"),
        "within_18_months": ("18个月内", "十八个月内", "未超过十八个月"),
        "beyond_18_months": ("超过18个月", "超过十八个月", "已过十八个月"),
        "mortgage_conflict": ("抵押权", "其他债权", "优于抵押权"),
        "worker_interest_harmed": ("损害建筑工人利益", "损害农民工利益"),
        "actual_constructor": ("实际施工人", "无资质实际施工人"),
        "direct_sue_employer": ("直接起诉发包人", "以发包人为被告", "向发包人主张"),
        "subrogation_claim": ("代位权诉讼", "怠于向发包人行使到期债权", "代位权"),
        "amount_owed_by_employer": ("发包人欠付工程款", "欠付转包人工程款", "欠付违法分包人工程款"),
        "termination_request": ("解除建设工程合同", "解除施工合同", "解除合同"),
        "employer_termination": ("发包人解除", "发包人要求解除"),
        "contractor_termination": ("承包人解除", "承包人要求解除"),
        "employer_assistance_breach": ("未提供材料", "未提供设备", "未提供场地", "未提供资金", "未提供技术资料", "不履行协助义务", "材料不符合强制性标准"),
        "urged_unperformed": ("催告后仍未履行", "经催告仍未履行"),
        "completed_quality_ok": ("已完工程质量合格", "已完成工程质量合格"),
        "completed_quality_bad": ("已完工程质量不合格", "已完成工程质量不合格"),
        "stoppage_loss": ("停工损失", "窝工损失", "停工窝工", "倒运", "机械设备调迁", "材料积压"),
        "employer_material_delay": ("未按约定提供原材料", "未按约定提供设备", "未按约定提供场地", "未按约定提供资金", "未按约定提供技术资料", "中途停建", "中途缓建"),
        "interest_claim": ("工程款利息", "欠付工程款利息", "主张利息"),
        "agreed_interest": ("约定利率", "约定利息"),
        "lpr_interest": ("LPR", "贷款市场报价利率"),
        "project_delivered": ("工程已交付", "实际交付"),
        "settlement_submitted": ("提交竣工结算文件", "提交结算文件"),
        "lawsuit_filed": ("起诉之日", "起诉时"),
        "actual_loss": ("损失", "停工损失", "窝工损失", "损失金额"),
        "interest_amount": ("利息金额", "利息"),
        "quality_deposit_amount": ("质量保证金", "质保金"),
    },
)


CONSTRUCTION_CONFIGS: Dict[str, ConstructionConfig] = {CONSTRUCTION_CONFIG.key: CONSTRUCTION_CONFIG}


def get_construction_config(contract_type: str | None = None) -> ConstructionConfig:
    key = (contract_type or "construction").strip().lower()
    aliases = {
        "construction_contract": "construction",
        "construction_project": "construction",
        "building": "construction",
        "工程": "construction",
        "建设工程": "construction",
        "建设工程合同": "construction",
        "施工合同": "construction",
    }
    return CONSTRUCTION_CONFIGS.get(aliases.get(key, key), CONSTRUCTION_CONFIG)
