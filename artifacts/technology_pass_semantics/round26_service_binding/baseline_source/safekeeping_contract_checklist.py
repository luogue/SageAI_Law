"""保管合同审查清单（第二版）。

本文件只定义审查检查点，不输出裁判结论。检查点由保管合同裁判树节点反向映射而来，
覆盖合同成立、有偿/无偿区分、妥善保管、亲自保管、不得使用、瑕疵告知、
贵重物品声明、消费保管、留置权和返还规则等核心规则。
"""

from __future__ import annotations

from typing import Tuple

from review_v2.house_lease_checklist import ReviewCheckpoint


def _required(
    item_id: str,
    node_id: str,
    title: str,
    risk_level: str,
    terms: Tuple[str, ...],
    risk_point: str,
    suggested_clause: str,
    legal_basis: str,
    legal_consequence_if_missing: str | None = None,
    semantic_question: str | None = None,
    pass_criteria: str | None = None,
    partial_criteria: str | None = None,
) -> ReviewCheckpoint:
    return ReviewCheckpoint(
        item_id=item_id,
        node_id=node_id,
        title=title,
        kind="required",
        risk_level=risk_level,
        terms=terms,
        risk_point_missing=risk_point,
        risk_point_present=f"合同已覆盖“{title}”相关安排，建议继续核对表述是否具体、保管物信息是否完整、责任边界是否清楚。",
        suggested_clause=suggested_clause,
        legal_basis=legal_basis,
        legal_consequence_if_missing=legal_consequence_if_missing or risk_point,
        semantic_question=semantic_question or f"合同是否已明确约定“{title}”，并能覆盖保管合同裁判树中对应的核心风险？",
        evidence_scope="正式合同条款及附件",
        pass_criteria=pass_criteria or f"正式合同条款或附件中存在与“{title}”相关的明确、可执行约定，且关键主体、保管物、期限、金额或选项已填写完整。",
        partial_criteria=partial_criteria or f"正式合同条款或附件中已有与“{title}”相关安排，但存在空白、未勾选、金额期限不完整、保管物范围不清或责任边界不明。",
    )


def _forbidden(
    item_id: str,
    node_id: str,
    title: str,
    risk_level: str,
    terms: Tuple[str, ...],
    risk_point: str,
    suggested_clause: str,
    legal_basis: str,
    legal_consequence_if_missing: str | None = None,
    semantic_question: str | None = None,
    pass_criteria: str | None = None,
    partial_criteria: str | None = None,
) -> ReviewCheckpoint:
    return ReviewCheckpoint(
        item_id=item_id,
        node_id=node_id,
        title=title,
        kind="forbidden",
        risk_level=risk_level,
        terms=terms,
        risk_point_missing=f"合同暂未发现“{title}”类明显不利表述，建议仍按公平、具体、可证明的方式约定保管安排。",
        risk_point_present=risk_point,
        suggested_clause=suggested_clause,
        legal_basis=legal_basis,
        legal_consequence_if_missing=legal_consequence_if_missing or risk_point,
        semantic_question=semantic_question or f"合同中是否存在“{title}”类不当排除法定权利、混淆合同性质或过度加重一方责任的风险表述？",
        evidence_scope="正式合同条款及附件",
        pass_criteria=pass_criteria or f"正式合同条款及附件中未发现“{title}”类风险表述。",
        partial_criteria=partial_criteria or f"正式合同条款及附件中存在接近“{title}”的表述，需要人工复核其是否公平、具体、可执行。",
    )


