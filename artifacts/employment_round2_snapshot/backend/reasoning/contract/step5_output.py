"""Step5: 最终报告输出（用户可见内容）"""
import json
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

def build_step5_prompt(contract_text: str, step1_result: Dict, step2_result: Dict, 
                      step3_result: Dict, step4_result: Dict, extra_requirements: str = "") -> str:
    """构建Step5的提示词 - 只输出用户可见内容"""
    # 格式化风险点
    risk_points_str = ""
    for i, risk in enumerate(step4_result["risk_points"]):
        risk_points_str += f"{i+1}. 【{risk['priority']}】{risk['description']}\n"
        risk_points_str += f"   - 修改建议：{risk['suggestion']}\n"
        risk_points_str += f"   - 替代措施：{risk['alternative']}\n"
    
    # 限制额外审查要求最大长度为200字
    original_extra_requirements = extra_requirements
    if extra_requirements and len(extra_requirements) > 200:
        logger.warning(f"[WARN] 用户额外要求超过200字限制，已截断")
        extra_requirements = extra_requirements[:200] + "...（已截断）"
    
    # 构建用户额外要求部分（强制置于最开头）
    has_extra_requirements = extra_requirements and extra_requirements.strip() and extra_requirements != "无"
    
    # 强制前置指令 - 用户额外要求必须优先执行
    extra_requirements_prefix = ""
    if has_extra_requirements:
        # 检测是否涉及房价下跌相关要求
        has_property_price_fall = any(keyword in extra_requirements for keyword in ['房价下跌', '情势变更', '显失公平', '减少损失'])
        
        # 如果涉及房价下跌，添加额外的法律分析要求
        additional_legal_analysis = ""
        if has_property_price_fall:
            additional_legal_analysis = """
        
【特别法律分析要求】：由于用户要求评估未来房价下跌时的合法途径，你必须重点分析以下法律原则：
1. **情势变更原则**：分析是否符合《民法典》第533条规定的情势变更情形，包括合同基础条件是否发生重大变化、继续履行是否显失公平等
2. **显失公平原则**：分析合同条款是否存在显失公平的情形，买方是否有权请求撤销或变更合同
3. **不可抗力与商业风险的区分**：明确房价下跌属于商业风险还是不可抗力，以及对应的法律后果
4. **合同解除权**：分析买方是否享有法定或约定的合同解除权
5. **违约责任的减轻**：分析买方在房价下跌情况下减轻违约责任的合法途径
        
请在"对用户额外要求的专项回应"章节中详细阐述以上分析内容。
"""
        
        extra_requirements_prefix = f"""【用户额外审查要求（必须优先执行）】：{extra_requirements}。你必须严格按照上述要求进行审查，并在最终报告中逐条回应用户的每项要求。如果用户要求从特定角色或立场审查，你必须遵循该立场。不得忽略、简化或自行修改用户的要求。{additional_legal_analysis}

【补充要求】：请在报告中优先回应用户的上述要求，并围绕这些要求进行重点分析。

"""

    # 打印测试日志
    if has_extra_requirements:
        logger.info(f"[STEP5] 用户额外要求: {extra_requirements}")
        logger.info(f"[STEP5] 额外要求前缀内容:\n{extra_requirements_prefix}")
    
    prompt = f"""{extra_requirements_prefix}## 任务：生成最终合同审查报告（用户可见版本）

请基于以下分析结果，生成一份专业、清晰的合同审查报告。报告将直接展示给用户，**不要包含任何内部推理过程、自检清单、置信度标注等技术细节**。

### 合同文本
{contract_text}

### 审查分析结果（内部传递，仅供参考）
- 合同类型：{step1_result['contract_type']}
- 核心结论：{step3_result['R_final']}
- 风险评估：{risk_points_str}

---

### 报告输出要求

请生成以下**用户可见**的内容，格式清晰、专业：

**一、合同基本信息概述**
- 合同类型、主要当事人、合同目的、关键条款摘要
- 用简洁的语言描述合同的核心内容

**二、对用户额外要求的专项回应**
{'（无用户额外要求）' if not has_extra_requirements else ''}
{'- 逐条列出用户要求及对应的审查结论（如果用户要求无意义或不合法，需给出解释）' if has_extra_requirements else ''}
{'- 如果用户要求从特定角色或立场审查，请明确标注并遵循该立场' if has_extra_requirements else ''}
{'- 如果用户要求评估未来房价下跌时的合法途径，必须分析情势变更、显失公平等法律原则，并给出具体建议' if has_extra_requirements and has_property_price_fall else ''}

**三、核心风险分级清单**
按优先级列出所有识别到的风险点，使用以下标注：
- 【强制修改】：不修改将导致合同无效或重大法律风险
- 【建议修改】：修改后可降低风险，但不修改不影响合同基本效力
- 【提示风险】：风险真实但发生概率低，仅需提示客户知悉

每个风险点包含：
- 风险描述
- 具体修改建议（或"仅提示风险，无具体修改建议"）
- 如客户不接受修改的替代风控措施

**四、关键风险评估表格**
使用Markdown表格格式：
| 风险点 | 发生概率 | 影响程度 | 综合风险等级 | 优先级 |

**五、审查结论与行动建议**
- 应该怎么做：列出具体的行动建议，区分必须执行和建议执行
- 为什么：简要说明理由
- 声明：【声明】本分析报告由AI生成，仅供参考，不构成正式法律意见。如有重要法律事务，请咨询执业律师。

---

**输出格式要求**：
请输出严格的JSON格式，包含以下字段：
- "contract_summary": 合同基本信息概述（字符串，Markdown格式）
- "extra_requirements_response": 对用户额外要求的专项回应（字符串，Markdown格式；无额外要求时为空字符串或说明）
- "risk_summary": 核心风险分级清单（字符串，Markdown格式）
- "risk_table": 关键风险评估表格（字符串，Markdown表格格式）
- "conclusion": 审查结论与行动建议（字符串，Markdown格式）

示例输出：
{{
    "contract_summary": "## 合同基本信息\\n\\n本案合同属于建设工程施工合同...",
    "extra_requirements_response": "## 对用户额外要求的专项回应\\n\\n1. 用户要求：重点审查违约责任\\n   - 审查结论：合同第5条违约责任条款明确，不存在不合理罚款...\\n\\n2. 用户要求：站在买方立场审查\\n   - 审查结论：从买方角度分析，发现以下不利于买方的条款...",
    "risk_summary": "## 核心风险分级清单\\n\\n1. 【强制修改】合同无效风险\\n   - 风险描述：...\\n   - 修改建议：...",
    "risk_table": "| 风险点 | 发生概率 | 影响程度 | 综合风险等级 | 优先级 |\\n|--------|----------|----------|--------------|--------|\\n| 合同无效风险 | 高 | 高 | 高风险 | 强制 |",
    "conclusion": "## 审查结论与行动建议\\n\\n**应该怎么做**：...\\n\\n**为什么**：...\\n\\n【声明】本分析报告由AI生成，仅供参考，不构成正式法律意见。"
}}

请严格输出JSON格式，不要添加任何其他内容！"""

    # 打印完整 prompt 测试日志
    logger.info(f"[STEP5] ===== 完整提示词 (共 {len(prompt)} 字符) =====")
    logger.info(f"[STEP5] 前500字符:\n{prompt[:500]}")
    logger.info(f"[STEP5] ===== 提示词结束 =====")

    return prompt

def parse_step5_output(output: str) -> Dict:
    """解析Step5的输出"""
    try:
        data = json.loads(output)
        
        # 验证必需字段
        required_fields = ["contract_summary", "extra_requirements_response", "risk_summary", "risk_table", "conclusion"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"缺少必需字段: {field}")
        
        return data
        
    except json.JSONDecodeError as e:
        logger.error(f"Step5 JSON解析失败: {e}")
        raise
    except ValueError as e:
        logger.error(f"Step5 数据格式验证失败: {e}")
        raise
