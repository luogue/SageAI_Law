#!/bin/bash
# ============================================================
# SageAI 回滚脚本
# 用法: bash rollback.sh [docker|backup|git]
#   docker - 回滚到上一个 Docker 镜像
#   backup - 校验指定备份并生成新候选文件（不切换数据库）
#   git    - 回滚到上一个 Git 版本
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

ROLLBACK_MODE="${1:-docker}"

echo "============================================="
echo "  SageAI 回滚操作"
echo "  模式: $ROLLBACK_MODE"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================="

case $ROLLBACK_MODE in
    docker)
        echo ""
        echo "回滚 Docker 镜像到上一个版本..."
        
        # 停止当前服务
        docker compose down
        
        # 拉取上一个镜像（使用 previous 标签）
        # 注意：需要事先打好 previous 标签
        docker tag sageai-backend:latest sageai-backend:rolled-back 2>/dev/null || true
        docker tag sageai-frontend:latest sageai-frontend:rolled-back 2>/dev/null || true
        
        if docker image inspect sageai-backend:previous >/dev/null 2>&1; then
            docker tag sageai-backend:previous sageai-backend:latest
            docker tag sageai-frontend:previous sageai-frontend:latest
            docker compose up -d
            echo "  [OK] 已回滚到上一个版本"
        else
            echo "  [ERROR] 未找到 previous 标签的镜像，无法回滚"
            echo "  请使用 backup 模式恢复数据库"
            exit 1
        fi
        ;;
        
    backup)
        # Stage a verified NEW candidate only. Never guess the latest backup or replace live data.
        : "${BACKUP_FILE:?Select a specific reviewed backup file}"
        : "${RESTORE_OUTPUT:?Set a NEW candidate path, never the active DB path}"
        case "${MAINTENANCE_MODE:-compose}" in
            compose)
                docker compose exec -T backend python /app/sqlite_maintenance.py stage --source "$BACKUP_FILE" --output "$RESTORE_OUTPUT"
                ;;
            local)
                "${PYTHON:-python3}" "$SCRIPT_DIR/backend/sqlite_maintenance.py" stage --source "$BACKUP_FILE" --output "$RESTORE_OUTPUT"
                ;;
            *) echo "Unknown MAINTENANCE_MODE" >&2; exit 2 ;;
        esac
        echo "Verified candidate staged. No database switch performed."
        ;;

    git)
        echo ""
        echo "回滚到上一个 Git 版本..."
        git log --oneline -5
        echo ""
        read -p "请输入要回滚到的 commit hash: " COMMIT_HASH
        
        if [ -z "$COMMIT_HASH" ]; then
            echo "  已取消"
            exit 0
        fi
        
        git reset --hard "$COMMIT_HASH"
        echo "  [OK] 已回滚到 $COMMIT_HASH"
        echo "  请运行 deploy.sh 重新部署"
        ;;
        
    *)
        echo "  未知回滚模式: $ROLLBACK_MODE"
        echo "  支持的模式: docker, backup, git"
        exit 1
        ;;
esac

echo ""
echo "============================================="
echo "  回滚完成"
echo "============================================="
