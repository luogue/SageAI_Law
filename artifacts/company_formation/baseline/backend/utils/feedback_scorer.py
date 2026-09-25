"""反馈质量评分器 - 调用SageAI进行智能评分"""
import json
import logging
import os
import asyncio
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Mock 模式已禁用（保留用于调试）
# LLM_MOCK_MODE = os.getenv('LLM_MOCK_MODE', 'false').lower() == 'true'


class FeedbackScorer:
    """反馈质量评分器"""
    
    def __init__(self):
        # 延迟导入以避免循环依赖
        from layers.inference_layer import InferenceLayer
        self.inference_layer = InferenceLayer()
    
    def _build_prompt(self, categories: list, comment: str, has_contract: bool) -> str:
        """构建评分提示词"""
        prompt = f"""
你是一个反馈质量分析专家。请根据用户反馈的内容，评估其对改进AI模型的价值，并给出0-100的质量分和奖励建议。

反馈分类：{json.dumps(categories)}
反馈描述：{comment}
是否上传合同文本：{"是" if has_contract else "否"}（如果上传，则加分）

评分标准：
- 描述具体、包含合同条款或错误定位（+30分）
- 勾选了具体分类（+10分）
- 描述了问题对实际工作的影响（+20分）
- 提出了改进方向或建议（+20分）
- 上传了有效合同文本（+20分，上限100）

请输出JSON格式：
{{
"quality_score": 0-100,
"reason": "简要评分理由",
"suggested_bonus": 1-5
}}

注意：
- quality_score必须是0-100之间的整数
- suggested_bonus根据分数自动换算：60-69→1次，70-79→2次，80-89→3次，90-100→4次，若上传合同+描述详细可再+1次，上限5次
- reason字段要简明扼要，说明评分依据
"""
        return prompt.strip()
    
    def _parse_score_result(self, result: str) -> Dict[str, Any]:
        """解析AI返回的评分结果"""
        try:
            # 尝试提取JSON部分
            if '{' in result:
                start = result.index('{')
                end = result.rindex('}') + 1
                json_str = result[start:end]
                data = json.loads(json_str)
                
                # 验证字段
                if isinstance(data.get('quality_score'), int) and 0 <= data['quality_score'] <= 100:
                    score = data['quality_score']
                else:
                    score = 0
                
                reason = str(data.get('reason', '')).strip()[:500]
                
                # 验证建议奖励
                suggested_bonus = data.get('suggested_bonus', 0)
                if not isinstance(suggested_bonus, int) or suggested_bonus < 0 or suggested_bonus > 5:
                    suggested_bonus = self._calculate_bonus(score)
                
                return {
                    'quality_score': score,
                    'reason': reason,
                    'suggested_bonus': suggested_bonus
                }
        except Exception as e:
            logger.error(f"解析评分结果失败: {e}")
        
        return {
            'quality_score': 0,
            'reason': '解析失败，默认评分',
            'suggested_bonus': 0
        }
    
    def _calculate_bonus(self, score: int) -> int:
        """根据分数计算建议奖励额度"""
        if score >= 90:
            return 4
        elif score >= 80:
            return 3
        elif score >= 70:
            return 2
        elif score >= 60:
            return 1
        return 0
    
    def score_feedback(self, categories: list, comment: str, has_contract: bool = False) -> Dict[str, Any]:
        """
        对反馈内容进行评分
        
        Args:
            categories: 反馈分类列表
            comment: 反馈描述内容
            has_contract: 是否上传了合同文本
        
        Returns:
            dict: 包含 quality_score, reason, suggested_bonus
        """
        # Mock 模式已禁用（保留用于调试）
        # if LLM_MOCK_MODE:
        #     logger.info("[MOCK MODE] 使用模拟反馈评分")
        #     base_score = 60
        #     base_score += len(categories) * 5
        #     comment_length = len(comment.strip())
        #     if comment_length >= 50:
        #         base_score += 10
        #     elif comment_length >= 30:
        #         base_score += 5
        #     if has_contract:
        #         base_score += 20
        #     quality_score = min(max(base_score, 60), 95)
        #     suggested_bonus = self._calculate_bonus(quality_score)
        #     if has_contract and suggested_bonus > 0 and suggested_bonus < 5:
        #         suggested_bonus += 1
        #     reason = f"Mock模式评分：描述长度{comment_length}字，分类{len(categories)}个，{'已' if has_contract else '未'}上传合同"
        #     logger.info(f"Mock反馈评分完成: score={quality_score}, bonus={suggested_bonus}")
        #     return {
        #         'quality_score': quality_score,
        #         'reason': reason,
        #         'suggested_bonus': suggested_bonus
        #     }
        
        # 正常模式：调用推理层获取评分
        prompt = self._build_prompt(categories, comment, has_contract)
        
        try:
            # 调用推理层获取评分
            result = self.inference_layer.run_inference(prompt, "")
            
            # 解析结果
            parsed = self._parse_score_result(result)
            
            # 如果上传了合同，额外加分（最多+1）
            if has_contract and parsed['suggested_bonus'] > 0 and parsed['suggested_bonus'] < 5:
                parsed['suggested_bonus'] += 1
                parsed['reason'] += "；上传合同额外+1次"
            
            logger.info(f"反馈评分完成: score={parsed['quality_score']}, bonus={parsed['suggested_bonus']}")
            return parsed
            
        except Exception as e:
            logger.error(f"反馈评分失败: {e}")
            return {
                'quality_score': 0,
                'reason': f'自动评分失败: {str(e)}',
                'suggested_bonus': 0
            }


# 全局评分器实例
feedback_scorer = FeedbackScorer()


def score_feedback_async(categories: list, comment: str, has_contract: bool = False):
    """异步评分（实际执行同步，可包装为异步）"""
    return feedback_scorer.score_feedback(categories, comment, has_contract)
