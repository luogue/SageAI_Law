"""Source-bound finance lease propositions and scenario facts shared by reviews.

Textual asset descriptions never verify physical existence. Remedy elections
are resolved once per contract, not independently by affirmative/negative rules.
"""
import re
from copy import deepcopy

from review_v2.clause_parser import formal_evidence_clauses


def compact(text):
    return re.sub(r"\s+", "", text or "")


def atom(key, text, *patterns):
    return {"element_id": key, "proposition": text, "terms": [text], "finance_lease_patterns": list(patterns)}


PROFILES = {
    "lessee_claim_against_seller": [
        atom("fl_direct_seller_claim", "承租人直接向供货方主张租赁物权利", r"承租人.{0,25}(?:直接|有权).{0,15}(?:供货方|出卖人|卖方).{0,20}(?:主张权利|索赔|行使.{0,10}权利)"),
        atom("fl_lessor_claim_assistance", "出租人协助承租人向供货方维权", r"出租人.{0,30}(?:协助|配合)", r"供货方|出卖人|卖方|索赔|主张权利"),
    ],
    "rent_composition_cost_profit": [
        atom("fl_rent_purchase_cost", "租金以购买价款或购置成本为基础", r"租金", r"购买价款|购买成本|购置成本|购置价款"),
        atom("fl_rent_return", "租金包含融资收益或合理利润", r"租金", r"融资收益率|融资利率|合理利润|融资成本|资金成本"),
    ],
    "lessee_risk_loss_burden": [atom("fl_loss_burden", "租赁物毁损灭失风险由承租人承担", r"租赁物", r"毁损[、，,]?灭失|毁损.{0,4}灭失", r"(?:风险.{0,10}承租人.{0,6}承担|承租人.{0,12}承担.{0,12}(?:风险|毁损))")],
    "three_party_identity": [
        atom("fl_lessor_identity", "出租人主体身份", r"出租人[：:].{2,}"),
        atom("fl_lessee_identity", "承租人主体身份", r"承租人[：:].{2,}"),
        atom("fl_seller_identity", "供货方主体身份", r"(?:供货方|出卖人|卖方)(?:为)?[：:].{2,}"),
    ],
    "lessee_use_pay_obligation": [
        atom("fl_lessee_use", "承租人使用租赁物的权利义务", r"承租人.{0,45}(?:使用|保管).{0,12}租赁物"),
        atom("fl_lessee_pay", "承租人支付租金义务", r"承租人.{0,45}(?:支付|给付|缴纳)租金"),
    ],
    "insurance_and_maintenance": [
        atom("fl_lessee_insurance", "承租人办理租赁物保险", r"承租人", r"(?:购买|投保|办理).{0,30}(?:保险|财产.{0,5}险|损坏险)"),
        atom("fl_lessee_maintenance", "承租人承担维修保养责任", r"(?:承租人.{0,15}(?:负责|承担|应当|应负责).{0,20}(?:维修|保养)|(?:维修|保养).{0,20}承租人.{0,8}(?:负责|承担))"),
    ],
    "end_ownership_agreed": [atom("fl_end_disposition", "租赁期满返还、续租或取得所有权的选择", r"(?:归还|返还).{0,12}出租人|续租|所有权转移给承租人|归承租人|归出租人")],
    "symbolic_price_transfer": [atom("fl_end_purchase", "支付留购或产权转移价款后取得所有权", r"产权转移费|留购价款|名义价款|象征性价款|一元购买", r"所有权.{0,12}(?:转移|归)|取得所有权|购买")],
    "end_return_condition": [atom("fl_return_condition", "返还租赁物时的状态标准", r"归还|返还", r"正常损耗|良好状态|正常使用.{0,8}状态|交接验收")],
    "sale_contract_attachment": [atom("fl_sale_contract_listed", "明确将设备购买或采购买卖合同列为附件", r"(?:设备购买|买卖|采购|购货|购买)合同", r"附件|附表", r"作为|均为|列为|包括|如下|清单|为本合同")],
    "invalid_asset_ownership": [atom("fl_invalid_return", "合同无效后的租赁物归属", r"(?:合同|融资租赁).{0,8}无效", r"租赁物.{0,15}(?:归属|返还|归)|返还出租人")],
    "lessee_refusal_conditions": [atom("fl_refusal", "迟延交付或严重不符合约定时的拒绝受领", r"拒绝受领|拒收", r"迟延|严重不符合|目的", r"可|有权")],
    "lessor_defect_warranty_exemption": [atom("fl_defect_default", "出租人原则上不承担质量瑕疵责任", r"出租人", r"不承担|免责", r"质量|瑕疵|使用目的")],
    "lessor_defect_exception": [atom("fl_defect_exception", "出租人干预选择等情形下的瑕疵责任例外", r"依赖.{0,8}技能|干预|决定选择|擅自变更", r"出租人", r"承担|责任|除外")],
    "sale_contract_failure_handling": [atom("fl_sale_failure", "买卖合同障碍导致租赁目的不能实现时的处理", r"(?:买卖|购买|购货)合同", r"无效|撤销|解除|无法交付", r"解除|退款|赔偿|损失")],
    "no_fault_loss_termination": [atom("fl_no_fault_loss", "不可归责且不能修复替代的毁损灭失处理", r"不可归责", r"不能修复|无法替代|替代物", r"解除|补偿|结算")],
    "termination_loss_calculation": [atom("fl_termination_net_loss", "收回租赁物后以未付债务扣减租赁物价值清算", r"租金|债务", r"减去|扣除|扣减|抵扣", r"租赁物.{0,10}价值|处置价款")],
    "value_settlement_rule": [atom("fl_surplus_return", "收回价值超过债务时返还差额", r"租赁物.{0,15}价值|处置价款", r"超过|高于|剩余", r"返还|退还")],
    "asset_valuation_method": [atom("fl_valuation", "收回租赁物的客观估值方法", r"租赁物", r"评估|拍卖|市场价|协商价|公开处置价")],
    "registration_attachment": [atom("fl_registration_document", "登记证明文件作为附件保存", r"登记证明|登记凭证|登记查询结果", r"附件|保存|提供")],
    "technical_delivery_attachment": [
        atom("fl_technical_document", "技术资料作为附件保存", r"技术规格|说明书|合格证|技术资料", r"附件|保存|提供"),
        atom("fl_delivery_document", "交付验收文件作为附件", r"验收文件|验收单|验收记录|交付单", r"附件|保存|提供"),
    ],
    "rent_registration_insurance_attachment": [
        atom("fl_rent_document", "租金支付表作为附件", r"租金支付表|租金测算表", r"附件"),
        atom("fl_registration_document", "登记证明文件作为附件保存", r"登记证明|登记凭证|登记查询结果", r"附件|保存|提供"),
        atom("fl_insurance_document", "保险凭证作为附件保存", r"保单|保险凭证|保险权益批单", r"附件|保存|提供"),
    ],
    "paid_most_rent_protection": [atom("fl_paid_rent_surplus", "已付大部分租金情形下收回租赁物的差额返还", r"大部分租金|多数租金", r"差额|超过", r"返还|退还")],
}
DEFAULTS = {
    "invalid_asset_ownership": "第760条", "lessee_refusal_conditions": "第740条",
    "lessor_defect_warranty_exemption": "第747条", "lessor_defect_exception": "第747条",
    "sale_contract_failure_handling": "第754条、第755条", "no_fault_loss_termination": "第754条、第756条",
}
SETTLEMENT = {"termination_loss_calculation", "value_settlement_rule", "asset_valuation_method", "paid_most_rent_protection"}
REMEDIES = {"rent_remedy_choice", "request_both_remedies"}
REALITY = {"real_asset_existence", "fake_asset_invalid"}


