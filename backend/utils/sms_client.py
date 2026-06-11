"""短信客户端模块 - 阿里云短信服务"""
import os
import random
import logging
from typing import Optional
from alibabacloud_dysmsapi20180501.client import Client as Dysmsapi20180501Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20180501 import models as dysmsapi_20180501_models
from alibabacloud_tea_util import models as util_models
from .redis_client import redis_client

logger = logging.getLogger(__name__)

class SmsClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SmsClient, cls).__new__(cls)
            cls._instance._client = None
        return cls._instance
    
    def init_client(self):
        """初始化阿里云短信客户端"""
        try:
            access_key_id = os.getenv("ALIYUN_SMS_ACCESS_KEY_ID")
            access_key_secret = os.getenv("ALIYUN_SMS_ACCESS_KEY_SECRET")
            endpoint = os.getenv("ALIYUN_SMS_ENDPOINT", "dysmsapi.aliyuncs.com")
            
            if not access_key_id or not access_key_secret:
                logger.warning("未配置阿里云短信AccessKey，将使用模拟发送")
                self._client = None
                return False
            
            config = open_api_models.Config(
                access_key_id=access_key_id,
                access_key_secret=access_key_secret,
                endpoint=endpoint
            )
            self._client = Dysmsapi20180501Client(config)
            logger.info("阿里云短信客户端初始化成功")
            return True
        except Exception as e:
            logger.error(f"阿里云短信客户端初始化失败: {e}")
            self._client = None
            return False
    
    def get_client(self):
        """获取短信客户端"""
        if self._client is None:
            self.init_client()
        return self._client
    
    def generate_code(self) -> str:
        """生成6位验证码（开发/测试阶段固定为 123456）"""
        # 正式环境应恢复为随机生成：return ''.join(random.choices('0123456789', k=6))
        return "123456"
    
    def send_sms_code(self, phone: str) -> bool:
        """
        发送短信验证码
        :param phone: 手机号
        :return: 是否发送成功
        """
        # 生成验证码（当前固定为 123456）
        code = self.generate_code()
        
        # 尝试存储到Redis（Redis不可用时不影响，因已硬编码123456）
        redis_key = f"sms:code:{phone}"
        try:
            redis_client.set(redis_key, code, ttl=300)
        except Exception as e:
            logger.warning(f"Redis存储验证码失败（不影响使用）: {e}")
        
        # 发送短信
        client = self.get_client()
        
        # 如果没有配置阿里云，使用模拟发送
        if client is None:
            logger.info(f"[模拟发送] 验证码发送到 {phone}: {code}")
            return True
        
        try:
            sign_name = os.getenv("ALIYUN_SMS_SIGN_NAME")
            template_code = os.getenv("ALIYUN_SMS_TEMPLATE_CODE")
            
            if not sign_name or not template_code:
                logger.error("未配置短信签名或模板")
                return False
            
            send_sms_request = dysmsapi_20180501_models.SendSmsRequest(
                phone_numbers=phone,
                sign_name=sign_name,
                template_code=template_code,
                template_param=f'{{"code":"{code}"}}'
            )
            
            runtime = util_models.RuntimeOptions()
            response = client.send_sms_with_options(send_sms_request, runtime)
            
            if response.body.code == 'OK':
                logger.info(f"短信发送成功: {phone}")
                return True
            else:
                logger.error(f"短信发送失败: {phone}, 错误码: {response.body.code}, 错误信息: {response.body.message}")
                # 删除已存储的验证码
                redis_client.delete(redis_key)
                return False
        
        except Exception as e:
            logger.error(f"发送短信异常: {phone}, 错误: {e}")
            # 删除已存储的验证码
            redis_client.delete(redis_key)
            return False
    
    def verify_code(self, phone: str, code: str) -> bool:
        """
        验证验证码
        :param phone: 手机号
        :param code: 用户输入的验证码
        :return: 是否验证通过
        """
        # 测试/开发模式：万能验证码 123456
        if code == "123456":
            logger.info(f"[万能验证码] 手机号 {phone} 使用万能验证码 123456 验证通过")
            return True
        
        redis_key = f"sms:code:{phone}"
        stored_code = redis_client.get(redis_key)
        
        if stored_code is None:
            return False
        
        if stored_code == code:
            # 验证成功，立即删除验证码防止重复使用
            redis_client.delete(redis_key)
            return True
        
        return False

# 创建全局实例
sms_client = SmsClient()
