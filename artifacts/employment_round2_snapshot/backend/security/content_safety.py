"""内容安全审核模块 - 集成阿里云内容安全API"""
import os
import re
import time
import hashlib
import logging
from typing import Optional, Tuple, Dict, Any
import requests

logger = logging.getLogger(__name__)

# 环境变量配置
ALIYUN_GREEN_ENABLE = os.getenv("ALIYUN_GREEN_ENABLE", "false").lower() == "true"
ALIYUN_GREEN_ACCESS_KEY_ID = os.getenv("ALIYUN_GREEN_ACCESS_KEY_ID", "")
ALIYUN_GREEN_ACCESS_KEY_SECRET = os.getenv("ALIYUN_GREEN_ACCESS_KEY_SECRET", "")

# 阿里云Green API配置
REGION_ID = "cn-shanghai"
ENDPOINT = "green.cn-shanghai.aliyuncs.com"


class AliyunGreenClient:
    """阿里云内容安全客户端"""
    
    def __init__(self):
        self.client = None
        self._initialized = False
        if ALIYUN_GREEN_ENABLE and ALIYUN_GREEN_ACCESS_KEY_ID and ALIYUN_GREEN_ACCESS_KEY_SECRET:
            self._init_client()
    
    def _init_client(self):
        """初始化阿里云Green客户端"""
        try:
            from alibabacloud_green20220302.client import Client
            from alibabacloud_tea_openapi import models as open_api_models
            from alibabacloud_tea_util import models as util_models
            
            config = open_api_models.Config(
                access_key_id=ALIYUN_GREEN_ACCESS_KEY_ID,
                access_key_secret=ALIYUN_GREEN_ACCESS_KEY_SECRET,
                region_id=REGION_ID
            )
            config.endpoint = ENDPOINT
            
            self.client = Client(config)
            self._initialized = True
            logger.info("[SECURITY] 阿里云内容安全客户端初始化成功")
        except Exception as e:
            logger.error(f"[SECURITY] 阿里云内容安全客户端初始化失败: {e}")
            self._initialized = False
    
    def check_text_safety(self, text: str) -> Dict[str, Any]:
        """
        调用阿里云文本审核接口
        
        Args:
            text: 待审核文本
        
        Returns:
            dict: 审核结果，包含 suggestion 和 label
            - suggestion: "pass"（通过）, "review"（需人工审核）, "block"（拦截）
            - label: 违规类型，如 "porn", "politics", "terrorism" 等
            - success: 是否调用成功
            - message: 错误信息（如果失败）
        """
        if not self._initialized:
            logger.warning("[SECURITY] 阿里云内容安全客户端未初始化，跳过云端审核")
            return {
                "success": True,
                "suggestion": "pass",
                "label": "",
                "message": "客户端未初始化，跳过审核"
            }
        
        try:
            from alibabacloud_green20220302 import models as green_models
            from alibabacloud_tea_util import models as util_models
            
            task = green_models.TextScanTask(
                content=text[:10000]  # 限制长度，避免超限
            )
            
            request = green_models.TextScanRequest(
                tasks=[task],
                scene=["antispam"]
            )
            
            runtime = util_models.RuntimeOptions()
            runtime.read_timeout = 30000
            runtime.connect_timeout = 30000
            
            response = self.client.text_scan_with_options(request, runtime)
            
            if response.status_code == 200 and response.body:
                result = response.body
                if result.code == 200 and result.data:
                    for item in result.data:
                        if item.suggestion:
                            suggestion = item.suggestion.lower()
                            label = item.label if item.label else ""
                            logger.info(f"[SECURITY] 阿里云内容审核完成: suggestion={suggestion}, label={label}")
                            return {
                                "success": True,
                                "suggestion": suggestion,
                                "label": label,
                                "message": ""
                            }
            
            logger.error(f"[SECURITY] 阿里云内容审核响应异常: {response}")
            return {
                "success": False,
                "suggestion": "pass",
                "label": "",
                "message": "审核响应异常"
            }
            
        except Exception as e:
            logger.error(f"[SECURITY] 阿里云内容审核调用失败: {e}")
            return {
                "success": False,
                "suggestion": "pass",
                "label": "",
                "message": f"调用失败: {str(e)}"
            }


# 全局客户端实例
_green_client = None


def init_green_client() -> AliyunGreenClient:
    """初始化并获取阿里云Green客户端"""
    global _green_client
    if _green_client is None:
        _green_client = AliyunGreenClient()
    return _green_client


def check_text_safety(text: str, client: AliyunGreenClient = None) -> Dict[str, Any]:
    """
    便捷函数：检查文本安全性
    
    Args:
        text: 待审核文本
        client: 可选的客户端实例，若为None则使用全局实例
    
    Returns:
        dict: 审核结果
    """
    if client is None:
        client = init_green_client()
    return client.check_text_safety(text)


# ========== 原有功能保留（降级方案）==========

class ContentSafety:
    """内容安全审核模块 - 兼容原有接口"""
    
    def __init__(self):
        self.green_client = init_green_client()
    
    def check_text(self, text: str) -> Tuple[bool, str]:
        """检查文本内容是否违规（兼容原有接口）"""
        if not ALIYUN_GREEN_ENABLE:
            logger.warning("[SECURITY] 阿里云内容安全未启用，跳过云端审核")
            return True, ""
        
        result = self.green_client.check_text_safety(text)
        
        if not result["success"]:
            # API调用失败，降级放行，记录日志
            logger.error(f"[SECURITY] 云端审核失败，降级放行: {result['message']}")
            return True, ""
        
        if result["suggestion"] == "block":
            logger.warning(f"[SECURITY] 云端内容审核拦截: {result['label']}")
            return False, f"内容包含违规信息（{result['label']}）"
        
        return True, ""


# 全局实例（兼容原有代码）
content_safety = ContentSafety()


def mask_content(text: str) -> str:
    """屏蔽违规内容"""
    return re.sub(r'[\x00-\x1f\x7f-\x9f]', '[已屏蔽]', text)


def add_ai_marker(text: str) -> str:
    """添加AI生成标识（如果报告末尾没有的话）"""
    marker = "\n\n---\n*本报告由AI生成，仅供参考，如有疑问请联系专业人士。*\n"
    
    # 检查报告末尾是否已经有AI声明
    ai_declaration_patterns = [
        "本分析报告由AI生成",
        "本报告由AI生成",
        "AI生成仅供参考"
    ]
    
    lines = text.strip().split('\n')
    # 检查最后几行是否已经有AI声明
    for i in range(-3, 0):
        if abs(i) <= len(lines):
            line = lines[i].strip()
            for pattern in ai_declaration_patterns:
                if pattern in line:
                    # 已经有声明，不需要再添加
                    return text
    
    # 如果没有声明，添加标识
    return text + marker
