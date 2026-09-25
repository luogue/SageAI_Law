"""Lease adjudication configuration tables.

Core adjudication code must stay generic. Contract-type differences live here:
labels, fact vocabulary, and enabled patch keys.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple


Terms = Tuple[str, ...]
MOUNT_PRE = "前置"
MOUNT_POST = "后置"
MOUNT_REPLACE = "替换"


@dataclass(frozen=True)
class PatchMount:
    patch_id: str
    node_id: str
    mount_mode: str
    patch_name: str = ""
    trigger_condition: str = ""
    legal_basis: str = ""
    logic: str = ""
    output_format: str = ""


PatchMounts = Tuple[PatchMount, ...]


@dataclass(frozen=True)
class LeaseTypeConfig:
    key: str
    display_name: str
    asset_label: str
    lessor_label: str
    tenant_label: str
    deposit_label: str = "押金"
    early_return_label: str = "提前返还"
    continue_use_label: str = "继续使用"
    defect_module_label: str = "租赁物自身瑕疵"
    procedure_court: str = "一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理"
    non_lessor_signer_result: str = "应列合同签署方为被告；是否追加实际出租人，需结合授权、追认或者表见代理事实判断"
    lease_before_transfer_conclusion: str = ""
    expropriation_conclusion: str = ""
    notified_defect_patch_label: str = ""
    patch_mounts: PatchMounts = field(default_factory=tuple)
    terms: Dict[str, Terms] = field(default_factory=dict)
    patch_labels: Dict[str, str] = field(default_factory=dict)
    patch_conclusions: Dict[str, str] = field(default_factory=dict)

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


COMMON_TERMS: Dict[str, Terms] = {
    "tenant": ("承租人", "租客", "租户", "乙方", "使用人"),
    "lessor": ("出租人", "房东", "车主", "设备出租方", "甲方"),
    "termination_request": ("解除合同", "提前终止合同", "要求终止", "单方解除", "提前解除"),
    "force_majeure": ("不可抗力", "洪水", "地震", "台风", "火灾导致无法使用"),
    "sublease_unauthorized": ("擅自转租", "私自转租", "未经同意转租", "擅自转借", "私自转借"),
    "fundamental_breach": ("根本违约", "严重违约"),
    "agreed_termination": ("约定解除", "合同约定可以解除", "按合同解除", "解除条款"),
    "jurisdiction_question": ("哪里起诉", "去哪起诉", "哪个法院", "管辖法院", "起诉地点", "起诉到哪里"),
    "defendant_question": ("告谁", "起诉谁", "列谁为被告", "被告是谁", "告对人"),
    "contract_invalid": ("合同无效", "无效合同", "合同未成立", "违法无效"),
    "contract_valid": ("合同有效", "签订租赁合同", "签了租赁合同", "双方合同"),
    "early_return": ("提前退租", "提前退还", "提前归还", "提前返还", "提前解除", "未到期退租"),
    "no_early_clause": ("没有提前退租约定", "无提前退租约定", "未约定提前退租", "合同没有约定提前退租"),
    "early_clause": ("提前退租不退押金", "提前退还不退押金", "提前退租扣押金", "提前退还扣押金", "提前退租违约金", "约定提前退租", "按约定扣", "押金不退"),
    "no_damage": ("没有损坏", "无损坏", "未损坏", "完好", "正常归还"),
    "damage": ("损坏", "破损", "坏了", "维修", "修理", "刮擦", "故障", "毁损"),
    "natural_wear": ("自然损耗", "自然磨损", "正常损耗", "正常磨损", "正常使用磨损", "老化", "合理损耗"),
    "unproven": ("无法证明", "不能证明", "证据不足", "无法举证", "不清楚是谁", "原因不明"),
    "tenant_fault": ("租客过错", "承租人过错", "租客造成", "承租人造成", "承租人原因", "租客原因", "人为损坏", "使用不当", "操作不当"),
    "check_in_notice": ("交付时告知", "入住时告知", "取车时告知", "交机时告知", "使用前告知", "原本就有", "本来就有"),
    "lessor_no_objection": ("出租人知情未异议", "房东知情未异议", "车主知情未异议", "出租方知情未异议", "未提异议", "没有异议", "知情"),
    "overbroad_clause_clause": ("合同", "条款", "约定", "写明", "载明", "规定"),
    "overbroad_clause_tenant": ("租客", "承租人", "乙方", "使用人"),
    "overbroad_clause_damage": ("损坏", "破损", "毁损", "损失", "故障"),
    "overbroad_clause_liability": ("赔偿", "承担", "负责", "扣押金", "扣除押金"),
    "overbroad_clause_scope": ("任何", "所有", "一切", "全部", "均", "都", "不论原因", "无论原因", "概由"),
    "changed_unforeseeable": ("无法预见", "不能预见", "订立合同时无法预见", "订约时无法预见", "突发政策", "政策突变", "疫情封控"),
    "changed_non_commercial": ("非商业风险", "不属于商业风险", "不是商业风险", "政策突变", "疫情封控"),
    "changed_unfair": ("继续履行显失公平", "继续履行明显不公平", "明显不公平", "显失公平", "无法正常经营"),
    "sublease_chain": ("转租链条", "次承租人", "二房东", "A租B", "B租C", "A租给B", "B租给C", "C出事", "C造成损坏", "转借链条"),
    "lessor_dead": ("出租人死亡", "出租人去世", "出租方死亡", "出租方去世", "所有权人死亡", "所有权人去世"),
    "lessor_heir_refuse": ("继承人拒绝履行", "继承人不认合同", "继承人要求搬走", "继承人要求返还", "继承人拒绝出租", "继承人不继续履行", "拒绝继续履行"),
    "term_expired": ("租赁期限届满", "租期届满", "租期已满", "合同到期", "合同期满", "租赁期满", "固定期限已满", "原租期结束"),
    "continue_use": ("继续使用", "继续占有", "继续居住", "继续开", "继续使用设备", "仍然使用", "到期后仍使用", "期满后继续使用"),
    "collect_rent_or_no_objection": ("继续收租", "继续收取租金", "仍收租", "照常收租", "收了租金", "未提出异议", "没有提出异议", "出租人无异议", "出租方没反对"),
    "no_new_contract": ("未签新合同", "没有签新合同", "未续签合同", "没有续签合同", "续租未签合同", "双方未签订新的租赁合同", "没签新的租赁合同"),
    "traffic_accident": ("交通事故", "车祸", "追尾", "撞车", "剐蹭事故", "事故责任", "发生事故"),
    "traffic_accident_tenant_responsible": ("承租人全责", "承租人主责", "承租人负全部责任", "承租人承担主要责任", "租客全责", "司机全责", "我方全责", "我方主责"),
    "traffic_accident_other_responsible": ("对方全责", "对方主责", "第三方全责", "事故对方全责", "承租人无责", "我方无责", "交警认定对方承担全部责任"),
    "traffic_accident_unknown_liability": ("责任未认定", "事故责任不明", "交警还未认定", "责任无法证明", "责任认定书还没出"),
}


HOUSE_CONFIG = LeaseTypeConfig(
    key="house",
    display_name="房屋租赁",
    asset_label="房屋",
    lessor_label="房东",
    tenant_label="租客",
    early_return_label="提前退租",
    continue_use_label="继续居住",
    defect_module_label="房屋自身瑕疵",
    procedure_court="租赁合同纠纷由房屋所在地人民法院处理",
    non_lessor_signer_result="应列房东妻子为被告，而非房东本人",
    lease_before_transfer_conclusion="租赁合同对新房主继续有效，租客无需搬走，押金事宜仍按原合同执行",
    expropriation_conclusion="合同自动终止，押金全额退还，补偿款归房东",
    notified_defect_patch_label="租客入住时已告知瑕疵且房东知情未提异议",
    patch_mounts=(
        PatchMount("tenant_death", "procedure_review", MOUNT_POST),
        PatchMount("changed_circumstances", "procedure_review", MOUNT_POST),
        PatchMount("illegal_asset", "procedure_review", MOUNT_POST),
        PatchMount("sublease_chain", "procedure_review", MOUNT_POST),
        PatchMount("lessor_death", "procedure_review", MOUNT_POST),
        PatchMount("indefinite_lease", "term_expiry", MOUNT_PRE),
    ),
    terms={
        **COMMON_TERMS,
        "asset": ("房屋", "房子", "出租屋", "租赁房屋"),
        "non_lessor_signer": ("妻子代签", "丈夫代签", "父母代签", "朋友代签", "中介代签", "不是房东本人", "非房东本人签署"),
        "third_party": ("邻居", "路人", "第三方", "外人", "中介打伤", "物业造成", "他人造成"),
        "asset_transfer": ("卖房", "出售房屋", "房屋出售", "新房主", "新业主", "买受人"),
        "lease_before_transfer": ("先租后卖", "出租后出售", "租期内卖房", "签租约后卖房", "租赁期间出售"),
        "transfer_before_lease": ("先卖后租", "卖房后又出租", "出售后出租", "已经卖了还出租"),
        "transfer_without_notice": ("未通知租客", "没有通知租客", "未提前通知", "没提前通知"),
        "pre_delivery_defect": ("交付前漏水", "入住前漏水", "交房前漏水", "交付前已有瑕疵", "入住前已有瑕疵", "房屋本来漏水"),
        "third_party_defect": ("楼上漏水", "楼上泡水", "邻居漏水", "物业管道漏水", "第三方原因导致漏水"),
        "expropriation": ("政府征收", "房屋征收", "拆迁", "被征收"),
        "serious_safety_risk": ("危房", "严重安全隐患", "不能安全居住", "无法居住", "房屋有倒塌风险"),
        "tenant_dead": ("承租人死亡", "承租人去世", "租客死亡", "租客去世", "租户死亡", "租户去世"),
        "cohabitant_or_cooperator": ("共同居住人", "共同经营人", "同住人", "一起住的人", "共同居住的家人", "共同经营伙伴"),
        "no_cohabitant_or_cooperator": ("无共同居住人或共同经营人", "没有共同居住人或共同经营人", "无共同居住人和共同经营人", "没有共同居住人和共同经营人"),
        "successor_continue": ("愿意继续承租", "要求继续承租", "继续承租", "继续租赁", "继续住", "接替履行", "接着租"),
        "successor_terminate": ("共同居住人要求解除", "共同经营人要求解除", "同住人要求解除", "继承人要求解除", "不愿继续承租", "不想继续租", "要求解除合同"),
        "illegal_asset": ("违法建筑", "违建", "未取得建设工程规划许可证", "没有建设工程规划许可证", "没有规划许可证", "未按规划建设", "违法建设"),
    },
    patch_labels={
        "illegal_asset": "补丁三：违法建筑",
    },
    patch_conclusions={
        "illegal_asset": "租赁物为违法建筑，合同无效，押金应返还，使用费另计，损失可主张赔偿。",
        "lessor_death": "出租人死亡，合同由继承人继续履行，押金处理不受影响。",
        "lessor_death_heir_refuse": "出租人死亡，合同由继承人继续履行，押金处理不受影响；继承人拒绝履行的，承租人可起诉要求继续履行或主张违约赔偿。",
    },
)


VEHICLE_CONFIG = LeaseTypeConfig(
    key="vehicle",
    display_name="车辆租赁",
    asset_label="车辆",
    lessor_label="出租人",
    tenant_label="承租人",
    defect_module_label="车辆自身瑕疵",
    patch_mounts=(
        PatchMount(
            "V2",
            "contract_type_identification",
            MOUNT_POST,
            "以租代购",
            "合同为融资租赁或以租代购，或约定期满后车辆归承租人",
            "《民法典》融资租赁合同章",
            "按融资租赁处理，不进入普通押金返还逻辑",
            "以租代购合同，适用融资租赁规则：所有权归出租人，违约可收回车辆，已付租金不予退还。",
        ),
        PatchMount(
            "V4",
            "proper_defendant",
            MOUNT_POST,
            "合同相对性原则例外-车辆",
            "承租人签订合同但车辆由第三人实际使用，承租人以不是本人驾驶抗辩",
            "《民法典》第465条",
            "承租人先向出租人承担合同责任，再向实际使用人追偿",
            "合同相对性原则适用：承租人向出租人承担全部责任，可另行向实际使用人追偿。",
        ),
        PatchMount("changed_circumstances", "procedure_review", MOUNT_POST),
        PatchMount("illegal_asset", "procedure_review", MOUNT_POST),
        PatchMount("sublease_chain", "procedure_review", MOUNT_POST),
        PatchMount("lessor_death", "procedure_review", MOUNT_POST),
        PatchMount(
            "V3",
            "contract_validity",
            MOUNT_PRE,
            "出租人审查义务",
            "承租人无有效驾驶资格",
            "《民法典》第1209条",
            "判断出租人是否审查承租人驾驶资格，未审查或明知无资格仍出租的承担相应责任",
            "出租人审查义务判断：已审查/未审查，过错成立/不成立，责任承担比例。",
        ),
        PatchMount("indefinite_lease", "term_expiry", MOUNT_PRE),
        PatchMount("traffic_accident_liability", "damage_cause", MOUNT_POST),
        PatchMount(
            "V1",
            "amount_calculation",
            MOUNT_POST,
            "停运损失",
            "车辆因承租人原因损坏且正在维修，出租人主张维修期间租金损失",
            "司法实践中车辆维修期间无法营运的损失由过错方承担",
            "日租金 × 实际维修天数；提供替代车辆或过度维修时不支持或调减",
            "承租人承担停运损失 [日租金 × 维修天数] 元",
        ),
    ),
    terms={
        **COMMON_TERMS,
        "asset": ("车辆", "汽车", "租赁车辆", "车子", "货车", "客车"),
        "non_lessor_signer": ("不是车主本人", "非车主本人签署", "代车主签", "朋友代签", "中介代签"),
        "third_party": ("路人", "第三方", "其他车辆", "对方车辆", "代驾", "他人造成"),
        "asset_transfer": (),
        "lease_before_transfer": (),
        "transfer_before_lease": (),
        "transfer_without_notice": (),
        "pre_delivery_defect": ("交车前故障", "取车前故障", "交付前已有故障", "车辆本来有故障", "交车前已有瑕疵"),
        "third_party_defect": ("事故对方造成", "其他车辆撞坏", "第三方原因导致故障", "维修厂造成损坏"),
        "expropriation": ("车辆被依法扣押", "车辆被强制报废", "车辆被征收"),
        "serious_safety_risk": ("刹车失灵", "严重安全隐患", "不能安全驾驶", "车辆无法安全使用"),
        "illegal_asset": ("套牌车", "报废车", "拼装车", "无牌车", "非法改装车辆", "车辆违法不能上路"),
        "financing_lease": ("融资租赁合同", "以租代购合同", "以租代购", "租赁期满后车辆所有权归承租人", "期满后车辆归承租人", "象征性支付尾款后过户", "尾款后过户", "期满过户"),
        "vehicle_no_driving_qualification": ("无证驾驶", "没有驾驶证", "无有效驾驶证", "驾驶证被吊销", "驾照被吊销", "驾驶证过期", "未成年人租车", "未成年人驾驶"),
        "lessor_checked_qualification": ("已审查驾驶证", "已经审查驾驶证", "核验了驾驶证", "查验驾驶证", "审核驾驶资格", "确认有驾驶证"),
        "lessor_failed_qualification_check": ("未审查驾驶证", "没有审查驾驶证", "未核验驾驶证", "明知无证仍出租", "知道无证还出租", "未审核驾驶资格"),
        "actual_user_vehicle": ("实际使用人", "实际驾驶人", "别人开的", "朋友开的", "他人驾驶", "第三人驾驶", "代驾开的", "车不是承租人开的"),
        "tenant_denies_actual_use_liability": ("车不是我开的", "不是我开的", "我不该赔", "不应由我赔", "我不负责", "与我无关", "不该找我赔"),
        "vehicle_under_repair": ("正在维修", "维修中", "送修", "修车期间", "维修期间", "车辆维修"),
        "stoppage_loss_claim": ("停运损失", "营运损失", "维修期间租金损失", "维修期间的租金损失", "租金损失", "停驶损失"),
        "vehicle_over_repair": ("过度维修", "扩大维修", "不合理维修", "维修不必要", "维修时间过长"),
        "replacement_vehicle_provided": ("提供代步车", "已提供代步车", "提供替代车辆", "已提供替代车辆", "备用车"),
        "repair_days": ("维修", "修理", "维修期间", "实际维修天数", "停运"),
        "daily_rent": ("日租金", "每日租金", "每天租金", "一天租金", "日租"),
    },
    patch_conclusions={
        "illegal_asset": "租赁车辆依法不能上路或属于违法车辆，合同无效，押金应返还，已实际使用期间的使用费另计，损失可主张赔偿。"
    },
)


EQUIPMENT_CONFIG = LeaseTypeConfig(
    key="equipment",
    display_name="设备租赁",
    asset_label="设备",
    lessor_label="出租方",
    tenant_label="承租方",
    defect_module_label="设备自身故障",
    patch_mounts=(
        PatchMount(
            "E3",
            "proper_defendant",
            MOUNT_POST,
            "实际使用人直接担责",
            "设备由第三人实际使用并造成设备损毁或他人损害",
            "《民法典》第1165条",
            "出租人可向承租人主张合同责任，也可向实际使用人主张侵权责任，但不得重复受偿",
            "实际使用人侵权责任成立，出租人可向承租人主张合同责任，也可直接向实际使用人主张侵权责任。",
        ),
        PatchMount("changed_circumstances", "procedure_review", MOUNT_POST),
        PatchMount("illegal_asset", "procedure_review", MOUNT_POST),
        PatchMount("sublease_chain", "procedure_review", MOUNT_POST),
        PatchMount("lessor_death", "procedure_review", MOUNT_POST),
        PatchMount(
            "E1",
            "asset_defect",
            MOUNT_REPLACE,
            "承租人防止损失扩大义务",
            "设备出现故障或异常，承租人未及时通知或未采取合理措施，损失因此扩大",
            "《民法典》第591条",
            "判断承租人是否及时通知并采取合理措施，未履行时对扩大损失承担责任",
            "承租人防止损失扩大义务：已履行/未履行，对扩大损失承担 [具体金额或比例]。",
        ),
        PatchMount("indefinite_lease", "term_expiry", MOUNT_PRE),
        PatchMount(
            "E2",
            "damage_status",
            MOUNT_PRE,
            "租赁物灭失后的租金支付",
            "设备在租赁期间被偷、被烧、被洪水冲走等完全灭失",
            "租赁物灭失导致合同无法继续履行，但已产生的租金义务不因灭失而免除",
            "灭失前租金仍需支付，未来租金不再支付；按可归责性判断赔偿责任",
            "设备灭失：灭失前租金仍需支付，未来租金不再支付，可归责/不可归责，赔偿责任 [具体金额]。",
        ),
    ),
    terms={
        **COMMON_TERMS,
        "asset": ("设备", "机器", "机械", "租赁设备", "生产设备", "施工设备"),
        "non_lessor_signer": ("不是设备所有人", "非设备所有人签署", "代出租方签", "中介代签"),
        "third_party": ("第三方", "操作员", "维修方", "承运方", "他人造成"),
        "asset_transfer": (),
        "lease_before_transfer": (),
        "transfer_before_lease": (),
        "transfer_without_notice": (),
        "pre_delivery_defect": ("交付前故障", "进场前故障", "交机前故障", "交付前已有瑕疵", "设备本来有故障"),
        "third_party_defect": ("第三方原因导致故障", "维修方造成损坏", "承运方造成损坏", "他人操作造成损坏"),
        "expropriation": ("设备被依法扣押", "设备被征收", "设备被查封"),
        "serious_safety_risk": ("严重安全隐患", "不能安全使用", "设备无法安全运行", "存在重大事故风险"),
        "illegal_asset": ("违法设备", "国家禁止使用设备", "未取得强制许可", "没有强制认证", "非法改装设备", "特种设备未检验"),
        "equipment_fault_abnormal": ("设备故障", "设备异常", "机器故障", "机器异常", "运行异常", "报警", "异响", "漏油", "过热"),
        "tenant_timely_notice": ("及时通知出租方", "马上通知出租方", "及时报修", "立即报修", "第一时间通知", "已采取合理措施", "停止使用设备"),
        "tenant_failed_notice_or_measures": ("未及时通知", "没有及时通知", "未通知出租方", "没有报修", "继续使用", "带病运行", "未采取合理措施", "放任故障"),
        "loss_expanded": ("损失扩大", "损失进一步扩大", "故障扩大", "故障恶化", "损坏加重", "扩大损失"),
        "equipment_scrapped": ("彻底报废", "设备报废", "机器报废", "无法修复", "完全损毁"),
        "equipment_total_loss": ("被偷", "被盗", "被烧", "烧毁", "洪水冲走", "被洪水冲走", "完全灭失", "灭失", "丢失", "遗失"),
        "loss_during_lease": ("租赁期间", "合同履行期间", "使用期间", "承租期间", "租期内"),
        "loss_tenant_fault": ("保管不善", "未锁门", "承租人过错", "承租方过错", "管理不善", "擅自拆除", "违规操作"),
        "loss_no_fault": ("自然灾害", "洪水", "地震", "不可抗力", "不可归责于双方", "无法归责于双方"),
        "unpaid_rent": ("拖欠租金", "欠付租金", "灭失前租金", "已产生租金", "未付租金"),
        "actual_user_equipment": ("实际使用人", "第三人使用", "第三人操作", "操作员", "工人操作", "借给第三人使用", "交给第三人使用"),
        "equipment_actual_user_damage": ("造成设备损毁", "造成设备损坏", "造成他人损害", "造成他人受伤", "操作造成损害", "使用时损毁"),
    },
    patch_conclusions={
        "illegal_asset": "租赁设备依法不得使用或缺少强制许可，合同无效，押金应返还，已实际使用期间的使用费另计，损失可主张赔偿。"
    },
)


LEASE_TYPE_CONFIGS: Dict[str, LeaseTypeConfig] = {
    HOUSE_CONFIG.key: HOUSE_CONFIG,
    VEHICLE_CONFIG.key: VEHICLE_CONFIG,
    EQUIPMENT_CONFIG.key: EQUIPMENT_CONFIG,
}


def get_lease_config(contract_type: str | None) -> LeaseTypeConfig:
    key = (contract_type or "house").strip().lower()
    aliases = {
        "housing": "house",
        "房屋": "house",
        "车辆": "vehicle",
        "car": "vehicle",
        "vehicle": "vehicle",
        "设备": "equipment",
        "machine": "equipment",
        "equipment": "equipment",
    }
    key = aliases.get(key, key)
    return LEASE_TYPE_CONFIGS.get(key, HOUSE_CONFIG)