SAFEKEEPING_REVIEW_CHECKLIST: Tuple[ReviewCheckpoint, ...] = (
    # ===== D-01 合同性质认定 =====
    _required("D-01-01", "safekeeping_contract_nature", "保管合同性质", "高", ("保管合同", "寄存合同", "保管人", "寄存人", "保管物"), "未明确合同性质为保管，可能与租赁、场地租赁、自助存放或仓储关系混淆，影响成立要件和责任标准。", "双方确认本合同为保管合同，寄存人将本合同约定保管物交付保管人保管，保管人负有妥善保管并返还保管物的义务。", "《民法典》第888条"),
    _required("D-01-02", "safekeeping_keep_return_purpose", "保管并返还原物目的", "高", ("保管并返还", "返还原物", "看管", "寄存", "代为保管"), "未写明保管并返还原物目的，容易被理解为仅提供场地或转移使用权。", "保管人接受保管物后，应按约定场所和方法妥善保管，并在寄存人领取或合同终止时返还原物及孳息。", "《民法典》第888条、第899条、第900条"),
    _required("D-01-03", "safekeeping_actual_control", "保管人实际控制保管物", "高", ("实际控制", "交给保管人", "保管人接收", "统一保管", "专人看管"), "未体现保管人实际控制保管物，可能被认定为场地租赁或自助存放而非保管。", "保管物交付后由保管人实际控制、看管和管理；寄存人仅享有按约领取和监督权，不自行控制保管场所。", "《民法典》第888条、第890条"),
    _forbidden("D-01-04", "safekeeping_venue_only_confusion", "仅提供场地却写保管", "中", ("仅提供场地", "自助存放", "不负责看管", "场地租赁", "自行保管"), "合同名为保管但实质只提供场地且排除看管义务，会导致合同性质和责任标准不清。", "建议改为：如保管人实际看管，应明确保管义务；如仅出租场地，应按场地租赁或租赁合同重写。", "《民法典》第888条"),

    # ===== D-02 合同成立要件 =====
    _required("D-02-01", "safekeeping_delivery_establishment", "保管物交付成立", "高", ("交付", "交给保管人", "接收", "保管开始", "成立"), "未约定保管物交付与合同成立的关系，可能因保管物尚未交付而发生合同是否成立争议。", "除双方另有书面约定外，本合同自寄存人将保管物交付保管人且保管人接收时成立。", "《民法典》第890条"),
    _required("D-02-02", "safekeeping_establishment_exception", "排除实践合同的特别约定", "中", ("另有约定", "签订时成立", "未交付仍成立", "预约交付", "生效"), "如希望签约即产生义务但未特别约定，可能被实践合同规则影响。", "双方特别约定，本合同自双方签字盖章之日起成立并生效；寄存人应于__日前交付保管物，保管人应按约接收。", "《民法典》第890条"),
    _required("D-02-03", "safekeeping_delivery_receipt", "交付凭证和接收确认", "高", ("交付凭证", "收据", "寄存单", "签收", "接收确认"), "未设置交付凭证，保管物是否交付、数量状态如何，后续举证困难。", "保管人接收保管物时应向寄存人出具寄存单、收据或电子接收凭证，载明保管物名称、数量、状态、交付时间和领取方式。", "《民法典》第888条、第890条"),
    _required("D-02-04", "safekeeping_before_delivery_risk", "交付前风险归属", "中", ("交付前", "尚未交付", "风险", "损坏", "灭失"), "未约定交付前风险，保管物在交付前损坏或丢失时责任容易争议。", "保管物交付保管人前的毁损、灭失风险由寄存人自行承担；保管人已迟延接收或存在过错的除外。", "《民法典》第890条、第509条"),

    # ===== D-03 保管物描述 =====
    _required("D-03-01", "safekeeping_item_name_quantity", "保管物名称和数量", "高", ("保管物名称", "数量", "件数", "重量", "清单"), "未明确保管物名称、数量或计量方式，返还和赔偿范围无法确定。", "保管物名称为__，数量/重量/件数为__，具体明细以附件《保管物清单》为准。", "《民法典》第470条、第888条"),
    _required("D-03-02", "safekeeping_item_status", "保管物状态记录", "高", ("状态", "外观", "瑕疵", "照片", "封存"), "未记录交付时状态，保管期间是否发生损坏难以判断。", "双方应在交付时共同确认保管物外观、功能、包装、瑕疵和封存情况，并以照片、视频或书面清单固定。", "《民法典》第893条、第897条"),
    _required("D-03-03", "safekeeping_item_nature_requirement", "保管物性质和特殊需求", "高", ("易腐", "易燃", "冷藏", "恒温", "特殊保管", "危险品"), "未说明保管物性质和特殊保管需求，保管方法错误可能造成损失。", "寄存人应在交付前书面说明保管物性质、瑕疵、危险性、保存温度、湿度、防火、防盗、防潮等特殊保管要求。", "《民法典》第893条"),
    _required("D-03-04", "safekeeping_item_value", "保管物价值确认", "中", ("价值", "市场价", "评估价", "赔偿上限", "声明价值"), "未确认保管物价值，毁损灭失后的赔偿金额争议较大。", "寄存人声明保管物参考价值为人民币__元；保管人可要求寄存人提供购买凭证、评估报告或其他价值证明。", "《民法典》第897条、第898条"),

    # ===== D-04 保管费与性质 =====
    _required("D-04-01", "safekeeping_fee_paid_or_unpaid", "有偿或无偿保管", "高", ("有偿保管", "无偿保管", "保管费", "免费保管", "费用"), "未明确保管费，根据法律可能被视为无偿保管，保管人责任标准会显著降低。", "双方确认本合同为□有偿保管 / □无偿保管。有偿保管的，保管费标准按本合同第__条执行；未勾选或约定不明的，按无偿保管处理。", "《民法典》第889条"),
    _required("D-04-02", "safekeeping_fee_amount_payment", "保管费金额和支付方式", "高", ("保管费", "金额", "支付方式", "支付时间", "结算"), "有偿保管未明确金额、支付节点和方式，保管费是否到期及留置权基础不清。", "保管费为人民币__元/日或__元/月，寄存人应于__日前通过__方式支付至保管人指定账户。", "《民法典》第889条、第903条"),
    _required("D-04-03", "safekeeping_fee_extra_costs", "额外费用承担", "中", ("额外费用", "仓储费", "搬运费", "保险费", "逾期费用"), "未约定额外保管、搬运、保险、逾期领取等费用，后续结算容易争议。", "因寄存人特殊保管要求、逾期领取、变更保管方式或第三方收费产生的合理额外费用，由寄存人承担，但保管人应提供费用凭证。", "《民法典》第509条、第902条、第903条"),
    _required("D-04-04", "safekeeping_fee_unclear_default", "费用约定不明的无偿后果", "中", ("约定不明", "视为无偿", "未约定费用", "免费", "责任标准"), "未提示费用不明视为无偿，双方可能误判责任标准。", "双方确认，如保管费未约定或约定不明确且无法补充确定的，本合同按无偿保管处理，保管人责任标准相应适用无偿保管规则。", "《民法典》第889条、第897条"),

    # ===== D-05 保管人义务 =====
    _required("D-05-01", "safekeeping_proper_custody", "妥善保管义务", "高", ("妥善保管", "保管义务", "安全措施", "防盗", "防火", "防潮"), "未明确妥善保管义务，保管人应采取何种安全措施不清。", "保管人应按保管物性质和本合同约定采取防盗、防火、防潮、防损、防污染等合理措施，妥善保管保管物。", "《民法典》第892条、第897条"),
    _required("D-05-02", "safekeeping_place_method", "保管场所和方法", "高", ("保管场所", "保管方法", "仓库", "保险柜", "冷藏", "封存"), "未约定保管场所和方法，发生损失时难以判断保管人是否尽责。", "保管场所为__，保管方法为__；保管人应按本合同约定场所、方法和安全等级保管保管物。", "《民法典》第892条"),
    _required("D-05-03", "safekeeping_place_method_change", "变更保管场所或方法", "高", ("变更保管场所", "改变保管方法", "紧急情况", "寄存人同意", "通知"), "未约定变更条件，保管人擅自改变保管场所或方法后责任不清。", "未经寄存人书面同意，保管人不得改变保管场所或方法；因紧急情况或为维护寄存人利益必须变更的，应及时通知寄存人。", "《民法典》第892条"),
    _required("D-05-04", "safekeeping_return_obligation", "返还保管物义务", "高", ("返还", "归还", "领取", "原物", "孳息"), "未明确返还义务，保管期满或寄存人领取时原物和孳息如何返还不清。", "保管人应在寄存人依法领取或保管期限届满时返还保管物原物及其孳息；双方另有消费保管约定的除外。", "《民法典》第899条、第900条、第901条"),

    # ===== D-06 寄存人义务 =====
    _required("D-06-01", "safekeeping_depositor_disclosure", "保管物瑕疵和特殊需求告知", "高", ("告知", "瑕疵", "特殊保管", "危险性", "说明"), "未约定寄存人告知义务，保管物自身性质导致损失时责任分配不清。", "寄存人应在交付前如实告知保管物瑕疵、特殊性质、危险性及特殊保管要求；未告知造成损失的，寄存人承担相应责任。", "《民法典》第893条"),
    _required("D-06-02", "safekeeping_valuable_declaration", "贵重物品声明义务", "高", ("贵重物品", "货币", "有价证券", "声明", "验收", "封存"), "寄存货币、有价证券或贵重物品未约定声明义务，毁损灭失后可能只能按一般物品赔偿。", "寄存货币、有价证券、珠宝、名表、贵金属、重要文件或其他贵重物品的，寄存人应事先声明并由保管人验收或封存。", "《民法典》第898条"),
    _required("D-06-03", "safekeeping_undeclared_valuable_consequence", "未声明贵重物品后果", "高", ("未声明", "一般物品", "赔偿", "贵重物品", "价值"), "未提示未声明贵重物品的后果，寄存人可能误以为可按实际高价值索赔。", "寄存人未声明贵重物品且保管人按一般物品接收保管的，毁损、灭失时按一般物品价值确定赔偿范围。", "《民法典》第898条"),
    _required("D-06-04", "safekeeping_depositor_packaging", "寄存人包装和交付协助", "中", ("包装", "密封", "标签", "交付资料", "危险标识"), "未约定包装、标签和交付协助义务，可能影响保管安全和责任认定。", "寄存人应按保管物性质提供适当包装、标签、危险标识和必要资料；包装不当导致损失的，由寄存人承担相应责任。", "《民法典》第509条、第893条"),

    # ===== D-07 保管物毁损灭失 =====
    _required("D-07-01", "safekeeping_paid_general_negligence", "有偿保管一般过失责任", "高", ("有偿保管", "一般过失", "赔偿责任", "注意义务", "保管不善"), "有偿保管未明确一般过失责任标准，保管物毁损灭失时责任判断不清。", "本合同为有偿保管的，保管人因未尽妥善保管义务造成保管物毁损、灭失的，应承担赔偿责任。", "《民法典》第897条"),
    _required("D-07-02", "safekeeping_unpaid_intent_gross", "无偿保管故意或重大过失责任", "高", ("无偿保管", "故意", "重大过失", "轻过失", "不承担"), "无偿保管未明确仅在故意或重大过失时担责，可能导致责任预期混乱。", "本合同为无偿保管的，保管人证明自己没有故意或者重大过失的，不承担保管物毁损、灭失赔偿责任。", "《民法典》第897条"),
    _required("D-07-03", "safekeeping_loss_cause_evidence", "损失原因和举证材料", "中", ("损失原因", "证明", "监控", "记录", "事故报告"), "未约定损失原因证明材料，发生毁损灭失后双方举证困难。", "保管物发生毁损、灭失或短少的，保管人应及时通知寄存人，并提供监控、出入库记录、事故报告、报警记录等可核验证据。", "《民法典》第897条、第509条"),
    _forbidden("D-07-04", "safekeeping_overbroad_liability_clause", "无论原因一律赔偿", "中", ("无论任何原因均赔偿", "一律赔偿", "不可抗力也赔偿", "轻微过失也赔偿"), "合同不区分有偿/无偿和过错程度，一概要求保管人赔偿，可能与法定责任标准冲突。", "建议改为：有偿保管按一般过失责任处理；无偿保管以故意或重大过失为责任基础；不可抗力、寄存人过错或保管物自身性质另按约定处理。", "《民法典》第897条"),

    # ===== D-08 转保管 =====
    _required("D-08-01", "safekeeping_no_transfer_to_third", "禁止擅自转保管", "中", ("转保管", "第三人保管", "不得转交", "委托第三人", "亲自保管"), "未禁止擅自转保管，保管人将保管物交给第三人后责任容易争议。", "未经寄存人书面同意，保管人不得将保管物转交第三人保管。", "《民法典》第894条"),
    _required("D-08-02", "safekeeping_transfer_agreed_condition", "约定转保管条件", "中", ("同意转保管", "第三方仓库", "书面同意", "转交", "分包保管"), "业务确需第三方保管但未约定条件，转保管是否有效和责任归属不清。", "确需转交第三人保管的，保管人应事先取得寄存人书面同意，并告知第三人名称、保管场所、保管方法和责任安排。", "《民法典》第894条"),
    _required("D-08-03", "safekeeping_transfer_liability", "转保管责任承担", "中", ("转保管责任", "第三人损失", "赔偿", "连带", "追偿"), "未约定转保管后的责任，第三人造成损失时寄存人追责路径不清。", "保管人经同意转保管的，仍应对第三人的保管行为向寄存人承担合同责任；第三人造成损失的，保管人赔偿后可依法追偿。", "《民法典》第894条、第577条"),
    _forbidden("D-08-04", "safekeeping_transfer_full_exemption", "转保管后一概免责", "中", ("转交后免责", "第三人负责", "保管人不再负责", "概不承担责任"), "合同约定保管人转保管后一概免责，可能使寄存人无法向合同相对方追责。", "建议改为：保管人经寄存人同意转保管的，仍对第三人保管行为承担合同责任；未经同意转保管造成损失的，保管人承担赔偿责任。", "《民法典》第894条"),

    # ===== D-09 保管人留置权 =====
    _required("D-09-01", "safekeeping_lien_condition", "保管人留置权条件", "中", ("留置权", "未支付保管费", "扣留保管物", "费用到期", "拒付"), "未约定留置权及条件，寄存人欠费时保管人能否留置保管物不清。", "寄存人未按约支付到期保管费、保管必要费用或其他应付款项的，保管人可依法对相应保管物行使留置权。", "《民法典》第903条"),
    _required("D-09-02", "safekeeping_lien_notice_scope", "留置通知和范围限制", "中", ("留置通知", "范围", "相当价值", "超额留置", "合理期限"), "未限制留置范围，可能发生超额留置或不当扣留。", "保管人行使留置权前应书面通知寄存人，并以欠付费用及合理实现费用相当价值范围为限，不得明显超额留置。", "《民法典》第448条、第453条、第903条"),
    _required("D-09-03", "safekeeping_lien_exclusion", "排除留置权的特别约定", "低", ("不得留置", "排除留置权", "禁止扣留", "另有约定", "约定排除"), "如双方希望排除留置权但未明确，保管人仍可能依法留置。", "双方特别约定：保管人不得以保管费或其他费用未付为由留置保管物；寄存人欠费的，保管人可另行主张付款责任。", "《民法典》第903条"),
    _forbidden("D-09-04", "safekeeping_improper_lien", "不当或超额留置", "中", ("留置全部物品", "价值远超欠费", "任意扣留", "不通知留置", "超额留置"), "合同允许保管人不通知、任意或超额留置，可能构成不当留置并产生赔偿风险。", "建议改为：留置应限于同一保管关系下到期未付费用及合理实现费用的相当范围，并提前通知寄存人。", "《民法典》第448条、第903条"),

    # ===== D-10 消费保管 =====
    _required("D-10-01", "safekeeping_consumptive_type", "消费保管类型识别", "中", ("消费保管", "货币保管", "可替代物", "同种类", "同品质"), "未识别是否消费保管，返还原物还是同种类物容易争议。", "双方确认本合同项下保管物属于□普通保管 / □消费保管；选择消费保管的，返还规则按本合同第__条执行。", "《民法典》第901条"),
    _required("D-10-02", "safekeeping_consumptive_return_rule", "同种类同品质数量返还", "中", ("返还同种类", "同数量", "同品质", "货币", "可替代物"), "消费保管未明确返还标准，返还数量、品质和币种可能争议。", "消费保管项下，保管人可返还相同种类、相同数量、相同品质的货币或可替代物，无需返还原物。", "《民法典》第901条"),
    _required("D-10-03", "safekeeping_currency_interest", "货币保管利息或收益", "低", ("货币", "利息", "收益", "孳息", "返还金额"), "货币消费保管未约定利息或收益归属，可能引发结算争议。", "保管货币的，保管人应返还同币种同金额货币；是否支付利息或收益按以下约定执行：__。", "《民法典》第901条、第510条"),
    _required("D-10-04", "safekeeping_consumptive_mixing", "可替代物混同保管", "低", ("混同", "同类物", "批量保管", "分装", "计量"), "可替代物混同保管未约定计量和品质标准，返还时容易发生短少或等级争议。", "可替代物可混同保管的，应按入库计量、质量等级和批次记录返还同种类、同数量、同品质物。", "《民法典》第901条"),

    # ===== D-11 保管物返还 =====
    _required("D-11-01", "safekeeping_depositor_anytime_retrieval", "寄存人随时领取权", "中", ("随时领取", "提前领取", "要求返还", "取回", "领取权"), "未约定寄存人随时领取权，保管期限内能否提前取回容易争议。", "寄存人可以随时领取保管物；双方约定保管期限的，提前领取时保管费按实际保管期间及合理费用结算。", "《民法典》第899条"),
    _required("D-11-02", "safekeeping_return_item_fruits", "返还原物及孳息", "中", ("返还原物", "孳息", "利息", "收益", "附属物"), "未约定返还原物及孳息，保管期间产生收益或附属物时归属不清。", "保管人返还保管物时，应一并返还保管物产生的孳息、附属物和相关资料；消费保管另有约定的除外。", "《民法典》第900条、第901条"),
    _required("D-11-03", "safekeeping_return_procedure", "领取和返还程序", "中", ("领取程序", "身份证明", "凭证", "签收", "返还确认"), "未约定领取凭证和返还手续，容易出现冒领取、错返还或是否返还争议。", "寄存人领取保管物时应出示寄存凭证和身份证明；双方应签署返还确认单，载明返还时间、状态、数量和经办人。", "《民法典》第509条、第899条"),
    _required("D-11-04", "safekeeping_overdue_retrieval", "逾期领取和额外费用", "低", ("逾期领取", "到期不取", "催告", "额外保管费", "合理期限"), "保管期满后寄存人逾期不取，未约定催告和费用承担会增加管理风险。", "保管期限届满后寄存人未领取的，保管人可书面催告其在合理期限内领取；逾期产生的合理额外保管费由寄存人承担。", "《民法典》第899条、第900条、第902条"),

    # ===== D-12 附件完整性 =====
    _required("D-12-01", "safekeeping_item_list_attachment", "保管物清单附件", "中", ("保管物清单", "附件", "明细", "编号", "数量"), "未将保管物清单作为附件，保管范围和返还对象难以固定。", "《保管物清单》作为本合同附件，列明保管物名称、数量、价值、编号、状态、包装和特殊保管要求，与本合同具有同等效力。", "《民法典》第469条、第470条、第888条"),
    _required("D-12-02", "safekeeping_photo_video_attachment", "照片视频和封存记录", "中", ("照片", "视频", "封存", "状态记录", "验收"), "未留存照片、视频或封存记录，保管物是否损坏、是否被调换难以证明。", "双方应将交付时照片、视频、封存记录、验收记录作为附件保存，作为判断保管物状态和返还状态的依据。", "《民法典》第893条、第897条"),
    _required("D-12-03", "safekeeping_special_instruction_attachment", "特殊保管说明附件", "低", ("特殊保管说明", "冷藏", "防潮", "危险品", "操作说明"), "特殊保管要求未形成附件，保管人执行标准不稳定。", "寄存人提供的特殊保管说明、操作手册、危险品说明、温湿度要求等作为本合同附件，保管人按附件执行。", "《民法典》第893条"),
    _required("D-12-04", "safekeeping_attachment_priority", "附件效力和冲突顺位", "中", ("附件", "同等效力", "冲突", "优先适用", "补充协议"), "未约定附件效力和冲突顺位，清单、照片、特殊说明与正文不一致时适用规则不清。", "本合同附件、补充协议、保管物清单、照片视频记录、特殊保管说明与正文具有同等效力；内容不一致的，按补充协议、特别约定、保管物清单、合同正文的顺序适用。", "《民法典》第510条、第511条"),
)


