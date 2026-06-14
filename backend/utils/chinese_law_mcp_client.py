"""Chinese Law MCP 客户端 - 用于法条校验"""
import os
import json
import logging
import asyncio
from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass, field
import httpx

logger = logging.getLogger(__name__)

# 法律知识库校验接口配置
CHINESE_LAW_MCP_URL = os.getenv(
    "CHINESE_LAW_MCP_URL",
    "https://open.chineselaw.com/open/hall_detect"
)

# API Key 配置
CHINESE_LAW_API_KEY = os.getenv(
    "CHINESE_LAW_API_KEY",
    "sk_oX2ws2hCtO0e4ooCg4mAlqtqFa6a5tMV"
)

# 请求超时配置
REQUEST_TIMEOUT = 30.0


@dataclass
class LawArticle:
    """法条数据结构"""
    law_name: str           # 法律名称
    article_num: str        # 条款号
    content: str            # 法条内容
    version: str            # 版本/生效日期
    is_valid: bool          # 是否有效
    source: str             # 数据来源


@dataclass
class ValidationResult:
    """校验结果"""
    status: str = ""             # 状态: ok, corrected, replaced, deleted, conflict
    original_citation: str = ""  # 原始引用文本
    corrected_citation: str = "" # 修正后的引用文本
    corrected_content: str = ""  # 修正后的内容
    versions: List[Dict] = field(default_factory=list)  # 多版本信息（用于冲突情况）
    message: str = ""            # 说明信息
    law_article: Optional[LawArticle] = None  # 法条详情


class ChineseLawMCPClient:
    """Chinese Law HTTP 客户端
    
    用于调用法律知识库校验接口，支持法条查询和校验功能
    """
    
    def __init__(self, base_url: str = CHINESE_LAW_MCP_URL, api_key: str = CHINESE_LAW_API_KEY):
        self.base_url = base_url
        self.api_key = api_key
        self._tools_cache: Optional[List[Dict]] = None
    
    def _build_headers(self) -> Dict[str, str]:
        """构建请求头，包含鉴权信息"""
        return {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }
    
    async def _send_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """发送请求到法律知识库服务"""
        url = f"{self.base_url}{endpoint}" if endpoint else self.base_url
        
        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
                if method == "GET":
                    response = await client.get(url, headers=self._build_headers(), params=data)
                else:
                    response = await client.post(url, headers=self._build_headers(), json=data)
                
                response.raise_for_status()
                result = response.json()
                
                if "error" in result:
                    logger.error(f"[LawAPI] 服务返回错误: {result['error']}")
                    raise Exception(result["error"].get("message", "Unknown error"))
                
                return result
                
        except httpx.TimeoutException:
            logger.error(f"[LawAPI] 请求超时: {url}")
            raise Exception("法律知识库服务请求超时")
        except httpx.HTTPError as e:
            logger.error(f"[LawAPI] HTTP 错误: {e}")
            raise Exception(f"法律知识库服务 HTTP 错误: {e}")
    
    async def detect(self, text: str) -> Dict:
        """调用检测接口
        
        Args:
            text: 待检测的文本内容
            
        Returns:
            检测结果
        """
        try:
            result = await self._send_request("POST", "", {"text": text})
            logger.debug(f"[LawAPI] 检测结果: {result}")
            return result
        except Exception as e:
            logger.warning(f"[LawAPI] 检测失败: {e}")
            return {}
    
    async def search_law(self, query: str, limit: int = 5) -> List[Dict]:
        """搜索法律条文
        
        Args:
            query: 搜索关键词或法条引用
            limit: 返回结果数量限制
            
        Returns:
            搜索结果列表
        """
        try:
            result = await self.detect(query)
            # 解析返回结果 - 接口返回的是 regulations 数组
            if result and isinstance(result, dict):
                regulations = result.get("regulations", [])
                if isinstance(regulations, list):
                    return regulations[:limit]
            return []
        except Exception as e:
            logger.warning(f"[LawAPI] 搜索失败: {e}")
            return []
    
    async def get_article(self, law_name: str, article_num: str) -> Optional[LawArticle]:
        """获取特定法条内容
        
        Args:
            law_name: 法律名称（如"民法典"或"《民法典》"）
            article_num: 条款号（如"143"）
            
        Returns:
            法条详情，如果不存在返回 None
        """
        try:
            # 构建查询字符串，添加书名号以提高匹配准确性
            if not law_name.startswith("《"):
                query_law_name = f"《{law_name}》"
            else:
                query_law_name = law_name
            
            query = f"{query_law_name}第{article_num}条"
            result = await self.detect(query)
            
            if result and isinstance(result, dict):
                regulations = result.get("regulations", [])
                if isinstance(regulations, list) and len(regulations) > 0:
                    reg = regulations[0]
                    # 从返回结果中提取数据
                    law_name_full = reg.get("name", law_name)
                    clause = reg.get("clause", f"第{article_num}条")
                    content = reg.get("think_tank_content", reg.get("content", ""))
                    validity_status = reg.get("validity_status", "现行有效")
                    implement_date = reg.get("implement_date", "")
                    
                    return LawArticle(
                        law_name=law_name_full.replace("《", "").replace("》", ""),
                        article_num=article_num,
                        content=content,
                        version=implement_date if implement_date else validity_status,
                        is_valid=(validity_status == "现行有效"),
                        source="chineselaw.com"
                    )
            return None
            
        except Exception as e:
            logger.warning(f"[LawAPI] 获取法条失败: {e}")
            return None
    
    async def validate_citation(
        self, 
        law_name: str, 
        article_num: str, 
        content: str = ""
    ) -> ValidationResult:
        """校验法条引用
        
        Args:
            law_name: 法律名称
            article_num: 条款号
            content: 引用的内容（用于匹配验证）
            
        Returns:
            校验结果
        """
        result = ValidationResult()
        result.original_citation = f"《{law_name}》第{article_num}条"
        
        # 尝试获取法条
        article = await self.get_article(law_name, article_num)
        
        if article is None:
            # 法条不存在，尝试搜索相似内容
            if content:
                search_results = await self.search_law(content[:50], limit=3)
                if search_results:
                    # 找到相似内容，可能是编号错误
                    for item in search_results:
                        item_content = item.get("think_tank_content", item.get("content", ""))
                        if content[:30] in item_content:
                            item_law_name = item.get("name", law_name).replace("《", "").replace("》", "")
                            item_clause = item.get("clause", "")
                            result.status = "corrected"
                            result.corrected_citation = f"《{item_law_name}》{item_clause}"
                            result.corrected_content = item_content
                            result.message = "编号错误，已自动修正为正确条款"
                            result.law_article = LawArticle(
                                law_name=item_law_name,
                                article_num=item.get("article_num", ""),
                                content=item_content,
                                version=item.get("implement_date", ""),
                                is_valid=(item.get("validity_status", "") == "现行有效"),
                                source="chineselaw.com"
                            )
                            return result
            
            # 完全找不到
            result.status = "deleted"
            result.message = f"未找到《{law_name}》第{article_num}条的相关信息"
            return result
        
        result.law_article = article
        
        # 检查法条是否有效
        if not article.is_valid:
            # 法条已废止，可能存在新旧版本冲突
            result.status = "conflict"
            result.message = f"《{law_name}》第{article_num}条已废止，请确认适用版本"
            result.versions = [{
                "version": article.version,
                "content": article.content,
                "is_valid": False
            }]
            # 尝试搜索现行有效版本
            search_results = await self.search_law(f"《{law_name}》第{article_num}条", limit=5)
            for item in search_results:
                if item.get("validity_status", "") == "现行有效":
                    item_content = item.get("think_tank_content", item.get("content", ""))
                    result.versions.append({
                        "version": item.get("implement_date", "现行有效"),
                        "content": item_content,
                        "is_valid": True
                    })
            return result
        
        # 法条有效，检查内容是否匹配
        if not content:
            # 没有提供内容，直接返回官方内容
            result.status = "ok"
            result.corrected_citation = result.original_citation
            result.corrected_content = article.content
            result.message = "引用编号正确"
            return result
        
        # 比较内容
        official_content = article.content
        if content in official_content or official_content[:50] in content:
            # 内容匹配
            result.status = "ok"
            result.corrected_citation = result.original_citation
            result.corrected_content = official_content
            result.message = "引用内容正确"
            return result
        else:
            # 内容不匹配，用官方内容替换
            result.status = "replaced"
            result.corrected_citation = result.original_citation
            result.corrected_content = official_content
            result.message = "引用内容已修正为官方版本"
            return result


