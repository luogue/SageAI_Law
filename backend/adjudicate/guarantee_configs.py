"""Guarantee-contract adjudication configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from adjudicate.lease_configs import MOUNT_POST, PatchMount


Terms = Tuple[str, ...]
PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class GuaranteeConfig:
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


GUARANTEE_CONFIG = GuaranteeConfig(
    key="guarantee",
    display_name="保证合同",
    fact_mapping={
        "合同主体": "债权人/保证人/债务人",
        "核心义务": "债务人不履行债务时，保证人代为履行或承担责任",
        "归责原则": "严格责任（保证人按约定承担保证责任）",
        "核心争议": "保证方式（一般/连带）→ 保证期间是否已过 → 债权人是否在保证期间内行使权利 → 主合同变更是否影响保证责任",
    },
    reused_modules=("管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"),
    patch_mounts=(
        PatchMount("G1", "guarantee_type", MOUNT_POST, "保证方式约定不明推定", "保证合同对保证方式没有约定或约定不明确", "《民法典》第686条", "没有约定或约定不明的，按一般保证承担保证责任", "保证方式约定不明，依法推定为一般保证。一般保证人享有先诉抗辩权，债权人须先向债务人主张权利。"),
        PatchMount("G2", "guarantee_period", MOUNT_POST, "保证期间确定规则", "需要确定保证期间", "《民法典》第692条", "有效约定按约定；没有约定、约定不明或约定早于/同于主债务期限的，适用六个月法定保证期间，且不中止不中断不延长", "保证期间为 [具体起止日期]，共计 [X] 个月。保证期间不发生中止、中断和延长。"),
        PatchMount("G3", "prior_lawsuit_defense", MOUNT_POST, "一般保证人先诉抗辩权", "一般保证人主张不承担保证责任", "《民法典》第687条", "一般保证人在债务人财产依法强制执行仍不能履行前，有权拒绝承担责任；法定例外或书面放弃除外", "一般保证人享有先诉抗辩权，债权人应先就债务人财产强制执行。如存在例外情形，先诉抗辩权消灭。"),
        PatchMount("G4", "exercise_within_period", MOUNT_POST, "保证期间内行使权利认定", "债权人主张已在保证期间内行使权利", "《民法典》第693条", "一般保证须在保证期间内起诉或仲裁债务人；连带保证须在保证期间内请求保证人承担责任", "债权人 [已/未] 在保证期间内依法行使权利，保证责任 [不消灭/消灭]。"),
        PatchMount("G5", "main_contract_change", MOUNT_POST, "主合同变更未经保证人同意", "主合同内容变更且未经保证人书面同意", "《民法典》第695条", "减轻债务的保证人仍对变更后债务担责；加重债务的保证人对加重部分免责", "主合同变更未经保证人书面同意，保证人对加重部分 [承担/不承担] 保证责任。"),
        PatchMount("G6", "assignment_transfer", MOUNT_POST, "债权转让与债务转移影响", "发生债权转让或债务转移", "《民法典》第696条、第697条", "债权转让未通知保证人对保证人不发生效力；债务转移未经保证人书面同意的，保证人对转移债务免责", "债权转让/债务转移 [已/未] 通知保证人/[经/未经] 保证人书面同意，保证责任 [不变/消灭/部分消灭]。"),
        PatchMount("G7", "joint_guarantee", MOUNT_POST, "共同保证责任承担", "同一债务有两个以上保证人", "《民法典》第699条、担保制度解释第29条", "有份额按份额承担；无份额的债权人可请求任一保证人在保证范围内承担责任；对部分保证人行权不及于其他保证人", "共同保证，[有/无] 约定保证份额，保证人 [按份额/连带] 承担保证责任。"),
        PatchMount("G8", "maximum_guarantee", MOUNT_POST, "最高额保证特殊规则", "保证合同为最高额保证", "《民法典》第690条、担保制度解释第30条", "保证期间无约定或约定不明的，自最高额保证终止之日或终止通知到达之日起六个月", "最高额保证，保证期间为 [最高额保证终止之日/收到终止通知之日起6个月]。"),
        PatchMount("G9", "contract_effect", MOUNT_POST, "保证合同无效后责任承担", "保证合同被确认无效", "《民法典》第682条、担保制度解释第32条、第33条", "保证合同无效后，各方按过错承担责任；一般保证人仍享有先诉抗辩权；未在保证期间内行权的可不承担赔偿责任", "保证合同无效，各方按过错承担责任。一般保证人仍享有先诉抗辩权。"),
        PatchMount("G10", "recourse", MOUNT_POST, "保证人追偿权与代位权", "保证人已承担保证责任", "《民法典》第700条", "保证人可在承担责任范围内向债务人追偿，并代位享有债权人对债务人的权利，但不得损害债权人利益", "保证人已承担保证责任 [金额] 元，有权向债务人追偿，并代位行使债权人对债务人的权利。"),
        PatchMount("G11", "guarantor_capacity", MOUNT_POST, "公司对外担保效力", "保证人为公司", "担保制度解释第7条", "法定代表人越权担保时，相对人善意并合理审查公司决议的，担保对公司有效；非善意的，对公司不发生效力", "公司对外担保，相对人 [善意/非善意]，担保合同 [对公司发生效力/对公司不发生效力]。"),
        PatchMount("G12", "guarantor_capacity", MOUNT_POST, "保证人主体资格特殊规定", "保证人为机关法人、公益非营利法人、居民委员会、村民委员会等特殊主体", "《民法典》第683条", "机关法人、公益非营利法人或非法人组织、居委会村委会原则上不得为保证人", "保证人 [具备/不具备] 保证人资格，保证合同 [有效/无效]。"),
        PatchMount("G13", "waiver_prior_lawsuit", MOUNT_POST, "放弃先诉抗辩权效力", "保证人书面表示放弃先诉抗辩权", "《民法典》第687条第2款第4项", "一般保证人书面放弃先诉抗辩权的，债权人可直接向保证人主张权利", "保证人 [已/未] 书面放弃先诉抗辩权，债权人 [可以/不可以] 直接向保证人主张权利。"),
        PatchMount("G14", "post_period_signature", MOUNT_POST, "保证期间届满后签字效力", "保证期间已过，保证人在催收通知上签字", "担保制度解释第34条", "保证责任消灭后仅在催收通知上签字不恢复责任；有新保证合同证据的除外", "保证期间已过，保证人签字 [不构成/构成] 新的保证合同，保证责任 [不恢复/按新合同处理]。"),
        PatchMount("G15", "main_debt_limitation", MOUNT_POST, "主债务诉讼时效届满影响", "主债务诉讼时效期间已届满", "担保制度解释第35条", "保证人知道或应当知道主债权时效届满仍提供保证的，不得以时效届满拒责；不知情的可抗辩", "保证人 [知道/不知道] 主债务诉讼时效已届满，[不得/可以] 以时效届满为由拒绝承担保证责任。"),
    ),
    terms={
        "jurisdiction_question": ("哪里起诉", "去哪里起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
        "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "告对人"),
        "guarantee_contract": ("保证合同", "保证人", "担保人", "保证担保", "担保合同", "保证条款"),
        "contract_date": ("签订保证合同", "保证合同签订", "主债务到期", "保证期间", "催收", "请求保证人", "起诉"),
        "third_party_tort": ("第三人侵权", "路人侵权", "外人造成损害", "他人侵权"),
        "main_contract_invalid": ("主合同无效", "主债权债务合同无效", "主债务合同无效"),
        "guarantee_invalid": ("保证合同无效", "担保合同无效", "保证无效"),
        "independent_guarantee_clause": ("担保独立", "保证合同效力独立", "主合同无效仍承担保证责任", "独立担保条款"),
        "state_org_guarantor": ("机关法人保证", "政府机关担保", "机关法人担保"),
        "public_nonprofit_guarantor": ("公益非营利法人担保", "学校担保", "医院担保", "公益组织担保", "村委会担保", "居委会担保"),
        "company_guarantor": ("公司担保", "公司作为保证人", "公司对外担保", "法定代表人担保"),
        "company_resolution": ("董事会决议", "股东会决议", "股东大会决议", "公司决议"),
        "creditor_good_faith": ("相对人善意", "债权人善意", "合理审查决议", "已审查公司决议"),
        "creditor_bad_faith": ("相对人非善意", "未审查决议", "明知越权", "应知越权"),
        "written_guarantee": ("书面保证合同", "书面担保", "保证条款", "单方书面保证", "签字担保"),
        "main_debt_exists": ("主债权存在", "债务真实存在", "主债务真实"),
        "guarantee_scope_agreed": ("约定保证范围", "保证范围约定", "仅保证本金", "包括利息违约金费用"),
        "unclear_guarantee_type": ("未约定保证方式", "保证方式不明", "约定不明确", "只写担保人", "只写保证人"),
        "general_guarantee": ("一般保证", "债务人不能履行时由保证人承担", "债务人无力偿还时保证人承担", "先由债务人承担"),
        "joint_guarantee_type": ("连带责任保证", "连带保证", "保证人与债务人承担连带责任", "连带责任"),
        "guarantee_period_agreed": ("约定保证期间", "保证期间为", "担保期限为"),
        "guarantee_period_unclear": ("未约定保证期间", "保证期间不明", "约定不明", "直至本息还清", "保证至还清为止"),
        "period_same_or_earlier": ("保证期间早于主债务履行期限", "保证期间与主债务同时届满", "与债务到期同时届满"),
        "main_debt_due_unclear": ("主债务履行期限不明", "还款期限不明", "债务到期不明"),
        "within_period_action": ("保证期间内", "担保期限内", "期间内主张", "期间内起诉", "期间内请求"),
        "action_against_debtor": ("起诉债务人", "对债务人提起诉讼", "申请仲裁债务人", "仲裁债务人"),
        "action_against_guarantor": ("请求保证人承担责任", "向保证人催收", "起诉保证人", "要求保证人还款"),
        "period_expired": ("保证期间已过", "超过保证期间", "担保期限已过", "保证责任消灭"),
        "only_sue_general_guarantor": ("仅起诉一般保证人", "只告一般保证人", "未起诉债务人只起诉保证人"),
        "debtor_enforced_unsatisfied": ("强制执行仍不能履行", "执行债务人财产仍不足", "执行终结未清偿"),
        "debtor_missing_no_property": ("债务人下落不明且无财产", "债务人失踪无财产"),
        "debtor_bankrupt": ("债务人破产", "受理债务人破产案件"),
        "debtor_insolvent": ("债务人资不抵债", "财产不足以清偿", "丧失履行能力"),
        "waived_prior_lawsuit": ("书面放弃先诉抗辩权", "放弃先诉抗辩权", "保证人放弃先诉抗辩"),
        "main_contract_changed": ("主合同变更", "变更主合同", "债务变更", "展期加息", "变更债务"),
        "guarantor_written_consent": ("保证人书面同意", "经保证人书面同意", "保证人同意变更"),
        "debt_aggravated": ("加重债务", "增加本金", "提高利率", "加重负担", "延长债务加重"),
        "debt_reduced": ("减轻债务", "减少本金", "降低利率", "减轻负担"),
        "credit_assignment": ("债权转让", "转让债权", "债权让与"),
        "assignment_notified": ("通知保证人", "已通知保证人", "告知保证人"),
        "assignment_prohibited": ("禁止债权转让", "不得转让债权"),
        "debt_transfer": ("债务转移", "债务转让", "转移债务"),
        "third_party_debt_join": ("第三人加入债务", "债务加入"),
        "multiple_guarantors": ("两个以上保证人", "多个保证人", "共同保证", "共同担保"),
        "guarantee_share_agreed": ("约定保证份额", "按份额承担", "保证份额"),
        "maximum_guarantee": ("最高额保证", "最高额担保", "最高债权额"),
        "maximum_period_unclear": ("最高额保证期间不明", "最高额保证未约定期间", "最高额担保期间不明"),
        "guarantee_terminated": ("最高额保证终止", "终止最高额保证", "收到终止通知"),
        "guarantor_paid": ("保证人已承担保证责任", "保证人代偿", "保证人已经还款", "保证人履行保证责任"),
        "paid_amount": ("代偿", "承担保证责任", "已经还款", "支付"),
        "recourse_claim": ("追偿", "向债务人追偿", "代位权", "代位行使"),
        "post_period_signature": ("保证期间已过后签字", "保证期间届满后签字", "催收通知上签字", "催收函签字"),
        "new_guarantee_contract": ("新的保证合同", "重新提供保证", "重新签订保证合同"),
        "main_debt_limitation_expired": ("主债务诉讼时效届满", "主债权诉讼时效已过", "主债务时效已过"),
        "guarantor_knows_limitation": ("保证人知道时效届满", "明知诉讼时效已过", "应当知道时效届满"),
        "guarantor_not_knows_limitation": ("保证人不知道时效届满", "不知诉讼时效已过"),
        "debtor_defense": ("债务人抗辩", "主张债务人抗辩", "债务人对债权人的抗辩"),
        "setoff_or_revocation": ("抵销权", "撤销权", "债务人享有抵销", "债务人享有撤销"),
        "actual_loss": ("损失", "赔偿", "责任金额"),
    },
)


GUARANTEE_CONFIGS: Dict[str, GuaranteeConfig] = {GUARANTEE_CONFIG.key: GUARANTEE_CONFIG}


def get_guarantee_config(contract_type: str | None = None) -> GuaranteeConfig:
    key = (contract_type or "guarantee").strip().lower()
    aliases = {
        "surety": "guarantee",
        "suretyship": "guarantee",
        "担保": "guarantee",
        "保证": "guarantee",
        "保证合同": "guarantee",
        "担保合同": "guarantee",
    }
    return GUARANTEE_CONFIGS.get(aliases.get(key, key), GUARANTEE_CONFIG)
