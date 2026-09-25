"""Work-contract adjudication configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from adjudicate.lease_configs import MOUNT_POST, PatchMount


Terms = Tuple[str, ...]
PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class WorkContractConfig:
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


WORK_CONTRACT_CONFIG = WorkContractConfig(
    key="work_contract",
    display_name="承揽合同",
    fact_mapping={
        "合同主体": "承揽人/定作人",
        "核心义务": "完成工作、交付符合质量要求的工作成果",
        "归责原则": "过错责任（承揽人对质量瑕疵承担责任）",
        "核心争议": "工作成果是否符合质量要求 → 瑕疵程度 → 定作人选择何种救济方式",
    },
    reused_modules=("管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"),
    patch_mounts=(
        PatchMount(
            "C7",
            "contract_type_identification",
            MOUNT_POST,
            "承揽/买卖合同定性争议",
            "合同名称与实质内容不一致，双方对合同性质存在争议",
            "《民法典》第770条及合同性质实质审查规则",
            "根据合同实质内容认定性质；买卖以转移所有权为目的，承揽以完成特定工作为目的",
            "根据合同实质内容认定为[承揽合同/买卖合同]。",
        ),
        PatchMount(
            "C6",
            "personal_completion",
            MOUNT_POST,
            "转包/分包的效力",
            "承揽人将工作交由第三人完成",
            "《民法典》第772条、第773条",
            "主要工作转包须经定作人同意；辅助工作可由第三人完成，但承揽人仍对成果负责",
            "转包[有效/无效]，承揽人[承担/不承担]责任。",
        ),
        PatchMount(
            "C9",
            "personal_completion",
            MOUNT_POST,
            "违法分包/转包",
            "承揽人将全部工作转包给第三人，或将主要工作肢解后分别转包",
            "《民法典》第772条",
            "未经定作人同意全部转包或肢解转包的，定作人可解除合同；违法转包导致质量问题的，承揽人承担全部责任",
            "未经同意违法转包，定作人可解除合同；质量问题由承揽人承担全部责任。",
        ),
        PatchMount(
            "C4",
            "customer_assistance",
            MOUNT_POST,
            "定作人提供的材料瑕疵",
            "定作人提供的材料不符合约定",
            "《民法典》第775条",
            "承揽人应及时检验并通知；未检验或未通知的承担相应责任",
            "材料瑕疵责任由[定作人/承揽人]承担。",
        ),
        PatchMount(
            "C5",
            "contractor_lien",
            MOUNT_POST,
            "承揽人保管义务",
            "定作人提供的材料或已完成的工作成果在承揽人保管期间毁损、灭失",
            "《民法典》第784条",
            "承揽人已尽合理保管义务的不承担责任；保管不善的承担赔偿责任",
            "承揽人保管[尽到/未尽到]妥善保管义务，[不承担/承担]赔偿责任。",
        ),
        PatchMount(
            "C3",
            "delivery_status",
            MOUNT_POST,
            "定作人任意解除权",
            "定作人在承揽人完成工作前主张解除合同",
            "《民法典》第787条",
            "定作人完成前可以随时解除合同，但应赔偿承揽人已投入成本、人工费、合理利润等损失",
            "定作人任意解除权[成立/不成立]，解除有效，应赔偿承揽人损失[具体金额]。",
        ),
        PatchMount(
            "C8",
            "delivery_status",
            MOUNT_POST,
            "定作人任意解除权的行使边界",
            "定作人主张任意解除权，但承揽人主张工作已完成、接近完成或已投入绝大部分成本",
            "《民法典》第787条及诚信原则",
            "任意解除权须在工作完成前行使；工作接近完成或已投入绝大部分成本的，解除权行使可能受诚信原则限制",
            "定作人任意解除权行使可能受限，仍应赔偿承揽人实际损失。",
        ),
        PatchMount(
            "C1",
            "quality_requirement",
            MOUNT_POST,
            "质量瑕疵认定标准",
            "定作人主张工作成果存在质量瑕疵",
            "《民法典》第781条",
            "质量标准按合同约定、样品图纸、行业标准、通常标准顺序认定；明知瑕疵仍接受的视为认可",
            "工作成果质量[符合/不符合][约定标准]，瑕疵[成立/不成立]。",
        ),
        PatchMount(
            "C2",
            "remedy_selection",
            MOUNT_POST,
            "定作人救济方式的选择权",
            "工作成果存在质量瑕疵",
            "《民法典》第781条",
            "定作人可合理选择修理、重作、减少报酬、赔偿损失等责任方式",
            "定作人合理选择[修理/重作/减少报酬/赔偿损失]，承揽人应承担[具体责任]。",
        ),
    ),
    terms={
        "jurisdiction_question": ("哪里起诉", "去哪起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
        "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "告对人"),
        "work_contract": ("承揽合同", "加工合同", "定作合同", "修理合同", "复制合同", "测试合同", "检验合同", "承揽人", "定作人", "工作成果", "加工费", "报酬"),
        "contract_nature_dispute": ("合同性质争议", "定性争议", "到底是买卖还是承揽", "名为买卖实为承揽", "名为承揽实为买卖", "合同名称与实质不一致"),
        "named_sale_contract": ("买卖合同", "销售合同", "采购合同", "购销合同"),
        "named_work_contract": ("承揽合同", "加工合同", "定作合同", "修理合同"),
        "customized_order": ("按定作人要求定制", "按客户要求定制", "定制", "非标准化", "个性化制作", "专门制作"),
        "specific_work": ("完成特定工作", "特定工作", "加工制作", "现场施工", "修理", "测试", "检验", "按图施工"),
        "standard_product": ("标准化产品", "成品", "通用产品", "现货", "批量产品", "规格产品"),
        "ownership_transfer": ("转移所有权", "交付所有权", "买断", "购买产品", "交付产品"),
        "contract_invalid": ("合同无效", "无效合同", "违法无效", "合同未成立"),
        "third_party_tort": ("路人侵权", "第三方侵权", "外人破坏", "陌生人损坏", "他人故意损坏"),
        "completion_date": ("交付", "应交付", "完工", "验收", "完成"),
        "main_work_subcontract": ("转包主要工作", "主要工作交给第三人", "主要工作分包", "擅自转包", "核心工作转包", "主体工作转包"),
        "total_subcontract": ("全部工作转包", "全部转包", "整体转包", "整项工作交给第三人", "全部交由第三人完成"),
        "disassembled_subcontract": ("肢解转包", "拆分后转包", "肢解后分别转包", "拆成多段转包", "拆分给多个第三人"),
        "auxiliary_subcontract": ("辅助工作转包", "辅助工作分包", "辅助部分交给第三人", "辅助工作由第三人完成"),
        "customer_consent": ("经定作人同意", "定作人同意", "已同意", "事先同意", "书面同意"),
        "customer_assistance_missing": ("不履行协助义务", "未履行协助义务", "未提供图纸", "未提供资料", "未提供场地", "不配合", "拒绝确认"),
        "urged_assistance": ("催告", "通知履行", "要求协助", "限期履行", "合理期限"),
        "assistance_overdue": ("逾期未履行", "逾期仍不履行", "仍不配合", "超过合理期限", "到期仍未提供", "逾期不履行"),
        "customer_change_request": ("中途变更要求", "中途变更", "变更设计", "修改图纸", "改规格", "改尺寸", "增加要求", "改派工作"),
        "workload_increased": ("工作量增加", "成本增加", "增加工时", "返工", "材料浪费", "增加报酬"),
        "contractor_loss": ("损失", "材料费", "人工费", "返工费", "合理利润", "追加费用", "承揽人损失"),
        "unpaid_remuneration": ("未支付报酬", "拖欠报酬", "拒付报酬", "少付报酬", "欠加工费", "欠报酬", "未付材料费", "欠材料费"),
        "lien": ("留置", "拒绝交付", "扣留成果", "留置权", "扣住工作成果"),
        "improper_lien": ("超额留置", "不当留置", "留置价值远超", "违法扣留", "扣留全部成果"),
        "customer_material_defect": ("定作人提供材料有瑕疵", "定作人材料有瑕疵", "材料不合格", "材料规格不符", "来料有瑕疵", "来料不合格"),
        "contractor_inspected_notice": ("及时检验并通知", "已检验并通知", "及时检验", "及时通知", "通知更换", "通知补齐"),
        "contractor_no_inspection_notice": ("未检验", "未及时检验", "未通知", "未及时通知", "没有通知"),
        "defect_caused_by_customer_material": ("因材料瑕疵导致", "因定作人材料导致", "由来料问题造成", "材料问题造成质量瑕疵"),
        "custody_damage": ("保管期间损坏", "保管期间灭失", "材料丢失", "成果丢失", "保管期间受潮", "保管期间毁损"),
        "proper_custody": ("妥善保管", "已合理保管", "已尽保管义务", "不可抗力"),
        "improper_custody": ("保管不善", "存放不当", "未防护", "未看管", "未妥善保管"),
        "result_delivered": ("已交付", "交付工作成果", "已经交付", "已完成并交付", "已验收", "已交货", "成果交付"),
        "not_delivered": ("未交付", "尚未交付", "未完成", "尚未完成", "完成前", "工作完成前"),
        "customer_termination": ("定作人解除", "定作人要求解除", "随时解除", "终止合同", "取消订单", "要求退单"),
        "termination_after_completion": ("完成后解除", "已完成后解除", "交付后解除", "验收后解除"),
        "near_completion": ("接近完成", "快完成", "基本完成", "即将完工", "临近完工"),
        "substantial_cost_invested": ("投入绝大部分成本", "已投入大量成本", "成本大部分已投入", "已经完成大部分工作", "大部分工作已完成"),
        "delay_delivery": ("延迟交付", "迟延交付", "逾期交付", "未按期交付", "拖延完工", "逾期完工"),
        "quality_defect": ("质量瑕疵", "质量不合格", "不符合质量要求", "质量问题", "瑕疵", "不合格", "装修不合格", "定作物有瑕疵"),
        "quality_conform": ("符合质量要求", "质量合格", "验收合格", "质量达标", "符合约定"),
        "contract_quality_standard": ("合同约定质量", "质量标准", "验收标准", "按约定", "符合合同标准"),
        "sample_drawing": ("样品", "图纸", "设计图", "样板", "样稿"),
        "industry_standard": ("行业标准", "国家标准", "通常标准", "通用标准"),
        "customer_knew_and_accepted": ("明知瑕疵仍接收", "知道瑕疵仍验收", "明知质量问题仍接受", "未提出异议", "接收成果未异议"),
        "minor_defect": ("轻微", "局部", "可修复", "小瑕疵", "不严重"),
        "serious_defect": ("严重", "无法修复", "不能修复", "修复成本过高", "大面积不合格"),
        "worthless_defect": ("完全无价值", "无法使用", "根本不能用", "完全不符合合同目的", "作废"),
        "repair_requested": ("要求修理", "要求修复", "修理", "修复", "维修", "修补"),
        "remake_requested": ("重作", "重新制作", "重新施工", "返工"),
        "reduce_pay_requested": ("减少报酬", "减价", "扣减报酬", "少付报酬", "扣款"),
        "compensation_requested": ("赔偿损失", "索赔", "赔钱", "赔偿"),
        "contractor_refuses_repair": ("拒绝修理", "拒绝修复", "拒绝重作", "不配合修复", "不愿返工"),
        "remuneration_amount": ("报酬", "价款", "加工费", "费用", "工钱"),
        "actual_loss": ("损失", "维修费", "重作费", "误工损失", "材料费", "实际损失"),
        "delay_loss": ("延迟损失", "迟延损失", "停工损失", "违约损失", "逾期损失"),
    },
)


WORK_CONTRACT_CONFIGS: Dict[str, WorkContractConfig] = {
    WORK_CONTRACT_CONFIG.key: WORK_CONTRACT_CONFIG,
}


def get_work_contract_config(contract_type: str | None = None) -> WorkContractConfig:
    key = (contract_type or "work_contract").strip().lower()
    aliases = {
        "contracting": "work_contract",
        "work": "work_contract",
        "service_work": "work_contract",
        "承揽": "work_contract",
        "承揽合同": "work_contract",
        "加工": "work_contract",
        "定作": "work_contract",
        "修理": "work_contract",
    }
    return WORK_CONTRACT_CONFIGS.get(aliases.get(key, key), WORK_CONTRACT_CONFIG)