class FinanceLeaseFacts:
    def __init__(self, clauses):
        self.clauses = list(formal_evidence_clauses(clauses))
        self.aliases, self.parties = {}, {}
        for c in self.clauses:
            for line in c.text.splitlines():
                m = re.match(r"\s*(出租[人方]|承租[人方]|供货方|出卖人)(?:（[^）]*）)?[：:]\s*([^（\n。]+)(?:（[^）]*?(甲方|乙方|丙方)[^）]*）)?", line)
                if m:
                    role = "出租人" if m[1].startswith("出租") else "承租人" if m[1].startswith("承租") else "供货方"
                    self.parties[role] = m[2].strip()
                    if m[3]:
                        self.aliases[m[3]] = role
        self.rows = []
        for c in self.clauses:
            for quote in re.split(r"(?<=[。；;])|\n", c.text):
                if not quote.strip():
                    continue
                quote = quote.strip()
                normalized = compact(quote).replace("出租方", "出租人").replace("承租方", "承租人").replace("租赁物件", "租赁物").replace("租赁财产", "租赁物")
                for alias, role in self.aliases.items():
                    normalized = normalized.replace(alias, role)
                self.rows.append({"clause_id": c.clause_id, "quote": quote, "text": quote, "location": c.location,
                                  "section_type": c.section_type, "block_type": c.block_type, "source_type": "CONTRACT_TEXT",
                                  "evidence_id": f"{c.clause_id}-FL-{len(self.rows)+1}", "finance_lease_normalized": normalized,
                                  "entailment_status": "SUPPORTS", "semantic_score": 1.0})
        self.text = "\n".join(r["finance_lease_normalized"] for r in self.rows)
        positive_back = self.search(r"(?<!非)(?<!不属于)售后回租|自有.{0,12}(?:出售|出卖).{0,25}租回|承租人.{0,10}出卖人.{0,8}(?:同一|相同)")
        positive_back = [r for r in positive_back if not re.search(r"如|若|不属于|不是|非售后", r["finance_lease_normalized"])]
        same = bool(self.parties.get("承租人") and self.parties.get("供货方") == self.parties["承租人"])
        self.sale_leaseback = bool(positive_back or same)
        self.sale_leaseback_evidence = positive_back or (self.search(r"承租人[：:]|供货方[：:]") if same else [])
        self.remedy_rent = self.search(r"(?:要求|请求|支付|付清|主张).{0,20}(?:全部|所有).{0,10}(?:租金)")
        self.remedy_return = self.search(r"(?:收回|取回)租赁物")
        self.election = self.search(r"择一|二者选一|不得.{0,15}同时.{0,25}(?:租金|救济)|(?:请求|要求).{0,15}全部.{0,8}租金.{0,10}(?:或|或者).{0,20}(?:解除|收回)")
        self.remedy_context = self.search(r"采取.{0,20}(?:措施|第)|不.{0,8}免除.{0,20}义务|同时.{0,30}(?:收回|租金)")
        self.double_remedy_risk = bool(self.remedy_rent and self.remedy_return and not self.election)
        self.fake = [r for r in self.search(r"虚构租赁物|租赁物不存在|无真实设备|无真实租赁物|空转融资")
                     if not re.search(r"不得|禁止|不存在虚构|没有虚构|保证|承诺|如|若", r["finance_lease_normalized"])]
        self.asset_structure = {key: self.search(pattern) for key, pattern in {
            "model": r"型号[：:]?[^，；。]{2,}", "quantity": r"数量[：:]?\d+", "seller": r"供货方(?:为)?[：:].{2,}",
            "price": r"价款|单价|总价|租赁本金", "description": r"租赁物.{0,12}[：:]|设备名称|租赁物名称",
        }.items()}

    def search(self, pattern):
        return [deepcopy(r) for r in self.rows if re.search(pattern, r["finance_lease_normalized"])]

    def evidence(self, node):
        result = []
        for source in self.rows:
            ids = [e["element_id"] for e in PROFILES.get(node, []) if supports(e, source)]
            if node in {"end_ownership_agreed", "symbolic_price_transfer", "end_return_condition"}:
                # Expiry and default return must not prove one another. Require
                # expiry in the clause or its owning article's heading/body.
                article = re.match(r"第[^条]+条", source["location"])
                context = "".join(c.text for c in self.clauses if article and c.location.startswith(article[0]) and c.level <= 1)
                if not re.search(r"期满|届满|到期", context + source["quote"]):
                    ids = []
            if ids:
                result.append({**deepcopy(source), "supports_element_ids": ids})
        return result

    def applicability(self, node):
        active, reason = True, "融资租赁一般审查事项。"
        evidence = []
        if node.startswith("sale_leaseback_"):
            active, evidence = self.sale_leaseback, self.sale_leaseback_evidence
            reason = "存在售后回租事实或出卖人与承租人主体同一。" if active else "未发现售后回租事实或出卖人与承租人主体同一；不要求直租合同补写回租条款。"
        elif node == "technical_delivery_attachment":
            evidence = [r for r in self.search(r"技术许可|技术开发|技术成果|源代码|设计图纸|工艺包|技术资料.{0,12}(?:交付|提供)")
                        if not re.search(r"不涉及|不包含|无需|不提供|如需|若涉及", r["finance_lease_normalized"])]
            active = bool(evidence)
            reason = "存在独立技术许可、开发或技术成果交付安排。" if active else "普通设备租赁未发现独立技术许可、开发或复杂技术成果交付事实，不要求另行设置技术资料附件。"
        elif node == "symbolic_price_transfer":
            evidence = self.search(r"产权转移费|留购价款|象征性价款|名义价款|一元购买")
            active, reason = bool(evidence), "仅在存在期满留购或产权转移价款安排时适用。"
        elif node == "end_return_condition":
            active, reason = bool(self.evidence(node) or self.search(r"期满.{0,35}(?:返还|归还)|(?:返还|归还).{0,10}出租人")), "仅在合同存在期满返还安排时适用。"
        elif node in SETTLEMENT:
            active, evidence = bool(self.remedy_return), self.remedy_return
            reason = "仅在合同存在出租人收回租赁物的救济安排时适用。"
        return {"status": "APPLICABLE" if active else "NOT_APPLICABLE", "applicable": active, "reason": reason,
                "source_evidence": evidence, "searched_clause_ids": [c.clause_id for c in self.clauses], "confidence": "high"}


