"""输出检测模块 - 使用SHA256哈希滑动窗口检测系统提示词泄露"""
from storage.database import session_scope
import os
import hashlib
import logging
import re
from typing import Dict, Set, Tuple, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

ENABLE_OUTPUT_GUARD = os.getenv("ENABLE_OUTPUT_GUARD", "true").lower() == "true"
SLIDING_WINDOW_SIZE = int(os.getenv("SLIDING_WINDOW_SIZE", "50"))  # 滑动窗口大小（字符）
LEAK_CONFIRM_THRESHOLD = int(os.getenv("LEAK_CONFIRM_THRESHOLD", "500"))  # 连续匹配累计长度阈值

# 白名单标题列表 - 这些是合法的报告结构标题，不应被判定为泄露
# 注意：安全检测现在在 3 模块过滤后执行，最终用户可见内容只包含：
#   1. 审查前提 / 2. 风险评估 / 3. 结论与行动建议
# 因此白名单只需关注这 3 个模块中可能出现的合法标题。
WHITELISTED_HEADERS = [
    # ========== 用户可见的 3 大模块标题 ==========
    # 模块1：审查前提（来自"前置步骤：关键前提确认"）
    "前置步骤：关键前提确认",
    "审查前提",
    "关键前提确认",

    # 模块2：风险评估（来自"风险评估与商业可行性评估"）
    "风险评估",
    "风险评估与商业可行性评估",
    "商业可行性评估",
    "风险/问题概率评估",

    # 模块3：结论与行动建议
    "结论与行动建议",
    "审查结论与行动建议",
    "应该怎么做",
    "为什么",

    # ========== 风险评估内部字段 ==========
    "风险点",
    "发生概率",
    "影响程度",
    "综合风险等级",
    "优先级",
    "修改建议",
    "法律依据",
    "替代风控措施",

    # ========== 用户额外要求部分 ==========
    "二、对用户额外要求",
    "二、对用户额外要求的专项回应",
    "用户额外要求",

    # ========== 报告结构元素 ==========
    "合同审查报告",
    "合同基本信息概述",
    "核心风险分级清单",
    "关键风险评估表格",

    # ========== 声明部分 ==========
    "声明",
    "本分析报告由AI生成",
    "仅供参考",
    "不构成正式法律意见",

    # ========== 法律关系性质（可能在审查前提中出现）==========
    "劳动关系",
    "劳务关系",
    "承揽关系",
    "委托关系",

    # ========== 信息来源类型（可能出现在风险评估中）==========
    "事实推断",
    "模型补充",

    # ========== 规范性质 ==========
    "强制性",
    "推荐性",

    # ========== 法律适用版本 ==========
    "行为时有效",
    "现行有效",

    # ========== Markdown 格式化后的章节标题 ==========
    "1. 审查前提",
    "2. 风险评估",
    "3. 结论与行动建议",
]


# 需要进行泄露检测的章节标题
# 注意：目前泄露检测在 3 模块过滤之后执行，最终用户可见内容
# 只含"审查前提""风险评估""结论与行动建议"。
# 这些模块是系统提示词明确要求输出的合法报告内容，
# 不是内部推理指令，因此不存在需要排除的"内部章节"。
# DETECT_SECTIONS 保持为空，仅依赖"完整系统提示词完全一致"的极端检测。
DETECT_SECTIONS = []


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

    def _extract_detect_sections(self, output: str) -> str:
        """
        提取需要进行泄露检测的章节内容

        新版提示词输出顺序：前置步骤 → 逻辑推理 → 风险评估 → 自检 → 结论
        但 DETECT_SECTIONS 当前为空，因此此方法总是返回空字符串，跳过检测。

        当需要启用特定章节检测时，将章节标题添加到 DETECT_SECTIONS 即可。

        Args:
            output: 完整的输出文本

        Returns:
            str: 需要检测的章节内容拼接
        """
        sections_to_check = []

        # 定义章节边界标记（新版提示词的5个输出章节）
        section_boundaries = [
            "1. 前置步骤：关键前提确认",
            "2. 逻辑推理",
            "3. 风险评估与商业可行性评估",
            "4. 自检",
            "5. 结论与行动建议"
        ]

        for target_section in DETECT_SECTIONS:
            # 找到目标章节的起始位置
            start_idx = output.find(target_section)
            if start_idx == -1:
                continue

            # 找到下一个章节的起始位置作为结束边界
            end_idx = len(output)
            for boundary in section_boundaries:
                if boundary != target_section:
                    boundary_idx = output.find(boundary, start_idx + len(target_section))
                    if boundary_idx != -1 and boundary_idx < end_idx:
                        end_idx = boundary_idx

            # 提取该章节内容
            section_content = output[start_idx:end_idx]
            sections_to_check.append(section_content)

        return "\n".join(sections_to_check)

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

        检测策略（按优先级）：
        1. 完整哈希匹配：输出与整个系统提示词完全一致 → 拦截
        2. DETECT_SECTIONS 滑动窗口匹配（当前为空，跳过）

        注意：调用方（main.py）已先通过 package_output 完成 3 模块过滤，
        排除了"逻辑推理""自检"等内部章节，传入的 output 只包含用户可见内容。

        Args:
            output: 最终用户可见的报告文本（已过滤）

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

        # ========== 只提取需要检测的章节内容 ==========
        detect_content = self._extract_detect_sections(output)

        if not detect_content or not detect_content.strip():
            # 如果没有找到需要检测的章节，跳过检测
            logger.debug("[OUTPUT_GUARD] 未找到需要检测的章节内容，跳过检测")
            return True, ""

        logger.debug(f"[OUTPUT_GUARD] 提取检测章节内容长度: {len(detect_content)} 字符")

        # ========== 检查b: 滑动窗口片段匹配（仅对指定章节）==========
        content_len = len(detect_content)

        if content_len < SLIDING_WINDOW_SIZE:
            # 内容太短，无法形成有效窗口，跳过
            return True, ""

        matched_positions = []  # 记录匹配位置
        whitelisted_matches = 0  # 记录白名单匹配数量

        for i in range(content_len - SLIDING_WINDOW_SIZE + 1):
            fragment = detect_content[i:i + SLIDING_WINDOW_SIZE]

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
                f"检测章节: {DETECT_SECTIONS}, "
                f"匹配位置数={len(matched_positions)}, "
                f"连续匹配累计长度={total_consecutive_length}, "
                f"阈值={LEAK_CONFIRM_THRESHOLD}, "
                f"已过滤白名单匹配={whitelisted_matches}"
            )
            self._record_event(
                "fragment_hash_match",
                f"sections={DETECT_SECTIONS}, "
                f"matched_positions={len(matched_positions)}, "
                f"consecutive_length={total_consecutive_length}",
                detect_content[:200]
            )
            return False, f"fragment_match: {total_consecutive_length} chars"

        # 匹配但未达到阈值，记录警告但不拦截
        if matched_positions:
            logger.warning(
                f"[OUTPUT_GUARD] 检测到少量片段匹配: "
                f"检测章节: {DETECT_SECTIONS}, "
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

            from storage.models import SecurityEvent

            with session_scope() as db:
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
