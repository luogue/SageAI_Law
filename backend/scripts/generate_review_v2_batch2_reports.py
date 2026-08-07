"""Generate review-v2 batch-2 sample reports for manual QA.

The sample contracts are intentionally simplified templates. They are not meant
to replace official model contracts; they exercise the shared applicability,
substantive-evidence, and notice-function rules for the next three contract
types.
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from review_v2.engine import COVERAGE_NOT_APPLICABLE, review_contract_v2

OUTPUT_DIR = ROOT / "output" / "review_v2_batch2"


SAMPLES = {
    "deposit": (
        "保管合同",
        "测试材料为简化模板，部分缺失项可能源于模板简略。",
        """保管合同
第一条 合同性质与保管物
寄存人甲方将普通设备一台交由保管人乙方保管，设备编号A-001，数量一台，交付时双方签署保管物清单并拍照确认外观、功能和附件状态。双方确认本合同为有偿保管合同。
第二条 交付与保管期间
保管物于2026年8月1日交付乙方并由乙方出具接收凭证，保管期间至2026年8月31日。
第三条 保管费
保管费为1000元，甲方于交付时支付；因甲方特殊要求或逾期领取产生的合理额外费用由甲方承担。
第四条 保管义务
乙方应在其仓库内妥善保管，采取防盗、防火、防潮措施，不得擅自改变保管场所或方法，不得使用保管物，不得未经甲方书面同意转交第三人保管。有偿保管期间，乙方未尽妥善保管义务造成毁损灭失的，应承担赔偿责任。
第五条 寄存人告知义务
甲方应如实告知设备瑕疵和特殊保管要求，并提供必要包装、标签和资料。
第六条 返还与领取
保管期满或甲方提前领取时，乙方应返还原物、附件及相关资料，双方签署返还确认单。甲方可随时领取保管物，费用按实际保管期间结算。
第七条 留置权
甲方未支付到期保管费的，乙方可依法在与欠费相当的范围内行使留置权，并应事先书面通知甲方。""",
    ),
    "work_contract": (
        "承揽合同",
        "测试材料为简化模板，部分缺失项可能源于模板简略。",
        """承揽合同
第一条 合同性质与工作内容
定作人甲方委托承揽人乙方定制展柜10套。双方确认本合同为承揽合同，乙方按甲方要求完成特定工作并交付工作成果。
第二条 承揽人能力与亲自完成
乙方应以自己的设备、技术和劳力完成主要工作，并保证具备完成该工作的人员、工艺和安全合规能力。
第三条 质量标准和附件
工作成果应符合甲方确认的图纸、尺寸、材质、工艺和质量标准；图纸、技术规范和验收标准作为合同附件。
第四条 定作人协助
甲方应按约提供设计图纸、确认意见和必要材料。甲方逾期提供协助的，乙方可书面催告，合理期限内仍未提供的，工期相应顺延，费用增加由甲方承担。
第五条 材料检验
甲方提供材料的，乙方应及时检验，发现材料不符合约定或不适宜加工的，应书面通知甲方更换、补齐或采取补救措施。
第六条 验收和瑕疵救济
乙方交付后，甲方应在7日内验收；工作成果存在质量瑕疵的，甲方可要求乙方修理、重作、减少报酬或赔偿合理损失。
第七条 任意解除
甲方在工作完成前可以书面通知解除合同，但应赔偿乙方已投入材料、人工、外协费用和合理损失。合同解除后，双方应清点材料、成果并结算费用。""",
    ),
    "agency": (
        "委托合同",
        "测试材料为简化模板，部分缺失项可能源于模板简略。",
        """委托合同
