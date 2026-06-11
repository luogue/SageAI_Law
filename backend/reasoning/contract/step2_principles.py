"""Step2: 基于原理的链式推理"""
import json
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

def build_step2_prompt(contract_text: str, step1_result: Dict) -> str:
    """构建Step2的提示词"""
    # 将principles转换为字符串
    principles_str = "\n".join([f"{i+1}. {p['name']}（{p['score']}分）：{p['description']}" 
                               for i, p in enumerate(step1_result["principles"])])
    
    prompt = f"""**【推理前提确定（必须执行）】**
在开始分析前，你必须完成以下操作：

1. **时间锚定**：从用户提供的材料中，确定本案核心法律事实所发生的最晚时间点（例如：合同签订、履行、违约、结算确认等关键行为的日期）。以 `【关键时间点】: [具体日期]` 格式输出。

2. **依据提取**：从用户提供的材料中，找出与本案争议直接相关的、明确的约定或公认的事实（如"双方确认的结算报告"、"承包人发函主张权利"等）。以 `【直接依据】: [原文引述或概括]` 格式输出。

3. **规则类型声明**：根据本案的核心争议（如优先权是否存续、合同是否有效等），列出你需要依赖的法律规则类型（例如：期限规则、主张方式规则、债权确定规则、合同效力规则等），但不要写出规则的具体内容。以 `【所需规则类型】: [规则1, 规则2, ...]` 格式输出。

4. **推理基准声明**：输出以下声明："本分析将严格基于上述【关键时间点】和【直接依据】进行推理。对于所需的【规则类型】，我将依据通用法律原则（如'权利应当及时行使'、'约定应当遵守'、'诚实信用'）进行补充，并标注【模型补充】。若我自认为的通用知识与从材料中提取的事实或声明不一致，我必须无条件服从材料中的事实。"

完成上述操作后，再执行该步骤原有的任务。

---

**核心基准约束（必须严格遵守）**
本分析必须严格以提供的合同文本为事实与法律结论的基准。不得自行创设与合同明确条款相矛盾的法律判断。若合同已对某一争议点作出约定，你的分析结论必须与此约定一致。

---

## 任务：基于基本原理的链式推理

### 合同文本
{contract_text}

### 关键审查前提
{', '.join(step1_result['premises'])}

### 基本原理列表（按权重排序）
{principles_str}

### 结构类型
{step1_result['structure_type']}

### 关键时间点
{step1_result.get('key_time_point', '【关键时间点】: [从材料中确定]')}

### 直接依据
{step1_result.get('direct_basis', '【直接依据】: [从材料中提取]')}

### 所需规则类型
{step1_result.get('required_rule_types', '【所需规则类型】: [根据争议确定]')}

---

### 推理要求

请基于上述合同文本、前提和原理，为排名前3的基本原理分别进行链式推理。

**推理格式要求（强制执行）**：
每一步必须拆解到"事实→规则→中间结论"的原子单位。

**针对排名第1的原理（{step1_result['principles'][0]['name']}）**：
- 步骤1：基于【事实X】+ 结合【规则Y】→ 推导出【中间结论Z1】
- 步骤2：基于【Z1】+ 结合【规则W】→ 推导出【中间结论Z2】
- 步骤3：基于【Z2】→ 推导出【最终结论R1】

**针对排名第2的原理（{step1_result['principles'][1]['name']}）**：
- 步骤1：基于【事实X】+ 结合【规则Y】→ 推导出【中间结论Z1】
- 步骤2：基于【Z1】+ 结合【规则W】→ 推导出【中间结论Z2】
- 步骤3：基于【Z2】→ 推导出【最终结论R2】

**针对排名第3的原理（{step1_result['principles'][2]['name']}）**：
- 步骤1：基于【事实X】+ 结合【规则Y】→ 推导出【中间结论Z1】
- 步骤2：基于【Z1】+ 结合【规则W】→ 推导出【中间结论Z2】
- 步骤3：基于【Z2】→ 推导出【最终结论R3】

### 假设条件列表
请单独列出所有影响结论但当前未知的信息（用问句形式）：
- [缺失信息项1？]
- [缺失信息项2？]

### 层级标注要求
为每个推理步骤标注层级类型：【宏观原则/中观机制/具体操作】
- 【宏观原则】：法律基本原则、核心规则
- 【中观机制】：具体法律制度、操作流程
- 【具体操作】：具体条款、事实认定

---

**输出要求**：请输出严格的JSON格式，包含以下字段：
- "assumptions": 假设条件列表（字符串数组）
- "reasoning_steps": 推理步骤列表，每个元素包含 "principle_index"（原理序号，1-3）、"principle_name"（原理名称）、"hierarchy_label"（层级标注）、"steps"（步骤列表）
- "conclusions": 结论列表，包含 "R1"、"R2"、"R3"

示例输出：
{{
    "assumptions": ["合同签订时间是否在2021年之前？", "是否存在补充协议？"],
    "reasoning_steps": [
        {{
            "principle_index": 1,
            "principle_name": "意思自治原则",
            "hierarchy_label": "宏观原则",
            "steps": [
                "步骤1：基于【合同第5条约定价款支付方式】+ 结合【意思自治原则】→ 推导出【双方意思表示真实有效】",
                "步骤2：基于【双方意思表示真实有效】+ 结合【合同法第8条】→ 推导出【合同对双方具有约束力】"
            ]
        }}
    ],
    "conclusions": {{
        "R1": "根据意思自治原则，合同条款有效",
        "R2": "根据诚实信用原则，双方应善意履行",
        "R3": "根据公平原则，权利义务对等"
    }}
}}

请严格输出JSON格式，不要添加任何其他内容！"""
    
    return prompt

def parse_step2_output(output: str) -> Dict:
    """解析Step2的输出"""
    try:
        data = json.loads(output)
        
        # 验证必需字段
        required_fields = ["assumptions", "reasoning_steps", "conclusions"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"缺少必需字段: {field}")
        
        # 验证conclusions包含R1, R2, R3
        if not all(k in data["conclusions"] for k in ["R1", "R2", "R3"]):
            raise ValueError("conclusions必须包含R1, R2, R3")
        
        # 验证reasoning_steps包含hierarchy_label
        for rs in data["reasoning_steps"]:
            if "hierarchy_label" not in rs:
                raise ValueError("reasoning_steps元素缺少hierarchy_label字段")
        
        return data
        
    except json.JSONDecodeError as e:
        logger.error(f"Step2 JSON解析失败: {e}")
        raise
    except ValueError as e:
        logger.error(f"Step2 数据格式验证失败: {e}")
        raise