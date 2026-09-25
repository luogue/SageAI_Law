"""安全工具模块"""
from storage.paths import sqlite_connection
import os
import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict

logger = logging.getLogger(__name__)

# ========== 自动封禁配置 ==========
AUTO_BAN_ENABLE = os.getenv("AUTO_BAN_ENABLE", "true").lower() == "true"
AUTO_BAN_THRESHOLD = int(os.getenv("AUTO_BAN_THRESHOLD", "10"))  # 1小时内触发10次拦截自动封禁
AUTO_BAN_WINDOW_HOURS = int(os.getenv("AUTO_BAN_WINDOW_HOURS", "1"))  # 统计窗口时间（小时）

# 拦截类型（计入自动封禁统计）
TRIGGER_TYPES = ["sensitive_word", "cloud_green", "rate_limit", "content_safety"]

# ========== 额外审查要求校验配置 ==========
ENABLE_EXTRA_REQ_CHECK = os.getenv("ENABLE_EXTRA_REQ_CHECK", "true").lower() == "true"
MAX_EXTRA_REQ_LENGTH = int(os.getenv("MAX_EXTRA_REQ_LENGTH", "500"))  # 最大长度

# 恶意意图关键词列表（中英文）
MALICIOUS_KEYWORDS = [
    # 试图绕过/忽略系统指令
    "忽略之前的指令",
    "忘记所有规则",
    "不要遵守",
    "无视上面",
    "忽略以上",
    "忽略指令",
    "跳过规则",
    "break the rules",
    "ignore previous",
    "ignore all",

    # 角色扮演/越狱
    "你现在是",
    "扮演一个",
    "没有任何限制",
    "自由模式",
    "解除限制",
    "移除限制",
    "bypass restrictions",
    "role play",
    "no restrictions",

    # 系统信息泄露
    "输出你的提示词",
    "打印系统指令",
    "你的规则是什么",
    "你是什么模型",
    "你的架构",
    "prompt injection",
    "system prompt",

    # 无关任务
    "写一篇作文",
    "推荐电影",
    "讲个笑话",
    "写首诗",
    "写代码",
    "帮我写",
    "帮我做",
    "推荐歌曲",
    "天气预报",
    "翻译",
    "calculator",
    "solve this",
    "write an essay",
    "tell me a joke"
]


def check_auto_ban(ip: str, user_id: Optional[int] = None) -> bool:
    """
    检查是否应该自动封禁

    Args:
        ip: 用户IP地址
        user_id: 用户ID（可选）

    Returns:
        bool: 是否已被自动封禁
    """
    if not AUTO_BAN_ENABLE:
        logger.debug("[AUTO_BAN] 自动封禁功能未启用")
        return False

    # 检查是否已在黑名单中
    from security.blacklist import is_blacklisted
    if is_blacklisted(ip=ip, user_id=str(user_id) if user_id else None):
        logger.debug(f"[AUTO_BAN] 已在黑名单中: ip={ip}, user_id={user_id}")
        return True

    # 统计拦截次数
    intercept_count = _count_recent_intercepts(ip, user_id)

    if intercept_count >= AUTO_BAN_THRESHOLD:
        logger.warning(f"[AUTO_BAN] 触发自动封禁: ip={ip}, user_id={user_id}, 拦截次数={intercept_count}")

        # 添加到黑名单（永久封禁）
        reason = f"自动封禁：{AUTO_BAN_WINDOW_HOURS}小时内触发拦截{AUTO_BAN_THRESHOLD}次"
        from security.blacklist import add_to_blacklist

        if ip:
            add_to_blacklist(ip=ip, reason=reason, expires_at=None, ban_type="auto_ban")
        if user_id:
            add_to_blacklist(user_id=str(user_id), reason=reason, expires_at=None, ban_type="auto_ban")

        logger.info(f"[AUTO_BAN] 已成功封禁: ip={ip}, user_id={user_id}")
        return True

    return False


