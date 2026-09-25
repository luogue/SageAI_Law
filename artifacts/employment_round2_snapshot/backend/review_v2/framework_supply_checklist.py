"""Review definitions specific to framework and recurring goods supply."""

from __future__ import annotations

from dataclasses import replace
from typing import Tuple

from review_v2.house_lease_checklist import ReviewCheckpoint, _required


def _framework(
    item_id: str,
    node_id: str,
    title: str,
    risk_level: str,
    terms: tuple[str, ...],
    risk: str,
    suggestion: str,
) -> ReviewCheckpoint:
    return replace(
        _required(item_id, node_id, title, risk_level, terms, risk, suggestion, "《民法典》第509条、第595条"),
        allowed_families=("SALE",),
        allowed_subject_matters=("GOODS",),
        allowed_subtypes=("FRAMEWORK_SUPPLY",),
        domain_owner="sale/goods/framework_supply",
        material_group="FRAMEWORK_SUPPLY",
    )


FRAMEWORK_SUPPLY_REVIEW_CHECKLIST: Tuple[ReviewCheckpoint, ...] = (
    _framework("FS-01", "framework_master_order_relationship", "主协议与订单关系", "高", ("长期供货", "采购订单", "共同构成"), "主协议与后续订单的关系不明，单批交易如何成立及适用哪些文件容易争议。", "主协议约定长期合作的一般规则；每批交易以有效订单及其确认成立，订单与主协议共同约束该批履行。"),
    _framework("FS-02", "framework_order_formation_confirmation", "订单形成与确认", "高", ("正式采购订单", "确认订单", "具有约束力"), "未明确订单发出、确认和生效程序，供应义务可能无法确定。", "采购订单应列明产品、数量和交期，经供应方书面确认后对双方具有约束力。"),
    _framework("FS-03", "framework_dynamic_quantity", "动态采购数量", "高", ("实际生产需求", "实际下达", "实际供货数量"), "框架关系中的动态数量机制不明，可能把预计需求误当固定采购义务。", "各批型号、数量和批次以经确认的订单为准，并按实际有效单据结算。"),
    _framework("FS-04", "framework_minimum_purchase", "最低采购承诺", "中", ("最低采购数量", "最低采购责任", "保底采购"), "最低采购承诺有无不清，可能产生保底采购或闲置产能索赔争议。", "双方明确约定是否存在最低采购承诺；不存在时，预测与计划不构成最低采购义务。"),
    _framework("FS-05", "framework_forecast_order_distinction", "预测与正式订单区分", "高", ("需求预测", "仅供", "正式采购订单", "具有约束力"), "预测与正式订单效力未区分，容易将生产计划错误升级为采购义务。", "滚动预测仅用于产能规划；只有正式订单经确认后才产生有约束力的采购义务。"),
    _framework("FS-06", "framework_periodic_settlement", "周期对账与结算", "高", ("结算周期", "对账", "实际供货数量", "付款依据"), "周期对账、异议和付款依据不明，会造成累计结算争议。", "按约定周期依据订单、送货、收货、退换货单据对账，双方确认后作为付款依据。"),
    _framework("FS-07", "framework_order_delivery_schedule", "订单交期与默认交期", "高", ("订单指定", "确认订单后", "完成交付"), "订单未约定交期时缺少默认交期，迟延起算点不明。", "按订单约定交期履行；订单未特别约定时，自订单确认后约定期限内交付。"),
    _framework("FS-08", "framework_order_amendment_cancellation", "订单变更与取消", "高", ("取消订单", "书面确认", "实际成本"), "已确认订单的变更或取消规则不清，专门生产成本如何承担容易争议。", "已确认订单原则上经双方书面同意方可变更或取消，并合理处理已发生且无法避免的成本。"),
    _framework("FS-09", "framework_price_validity", "价格有效期", "中", ("价格", "保持稳定", "有效期"), "长期供货价格适用期间不明，批次价格可能反复争议。", "产品价格在约定周期内保持稳定，到期后依约定机制复核。"),
    _framework("FS-10", "framework_price_adjustment_trigger", "价格调整触发与程序", "高", ("价格调整", "变化超过", "协商确定", "书面确认"), "调价触发、计算依据或确认程序不清，可能形成单方调价风险。", "达到客观触发条件后任一方可申请调价，双方依据可核验成本因素协商并书面确认。"),
    _framework("FS-11", "framework_confirmed_order_price", "已确认订单价格保护", "高", ("不得单方提高", "已确认", "原约定履行"), "调价可能追溯影响已确认订单，破坏既有订单的价格确定性。", "新价格仅适用于其生效后确认的订单，既有已确认订单仍按原价格履行。"),
    _framework("FS-12", "framework_future_order_deadlock", "调价僵局后的未来订单", "中", ("无法达成", "停止接受新的采购订单", "未来订单"), "调价协商失败后未来订单如何处理不明，可能造成无限期供应义务。", "在约定协商期内未达成新价格时，任一方可暂停接受未来新订单，但不影响既有订单。"),
    _framework("FS-13", "framework_termination_effect", "终止后已确认订单", "高", ("终止", "已经确认的采购订单", "继续履行"), "主协议终止是否影响已确认订单不明，会造成在制品和交付争议。", "主协议届满或终止不影响此前已确认订单继续履行，双方另有书面约定除外。"),
    _framework("FS-14", "framework_document_precedence", "文件效力与条件变更", "高", ("文件效力顺序", "内容不一致", "特别变更", "授权人员"), "正文、附件、订单和变更文件发生冲突时缺少效力顺序。", "明确文件效力顺序；订单仅在明确标注特别变更并经双方授权人员书面确认时覆盖主协议。"),
)