def supports(element, evidence):
    text = evidence.get("finance_lease_normalized", "")
    if re.search(r"不得.{0,8}主张权利|无权.{0,8}索赔|不(?:承担|负责).{0,8}(?:维修|保养)", text):
        return False
    return bool(text) and all(re.search(p, text) for p in element.get("finance_lease_patterns", []))


def apply(items, facts):
    for item in items:
        if item.coverage_status in {"不适用", "INSUFFICIENT_CONTEXT"}:
            continue
        node = item.node_id
        if node in PROFILES:
            evidence = facts.evidence(node)
            supported = {key for e in evidence for key in e["supports_element_ids"]}
            complete = all(e["element_id"] in supported for e in PROFILES[node])
            item.evidence_clauses, item.evidence_location = evidence, "；".join(dict.fromkeys(e["location"] for e in evidence))
            item.coverage_status = "通过" if complete else "部分覆盖" if evidence else "缺失"
            item.status, item.issue_type = ("已覆盖", "通过") if complete else ("部分覆盖", "条款缺陷") if evidence else ("缺失或不明确", "完全缺失")
            item.judge_source = "rule_fallback"
            item.needs_manual_review = False
            item.reasoning_summary = ("原文直接覆盖：" if complete else "未完整覆盖：") + "、".join(e["proposition"] for e in PROFILES[node] if complete or e["element_id"] not in supported) + "。"
            item.risk_point_description = item.reasoning_summary
            item.decision_trace["finance_lease_binding"] = {"evidence_ids": [e["evidence_id"] for e in evidence]}
        override_pattern = {
            "lessee_refusal_conditions": r"不得拒收|不得拒绝受领",
            "lessor_defect_warranty_exemption": r"出租人.{0,20}(?:任何|一切|无论).{0,20}(?:免责|不承担)|无论.{0,25}出租人.{0,20}不承担",
            "lessor_defect_exception": r"出租人.{0,20}(?:任何|一切|无论).{0,20}(?:免责|不承担)|无论.{0,25}出租人.{0,20}不承担",
        }.get(node)
        overrides = facts.search(override_pattern) if override_pattern else []
        if node in DEFAULTS and overrides:
            item.decision_trace["finance_lease_boundary_override"] = overrides
            item.coverage_status, item.status, item.issue_type = "部分覆盖", "责任边界待明确", "条款缺陷"
            item.evidence_clauses = overrides
            item.reasoning_summary = item.risk_point_description = "合同存在排除拒绝受领或概括免除出租人责任的表述，需保留法定例外并明确责任边界。"
        if node in DEFAULTS and item.coverage_status == "缺失" and not overrides:
            item.decision_trace["statutory_default_resolution"] = {
                "status": "CLEAR_DEFAULT", "authority": "《民法典》" + DEFAULTS[node],
                "fully_supplements_contract_gap": True, "residual_gap": []}
            item.decision_trace["finance_lease_non_contractual"] = {
                "nature": "LEGAL_REMINDER", "reason": f"合同未复述该项规则，适用《民法典》{DEFAULTS[node]}的法定规则；没有直接改变该责任边界的文本证据，不作为重大条款缺失。",
                "authority": "《民法典》" + DEFAULTS[node], "external_fact_verified": False}
        if node in REALITY:
            item.decision_trace["finance_lease_asset_reality"] = {"text_structure_complete": all(facts.asset_structure.values()),
                "external_fact_status": "NOT_VERIFIED", "structure_evidence": facts.asset_structure, "risk_evidence": facts.fake}
            if not facts.fake:
                item.decision_trace["finance_lease_non_contractual"] = {"nature": "EXTERNAL_FACT_VERIFICATION",
                    "reason": ("文本已列明租赁物型号、数量、供货方及价款等交易结构。" if all(facts.asset_structure.values()) else "文本中的租赁物资料尚需补充或核验。") + "实际租赁物是否存在、权属及交付情况属于合同外事实，不能仅凭合同声明确认；文本未发现虚构安排。"}
            else:
                item.evidence_clauses = deepcopy(facts.fake)
                item.coverage_status = item.issue_type = "风险条款"
                item.status, item.risk_level = "发现虚构租赁物线索", "高"
                item.reasoning_summary = item.risk_point_description = "合同出现租赁物不存在或虚构安排的直接线索，需核验实际交易，存在效力风险。"
                item.decision_trace["finding_parent_group"] = "finance_lease_asset_reality"
        if node in SETTLEMENT:
            item.decision_trace["finance_lease_recovery_exposure"] = {
                "double_recovery": facts.double_remedy_risk,
                "evidence": facts.remedy_rent + facts.remedy_return}
            item.decision_trace["finding_parent_group"] = "finance_lease_recovery_settlement"
            item.decision_trace["risk_category"] = "收回租赁物后的净额清算"
        if node in REMEDIES:
            evidence = {r["evidence_id"]: r for r in facts.remedy_rent + facts.remedy_return + facts.remedy_context + facts.election}
            item.decision_trace["finance_lease_shared_remedy"] = {"fact_id": "finance_lease.remedy_election", "potential_double_recovery": facts.double_remedy_risk,
                "evidence": list(evidence.values()), "election_evidence": facts.election}
            item.decision_trace["finding_parent_group"] = "finance_lease_remedy_election"
            item.decision_trace["risk_category"] = "救济方式及重复受偿"
            if not facts.double_remedy_risk:
                item.coverage_status, item.status, item.issue_type = "通过", "已明确救济边界" if facts.election else "文本未发现双重救济", "通过"
                item.evidence_clauses = deepcopy(facts.election)
                item.reasoning_summary = item.risk_point_description = "合同约定互斥救济择一。" if facts.election else "文本未同时授予全部租金请求权和收回租赁物权利，未发现双重救济安排。"


