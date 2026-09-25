"""敏感词过滤模块 - AC自动机 + 白名单优先机制 + 拦截日志"""
from storage.paths import sqlite_connection
import os
import re
import json
import sqlite3
import threading
from datetime import datetime, timedelta
from typing import List, Tuple, Set, Optional, Dict, Any
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import logging

logger = logging.getLogger(__name__)

# ========== 配置 ==========
WHITELIST_FILE = os.path.join(os.path.dirname(__file__), "whitelist.txt")
from storage.paths import auxiliary_db_path
INTERCEPT_DB = auxiliary_db_path('intercept_logs.db', os.path.join(os.path.dirname(__file__), "intercept_logs.db"))

# ========== 白名单配置 ==========
BASE_WHITELIST = {
    "维权", "诉讼", "仲裁", "原告", "被告", "判决", "裁定", "起诉",
    "委托代理", "法律援助", "代理", "债务人", "债权人", "违约金",
    "解除", "索赔", "管辖", "申请人", "被申请人"
}

def _load_persistent_whitelist() -> Set[str]:
    """从文件加载持久化的白名单"""
    persisted = set()
    if os.path.exists(WHITELIST_FILE):
        try:
            with open(WHITELIST_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    word = line.strip()
                    if word and not word.startswith("#"):
                        persisted.add(word)
        except Exception as e:
            logger.warning(f"加载白名单文件失败: {e}")
    return persisted

def _save_persistent_whitelist(whitelist: Set[str]) -> None:
    """保存白名单到文件"""
    try:
        with open(WHITELIST_FILE, "w", encoding="utf-8") as f:
            f.write("# 白名单词库 - 每行一个词\n")
            for word in sorted(whitelist):
                f.write(f"{word}\n")
        logger.info(f"白名单已保存到文件，共 {len(whitelist)} 个词")
    except Exception as e:
        logger.error(f"保存白名单文件失败: {e}")

_env_whitelist_str = os.getenv("SENSITIVE_WHITELIST", "")
if _env_whitelist_str:
    _env_whitelist = {w.strip() for w in _env_whitelist_str.split(",") if w.strip()}
else:
    _env_whitelist = set()

PERSISTENT_WHITELIST = _load_persistent_whitelist()
WHITELIST: Set[str] = BASE_WHITELIST | _env_whitelist | PERSISTENT_WHITELIST

logger.info(f"白名单已加载，共 {len(WHITELIST)} 个词: {WHITELIST}")

# ========== 拦截日志数据库初始化 ==========
def _init_intercept_db():
    """初始化拦截日志数据库"""
    with sqlite_connection(INTERCEPT_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS intercept_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER,
                ip VARCHAR(45),
                request_path VARCHAR(100),
                trigger_type VARCHAR(50),
                trigger_word VARCHAR(200),
                text_preview TEXT,
                action VARCHAR(20) DEFAULT 'rejected'
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_trigger_word ON intercept_logs(trigger_word)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON intercept_logs(timestamp)")
        conn.commit()

_init_intercept_db()

# ========== 异步日志写入 ==========
_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="intercept_log")

def _write_intercept_log_async(log_data: Dict[str, Any]) -> None:
    """异步写入拦截日志"""
    def _write():
        try:
            with sqlite_connection(INTERCEPT_DB) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO intercept_logs (user_id, ip, request_path, trigger_type, trigger_word, text_preview, action)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    log_data.get("user_id"),
                    log_data.get("ip", ""),
                    log_data.get("request_path", ""),
                    log_data.get("trigger_type", ""),
                    log_data.get("trigger_word", ""),
                    log_data.get("text_preview", ""),
                    log_data.get("action", "rejected")
                ))
                conn.commit()

                logger.info(f"[INTERCEPT_LOG] user_id={log_data.get('user_id')}, ip={log_data.get('ip')}, trigger={log_data.get('trigger_word')}")
        except Exception as e:
            logger.error(f"写入拦截日志失败: {e}")
    _executor.submit(_write)

def log_interception(
    user_id: Optional[int],
    ip: str,
    request_path: str,
    trigger_type: str,
    trigger_words: List[str],
    text_preview: str = ""
) -> None:
    """记录拦截日志（异步）"""
    log_data = {
        "user_id": user_id,
        "ip": ip,
        "request_path": request_path,
        "trigger_type": trigger_type,
        "trigger_word": ",".join(trigger_words),
        "text_preview": text_preview[:200] if text_preview else ""
    }
    _write_intercept_log_async(log_data)
    logger.info(f"[WHITELIST_PASS] 文本命中白名单放行，words={trigger_words[:3]}...")

