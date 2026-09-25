"""Build ordinary ReviewCheckpoint rows and source-verifiable requirements.

These are configurations for the existing semantic coverage pipeline, not a
second review engine. Stable node/element IDs are shared across sibling types.
"""
from dataclasses import replace
from review_v2.house_lease_checklist import _required, _forbidden
from review_v2.lease_semantics import requirement
from review_v2.sale_contract_checklist import SALE_REVIEW_CHECKLIST

PROFILES = {}
CONDITIONS = {}
ADVERSE = {}


def required(prefix, number, node, title, terms, law, elements, *, trigger=(), risk="中", suggestion=""):
    rows = [requirement(node + "_" + str(i), label, *patterns) for i, (label, patterns) in enumerate(elements, 1)]
    PROFILES[node] = rows
    if trigger:
        CONDITIONS[node] = trigger
    row = _required(
        f"{prefix}-{number:02d}-01", node, title, risk, tuple(terms),
        f"需核对{title}的具体安排；文本未覆盖的要素不等于相关法定权利不存在。",
        suggestion or "建议明确：" + "；".join(label for label, _ in elements) + "。",
        law, pass_criteria="全部专项要素均有可定位的合同原文支持。",
        partial_criteria="部分要素有原文支持，其他要素缺失、留有空白或仅待另行协商。",
    )
    return replace(row, domain_owner=prefix.lower(), applicable_if="出现" + "、".join(trigger) + "安排时适用" if trigger else "始终适用")


def forbidden(prefix, number, node, title, terms, law, patterns, suggestion):
    ADVERSE[node] = tuple(patterns)
    return replace(_forbidden(f"{prefix}-{number:02d}-01", node, title, "高", tuple(terms),
        f"发现{title}的直接约定，存在效力或履行风险，需结合适用法律及具体事实核验。", suggestion, law),
        domain_owner=prefix.lower(), polarity="NEGATIVE_CLAUSE_CHECK",
        pass_criteria="全文检索充分且未发现禁止性不利约定；无需合同另行声明不存在该风险。",
        partial_criteria="仅在证据或检索范围不足时需进一步复核，不以缺少禁止性条款判定缺失。",
        legal_consequence_if_missing="未发现禁止性不利约定时不产生该项风险；不要求新增风险条款。")


def common_rows():
    # Keep original node IDs, semantics and legal provenance. Labor dispute
    # resolution is intentionally specialized (mandatory arbitration first).
    return tuple(r for r in SALE_REVIEW_CHECKLIST if r.node_id in {"common_effective_clause", "common_notice_delivery"})
