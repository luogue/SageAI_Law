#!/bin/bash
# ============================================================
# SageAI 数据库备份脚本
# 用法: bash backup.sh
# 建议: 添加到 crontab 每日执行
#       0 3 * * * /path/to/sage/backup.sh >> /var/log/sageai-backup.log 2>&1
# ============================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKUP_DIR="${BACKUP_DIR:-$SCRIPT_DIR/backups}"
DB_PATH="${DB_PATH:-$SCRIPT_DIR/backend/data/app.db}"
DATE=$(date '+%Y%m%d_%H%M%S')
BACKUP_NAME="sageai_db_${DATE}.sqlite"

echo "============================================="
echo "  SageAI 数据库备份"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================="

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份数据库
if [ -f "$DB_PATH" ]; then
    echo "  备份文件: $DB_PATH -> $BACKUP_DIR/$BACKUP_NAME"
    cp "$DB_PATH" "$BACKUP_DIR/$BACKUP_NAME"
    echo "  [OK] 备份完成"
else
    echo "  [WARN] 数据库文件不存在: $DB_PATH"
    exit 1
fi

# 压缩备份
gzip "$BACKUP_DIR/$BACKUP_NAME"
echo "  [OK] 已压缩: ${BACKUP_NAME}.gz"

# 清理旧备份（保留最近 30 天）
find "$BACKUP_DIR" -name "sageai_db_*.sqlite.gz" -mtime +30 -delete
DELETED_COUNT=$(find "$BACKUP_DIR" -name "sageai_db_*.sqlite.gz" -mtime +30 2>/dev/null | wc -l)
echo "  [OK] 已清理 ${DELETED_COUNT} 个过期备份"

echo "============================================="
echo "  备份完成: ${BACKUP_NAME}.gz"
echo "============================================="
