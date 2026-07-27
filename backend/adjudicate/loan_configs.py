"""Loan-contract adjudication configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from adjudicate.lease_configs import MOUNT_POST, MOUNT_PRE, PatchMount


Terms = Tuple[str, ...]
PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class LoanConfig:
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


LOAN_CONFIG = LoanConfig(
    key="loan",
    display_name="借款合同",
    fact_mapping={
        "合同主体": "贷款人/借款人/保证人",
        "核心义务": "提供借款（贷款人）/ 返还借款并支付利息（借款人）",
        "归责原则": "严格责任（未按约还款即构成违约）",
        "核心争议": "本金多少 → 利率多少 → 利息怎么算 → 还了没有 → 保证人是否担责",
    },
    reused_modules=("管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"),
    patch_mounts=(
        PatchMount("L1", "contract_type_identification", MOUNT_POST, "金融借款与民间借贷区分", "需要确定出借人是否为持牌金融机构", "《民法典》第667条、民间借贷司法解释第1条", "持牌金融机构发放贷款为金融借款；自然人、非金融企业等非持牌主体之间资金融通为民间借贷", "本案为 [金融借款/民间借贷]，适用 [金融监管规定/民间借贷司法解释]。"),
        PatchMount("L2", "loan_fact", MOUNT_POST, "砍头息认定", "借条金额与实际到账金额不一致，利息预先扣除", "《民法典》第670条", "按实际借款数额认定本金并计算利息", "存在砍头息 [金额] 元，本金应认定为实际借款数额 [金额] 元。"),
        PatchMount("L3", "interest_cap", MOUNT_POST, "利率上限审查", "合同约定利率", "民间借贷司法解释第26条、第29条", "民间借贷利率、逾期利率、违约金及其他费用总和不得超过合同成立时一年期LPR四倍", "合同成立时一年期LPR为 [X]%，四倍为 [Y]%。约定利率 [Z]% [超过/未超过] 上限，应按 [Y/Z]% 计算。"),
        PatchMount("L4", "repayment_review", MOUNT_POST, "还款冲抵顺序", "借款人部分还款且不足以清偿全部债务", "《民法典》第561条", "除另有约定外，按费用、利息、本金顺序冲抵", "部分还款 [金额] 元，按 [费用→利息→本金] 顺序冲抵，尚欠本金 [金额] 元。"),
        PatchMount("L5", "loan_fact", MOUNT_POST, "仅有转账凭证的借贷关系认定", "原告仅凭转账记录起诉，无借条或欠条", "民间借贷司法解释第17条", "转账凭证可初步证明借贷关系；被告主张其他用途的，由被告举证", "仅有转账凭证，被告 [能/不能] 证明转账系其他用途，借贷关系 [成立/不成立]。"),
        PatchMount("L6", "loan_old_for_new", MOUNT_POST, "借新还旧中保证人责任", "新贷款用于偿还旧贷款", "担保制度相关司法解释", "同一保证人或保证人知道借新还旧的承担保证责任；不同保证人且不知情的不承担", "借新还旧，保证人 [知道/不知道]，新贷与旧贷 [同一/不同一] 保证人，保证人 [应/不应] 承担保证责任。"),
        PatchMount("L7", "contract_effect", MOUNT_POST, "职业放贷人认定", "借款人主张出借人为职业放贷人", "民间借贷司法解释第13条", "未取得放贷资格并以营利为目的向社会不特定对象反复放贷的，合同无效", "出借人 [构成/不构成] 职业放贷人，借款合同 [无效/有效]。"),
        PatchMount("L8", "spousal_debt", MOUNT_POST, "夫妻共同债务认定", "出借人主张夫妻双方共同偿还", "夫妻共同债务规则", "审查是否用于家庭日常生活、共同生活共同经营或夫妻共同意思表示", "本案借款 [属于/不属于] 夫妻共同债务，[应由/不应由] 夫妻双方共同偿还。"),
        PatchMount("L9", "limitation", MOUNT_POST, "诉讼时效中断", "借款人主张诉讼时效已过，出借人主张曾催收或借款人承诺还款", "《民法典》诉讼时效中断规则", "催收、起诉、部分还款或还款承诺可中断时效，中断后重新计算三年", "诉讼时效 [已中断/未中断]，[已/未] 超过3年诉讼时效。"),
        PatchMount("L10", "loan_fact", MOUNT_POST, "债权凭证未载明债权人", "借据、收据、欠条未写明债权人", "民间借贷司法解释第2条", "凭证持有人可初步证明债权人资格；被告有事实依据抗辩的，需进一步审查", "债权凭证未载明债权人，原告债权人资格 [成立/不成立]。"),
        PatchMount("L11", "contract_type_identification", MOUNT_POST, "以买卖担保借款", "以签订买卖合同作为借款担保，债权人请求履行买卖合同", "民间借贷司法解释相关规则", "实质为借贷担保的，按民间借贷审理，不得直接请求过户实现流质效果", "本案实质为 [民间借贷/买卖合同]，应按 [民间借贷/买卖合同] 法律关系审理。"),
        PatchMount("L12", "loan_purpose", MOUNT_POST, "未按约定用途使用借款", "借款人未按约定用途使用借款", "《民法典》第673条", "贷款人可停止发放、提前收回借款或解除合同", "借款人未按约定用途使用借款，贷款人 [可以/不可以] 提前收回借款或解除合同。"),
        PatchMount("L13", "loan_fact", MOUNT_PRE, "贷款人未按约定提供借款", "贷款人未按约定日期或数额提供借款", "《民法典》第671条", "未按时提供造成损失的赔偿；未足额提供的按实际提供金额认定本金", "贷款人 [已/未] 按约定提供借款，造成损失 [金额] 元，[应/不应] 赔偿。"),
        PatchMount("L14", "contract_formation", MOUNT_POST, "自然人间借款成立时间", "自然人之间借款合同", "《民法典》第679条、民间借贷司法解释第9条", "自然人借款自现金收到、转账到账或取得票据权利时成立；未提供借款的合同未成立", "自然人间借款合同，贷款人 [已/未] 提供借款，合同 [成立/未成立]。"),
        PatchMount("L15", "contract_effect", MOUNT_POST, "企业间借贷效力", "法人或非法人组织之间为生产经营需要借贷", "民间借贷司法解释第11条", "为生产经营需要订立的企业间借贷，除法定无效情形外有效", "企业间借贷 [有效/无效]。"),
    ),
    terms={
        "jurisdiction_question": ("哪里起诉", "去哪里起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
        "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "告对人"),
        "loan_contract": ("借款合同", "借贷", "借款人", "贷款人", "出借人", "借条", "欠条", "本金", "利息"),
        "contract_date": ("借款日期", "合同签订", "出借", "放款", "转账", "到期", "还款期限"),
        "third_party_tort": ("第三人侵权", "路人侵权", "外人造成损害", "他人侵权"),
        "financial_institution_lender": ("银行", "信托公司", "消费金融公司", "小额贷款公司", "金融机构", "持牌金融机构"),
        "private_lender": ("自然人出借", "朋友借款", "民间借贷", "个人借款", "非金融企业出借"),
        "sale_security": ("买卖合同作为担保", "以买卖担保借款", "让与担保", "借款到期不过户", "请求履行买卖合同", "流质"),
        "natural_person_loan": ("自然人之间", "个人之间", "朋友之间", "个人借款"),
        "loan_provided": ("已经提供借款", "实际到账", "收到借款", "现金收到", "转账到账", "资金到账", "已放款"),
        "loan_not_provided": ("未提供借款", "没有放款", "未放款", "未到账", "没有收到借款"),
        "contract_invalid": ("合同无效", "无效合同", "违法无效"),
        "relending_bank_loan": ("套取金融机构贷款转贷", "银行贷款转贷", "转贷牟利"),
        "illegal_fund_source": ("非法吸收存款", "向公众集资", "向职工集资转贷", "向营利法人借贷后转贷"),
        "illegal_purpose_known": ("明知用于赌博", "明知用于诈骗", "明知违法犯罪", "用于违法犯罪"),
        "public_order_violation": ("违背公序良俗", "违反公序良俗"),
        "professional_lender_claim": ("职业放贷人", "职业放贷", "反复放贷", "经常放贷", "向不特定对象放贷"),
        "professional_lender_proved": ("多次反复", "放贷对象众多", "经常性放贷", "营业性放贷", "经营性放贷"),
        "enterprise_loan": ("企业间借贷", "公司之间借款", "法人之间借贷", "企业之间借款"),
        "business_need": ("生产经营需要", "经营周转", "公司经营", "生产经营"),
        "loan_voucher": ("借据", "借条", "欠条", "收据", "债权凭证"),
        "voucher_no_creditor": ("未载明债权人", "没写债权人", "借条没有写出借人", "欠条未写债权人"),
        "only_transfer_record": ("仅有转账凭证", "只有转账记录", "无借条只有转账", "没有借条只有转账", "仅凭银行流水"),
        "other_purpose_defense": ("抗辩转账系其他用途", "说是偿还旧债", "说不是借款", "主张货款", "主张赠与"),
        "other_purpose_proved": ("能证明其他用途", "已证明不是借款", "证明系货款", "证明系赠与", "证明系偿还旧债"),
        "nominal_principal": ("借条金额", "合同本金", "约定本金", "写明本金", "名义本金"),
        "actual_received": ("实际收到", "实际到账", "实际借款数额", "到账金额", "实收本金"),
        "deducted_interest": ("砍头息", "预扣利息", "先扣利息", "利息预先扣除", "扣除服务费"),
        "repaid": ("已还款", "已经还款", "部分还款", "偿还", "归还"),
        "partial_repayment": ("部分还款", "未还清", "不足以清偿", "只还了一部分"),
        "repayment_amount": ("还款", "偿还", "归还", "部分还款"),
        "cost_amount": ("费用", "诉讼费", "律师费", "实现债权费用"),
        "interest_amount": ("利息", "逾期利息", "借期内利息"),
        "principal_amount": ("本金", "借款本金", "尚欠本金"),
        "interest_agreed": ("约定利息", "约定利率", "月息", "年利率", "利率"),
        "no_interest_agreed": ("没有约定利息", "未约定利息", "无利息约定", "没写利息"),
        "annual_rate": ("年利率", "年息", "年化利率"),
        "monthly_rate": ("月息", "月利率"),
        "lpr_rate": ("LPR", "一年期LPR", "贷款市场报价利率"),
        "overdue_interest": ("逾期利息", "逾期利率", "逾期还款利息"),
        "no_overdue_rate": ("未约定逾期利率", "没有逾期利率", "未写逾期利息"),
        "compound_interest": ("复利", "利滚利", "对利息计息"),
        "compound_agreed": ("明确约定复利", "约定对期内利息计收复利"),
        "liquidated_damage_or_fee": ("违约金", "服务费", "管理费", "咨询费", "其他费用"),
        "early_repayment": ("提前还款", "提前偿还", "提前归还"),
        "early_repayment_forbidden": ("禁止提前还款", "不得提前还款", "提前还款违约", "提前还款需支付违约金"),
        "extension_request": ("申请展期", "要求展期", "延期还款", "还款展期"),
        "extension_before_due": ("到期前申请", "还款期限届满前申请"),
        "lender_agreed_extension": ("贷款人同意展期", "出借人同意展期", "同意延期"),
        "guarantee_contract": ("保证合同", "保证人", "担保人", "提供保证", "保证担保"),
        "joint_guarantee": ("连带责任保证", "承担连带责任", "连带保证"),
        "general_guarantee": ("一般保证", "先诉抗辩权"),
        "guarantee_period_expired": ("保证期间已过", "超过保证期间", "担保期限已过"),
        "loan_old_for_new": ("借新还旧", "新贷还旧贷", "以新贷偿还旧贷"),
        "same_guarantor": ("同一保证人", "新旧贷保证人相同"),
        "guarantor_knows": ("保证人知道", "保证人明知", "保证合同写明借新还旧"),
        "guarantor_not_knows": ("保证人不知道", "保证人不知情", "不应当知道"),
        "spousal_debt": ("夫妻共同债务", "配偶共同偿还", "夫妻双方共同偿还", "夫妻共同还款"),
        "daily_family_need": ("家庭日常生活需要", "家庭生活", "家用"),
        "joint_business_or_intent": ("共同经营", "共同生产经营", "夫妻共同意思表示", "配偶签字", "配偶追认", "用于夫妻共同生活"),
        "beyond_family_need": ("超出家庭日常生活", "大额借款", "明显超过家用"),
        "misuse_loan": ("未按约定用途使用借款", "改变借款用途", "挪作他用", "未用于约定用途"),
        "lender_not_provide": ("贷款人未按约定提供借款", "出借人未按时放款", "未足额放款", "未按约定数额提供"),
        "lender_late_provide": ("未按时提供", "逾期放款", "迟延放款"),
        "limitation_defense": ("诉讼时效已过", "超过诉讼时效", "时效抗辩", "过了三年"),
        "collection_or_ack": ("催收", "书面催收", "起诉", "还款承诺", "部分还款", "承诺还款", "同意履行"),
    },
)


LOAN_CONFIGS: Dict[str, LoanConfig] = {LOAN_CONFIG.key: LOAN_CONFIG}


def get_loan_config(contract_type: str | None = None) -> LoanConfig:
    key = (contract_type or "loan").strip().lower()
    aliases = {
        "borrow": "loan",
        "lending": "loan",
        "credit": "loan",
        "借款": "loan",
        "借贷": "loan",
        "借款合同": "loan",
        "民间借贷": "loan",
        "金融借款": "loan",
    }
    return LOAN_CONFIGS.get(aliases.get(key, key), LOAN_CONFIG)
