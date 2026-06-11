"""输入层：负责接收原始输入，提取关键事实"""
import re
import io
from typing import Dict, Optional

class InputLayer:
    ALLOWED_EXTENSIONS = ('.docx', '.txt', '.pdf')
    MIN_TEXT_LENGTH = 100
    
    def __init__(self):
        pass
    
    def validate_file_format(self, filename: str) -> bool:
        """校验文件格式"""
        return filename.lower().endswith(self.ALLOWED_EXTENSIONS)
    
    def extract_text_from_file(self, file) -> str:
        """从文件中提取文本内容"""
        filename = file.filename.lower()

        if not self.validate_file_format(filename):
            raise ValueError("不支持的文件格式，请上传.docx/.txt/.pdf文件")

        try:
            file_content = file.file.read()

            if filename.endswith('.txt'):
                return self._extract_from_txt_content(file_content)

            elif filename.endswith('.docx'):
                return self._extract_from_docx_content(file_content)

            elif filename.endswith('.pdf'):
                return self._extract_from_pdf_content(file_content)

            else:
                raise ValueError("不支持的文件格式，请上传.docx/.txt/.pdf文件")

        except ValueError as e:
            raise ValueError(f"{str(e)}")
        except Exception as e:
            raise ValueError(f"文件格式损坏，无法读取：{str(e)}")

    def _extract_from_txt_content(self, content: bytes) -> str:
        """从TXT文件内容提取文本"""
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                text = content.decode('gbk', errors='replace')  # 添加 errors='replace' 处理不支持的字符
            except UnicodeDecodeError:
                text = content.decode('gb2312', errors='replace')
        return text

    def _extract_from_docx_content(self, content: bytes) -> str:
        """从DOCX文件内容提取文本"""
        try:
            from docx import Document
            document = Document(io.BytesIO(content))
            text = '\n'.join([paragraph.text for paragraph in document.paragraphs])
            if not text.strip():
                raise ValueError("文件内容为空")
            return text
        except ImportError:
            raise ValueError("缺少python-docx依赖，请安装：pip install python-docx")
        except Exception as e:
            raise ValueError(f"DOCX文件解析失败：{str(e)}")

    def _extract_from_pdf_content(self, content: bytes) -> str:
        """从PDF文件内容提取文本"""
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(content))

            if reader.is_encrypted:
                raise ValueError("PDF文件已加密，无法读取")

            text = ''
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'

            if not text.strip():
                raise ValueError("PDF文件内容为空或无法提取文本")
            return text
        except ImportError:
            raise ValueError("缺少pypdf依赖，请安装：pip install pypdf")
        except Exception as e:
            raise ValueError(f"PDF文件解析失败：{str(e)}")
    
    def validate_content(self, text: str) -> bool:
        """校验内容非空"""
        if not text or len(text.strip()) < self.MIN_TEXT_LENGTH:
            return False
        return True
    
    def extract_key_facts(self, contract_text: str) -> Dict:
        """从合同文本中提取关键事实"""
        facts = {
            "basic_info": self._extract_basic_info(contract_text),
            "key_clauses": self._extract_key_clauses(contract_text),
            "dispute_focus": self._extract_dispute_focus(contract_text)
        }
        return facts
    
    def _extract_basic_info(self, text: str) -> Dict:
        """提取基本案情信息"""
        info = {
            "contract_type": self._extract_contract_type(text),
            "parties": self._extract_parties(text),
            "subject_matter": self._extract_subject_matter(text),
            "amount": self._extract_amount(text),
            "sign_date": self._extract_sign_date(text),
            "validity_period": self._extract_validity_period(text)
        }
        return info
    
    def _extract_contract_type(self, text: str) -> str:
        """提取合同类型"""
        patterns = [
            r'(买卖合同|租赁合同|服务合同|借款合同|劳动合同|合作协议|保密协议)',
            r'合同名称[：:]?\s*([^\n]+)',
            r'鉴于[^\n]*([^\n]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return "未明确"
    
    def _extract_parties(self, text: str) -> str:
        """提取双方当事人"""
        patterns = [
            r'(甲方|甲方：|甲方名称)[：:]?\s*([^\n]+)',
            r'(乙方|乙方：|乙方名称)[：:]?\s*([^\n]+)',
            r'(出卖人|买受人|出租人|承租人|债权人|债务人)[：:]?\s*([^\n]+)'
        ]
        parties = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                parties.append(f"{match[0]}: {match[1].strip()}")
        return "; ".join(parties) if parties else "未明确"
    
    def _extract_subject_matter(self, text: str) -> str:
        """提取合同标的"""
        patterns = [
            r'标的[：:]?\s*([^\n]+)',
            r'合同标的[：:]?\s*([^\n]+)',
            r'标的物[：:]?\s*([^\n]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return "未明确"
    
    def _extract_amount(self, text: str) -> str:
        """提取合同金额"""
        patterns = [
            r'(?:人民币|￥|¥)\s*([\d,.]+)',
            r'金额[：:]?\s*(人民币)?\s*([\d,.]+)',
            r'价款[：:]?\s*(人民币)?\s*([\d,.]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1) if match.group(1) else match.group(2)
        return "未明确"
    
    def _extract_sign_date(self, text: str) -> str:
        """提取签订日期"""
        pattern = r'(签订日期|签署日期|合同日期)[：:]?\s*(\d{4}[\-/年]\d{1,2}[\-/月]\d{1,2}[日号]?)'
        match = re.search(pattern, text)
        if match:
            return match.group(2).strip()
        return "未明确"
    
    def _extract_validity_period(self, text: str) -> str:
        """提取有效期"""
        patterns = [
            r'有效期[：:]?\s*([^\n]+)',
            r'期限[：:]?\s*([^\n]+)',
            r'自(\d{4}[\-/年]\d{1,2}[\-/月]\d{1,2})至(\d{4}[\-/年]\d{1,2}[\-/月]\d{1,2})'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return "未明确"
    
    def _extract_key_clauses(self, text: str) -> Dict:
        """提取主要条款"""
        clauses = {
            "payment_terms": self._extract_payment_terms(text),
            "liability": self._extract_liability(text),
            "termination": self._extract_termination(text),
            "confidentiality": self._extract_confidentiality(text),
            "dispute_resolution": self._extract_dispute_resolution(text)
        }
        return clauses
    
    def _extract_payment_terms(self, text: str) -> str:
        """提取付款条款"""
        pattern = r'(付款方式|付款时间|结算方式)[：:]?\s*([^\n]+)'
        match = re.search(pattern, text)
        if match:
            return match.group(2).strip()
        return "未明确"
    
    def _extract_liability(self, text: str) -> str:
        """提取违约责任"""
        pattern = r'(违约责任|违约条款)[：:]?\s*([^\n]+)'
        match = re.search(pattern, text)
        if match:
            return match.group(2).strip()
        return "未明确"
    
    def _extract_termination(self, text: str) -> str:
        """提取终止条款"""
        pattern = r'(合同解除|终止条款|解除条件)[：:]?\s*([^\n]+)'
        match = re.search(pattern, text)
        if match:
            return match.group(2).strip()
        return "未明确"
    
    def _extract_confidentiality(self, text: str) -> str:
        """提取保密条款"""
        pattern = r'(保密条款|保密义务)[：:]?\s*([^\n]+)'
        match = re.search(pattern, text)
        if match:
            return match.group(2).strip()
        return "未明确"
    
    def _extract_dispute_resolution(self, text: str) -> str:
        """提取争议解决"""
        pattern = r'(争议解决|管辖法院|仲裁)[：:]?\s*([^\n]+)'
        match = re.search(pattern, text)
        if match:
            return match.group(2).strip()
        return "未明确"
    
    def _extract_dispute_focus(self, text: str) -> str:
        """提取争议焦点"""
        patterns = [
            r'(争议焦点|争议事项)[：:]?\s*([^\n]+)',
            r'(双方争议|主要分歧)[：:]?\s*([^\n]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(2).strip()
        return "未明确"
    
    def process(self, file, additional_instructions: Optional[str] = "") -> Dict:
        """处理输入，返回结构化JSON数据"""
        try:
            # 提取文本（已包含文件格式校验和编码异常捕获）
            contract_text = self.extract_text_from_file(file)
            
            # 内容非空校验
            if not self.validate_content(contract_text):
                return {
                    "status": "error",
                    "message": "合同内容过短，请确认文件是否正确"
                }
            
            # 提取关键事实
            facts = self.extract_key_facts(contract_text)
            
            # 构建结构化输出
            result = {
                "contract_text": contract_text,
                "facts": facts,
                "user_instructions": additional_instructions or "无",
                "status": "success"
            }
            
            return result
            
        except ValueError as e:
            # 已知的校验错误
            return {
                "status": "error",
                "message": str(e)
            }
        except Exception as e:
            # 未知错误
            return {
                "status": "error",
                "message": f"文件处理失败：{str(e)}"
            }
