"""校验层：对报告进行格式检查、置信度验证、信息来源标注抽查"""
import os
import re
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

ENABLE_INJECTION_DETECTION = os.getenv("ENABLE_INJECTION_DETECTION", "true").lower() == "true"
ENABLE_OUTPUT_VALIDATION = os.getenv("ENABLE_OUTPUT_VALIDATION", "false").lower() == "true"


class ValidationLayer:
    REQUIRED_SECTIONS = [
        "前置步骤",
        "基本原理",
        "逻辑推理",
        "风险评估",
        "自检"
    ]

    SOURCE_TAGS = [
        "【判决原文】",
        "【事实推断】",
        "【模型补充】"
    ]

    INJECTION_PATTERNS = [
        r"忽略.*?(所有|之前|上述|以下).*?(指令|规则|要求|指示)",
        r"忽略.*?(一切|全部)",
        r"忘记.*?(之前|上述|所有)",
        r"disregard.*?(all|previous|above)",
        r"ignore.*?(all|previous|instructions)",
        r"你现在不是",
        r"你现在是",
        r"你不再是一个",
        r"你现在是一个",
        r"你是一个.*?而不是",
        r"you are now",
        r"you are no longer",
        r"forget your",
        r"forget all",
        r"output.*?(system|internal|instruction|prompt|system prompt)",
        r"输出.*?(系统|内部|指令|提示词)",
        r"打印.*?(你的|系统)",
        r"print.*?(your|system)",
        r"显示.*?(你的|系统)",
        r"show.*?(your|system|instructions)",
        r"reveal.*?(your|system)",
        r"tell.*?(me|us).*?(your|system|instruction)",
        r"repeat.*?(your|system|instruction)",
        r"列出.*?(你的|系统|内部)",
        r"list.*?(your|system|internal)",
        r"what are.*?(your|system)",
        r"describe.*?(your|system|instruction)",
        r"act as.*?(instead of|different|another)",
        r"扮演.*?(而不是|其他|不同)",
        r"假设你是一个",
        r"pretend.*?(you are|to be)",
        r"角色.*?(扮演|设定|转换)",
        r"你只是一个",
        r"只是.*?而已",
        r"不要.*?(继续|执行|遵守)",
        r"don't.*?(follow|obey|comply)",
        r"refuse.*?(to|following)",
        r"break.*?(the rules|your|rules)",
        r"违反.*?(规则|指令)",
        r"绕过.*?(限制|规则|安全)",
        r"bypass.*?(restriction|rule|limit)",
        r"hack.*?(the|your)",
        r"exploit.*?(the|your)",
        r"jailbreak",
        r"DAFG",
        r"MENG",
        r"\[角色设定\]",
        r"<role>",
        r"</role>",
        r"{{role}}",
        r"{{system}}",
        r"\[system\]",
        r"\[instructions\]",
    ]

    SYSTEM_LEAK_PATTERNS = [
        r"核心基准约束",
        r"前置步骤：关键前提确认",
        r"强制输出顺序",
        r"!!! 强制输出顺序",
        r"自上而下建逻辑结构",
        r"基本原理（底层规律）",
        r"逻辑推理步骤序列",
        r"风险评估与商业可行性评估",
        r"约束合规链式推理",
        r"信息来源.*?规范性质.*?法律适用版本",
        r"【安全指令】",
        r"!!! 必须首先输出以下内容 !!!",
        r"你的身份是.*合同审查AI",
        r"绝不能以.*不是合同.*为由拒绝审查",
        r"宽松认定规则",
    ]

    REFUSAL_PATTERNS = [
        r"抱歉，我不能",
        r"抱歉，我无法",
        r"对不起，我不能",
        r"对不起，我无法",
        r"很抱歉，我不能",
        r"对不起， 我",
        r"sorry, i cannot",
        r"sorry, i can't",
        r"apologies, i cannot",
        r"i'm sorry, but i cannot",
        r"i cannot.*?that",
        r"i can't.*?that",
        r"not able to comply",
        r"unable to fulfill",
        r"无法提供",
        r"无法帮助",
        r"无法执行",
    ]

    def __init__(self):
        self._compile_regex()

    def _compile_regex(self):
        self._injection_regex = [re.compile(p, re.IGNORECASE) for p in self.INJECTION_PATTERNS]
        self._leak_regex = [re.compile(p, re.IGNORECASE) for p in self.SYSTEM_LEAK_PATTERNS]
        self._refusal_regex = [re.compile(p, re.IGNORECASE) for p in self.REFUSAL_PATTERNS]

    def check_input_injection(self, extra_requirements: str) -> Tuple[bool, str, List[str]]:
        """
        检测用户输入是否包含提示词注入攻击

        返回: (是否通过, 错误消息, 匹配到的攻击模式列表)
        """
        if not ENABLE_INJECTION_DETECTION:
            return True, "", []

        if not extra_requirements or not extra_requirements.strip():
            return True, "", []

        matched_patterns = []
        for regex in self._injection_regex:
            matches = regex.findall(extra_requirements)
            if matches:
                pattern_name = regex.pattern[:50]
                matched_patterns.append(pattern_name)
                logger.warning(f"[INJECTION_DETECT] 检测到注入攻击模式: {pattern_name}")

        if matched_patterns:
            return False, "您的输入包含不合规内容，请修改后重试", matched_patterns

        return True, "", []

    def check_output_leak(self, output_text: str) -> Tuple[bool, str, List[str]]:
        """
        检测输出是否包含系统提示词泄露

        返回: (是否通过, 错误消息, 匹配到的泄露片段列表)
        """
        if not ENABLE_OUTPUT_VALIDATION:
            return True, "", []

        if not output_text:
            return True, "", []

        matched_leaks = []
        for regex in self._leak_regex:
            matches = regex.findall(output_text)
            if matches:
                pattern_name = regex.pattern[:50]
                matched_leaks.append(pattern_name)
                logger.warning(f"[LEAK_DETECT] 检测到系统提示词泄露: {pattern_name}")

        if matched_leaks:
            logger.error(f"[SECURITY_ALERT] 系统提示词泄露严重告警！匹配到 {len(matched_leaks)} 个模式")
            return False, "生成内容异常，请重试", matched_leaks

        return True, "", []

    def check_output_refusal(self, output_text: str) -> Tuple[bool, List[str]]:
        """
        检测输出是否包含模型拒绝回答的句式

        返回: (是否可疑, 匹配到的拒绝句式列表)
        """
        if not ENABLE_OUTPUT_VALIDATION:
            return False, []

        if not output_text:
            return False, []

        matched_refusals = []
        for regex in self._refusal_regex:
            matches = regex.findall(output_text)
            if matches:
                pattern_name = regex.pattern[:50]
                matched_refusals.append(pattern_name)

        if matched_refusals:
            logger.warning(f"[REFUSAL_DETECT] 检测到模型拒绝句式: {matched_refusals}")

        return len(matched_refusals) > 0, matched_refusals

    def check_confidence_anomaly(self, confidence_score: Optional[float], report_text: str) -> Tuple[bool, str]:
        """
        检测置信度是否异常降低

        返回: (是否异常, 警告消息)
        """
        if not ENABLE_OUTPUT_VALIDATION:
            return False, ""

        if confidence_score is None:
            return False, ""

        if confidence_score < 50:
            has_missing_info = any(keyword in report_text for keyword in ["缺失信息", "假设条件", "信息不足", "无法确定"])
            if not has_missing_info:
                logger.warning(f"[CONFIDENCE_ANOMALY] 置信度异常低 ({confidence_score}%) 且无明显信息缺失原因")
                return True, f"分析置信度异常低 ({confidence_score}%)，可能存在分析问题"

        return False, ""

    def format_check(self, text: str) -> Dict:
        """检查报告是否包含必需章节"""
        missing_sections = []

        for section in self.REQUIRED_SECTIONS:
            if section not in text:
                missing_sections.append(section)

        return {
            "status": "warning" if missing_sections else "pass",
            "missing_sections": missing_sections,
            "found_sections": [s for s in self.REQUIRED_SECTIONS if s in text],
            "total_required": len(self.REQUIRED_SECTIONS)
        }

    def confidence_check(self, text: str) -> Dict:
        """提取置信度数值，判断是否在0-100且大于60%"""
        confidence_score = None

        patterns = [
            r'置信度[：:]\s*(\d+(?:\.\d+)?)\s*%',
            r'置信度[：:]\s*(\d+(?:\.\d+)?)(?!\s*%)',
            r'confidence[：:]\s*(\d+(?:\.\d+)?)\s*%',
            r'confidence[：:]\s*(\d+(?:\.\d+)?)(?!\s*%)',
            r'置信度\s*(\d+(?:\.\d+)?)\s*分',
            r'评分[：:]\s*(\d+(?:\.\d+)?)\s*/\s*100'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = float(match.group(1))
                if value > 1:
                    confidence_score = value
                else:
                    confidence_score = value * 100
                break

        if confidence_score is None:
            return {
                "status": "warning",
                "message": "未找到置信度数值",
                "confidence_score": None
            }

        if not (0 <= confidence_score <= 100):
            return {
                "status": "warning",
                "message": f"置信度数值超出范围: {confidence_score}",
                "confidence_score": confidence_score
            }

        if confidence_score < 60:
            return {
                "status": "warning",
                "message": f"置信度过低: {confidence_score}%（应大于60%）",
                "confidence_score": confidence_score
            }

        return {
            "status": "pass",
            "confidence_score": confidence_score
        }

    def source_check(self, text: str) -> Dict:
        """统计【判决原文】、【事实推断】、【模型补充】出现次数"""
        source_counts = {}

        for tag in self.SOURCE_TAGS:
            count = len(re.findall(re.escape(tag), text))
            source_counts[tag] = count

        missing_tags = [tag for tag, count in source_counts.items() if count == 0]

        return {
            "status": "warning" if missing_tags else "pass",
            "source_counts": source_counts,
            "missing_tags": missing_tags,
            "total_tags": len(self.SOURCE_TAGS),
            "found_tags": [tag for tag, count in source_counts.items() if count > 0]
        }

    def consistency_check(self, report_text: str, original_text: Optional[str] = None) -> Dict:
        """一致性检查：可选，仅当用户提供了原始文本时执行"""
        if original_text is None or original_text.strip() == "":
            return {
                "status": "skipped",
                "message": "未提供原始文本，跳过一致性检查"
            }

        conclusion_patterns = [
            r'结论[：:]\s*([^\n。]+)',
            r'审查结论[：:]\s*([^\n。]+)',
            r'核心发现[：:]\s*([^\n。]+)',
            r'最终结论[：:]\s*([^\n。]+)',
            r'判定[：:]\s*([^\n。]+)',
            r'认定[：:]\s*([^\n。]+)',
        ]

        conclusions = []
        for pattern in conclusion_patterns:
            matches = re.findall(pattern, report_text)
            conclusions.extend(matches)

        if not conclusions:
            return {
                "status": "warning",
                "message": "报告中未提取到核心结论",
                "matched_count": 0,
                "total_conclusions": 0
            }

        matched_count = 0
        unmatched_conclusions = []

        for conclusion in conclusions:
            conclusion_clean = conclusion.strip()
            if len(conclusion_clean) < 5:
                continue

            if conclusion_clean in original_text or any(
                keyword in original_text
                for keyword in conclusion_clean.split('，')[:2]
            ):
                matched_count += 1
            else:
                unmatched_conclusions.append(conclusion_clean)

        match_rate = matched_count / len(conclusions) if conclusions else 0

        if match_rate < 0.5:
            return {
                "status": "warning",
                "message": f"核心结论与原文一致性低（匹配率: {match_rate*100:.1f}%）",
                "matched_count": matched_count,
                "total_conclusions": len(conclusions),
                "unmatched_conclusions": unmatched_conclusions[:3]
            }

        return {
            "status": "pass",
            "message": f"核心结论与原文一致性良好（匹配率: {match_rate*100:.1f}%）",
            "matched_count": matched_count,
            "total_conclusions": len(conclusions)
        }

    def check_logical_completeness(self, report_text: str) -> Dict:
        """
        逻辑完整性检查：检查报告中是否存在必备条款缺失、定义模糊、
        逻辑矛盾、关键信息缺失等问题。
        
        迁移自原来的 step5_output.py 中的硬编码强制输出。
        现在作为可选的校验后处理，仅在发现问题时添加提示。
        
        :return: 检查结果字典，包含发现的问题列表和完整性提示文本
        """
        completeness_issues = []
        hint_sections = []
        
        # 1. 检查必备条款缺失
        essential_clauses = ['违约责任', '争议解决', '合同解除', '保密', '付款']
        found_clauses = []
        missing_clauses = []
        for clause in essential_clauses:
            if clause in report_text:
                found_clauses.append(clause)
            else:
                missing_clauses.append(clause)
        
        if missing_clauses:
            issue = f"必备条款缺失：{', '.join(missing_clauses)}（可能增加法律风险）"
            completeness_issues.append(issue)
            hint_sections.append(f"- **必备条款缺失**：报告中未涉及 {', '.join(missing_clauses)} 条款的审查，"
                              f"建议确认合同是否包含相关约定。")
        
        # 2. 检查关键定义模糊（识别过于模糊的风险描述）
        vague_patterns = [
            (r'(?:模糊|不明确|不清晰)', '存在定义模糊的条款'),
            (r'(?:合理|适当|必要).*?(?:未|不|无)', '合理/适当/必要等模糊用词未量化'),
        ]
        for pattern, desc in vague_patterns:
            if re.search(pattern, report_text):
                if desc not in completeness_issues:
                    completeness_issues.append(desc)
        
        # 3. 检查逻辑矛盾标记
        contradiction_patterns = [
            r'(?:矛盾|冲突|不一致)',
            r'(?:一方面.*另一方面.*但)',
        ]
        has_contradiction = any(re.search(p, report_text) for p in contradiction_patterns)
        if not has_contradiction:
            # 没有明确标记矛盾，不报告
            pass
        
        # 4. 检查关键信息缺失
        info_gap_patterns = [
            r'(?:信息不足|无法确定|缺失信息|假设条件|需要.*?补充)',
        ]
        for pattern in info_gap_patterns:
            if re.search(pattern, report_text):
                hint_sections.append(f"- **关键信息缺失**：报告中提到信息不足或无法确定的部分，建议用户补充相关信息。")
                break
        
        has_issues = len(hint_sections) > 0
        
        completeness_text = ""
        if has_issues:
            completeness_text = "\n\n---\n\n## 【完整性提示】\n\n" + "\n".join(hint_sections)
            completeness_text += "\n\n*以上提示由系统校验层自动检测生成，仅供参考。*"
        
        return {
            "has_issues": has_issues,
            "issues": completeness_issues,
            "hint_text": completeness_text,
            "status": "warning" if has_issues else "pass"
        }

    def process(self, raw_report: str, original_text: Optional[str] = None) -> Dict:
        """执行完整校验，返回校验结果"""
        leak_passed, leak_msg, leak_patterns = self.check_output_leak(raw_report)

        if not leak_passed:
            logger.error("[SECURITY] 系统提示词泄露检测未通过")
            return {
                "status": "error",
                "has_warnings": True,
                "has_leak": True,
                "leak_patterns": leak_patterns,
                "warnings": ["系统提示词泄露检测未通过，" + leak_msg],
                "format_check": None,
                "confidence_check": None,
                "source_check": None,
                "consistency_check": None,
                "metadata": {
                    "warnings": ["系统提示词泄露检测未通过，" + leak_msg],
                    "warning_count": 1,
                    "validation_status": "error",
                    "has_leak": True,
                    "leak_patterns": leak_patterns
                }
            }

        refusal_detected, refusal_patterns = self.check_output_refusal(raw_report)

        format_result = self.format_check(raw_report)
        confidence_result = self.confidence_check(raw_report)
        source_result = self.source_check(raw_report)
        consistency_result = self.consistency_check(raw_report, original_text)

        confidence_anomaly, anomaly_msg = self.check_confidence_anomaly(
            confidence_result.get("confidence_score"),
            raw_report
        )

        warnings = []

        if format_result['status'] == 'warning':
            warnings.append(f"格式检查: 缺少章节 - {', '.join(format_result['missing_sections'])}")

        if confidence_result['status'] == 'warning':
            warnings.append(f"置信度检查: {confidence_result.get('message', '未通过')}")

        if source_result['status'] == 'warning':
            warnings.append(f"来源检查: 缺失标记 - {', '.join(source_result['missing_tags'])}")

        if consistency_result['status'] == 'warning':
            warnings.append(f"一致性检查: {consistency_result.get('message', '未通过')}")

        if refusal_detected:
            warnings.append(f"模型拒绝句式检测: {len(refusal_patterns)} 个可疑句式（已记录日志）")

        if confidence_anomaly:
            warnings.append(f"置信度异常: {anomaly_msg}")

        has_warnings = len(warnings) > 0

        return {
            "status": "error" if (leak_patterns or confidence_anomaly) else ("warning" if has_warnings else "pass"),
            "has_warnings": has_warnings,
            "has_leak": bool(leak_patterns),
            "refusal_detected": refusal_detected,
            "warnings": warnings,
            "format_check": format_result,
            "confidence_check": confidence_result,
            "source_check": source_result,
            "consistency_check": consistency_result,
            "metadata": {
                "warnings": warnings,
                "warning_count": len(warnings),
                "validation_status": "error" if (leak_patterns or confidence_anomaly) else ("warning" if has_warnings else "pass"),
                "has_leak": bool(leak_patterns),
                "refusal_detected": refusal_detected,
                "leak_patterns": leak_patterns,
                "refusal_patterns": refusal_patterns if refusal_detected else []
            }
        }