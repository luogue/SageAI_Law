"""押金裁判 API 路由 - 独立于合同审查主流程"""
import logging
from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict

from adjudicate.engine import adjudicate_deposit
from adjudicate.engine_v2 import adjudicate_deposit_v2
from adjudicate.agency_engine import adjudicate_agency
from adjudicate.loan_engine import adjudicate_loan
from adjudicate.property_engine import adjudicate_property_management
from adjudicate.sale_engine import adjudicate_sale
from adjudicate.safekeeping_engine import adjudicate_safekeeping
from adjudicate.service_engine import adjudicate_service
from adjudicate.transport_engine import adjudicate_transportation
from adjudicate.work_contract_engine import adjudicate_work_contract

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/adjudicate", tags=["adjudicate_deposit"])


class FactsInput(BaseModel):
    """裁判输入事实对象"""
    contract_valid: Optional[bool] = Field(True, description="合同是否有效")
    contract_end_date: Optional[str] = Field(None, description="合同终止日 (YYYY-MM-DD)")
    contract_clauses: Optional[List[str]] = Field(None, description="合同条款列表")
    contract: Optional[Dict[str, Any]] = Field(None, description="合同详细字段")
    
    has_third_party: bool = Field(False, description="是否有第三人侵权")
    is_early_termination: bool = Field(False, description="是否提前退租")
    has_damage: bool = Field(False, description="是否确有损坏")
    
    damage_reason: Optional[str] = Field(None, description="损坏原因: natural_wear/tenant_fault")
    damage_item: Optional[str] = Field(None, description="损坏物类型: decoration 为装修加装物")
    damage_claimed_by: Optional[str] = Field(None, description="主张赔偿方: landlord/tenant")
    evidence_can_prove_cause: bool = Field(True, description="证据能否证明损坏原因")
    
    notified_at_check_in: bool = Field(False, description="入住时是否已告知瑕疵")
    landlord_remained_silent: bool = Field(False, description="房东知悉后是否保持沉默")
    landlord_know_date: Optional[str] = Field(None, description="房东知道解除事由的日期")
    
    agreed_deduction: float = Field(0.0, description="合同约定的扣款金额")
    repair_quote: float = Field(0.0, description="维修报价")
    vacancy_days: int = Field(0, description="空置天数")
    daily_rent: float = Field(0.0, description="日租金")
    tenant_has_repair_claim: bool = Field(False, description="租客是否有维修费用反诉")


class AdjudicateResult(BaseModel):
    """裁判结果"""
    success: bool = True
    result: str = Field(..., description="判决结果文本")
    triggered_patches: List[str] = Field(default_factory=list, description="触发的补丁清单")
    path: List[str] = Field(default_factory=list, description="裁判决策路径")


class NaturalLanguageFactsInput(BaseModel):
    """第二版裁判引擎：自然语言案件事实输入"""
    case_text: str = Field(..., min_length=1, description="自然语言描述的合同纠纷案件事实")
    contract_type: str = Field("house", description="合同类型: house/vehicle/equipment/property_management/transportation/work_contract/deposit/sale/agency/loan/service")


class AdjudicateV2Result(BaseModel):
    """第二版裁判引擎输出"""
    success: bool = True
    result: str
    major_premise: str
    minor_premise: str
    conclusion: str
    triggered_patches: List[str] = Field(default_factory=list)
    path: List[str] = Field(default_factory=list)
    facts: Dict[str, Any] = Field(default_factory=dict)


@router.post("/deposit", response_model=AdjudicateResult, summary="押金纠纷裁判")
async def adjudicate_deposit_endpoint(facts: FactsInput, request: Request):
    """
    租赁押金纠纷裁判接口
    
    输入租赁押金纠纷的各项事实参数，返回裁判结果及触发的法律补丁清单。
    完全独立于合同文本审查主流程。
    """
    logger.info("收到押金裁判请求")
    
    # 构建事实字典，过滤 None 值
    facts_dict = facts.model_dump(exclude_none=True)
    
    try:
        output = adjudicate_deposit(facts_dict)
        return AdjudicateResult(
            success=True,
            result=output["result"],
            triggered_patches=output["triggered_patches"],
            path=output.get("path", []),
        )
    except Exception as e:
        logger.exception("裁判引擎异常")
        return AdjudicateResult(
            success=False,
            result=f"裁判引擎错误: {str(e)}",
            triggered_patches=[],
        )


@router.post("/deposit-v2", response_model=AdjudicateV2Result, summary="合同纠纷裁判引擎第二版")
async def adjudicate_deposit_v2_endpoint(payload: NaturalLanguageFactsInput, request: Request):
    """
    第二版合同纠纷裁判引擎。

    输入自然语言案件事实，接口内部按合同类型完成事实要素抽取、前置拦截、主决策树运行，并输出三段式裁判结论。
    该接口独立于合同审查主流程和旧版结构化押金裁判接口。
    """
    logger.info("收到合同裁判第二版请求")

    try:
        if payload.contract_type in {"property_management", "property", "物业", "物业服务"}:
            output = adjudicate_property_management(payload.case_text)
        elif payload.contract_type in {"transportation", "transport", "freight", "运输", "货运", "物流"}:
            output = adjudicate_transportation(payload.case_text)
        elif payload.contract_type in {"work_contract", "contracting", "work", "承揽", "承揽合同", "加工", "定作", "修理"}:
            output = adjudicate_work_contract(payload.case_text)
        elif payload.contract_type in {"deposit", "safekeeping", "custody", "bailment", "deposit_contract", "保管", "保管合同", "寄存"}:
            output = adjudicate_safekeeping(payload.case_text)
        elif payload.contract_type in {"sale", "sales", "purchase", "purchase_sale", "goods_sale", "买卖", "买卖合同", "货物买卖"}:
            output = adjudicate_sale(payload.case_text)
        elif payload.contract_type in {"agency", "entrustment", "mandate", "commission", "agent", "委托", "委托合同", "代理"}:
            output = adjudicate_agency(payload.case_text)
        elif payload.contract_type in {"loan", "borrow", "lending", "credit", "借款", "借贷", "借款合同", "民间借贷", "金融借款"}:
            output = adjudicate_loan(payload.case_text)
        elif payload.contract_type in {"service", "services", "consumer_service", "training", "fitness", "服务", "服务合同", "培训", "健身", "美容"}:
            output = adjudicate_service(payload.case_text)
        else:
            output = adjudicate_deposit_v2(payload.case_text, contract_type=payload.contract_type)
        return AdjudicateV2Result(**output)
    except Exception as e:
        logger.exception("合同裁判第二版引擎异常")
        return AdjudicateV2Result(
            success=False,
            result=f"裁判引擎错误: {str(e)}",
            major_premise="",
            minor_premise="",
            conclusion=f"裁判引擎错误: {str(e)}",
            triggered_patches=[],
            path=[],
            facts={},
        )
