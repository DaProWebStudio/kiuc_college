#!/usr/bin/env bash
# Ежедневный дамп PostgreSQL-БД проекта КИУК-колледж.
#
# Что делает:
#   1. Читает креды БД из .env (DATABASE_NAME/USER/PASSWORD/HOST)
#   2. Делает pg_dump в /var/www/kiuc_college/backups/kiuc-college-YYYYMMDD-HHMMSS.dump
#      (custom-format, сжатый, готов к pg_restore)
#   3. Удаляет дампы старше KEEP_DAYS (по умолчанию 30)
#   4. Логирует в backups/backup.log
#
# Запуск:
#   ./scripts/backup_db.sh
#
# Для cron — см. config/deploy/backup.cron

set -euo pipefail

PROJECT_DIR="/var/www/kiuc_college"
BACKUP_DIR="${PROJECT_DIR}/backups"
KEEP_DAYS="${KEEP_DAYS:-30}"
LOG_FILE="${BACKUP_DIR}/backup.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "${LOG_FILE}"
}

mkdir -p "${BACKUP_DIR}"

# Загружаем .env (только переменные DATABASE_*, чтобы не засорять окружение)
if [[ ! -f "${PROJECT_DIR}/.env" ]]; then
    log "ERROR: ${PROJECT_DIR}/.env not found"
    exit 1
fi

# shellcheck disable=SC2046
export $(grep -E '^DATABASE_' "${PROJECT_DIR}/.env" | xargs)

: "${DATABASE_NAME:?DATABASE_NAME is empty}"
: "${DATABASE_USER:?DATABASE_USER is empty}"
: "${DATABASE_PASSWORD:?DATABASE_PASSWORD is empty}"
: "${DATABASE_HOST:=localhost}"
: "${DATABASE_PORT:=5432}"

STAMP=$(date +%Y%m%d-%H%M%S)
DUMP_FILE="${BACKUP_DIR}/kiuc-college-${STAMP}.dump"

log "→ pg_dump → ${DUMP_FILE}"

PGPASSWORD="${DATABASE_PASSWORD}" pg_dump \
    -h "${DATABASE_HOST}" \
    -p "${DATABASE_PORT}" \
    -U "${DATABASE_USER}" \
    -d "${DATABASE_NAME}" \
    --no-owner --no-privileges \
    -F c \
    -f "${DUMP_FILE}"

SIZE=$(du -h "${DUMP_FILE}" | cut -f1)
log "✓ dump ${SIZE} → $(basename "${DUMP_FILE}")"

# Ротация: удаляем дампы старше KEEP_DAYS дней
DELETED=$(find "${BACKUP_DIR}" -maxdepth 1 -name 'kiuc-college-*.dump' -type f -mtime "+${KEEP_DAYS}" -print -delete | wc -l)
if [[ "${DELETED}" -gt 0 ]]; then
    log "✓ pruned ${DELETED} dumps older than ${KEEP_DAYS} days"
fi

log "done"
