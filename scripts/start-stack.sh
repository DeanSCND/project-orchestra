#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cleanup() {
  trap - EXIT
  if [[ -n "${DAEMON_PID:-}" && -d "/proc/${DAEMON_PID}" ]]; then
    kill "${DAEMON_PID}" 2>/dev/null || true
  fi
  if [[ -n "${WEB_PID:-}" && -d "/proc/${WEB_PID}" ]]; then
    kill "${WEB_PID}" 2>/dev/null || true
  fi
}

trap cleanup EXIT INT TERM

export ORCHESTRA_DAEMON_ALLOW_INSECURE_WS="${ORCHESTRA_DAEMON_ALLOW_INSECURE_WS:-1}"
export PYTHONPATH="${ROOT_DIR}:${PYTHONPATH:-}"

(
  cd "${ROOT_DIR}"
  python3 -m packages.daemon.orchestra_daemon.main
) &
DAEMON_PID=$!

(
  cd "${ROOT_DIR}/packages/web-ui"
  if [[ ! -d node_modules ]]; then
    npm install
  fi
  npm run dev
) &
WEB_PID=$!

wait -n || true
cleanup
