"""Step4: 风险评估与商业可行性评估"""
import json
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

# 价格下跌相关关键词
PRICE_FALL_KEYWORDS = ["价格下跌", "价格波动", "价格调整", "价格风险", "市场价格", "原材料价格", "人工成本"]

def analyze_price_fall_risk(contract_text: str, extra_requirements: str) -> Dict:
    """分析价格下跌风险"""
    return {
        "has_price_fall_risk": any(kw in contract_text or kw in extra_requirements for kw in PRICE_FALL_KEYWORDS),
        "risk_level": "中" if any(kw in contract_text or kw in extra_requirements for kw in PRICE_FALL_KEYWORDS) else "低",
        "description": "合同涉及价格相关条款，存在价格波动风险"
    }

def build_step4_prompt(contract_text: str, step1_result: Dict, step3_result: Dict) -> str:
    """构建Step4的提示词"""
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

## 任务：风险评估与商业可行性评估

### 合同文本
{contract_text}

### 关键审查前提
{chr(10).join([f"- {p}" for p in step1_result['premises']])}

### 最终推理结论
{step3_result['R_final']}

### 关键时间点
{step1_result.get('key_time_point', '【关键时间点】: [从材料中确定]')}

### 直接依据
{step1_result.get('direct_basis', '【直接依据】: [从材料中提取]')}

### 所需规则类型
{step1_result.get('required_rule_types', '【所需规则类型】: [根据争议确定]')}

---

### 风险评估要求

请识别合同中的所有风险点，并按照以下标准进行评估：

**风险分级标准**：
- 【强制】强制修改（底线条款）：不修改将导致合同部分或整体无效，或直接引发重大法律风险
- 【建议】建议修改（优化条款）：修改后可降低风险，但不修改不影响合同基本效力
- 【提示】仅提示风险（商业容忍）：风险真实但发生概率低，或实务中极少修改

**输出格式要求**（每个风险点）：
- 风险描述：清晰描述风险内容
- 发生概率：高/中/低（必须标注判断依据来源：【行业统计/法规要求/通用经验/模型估算】）
- 影响程度：高/中/低（必须标注判断依据来源）
- 修改建议：具体修改措辞，或"无具体修改建议，仅提示"
- 优先级：强制/建议/提示
- 替代措施：如客户不接受修改，可采取的替代风控措施

### 信息来源标注要求
对于每个风险点的判断依据，必须标注信息来源类型：
- 【行业统计】：基于行业数据的统计结果
- 【法规要求】：基于法律法规的明确要求
- 【通用经验】：基于实务中的通用经验
- 【模型估算】：模型基于推理的估算

### 规范性质标注要求
当引用任何规范、标准、示范文本时，必须标注：
- 【强制性】：法律、行政法规、强制性国家标准（GB/GB/T中带"强制"字样的部分）
- 【推荐性】：行业标准、地方标准、团体标准、示范文本

### 法律适用版本标注
引用法律或司法解释时，必须标注：
- 【行为时有效】：指案件事实发生当时施行的法律或司法解释
- 【现行有效】：指当前（2026年）施行的法律或司法解释
- 标注格式：`【《建工解释一》第41条（现行有效，2021年施行）】` 或 `【《建工解释二》第22条（行为时有效，2019年施行）】`

---

**输出要求**：请输出严格的JSON格式，包含以下字段：
- "risk_points": 风险点列表，每个元素包含 "description"（风险描述）、"probability"（发生概率）、"probability_source"（概率依据）、"impact"（影响程度）、"impact_source"（影响依据）、"suggestion"（修改建议）、"priority"（优先级）、"alternative"（替代措施）、"normative_nature"（规范性质）、"legal_version"（法律适用版本）

示例输出：
{{
    "risk_points": [
        {{
            "description": "合同未约定价款支付期限",
            "probability": "中",
            "probability_source": "【通用经验】建设工程合同通常会约定支付期限",
            "impact": "高",
            "impact_source": "【法规要求】《民法典》第511条规定履行期限不明确的处理",
            "suggestion": "建议增加：'甲方应于工程竣工验收合格后30日内支付全部价款'",
            "priority": "建议",
            "alternative": "要求甲方提供支付担保",
            "normative_nature": "【推荐性】",
            "legal_version": "【现行有效】"
        }}
    ]
}}

请严格输出JSON格式，不要添加任何其他内容！"""
    
    return prompt

def parse_step4_output(output: str) -> Dict:
    """解析Step4的输出"""
    try:
        data = json.loads(output)
        
        # 验证必需字段
        if "risk_points" not in data:
            raise ValueError("缺少必需字段: risk_points")
        
        if not isinstance(data["risk_points"], list):
            raise ValueError("risk_points必须是列表")
        
        # 验证每个风险点的格式
        required_fields = ["description", "probability", "probability_source", 
                          "impact", "impact_source", "suggestion", "priority", 
                          "alternative", "normative_nature", "legal_version"]
        for i, risk in enumerate(data["risk_points"]):
            for field in required_fields:
                if field not in risk:
                    raise ValueError(f"风险点{i+1}缺少必需字段: {field}")
        
        return data
        
    except json.JSONDecodeError as e:
        logger.error(f"Step4 JSON解析失败: {e}")
        raise
    except ValueError as e:
        logger.error(f"Step4 数据格式验证失败: {e}")
        raise