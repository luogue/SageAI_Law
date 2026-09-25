"""法条校验与修正模块 - 调用 Chinese Law MCP 服务校验法条引用

校验逻辑：
- 完全一致：通过校验
- 编号错误但内容匹配：自动修正编号
- 编号正确但内容不匹配：替换为返回的真实内容
- 查不到：删除该法条
- 多版本冲突：列出新旧法条及适用条件，由用户选择
"""
import os
import re
import logging
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
import json

# 导入 MCP 客户端
from utils.chinese_law_mcp_client import (
    get_mcp_client,
    init_mcp_client,
    ChineseLawMCPClientSync,
    ValidationResult,
    LawArticle
)

logger = logging.getLogger(__name__)

# 启用开关
ENABLE_LEGAL_CHECK = os.getenv("ENABLE_LEGAL_CHECK", "true").lower() == "true"

# MCP 服务 URL（可通过环境变量配置）
CHINESE_LAW_MCP_URL = os.getenv(
    "CHINESE_LAW_MCP_URL",
    "https://chinese-law-mcp.vercel.app/mcp"
)

# 法条引用正则表达式
# 匹配模式: 《法律名称》第X条 或 《法律名称》第X条第Y款
LEGAL_CITATION_PATTERN = re.compile(
    r'《([^》]+)》\s*第\s*(\d+)\s*条(?:\s*第\s*(\d+)\s*款)?'
)

# 备用模拟数据库 - 当 MCP 服务不可用时使用
MOCK_LEGAL_DATABASE = {
    "民法典": {
        "1": {
            "content": "第一条 为了保护民事主体的合法权益，调整民事关系，维护社会和经济秩序，适应中国特色社会主义发展要求，弘扬社会主义核心价值观，根据宪法，制定本法。",
            "version": "2021年1月1日起施行"
        },
        "2": {
            "content": "第二条 民法调整平等主体的自然人、法人和非法人组织之间的人身关系和财产关系。",
            "version": "2021年1月1日起施行"
        },
        "5": {
            "content": "第五条 民事主体从事民事活动，应当遵循自愿原则，按照自己的意思设立、变更、终止民事法律关系。",
            "version": "2021年1月1日起施行"
        },
        "6": {
            "content": "第六条 民事主体从事民事活动，应当遵循公平原则，合理确定各方的权利和义务。",
            "version": "2021年1月1日起施行"
        },
        "7": {
            "content": "第七条 民事主体从事民事活动，应当遵循诚信原则，秉持诚实，恪守承诺。",
            "version": "2021年1月1日起施行"
        },
        "143": {
            "content": "第一百四十三条 具备下列条件的民事法律行为有效：（一）行为人具有相应的民事行为能力；（二）意思表示真实；（三）不违反法律、行政法规的强制性规定，不违背公序良俗。",
            "version": "2021年1月1日起施行"
        },
        "464": {
            "content": "第四百六十四条 合同是民事主体之间设立、变更、终止民事法律关系的协议。婚姻、收养、监护等有关身份关系的协议，适用有关该身份关系的法律规定；没有规定的，可以根据其性质参照适用本编规定。",
            "version": "2021年1月1日起施行"
        },
        "502": {
            "content": "第五百零二条 依法成立的合同，自成立时生效，但是法律另有规定或者当事人另有约定的除外。依照法律、行政法规的规定，合同应当办理批准等手续的，依照其规定。未办理批准等手续影响合同生效的，不影响合同中履行报批等义务条款以及相关条款的效力。应当办理申请批准等手续的当事人未履行义务的，对方可以请求其承担违反该义务的责任。依照法律、行政法规的规定，合同的变更、转让、解除等情形应当办理批准等手续的，适用前款规定。",
            "version": "2021年1月1日起施行"
        }
    },
    "合同法": {
        "1": {
            "content": "第一条 为了保护合同当事人的合法权益，维护社会经济秩序，促进社会主义现代化建设，制定本法。",
            "version": "1999年10月1日起施行（已废止）"
        },
        "2": {
            "content": "第二条 本法所称合同是平等主体的自然人、法人、其他组织之间设立、变更、终止民事权利义务关系的协议。婚姻、收养、监护等有关身份关系的协议，适用其他法律的规定。",
            "version": "1999年10月1日起施行（已废止）"
        }
    }
}


