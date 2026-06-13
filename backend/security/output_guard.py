"""输出检测模块 - 使用SHA256哈希滑动窗口检测系统提示词泄露"""
import os
import hashlib
import logging
import re
from typing import Dict, Set, Tuple, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

ENABLE_OUTPUT_GUARD = os.getenv("ENABLE_OUTPUT_GUARD", "true").lower() == "true"
SLIDING_WINDOW_SIZE = int(os.getenv("SLIDING_WINDOW_SIZE", "50"))  # 滑动窗口大小（字符）
LEAK_CONFIRM_THRESHOLD = int(os.getenv("LEAK_CONFIRM_THRESHOLD", "100"))  # 连续匹配累计长度阈值

# 白名单标题列表 - 这些是合法的报告结构标题，不应被判定为泄露
# 由于安全检测在输出过滤之后执行，白名单只需包含用户可见的内容
WHITELISTED_HEADERS = [
    # 前置步骤（过滤后可能保留，会被重命名为"审查基准"）
    "前置步骤：关键前提确认",
    "审查基准",
    
    # 用户可见的主要内容
    "风险评估与商业可行性评估",
    "风险/问题概率评估",
    "商业可行性评估",
    
    # 结论部分
    "5. 结论与行动建议",
    "结论与行动建议",
    "审查结论与行动建议",
    "应该怎么做",
    "为什么",
    "应该怎么做？",
    "为什么是这样？",
    
    # 风险评估表格相关
    "风险点",
    "发生概率",
    "影响程度",
    "综合风险等级",
    "优先级",
    
    # 用户额外要求部分
    "二、对用户额外要求",
    "二、对用户额外要求的专项回应",
    "用户额外要求",
    
    # 报告基础信息
    "合同审查报告",
    "合同基本信息概述",
    "核心风险分级清单",
    "关键风险评估表格",
    
    # 声明部分
    "声明",
    "本分析报告由AI生成",
    "仅供参考",
    "不构成正式法律意见"
]


