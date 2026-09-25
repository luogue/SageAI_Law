"""Step3: 多原理交叉验证和闭环补全"""
import json
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def build_step3_prompt(contract_text: str, step1_result: Dict, step2_result: Dict) -> str:
    """构建Step3的提示词"""
    # 将推理步骤转换为字符串
    reasoning_str = ""
    for rs in step2_result["reasoning_steps"]:
        reasoning_str += f"【原理{rs['principle_index']}: {rs['principle_name']}】\n"
        for step in rs["steps"]:
            reasoning_str += f"  - {step}\n"
    
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

## 任务：多原理交叉验证与闭环补全

### 合同文本
{contract_text}

### 已完成的推理结论
R1（{step1_result['principles'][0]['name']}）：{step2_result['conclusions']['R1']}
R2（{step1_result['principles'][1]['name']}）：{step2_result['conclusions']['R2']}
R3（{step1_result['principles'][2]['name']}）：{step2_result['conclusions']['R3']}

### 推理步骤详情
{reasoning_str}

### 其他原理（排名第4及以后）
{chr(10).join([f"{i+1}. {p['name']}（{p['score']}分）：{p['description']}" 
              for i, p in enumerate(step1_result["principles"][3:])])}

### 关键时间点
{step1_result.get('key_time_point', '【关键时间点】: [从材料中确定]')}

### 直接依据
{step1_result.get('direct_basis', '【直接依据】: [从材料中提取]')}

### 所需规则类型
{step1_result.get('required_rule_types', '【所需规则类型】: [根据争议确定]')}

---

### 验证要求

1. **一致性检查**：检查R1、R2、R3三者是否自洽、是否存在矛盾。

2. **矛盾解释**：如果存在矛盾，请使用排名第4及以后的原理来解释矛盾产生的原因。

3. **闭环补全**：基于交叉验证结果，推导出解决矛盾后的最终结论R_final，确保逻辑链条完整闭合。

4. **层级标注**：为最终结论标注层级类型：【宏观原则/中观机制/具体操作】

5. **信息来源标注**：
   - 【判决原文】：判决书、政府审查意见等权威来源中明确写明的信息
   - 【事实推断】：基于权威来源事实可合理推导出的结论，非原文直接表述
   - 【模型补充】：权威来源未提供，模型基于法律原理或通用经验的独立推断

6. **规范性质标注**（当引用任何规范、标准、示范文本时）：
   - 【强制性】：法律、行政法规、强制性国家标准（GB/GB/T中带"强制"字样的部分）
   - 【推荐性】：行业标准、地方标准、团体标准、示范文本

7. **法律适用版本标注**（当引用法律或司法解释时）：
   - 【行为时有效】：指案件事实发生当时施行的法律或司法解释
   - 【现行有效】：指当前（2026年）施行的法律或司法解释
   - 标注格式：`【《建工解释一》第41条（现行有效，2021年施行）】` 或 `【《建工解释二》第22条（行为时有效，2019年施行）】`

---

**输出要求**：请输出严格的JSON格式，包含以下字段：
- "is_consistent": 是否自洽（布尔值）
- "conflicts": 矛盾点列表（字符串数组，无矛盾则为空数组）
- "conflict_explanation": 矛盾解释（字符串）
- "R_final": 最终结论（字符串）
- "hierarchy_label": 层级标注（字符串）
- "information_source": 信息来源（字符串）
- "normative_nature": 规范性质（字符串，如"【强制性】"或"【推荐性】"）
- "legal_version": 法律适用版本（字符串，如"【行为时有效】"或"【现行有效】"）

示例输出：
{{
    "is_consistent": true,
    "conflicts": [],
    "conflict_explanation": "R1、R2、R3三者逻辑自洽，无矛盾",
    "R_final": "综合分析，合同条款合法有效，双方应按约履行",
    "hierarchy_label": "宏观原则",
    "information_source": "【事实推断】基于合同文本和法律规定推导得出",
    "normative_nature": "【强制性】",
    "legal_version": "【行为时有效】"
}}

请严格输出JSON格式，不要添加任何其他内容！"""
    
    return prompt

def parse_step3_output(output: str) -> Dict:
    """解析Step3的输出"""
    try:
        data = json.loads(output)
        
        # 验证必需字段
        required_fields = ["is_consistent", "conflicts", "conflict_explanation", 
                          "R_final", "hierarchy_label", "information_source", 
                          "normative_nature", "legal_version"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"缺少必需字段: {field}")
        
        return data
        
    except json.JSONDecodeError as e:
        logger.error(f"Step3 JSON解析失败: {e}")
        raise
    except ValueError as e:
        logger.error(f"Step3 数据格式验证失败: {e}")
        raise