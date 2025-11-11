# Project Orchestra - System Overview

## Problem Statement

Modern AI-assisted development tools (Claude Code, Cursor, Aider, Droid) are powerful but operate in isolation. Developers must manually coordinate between tools, copy context, and monitor multiple terminal sessions. This creates:

- **Context switching overhead** - Jumping between tools wastes time
- **Lost parallelization** - Can't leverage multiple agents simultaneously  
- **Poor observability** - Hard to track what each agent is doing
- **Security concerns** - Direct tmux access exposes development machine

## Solution: Project Orchestra

A web-based orchestration platform that:

1. **Centralizes Control** - Single web interface for all agents
2. **Enables Delegation** - Primary agent (Claude Code) delegates to specialists
3. **Provides Observability** - Real-time terminal streaming for all agents
4. **Secures Access** - Auth0 + Twingate zero-trust architecture
5. **Parallelizes Work** - Multiple agents execute tasks simultaneously

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Web UI (Next.js 14)                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │ • Auth0 Login (Google OAuth)                       │ │
│  │ • Conversational Chat Interface                    │ │
│  │ • Multi-Terminal View (xterm.js)                   │ │
│  │ • Task Status Dashboard                            │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
                          │ HTTPS/WSS over Twingate
                          ▼
┌─────────────────────────────────────────────────────────┐
│         Orchestra Daemon (FastAPI/Python)                │
│  ┌────────────────────────────────────────────────────┐ │
│  │ • JWT Authentication Middleware                    │ │
│  │ • WebSocket Server (Real-time Events)             │ │
│  │ • REST API (Commands)                              │ │
│  │ • Tmux Session Manager (libtmux)                   │ │
│  │ • Agent Bridge Protocol                            │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
                          │ Local process management
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Tmux Sessions (Agent Isolation)             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │   Primary    │ │   Droid      │ │   Cursor     │   │
│  │ Claude Code  │ │  (Backend)   │ │ (Frontend)   │   │
│  │              │ │              │ │              │   │
│  │ Orchestrates │ │ Implements   │ │ Implements   │   │
│  │ & Delegates  │ │ Python APIs  │ │ React UIs    │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
│  ┌──────────────┐                                       │
│  │   Aider      │                                       │
│  │  (Git/Tests) │                                       │
│  └──────────────┘                                       │
└─────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Web UI (packages/web-ui/)
**Technology:** Next.js 14, React, TypeScript, Tailwind CSS, shadcn/ui

**Responsibilities:**
- User authentication via Auth0
- Real-time WebSocket connection to daemon
- Chat interface for natural language task input
- Terminal streaming (xterm.js) for agent output
- Task status visualization (React Flow)
- Multi-terminal tab management

### 2. Orchestra Daemon (packages/daemon/)
**Technology:** FastAPI, Python 3.11, libtmux, asyncio

**Responsibilities:**
- JWT authentication and authorization
- WebSocket server for bi-directional communication
- REST API for commands (spawn agent, delegate task, kill session)
- Tmux session lifecycle management
- Agent-to-agent message routing
- Event logging and telemetry

### 3. Agent Wrappers (packages/agent-wrappers/)
**Technology:** Bash scripts

**Responsibilities:**
- Launch secondary agents in tmux sessions
- Register agents with daemon
- Wrap stdin/stdout for structured communication
- Handle agent crashes and restarts

### 4. Claude Configuration (packages/claude-config/)
**Technology:** Markdown (CLAUDE.md), YAML (hooks, MCP config)

**Responsibilities:**
- Define primary agent orchestration rules
- Configure delegation skills
- Setup hooks for telemetry capture
- MCP server configuration

## Key Workflows

### Workflow 1: User Authenticates
```
1. User → Web UI: Click "Login"
2. Web UI → Auth0: Redirect to Google OAuth
3. Auth0 → Web UI: Return JWT token
4. Web UI → Daemon: WebSocket + JWT in query param
5. Daemon: Validates JWT, accepts connection
```

### Workflow 2: User Sends Task
```
1. User → Web UI: Types "Build REST API with JWT auth"
2. Web UI → Daemon: {"type": "user_message", "content": "..."}
3. Daemon → Claude tmux: Send message via stdin
4. Claude: Analyzes task, creates delegation plan
5. Claude → Daemon: Calls /api/delegate via HTTP
6. Daemon: Spawns Droid agent, sends task
7. Droid: Executes, returns result
8. Daemon → Web UI: Stream all outputs via WebSocket
```

### Workflow 3: Monitor Multiple Agents
```
1. Web UI: User clicks "Droid" terminal tab
2. Web UI → Daemon: {"type": "subscribe_terminal", "session_id": "sess-droid-001"}
3. Daemon: Starts async terminal capture loop (2 FPS)
4. Daemon → Web UI: Stream terminal output
5. Web UI: Render in xterm.js
```

