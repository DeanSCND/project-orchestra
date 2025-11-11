#!/bin/bash
# Script to create new issues based on Opus feedback

cd /home/dean/Development/RandD/project-orchestra

echo "Creating new issues for redesign..."

# Issue #16: Task Router (CRITICAL - Killer Feature)
gh issue create \
  --title "Task Router - Intelligent Task Classification and Routing" \
  --milestone "Milestone 2: Multi-Agent Orchestration" \
  --label "P0,backend" \
  --body "## Objective
Implement intelligent task router that analyzes tasks and routes to optimal agent based on task type AND cost.

## Why This Is The Killer Feature
- 70% cost savings by routing simple tasks to cheap models
- Automatic tool selection (no manual decision fatigue)
- Cost-aware routing with hard limits

## Implementation
\`\`\`yaml
# config/task_router.yaml
routing_rules:
  - name: \"Code Review\"
    patterns: [\"review\", \"check code\"]
    delegate_to: \"gpt-4o-mini\"
    max_cost_usd: 0.50
  
  - name: \"UI Implementation\"
    patterns: [\"react\", \"frontend\", \"ui\"]
    delegate_to: \"claude-sonnet\"
    max_cost_usd: 2.00
\`\`\`

## Acceptance Criteria
- [ ] YAML config loaded
- [ ] Pattern matching works
- [ ] Cost limits enforced
- [ ] Default fallback defined
- [ ] 80%+ routing accuracy

**Estimate:** 8 hours | **Priority:** P0 (Killer Feature)"

# Issue #17: Summary Protocol
gh issue create \
  --title "Summary Protocol - Prevent Context Pollution" \
  --milestone "Milestone 2: Multi-Agent Orchestration" \
  --label "P0,backend" \
  --body "## Objective
Implement structured summary protocol so primary agent sees high-level results, not full logs.

## Problem
Primary agent's context window fills with implementation details from secondary agents.

## Solution
\`\`\`python
class TaskSummary(BaseModel):
    task_id: str
    status: str
    changes: str  # \"3 files modified\"
    loc_added: int
    duration_sec: int
    cost_usd: float
    errors: List[str]
    next_actions: List[str]
\`\`\`

## Acceptance Criteria
- [ ] Structured summary model
- [ ] Parse full output → summary
- [ ] Primary agent receives ONLY summary
- [ ] Link to full logs for deep dive

**Estimate:** 4 hours | **Priority:** P0"

# Issue #18: Cost Tracking System
gh issue create \
  --title "Real-Time Cost Tracking and Monitoring" \
  --milestone "Milestone 2: Multi-Agent Orchestration" \
  --label "P0,backend,frontend" \
  --body "## Objective
Track costs per agent/model in real-time. Prove ROI with hard numbers.

## Implementation
\`\`\`python
class CostTracker:
    model_costs = {
        \"gpt-4o-mini\": {\"input\": 0.15/1M, \"output\": 0.60/1M},
        \"claude-sonnet\": {\"input\": 3.00/1M, \"output\": 15.00/1M}
    }
    
    def track(self, model, tokens): ...
    def get_session_cost(self): ...
    def get_cost_by_agent(self): ...
\`\`\`

## UI Component
Dashboard widget showing:
- Session total cost
- Cost by agent
- Warning when >$10

**Estimate:** 4 hours | **Priority:** P0"

# Issue #19: CLI Wrapper Standardization
gh issue create \
  --title "Standardized CLI Wrapper Interface" \
  --milestone "Milestone 2: Multi-Agent Orchestration" \
  --label "P1,backend" \
  --body "## Objective
Create base wrapper that works with ALL CLI tools (Claude, Droid, Cursor, Aider).

## Features
- Standardized start_agent() interface
- Structured output parsing
- Event streaming to daemon
- Error handling

\`\`\`bash
# wrappers/base-wrapper.sh
start_agent() {
    \$TOOL --task \"\$TASK\" 2>&1 | parse_and_send
}
\`\`\`

**Estimate:** 4 hours | **Priority:** P1"

# Issue #20: Nano-Agent Integration
gh issue create \
  --title "Nano-Agent MCP Integration for Multi-Model Routing" \
  --milestone "Milestone 2: Multi-Agent Orchestration" \
  --label "P0,backend" \
  --body "## Objective
Integrate nano-agent MCP for tiered model selection.

## Why
- Access to gpt-4o-mini, o3-mini for cheap tasks
- Automatic tier selection (simple/medium/complex)
- Cost optimization built-in

## Implementation
\`\`\`python
class NanoAgentClient:
    async def execute_task(
        task: str, 
        tier: str = \"auto\",
        max_cost: float = None
    ): ...
\`\`\`

**Estimate:** 6 hours | **Priority:** P0"

# Issue #21: Terminal Grid View
gh issue create \
  --title "Terminal Grid View - Multi-Agent Monitoring" \
  --milestone "Milestone 2: Multi-Agent Orchestration" \
  --label "P1,frontend" \
  --body "## Objective
Grid view to see multiple agent terminals simultaneously.

## Features
- 2x2 or 4x1 grid layouts
- Agent name + status badge per cell
- Cost and duration in footer
- Expand to fullscreen

**Estimate:** 6 hours | **Priority:** P1"

echo "✅ Created 6 new issues for redesign"

# Update Issue #2 with security fix
gh issue comment 2 --body "## 🚨 SECURITY UPDATE (from Opus review)

**Current approach is INSECURE:** JWT token in WebSocket URL query param

**Why it's bad:**
- Logged in browser history
- Visible in proxy/server logs
- Can't be revoked mid-session

**New approach (SECURE):**
1. Accept WebSocket connection
2. Request auth over established connection
3. Client sends JWT in first message
4. Validate and continue or close

\`\`\`python
@app.websocket(\"/ws/observe\")
async def websocket_observe(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({\"type\": \"auth_required\"})
    auth_msg = await websocket.receive_json()
    # Validate token, then proceed
\`\`\`

This is a P0 security fix that MUST be implemented."

echo "✅ Updated Issue #2 with security fix"
echo ""
echo "All issues created/updated!"
echo "View: https://github.com/DeanSCND/project-orchestra/issues"
