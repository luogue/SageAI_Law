"""前置校验模块 - 文件格式、大小、文本内容等"""
import io
import re
import logging
from typing import Tuple, Optional, List
from fastapi import UploadFile

logger = logging.getLogger(__name__)

# 配置
ALLOWED_EXTENSIONS = {'.docx', '.txt', '.pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MIN_CONTENT_LENGTH = 100  # 最少100字符

# 合同关键词（用于判断是否是合同）
CONTRACT_KEYWORDS = [
    '合同', '协议', '约定', '甲方', '乙方', '丙方',
    '权利', '义务', '责任', '违约', '解除', '终止',
    '签署', '签订', '盖章', '生效', '有效期',
    '价款', '金额', '付款', '交货', '服务',
    '保密', '知识产权', '仲裁', '诉讼', '管辖'
]


class ValidationError(Exception):
    """校验错误"""
    def __init__(self, error_code: str, message: str, filename: str = None):
        self.error_code = error_code
        self.message = message
        self.filename = filename
        super().__init__(message)


def validate_file_basic(file: UploadFile) -> Tuple[bool, Optional[dict]]:
    """
    基础文件校验：格式、大小
    
    返回: (是否通过, 错误信息)
    """
    filename = file.filename or "unknown"
    
    # 1. 校验扩展名
    file_ext = filename[filename.rfind('.'):].lower() if '.' in filename else ''
    if file_ext not in ALLOWED_EXTENSIONS:
        return False, {
            "error_code": "INVALID_FORMAT",
            "message": f"不支持的文件格式，请上传 {', '.join(ALLOWED_EXTENSIONS)} 格式文件",
            "filename": filename
        }
    
    # 2. 校验大小
    file.file.seek(0, io.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        size_mb = MAX_FILE_SIZE / (1024 * 1024)
        return False, {
            "error_code": "FILE_TOO_LARGE",
            "message": f"文件大小超过限制（最大 {size_mb}MB）",
            "filename": filename
        }
    
    return True, None


def validate_content(contract_text: str, filename: str = "unknown") -> Tuple[bool, Optional[dict]]:
    """
    文本内容校验：长度、是否是合同
    
    返回: (是否通过, 错误信息)
    """
    # 1. 去除空白字符后的长度检查
    clean_text = contract_text.strip()
    if len(clean_text) < MIN_CONTENT_LENGTH:
        return False, {
            "error_code": "CONTENT_TOO_SHORT",
            "message": f"合同内容过短（至少需要 {MIN_CONTENT_LENGTH} 字符），请上传完整合同",
            "filename": filename
        }
    
    # 2. 检查是否包含合同关键词
    keyword_count = 0
    for keyword in CONTRACT_KEYWORDS:
        if keyword in contract_text:
            keyword_count += 1
    
    # 至少需要2个关键词
    if keyword_count < 2:
        return False, {
            "error_code": "NOT_CONTRACT",
            "message": "文件内容似乎不是合同，请确认上传正确的文件",
            "filename": filename,
            "keyword_count": keyword_count
        }
    
    return True, None


def validate_with_extractor(file_content: bytes, filename: str, extractor_func) -> Tuple[bool, Optional[dict], str]:
    """
    综合校验：结合文本提取器
    
    参数:
        file_content: 文件内容二进制
        filename: 文件名
        extractor_func: 文本提取函数，接收(file_obj)返回{'status': 'success'/'error', 'contract_text': '', ...}
    
    返回: (是否通过, 错误信息, 提取的文本)
    """
    # 创建临时文件对象
    class TempFileObj:
        def __init__(self, content, name):
            self.file = io.BytesIO(content)
            self.filename = name
    
    temp_file = TempFileObj(file_content, filename)
    
    # 1. 提取文本
    try:
        extract_result = extractor_func(temp_file, "")
    except Exception as e:
        logger.error(f"文本提取失败: {e}")
        return False, {
            "error_code": "EXTRACTION_FAILED",
            "message": f"文件解析失败: {str(e)}",
            "filename": filename
        }, ""
    
    if extract_result.get('status') != 'success':
        return False, {
            "error_code": "EXTRACTION_FAILED",
            "message": extract_result.get('message', '文件解析失败'),
            "filename": filename
        }, ""
    
    contract_text = extract_result.get('contract_text', '')
    
    # 2. 内容校验
    valid, error_info = validate_content(contract_text, filename)
    if not valid:
        return False, error_info, contract_text
    
    return True, None, contract_text
