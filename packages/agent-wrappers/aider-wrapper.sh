#!/usr/bin/env bash
set -euo pipefail

TASK=${1:-"No task provided"}
RUN_ID=${ORCHESTRA_RUN_ID:-unknown}

echo "{\"event\":\"agent_started\",\"agent\":\"aider\",\"run_id\":\"${RUN_ID}\"}"
echo "{\"event\":\"task_received\",\"agent\":\"aider\",\"task\":\"${TASK}\"}"
sleep 1
echo "{\"event\":\"task_completed\",\"agent\":\"aider\"}"
sleep 5
