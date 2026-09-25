#!/usr/bin/env bash
# Default: snapshot the running Compose backend's configured DB into its data volume.
# Local: MAINTENANCE_MODE=local DB_PATH=/absolute/app.db BACKUP_DIR=/absolute/backups bash backup.sh
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MODE="${MAINTENANCE_MODE:-compose}"
NAME="sageai_db_$(date -u '+%Y%m%dT%H%M%SZ')_${RANDOM}.sqlite"
case "$MODE" in
  compose)
    OUTPUT="${BACKUP_DIR:-/app/data/backups}/$NAME"
    docker compose --project-directory "$SCRIPT_DIR" exec -T backend python /app/sqlite_maintenance.py backup --configured --output "$OUTPUT"
    ;;
  local)
    : "${DB_PATH:?Set DB_PATH to the actual database file}"
    : "${BACKUP_DIR:?Set BACKUP_DIR explicitly}"
    "${PYTHON:-python3}" "$SCRIPT_DIR/backend/sqlite_maintenance.py" backup --source "$DB_PATH" --output "$BACKUP_DIR/$NAME"
    ;;
  *) echo "Unknown MAINTENANCE_MODE: $MODE" >&2; exit 2 ;;
esac
# No automatic pruning: retain snapshots until the retention policy is approved.
