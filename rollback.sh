#!/bin/bash
# ============================================================
# SageAI 回滚脚本
# 用法: bash rollback.sh [docker|backup|git]
#   docker - 回滚到上一个 Docker 镜像
#   backup - 从最近一次备份恢复数据库
#   git    - 回滚到上一个 Git 版本
# ============================================================
set -e

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
        echo ""
        echo "从最近备份恢复数据库..."
        
        BACKUP_DIR="$SCRIPT_DIR/backups"
        LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/sageai_db_*.sqlite.gz 2>/dev/null | head -1)
        
        if [ -z "$LATEST_BACKUP" ]; then
            echo "  [ERROR] 未找到备份文件"
            exit 1
        fi
        
        echo "  找到备份: $LATEST_BACKUP"
        
        # 解压备份
        gunzip -c "$LATEST_BACKUP" > "$BACKUP_DIR/restore_temp.db"
        
        # 停止服务
        docker compose down 2>/dev/null || true
        
        # 恢复数据库
        DB_PATH="$SCRIPT_DIR/backend/data/app.db"
        if [ -f "$DB_PATH" ]; then
            cp "$DB_PATH" "$DB_PATH.bak_$(date '+%Y%m%d_%H%M%S')"
            echo "  [OK] 已备份当前数据库"
        fi
        
        cp "$BACKUP_DIR/restore_temp.db" "$DB_PATH"
        rm "$BACKUP_DIR/restore_temp.db"
        
        # 重启服务
        docker compose up -d
        
        echo "  [OK] 数据库已恢复"
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
