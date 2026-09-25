"""Brokerage-contract adjudication configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from adjudicate.lease_configs import MOUNT_POST, PatchMount


Terms = Tuple[str, ...]
PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class BrokerageConfig:
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


BROKERAGE_CONFIG = BrokerageConfig(
    key="brokerage",
    display_name="中介合同",
    fact_mapping={
        "合同主体": "中介人/委托人",
        "核心义务": "报告订约机会或提供媒介服务（中介人）/ 支付报酬（委托人）",
        "归责原则": "过错责任（中介人违反如实报告义务承担赔偿责任）",
        "核心争议": "合同性质认定 → 是否促成合同成立 → 报酬如何计算 → 是否构成“跳单” → 是否违反如实报告义务",
    },
    reused_modules=("管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"),
    patch_mounts=(
        PatchMount("M1", "contract_nature", MOUNT_POST, "中介合同的性质认定", "合同名称或内容模糊，双方对合同性质存在争议", "《民法典》第961条", "按是否报告订约机会、提供媒介服务且不参与交易认定合同性质", "合同性质认定为 [中介合同/行纪合同/委托合同]。"),
        PatchMount("M2", "bypass_order", MOUNT_POST, "“跳单”的认定标准", "委托人绕开中介人直接订立合同，中介人主张报酬", "《民法典》第965条", "审查接受服务、利用交易机会、绕开中介直接订约三个要件及例外情形", "构成/不构成“跳单”，委托人应/不应支付报酬。"),
        PatchMount("M3", "remuneration_calculation", MOUNT_POST, "报酬的计算与负担", "中介人促成合同成立，双方对报酬有争议", "《民法典》第963条", "有约定按约定；无约定或约定不明按劳务合理确定；媒介服务由交易当事人平均负担", "报酬按约定/合理确定，由委托人/合同当事人平均负担。"),
        PatchMount("M4", "necessary_expense", MOUNT_POST, "未促成合同成立时的必要费用", "中介人未促成合同成立，主张必要费用", "《民法典》第964条", "未促成不得请求报酬；有约定时可请求必要费用", "中介人不得请求报酬，可/不可请求必要费用。"),
        PatchMount("M5", "truthful_report", MOUNT_POST, "中介人如实报告义务的违反", "委托人主张中介人未如实报告或提供虚假信息", "《民法典》第962条", "故意隐瞒重要事实或提供虚假情况并损害委托人利益的，丧失报酬请求权并赔偿", "中介人可以/不可以请求报酬，应/不应赔偿。"),
        PatchMount("M6", "best_efforts", MOUNT_POST, "中介人的尽力义务", "委托人主张中介人未尽力促成交易", "诚信原则", "依据合同内容和诚信原则审查中介人是否尽力履行", "中介人已/未履行尽力义务，构成/不构成违约。"),
        PatchMount("M7", "termination", MOUNT_POST, "中介合同解除", "委托人或中介人主张解除中介合同", "《民法典》第966条、第933条", "参照委托合同随时解除规则，按是否有偿确定损害赔偿范围", "中介合同解除有效，赔偿范围为直接损失/直接损失+可得利益。"),
        PatchMount("M8", "oral_contract", MOUNT_POST, "口头中介协议的效力", "双方未签书面中介合同，但存在口头中介合意", "《民法典》第961条", "中介合同不强制书面形式，有证据证明口头合意的合同成立", "口头中介协议成立/不成立。"),
        PatchMount("M9", "staff_act", MOUNT_POST, "中介人工作人员行为的责任归属", "中介人工作人员的行为引发争议", "职务行为责任规则", "审查工作人员行为是否属于职务行为", "责任由中介人/工作人员承担。"),
        PatchMount("M10", "policy_failure", MOUNT_POST, "政策原因导致交易不成的责任", "因限购、贷款政策变化等导致交易不成", "《民法典》第964条", "交易未成不得请求报酬；可依约请求必要费用", "中介人不得请求报酬，可请求必要费用。"),
        PatchMount("M11", "principal_wrong_info", MOUNT_POST, "委托人提供信息有误导致中介服务瑕疵", "委托人提供的信息有误，导致中介服务存在瑕疵", "诚信原则及过错责任", "委托人提供错误信息承担相应责任；中介人明知仍服务的也承担责任", "委托人/中介人承担相应责任。"),
        PatchMount("M12", "standard_clause", MOUNT_POST, "中介合同格式条款的效力", "中介合同中的格式条款被主张无效", "《民法典》第496条、第497条", "不合理免除或减轻责任、加重对方责任、限制主要权利的格式条款无效", "格式条款有效/无效。"),
        PatchMount("M13", "exclusive_entrustment", MOUNT_POST, "独家委托 vs 非独家委托对“跳单”认定的影响", "委托人同时委托多家中介人，原中介人主张“跳单”", "《民法典》第965条", "非独家委托且通过其他中介正当获取相同信息并成交的，不构成跳单", "委托属于/不属于独家委托，构成/不构成“跳单”。"),
        PatchMount("M14", "burden_of_proof", MOUNT_POST, "中介合同纠纷的举证责任", "双方对中介合同关系或中介义务履行存在争议", "民事诉讼举证责任规则", "主张中介合同关系或义务完成的一方承担举证责任", "委托人/中介人承担举证责任。"),
        PatchMount("M15", "post_contract_obligation", MOUNT_POST, "中介合同终止后的后合同义务", "中介合同终止后，一方主张另一方违反后合同义务", "《民法典》第558条", "合同终止后仍应履行通知、协助、保密等义务", "一方违反/未违反后合同义务，应/不应承担责任。"),
    ),
    terms={
        "jurisdiction_question": ("哪里起诉", "去哪里起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
        "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "适格被告"),
        "brokerage_contract": ("中介合同", "中介人", "委托人", "中介费", "佣金", "居间", "媒介服务", "报告订约机会", "房产中介"),
        "contract_date": ("签订中介合同", "合同签订", "提供中介服务", "促成合同", "支付中介费", "催告"),
        "third_party_tort": ("第三人侵权", "外人侵权", "他人侵权"),
        "nature_dispute": ("合同性质争议", "中介还是委托", "中介还是行纪", "名为委托实为中介", "合同性质不明", "居间还是委托"),
        "intro_or_media_service": ("介绍交易机会", "报告订约机会", "提供媒介服务", "撮合交易", "介绍买家", "介绍卖家", "介绍房源", "带看", "居间服务"),
        "not_party_to_deal": ("不参与交易", "不作为买卖双方", "只是介绍", "仅提供信息", "不承担交易合同权利义务"),
        "own_name_trade": ("以自己名义", "自己名义与第三人交易", "行纪人", "代购代销", "寄售"),
        "principal_name_affair": ("以委托人名义", "代理委托人", "受托人以委托人名义", "处理委托事务"),
        "sale_own_obligation": ("自己买卖", "转移所有权", "直接买受", "直接出售", "承担买卖合同义务"),
        "oral_contract": ("口头约定", "未签书面合同", "没有书面合同", "口头中介", "口头居间"),
        "evidence_exists": ("有聊天记录", "有交易记录", "有证据证明", "有委托凭证", "有转账记录", "有看房记录", "有带看单"),
        "standard_clause_dispute": ("格式条款", "霸王条款", "免除中介责任", "加重委托人责任", "限制主要权利", "条款无效"),
        "unreasonable_standard_clause": ("不合理免除", "不合理减轻", "免除中介责任", "减轻中介责任", "加重委托人责任", "加重责任", "限制主要权利", "排除主要权利", "显失公平"),
        "report_brokerage": ("报告中介", "指示中介", "报告订约机会", "提供交易机会"),
        "media_brokerage": ("媒介中介", "媒介服务", "撮合买卖双方", "撮合双方签约"),
        "exclusive_entrustment": ("独家委托", "独家代理", "只能通过该中介", "排他委托"),
        "non_exclusive_entrustment": ("非独家委托", "多家中介", "同时委托多家", "不是独家", "普通委托"),
        "truthful_report_dispute": ("未如实报告", "隐瞒重要事实", "故意隐瞒", "虚假信息", "虚假情况", "欺骗委托人", "房屋真实情况未告知"),
        "important_fact_hidden": ("隐瞒重要事实", "故意隐瞒", "隐瞒抵押", "隐瞒查封", "隐瞒漏水", "隐瞒凶宅", "隐瞒产权瑕疵"),
        "false_information": ("提供虚假情况", "虚假信息", "假房源", "虚假价格", "虚假承诺", "信息不实"),
        "principal_loss": ("损害委托人利益", "委托人受损", "造成损失", "损失"),
        "best_efforts_dispute": ("未尽力", "没有积极促成", "没有撮合", "服务不到位", "怠于服务", "不作为"),
        "best_efforts_done": ("积极联系", "多次沟通", "已安排带看", "已协助谈判", "已尽力促成"),
        "staff_act_dispute": ("工作人员", "业务员", "经纪人", "中介员工", "门店员工", "员工行为"),
        "staff_scope_act": ("职务行为", "以公司名义", "工作期间", "代表中介公司", "使用公司账号", "盖公司章"),
        "principal_wrong_info": ("委托人提供信息有误", "委托人信息错误", "卖方提供信息不实", "业主提供错误信息", "房源信息由委托人提供"),
        "broker_knew_wrong_info": ("中介明知", "中介应知", "知道信息有误", "应当知道信息有误", "仍继续服务"),
        "bypass_claim": ("跳单", "绕开中介", "绕过中介", "私下成交", "直接签约", "直接订立合同", "避开中介"),
        "accepted_service": ("接受中介服务", "接受服务", "看房", "带看", "咨询中介", "接受撮合"),
        "used_opportunity": ("利用中介提供的信息", "利用交易机会", "利用房源信息", "利用媒介服务", "用中介介绍的", "使用中介资源"),
        "bypassed_direct_contract": ("绕开中介直接签约", "绕过中介直接成交", "私下签约", "私下成交", "直接与对方签合同", "直接订立合同"),
        "other_broker_legitimate": ("通过其他中介", "其他中介促成", "正当途径获取相同信息", "支付了其他中介费", "正常市场价中介费"),
        "original_broker_not_cause": ("原中介未促成", "中介未促成合同", "未能促成交易", "不是原中介促成"),
        "contract_concluded": ("合同成立", "交易达成", "买卖合同已签", "租赁合同已签", "双方签约", "促成合同成立", "交易完成", "成交"),
        "contract_not_concluded": ("合同未成立", "交易未成", "没有成交", "未成交", "没有签约", "未能签约", "未促成合同"),
        "remuneration_claim": ("报酬", "中介费", "佣金", "服务费", "居间费", "要求支付中介费", "主张报酬"),
        "remuneration_agreed": ("约定中介费", "报酬有约定", "佣金约定", "按约定支付", "约定报酬"),
        "remuneration_unclear": ("未约定报酬", "报酬约定不明", "佣金不明", "中介费不明"),
        "both_parties_bear": ("双方平均负担", "买卖双方分担", "合同当事人平均负担", "双方各半"),
        "necessary_expense_claim": ("必要费用", "交通费", "通讯费", "实际支出", "支出费用", "请求费用"),
        "expense_agreed": ("约定必要费用", "约定支付费用", "费用有约定", "按约定支付必要费用"),
        "policy_failure": ("限购", "贷款政策变化", "政策原因", "政策变化", "限贷", "购房资格变化", "政策导致交易不成"),
        "termination_request": ("解除中介合同", "解除合同", "随时解除", "终止中介合同", "不再委托"),
        "paid_brokerage": ("有偿中介", "有偿合同", "约定报酬", "收取中介费", "收佣金"),
        "unpaid_brokerage": ("无偿中介", "免费中介", "无偿服务"),
        "termination_loss": ("解除造成损失", "直接损失", "可得利益损失", "损失"),
        "post_contract_obligation": ("后合同义务", "终止后", "解除后", "合同终止后", "保密义务", "协助义务", "通知义务"),
        "post_contract_breach": ("泄露信息", "拒绝协助", "拒绝通知", "违反保密", "未移交资料", "违反后合同义务"),
        "burden_proof_dispute": ("举证责任", "无法举证", "证据不足", "谁举证", "不能证明", "中介义务履行争议", "中介关系争议"),
        "broker_claim_completed": ("中介人主张已完成", "中介主张已促成", "中介主张完成义务", "中介要求证明已服务"),
        "principal_claim_not_completed": ("委托人主张未完成", "委托人说未服务", "委托人主张中介未完成义务"),
        "proof_completed": ("已完成举证", "有证据证明", "证据充分", "聊天记录证明", "带看记录证明"),
        "actual_loss": ("损失", "赔偿", "损失金额", "费用", "必要费用", "中介费", "佣金", "报酬"),
    },
)


BROKERAGE_CONFIGS: Dict[str, BrokerageConfig] = {
    BROKERAGE_CONFIG.key: BROKERAGE_CONFIG,
}


def get_brokerage_config(contract_type: str | None = None) -> BrokerageConfig:
    key = (contract_type or "brokerage").strip().lower()
    aliases = {
        "broker": "brokerage",
        "intermediary": "brokerage",
        "intermediary_contract": "brokerage",
        "brokerage_contract": "brokerage",
        "居间": "brokerage",
        "居间合同": "brokerage",
        "中介": "brokerage",
        "中介合同": "brokerage",
    }
    return BROKERAGE_CONFIGS.get(aliases.get(key, key), BROKERAGE_CONFIG)
