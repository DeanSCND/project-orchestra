#!/usr/bin/env bash
set -euo pipefail

TASK=${1:-"No task provided"}
RUN_ID=${ORCHESTRA_RUN_ID:-unknown}

echo "{\"event\":\"agent_started\",\"agent\":\"claude\",\"run_id\":\"${RUN_ID}\"}"
echo "{\"event\":\"task_received\",\"agent\":\"claude\",\"task\":\"${TASK}\"}"
sleep 1
echo "{\"event\":\"delegating\",\"agent\":\"claude\"}"
sleep 5
