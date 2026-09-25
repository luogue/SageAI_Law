"""Construction subtype and canonical party roles for applicability."""
from __future__ import annotations
import re

def classify(text: str) -> dict:
    sample = (text or "")[:2500]
    if re.search(r"(?:建设工程|工程|施工)施工?劳务分包合同|建筑劳务分包合同|劳务作业", sample):
        return {"subtype": "LABOR_SUBCONTRACT", "party_roles": {"甲方": "UPSTREAM_CONTRACTOR_OR_LABOR_CLIENT", "乙方": "LABOR_SUBCONTRACTOR"}}
    if re.search(r"专业分包合同|专业工程分包", sample):
        return {"subtype": "SPECIALTY_SUBCONTRACT", "party_roles": {"甲方": "UPSTREAM_CONTRACTOR", "乙方": "SPECIALTY_SUBCONTRACTOR"}}
    if re.search(r"EPC|设计[、-]?采购[、-]?施工.*总承包|工程总承包", sample):
        return {"subtype": "EPC", "party_roles": {"甲方": "OWNER_OR_EMPLOYER", "乙方": "EPC_CONTRACTOR"}}
    if re.search(r"勘察合同", sample):
        return {"subtype": "SURVEY", "party_roles": {"甲方": "OWNER_OR_EMPLOYER", "乙方": "SURVEY_CONTRACTOR"}}
    if re.search(r"设计合同", sample):
        return {"subtype": "DESIGN", "party_roles": {"甲方": "OWNER_OR_EMPLOYER", "乙方": "DESIGN_CONTRACTOR"}}
    return {"subtype": "GENERAL_CONSTRUCTION", "party_roles": {"甲方": "OWNER_OR_EMPLOYER", "乙方": "GENERAL_CONTRACTOR"}}

LABOR_OWNER_ONLY_NODES = {"construction_license_and_approval", "employer_permit_assistance", "employer_material_fund_site_obligation", "priority_payment_right", "priority_claim_18_months", "priority_no_waiver_worker_interest", "priority_scope_quality_condition", "completion_date_identification"}

def applicability(text: str, node_id: str):
    if classify(text)["subtype"] == "LABOR_SUBCONTRACT" and node_id == "subcontract_to_qualified_party":
        return False, "本项检查专业分包的资质及发包人同意条件；当前为劳务分包，乙方向下转包/再分包的限制不能证明甲方向乙方的当前分包已获上游授权。劳务合规及主体资格由对应专项审查。"
    if classify(text)["subtype"] == "LABOR_SUBCONTRACT" and node_id in LABOR_OWNER_ONLY_NODES:
        return False, "劳务分包合同不直接适用建设单位—总承包人专属规则。"
    return None