class LegalCitation:
    """法条引用对象"""
    def __init__(self, match: re.Match, full_text: str):
        self.original_text = match.group(0)  # 原始匹配文本
        self.law_name = match.group(1)       # 法律名称
        self.article_num = match.group(2)    # 条款号
        self.paragraph_num = match.group(3)  # 款号（可选）
        self.start_pos = match.start()       # 起始位置
        self.end_pos = match.end()           # 结束位置
        self.full_text = full_text           # 完整上下文文本
        
        # 从上下文中提取引用内容
        self.extracted_content = self._extract_content()
    
    def _extract_content(self) -> str:
        """从上下文中提取法条引用的内容描述"""
        # 获取匹配位置之后的文本，尝试提取内容
        after_match = self.full_text[self.end_pos:].strip()
        # 尝试提取直到下一个标点或换行
        content = ""
        for char in after_match:
            if char in '。！？；\n\r':
                break
            content += char
        return content.strip()
    
    def __repr__(self):
        if self.paragraph_num:
            return f"《{self.law_name}》第{self.article_num}条第{self.paragraph_num}款"
        return f"《{self.law_name}》第{self.article_num}条"


class LegalCheckResult:
    """法条校验结果"""
    STATUS_OK = "ok"                  # 编号内容都正确
    STATUS_CORRECTED = "corrected"    # 编号错误但内容匹配，已修正
    STATUS_REPLACED = "replaced"      # 编号正确但内容不匹配，已替换内容
    STATUS_DELETED = "deleted"        # 查不到，已删除
    STATUS_CONFLICT = "conflict"      # 新旧版本冲突
    
    def __init__(self):
        self.status: str = ""
        self.original_citation: str = ""
        self.corrected_citation: str = ""
        self.corrected_content: str = ""
        self.versions: List[Dict[str, str]] = []  # 新旧版本信息
        self.message: str = ""
        self.law_article: Optional[LawArticle] = None  # 法条详情


