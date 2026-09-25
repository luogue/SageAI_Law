"""Sale-contract adjudication configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from adjudicate.lease_configs import MOUNT_POST, PatchMount


Terms = Tuple[str, ...]
PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class SaleConfig:
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


SALE_CONFIG = SaleConfig(
    key="sale",
    display_name="买卖合同",
    fact_mapping={
        "合同主体": "出卖人/买受人",
        "核心义务": "转移所有权 + 交付符合质量要求的标的物",
        "归责原则": "严格责任（出卖人对质量瑕疵承担责任）",
        "三重逻辑": "所有权转移 + 风险负担 + 瑕疵担保",
        "核心争议": "标的物是否交付 → 风险谁承担 → 质量是否符合要求 → 如何救济",
    },
    reused_modules=("管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"),
    patch_mounts=(
        PatchMount("B1", "contract_nature", MOUNT_POST, "分期付款买卖", "买受人分期支付总价款", "《民法典》第634条", "未付到期价款达到总价款五分之一且催告后仍未支付的，出卖人可请求全部价款或解除合同", "分期付款买卖，未付价款达总价款的 [比例]，出卖人 [可以/不可以] 请求支付全部价款或解除合同。"),
        PatchMount("B2", "contract_nature", MOUNT_POST, "试用买卖", "约定由买受人试用或检验标的物，以认可标的物为条件", "《民法典》第637条至第640条", "审查试用期、购买表示、默示购买行为及试用期风险负担", "试用买卖，试用期限 [已/未] 届满，买受人 [已/未] 表示购买，合同 [成立/不成立]。"),
        PatchMount("B3", "contract_nature", MOUNT_POST, "所有权保留买卖", "合同约定买受人未履行支付价款或其他义务时所有权属于出卖人", "《民法典》第641条至第643条", "审查登记、催告、取回权和回赎机会", "所有权保留 [已/未] 登记，买受人 [已/未] 触发取回权情形，出卖人 [有权/无权] 取回标的物。"),
        PatchMount("B4", "contract_nature", MOUNT_POST, "凭样品买卖", "买卖双方凭样品确定标的物质量", "《民法典》买卖合同质量瑕疵规则", "交付标的物应与样品及说明质量一致，不一致按质量瑕疵处理", "凭样品买卖，交付标的物 [符合/不符合] 样品质量，出卖人应承担相应违约责任。"),
        PatchMount("B5", "ownership_transfer", MOUNT_POST, "一物数卖", "出卖人就同一标的物订立多重买卖合同", "买卖合同司法解释第6条", "先受领交付优先；均未受领的先付款优先；均未受领也未付款的合同成立在先优先", "一物数卖，按 [先行受领交付/先行支付价款/合同成立在先] 规则确定履行对象。"),
        PatchMount("B6", "damage_compensation", MOUNT_POST, "可得利益损失", "守约方主张预期利润损失", "《民法典》第584条", "确认违约、实际损失、可得利益和可预见范围，超出可预见范围不支持", "可得利益损失 [成立/不成立]，赔偿金额为 [实际损失 + 可得利益] 元，但不得超过可预见范围。"),
        PatchMount("B7", "contract_effect", MOUNT_POST, "免责条款效力审查", "合同有减轻或免除出卖人瑕疵担保责任的条款", "《民法典》第618条", "出卖人故意或重大过失不告知瑕疵的，不得主张免责或限责", "免责条款 [有效/无效]，出卖人 [应/不应] 承担瑕疵担保责任。"),
        PatchMount("B8", "remedy_execution", MOUNT_POST, "定金与违约金、赔偿损失的关系", "合同同时约定定金和违约金，或守约方同时主张定金和赔偿损失", "《民法典》定金、违约金及损害赔偿规则", "定金与违约金只能择一；定金不足以弥补损失的，可请求赔偿超过定金部分", "定金与违约金不可以并用，守约方应择一主张；定金不足部分可以另行主张赔偿。"),
        PatchMount("B9", "defect_severity", MOUNT_POST, "合同目的不能实现的认定标准", "买受人主张质量瑕疵致使合同目的不能实现", "《民法典》第610条", "审查能否正常使用、价值是否严重减损、合同主要目的是否落空", "合同目的 [已/未] 落空，买受人 [可以/不可以] 拒绝接受标的物或解除合同。"),
        PatchMount("B10", "inspection_period", MOUNT_POST, "买受人检验期限的推定", "当事人未约定检验期限，买受人签收载明数量、型号、规格的单据", "《民法典》第623条", "推定已对数量和外观瑕疵完成检验，但不适用于隐蔽瑕疵且可被相反证据推翻", "买受人 [已/未] 签收载明数量/型号/规格的单据，[推定/不推定] 已完成数量和外观瑕疵检验。"),
        PatchMount("B11", "delivery_review", MOUNT_POST, "电子信息产品的交付", "标的物为无需以有形载体交付的电子信息产品", "买卖合同司法解释第2条", "交付方式约定不明且无法确定的，自买受人收到电子信息产品或权利凭证时完成交付", "电子信息产品，交付方式约定不明，自买受人收到电子信息产品或权利凭证时完成交付。"),
        PatchMount("B12", "delivery_review", MOUNT_POST, "多交标的物的处理", "出卖人多交标的物", "买卖合同司法解释第3条", "买受人可以接收或拒绝多交部分；拒收代管费用由出卖人承担，非因买受人故意或重大过失的损失由出卖人承担", "多交标的物，买受人 [接收/拒绝接收]，代为保管费用由出卖人承担。"),
        PatchMount("B13", "contract_formation", MOUNT_POST, "发票的证明效力", "仅以发票证明交付或付款事实", "买卖合同司法解释第5条", "专用发票及抵扣资料通常不足以单独证明交付；普通发票可按约定或交易习惯证明付款", "发票 [可以/不足以] 证明 [交付/付款] 事实。"),
        PatchMount("B14", "trial_sale_risk", MOUNT_POST, "试用买卖中标的物风险负担", "试用期间标的物毁损、灭失", "《民法典》第640条", "试用期内标的物毁损灭失风险由出卖人承担", "试用期内标的物毁损灭失，风险由出卖人承担。"),
        PatchMount("B15", "contract_nature", MOUNT_POST, "招标投标买卖与拍卖", "合同通过招标投标或拍卖方式订立", "《民法典》第644条、第645条", "适用招标投标法、拍卖法等特别法，特别法未规定的适用买卖合同一般规定", "招标投标买卖/拍卖，适用特别法规定。"),
    ),
    terms={
        "jurisdiction_question": ("哪里起诉", "去哪里起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
        "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "告对人"),
        "sale_contract": ("买卖合同", "买卖", "出卖人", "买受人", "卖方", "买方", "货款", "标的物"),
        "written_contract": ("书面合同", "签订买卖合同", "签了合同", "合同约定"),
        "no_written_contract": ("无书面合同", "没有书面合同", "未签书面合同", "没有签合同"),
        "delivery_note": ("送货单", "收货单", "结算单", "对账单", "发票", "交易习惯", "交易方式"),
        "invoice_only": ("仅以发票", "仅以增值税专用发票", "只有发票", "仅凭发票", "只有增值税发票", "只有普通发票"),
        "vat_invoice": ("增值税专用发票", "税款抵扣资料", "抵扣资料"),
        "ordinary_invoice": ("普通发票", "发票作为付款凭证", "以发票证明付款"),
        "contract_invalid": ("合同无效", "无效合同", "违法无效", "合同不成立"),
        "no_disposition_right": ("无处分权", "无权处分", "不能转移所有权", "不是所有权人", "所有权不能转移"),
        "delivery_date": ("交付", "收货", "签收", "应交付", "付款", "合同成立"),
        "third_party_tort": ("路人侵权", "第三方侵权", "他人损害", "外人造成"),
        "installment_sale": ("分期付款", "分期支付", "分次付款", "按期付款"),
        "total_price": ("总价款", "总价", "全部价款"),
        "unpaid_price": ("未支付到期价款", "未付价款", "欠付价款", "拖欠货款", "未支付货款"),
        "seller_urged": ("催告", "经催告", "书面催告", "催款"),
        "reasonable_period_unpaid": ("合理期限内仍未支付", "催告后仍未付款", "催告后未支付", "仍未付清"),
        "trial_sale": ("试用买卖", "试用期", "试用", "先试后买", "试用期限"),
        "trial_period_expired": ("试用期届满", "试用期限届满", "试用期满"),
        "buyer_accepts_purchase": ("表示购买", "同意购买", "确认购买", "视为购买", "支付部分价款", "转卖", "出租", "设立担保"),
        "buyer_refuses_purchase": ("拒绝购买", "不同意购买", "退回试用品"),
        "trial_damage": ("试用期内毁损", "试用期间毁损", "试用期间标的物毁损灭失", "试用期内标的物毁损灭失", "试用期内灭失", "试用期间灭失", "试用期间损坏"),
        "title_retention": ("所有权保留", "未付清前所有权属于出卖人", "所有权属于卖方", "保留所有权"),
        "registered": ("已登记", "办理登记", "登记所有权保留"),
        "not_registered": ("未登记", "没有登记"),
        "seller_retake": ("取回标的物", "要求取回", "出卖人取回", "收回标的物"),
        "redemption": ("回赎", "回赎期限", "消除取回事由"),
        "sample_sale": ("凭样品买卖", "样品", "封存样品", "按样品"),
        "sample_conform": ("符合样品", "与样品一致", "质量相同"),
        "sample_nonconform": ("不符合样品", "与样品不一致", "不同于样品"),
        "tender_auction": ("招标投标", "招投标", "拍卖", "竞拍", "中标"),
        "delivered": ("已交付", "交付完成", "已经交货", "买受人已收货", "签收"),
        "not_delivered": ("未交付", "迟延交付", "逾期交付", "未按期交付", "没有交货"),
        "delivery_to_carrier": ("交付承运人", "交给第一承运人", "交给承运人", "货交承运人", "承运人收货"),
        "electronic_product": ("电子信息产品", "数字产品", "软件", "电子文件", "账号", "激活码", "权利凭证"),
        "electronic_received": ("收到电子信息产品", "收到权利凭证", "收到账号", "收到激活码", "已下载"),
        "over_delivery": ("多交标的物", "多交货", "超量交付", "多送货"),
        "buyer_accepts_extra": ("接收多交部分", "接受多交部分", "同意接收多交"),
        "buyer_rejects_extra": ("拒绝接收多交", "拒收多交部分", "拒绝多交部分"),
        "custody_extra_fee": ("代为保管费用", "保管费用", "保管费"),
        "unpaid_payment": ("未支付价款", "拖欠货款", "欠货款", "迟延付款", "未按期付款"),
        "suspend_payment_right": ("中止支付", "暂停付款", "第三人享有权利", "权利瑕疵"),
        "seller_security": ("提供担保", "适当担保"),
        "risk_loss": ("毁损", "灭失", "损坏", "丢失", "风险负担", "货物损失"),
        "before_delivery": ("交付前", "交货前", "签收前", "收货前"),
        "after_delivery": ("交付后", "交货后", "签收后", "收货后"),
        "buyer_delay_caused_non_delivery": ("买受人原因未按期交付", "买方原因未交付", "买受人拖延受领", "买受人原因导致未交付"),
        "in_transit_sale": ("路货买卖", "在途标的物", "在途货物"),
        "buyer_refuses_collect": ("未收取标的物", "拒绝收货", "不收货", "拒绝受领", "未按约定收取"),
        "quality_nonconform": ("质量不合格", "质量不符合", "质量瑕疵", "不符合质量要求", "存在质量问题", "货不对板"),
        "quality_conform": ("质量合格", "符合质量要求", "符合约定", "验收合格"),
        "quality_standard": ("质量标准", "国家标准", "行业标准", "质量说明", "约定质量", "通常标准"),
        "inspection_period_agreed": ("约定检验期限", "检验期", "异议期", "约定异议期限"),
        "timely_notice": ("期限内通知", "及时通知", "已提出异议", "合理期限内通知", "质保期内通知"),
        "late_notice": ("未及时通知", "逾期通知", "合理期限内未通知", "二年内未通知", "怠于通知"),
        "signed_document": ("签收送货单", "签收确认单", "签收单", "送货单载明数量型号规格", "确认单载明数量型号规格"),
        "hidden_defect": ("隐蔽瑕疵", "内部瑕疵", "无法外观发现"),
        "short_inspection_period": ("检验期限过短", "异议期过短", "检验期太短"),
        "seller_knew_defect": ("出卖人知道瑕疵", "卖方明知瑕疵", "应当知道瑕疵", "故意隐瞒瑕疵"),
        "minor_defect": ("轻微瑕疵", "可修理", "可更换", "小瑕疵"),
        "general_defect": ("一般瑕疵", "影响使用但可补救", "可补救"),
        "serious_defect": ("严重瑕疵", "无法正常使用", "使用价值严重减损", "合同目的不能实现", "主要目的落空", "无法实现合同目的"),
        "repair_requested": ("要求修理", "修理", "维修"),
        "replace_requested": ("要求更换", "更换"),
        "return_requested": ("退货", "解除合同", "拒绝接受", "要求解除"),
        "reduce_price_requested": ("减少价款", "降价", "扣减价款", "少付货款"),
        "compensation_requested": ("赔偿损失", "要求赔偿", "损失赔偿"),
        "actual_loss": ("实际损失", "损失", "维修费", "差价损失"),
        "expected_profit": ("可得利益", "预期利润", "利润损失", "转售利润"),
        "foreseeable_amount": ("可预见范围", "可预见金额", "订约时可预见"),
        "deposit_penalty": ("定金", "定金罚则", "双倍返还定金"),
        "liquidated_damage": ("违约金", "约定违约金"),
        "third_party_right": ("第三人享有权利", "抵押", "质押", "租赁权", "被查封", "权利瑕疵"),
        "buyer_knew_right": ("买受人知道", "买方明知", "应当知道第三人权利"),
        "buyer_not_knew_right": ("买受人不知道", "买方不知情", "不知存在第三人权利"),
        "multi_sale": ("一物数卖", "多重买卖", "卖给多人", "同一标的物卖给多人"),
        "first_delivery": ("先行受领交付", "先收货", "已经先交付"),
        "first_payment": ("先行支付价款", "先付款", "先支付货款"),
        "first_contract": ("合同成立在先", "先签合同", "合同在先"),
        "exemption_clause": ("免责条款", "免除瑕疵责任", "不承担质量责任", "减轻瑕疵责任", "限责条款"),
        "seller_intent_gross_no_notice": ("故意不告知", "重大过失不告知", "故意隐瞒", "明知不告知"),
    },
)


SALE_CONFIGS: Dict[str, SaleConfig] = {SALE_CONFIG.key: SALE_CONFIG}


def get_sale_config(contract_type: str | None = None) -> SaleConfig:
    key = (contract_type or "sale").strip().lower()
    aliases = {
        "sales": "sale",
        "purchase": "sale",
        "purchase_sale": "sale",
        "goods_sale": "sale",
        "买卖": "sale",
        "买卖合同": "sale",
        "货物买卖": "sale",
    }
    return SALE_CONFIGS.get(aliases.get(key, key), SALE_CONFIG)