class ChineseLawMCPClientSync:
    """同步版本的法律知识库客户端（用于非异步环境）"""
    
    def __init__(self, base_url: str = CHINESE_LAW_MCP_URL, api_key: str = CHINESE_LAW_API_KEY):
        self.async_client = ChineseLawMCPClient(base_url, api_key)
    
    def _run_async(self, coro):
        """在同步环境中运行异步函数"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果已有运行中的事件循环，创建新的
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, coro)
                    return future.result()
            return loop.run_until_complete(coro)
        except RuntimeError:
            # 没有事件循环，创建新的
            return asyncio.run(coro)
    
    def detect(self, text: str) -> Dict:
        """同步调用检测接口"""
        return self._run_async(self.async_client.detect(text))
    
    def search_law(self, query: str, limit: int = 5) -> List[Dict]:
        """同步搜索法律条文"""
        return self._run_async(self.async_client.search_law(query, limit))
    
    def get_article(self, law_name: str, article_num: str) -> Optional[LawArticle]:
        """同步获取法条内容"""
        return self._run_async(self.async_client.get_article(law_name, article_num))
    
    def validate_citation(
        self, 
        law_name: str, 
        article_num: str, 
        content: str = ""
    ) -> ValidationResult:
        """同步校验法条引用"""
        return self._run_async(
            self.async_client.validate_citation(law_name, article_num, content)
        )


# 全局客户端实例
_mcp_client: Optional[ChineseLawMCPClientSync] = None


def get_mcp_client() -> ChineseLawMCPClientSync:
    """获取全局法律知识库客户端实例"""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = ChineseLawMCPClientSync()
    return _mcp_client


def init_mcp_client(base_url: str = None, api_key: str = None) -> ChineseLawMCPClientSync:
    """初始化法律知识库客户端"""
    global _mcp_client
    _mcp_client = ChineseLawMCPClientSync(
        base_url or CHINESE_LAW_MCP_URL,
        api_key or CHINESE_LAW_API_KEY
    )
    return _mcp_client