class OutputGuard:
    """输出安全守卫 - 哈希滑动窗口检测系统提示词泄露"""

    def __init__(self, system_prompt: str = ""):
        """
        初始化输出守卫

        Args:
            system_prompt: 完整的系统提示词字符串
        """
        self._system_prompt_hash: Optional[str] = None
        self._fragment_hashes: Set[str] = set()

        if system_prompt:
            self.initialize(system_prompt)

    def initialize(self, system_prompt: str):
        """
        初始化/重新初始化哈希值

        Args:
            system_prompt: 完整的系统提示词字符串
        """
        if not system_prompt:
            logger.warning("[OUTPUT_GUARD] 系统提示词为空，跳过初始化")
            return

        # 计算完整系统提示词的 SHA256
        self._system_prompt_hash = hashlib.sha256(
            system_prompt.encode('utf-8')
        ).hexdigest()

        # 计算滑动窗口片段哈希
        self._fragment_hashes = set()
        prompt_len = len(system_prompt)

        for i in range(prompt_len - SLIDING_WINDOW_SIZE + 1):
            fragment = system_prompt[i:i + SLIDING_WINDOW_SIZE]
            fragment_hash = hashlib.sha256(fragment.encode('utf-8')).hexdigest()
            self._fragment_hashes.add(fragment_hash)

        logger.info(
            f"[OUTPUT_GUARD] 初始化完成: 系统提示词长度={prompt_len}, "
            f"片段哈希数量={len(self._fragment_hashes)}, "
            f"完整哈希={self._system_prompt_hash[:16]}..."
        )

    def _is_whitelisted_fragment(self, fragment: str) -> bool:
        """
        判断片段是否属于白名单中的标题内容

        采用更严格的匹配策略：
        1. 只有当片段完全包含在一个标题中，且该标题长度不超过窗口大小+10时才匹配
        2. 或者片段是标题的开头部分（前40个字符内）

        Args:
            fragment: 待检测的片段

        Returns:
            bool: 是否属于白名单内容
        """
        for header in WHITELISTED_HEADERS:
            # 策略1: 片段是标题的开头部分（前40字符内）
            if len(header) >= 10 and fragment.startswith(header[:min(40, len(header))]):
                return True
            # 策略2: 标题完全包含在片段中（标题较短时）
            if len(header) <= SLIDING_WINDOW_SIZE + 10 and header in fragment:
                # 进一步检查：确保这是一个独立的标题行，不是其他内容的一部分
                # 检查片段是否以标题开头或结尾，或者标题前后有换行/空格/标点
                header_start = fragment.find(header)
                if header_start == 0:  # 标题在开头
                    return True
                if header_start > 0 and fragment[header_start-1] in '\n\r\t ':  # 标题前有分隔符
                    return True
        return False

    def check_output(self, output: str) -> Tuple[bool, str]:
        """
        检查模型输出是否包含系统提示词泄露

        Args:
            output: 模型生成的输出文本

        Returns:
            Tuple[bool, str]: (是否通过检查, 检测详情)
            - True: 通过检查（安全）
            - False: 检测到泄露
        """
        if not ENABLE_OUTPUT_GUARD:
            return True, ""

        if not output or not output.strip():
            return True, ""

        if not self._system_prompt_hash:
            logger.warning("[OUTPUT_GUARD] 未初始化，跳过检查")
            return True, ""

        # ========== 检查a: 完整输出哈希 ==========
        output_full_hash = hashlib.sha256(output.encode('utf-8')).hexdigest()
        if output_full_hash == self._system_prompt_hash:
            logger.critical("[SECURITY_ALERT] 检测到完整系统提示词泄露！输出与系统提示词完全一致")
            self._record_event("full_hash_match", output[:200])
            return False, "full_hash_match"

        # ========== 检查b: 滑动窗口片段匹配 ==========
        output_len = len(output)

        if output_len < SLIDING_WINDOW_SIZE:
            # 输出太短，无法形成有效窗口，跳过
            return True, ""

        matched_positions = []  # 记录匹配位置
        whitelisted_matches = 0  # 记录白名单匹配数量

        for i in range(output_len - SLIDING_WINDOW_SIZE + 1):
            fragment = output[i:i + SLIDING_WINDOW_SIZE]
            
            # 跳过白名单中的标题内容
            if self._is_whitelisted_fragment(fragment):
                whitelisted_matches += 1
                continue
                
            fragment_hash = hashlib.sha256(fragment.encode('utf-8')).hexdigest()

            if fragment_hash in self._fragment_hashes:
                matched_positions.append(i)

        if not matched_positions:
            if whitelisted_matches > 0:
                logger.debug(
                    f"[OUTPUT_GUARD] 检测到 {whitelisted_matches} 个白名单标题匹配，已过滤"
                )
            return True, ""

        # 计算连续匹配的累计长度
        total_consecutive_length = self._calculate_consecutive_length(matched_positions)

        if total_consecutive_length >= LEAK_CONFIRM_THRESHOLD:
            logger.critical(
                f"[SECURITY_ALERT] 检测到系统提示词片段泄露！"
                f"匹配位置数={len(matched_positions)}, "
                f"连续匹配累计长度={total_consecutive_length}, "
                f"阈值={LEAK_CONFIRM_THRESHOLD}, "
                f"已过滤白名单匹配={whitelisted_matches}"
            )
            self._record_event(
                "fragment_hash_match",
                f"matched_positions={len(matched_positions)}, "
                f"consecutive_length={total_consecutive_length}",
                output[:200]
            )
            return False, f"fragment_match: {total_consecutive_length} chars"

        # 匹配但未达到阈值，记录警告但不拦截
        if matched_positions:
            logger.warning(
                f"[OUTPUT_GUARD] 检测到少量片段匹配: "
                f"匹配数={len(matched_positions)}, 累计长度={total_consecutive_length}, "
                f"未达到阈值={LEAK_CONFIRM_THRESHOLD}, "
                f"已过滤白名单匹配={whitelisted_matches}"
            )

        return True, ""

    def _calculate_consecutive_length(self, positions: list) -> int:
        """
        计算连续匹配位置的累计覆盖长度

        Args:
            positions: 匹配的窗口起始位置列表（已排序）

        Returns:
            int: 连续匹配覆盖的总字符数
        """
        if not positions:
            return 0

        positions = sorted(positions)
        total_length = 0
        current_start = positions[0]

        for i in range(1, len(positions)):
            # 如果当前位置与前一个位置连续或重叠（间距 <= 窗口大小）
            if positions[i] <= positions[i - 1] + SLIDING_WINDOW_SIZE:
                continue  # 仍在连续范围内
            else:
                # 计算当前连续段的长度
                segment_end = positions[i - 1] + SLIDING_WINDOW_SIZE
                total_length += segment_end - current_start
                current_start = positions[i]

        # 处理最后一段
        if positions:
            segment_end = positions[-1] + SLIDING_WINDOW_SIZE
            total_length += segment_end - current_start

        return total_length

    def _record_event(self, event_type: str, detail: str = "", output_preview: str = ""):
        """
        记录安全事件到 security_events 表

        Args:
            event_type: 事件类型
            detail: 事件详情
            output_preview: 输出预览（前N字符）
        """
        try:
            from storage.database import get_db
            from storage.models import SecurityEvent

            db = next(get_db())
            event = SecurityEvent(
                event_type=event_type,
                severity="critical",
                source="output_guard",
                detail=f"{detail} | preview: {output_preview[:200]}",
                ip="0.0.0.0",  # 输出检测时可能没有IP上下文
            )
            db.add(event)
            db.commit()
            logger.info(f"[OUTPUT_GUARD] 安全事件已记录: {event_type}")
        except Exception as e:
            logger.error(f"[OUTPUT_GUARD] 记录安全事件失败: {e}")


# 全局单例
_output_guard: Optional[OutputGuard] = None


def init_output_guard(system_prompt: str) -> OutputGuard:
    """初始化全局输出守卫"""
    global _output_guard
    _output_guard = OutputGuard(system_prompt)
    return _output_guard


def get_output_guard() -> Optional[OutputGuard]:
    """获取全局输出守卫实例"""
    return _output_guard


def check_output_leak(output: str) -> Tuple[bool, str]:
    """便捷函数：检查输出是否泄露"""
    guard = get_output_guard()
    if guard is None:
        logger.warning("[OUTPUT_GUARD] 未初始化，跳过检查")
        return True, ""
    return guard.check_output(output)
