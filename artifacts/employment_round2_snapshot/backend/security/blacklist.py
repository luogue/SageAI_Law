"""黑名单管理模块"""
import sqlite3
import threading
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class BlacklistManager:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent.parent / "data" / "blacklist.db"
        self.db_path = str(db_path)
        self._lock = threading.Lock()
        self._init_db()

    def _init_db(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            # 创建表（如果不存在）
            conn.execute("""
                CREATE TABLE IF NOT EXISTS blacklist (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    blacklist_type TEXT NOT NULL,
                    value TEXT NOT NULL UNIQUE,
                    reason TEXT,
                    ban_type TEXT DEFAULT 'manual',
                    input_preview TEXT,
                    trigger_rule TEXT,
                    is_unbanned INTEGER DEFAULT 0,
                    unbanned_by TEXT,
                    unban_reason TEXT,
                    unbanned_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP
                )
            """)
            
            # 检查是否需要添加新列（兼容旧数据库）
            new_columns = {
                "ban_type": "TEXT DEFAULT 'manual'",
                "input_preview": "TEXT",
                "trigger_rule": "TEXT",
                "is_unbanned": "INTEGER DEFAULT 0",
                "unbanned_by": "TEXT",
                "unban_reason": "TEXT",
                "unbanned_at": "TIMESTAMP",
                "expires_at": "TIMESTAMP",
            }
            cursor = conn.execute("PRAGMA table_info(blacklist)")
            existing_cols = [col[1] for col in cursor.fetchall()]
            for col_name, col_def in new_columns.items():
                if col_name not in existing_cols:
                    try:
                        conn.execute(f"ALTER TABLE blacklist ADD COLUMN {col_name} {col_def}")
                        logger.info(f"[BLACKLIST] 已添加 {col_name} 列")
                    except sqlite3.OperationalError:
                        pass
            
            # 添加索引
            try:
                conn.execute("CREATE INDEX IF NOT EXISTS idx_blacklist_value ON blacklist(value)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_blacklist_type ON blacklist(blacklist_type)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_blacklist_expires ON blacklist(expires_at)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_blacklist_ban_type ON blacklist(ban_type)")
            except Exception as e:
                logger.warning(f"[BLACKLIST] 创建索引失败: {e}")
            
            conn.commit()
            conn.close()

    def add(self, blacklist_type: str, value: str, reason: str = "", expires_at: Optional[datetime] = None,
            ban_type: str = "manual", input_preview: str = "", trigger_rule: str = "") -> bool:
        """
        添加到黑名单
        
        Args:
            blacklist_type: 'ip' 或 'user_id'
            value: IP地址或用户ID
            reason: 封禁原因
            expires_at: 过期时间，None表示永久封禁
            ban_type: 封禁类型 (manual, prompt_injection, auto_ban, output_leak)
            input_preview: 触发封禁的原始输入
            trigger_rule: 触发规则描述
        
        Returns:
            bool: 是否添加成功
        """
        with self._lock:
            try:
                conn = sqlite3.connect(self.db_path)
                # 先检查是否存在，如果存在则更新
                cursor = conn.execute(
                    "SELECT id, is_unbanned FROM blacklist WHERE blacklist_type = ? AND value = ?",
                    (blacklist_type, value)
                )
                existing = cursor.fetchone()
                if existing and existing[1] == 1:
                    # 已解封的记录，重新封禁
                    conn.execute(
                        "UPDATE blacklist SET reason=?, ban_type=?, input_preview=?, trigger_rule=?, "
                        "is_unbanned=0, unbanned_by=NULL, unban_reason=NULL, unbanned_at=NULL, "
                        "expires_at=?, created_at=CURRENT_TIMESTAMP "
                        "WHERE blacklist_type=? AND value=?",
                        (reason, ban_type, input_preview[:500] if input_preview else "",
                         trigger_rule, expires_at.isoformat() if expires_at else None,
                         blacklist_type, value)
                    )
                else:
                    conn.execute(
                        "INSERT OR REPLACE INTO blacklist "
                        "(blacklist_type, value, reason, ban_type, input_preview, trigger_rule, expires_at) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (blacklist_type, value, reason, ban_type,
                         input_preview[:500] if input_preview else "",
                         trigger_rule, expires_at.isoformat() if expires_at else None)
                    )
                conn.commit()
                affected = conn.total_changes > 0
                conn.close()
                if affected:
                    logger.info(f"[BLACKLIST] 已添加到黑名单: type={blacklist_type}, value={value}, "
                               f"ban_type={ban_type}, expires_at={expires_at}")
                return affected
            except Exception as e:
                logger.error(f"[BLACKLIST] 添加黑名单失败: {e}")
                return False

    def remove(self, blacklist_type: str, value: str) -> bool:
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.execute(
                "DELETE FROM blacklist WHERE blacklist_type = ? AND value = ?",
                (blacklist_type, value)
            )
            conn.commit()
            affected = cursor.rowcount > 0
            conn.close()
            if affected:
                logger.info(f"[BLACKLIST] 已从黑名单移除: type={blacklist_type}, value={value}")
            return affected

    def is_blacklisted(self, blacklist_type: str, value: str) -> bool:
        """检查是否在黑名单中（考虑过期时间和解封状态）"""
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.execute(
                "SELECT expires_at, is_unbanned FROM blacklist WHERE blacklist_type = ? AND value = ?",
                (blacklist_type, value)
            )
            row = cursor.fetchone()
            conn.close()
            
            if row:
                expires_at, is_unbanned = row[0], row[1]
                # 已解封的不算黑名单
                if is_unbanned:
                    return False
                if expires_at is None:
                    # 永久封禁
                    return True
                # 检查是否过期
                try:
                    expire_time = datetime.fromisoformat(expires_at)
                    return expire_time > datetime.now()
                except:
                    return True
            return False

    def check(self, ip: str = None, user_id: str = None) -> Optional[str]:
        if ip and self.is_blacklisted("ip", ip):
            return ip
        if user_id and self.is_blacklisted("user_id", user_id):
            return user_id
        return None

    def get_all(self) -> List[dict]:
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.execute("SELECT * FROM blacklist ORDER BY created_at DESC")
            rows = cursor.fetchall()
            conn.close()
            return [
                {
                    "id": r[0],
                    "type": r[1],
                    "value": r[2],
                    "reason": r[3],
                    "ban_type": r[4] if len(r) > 4 else "manual",
                    "input_preview": r[5] if len(r) > 5 else "",
                    "trigger_rule": r[6] if len(r) > 6 else "",
                    "is_unbanned": bool(r[7]) if len(r) > 7 else False,
                    "unbanned_by": r[8] if len(r) > 8 else "",
                    "unban_reason": r[9] if len(r) > 9 else "",
                    "unbanned_at": r[10] if len(r) > 10 else None,
                    "created_at": r[11] if len(r) > 11 else None,
                    "expires_at": r[12] if len(r) > 12 else None
                }
                for r in rows
            ]

    def get_auto_ban_stats(self, hours: int = 24) -> Dict[str, Any]:
        """获取自动封禁统计数据"""
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            # 计算时间范围
            cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
            
            # 统计新增封禁数
            cursor = conn.execute(
                "SELECT COUNT(*) FROM blacklist WHERE created_at >= ?",
                (cutoff,)
            )
            new_bans = cursor.fetchone()[0]
            
            # 统计永久封禁数
            cursor = conn.execute("SELECT COUNT(*) FROM blacklist WHERE expires_at IS NULL")
            permanent_bans = cursor.fetchone()[0]
            
            # 统计临时封禁数
            cursor = conn.execute("SELECT COUNT(*) FROM blacklist WHERE expires_at IS NOT NULL")
            temporary_bans = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "new_bans_last_24h": new_bans,
                "permanent_bans": permanent_bans,
                "temporary_bans": temporary_bans,
                "total_bans": permanent_bans + temporary_bans
            }

    def cleanup_expired(self) -> int:
        """清理已过期的黑名单记录"""
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            now = datetime.now().isoformat()
            cursor = conn.execute(
                "DELETE FROM blacklist WHERE expires_at IS NOT NULL AND expires_at <= ?",
                (now,)
            )
            deleted = cursor.rowcount
            conn.commit()
            conn.close()
            if deleted > 0:
                logger.info(f"[BLACKLIST] 清理了 {deleted} 条过期记录")
            return deleted