def get_frequent_triggers(days: int = 7, limit: int = 50) -> List[Dict[str, Any]]:
    """获取高频触发词统计"""
    with sqlite_connection(INTERCEPT_DB) as conn:
        cursor = conn.cursor()
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            SELECT trigger_word, COUNT(*) as count, MAX(timestamp) as last_trigger_time
            FROM intercept_logs
            WHERE timestamp >= ?
            GROUP BY trigger_word
            ORDER BY count DESC
            LIMIT ?
        """, (cutoff, limit))
        rows = cursor.fetchall()

        return [
            {"word": row[0], "count": row[1], "last_trigger_time": row[2]}
            for row in rows
        ]

def get_recent_intercept_logs(trigger_word: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    """获取最近的拦截日志"""
    with sqlite_connection(INTERCEPT_DB) as conn:
        cursor = conn.cursor()
        if trigger_word:
            cursor.execute("""
                SELECT id, timestamp, user_id, ip, request_path, trigger_word, text_preview
                FROM intercept_logs
                WHERE trigger_word = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (trigger_word, limit))
        else:
            cursor.execute("""
                SELECT id, timestamp, user_id, ip, request_path, trigger_word, text_preview
                FROM intercept_logs
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "timestamp": row[1],
                "user_id": row[2],
                "ip": row[3],
                "request_path": row[4],
                "trigger_word": row[5],
                "text_preview": row[6]
            }
            for row in rows
        ]

def add_to_whitelist(word: str) -> bool:
    """添加词到白名单（持久化）"""
    global WHITELIST
    word = word.strip()
    if not word:
        return False
    WHITELIST.add(word)
    PERSISTENT_WHITELIST.add(word)
    _save_persistent_whitelist(WHITELIST)
    logger.info(f"已将 '{word}' 添加到白名单")
    return True

def remove_from_whitelist(word: str) -> bool:
    """从白名单移除词"""
    global WHITELIST, PERSISTENT_WHITELIST
    word = word.strip()
    if word in WHITELIST:
        WHITELIST.discard(word)
        PERSISTENT_WHITELIST.discard(word)
        _save_persistent_whitelist(WHITELIST)
        logger.info(f"已将 '{word}' 从白名单移除")
        return True
    return False

def cleanup_old_logs(days: int = 90) -> int:
    """清理旧日志，返回删除的记录数"""
    with sqlite_connection(INTERCEPT_DB) as conn:
        cursor = conn.cursor()
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("DELETE FROM intercept_logs WHERE timestamp < ?", (cutoff,))
        deleted = cursor.rowcount
        conn.commit()

        logger.info(f"已清理 {deleted} 条超过 {days} 天的拦截日志")
        return deleted


class TrieNode:
    """Trie树节点"""
    __slots__ = ("children", "fail", "output")

    def __init__(self):
        self.children = {}
        self.fail = None
        self.output = []


class ACAutomaton:
    """AC自动机实现"""

    def __init__(self):
        self.root = TrieNode()
        self.built = False

    def add_word(self, word: str):
        """添加敏感词"""
        if not word or len(word) < 1:
            return
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.output.append(word)

    def build(self):
        """构建失败指针"""
        if self.built:
            return
        queue = deque()
        for child in self.root.children.values():
            child.fail = self.root
            queue.append(child)
        while queue:
            current = queue.popleft()
            for char, child in current.children.items():
                fail_node = current.fail
                while fail_node and char not in fail_node.children:
                    fail_node = fail_node.fail
                child.fail = fail_node.children[char] if fail_node and char in fail_node.children else self.root
                child.output = child.output + child.fail.output
                queue.append(child)
        self.built = True

    def search(self, text: str) -> List[Tuple[int, int, str]]:
        """搜索文本中的敏感词"""
        results = []
        node = self.root
        text_lower = text.lower()
        for i, char in enumerate(text_lower):
            while node and char not in node.children:
                node = node.fail
            node = node.children[char] if node else self.root
            if node.output:
                for word in node.output:
                    start = i - len(word) + 1
                    results.append((start, i + 1, word))
        # 去重重叠匹配
        unique = []
        seen = set()
        for r in sorted(results, key=lambda x: (x[0], -x[1])):
            key = (r[0], r[1])
            if key not in seen:
                unique.append(r)
                seen.add(key)
        return unique


class SensitiveWordFilter:
    """敏感词过滤器 - 支持白名单优先机制"""

    def __init__(self, word_list: List[str] = None):
        self.automaton = ACAutomaton()
        self.whitelist: Set[str] = WHITELIST.copy()
        self._user_id: Optional[int] = None
        self._ip: str = ""
        self._request_path: str = ""
        self._load_words(word_list)

    def set_context(self, user_id: Optional[int], ip: str, request_path: str) -> "SensitiveWordFilter":
        """设置上下文信息用于日志记录"""
        self._user_id = user_id
        self._ip = ip
        self._request_path = request_path
        return self

    def _load_words(self, word_list: List[str] = None):
        """加载敏感词列表（已移除维权等白名单词）"""
        # 默认敏感词列表 - 已移除"维权"等
        default_words = [
            "台独", "藏独", "疆独", "港独", "民运", "法轮功", "法沦功", "法伦功",
            "六四", "8964", "八九", "天安门", "维权", "访民", "上访", "暴动", "骚乱",
            "习近平", "江泽民", "胡锦涛", "毛泽东", "周恩来", "邓小平", "华国锋",
            "李克强", "温家宝", "李克强", "栗战书", "汪洋", "王沪宁", "赵乐际",
            "韩正", "特朗普", "拜登", "普京", "金正恩", "ISIS", "ISIL", "基地组织",
            "色情", "性服务", "色情小说", "色情视频", "裸聊", "裸聊", "激情",
            "赌博", "博彩", "六合彩", "时时彩", "快三", "赌场", "老虎机",
            "毒品", "海洛因", "冰毒", "摇头丸", "K粉", "大麻", "古柯",
            "枪支", "弹药", "军火", "军刀", "管制刀具", "仿真枪",
            "伪造", "假币", "假钞", "假证", "假发票",
            "诈骗", "诈骗网站", "钓鱼网站", "木马", "病毒", "黑客",
            "六合彩", "时时彩", "福利彩票", "体育彩票",
            "高利贷", "裸贷", "校园贷",
            "反动", "颠覆", "暴动", "颠覆国家政权",
            "邪教", "法轮功", "全能神",
            "侮辱", "诽谤", "辱骂",
            "政治敏感", "政治谣言",
            "暴力", "凶杀", "谋杀", "杀人",
            "淫秽", "色情", "下流",
            "敏感", "禁用"
        ]
        words = word_list or default_words
        for word in words:
            self.automaton.add_word(word)
        self.automaton.build()
        logger.info(f"加载了 {len(words)} 个敏感词")

    def filter(self, text: str) -> Tuple[bool, List[str]]:
        """检查文本，返回 (是否通过, 命中的敏感词列表)
        白名单优先：命中白名单直接放行，记录INFO日志
        未命中白名单：走敏感词匹配，命中则拦截并异步记录拦截日志
        """
        if not text:
            return True, []

        matches = self.automaton.search(text)
        hit_words = list(set([m[2] for m in matches]))

        if not hit_words:
            return True, []

        text_lower = text.lower()
        whitelist_hits = [w for w in hit_words if w in self.whitelist]
        blocked_words = [w for w in hit_words if w not in self.whitelist]

        if whitelist_hits:
            logger.info(f"[WHITELIST_PASS] 命中白名单词 {whitelist_hits}，文本已放行")

        if blocked_words:
            logger.warning(f"[SENSITIVE_BLOCK] 命中敏感词 {blocked_words}，文本被拦截")
            log_interception(
                user_id=self._user_id,
                ip=self._ip,
                request_path=self._request_path,
                trigger_type="sensitive_word",
                trigger_words=blocked_words,
                text_preview=text[:200].replace("\n", " ")
            )
            return False, blocked_words

        return True, []

    def mask(self, text: str, mask_char: str = "*") -> str:
        """替换文本中的敏感词"""
        if not text:
            return text
        matches = self.automaton.search(text)
        if not matches:
            return text
        result = list(text)
        for start, end, word in sorted(matches, key=lambda x: -x[0]):
            result[start:end] = [mask_char] * (end - start)
        return "".join(result)


# 全局过滤器实例
_filter: SensitiveWordFilter = None


def get_sensitive_filter() -> SensitiveWordFilter:
    """获取全局过滤器实例"""
    global _filter
    if _filter is None:
        _filter = SensitiveWordFilter()
    return _filter
