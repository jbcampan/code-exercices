#!/usr/bin/env bash
# deploy.sh — Deployment CLI tool

set -e
set -u

# ─── Constants ────────────────────────────────────────────────────────────────
LOCK_FILE="/tmp/deploy.lock"
LOG_FILE="deploy.log"
VALID_ENVS=("dev" "staging" "prod")

# ─── Trap / cleanup ───────────────────────────────────────────────────────────
cleanup() {
    if [[ -f "$LOCK_FILE" ]]; then
        rm -f "$LOCK_FILE"
        echo "Lock file removed."
    fi
}

trap "cleanup" EXIT

# ─── Logging ──────────────────────────────────────────────────────────────────
log() {
    local message="$1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $message" >> "$LOG_FILE"
}

# ─── Validation ───────────────────────────────────────────────────────────────
validate_env() {
    local env="$1"

    for valid_env in "${VALID_ENVS[@]}"; do
        if [[ "$env" == "$valid_env" ]]; then
            return 0
        fi
    done

    echo "Error: invalid environment '$env'. Valid values: ${VALID_ENVS[*]}"
    exit 1
}

# ─── Sub-commands ─────────────────────────────────────────────────────────────
cmd_status() {
    local env="$1"

    echo "Deployment status for '$env': RUNNING"
    log "Status checked for environment '$env'"
}

cmd_start() {
    local env="$1"
    local dry_run="$2"

    if [[ "$dry_run" == "true" ]]; then
        echo "[DRY-RUN] Would start deployment on '$env'"
        log "DRY-RUN start deployment on '$env'"
        return
    fi

    touch "$LOCK_FILE"
    echo "Starting deployment on '$env'..."
    log "Deployment started on '$env'"

    sleep 1

    echo "Deployment completed."
    log "Deployment completed on '$env'"
}

cmd_rollback() {
    local env="$1"
    local dry_run="$2"

    if [[ "$dry_run" == "true" ]]; then
        echo "[DRY-RUN] Would rollback deployment on '$env'"
        log "DRY-RUN rollback on '$env'"
        return
    fi

    touch "$LOCK_FILE"
    echo "Rolling back deployment on '$env'..."
    log "Rollback started on '$env'"

    sleep 1

    echo "Rollback completed."
    log "Rollback completed on '$env'"
}

# ─── Argument parsing ─────────────────────────────────────────────────────────
usage() {
    echo "Usage: $(basename "$0") <command> [--env dev|staging|prod] [--dry-run]"
    echo "Commands: status | start | rollback"
    exit 1
}

main() {
    if [[ $# -lt 1 ]]; then
        usage
    fi

    local command="$1"
    shift

    local env="dev"
    local dry_run="false"

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --env)
                shift
                if [[ $# -eq 0 ]]; then
                    echo "Error: --env requires a value"
                    exit 1
                fi
                env="$1"
                ;;
            --dry-run)
                dry_run="true"
                ;;
            *)
                echo "Unknown option: $1"
                usage
                ;;
        esac
        shift
    done

    validate_env "$env"

    case "$command" in
        status)
            cmd_status "$env"
            ;;
        start)
            cmd_start "$env" "$dry_run"
            ;;
        rollback)
            cmd_rollback "$env" "$dry_run"
            ;;
        *)
            echo "Unknown command: $command"
            usage
            ;;
    esac
}

main "$@"