## Security Model

### Authentication Flow
1. **User → Auth0:** Google OAuth 2.0 (PKCE flow)
2. **Auth0 → User:** JWT access token (1 hour expiry)
3. **User → Daemon:** JWT in WebSocket query param
4. **Daemon:** Validates JWT signature with Auth0 public key

### Network Security
- **Twingate:** Zero-trust network access (no public ports)
- **TLS:** All traffic encrypted (HTTPS/WSS)
- **IP Whitelist:** Restrict daemon to localhost + Twingate subnet

### Authorization
- **Roles:** `developer` (spawn agents, view sessions), `admin` (kill agents, view all users)
- **Scope:** JWT includes Auth0 permissions
- **Enforcement:** Every API call checks JWT scope

### Audit Trail
- **All actions logged:** User login, agent spawn, task delegation
- **Structured logs:** JSON format with user ID, timestamp, action
- **Retention:** 30 days (configurable)

## Data Flow

### Message Types (WebSocket)

**Client → Daemon:**
```json
{
  "type": "user_message",
  "content": "Implement user authentication",
  "session_id": "sess-primary"
}
```

**Daemon → Client:**
```json
{
  "type": "claude_response",
  "content": "I'll delegate this to Droid...",
  "actions": [{"type": "approve_plan", "task_ids": [1, 2]}]
}
```

**Daemon → Client (Terminal Stream):**
```json
{
  "type": "terminal_output",
  "session_id": "sess-droid-001",
  "data": "> droid\nAnalyzing task...\n",
  "timestamp": 1704067200000
}
```

**Daemon → Client (Task Update):**
```json
{
  "type": "task_update",
  "task_id": 1,
  "agent": "droid",
  "status": "running",
  "elapsed_ms": 45000
}
```

## Technology Stack

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript 5.3+
- **Styling:** Tailwind CSS 3.4+, shadcn/ui
- **State:** Zustand 4.5+ (WebSocket state)
- **Terminal:** xterm.js 5.3+
- **Auth:** @auth0/nextjs-auth0 3.5+

### Backend
- **Framework:** FastAPI 0.115+
- **Language:** Python 3.11+
- **Async:** asyncio, uvicorn
- **Tmux:** python-libtmux 0.38+
- **Auth:** PyJWT 2.9+
- **Config:** Pydantic 2.9+

### Infrastructure
- **Container:** Docker 24+
- **Orchestration:** Docker Compose (dev), Kubernetes (prod)
- **Networking:** Twingate
- **Auth:** Auth0
- **Monitoring:** Prometheus + Grafana (future)

## Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| **WebSocket Latency** | <100ms (p99) | Time from client send to server receive |
| **Terminal Refresh** | 2 FPS (500ms) | Tmux capture frequency |
| **Message Throughput** | 100 msg/sec per connection | Load test benchmark |
| **Concurrent Users** | 100+ | Simultaneous WebSocket connections |
| **Agent Spawn Time** | <2 seconds | Time to launch tmux + agent CLI |
| **Memory per Agent** | <500MB | tmux + agent process RSS |

## Deployment Topology

### Development
```
Developer Laptop:
  - Web UI (localhost:3000)
  - Daemon (localhost:8080)
  - Tmux sessions (local)
  - No Twingate (local-only)
```

### Production
```
User Browser:
  - Web UI (https://orchestra.example.com)
    ↓ (via Twingate)
Developer Machine:
  - Twingate Connector
  - Daemon (localhost:8080, exposed via Twingate)
  - Tmux sessions (isolated per user)
```

### Future: Multi-Machine
```
User Browser → Twingate → Load Balancer
                             ↓
                    ┌────────┼────────┐
                    ↓        ↓        ↓
              Daemon 1   Daemon 2   Daemon 3
                    ↓        ↓        ↓
              Cloud VM   Cloud VM   Cloud VM
             (GPU agents) (CPU) (Tests)
```

## Success Metrics

### PoC Success (Milestone 1)
- ✅ <1 second latency (user message → Claude response)
- ✅ 30-minute session without crashes
- ✅ Terminal output streams smoothly (no lag)
- ✅ Auth0 login works 100% of attempts

### Production Success (Milestone 5)
- ✅ 100+ concurrent users
- ✅ 99.9% uptime (3 nines)
- ✅ <5% error rate under load
- ✅ Security audit: 0 critical vulnerabilities
- ✅ Developer satisfaction: 4.5/5 stars

## Next Steps

1. Read [01-ARCHITECTURE.md](01-ARCHITECTURE.md) for detailed component design
2. Review [02-SECURITY.md](02-SECURITY.md) for threat model
3. Follow [05-DEVELOPMENT.md](05-DEVELOPMENT.md) to setup local environment
4. Check GitHub Project board for current priorities

---

**Document Version:** 1.0  
**Last Updated:** January 2025  
**Owner:** Product Team
