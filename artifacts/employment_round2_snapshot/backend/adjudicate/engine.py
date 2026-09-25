"""
租赁押金纠纷裁判引擎
输入：facts (dict)，输出：判决结果 + 触发的补丁清单
"""

from datetime import datetime, date
from typing import Dict, Any, List, Optional


def calculate_loss(facts: dict) -> float:
    """
    计算实际损失（占位函数）
    实际对接时应接入维修报价 / 空置期租金计算 / 市场公允价值评估
    """
    loss = facts.get("repair_quote", 0.0)

    vacancy_days = facts.get("vacancy_days", 0)
    daily_rent = facts.get("daily_rent", 0.0)
    if vacancy_days > 0 and daily_rent > 0:
        loss += vacancy_days * daily_rent

    return loss


def parse_date(value) -> Optional[date]:
    """将字符串或 date 对象统一转为 date"""
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"):
            try:
                return datetime.strptime(value.strip(), fmt).date()
            except ValueError:
                continue
    return None


def years_between(start: date, end: date) -> float:
    """计算两个日期相差的年数（近似，用于 3 年 / 1 年判断）"""
    return (end - start).days / 365.25


def adjudicate_deposit(facts: dict) -> Dict[str, Any]:
    """
    租赁押金纠纷裁判引擎

    :param facts: 事实对象
    :return: {"result": str, "triggered_patches": list[str], "path": list[str]}
    """
    triggered_patches: List[str] = []
    decision_path: List[str] = []
    today = date.today()
    contract_end_date = parse_date(facts.get("contract_end_date"))

    # ===== 阶段 0：入口防火墙 =====

    if facts.get("has_third_party", False):
        triggered_patches.append("P4-侵权第三方分流")
        return {
            "result": "直接分流至侵权责任轨道，本合同树终止",
            "triggered_patches": triggered_patches,
            "path": ["阶段0-入口防火墙", "P4-侵权第三方分流"],
        }

    if contract_end_date and years_between(contract_end_date, today) > 3:
        triggered_patches.append("P5-诉讼时效已过")
        return {
            "result": "诉讼时效已过，驳回请求",
            "triggered_patches": triggered_patches,
            "path": ["阶段0-入口防火墙", "P5-诉讼时效已过（>3年）"],
        }

    # ===== 阶段 1：主决策树 =====

    # 节点 A：合同效力审查
    if facts.get("contract_valid") is False:
        triggered_patches.append("基础规则-合同无效")
        return {
            "result": "判决：押金全额返还",
            "triggered_patches": triggered_patches,
            "path": ["阶段1-主决策树", "A-合同效力审查", "合同无效→全额返还"],
        }

    # 节点 A-挂载：补丁 1
    clauses = list(facts.get("contract_clauses", []))
    if isinstance(clauses, list):
        clauses = [str(c) for c in clauses]
    if "任何损坏均由租客赔偿" in clauses:
        triggered_patches.append("P1-格式条款无效")
        decision_path.append("A-格式条款审查→P1触发")

    # 节点 B：期限审查
    if facts.get("is_early_termination", False):
        contract = facts.get("contract", {}) if isinstance(facts.get("contract"), dict) else {}
        if contract.get("has_early_termination_clause"):
            landlord_know_date = parse_date(facts.get("landlord_know_date"))
            if landlord_know_date and years_between(landlord_know_date, today) > 1:
                triggered_patches.append("P6-解除权消灭")
                return {
                    "result": "判决：解除权消灭，房东无权扣款",
                    "triggered_patches": triggered_patches,
                    "path": ["阶段1-主决策树", "B-期限审查", "提前退租", "P6-解除权消灭（>1年）"],
                }
            else:
                return {
                    "result": "判决：提前退租按约定处理，押金不退还",
                    "triggered_patches": triggered_patches,
                    "path": ["阶段1-主决策树", "B-期限审查", "提前退租", "有约定→不退押金"],
                }

    # 节点 C：损坏事实
    if facts.get("has_damage") is False:
        return {
            "result": "判决：无损坏，押金全额返还",
            "triggered_patches": triggered_patches,
            "path": ["阶段1-主决策树", "C-损坏事实审查", "无损坏→全额返还"],
        }

    # 补丁 7：装修处置
    if facts.get("damage_item") == "decoration":
        triggered_patches.append("P7-装修处置分支")
        return {
            "result": "启动装修处置分支：需查实是否经出租人同意后，决定补偿或恢复原状",
            "triggered_patches": triggered_patches,
            "path": ["阶段1-主决策树", "D-损坏原因分类", "P7-装修加装物分支"],
        }

    # 补丁 3：举证责任
    if facts.get("evidence_can_prove_cause") is False:
        if facts.get("damage_claimed_by") == "landlord":
            triggered_patches.append("P3-举证不能")
            return {
                "result": "判决：举证不能，押金全额返还",
                "triggered_patches": triggered_patches,
                "path": ["阶段1-主决策树", "D-损坏原因分类", "P3-举证不能→全额返还"],
            }

    # 原因 A：自然损耗
    if facts.get("damage_reason") == "natural_wear":
        return {
            "result": "判决：自然损耗，出租人免责，押金全额返还",
            "triggered_patches": triggered_patches,
            "path": ["阶段1-主决策树", "D-损坏原因分类", "自然损耗→全额返还"],
        }

    # 原因 B：承租人过错
    if facts.get("damage_reason") == "tenant_fault":
        actual_loss = calculate_loss(facts)
        max_allowed = actual_loss * 1.3
        agreed = float(facts.get("agreed_deduction", 0))

        if agreed > max_allowed:
            final_deduction = actual_loss
            triggered_patches.append(f"P2-违约金调减（约定{agreed}→实际{final_deduction:.2f}）")
        else:
            final_deduction = agreed

        if facts.get("tenant_has_repair_claim", False):
            triggered_patches.append("P8-同时履行抗辩主张")

        return {
            "result": f"判决：承租人过错，扣除 {final_deduction:.2f} 元后返还余额",
            "triggered_patches": triggered_patches,
            "path": ["阶段1-主决策树", "D-损坏原因分类", "承租人过错→赔偿扣除"],
        }

    # 节点 E：隐性补丁
    if facts.get("notified_at_check_in") is True and facts.get("landlord_remained_silent") is True:
        triggered_patches.append("隐性补丁-默示同意/权利滥用")
        return {
            "result": "判决：入住时已知悉且未提异议，不得事后追责，押金全额返还",
            "triggered_patches": triggered_patches,
            "path": ["阶段1-主决策树", "E-隐性补丁", "默示同意/权利滥用→全额返还"],
        }

    return {
        "result": "无法归类：请补充事实信息",
        "triggered_patches": triggered_patches,
        "path": ["阶段1-主决策树", "兜底-信息不足"],
    }
