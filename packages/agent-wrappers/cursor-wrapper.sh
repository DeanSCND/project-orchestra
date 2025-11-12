#!/usr/bin/env bash
set -euo pipefail

TASK=${1:-"No task provided"}
RUN_ID=${ORCHESTRA_RUN_ID:-unknown}

echo "{\"event\":\"agent_started\",\"agent\":\"cursor\",\"run_id\":\"${RUN_ID}\"}"
echo "{\"event\":\"task_received\",\"agent\":\"cursor\",\"task\":\"${TASK}\"}"
sleep 1
echo "{\"event\":\"task_completed\",\"agent\":\"cursor\"}"
sleep 5