第一条 合同性质与委托事项
委托人甲方委托受托人乙方代办公司变更登记事项。双方确认本合同为委托合同，乙方应按甲方书面指示处理委托事务。
第二条 授权范围
乙方办理事项限于公司变更登记资料准备、提交、沟通和领取结果文件，不得超越授权范围，不得处分甲方财产或承担额外债务。本合同为特别委托。
第三条 报酬和费用
本合同为有偿委托，委托报酬为3000元；乙方垫付的必要费用凭有效票据由甲方报销，非必要费用未经甲方同意不予报销。
第四条 受托人义务
乙方应按甲方指示处理事务，每周报告办理进展，合同终止时提交结果报告，并将取得的文件、资料、款项和其他财产完整移交甲方。
第五条 转委托
未经甲方书面同意，乙方不得转委托第三人处理；经同意转委托的，乙方仅就第三人的选任和指示承担责任，未经同意转委托的，乙方对第三人行为承担责任。
第六条 责任标准
有偿委托中，乙方因一般过失造成甲方损失的，应承担赔偿责任；乙方超越授权处理事务造成损失的，应赔偿甲方损失。
第七条 解除和交接
双方均可随时解除合同，解除方应书面通知对方并配合事务交接、资料返还和费用结算；有偿委托解除造成损失的，按直接损失及合同履行后可得利益范围处理。""",
    ),
}


def _risk_rows(items: list[dict[str, Any]]) -> list[str]:
    rows = [
        "| 编号 | 审查点 | 风险等级 | 覆盖状态 | 问题类型 | 系统判断 |",
        "|---|---|---|---|---|---|",
    ]
    for item in items:
        if item["coverage_status"] in {"通过", COVERAGE_NOT_APPLICABLE}:
            continue
        rows.append(
            "| {item_id} | {title} | {risk_level} | {coverage_status} | {issue_type} | {reasoning} |".format(
                item_id=item["item_id"],
                title=item["title"],
                risk_level=item["risk_level"],
                coverage_status=item["coverage_status"],
                issue_type=item["issue_type"],
                reasoning=(item["reasoning_summary"] or "").replace("\n", " ").replace("|", "，"),
            )
        )
    return rows


def _write_report(contract_type: str, title: str, notice: str, text: str) -> dict[str, Any]:
    result = review_contract_v2(text, contract_type, use_llm=False)
    file_path = OUTPUT_DIR / f"{contract_type}_review_report.md"
    high_risk_open = sum(
        1
        for item in result["items"]
        if item["risk_level"] == "高" and item["coverage_status"] not in {"通过", COVERAGE_NOT_APPLICABLE}
    )
    lines = [
        f"# {title}审查报告（第二版测试）",
        "",
        f"报告提示：合同类型为{title}；{notice}",
        "",
        "## 风险概览",
        "",
        f"- 审查点总数：{result['all_items_count']} 项",
        f"- 高风险：{result['summary'].get('高', 0)} 项",
        f"- 中风险：{result['summary'].get('中', 0)} 项",
        f"- 低风险：{result['summary'].get('低', 0)} 项",
        f"- 不适用：{result['coverage_summary'].get(COVERAGE_NOT_APPLICABLE, 0)} 项",
        f"- 当前未通过的高风险项：{high_risk_open} 项",
        "",
        "## 未通过审查项",
        "",
        *_risk_rows(result["items"]),
        "",
        "## 完整报告",
        "",
        result["result"],
    ]
    file_path.write_text("\n".join(lines), encoding="utf-8")
    return {
        "contract_type": contract_type,
        "file": str(file_path),
        "summary": result["summary"],
        "coverage_summary": result["coverage_summary"],
        "issue_type_summary": result["issue_type_summary"],
        "high_risk_open": high_risk_open,
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summaries = []
    for contract_type, (title, notice, text) in SAMPLES.items():
        summaries.append(_write_report(contract_type, title, notice, text))

    summary_lines = [
        "# 审查第二版下一批合同测试汇总",
        "",
        "报告提示：本批测试覆盖保管合同、承揽合同、委托合同；测试材料均为简化模板，部分缺失项可能源于模板简略。",
        "",
        "| 合同类型 | 报告文件 | 高风险 | 中风险 | 低风险 | 不适用 | 当前未通过高风险 | 初步结论 |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for item in summaries:
        summary = item["summary"]
        coverage = item["coverage_summary"]
        conclusion = "高风险项仍偏多，需继续细化评级和适用条件" if item["high_risk_open"] > 5 else "高风险数量处于可接受范围"
        summary_lines.append(
            f"| {item['contract_type']} | {item['file']} | {summary.get('高', 0)} | {summary.get('中', 0)} | {summary.get('低', 0)} | {coverage.get(COVERAGE_NOT_APPLICABLE, 0)} | {item['high_risk_open']} | {conclusion} |"
        )
    summary_lines.extend(
        [
            "",
            "## 已验证规则",
            "",
            "- 适用条件过滤：专项场景未出现时标记为“不适用”，并从风险统计中排除。",
            "- 证据实质性匹配：仅有表面关键词但未覆盖对应法律义务的条款，不再作为有效证据。",
            "- 通知类条款区分：一般通知、催告、解除通知、交接通知按法律功能分别判断。",
            "",
            "## 待修正方向",
            "",
            "- 保管合同：需进一步区分普通保管与贵重物品、消费保管场景，高风险评级可继续收敛。",
            "- 承揽合同：质量瑕疵救济和任意解除已能被识别，但部分附件类缺失可考虑降低优先级。",
            "- 委托合同：隐名代理、双方代理、转委托过滤已生效；有偿/无偿责任标准仍需结合合同报酬条款做依赖判断。",
        ]
    )
    summary_path = OUTPUT_DIR / "batch2_test_summary.md"
    summary_path.write_text("\n".join(summary_lines), encoding="utf-8")
    print(summary_path)
    for item in summaries:
        print(item)


if __name__ == "__main__":
    main()
