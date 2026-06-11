"""多步骤推理调度器：协调Step1~Step5的执行"""
import json
import logging
from typing import Dict, Any, Callable

from .step1_premise import build_step1_prompt, parse_step1_output
from .step2_principles import build_step2_prompt, parse_step2_output
from .step3_reasoning import build_step3_prompt, parse_step3_output
from .step4_risk import build_step4_prompt, parse_step4_output
from .step5_output import build_step5_prompt, parse_step5_output
from .step4_risk import PRICE_FALL_KEYWORDS, analyze_price_fall_risk

logger = logging.getLogger(__name__)

MAX_RETRIES = 3

def call_with_retry(build_prompt_func: Callable, parse_output_func: Callable, 
                   *args, **kwargs) -> Dict:
    """
    调用LLM并进行重试，包含JSON格式校验
    
    :param build_prompt_func: 构建提示词的函数
    :param parse_output_func: 解析输出的函数
    :param args: 传递给build_prompt_func的位置参数
    :param kwargs: 传递给build_prompt_func的关键字参数
    :return: 解析后的结果
    :raises Exception: 重试耗尽仍失败
    """
    from ..llm_client import call_llm, AllModelsFailedError
    
    for attempt in range(MAX_RETRIES):
        try:
            # 构建提示词
            prompt = build_prompt_func(*args, **kwargs)
            
            # 调用LLM（强制JSON格式，内部已含多模型降级+重试）
            output = call_llm(prompt, response_format="json")
            
            # 解析和验证输出
            result = parse_output_func(output)
            
            logger.info(f"步骤执行成功（第{attempt+1}次尝试）")
            return result
            
        except AllModelsFailedError:
            # 所有模型均失败，无需重试，直接向上抛出
            logger.error(f"步骤执行失败：所有模型均不可用")
            raise
        except json.JSONDecodeError as e:
            logger.warning(f"JSON解析失败（第{attempt+1}次尝试）: {e}")
            if attempt == MAX_RETRIES - 1:
                raise Exception(f"JSON解析失败（{MAX_RETRIES}次重试后）: {e}")
            continue
        except ValueError as e:
            logger.warning(f"数据格式验证失败（第{attempt+1}次尝试）: {e}")
            if attempt == MAX_RETRIES - 1:
                raise Exception(f"数据格式验证失败（{MAX_RETRIES}次重试后）: {e}")
            continue
        except Exception as e:
            logger.warning(f"步骤执行失败（第{attempt+1}次尝试）: {e}")
            if attempt == MAX_RETRIES - 1:
                raise Exception(f"步骤执行失败（{MAX_RETRIES}次重试后）: {e}")
            continue

def run_multi_step_reasoning(contract_text: str, extra_requirements: str = "") -> Dict[str, Any]:
    """
    执行完整的多步骤合同审查推理流程
    
    :param contract_text: 合同文本
    :param extra_requirements: 用户额外要求
    :return: 包含所有步骤结果和最终报告的字典
    """
    logger.info("========== 开始多步骤合同审查推理 ==========")
    
    try:
        # Step1: 前置步骤 - 关键前提确认
        logger.info("[Step1] 执行关键前提确认...")
        step1_result = call_with_retry(build_step1_prompt, parse_step1_output, contract_text)
        logger.info(f"[Step1] 完成：合同类型={step1_result['contract_type']}，前提数={len(step1_result['premises'])}，原理数={len(step1_result['principles'])}")
        
        # Step2: 基于原理的链式推理
        logger.info("[Step2] 执行链式推理...")
        step2_result = call_with_retry(build_step2_prompt, parse_step2_output, 
                                      contract_text, step1_result)
        logger.info(f"[Step2] 完成：假设数={len(step2_result['assumptions'])}，推理步骤数={len(step2_result['reasoning_steps'])}")
        
        # Step3: 多原理交叉验证和闭环补全
        logger.info("[Step3] 执行交叉验证...")
        step3_result = call_with_retry(build_step3_prompt, parse_step3_output, 
                                      contract_text, step1_result, step2_result)
        logger.info(f"[Step3] 完成：是否自洽={step3_result['is_consistent']}")
        
        # Step4: 风险评估
        logger.info("[Step4] 执行风险评估...")
        step4_result = call_with_retry(build_step4_prompt, parse_step4_output, 
                                      contract_text, step1_result, step3_result, extra_requirements)
        logger.info(f"[Step4] 完成：风险点数={len(step4_result['risk_points'])}")
        
        # 如果用户额外要求涉及房价下跌相关关键词，执行专项风险分析
        if extra_requirements and any(kw in extra_requirements for kw in PRICE_FALL_KEYWORDS):
            logger.info("[Step4] 检测到房价下跌关键词，执行专项风险分析...")
            try:
                price_fall_risk = analyze_price_fall_risk(contract_text, extra_requirements)
                step4_result["risk_points"].append(price_fall_risk)
                logger.info(f"[Step4] 房价下跌专项风险已追加，当前风险点数={len(step4_result['risk_points'])}")
            except Exception as e:
                logger.warning(f"[Step4] 房价下跌专项分析失败: {e}，跳过")
        
        # Step5: 最终报告输出
        logger.info("[Step5] 生成最终报告...")
        step5_result = call_with_retry(build_step5_prompt, parse_step5_output, 
                                      contract_text, step1_result, step2_result, 
                                      step3_result, step4_result, extra_requirements)
        logger.info("[Step5] 完成")
        
        # 整合所有结果 - 只返回用户可见的最终报告
        # 内部步骤结果仅用于日志记录，不返回给前端
        # 注意：step5_output.py 已经要求模型输出完整的报告结构，包括标题和声明
        # 构建报告时包含对用户额外要求的专项回应
        extra_response_section = step5_result.get("extra_requirements_response", "")
        if extra_response_section and extra_response_section.strip():
            extra_response_section = f"\n\n---\n\n{extra_response_section}"
        
        final_report_markdown = f"""{step5_result["contract_summary"]}
{extra_response_section}

---

{step5_result["risk_summary"]}

---

{step5_result["risk_table"]}

---

{step5_result["conclusion"]}
"""
        
        final_result = {
            # 内部步骤结果（仅用于日志和审计，不返回给前端）
            "_internal": {
                "step1_premise": step1_result,
                "step2_principles": step2_result,
                "step3_reasoning": step3_result,
                "step4_risk": step4_result,
            },
            # 用户可见的最终报告
            "final_report": final_report_markdown,
            "report_sections": {
                "contract_summary": step5_result["contract_summary"],
                "risk_summary": step5_result["risk_summary"],
                "risk_table": step5_result["risk_table"],
                "conclusion": step5_result["conclusion"]
            }
        }
        
        logger.info("========== 多步骤合同审查推理完成 ==========")
        return final_result
        
    except Exception as e:
        logger.error(f"多步骤推理失败: {e}")
        raise