#!/usr/bin/env bash
set -euo pipefail

TASK=${1:-"No task provided"}
RUN_ID=${ORCHESTRA_RUN_ID:-unknown}

echo "{\"event\":\"agent_started\",\"agent\":\"droid\",\"run_id\":\"${RUN_ID}\"}"
echo "{\"event\":\"task_received\",\"agent\":\"droid\",\"task\":\"${TASK}\"}"
sleep 1
echo "modified: app/models/user.py"
echo "modified: app/api/users.py"
echo "modified: app/schemas/user.py"
sleep 1
echo "{\"event\":\"task_completed\",\"agent\":\"droid\"}"
