"""Agency-contract adjudication configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from adjudicate.lease_configs import MOUNT_POST, MOUNT_PRE, PatchMount


Terms = Tuple[str, ...]
PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class AgencyConfig:
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


AGENCY_CONFIG = AgencyConfig(
    key="agency",
    display_name="委托合同",
    fact_mapping={
        "合同主体": "委托人/受托人",
        "核心义务": "按指示处理委托事务（受托人）/ 支付报酬和费用（委托人）",
        "归责原则": "有偿=一般过失；无偿=故意或重大过失；越权=绝对责任",
        "核心争议": "事务是否妥善处理 → 是否存在过错 → 责任标准 → 赔偿多少",
    },
    reused_modules=("管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"),
    patch_mounts=(
        PatchMount("A1", "contract_type_identification", MOUNT_POST, "委托合同性质认定", "合同名称与实质内容不一致，或双方对委托、承揽、中介、行纪性质存在争议", "《民法典》第919条", "按合同实质判断：委托处理事务，承揽完成工作成果，中介报告订约机会，行纪以自己名义交易", "按实质内容认定为 [委托/承揽/中介/行纪] 合同。"),
        PatchMount("A2", "trustee_fault", MOUNT_POST, "有偿/无偿委托责任标准", "受托人处理委托事务造成损失，或受托人超越权限", "《民法典》第929条", "有偿委托按一般过错承担责任；无偿委托仅故意或重大过失担责；越权造成损失直接担责", "受托人责任标准为 [有偿一般过错/无偿故意重大过失/越权直接赔偿]。"),
        PatchMount("A3", "sub_entrustment", MOUNT_POST, "转委托责任", "受托人将委托事务转交第三人处理", "《民法典》第923条", "经同意或追认的，受托人仅对第三人的选任和指示负责；未经同意的，受托人对第三人行为负责；紧急情形除外", "转委托 [有效/无效]，受托人承担 [选任指示责任/全部责任]。"),
        PatchMount("A4", "trustee_obligation", MOUNT_POST, "自己代理与双方代理", "受托人以委托人名义与自己交易，或同时代理交易双方", "《民法典》第168条", "未经同意或追认不得自己代理、双方代理；交易显失公平的可依法否定效力", "自己代理/双方代理 [有效/无效]，受托人 [承担/不承担] 赔偿责任。"),
        PatchMount("A5", "undisclosed_agency", MOUNT_POST, "委托人介入权", "受托人以自己名义与第三人订约，第三人原因导致不履行", "《民法典》第926条", "受托人披露第三人后，委托人可以介入行使受托人对第三人的权利，但第三人如知道委托人就不会订约的除外", "委托人介入权 [成立/不成立]，可向第三人主张权利。"),
        PatchMount("A6", "undisclosed_agency", MOUNT_POST, "第三人选择权", "受托人以自己名义订约，委托人原因导致不履行", "《民法典》第926条", "受托人披露委托人后，第三人可选择受托人或委托人主张权利，选定后不得变更", "第三人选择权成立，可选择 [委托人/受托人] 主张权利。"),
        PatchMount("A7", "arbitrary_termination", MOUNT_POST, "任意解除权及赔偿范围", "委托人或受托人任意解除委托合同", "《民法典》第933条", "可随时解除；有偿委托因不可归责于解除方造成损失的赔偿直接损失和可得利益，无偿委托赔偿直接损失", "委托合同已解除，解除方赔偿范围为 [直接损失/直接损失和可得利益]。"),
        PatchMount("A8", "principal_obligation", MOUNT_POST, "委托人另行委托", "委托人将同一事务另行委托第三人处理", "《民法典》第931条", "另行委托经受托人同意或不影响原委托的，受托人仍可请求费用和报酬；造成损失的按过错赔偿", "委托人另行委托 [有效/构成违约]，损失由 [委托人/受托人] 承担。"),
        PatchMount("A9", "trustee_obligation", MOUNT_POST, "共同受托人连带责任", "两个以上受托人共同处理委托事务", "《民法典》第932条", "共同受托人对委托人承担连带责任", "共同受托人对委托人承担连带责任。"),
        PatchMount("A10", "contract_termination", MOUNT_POST, "终止后的继续处理义务", "委托人死亡、终止或受托人死亡、丧失行为能力、终止后，立即停止会损害委托人利益", "《民法典》第934条、第935条", "原则上终止；但另有约定、事务性质不宜终止或停止会损害委托人利益的，应继续处理至继承人等接手", "委托合同 [终止/继续处理至接手]。"),
        PatchMount("A11", "trustee_obligation", MOUNT_POST, "受托人指示遵守义务", "受托人变更委托人指示或未按指示处理事务", "《民法典》第922条", "应按指示处理；需变更指示的应经同意，情况紧急难以联系的应妥善处理并及时报告", "受托人违反指示义务，应赔偿因此造成的损失。"),
        PatchMount("A12", "trustee_obligation", MOUNT_POST, "受托人报告义务", "受托人未报告或虚假报告委托事务处理情况", "《民法典》第924条", "受托人应按委托人要求报告事务处理情况，终止时报告结果", "受托人违反报告义务，应承担相应责任。"),
        PatchMount("A13", "trustee_obligation", MOUNT_POST, "取得财产转交义务", "受托人处理委托事务取得财产但未转交委托人", "《民法典》第927条", "受托人应将处理委托事务取得的财产转交委托人", "受托人应返还取得财产并赔偿损失。"),
        PatchMount("A14", "contract_effect", MOUNT_POST, "格式条款效力审查", "委托合同中存在排除主要义务、免除重大过错责任或不合理加重对方责任的格式条款", "《民法典》第496条、第497条", "未提示说明或不合理免除责任、加重对方责任、排除主要权利的格式条款不发生效力", "格式条款 [有效/无效]。"),
        PatchMount("A15", "principal_obligation", MOUNT_POST, "不可归责受托人的报酬请求", "委托事务不能完成且不可归责于受托人，受托人请求相应报酬", "《民法典》第928条", "因不可归责受托人的事由不能完成事务的，委托人应支付相应报酬；另有约定除外", "委托人应向受托人支付相应报酬。"),
        PatchMount("A16", "defense_continuation", MOUNT_POST, "介入权/选择权后的抗辩延续", "委托人介入权或第三人选择权行使后，相对方主张原合同抗辩", "《民法典》第926条", "相对方对受托人享有的抗辩，可以向介入后的委托人或被选择方继续主张", "原合同抗辩继续存在，不因介入权或选择权行使而消灭。"),
    ),
    terms={
        "jurisdiction_question": ("哪里起诉", "去哪里起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
        "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "告对人"),
        "agency_contract": ("委托合同", "委托人", "受托人", "代理处理", "代办", "代为处理", "委托事务"),
        "contract_invalid": ("合同无效", "无效合同", "违法无效", "合同不成立"),
        "contract_date": ("合同签订", "签订合同", "委托发生", "受托处理", "应履行", "解除合同"),
        "third_party_tort": ("路人侵权", "第三人侵权", "外人造成损害", "他人侵权"),
        "nature_dispute": ("合同性质争议", "到底是什么合同", "名为", "实为", "定性争议", "性质不一致"),
        "process_affairs": ("处理事务", "办理事务", "代为处理", "代办", "管理事务", "代理事项"),
        "complete_work": ("完成工作成果", "交付工作成果", "加工", "定作", "修理", "承揽"),
        "intermediary_service": ("报告订约机会", "提供媒介服务", "撮合交易", "中介合同", "居间"),
        "commission_trade": ("以自己名义买卖", "以自己名义交易", "行纪", "代销", "寄售"),
        "paid_agency": ("有偿委托", "约定报酬", "支付报酬", "服务费", "代理费"),
        "unpaid_agency": ("无偿委托", "免费帮忙", "不收报酬", "无报酬", "未约定报酬"),
        "general_mandate": ("概括委托", "一般委托", "全权处理", "处理所有事务"),
        "special_mandate": ("特别委托", "专项委托", "只委托", "仅限", "具体事项"),
        "expense_advance": ("预付费用", "垫付费用", "必要费用", "交通费", "材料费", "手续费"),
        "nonnecessary_expense": ("非必要费用", "不合理费用", "擅自扩大费用"),
        "remuneration_unpaid": ("未支付报酬", "拖欠报酬", "不给代理费", "未付服务费"),
        "matter_completed": ("事务完成", "已经完成委托事项", "办成了", "已办妥"),
        "matter_unfinished_no_trustee_fault": ("不可归责于受托人", "不是受托人原因", "因委托人原因未完成", "客观原因不能完成"),
        "matter_unfinished_trustee_fault": ("受托人原因未完成", "受托人过错未完成", "受托人未办成"),
        "trustee_loss_no_fault": ("受托人无过错受损", "处理事务时受托人受损", "受托人为委托事务遭受损失"),
        "instruction_changed_without_consent": ("未按指示", "擅自变更指示", "违反委托人指示", "没有按要求办理"),
        "emergency_handling": ("情况紧急", "紧急情况", "来不及联系", "难以联系委托人"),
        "timely_report": ("及时报告", "事后报告", "马上告知", "已报告委托人"),
        "sub_entrustment": ("转委托", "转托第三人", "交给第三人办理", "委托别人处理"),
        "principal_consent": ("委托人同意", "经委托人同意", "授权转委托", "同意转委托"),
        "ratification": ("事后追认", "委托人追认", "认可转委托"),
        "emergency_sub_entrustment": ("紧急转委托", "情况紧急转委托", "为保护委托人利益转委托"),
        "selection_instruction_fault": ("选任不当", "指示错误", "第三人不合适", "监督不当"),
        "self_agency": ("自己代理", "与自己交易", "受托人与自己交易"),
        "both_side_agency": ("双方代理", "同时代理双方", "同时代理交易双方"),
        "consent_or_ratification": ("同意或追认", "明确同意", "事后追认", "双方认可"),
        "unfair_price": ("显失公平", "价格明显不公", "损害委托人利益"),
        "report_failure": ("未报告", "拒绝报告", "不汇报", "没有报告处理情况"),
        "false_report": ("虚假报告", "隐瞒情况", "报告不实"),
        "property_obtained": ("取得财产", "收到款项", "收回款项", "取得货物", "取得利益"),
        "property_not_transferred": ("未转交", "拒不转交", "没有交给委托人", "占有不还"),
        "trustee_loss": ("造成损失", "委托事务损失", "事务处理造成损失", "办事造成损害"),
        "trustee_fault": ("受托人过错", "疏忽", "一般过失", "处理不当", "未尽注意义务"),
        "trustee_no_fault": ("受托人无过错", "没有过错", "尽到注意义务"),
        "trustee_intent_gross": ("故意", "重大过失", "故意或重大过失", "严重疏忽"),
        "trustee_proves_no_intent_gross": ("能证明无故意或重大过失", "不存在故意或重大过失", "仅一般过失"),
        "over_authority": ("越权", "超越权限", "超出授权范围", "无权代理"),
        "actual_loss": ("实际损失", "损失", "赔偿", "费用", "报酬", "款项"),
        "expected_profit": ("可得利益", "预期利益", "利润损失"),
        "third_party_cause": ("第三人原因", "第三方原因", "第三人违约"),
        "principal_fault": ("委托人原因", "委托人过错", "委托人提供资料错误", "委托人不配合"),
        "force_majeure": ("不可抗力", "自然灾害", "政府原因"),
        "trustee_own_name": ("以受托人自己名义", "以自己名义", "受托人名义签约"),
        "third_party_knows_agency": ("第三人知道委托关系", "第三人知道受托人与委托人关系", "明知代理关系"),
        "third_party_unknown_agency": ("第三人不知道委托关系", "第三人不知委托人", "隐名委托", "间接代理"),
        "third_party_fault_nonperformance": ("第三人不履行", "第三人违约", "第三人拒绝履行"),
        "principal_fault_nonperformance": ("委托人不履行", "委托人违约", "委托人原因导致不能履行"),
        "trustee_disclosed_third_party": ("披露第三人", "告知第三人身份"),
        "trustee_disclosed_principal": ("披露委托人", "告知委托人身份"),
        "third_party_would_not_contract": ("知道委托人就不会订约", "若知委托人不会签约"),
        "third_party_selected_principal": ("选择委托人", "向委托人主张"),
        "third_party_selected_trustee": ("选择受托人", "向受托人主张"),
        "defense_continuation": ("继续主张抗辩", "原有抗辩", "抗辩权继续", "抵销抗辩"),
        "arbitrary_termination": ("任意解除", "随时解除", "单方解除委托", "无理由解除委托"),
        "principal_terminates": ("委托人解除", "委托人单方解除"),
        "trustee_terminates": ("受托人解除", "受托人单方解除"),
        "termination_loss": ("解除造成损失", "因解除受损", "解除损失"),
        "not_attributable_termination": ("不可归责于解除方", "不是解除方原因"),
        "direct_loss": ("直接损失", "实际支出", "已发生费用"),
        "liquidated_damage": ("违约金", "约定违约金"),
        "separate_entrustment": ("另行委托", "又委托他人", "委托第三人同时处理", "另找人处理"),
        "trustee_consented_separate": ("受托人同意另行委托", "受托人知情同意"),
        "separate_caused_loss": ("另行委托造成损失", "重复委托造成损失"),
        "joint_trustees": ("共同受托人", "两个受托人", "多名受托人", "共同处理委托事务"),
        "principal_dead_or_terminated": ("委托人死亡", "委托人终止", "委托人去世", "委托人破产终止"),
        "trustee_dead_or_incapable": ("受托人死亡", "受托人丧失民事行为能力", "受托人终止", "受托人去世"),
        "no_termination_agreement": ("没有终止约定", "未约定不终止", "无继续约定"),
        "continuing_needed": ("停止会损害委托人利益", "继续处理才不损害利益", "必须继续处理", "等待继承人接手"),
        "format_clause": ("格式条款", "预先拟定", "不能协商", "模板合同", "霸王条款"),
        "prompt_explain": ("已提示说明", "明确提示", "特别说明"),
        "unreasonable_clause": ("免除受托人重大过失责任", "排除主要权利", "不合理加重责任", "免除主要义务"),
    },
)


AGENCY_CONFIGS: Dict[str, AgencyConfig] = {AGENCY_CONFIG.key: AGENCY_CONFIG}


def get_agency_config(contract_type: str | None = None) -> AgencyConfig:
    key = (contract_type or "agency").strip().lower()
    aliases = {
        "entrustment": "agency",
        "mandate": "agency",
        "commission": "agency",
        "agent": "agency",
        "代理": "agency",
        "委托": "agency",
        "委托合同": "agency",
    }
    return AGENCY_CONFIGS.get(aliases.get(key, key), AGENCY_CONFIG)