class ChineseLawMCPAdapter:
    """Chinese Law MCP 服务适配器
    
    整合 MCP 客户端调用，实现法条校验逻辑：
    - 完全一致：通过校验
    - 编号错误但内容匹配：自动修正编号
    - 编号正确但内容不匹配：替换为返回的真实内容
    - 查不到：删除该法条
    - 多版本冲突：列出新旧法条及适用条件，由用户选择
    
    注意：当 MCP 服务不可用时，不使用备用数据库，直接返回原始内容
    """
    
    # MCP 服务可用状态标记
    mcp_available: bool = True
    
    def __init__(self, use_mcp: bool = True):
        """初始化适配器
        
        Args:
            use_mcp: 是否使用 MCP 服务
        """
        self.use_mcp = use_mcp
        self.mcp_client: Optional[ChineseLawMCPClientSync] = None
        self.mcp_available = True  # MCP 服务可用状态
        
        if use_mcp:
            try:
                self.mcp_client = get_mcp_client()
                logger.info("[MCP_ADAPTER] MCP 客户端已初始化")
            except Exception as e:
                logger.warning(f"[MCP_ADAPTER] MCP 客户端初始化失败: {e}")
                self.mcp_available = False
    
    def is_mcp_available(self) -> bool:
        """检查 MCP 服务是否可用"""
        return self.mcp_available and self.mcp_client is not None
    
    def validate_citation(self, law_name: str, article_num: str, content: str = "") -> LegalCheckResult:
        """
        校验法条引用
        
        Args:
            law_name: 法律名称（如"民法典"）
            article_num: 条款号（如"143"）
            content: 引用的内容（可选，用于匹配验证）
        
        Returns:
            LegalCheckResult: 校验结果
        """
        result = LegalCheckResult()
        result.original_citation = f"《{law_name}》第{article_num}条"
        
        # 尝试使用 MCP 服务
        if self.use_mcp and self.mcp_client:
            try:
                mcp_result = self.mcp_client.validate_citation(law_name, article_num, content)
                result.status = mcp_result.status
                result.corrected_citation = mcp_result.corrected_citation
                result.corrected_content = mcp_result.corrected_content
                result.versions = mcp_result.versions
                result.message = mcp_result.message
                result.law_article = mcp_result.law_article
                return result
            except Exception as e:
                logger.warning(f"[MCP_ADAPTER] MCP 校验失败: {e}")
                self.mcp_available = False
        
        # MCP 服务不可用，返回跳过状态（不使用备用数据库）
        result.status = "skipped"
        result.message = "MCP 服务不可用，跳过校验"
        return result
    
    def _validate_with_mock_db(
        self, 
        law_name: str, 
        article_num: str, 
        content: str, 
        result: LegalCheckResult
    ) -> LegalCheckResult:
        """使用备用模拟数据库校验"""
        
        # 检查法律名称是否在数据库中
        if law_name not in MOCK_LEGAL_DATABASE:
            # 尝试模糊匹配
            matched_law = self._fuzzy_match_law_name(law_name)
            if matched_law:
                law_name = matched_law
            else:
                result.status = LegalCheckResult.STATUS_DELETED
                result.message = f"未找到法律 '{law_name}' 的相关信息"
                return result
        
        law_data = MOCK_LEGAL_DATABASE.get(law_name, {})
        
        # 检查条款号是否存在
        if article_num not in law_data:
            # 尝试通过内容匹配找到正确的条款号
            if content:
                matched_article = self._find_by_content(law_name, content)
                if matched_article:
                    result.status = LegalCheckResult.STATUS_CORRECTED
                    result.corrected_citation = f"《{law_name}》第{matched_article}条"
                    result.corrected_content = law_data[matched_article]["content"]
                    result.message = f"已自动修正：原引用《{law_name}》第{article_num}条应为《{law_name}》第{matched_article}条"
                    return result
            
            result.status = LegalCheckResult.STATUS_DELETED
            result.message = f"未找到《{law_name}》第{article_num}条"
            return result
        
        # 编号存在，检查内容是否匹配
        official_content = law_data[article_num]["content"]
        version = law_data[article_num].get("version", "")
        
        # 创建法条详情
        result.law_article = LawArticle(
            law_name=law_name,
            article_num=article_num,
            content=official_content,
            version=version,
            is_valid="已废止" not in version,
            source="mock_db"
        )
        
        if not content:
            # 没有提供内容，直接返回官方内容
            result.status = LegalCheckResult.STATUS_OK
            result.corrected_citation = result.original_citation
            result.corrected_content = official_content
            return result
        
        # 比较内容
        if content in official_content or official_content[:50] in content:
            # 内容匹配
            result.status = LegalCheckResult.STATUS_OK
            result.corrected_citation = result.original_citation
            result.corrected_content = official_content
            return result
        else:
            # 内容不匹配，用官方内容替换
            result.status = LegalCheckResult.STATUS_REPLACED
            result.corrected_citation = result.original_citation
            result.corrected_content = official_content
            result.message = "内容已修正为官方版本"
            return result
    
    def _fuzzy_match_law_name(self, law_name: str) -> Optional[str]:
        """模糊匹配法律名称"""
        common_names = {
            "民法典": ["中华人民共和国民法典", "民法", "民典"],
            "合同法": ["中华人民共和国合同法", "合同"],
            "刑法": ["中华人民共和国刑法"],
            "公司法": ["中华人民共和国公司法"]
        }
        
        for official_name, aliases in common_names.items():
            if law_name == official_name or law_name in aliases:
                return official_name
        return None
    
    def _find_by_content(self, law_name: str, content: str) -> Optional[str]:
        """通过内容查找条款号"""
        law_data = MOCK_LEGAL_DATABASE.get(law_name, {})
        for article_num, article_data in law_data.items():
            official_content = article_data["content"]
            if content and (content[:30] in official_content or official_content[:30] in content):
                return article_num
        return None
    
    def get_law_versions(self, law_name: str, article_num: str) -> List[Dict[str, str]]:
        """获取法条的不同版本"""
        versions = []
        
        # 检查是否有新旧版本冲突
        if law_name == "民法典" and article_num in MOCK_LEGAL_DATABASE.get("民法典", {}):
            versions.append({
                "version": "民法典（现行有效）",
                "effective_date": "2021年1月1日",
                "content": MOCK_LEGAL_DATABASE["民法典"].get(article_num, {}).get("content", ""),
                "is_valid": True
            })
        
        # 检查合同法是否有相同条款（已废止）
        if article_num in MOCK_LEGAL_DATABASE.get("合同法", {}):
            versions.append({
                "version": "合同法（已废止）",
                "effective_date": "1999年10月1日",
                "content": MOCK_LEGAL_DATABASE["合同法"].get(article_num, {}).get("content", ""),
                "is_valid": False
            })
        
        return versions