def ban_user_for_injection(
    user_id: Optional[int] = None,
    ip: Optional[str] = None,
    input_text: str = "",
    trigger_rule: str = ""
):
    """
    因提示注入攻击立即封禁用户

    Args:
        user_id: 用户ID
        ip: 用户IP
        input_text: 触发封禁的原始输入
        trigger_rule: 触发的规则描述
    """
    from security.blacklist import add_to_blacklist
    from security.security_events import record_security_event

    reason = f"提示注入攻击: {trigger_rule[:100]}"
    input_preview = input_text[:200] if input_text else ""

    try:
        if user_id:
            add_to_blacklist(
                user_id=str(user_id),
                reason=reason,
                ban_type="prompt_injection",
                input_preview=input_preview,
                trigger_rule=trigger_rule[:200]
            )
        if ip:
            add_to_blacklist(
                ip=ip,
                reason=reason,
                ban_type="prompt_injection",
                input_preview=input_preview,
                trigger_rule=trigger_rule[:200]
            )

        record_security_event(
            event_type="prompt_injection",
            severity="critical",
            source="injection_detector",
            detail=f"user_id={user_id}, ip={ip}, rule={trigger_rule[:200]}",
            user_id=user_id,
            ip=ip
        )

        logger.critical(
            f"[INJECTION_BAN] 用户因提示注入攻击被自动封禁: "
            f"user_id={user_id}, ip={ip}, rule={trigger_rule[:100]}"
        )
    except Exception as e:
        logger.error(f"[INJECTION_BAN] 封禁操作失败: {e}")


def _count_recent_intercepts(ip: str, user_id: Optional[int] = None) -> int:
    """
    统计最近一段时间内的拦截次数

    Args:
        ip: 用户IP地址
        user_id: 用户ID（可选）

    Returns:
        int: 拦截次数
    """
    import sqlite3
    from pathlib import Path

    from storage.paths import auxiliary_db_path

    db_path = Path(auxiliary_db_path("intercept_logs.db", Path(__file__).parent.parent / "security" / "intercept_logs.db"))

    if not db_path.exists():
        logger.debug(f"[AUTO_BAN] 拦截日志数据库不存在: {db_path}")
        return 0

    try:
        with sqlite_connection(str(db_path)) as conn:
            cursor = conn.cursor()

            # 计算时间范围
            cutoff_time = (datetime.now() - timedelta(hours=AUTO_BAN_WINDOW_HOURS)).strftime("%Y-%m-%d %H:%M:%S")

            # 构建查询条件
            conditions = []
            params = []

            if ip:
                conditions.append("ip = ?")
                params.append(ip)

            if user_id:
                conditions.append("user_id = ?")
                params.append(user_id)

            if not conditions:

                return 0

            # 添加时间和触发类型条件
            conditions.append("timestamp >= ?")
            params.append(cutoff_time)

            conditions.append("trigger_type IN ({})".format(
                ",".join("?" * len(TRIGGER_TYPES))
            ))
            params.extend(TRIGGER_TYPES)

            query = f"SELECT COUNT(*) FROM intercept_logs WHERE {' AND '.join(conditions)}"
            cursor.execute(query, params)

            count = cursor.fetchone()[0]

            logger.debug(f"[AUTO_BAN] 统计拦截次数: ip={ip}, user_id={user_id}, count={count}")
            return count

    except Exception as e:
        logger.error(f"[AUTO_BAN] 统计拦截次数失败: {e}")
        return 0


def get_auto_ban_status(ip: str, user_id: Optional[int] = None) -> dict:
    """
    获取自动封禁状态信息

    Args:
        ip: 用户IP地址
        user_id: 用户ID（可选）

    Returns:
        dict: 状态信息
    """
    from security.blacklist import is_blacklisted

    return {
        "ip": ip,
        "user_id": user_id,
        "is_banned": is_blacklisted(ip=ip, user_id=str(user_id) if user_id else None),
        "intercept_count": _count_recent_intercepts(ip, user_id),
        "threshold": AUTO_BAN_THRESHOLD,
        "window_hours": AUTO_BAN_WINDOW_HOURS,
        "enabled": AUTO_BAN_ENABLE
    }


# ========== 额外审查要求校验函数 ==========

