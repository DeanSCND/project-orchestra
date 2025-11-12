#!/usr/bin/env bash
set -euo pipefail

TASK=${1:-"No task provided"}
RUN_ID=${ORCHESTRA_RUN_ID:-unknown}

echo "{\"event\":\"agent_started\",\"agent\":\"codex\",\"run_id\":\"${RUN_ID}\"}"
echo "{\"event\":\"task_received\",\"agent\":\"codex\",\"task\":\"${TASK}\"}"

if command -v codex >/dev/null 2>&1; then
  echo "{\"event\":\"info\",\"agent\":\"codex\",\"message\":\"Dispatching task to Codex CLI\"}"
  codex "${TASK}"
else
  echo "{\"event\":\"info\",\"agent\":\"codex\",\"message\":\"Codex CLI not installed; emitting sample output\"}"
  sleep 1
  echo "modified: codex_app/main.py"
  echo "modified: codex_app/tests/test_main.py"
  echo "modified: codex_app/utils.py"
fi

echo "{\"event\":\"task_completed\",\"agent\":\"codex\"}"