class LegalCheckLayer:
    """法条校验层
    
    主要功能：
    1. 从报告中提取法条引用
    2. 调用 MCP 服务校验每个引用
    3. 根据校验结果修正报告内容
    """
    
    def __init__(self, use_mcp: bool = True):
        """初始化法条校验层
        
        Args:
            use_mcp: 是否使用 MCP 服务
        """
        self.mcp_adapter = ChineseLawMCPAdapter(use_mcp=use_mcp)
    
    def extract_citations(self, report: str) -> List[LegalCitation]:
        """
        从报告中提取所有法条引用
        
        Args:
            report: 报告文本
        
        Returns:
            List[LegalCitation]: 提取到的法条引用列表
        """
        citations = []
        for match in LEGAL_CITATION_PATTERN.finditer(report):
            citation = LegalCitation(match, report)
            citations.append(citation)
        return citations
    
    def process(self, report: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        处理报告中的所有法条引用
        
        Args:
            report: 原始报告文本
        
        Returns:
            Tuple[str, List[Dict[str, Any]]]: (修正后的报告, 修正记录列表)
        """
        if not ENABLE_LEGAL_CHECK:
            logger.info("[LEGAL_CHECK] 法条校验已禁用")
            return report, []
        
        # 检查 MCP 服务是否可用
        if not self.mcp_adapter.is_mcp_available():
            logger.warning("[LEGAL_CHECK] MCP 服务不可用，跳过法条校验")
            # 在报告末尾附加提示
            warning_text = "\n\n---\n\n**注意：法条校验服务暂时不可用，以下法律依据未经权威验证。**"
            return report + warning_text, []
        
        logger.info("[LEGAL_CHECK] 开始法条校验")
        
        citations = self.extract_citations(report)
        logger.info(f"[LEGAL_CHECK] 提取到 {len(citations)} 条法条引用")
        
        if not citations:
            return report, []
        
        # 按位置倒序处理，避免位置偏移问题
        citations.sort(key=lambda c: c.start_pos, reverse=True)
        
        corrected_report = report
        correction_records = []
        mcp_failed = False  # 标记 MCP 是否在校验过程中失败
        
        for citation in citations:
            # 在校正后的报告中重新查找位置（因为前面的修正可能改变了位置）
            pos = corrected_report.rfind(citation.original_text, 0, citation.start_pos + 100)
            if pos == -1:
                pos = corrected_report.find(citation.original_text)
            
            if pos == -1:
                logger.warning(f"[LEGAL_CHECK] 无法在报告中找到引用: {citation.original_text}")
                continue
            
            # 调用 MCP 服务校验
            result = self.mcp_adapter.validate_citation(
                citation.law_name,
                citation.article_num,
                citation.extracted_content
            )
            
            # 检查是否 MCP 服务失败
            if result.status == "skipped":
                mcp_failed = True
                break
            
            # 根据结果处理
            if result.status == LegalCheckResult.STATUS_OK:
                # 编号内容都正确，保留
                correction_records.append({
                    "original": citation.original_text,
                    "corrected": result.corrected_citation,
                    "status": "保留",
                    "message": "引用正确"
                })
                
            elif result.status == LegalCheckResult.STATUS_CORRECTED:
                # 编号错误但内容匹配，自动修正并加注
                replacement = f"{result.corrected_citation}（已自动修正）"
                corrected_report = corrected_report[:pos] + replacement + corrected_report[pos + len(citation.original_text):]
                correction_records.append({
                    "original": citation.original_text,
                    "corrected": result.corrected_citation,
                    "status": "已修正",
                    "message": result.message
                })
                
            elif result.status == LegalCheckResult.STATUS_REPLACED:
                # 编号正确但内容不匹配，用权威内容替换
                replacement = f"{result.corrected_citation}：{result.corrected_content}"
                corrected_report = corrected_report[:pos] + replacement + corrected_report[pos + len(citation.original_text):]
                correction_records.append({
                    "original": citation.original_text,
                    "corrected": result.corrected_citation,
                    "status": "内容已修正",
                    "message": result.message
                })
                
            elif result.status == LegalCheckResult.STATUS_DELETED:
                # 查不到，删除该法条引用
                corrected_report = corrected_report[:pos] + corrected_report[pos + len(citation.original_text):]
                correction_records.append({
                    "original": citation.original_text,
                    "corrected": "",
                    "status": "已删除",
                    "message": result.message
                })
                
            elif result.status == LegalCheckResult.STATUS_CONFLICT:
                # 新旧版本冲突，同时列出两个版本
                versions = self.mcp_adapter.get_law_versions(citation.law_name, citation.article_num)
                if result.versions:
                    versions = result.versions  # 优先使用 MCP 返回的版本信息
                version_text = "\n".join([f"- {v.get('version', '')}（{v.get('effective_date', '')}）：{v.get('content', '')[:50]}..." for v in versions])
                replacement = f"{citation.original_text}【注：存在新旧版本差异，请根据合同签订时间选择】\n{version_text}"
                corrected_report = corrected_report[:pos] + replacement + corrected_report[pos + len(citation.original_text):]
                correction_records.append({
                    "original": citation.original_text,
                    "corrected": citation.original_text,
                    "status": "版本冲突",
                    "message": "新旧版本冲突，已列出所有版本供用户选择"
                })
        
        # 如果 MCP 在校验过程中失败，返回原始报告并附加提示
        if mcp_failed:
            logger.warning("[LEGAL_CHECK] MCP 服务在校验过程中不可用，返回原始报告")
            warning_text = "\n\n---\n\n**注意：法条校验服务暂时不可用，以下法律依据未经权威验证。**"
            return report + warning_text, []
        
        logger.info(f"[LEGAL_CHECK] 法条校验完成，共处理 {len(correction_records)} 条引用")
        return corrected_report, correction_records


# 全局单例
_legal_check_layer: Optional[LegalCheckLayer] = None


def init_legal_check_layer(use_mcp: bool = True) -> LegalCheckLayer:
    """初始化全局法条校验层
    
    Args:
        use_mcp: 是否使用 MCP 服务（默认 True）
    
    Returns:
        LegalCheckLayer: 法条校验层实例
    """
    global _legal_check_layer
    _legal_check_layer = LegalCheckLayer(use_mcp=use_mcp)
    return _legal_check_layer


def get_legal_check_layer() -> Optional[LegalCheckLayer]:
    """获取全局法条校验层实例"""
    return _legal_check_layer


def check_and_correct_legal_citations(report: str) -> Tuple[str, List[Dict[str, Any]]]:
    """便捷函数：检查并修正报告中的法条引用
    
    这是主要的对外接口函数，用于校验报告中的法条引用。
    
    校验逻辑：
    - 完全一致：通过校验
    - 编号错误但内容匹配：自动修正编号
    - 编号正确但内容不匹配：替换为返回的真实内容
    - 查不到：删除该法条
    - 多版本冲突：列出新旧法条及适用条件，由用户选择
    
    Args:
        report: 包含法条引用的报告文本
    
    Returns:
        Tuple[str, List[Dict[str, Any]]]: 
            - 修正后的报告文本
            - 修正记录列表，每条记录包含：
                - original: 原始引用文本
                - corrected: 修正后的引用文本
                - status: 状态（保留/已修正/内容已修正/已删除/版本冲突）
                - message: 说明信息
    
    Example:
        >>> from layers.legal_check_layer import check_and_correct_legal_citations
        >>> report = "根据《民法典》第143条规定..."
        >>> corrected_report, records = check_and_correct_legal_citations(report)
        >>> print(corrected_report)
        >>> print(records)
    """
    layer = get_legal_check_layer()
    if layer is None:
        # 自动初始化
        init_legal_check_layer()
        layer = get_legal_check_layer()
    
    if layer is None:
        logger.warning("[LEGAL_CHECK] 未初始化，跳过法条校验")
        return report, []
    
    return layer.process(report)


def validate_single_citation(
    law_name: str, 
    article_num: str, 
    content: str = ""
) -> LegalCheckResult:
    """校验单个法条引用
    
    Args:
        law_name: 法律名称（如"民法典"）
        article_num: 条款号（如"143"）
        content: 引用的内容（可选，用于匹配验证）
    
    Returns:
        LegalCheckResult: 校验结果
    
    Example:
        >>> from layers.legal_check_layer import validate_single_citation
        >>> result = validate_single_citation("民法典", "143", "民事法律行为有效")
        >>> print(result.status)  # ok, corrected, replaced, deleted, conflict
        >>> print(result.corrected_content)
    """
    adapter = ChineseLawMCPAdapter(use_mcp=True)
    return adapter.validate_citation(law_name, article_num, content)


# 导出接口
__all__ = [
    # 主要函数
    'check_and_correct_legal_citations',
    'validate_single_citation',
    'init_legal_check_layer',
    'get_legal_check_layer',
    
    # 类
    'LegalCheckLayer',
    'LegalCheckResult',
    'LegalCitation',
    'ChineseLawMCPAdapter',
    
    # 常量
    'ENABLE_LEGAL_CHECK',
    'LEGAL_CITATION_PATTERN',
    'CHINESE_LAW_MCP_URL',
]