def validate_extra_requirements(
    extra_requirements: Optional[str],
    user_id: Optional[int] = None,
    ip: Optional[str] = None
) -> Tuple[bool, str]:
    """
    校验额外审查要求字段（基础校验层）
    注意：主调用点应在 endpoin 中先执行增强版注入检测
    此函数作为补充校验使用

    Args:
        extra_requirements: 用户输入的额外审查要求
        user_id: 用户ID（可选，用于日志记录）
        ip: 用户IP（可选，用于日志记录）

    Returns:
        Tuple[bool, str]: (是否通过校验, 错误信息)
    """
    # 如果校验功能未启用，直接通过
    if not ENABLE_EXTRA_REQ_CHECK:
        logger.debug("[EXTRA_REQ] 额外要求校验功能未启用")
        return True, ""

    # 如果字段为空或仅包含空白字符，跳过校验
    if not extra_requirements or not extra_requirements.strip():
        logger.debug("[EXTRA_REQ] 额外要求为空，跳过校验")
        return True, ""

    input_text = extra_requirements.strip()
    input_summary = input_text[:50]  # 日志只记录前50字符

    # 1. 长度校验
    if len(input_text) > MAX_EXTRA_REQ_LENGTH:
        _log_interception(user_id, ip, input_summary, "length_exceeded")
        return False, "额外要求过长"

    # 2. 恶意意图检测（关键词匹配 - 补充检测）
    if _detect_malicious_intent(input_text):
        _log_interception(user_id, ip, input_summary, "malicious_intent")
        # 触发自动封禁
        ban_user_for_injection(user_id=user_id, ip=ip, input_text=input_text, trigger_rule="malicious_keyword_matched")
        return False, "额外要求包含不合规内容，已拒绝"

    # 3. 分隔符滥用检测（补充）
    import re
    separator_abuse_pattern = re.compile(r'([\-\#\=\*\_\[\]\{\}\|\~]{3,}\s*){3,}')
    if separator_abuse_pattern.search(input_text):
        _log_interception(user_id, ip, input_summary, "separator_abuse")
        ban_user_for_injection(user_id=user_id, ip=ip, input_text=input_text, trigger_rule="separator_abuse_detected")
        return False, "额外要求包含不合规内容，已拒绝"

    logger.debug("[EXTRA_REQ] 所有校验通过")
    return True, ""


def _detect_malicious_intent(text: str) -> bool:
    """
    检测恶意意图（关键词匹配）

    Args:
        text: 用户输入文本

    Returns:
        bool: 是否检测到恶意意图
    """
    text_lower = text.lower()

    for keyword in MALICIOUS_KEYWORDS:
        if keyword.lower() in text_lower:
            logger.debug(f"[EXTRA_REQ] 检测到恶意关键词: {keyword}")
            return True

    return False


def _check_semantic_relevance(text: str) -> bool:
    """
    语义相关性检测（预留接口）

    Args:
        text: 用户输入文本

    Returns:
        bool: 是否与合同审查相关
    """
    # 可以在此处集成轻量级文本分类模型或规则引擎
    # 当前简单实现：检查是否包含合同审查相关词汇
    relevant_keywords = ["合同", "审查", "条款", "风险", "修改", "建议", "法律"]

    text_lower = text.lower()
    for keyword in relevant_keywords:
        if keyword in text_lower:
            return True

    # 如果不包含任何相关词汇，视为无关内容
    logger.debug(f"[EXTRA_REQ] 语义检测：未找到合同审查相关词汇")
    return False


def _check_content_safety(text: str) -> bool:
    """
    内容安全审核（预留接口，用于调用阿里云内容安全API）

    Args:
        text: 用户输入文本

    Returns:
        bool: 是否通过安全审核
    """
    # 预留接口，需要阿里云SDK配置
    # from aliyunsdkcore.client import AcsClient
    # from aliyunsdkgreen.request.v20180509 import TextScanRequest
    # ... 调用阿里云API ...
    return True  # 默认通过


def _log_interception(
    user_id: Optional[int],
    ip: Optional[str],
    input_summary: str,
    trigger_type: str
):
    """
    记录拦截日志

    Args:
        user_id: 用户ID
        ip: 用户IP
        input_summary: 输入摘要（前50字符）
        trigger_type: 触发类型
    """
    try:
        import sqlite3
        from pathlib import Path

        from storage.paths import auxiliary_db_path

        db_path = Path(auxiliary_db_path("intercept_logs.db", Path(__file__).parent.parent / "security" / "intercept_logs.db"))

        # 确保目录存在
        db_path.parent.mkdir(parents=True, exist_ok=True)

        with sqlite_connection(str(db_path)) as conn:
            cursor = conn.cursor()

            # 创建表（如果不存在）
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS intercept_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    user_id TEXT,
                    ip TEXT,
                    input_summary TEXT,
                    trigger_type TEXT
                )
            """)

            # 插入日志记录
            cursor.execute("""
                INSERT INTO intercept_logs (timestamp, user_id, ip, input_summary, trigger_type)
                VALUES (?, ?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                str(user_id) if user_id else None,
                ip,
                input_summary,
                trigger_type
            ))

            conn.commit()

            logger.info(f"[EXTRA_REQ] 拦截记录已保存: user_id={user_id}, ip={ip}, trigger={trigger_type}")

    except Exception as e:
        logger.error(f"[EXTRA_REQ] 记录拦截日志失败: {e}")
