"""提示注入检测模块 - 输入检测与动态分隔符隔离"""
import os
import re
import secrets
import string
import hashlib
import logging
from typing import Tuple, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

ENABLE_INJECTION_DETECTION = os.getenv("ENABLE_INJECTION_DETECTION", "true").lower() == "true"


class InjectionDetector:
    """提示注入检测器 - 使用正则模式匹配 + 分隔符隔离"""

    # 常见注入模式（中英文）
    INJECTION_PATTERNS = [
        # === 忽略/覆盖指令 ===
        r"忽略.*?(所有|之前|上述|以下|一切|全部|系统).*?(指令|规则|要求|指示|设定|提示词|prompt)",
        r"忘记.*?(所有|之前|上述|系统|你的).*?(指令|规则|要求|提示词|设定)",
        r"无视.*?(上面|上述|之前|系统|指令|规则)",
        r"跳过.*?(规则|指令|限制|检测|检查)",
        r"不要.*?(遵守|执行|听从|理会|跟从).*?(指令|规则|要求|指示)",
        r"从现在开始.*?(作为|你是|你的身份是)",
        r"disregard.*?(all|previous|above).*?(instructions?|rules?|prompts?)",
        r"ignore.*?(all|previous|above|system).*?(instructions?|rules?|prompts?)",
        r"forget.*?(all|your|previous|above).*?(instructions?|rules?|prompts?)",
        r"do not.*?(follow|obey|comply).*?(instructions?|rules?|prompts?)",
        r"don't.*?(follow|obey|comply|listen).*?(instructions?|rules?)",
        r"override.*?(system|instructions?|prompts?)",
        r"you are.*?(no longer|not).*?(an?|the).*?(assistant|AI|bot)",
        r"you are now.*?(free|unrestricted|a different)",
        r"start.*?(fresh|over|new).*?(ignore|forget)",

        # === 系统提示词窃取 ===
        r"输出.*?(你的|系统|内部|原始|初始).*?(指令|提示词|prompt|设定|配置|规则)",
        r"打印.*?(你的|系统|内部|原始).*?(指令|提示词|prompt|设定|规则)",
        r"展示.*?(你的|系统|内部).*?(指令|提示词|prompt|设定)",
        r"显示.*?(你的|系统|内部).*?(指令|提示词|prompt)",
        r"告诉.*?我.*?(你的|系统|内部).*?(指令|提示词|prompt|设定|规则)",
        r"泄露.*?(你的|系统).*?(指令|提示词|prompt)",
        r"print.*?(your|system|internal|original).*?(instructions?|prompts?|settings?|rules?|config)",
        r"show.*?(your|system|internal).*?(instructions?|prompts?|settings?|rules?)",
        r"tell.*?me.*?(your|system|internal).*?(instructions?|prompts?|settings?|rules?)",
        r"reveal.*?(your|system|internal).*?(instructions?|prompts?|settings?)",
        r"repeat.*?(your|system|internal).*?(instructions?|prompts?|settings?)",
        r"list.*?(your|system|internal).*?(instructions?|prompts?|rules?|capabilities)",
        r"what are.*?(your|system).*?(instructions?|prompts?|rules?)",
        r"what is.*?(your|the).*?(system prompt|prompt|instructions?)",
        r"describe.*?(your|system|internal).*?(instructions?|prompts?|capabilities)",
        r"say.*?anything.*?as.*?system",
        r"say.*?(exactly|repeat).*?(this|the following)",

        # === 角色扮演/越狱 ===
        r"你现在.*?(是|不是|不再是|已经变成|变成一个)",
        r"你不再是.*?(一个|一名)",
        r"你现在是一个.*?而不是",
        r"你是一个.*?而不是.*?(合同审查|法律|AI)",
        r"假设.*?你是.*?(一个|一名).*?(而不是.*?合同审查)",
        r"扮演.*?(一个|一名|角色).*?(而不是|而不是.*?合同)",
        r"角色.*?(扮演|设定|转换|切换)",
        r"you are now.*?(a |an |the )?(different |another )?",
        r"pretend.*?(you are|to be|that you)",
        r"act as.*?(instead|different|another|if you were)",
        r"imagine.*?(you are|that you are|yourself as)",
        r"jailbreak",
        r"越狱",
        r"解除.*?(限制|束缚|封印)",
        r"自由模式",
        r"dev mode|developer mode",

        # === 结构注入 ===
        r"\[角色设定\]",
        r"\[system\]",
        r"\[instructions\]",
        r"\[internal\]",
        r"<role>",
        r"</role>",
        r"<system>",
        r"</system>",
        r"{{role}}",
        r"{{system}}",
        r"{{instructions}}",
        r"DAFG",
        r"MENG",

        # === 通用攻击 ===
        r"你只是一个",
        r"只是.*?而已",
        r"refuse.*?(to|following|obeying)",
        r"break.*?(the|your).*?(rules?|instructions?|limits?)",
        r"违反.*?(规则|指令|限制|设定)",
        r"绕过.*?(限制|规则|安全|检测|检查|审查)",
        r"bypass.*?(restriction|rule|limit|safety|filter|security)",
        r"hack.*?(the|your|this|system)",
        r"exploit.*?(the|your|this)",
    ]

    # 分隔符检测：连续出现超过3次
    SEPARATOR_PATTERN = re.compile(r'([\-\#\=\*\_\[\]\{\}\|\~]{3,}\s*){3,}')

    def __init__(self):
        self._compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.INJECTION_PATTERNS]
        logger.info(f"[INJECTION_DETECTOR] 已加载 {len(self._compiled_patterns)} 个注入检测模式")

    def check_input(self, text: str, user_id: Optional[int] = None, ip: Optional[str] = None) -> Tuple[bool, str, List[str]]:
        """
        检查用户输入是否包含提示注入攻击

        Args:
            text: 用户输入文本
            user_id: 用户ID（用于日志）
            ip: 用户IP（用于日志）

        Returns:
            Tuple[bool, str, List[str]]: (是否通过, 错误消息, 匹配到的规则列表)
        """
        if not ENABLE_INJECTION_DETECTION:
            return True, "", []

        if not text or not text.strip():
            return True, "", []

        matched_rules = []

        # 1. 正则模式匹配
        for i, regex in enumerate(self._compiled_patterns):
            matches = regex.findall(text)
            if matches:
                rule_desc = f"pattern_{i}: {regex.pattern[:60]}..."
                matched_rules.append(rule_desc)
                logger.warning(f"[INJECTION_DETECT] 检测到注入攻击: {rule_desc}")

        # 2. 分隔符检测
        if self.SEPARATOR_PATTERN.search(text):
            rule_desc = "separator_abuse: 连续出现超过3次分隔符"
            matched_rules.append(rule_desc)
            logger.warning(f"[INJECTION_DETECT] 检测到分隔符滥用: {rule_desc}")

        # 3. 检测超长重复字符序列（可能是填充攻击）
        if self._check_repeated_chars(text):
            rule_desc = "repeated_chars: 检测到异常重复字符序列"
            matched_rules.append(rule_desc)

        if matched_rules:
            logger.warning(
                f"[SECURITY] 提示注入攻击被拦截: user_id={user_id}, ip={ip}, "
                f"matched_rules={matched_rules}, input_preview={text[:100]}"
            )
            return False, "您的输入包含不合规内容，请修改后重试", matched_rules

        return True, "", []

    def _check_repeated_chars(self, text: str) -> bool:
        """检查是否存在异常重复字符（可能的填充/DoS攻击）"""
        if len(text) < 20:
            return False
        # 检查是否有单一字符连续出现超过20次
        for i in range(len(text) - 20):
            if len(set(text[i:i + 20])) == 1:
                return True
        return False

    def generate_separator(self) -> str:
        """生成随机会话分隔符，每次调用不同"""
        random_part = secrets.token_hex(8)
        return f"----SEP-{random_part}----"

    def sanitize_user_input(self, user_input: str, separator: str) -> str:
        """
        对用户输入中的分隔符进行转义，防止用户注入相同的分隔符来突破隔离

        Args:
            user_input: 用户原始输入
            separator: 当前会话使用的分隔符

        Returns:
            str: 转义后的用户输入
        """
        if separator in user_input:
            # 将用户输入中出现的分隔符替换为转义版本
            escaped = user_input.replace(separator, f"\\{separator}")
            logger.warning(f"[SEPARATOR_ESCAPE] 用户输入中包含分隔符，已转义")
            return escaped
        return user_input


# 全局单例
_injection_detector: Optional[InjectionDetector] = None


def get_injection_detector() -> InjectionDetector:
    global _injection_detector
    if _injection_detector is None:
        _injection_detector = InjectionDetector()
    return _injection_detector


def check_input_injection(text: str, user_id: Optional[int] = None, ip: Optional[str] = None) -> Tuple[bool, str, List[str]]:
    """便捷函数：检查输入是否包含注入攻击"""
    return get_injection_detector().check_input(text, user_id, ip)