def get_safekeeping_checklist() -> Tuple[ReviewCheckpoint, ...]:
    return SAFEKEEPING_REVIEW_CHECKLIST


# Declarative bindings to cross-domain facts; aggregation stays in the engine.
from dataclasses import replace
_LEGAL_TOPICS = {
 'safekeeping_contract_nature': ('custody_definition',),
 'safekeeping_keep_return_purpose': ('custody_definition','return_original_fruits'),
 'safekeeping_actual_control': ('custody_definition','custody_delivery_formation'),
 'safekeeping_venue_only_confusion': ('custody_definition',),
 'safekeeping_delivery_establishment': ('custody_delivery_formation',),
 'safekeeping_establishment_exception': ('custody_delivery_formation',),
 'safekeeping_delivery_receipt': ('custody_receipt',),
 'safekeeping_before_delivery_risk': ('pre_delivery_risk',),
 'safekeeping_item_name_quantity': ('subject_description',),
 'safekeeping_item_status': ('state_records',),
 'safekeeping_item_nature_requirement': ('defect_disclosure',),
 'safekeeping_item_value': ('value_assessment',),
 'safekeeping_fee_paid_or_unpaid': ('custody_fee_obligation',),
 'safekeeping_fee_unclear_default': ('unclear_custody_fee_default',),
 'safekeeping_proper_custody': ('proper_custody','custody_loss_liability'),
 'safekeeping_place_method': ('custody_method',),
 'safekeeping_place_method_change': ('custody_method',),
 'safekeeping_return_obligation': ('return_original_fruits','retrieval_right'),
 'safekeeping_depositor_disclosure': ('defect_disclosure',),
 'safekeeping_valuable_declaration': ('valuable_declaration',),
 'safekeeping_undeclared_valuable_consequence': ('valuable_declaration',),
 'safekeeping_depositor_packaging': ('packaging_assistance',),
 'safekeeping_paid_general_negligence': ('custody_loss_liability',),
 'safekeeping_unpaid_intent_gross': ('custody_loss_liability',),
 'safekeeping_loss_cause_evidence': ('state_records',),
 'safekeeping_overbroad_liability_clause': ('custody_loss_liability',),
 'safekeeping_no_transfer_to_third': ('unauthorized_subcustody',),
 'safekeeping_transfer_agreed_condition': ('unauthorized_subcustody',),
 'safekeeping_transfer_liability': ('unauthorized_subcustody','general_breach_liability'),
 'safekeeping_transfer_full_exemption': ('unauthorized_subcustody','authorized_subcustody_liability'),
 'safekeeping_lien_condition': ('custody_lien_source',),
 'safekeeping_lien_exclusion': ('custody_lien_source',),
 'safekeeping_consumptive_type': ('fungible_return',),
 'safekeeping_consumptive_return_rule': ('fungible_return',),
 'safekeeping_currency_interest': ('income_agreement',),
 'safekeeping_consumptive_mixing': ('fungible_return',),
 'safekeeping_depositor_anytime_retrieval': ('retrieval_right',),
 'safekeeping_return_item_fruits': ('return_original_fruits',),
 'safekeeping_return_procedure': ('retrieval_procedure',),
 'safekeeping_overdue_retrieval': ('overdue_payment_context','overdue_retrieval_context','extra_fee_arrangement','overdue_retrieval','necessary_disposal_costs'),
 'safekeeping_item_list_attachment': ('subject_description','written_attachments'),
 'safekeeping_photo_video_attachment': ('state_records',),
 'safekeeping_special_instruction_attachment': ('defect_disclosure','written_attachments'),
 'safekeeping_attachment_priority': ('attachment_precedence','intent_interpretation'),
 'safekeeping_fee_amount_payment': ('custody_fee_obligation','remuneration_payment','performance_cooperation','unclear_contract_terms'),
 'safekeeping_fee_extra_costs': ('performance_cooperation','unclear_contract_terms'),
 'safekeeping_lien_notice_scope': ('divisible_lien_scope','lien_realization_period','custody_lien_source'),
 'safekeeping_improper_lien': ('divisible_lien_scope','lien_same_relationship','custody_lien_source'),
}
SAFEKEEPING_REVIEW_CHECKLIST=tuple(replace(c,legal_basis_topics=_LEGAL_TOPICS[c.node_id],legal_basis_domain='custody') if c.node_id in _LEGAL_TOPICS else c for c in SAFEKEEPING_REVIEW_CHECKLIST)
from review_v2.shared_fact_concepts import register
_CONCEPT_BINDINGS = {
 'safekeeping_loss_cause_evidence': ('movement_records','retained_visual_records'),
 'safekeeping_return_procedure': ('handover_receipt','retrieval_workflow','signed_handover_record'),
 'safekeeping_photo_video_attachment': ('retained_visual_records','acceptance_record'),
 'safekeeping_return_item_fruits': ('return_entrusted_property','return_property_fruits'),
 'safekeeping_depositor_packaging': ('depositor_packaging_duty','depositor_delivery_assistance'),
 'safekeeping_keep_return_purpose': ('return_entrusted_property',),
 'safekeeping_fee_unclear_default': ('uncertain_remuneration_default',),
 'safekeeping_no_transfer_to_third': ('unauthorized_delegation_control',),
 'safekeeping_transfer_liability': ('unauthorized_delegation_liability','authorized_delegation_liability'),
 'safekeeping_unpaid_intent_gross': ('gratuitous_fault_standard',),
 'safekeeping_actual_control': ('accepted_handover','custody_duty'),
 'safekeeping_delivery_receipt': ('handover_receipt',),
 'safekeeping_fee_extra_costs': ('incidental_service_fees','overdue_service_fees','disposal_cost_allocation','expense_verification'),
 'safekeeping_paid_general_negligence': ('custody_negligence_compensation',),
 'safekeeping_attachment_priority': ('attachment_effect','document_precedence'),
 'safekeeping_lien_exclusion': ('lien_exclusion',),
}
for _node, _keys in _CONCEPT_BINDINGS.items(): register(_node, _keys)
SAFEKEEPING_REVIEW_CHECKLIST = tuple(replace(c, fact_concepts=_CONCEPT_BINDINGS[c.node_id],
    optional_trigger_patterns=(r'(?:排除|限制|放弃)留置权|不得留置|禁止扣留',) if c.node_id=='safekeeping_lien_exclusion' else (),
    applicable_if='存在排除或限制留置权的特别安排时适用' if c.node_id=='safekeeping_lien_exclusion' else c.applicable_if)
    if c.node_id in _CONCEPT_BINDINGS else c for c in SAFEKEEPING_REVIEW_CHECKLIST)

SAFEKEEPING_REVIEW_CHECKLIST = tuple(replace(c, unless_fact_concepts=('remuneration_determinable',),
    applicable_if='报酬是否有偿或金额、计算方式无法确定时适用')
    if c.node_id=='safekeeping_fee_unclear_default' else c for c in SAFEKEEPING_REVIEW_CHECKLIST)