def finalize_remedies(items):
    """Materialize the shared adverse fact before risk dimensions/aggregation."""
    for item in items:
        exposure = item.decision_trace.get("finance_lease_recovery_exposure") or {}
        if exposure.get("double_recovery") and item.coverage_status in {"缺失", "部分覆盖"}:
            item.risk_level = "高"
        boundary = item.decision_trace.get("finance_lease_boundary_override")
        if boundary:
            item.coverage_status, item.status, item.issue_type = "部分覆盖", "责任边界待明确", "条款缺陷"
            item.evidence_clauses = deepcopy(boundary)
        fact = item.decision_trace.get("finance_lease_shared_remedy") or {}
        if not fact.get("potential_double_recovery"):
            continue
        item.coverage_status, item.status, item.issue_type = "风险条款", "存在双重救济歧义", "风险条款"
        item.risk_level, item.needs_manual_review = "高", False
        item.reasoning_summary = item.risk_point_description = "合同同时列有要求全部租金与收回租赁物的救济，未明确互斥择一，可能允许同时主张并造成重复受偿。"
        item.legal_consequence_if_missing = "应明确全部租金请求与解除收回的选择关系；收回后的赔偿应扣减租赁物价值，避免重复受偿。"
        item.suggested_clause_example = "同一违约下，出租人应在请求支付全部未付租金与解除合同收回租赁物之间择一；选择收回的，应以未付租金及合理费用扣减租赁物价值进行清算。"
        item.evidence_clauses = [dict(deepcopy(e), supporting_element_ids=["fl_remedy_election"], supports_element_ids=["fl_remedy_election"], support_type="DIRECT") for e in fact["evidence"]]
        item.evidence_location = "；".join(dict.fromkeys(e["location"] for e in item.evidence_clauses))
        item.coverage_elements = [{"element_id": "fl_remedy_election", "proposition": "全部租金请求与收回租赁物并列且未明确择一，存在重复受偿歧义", "status": "ADVERSE", "entailment": "SUPPORTS", "risk_relevant": True,
            "evidence_ids": [e["evidence_id"] for e in item.evidence_clauses], "source_clause_ids": list(dict.fromkeys(e["clause_id"] for e in item.evidence_clauses)),
            "supporting_evidence": [{"clause_id": e["clause_id"], "quote": e["quote"]} for e in item.evidence_clauses]}]
