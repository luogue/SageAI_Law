"""恶意行为检测和自动黑名单模块"""
import time
import threading
import os
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple
from .blacklist import blacklist_manager

logger = logging.getLogger(__name__)

class MaliciousBehaviorTracker:
    """恶意行为追踪器"""
    
    # 违规类型
    TYPE_FORMAT_ERROR = "format_error"
    TYPE_SIZE_EXCEEDED = "size_exceeded"
    TYPE_CONTENT_TOO_SHORT = "content_too_short"
    TYPE_NOT_CONTRACT = "not_contract"
    TYPE_SENSITIVE_CONTENT = "sensitive_content"
    TYPE_RATE_LIMIT = "rate_limit"
    
    # 违规阈值配置
    DEFAULT_THRESHOLD = 10  # 每小时10次
    DEFAULT_BAN_DURATION = 3600  # 默认封禁1小时
    
    def __init__(self):
        self._lock = threading.Lock()
        # 存储违规记录: {identifier: {type: [timestamps]}}
        self._violations: Dict[str, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
        # 存储自动封禁记录
        self._auto_bans: Dict[str, Tuple[float, str]] = {}  # {identifier: (ban_until, reason)}
        
        # 从环境变量读取配置
        self._threshold = int(os.getenv("MALICIOUS_THRESHOLD", self.DEFAULT_THRESHOLD))
        self._ban_duration = int(os.getenv("MALICIOUS_BAN_DURATION", self.DEFAULT_BAN_DURATION))
        
        # 启动清理线程
        self._stop_event = threading.Event()
        self._cleanup_thread = threading.Thread(target=self._cleanup_expired, daemon=True)
        self._cleanup_thread.start()
        
        logger.info(f"恶意行为检测器初始化完成，阈值: {self._threshold}/小时，封禁时长: {self._ban_duration/3600}小时")
    
    def record_violation(self, identifier: str, violation_type: str, reason: str = ""):
        """记录违规行为"""
        current_time = time.time()
        should_ban = False
        ban_reason = ""
        
        with self._lock:
            # 记录违规
            self._violations[identifier][violation_type].append(current_time)
            
            # 计算该标识符在过去1小时内的总违规次数
            total_violations = 0
            one_hour_ago = current_time - 3600
            for type_list in self._violations[identifier].values():
                total_violations += len([t for t in type_list if t >= one_hour_ago])
            
            # 检查是否达到封禁阈值
            if total_violations >= self._threshold and identifier not in self._auto_bans:
                ban_until = current_time + self._ban_duration
                self._auto_bans[identifier] = (ban_until, f"1小时内违规{total_violations}次: {reason}")
                should_ban = True
                ban_reason = f"1小时内违规{total_violations}次"
        
        # 如果需要自动封禁，添加到黑名单
        if should_ban:
            self._auto_add_to_blacklist(identifier, ban_reason)
    
    def is_auto_banned(self, identifier: str) -> Tuple[bool, str]:
        """检查是否被自动封禁"""
        with self._lock:
            if identifier not in self._auto_bans:
                return False, ""
            
            ban_until, reason = self._auto_bans[identifier]
            if time.time() < ban_until:
                remaining = int((ban_until - time.time()) / 60)
                return True, f"自动封禁，剩余{remaining}分钟: {reason}"
            else:
                # 过期了，移除
                del self._auto_bans[identifier]
                return False, ""
    
    def get_violation_stats(self, identifier: str) -> Dict[str, int]:
        """获取指定标识符的违规统计"""
        one_hour_ago = time.time() - 3600
        stats = defaultdict(int)
        
        with self._lock:
            if identifier not in self._violations:
                return dict(stats)
            
            for violation_type, timestamps in self._violations[identifier].items():
                count = len([t for t in timestamps if t >= one_hour_ago])
                if count > 0:
                    stats[violation_type] = count
        
        return dict(stats)
    
    def _auto_add_to_blacklist(self, identifier: str, reason: str):
        """自动添加到黑名单"""
        # 尝试判断是IP还是用户ID
        blacklist_type = "ip"
        if identifier.isdigit() or identifier.startswith("user"):
            blacklist_type = "user_id"
        
        try:
            added = blacklist_manager.add(blacklist_type, identifier, f"[自动封禁] {reason}")
            if added:
                logger.warning(f"自动封禁 {blacklist_type}: {identifier} - {reason}")
        except Exception as e:
            logger.error(f"自动封禁失败: {e}")
    
    def _cleanup_expired(self):
        """清理过期的违规记录（后台线程）"""
        while not self._stop_event.is_set():
            try:
                cutoff_time = time.time() - 3600 * 2  # 保留2小时内的记录
                with self._lock:
                    for identifier in list(self._violations.keys()):
                        for violation_type in list(self._violations[identifier].keys()):
                            self._violations[identifier][violation_type] = [
                                t for t in self._violations[identifier][violation_type]
                                if t >= cutoff_time
                            ]
                        # 清理空的标识符
                        if not any(self._violations[identifier].values()):
                            del self._violations[identifier]
                    
                    # 清理过期的自动封禁记录
                    for identifier in list(self._auto_bans.keys()):
                        if time.time() >= self._auto_bans[identifier][0]:
                            del self._auto_bans[identifier]
            except Exception as e:
                logger.error(f"清理过期记录失败: {e}")
            
            # 每分钟清理一次
            self._stop_event.wait(60)
    
    def close(self):
        """关闭"""
        self._stop_event.set()
        if self._cleanup_thread.is_alive():
            self._cleanup_thread.join(timeout=5)
    
    def reset_identifier(self, identifier: str):
        """重置指定标识符的违规记录"""
        with self._lock:
            if identifier in self._violations:
                del self._violations[identifier]
            if identifier in self._auto_bans:
                del self._auto_bans[identifier]


# 全局实例
_malicious_tracker: MaliciousBehaviorTracker = None


def get_malicious_tracker() -> MaliciousBehaviorTracker:
    """获取全局恶意行为追踪器"""
    global _malicious_tracker
    if _malicious_tracker is None:
        _malicious_tracker = MaliciousBehaviorTracker()
    return _malicious_tracker


def record_violation(ip: str = None, user_id: str = None, violation_type: str = "", reason: str = ""):
    """记录违规（便捷函数）"""
    tracker = get_malicious_tracker()
    if ip:
        tracker.record_violation(ip, violation_type, reason)
    if user_id:
        tracker.record_violation(str(user_id), violation_type, reason)


def is_auto_banned(ip: str = None, user_id: str = None) -> Tuple[bool, str]:
    """检查是否被自动封禁"""
    tracker = get_malicious_tracker()
    if ip:
        banned, reason = tracker.is_auto_banned(ip)
        if banned:
            return banned, reason
    if user_id:
        banned, reason = tracker.is_auto_banned(str(user_id))
        if banned:
            return banned, reason
    return False, ""