# 全局实例
blacklist_manager = BlacklistManager()

def unban(blacklist_type: str, value: str, admin_user: str, unban_reason: str = "") -> bool:
    """解封黑名单记录（标记为已解封）"""
    with blacklist_manager._lock:
        try:
            conn = sqlite3.connect(blacklist_manager.db_path)
            now = datetime.now().isoformat()
            cursor = conn.execute(
                "UPDATE blacklist SET is_unbanned=1, unbanned_by=?, unban_reason=?, unbanned_at=? "
                "WHERE blacklist_type=? AND value=?",
                (admin_user, unban_reason, now, blacklist_type, value)
            )
            conn.commit()
            affected = cursor.rowcount > 0
            conn.close()
            if affected:
                logger.info(f"[BLACKLIST] 已解封: type={blacklist_type}, value={value}, by={admin_user}")
            return affected
        except Exception as e:
            logger.error(f"[BLACKLIST] 解封失败: {e}")
            return False


# 便捷函数
def add_to_blacklist(ip: str = None, user_id: str = None, reason: str = "", expires_at: Optional[datetime] = None,
                     ban_type: str = "manual", input_preview: str = "", trigger_rule: str = ""):
    if ip:
        blacklist_manager.add("ip", ip, reason, expires_at, ban_type, input_preview, trigger_rule)
    if user_id:
        blacklist_manager.add("user_id", user_id, reason, expires_at, ban_type, input_preview, trigger_rule)

def is_blacklisted(ip: str = None, user_id: str = None) -> bool:
    return blacklist_manager.check(ip, user_id) is not None

def check_blacklist(ip: str = None, user_id: str = None) -> str | None:
    """检查IP或用户ID是否在黑名单，返回被拦截的类型（用于middleware）"""
    return blacklist_manager.check(ip, user_id)

def get_blacklist_stats(hours: int = 24) -> Dict[str, Any]:
    return blacklist_manager.get_auto_ban_stats(hours)
