"""Finance-lease adjudication configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from adjudicate.lease_configs import MOUNT_POST, PatchMount


Terms = Tuple[str, ...]
PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class FinanceLeaseConfig:
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


FINANCE_LEASE_CONFIG = FinanceLeaseConfig(
    key="finance_lease",
    display_name="融资租赁合同",
    fact_mapping={
        "合同主体": "出租人/承租人/出卖人",
        "核心义务": "出资购买租赁物并提供给承租人使用（出租人）/ 支付租金并妥善保管租赁物（承租人）",
        "归责原则": "出租人一般不承担租赁物瑕疵担保责任（例外：干预选择/依赖技能）",
        "核心争议": "是否构成融资租赁法律关系 → 租金是否支付 → 违约救济方式选择（租金加速到期 vs 解除收回） → 租赁物归属与价值清算",
    },
    reused_modules=("管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"),
    patch_mounts=(
        PatchMount("F1", "finance_lease_nature", MOUNT_POST, "融资租赁法律关系认定", "当事人对是否构成融资租赁合同存在争议", "《民法典》第735条、融资租赁司法解释第1条", "结合标的物性质、价值、租金构成、权利义务综合判断；不构成的按实际法律关系处理", "本案 [构成/不构成] 融资租赁法律关系，应按 [融资租赁合同/实际法律关系] 处理。"),
        PatchMount("F2", "contract_effect", MOUNT_POST, "虚构租赁物合同无效", "租赁物不存在或为虚构", "《民法典》第737条", "以虚构租赁物方式订立的融资租赁合同无效", "租赁物为虚构，融资租赁合同无效。"),
        PatchMount("F3", "quality_defect", MOUNT_POST, "出租人瑕疵担保责任例外", "租赁物不符合约定，承租人要求出租人承担责任", "《民法典》第747条、融资租赁司法解释第8条", "原则上出租人不担责；承租人依赖出租人技能、出租人干预或决定选择、擅自变更租赁物的除外", "出租人 [不承担/承担] 租赁物质量瑕疵担保责任。"),
        PatchMount("F4", "rent_remedy_choice", MOUNT_POST, "承租人违约时出租人救济方式选择", "承租人欠付租金，经催告后仍不支付", "《民法典》第752条、融资租赁司法解释第10条", "出租人可选择请求支付全部租金，或解除合同收回租赁物；两者只能择一", "出租人选择 [请求支付全部租金/解除合同收回租赁物]，[可以/不可以] 同时主张另一项救济。"),
        PatchMount("F5", "risk_loss", MOUNT_POST, "租赁物毁损灭失后租金义务", "租赁物在承租人占有期间毁损、灭失", "《民法典》第751条、第754条、第756条", "可归责于承租人的继续支付租金；不可归责且不能修复替代的可解除并按折旧补偿", "租赁物毁损灭失 [可归责/不可归责] 于承租人，承租人 [应继续支付租金/可解除合同并按折旧补偿]。"),
        PatchMount("F6", "unauthorized_disposition", MOUNT_POST, "所有权登记与善意取得", "承租人擅自处分租赁物，第三人主张善意取得", "《民法典》第745条、担保制度解释第67条", "出租人所有权未经登记不得对抗善意第三人；已登记可对抗", "租赁物所有权 [已/未] 登记，[可以/不可以] 对抗善意第三人。"),
        PatchMount("F7", "value_settlement", MOUNT_POST, "租赁物收回后的价值清算", "期满归承租人且已付大部分租金，出租人收回租赁物", "《民法典》第758条", "收回价值超过欠付租金及其他费用的，承租人可请求返还差额", "租赁物价值 [金额] 元，欠付租金及其他费用 [金额] 元，差额 [金额] 元，出租人 [应/不应] 返还 [金额] 元。"),
        PatchMount("F8", "finance_lease_nature", MOUNT_POST, "售后回租认定", "承租人将自有物出卖给出租人后再租回", "融资租赁司法解释第2条", "不应仅以承租人和出卖人系同一人为由否定融资租赁法律关系", "售后回租 [构成/不构成] 融资租赁法律关系。"),
        PatchMount("F9", "termination_loss", MOUNT_POST, "解除收回后的损失赔偿计算", "出租人解除合同、收回租赁物并主张赔偿损失", "融资租赁司法解释第11条", "损失为全部未付租金及其他费用减去收回租赁物价值的差额", "损失赔偿范围为全部未付租金及其他费用 [金额] 元减去收回租赁物价值 [金额] 元，差额 [金额] 元。"),
        PatchMount("F10", "sale_contract_failure", MOUNT_POST, "买卖合同无效导致解除的处理", "买卖合同解除、无效或撤销导致融资租赁合同解除", "《民法典》第754条、第755条", "租赁物由承租人选择的，出租人可向承租人主张损失；由出租人选择的自行承担", "租赁物由 [承租人/出租人] 选择，出租人 [有权/无权] 向承租人主张赔偿损失。"),
        PatchMount("F11", "repurchase_guarantee", MOUNT_POST, "回购担保认定与处理", "融资租赁交易涉及出卖人或第三方回购担保", "融资租赁回购担保规则、担保制度规则", "审查回购合同、回购条件和公司决议，条件成就且程序合规的履行回购义务", "回购担保 [有效/无效]，回购条件 [已/未] 成就，回购人 [应/不应] 履行回购义务。"),
        PatchMount("F12", "possession_use", MOUNT_POST, "出租人妨碍占有使用责任", "出租人无正当理由收回、妨碍或干扰承租人占有使用租赁物", "《民法典》第748条", "出租人无正当理由妨碍承租人占有使用造成损失的，应赔偿", "出租人 [构成/不构成] 妨碍承租人占有使用租赁物，[应/不应] 赔偿损失。"),
        PatchMount("F13", "contract_assignment", MOUNT_POST, "融资租赁合同转让影响", "出租人转让融资租赁合同项下部分或全部权利", "融资租赁司法解释第4条", "出租人权利转让不影响融资租赁合同继续履行，受让方不得仅以转让为由请求解除或变更", "融资租赁合同权利转让，合同 [继续有效/不得解除]。"),
        PatchMount("F14", "third_party_damage", MOUNT_POST, "租赁物致人损害责任", "承租人占有期间租赁物造成第三人人身或财产损害", "《民法典》第749条", "承租人占有期间租赁物致第三人损害的，出租人不承担责任", "租赁物致人损害发生在承租人占有期间，出租人不承担责任。"),
        PatchMount("F15", "contract_effect", MOUNT_POST, "合同无效时租赁物归属", "融资租赁合同被确认无效", "《民法典》第760条", "合同无效时租赁物归属有约定按约定；无约定或不明的返还出租人", "融资租赁合同无效，租赁物归属 [按约定/返还出租人]。"),
    ),
    terms={
        "jurisdiction_question": ("哪里起诉", "去哪里起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
        "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "告对人"),
        "finance_lease_contract": ("融资租赁合同", "融资租赁", "出租人", "承租人", "出卖人", "租赁物", "租金"),
        "contract_date": ("签订融资租赁合同", "合同签订", "租金到期", "交付租赁物", "催告", "解除合同", "收回租赁物"),
        "third_party_tort": ("第三人侵权", "路人侵权", "外人造成损害", "他人侵权"),
        "nature_dispute": ("合同性质争议", "名为融资租赁", "实为借款", "不构成融资租赁", "是否构成融资租赁"),
        "real_asset": ("租赁物真实存在", "设备真实存在", "车辆真实存在", "真实租赁物"),
        "fake_asset": ("虚构租赁物", "租赁物不存在", "没有真实租赁物", "虚假租赁物"),
        "rent_includes_cost_profit": ("租金包含成本和利润", "租金覆盖购买成本", "租金构成包含成本", "合理利润"),
        "not_finance_lease": ("实为借款", "只有融资没有融物", "不具有融物属性", "没有买卖关系"),
        "sale_leaseback": ("售后回租", "自有物出卖给出租人再租回", "承租人和出卖人是同一人", "卖给出租人再租回"),
        "admin_license_issue": ("未取得行政许可", "经营使用需行政许可", "没有行政许可"),
        "contract_invalid": ("融资租赁合同无效", "融资租赁无效", "无效合同"),
        "invalid_asset_ownership_agreed": ("无效时归属有约定", "合同无效后租赁物归属约定"),
        "seller_non_delivery": ("出卖人未交付", "迟延交付", "未按约定交付", "催告后仍未交付"),
        "serious_nonconform_delivery": ("标的物严重不符合约定", "租赁物严重不符合约定", "严重质量问题"),
        "lessee_refuses_accept": ("拒绝受领", "承租人拒收", "拒绝接收租赁物"),
        "timely_notify_lessor": ("及时通知出租人", "已通知出租人", "马上通知出租人"),
        "unjustified_refusal": ("无正当理由拒绝受领", "无故拒收", "未及时通知出租人"),
        "quality_defect": ("质量瑕疵", "租赁物不符合约定", "不符合使用目的", "设备质量问题", "车辆质量问题"),
        "lessee_selected_asset": ("承租人选择出卖人和租赁物", "承租人自行选择", "承租人选定"),
        "lessor_skill_reliance": ("依赖出租人技能", "出租人推荐", "依靠出租人专业能力"),
        "lessor_intervened_choice": ("出租人干预选择", "出租人决定选择", "出租人起决定作用", "出租人擅自变更租赁物", "擅自变更出卖人"),
        "claim_against_seller": ("向出卖人索赔", "承租人索赔", "出卖人违约索赔"),
        "lessor_failed_assist": ("出租人未协助索赔", "未提供必要协助", "明知瑕疵未告知", "怠于行使索赔权"),
        "lessor_wrongfully_repossess": ("无正当理由收回租赁物", "出租人擅自收回", "妨碍占有使用", "干扰承租人使用"),
        "third_party_damage": ("造成第三人损害", "致第三人人身损害", "致第三人财产损失", "租赁物伤人"),
        "during_lessee_possession": ("承租人占有期间", "使用期间", "承租期间", "由承租人占有"),
        "maintenance_issue": ("未妥善保管", "未履行维修义务", "保管不善", "使用不当"),
        "unpaid_rent": ("欠付租金", "未支付租金", "逾期支付租金", "拖欠租金"),
        "lessor_urged": ("催告", "经催告", "书面催告", "催收"),
        "reasonable_period_unpaid": ("合理期限内仍不支付", "催告后仍未支付", "仍未付款"),
        "rent_arrears_periods": ("欠付租金", "拖欠租金"),
        "rent_arrears_amount": ("欠付租金", "未付租金", "拖欠租金"),
        "total_rent_amount": ("全部租金", "总租金", "租金总额"),
        "request_all_rent": ("请求支付全部租金", "租金加速到期", "要求全部未付租金", "支付全部剩余租金"),
        "request_terminate_repossess": ("解除合同收回租赁物", "解除并收回租赁物", "要求收回租赁物", "解除合同"),
        "request_both_remedies": ("同时请求全部租金和解除合同", "既请求全部租金又解除", "同时主张另一项救济"),
        "termination_loss_claim": ("赔偿损失", "主张损失赔偿", "解除后损失"),
        "all_unpaid_fees": ("全部未付租金及其他费用", "全部未付租金", "未付租金及费用"),
        "repossessed_asset_value": ("收回租赁物价值", "租赁物价值", "评估价值"),
        "asset_loss": ("毁损灭失", "毁损", "灭失", "损坏灭失", "设备灭失", "车辆灭失"),
        "lessee_fault_loss": ("承租人原因", "承租人过错", "保管不善", "使用不当"),
        "no_fault_loss": ("不可归责于当事人", "不可抗力", "自然灾害", "无法归责"),
        "cannot_repair_replace": ("不能修复", "无法修复", "不能确定替代物", "无法替代"),
        "unauthorized_disposition": ("擅自处分租赁物", "未经同意转让", "未经同意抵押", "未经同意质押", "投资入股", "私自出售"),
        "ownership_registered": ("所有权已登记", "办理所有权登记", "已登记"),
        "ownership_unregistered": ("所有权未登记", "未办理登记", "未经登记", "未登记"),
        "good_faith_third_party": ("善意第三人", "第三人善意取得", "善意取得"),
        "end_ownership_agreed": ("期满归承租人", "租赁期满归承租人所有", "期满所有权归承租人"),
        "end_ownership_unclear": ("期满归属不明", "未约定归属", "所有权归属不明"),
        "symbolic_price": ("象征性价款", "支付一元", "名义价款", "象征性支付"),
        "paid_most_rent": ("已支付大部分租金", "支付大部分租金", "已付大部分"),
        "unable_pay_remaining": ("无力支付剩余租金", "无法支付剩余租金", "剩余租金无力支付"),
        "asset_value": ("租赁物价值", "收回租赁物价值", "评估价值"),
        "unpaid_fees": ("欠付租金及其他费用", "未付租金及费用", "剩余租金及费用"),
        "sale_contract_invalid": ("买卖合同无效", "买卖合同解除", "买卖合同被撤销"),
        "asset_chosen_by_lessee": ("租赁物由承租人选择", "出卖人由承租人选择", "承租人选定租赁物"),
        "asset_chosen_by_lessor": ("租赁物由出租人选择", "出租人选定租赁物"),
        "repurchase_guarantee": ("回购担保", "回购合同", "出卖人回购", "第三方回购"),
        "repurchase_condition_met": ("回购条件成就", "达到回购条件"),
        "repurchase_resolution": ("回购人公司决议", "公司决议", "股东会决议"),
        "contract_assignment": ("出租人转让权利", "融资租赁合同权利转让", "转让融资租赁合同项下权利"),
        "assignee_requests_termination": ("受让方请求解除", "受让方请求变更", "以转让为由解除"),
    },
)


FINANCE_LEASE_CONFIGS: Dict[str, FinanceLeaseConfig] = {FINANCE_LEASE_CONFIG.key: FINANCE_LEASE_CONFIG}


def get_finance_lease_config(contract_type: str | None = None) -> FinanceLeaseConfig:
    key = (contract_type or "finance_lease").strip().lower()
    aliases = {
        "financial_lease": "finance_lease",
        "leasing": "finance_lease",
        "融资租赁": "finance_lease",
        "融资租赁合同": "finance_lease",
        "售后回租": "finance_lease",
    }
    return FINANCE_LEASE_CONFIGS.get(aliases.get(key, key), FINANCE_LEASE_CONFIG)
