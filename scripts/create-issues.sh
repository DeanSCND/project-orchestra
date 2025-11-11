#!/bin/bash
# Script to create all Project Orchestra GitHub issues

cd /home/dean/Development/RandD/project-orchestra

# Issue #2: FastAPI WebSocket Server with JWT Auth
gh issue create \
  --title "FastAPI WebSocket Server with JWT Auth" \
  --milestone "Milestone 1: PoC - Primary Agent Interface" \
  --label "P0,backend,security" \
  --body "## Objective
Build core daemon with WebSocket support and JWT validation.

## Technical Requirements
- FastAPI with WebSocket routes
- JWT validation middleware (Auth0 public key)
- WebSocket connection manager
- JSON event protocol
- Rate limiting (10 msg/sec per connection)

## Acceptance Criteria
- [ ] /api/health endpoint returns 200
- [ ] WebSocket at /ws/observe with JWT auth
- [ ] JWT validation rejects invalid tokens
- [ ] Send/receive JSON messages
- [ ] Unit tests (80%+ coverage)

## Code Snippet
\`\`\`python
@app.websocket(\"/ws/observe\")
async def websocket_observe(
    websocket: WebSocket,
    token: str = Query(...)
):
    payload = verify_jwt_token(token)
    await manager.connect(websocket, payload[\"sub\"])
\`\`\`

**Estimate:** 8 hours | **Priority:** P0"

# Issue #3: Tmux Session Manager with libtmux
gh issue create \
  --title "Tmux Session Manager with libtmux" \
  --milestone "Milestone 1: PoC - Primary Agent Interface" \
  --label "P0,backend" \
  --body "## Objective
Implement Python wrapper for tmux using libtmux.

## Technical Requirements
- Use python-libtmux for tmux control
- Session lifecycle (spawn, kill, capture)
- Async output streaming (2 FPS)
- Error handling for crashed sessions

## Acceptance Criteria
- [ ] Can spawn new tmux session
- [ ] Send commands to session
- [ ] Capture pane output
- [ ] Async streaming without blocking
- [ ] Crashed sessions detected

## Dependencies
python-libtmux = \"^0.38.0\"

**Estimate:** 6 hours | **Priority:** P0"

# Issue #4: Next.js UI with Auth0
gh issue create \
  --title "Next.js 14 UI with Auth0 Integration" \
  --milestone "Milestone 1: PoC - Primary Agent Interface" \
  --label "P0,frontend,security" \
  --body "## Objective
Build Next.js frontend with Auth0 authentication.

## Technical Requirements
- Next.js 14 App Router
- Auth0 SDK (Google OAuth)
- Tailwind CSS + shadcn/ui
- TypeScript strict mode
- Mobile-responsive

## Acceptance Criteria
- [ ] Login page with Auth0
- [ ] Protected dashboard route
- [ ] JWT stored securely
- [ ] Logout functionality
- [ ] Mobile-responsive (375px+)

## Dependencies
@auth0/nextjs-auth0: ^3.5.0

**Estimate:** 8 hours | **Priority:** P0"

# Issue #5: xterm.js Terminal Component
gh issue create \
  --title "xterm.js Terminal Streaming Component" \
  --milestone "Milestone 1: PoC - Primary Agent Interface" \
  --label "P0,frontend" \
  --body "## Objective
Build React component with xterm.js for terminal streaming.

## Technical Requirements
- xterm.js 5.3+ with FitAddon
- WebSocket integration
- Auto-scroll toggle
- Copy support
- 2 FPS update rate

## Acceptance Criteria
- [ ] Terminal renders tmux output
- [ ] Auto-scroll works
- [ ] Copy text functionality
- [ ] No memory leaks
- [ ] Responsive sizing

**Estimate:** 6 hours | **Priority:** P0"

# Issue #6: Chat Interface Component
gh issue create \
  --title "Conversational Chat Interface" \
  --milestone "Milestone 1: PoC - Primary Agent Interface" \
  --label "P0,frontend" \
  --body "## Objective
Build chat interface for natural language task input.

## Technical Requirements
- Message list with markdown rendering
- Input field with send button
- Action buttons (Approve/Modify)
- Message history
- Auto-scroll

## Acceptance Criteria
- [ ] Render user/AI messages
- [ ] Markdown code blocks work
- [ ] Action buttons functional
- [ ] Scroll to bottom on new message

**Estimate:** 6 hours | **Priority:** P0"

# Issue #7: WebSocket Connection Manager
gh issue create \
  --title "WebSocket Client with Auto-Reconnect" \
  --milestone "Milestone 1: PoC - Primary Agent Interface" \
  --label "P1,frontend" \
  --body "## Objective
Implement robust WebSocket client with reconnection logic.

## Technical Requirements
- Auto-reconnect with exponential backoff
- Heartbeat ping/pong
- Connection state management (Zustand)
- Queue messages during disconnect

## Acceptance Criteria
- [ ] Auto-reconnects on disconnect
- [ ] Max 5 reconnect attempts
- [ ] Heartbeat every 30s
- [ ] State persists across reconnects

**Estimate:** 4 hours | **Priority:** P1"

# Issue #8: Environment Configuration
gh issue create \
  --title "Environment Configuration & Secrets" \
  --milestone "Milestone 1: PoC - Primary Agent Interface" \
  --label "P1,infrastructure,security" \
  --body "## Objective
Setup environment configuration for Auth0, daemon URL, etc.

## Technical Requirements
- .env.example files for web-ui and daemon
- Pydantic Settings for daemon config
- Next.js environment variables
- Secret validation on startup

## Files
- packages/web-ui/.env.example
- packages/daemon/.env.example
- orchestra/core/config.py

**Estimate:** 2 hours | **Priority:** P1"

# Issue #9: Docker Development Stack
gh issue create \
  --title "Docker Compose for Local Development" \
  --milestone "Milestone 1: PoC - Primary Agent Interface" \
  --label "P2,infrastructure" \
  --body "## Objective
Create docker-compose.yml for easy local development.

## Services
- web-ui (Next.js dev server)
- daemon (uvicorn with reload)
- Optional: Redis for future features

## Acceptance Criteria
- [ ] docker-compose up starts all services
- [ ] Hot reload works for both services
- [ ] Environment variables injected

**Estimate:** 4 hours | **Priority:** P2"

# Milestone 2 Issues

# Issue #10: Agent Spawning System
gh issue create \
  --title "Dynamic Agent Spawning System" \
  --milestone "Milestone 2: Multi-Agent Orchestration" \
  --label "P0,backend" \
  --body "## Objective
Implement system to spawn secondary agents (Droid, Cursor, Aider) on demand.

## Technical Requirements
- Agent type registry
- Spawn agent in new tmux session
- Track agent lifecycle
- Auto-cleanup on idle timeout

## API Endpoint
POST /api/agents/spawn
{\"agent_type\": \"droid\", \"working_dir\": \"/workspace\"}

**Estimate:** 8 hours | **Priority:** P0"

# Issue #11: Agent Bridge Protocol
gh issue create \
  --title "Agent-Bridge Communication Protocol" \
  --milestone "Milestone 2: Multi-Agent Orchestration" \
  --label "P0,backend" \
  --body "## Objective
Implement structured messaging protocol between primary and secondary agents.

## Technical Requirements
- Ticket-based correlation IDs
- Message routing
- Async reply handling
- Timeout detection

## Message Format
{\"ticket_id\": \"uuid\", \"agent\": \"droid\", \"payload\": \"...\"}

**Estimate:** 8 hours | **Priority:** P0"

# Issue #12: Claude Delegation Skill
gh issue create \
  --title "Claude Code Delegation Skill" \
  --milestone "Milestone 2: Multi-Agent Orchestration" \
  --label "P0,backend" \
  --body "## Objective
Create Claude Skill for delegating tasks to secondary agents.

## File
packages/claude-config/skills/delegate_to_agent.md

## Skill Content
- Available agent descriptions
- Delegation process
- API call examples
- Review/approval workflow

**Estimate:** 4 hours | **Priority:** P0"

# Issue #13: Terminal Tabs Component
gh issue create \
  --title "Multi-Terminal Tab Interface" \
  --milestone "Milestone 2: Multi-Agent Orchestration" \
  --label "P0,frontend" \
  --body "## Objective
Build tabbed interface to view multiple agent terminals.

## Technical Requirements
- Tab bar with agent names
- Status badges (running/idle/error)
- Switch between terminal views
- Close tab (kill agent)

## Acceptance Criteria
- [ ] Multiple terminals in tabs
- [ ] Click tab to switch view
- [ ] Status badges update real-time

**Estimate:** 6 hours | **Priority:** P0"

# Issue #14: Task Status Panel
gh issue create \
  --title "Task Status Dashboard Panel" \
  --milestone "Milestone 2: Multi-Agent Orchestration" \
  --label "P1,frontend" \
  --body "## Objective
Build panel showing active tasks and agent assignments.

## Technical Requirements
- Table with task ID, agent, status, duration
- Click row to view agent terminal
- Status updates via WebSocket
- Color-coded status badges

**Estimate:** 6 hours | **Priority:** P1"

# Issue #15: Agent Wrapper Scripts
gh issue create \
  --title "Secondary Agent Wrapper Scripts" \
  --milestone "Milestone 2: Multi-Agent Orchestration" \
  --label "P1,backend" \
  --body "## Objective
Create bash wrappers for Droid, Cursor, Aider to standardize startup.

## Files
- packages/agent-wrappers/droid-wrapper.sh
- packages/agent-wrappers/cursor-wrapper.sh
- packages/agent-wrappers/aider-wrapper.sh

## Functionality
- Register agent with daemon
- Wrap stdin/stdout for protocol
- Handle crashes

**Estimate:** 4 hours | **Priority:** P1"

echo "✅ All issues created successfully!"
echo "View them at: https://github.com/DeanSCND/project-orchestra/issues"
