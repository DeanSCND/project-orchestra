# Project Orchestra 🎼

**Your Personal AI Command Center**

Stop manually coordinating Claude Code, Cursor, Droid, and Aider. Let Orchestra intelligently route tasks to the right tool at the right price, with full observability.

## 🎯 The Problem (After 9 Months of AI Coding)

❌ **Context window pollution** - Primary agents get bogged down in implementation details  
❌ **Artificial serialization** - Tasks that could run parallel are forced sequential  
❌ **Manual tool selection** - You pick tools for each task instead of automatic routing  
❌ **Cost blindness** - No idea which model is cost-effective for what  
❌ **Zero remote monitoring** - Can't check on long sessions from phone  

## 💡 The Solution

✅ **Smart Task Routing** - Automatic tool selection based on task type and cost  
✅ **Cost Optimization** - Route simple tasks to cheap models (70% savings)  
✅ **Parallel Execution** - Multiple agents work simultaneously (3x speedup)  
✅ **Summary Protocol** - Maintain hierarchy without context pollution  
✅ **Full Observability** - Monitor everything from anywhere (mobile-ready)  

## 🎯 Not Another Framework

This isn't competing with AutoGen or CrewAI. It orchestrates the **actual CLI tools** you already use:
- **Claude Code** - Best for architecture and planning
- **Droid** - Best for long refactors and backend work
- **Cursor** - Best for UI/frontend work
- **Aider** - Best for git operations and tests

**Why CLI tools?** They're stable interfaces that providers maintain. You just configure routing.

## ✨ Key Features

- 🤖 **Multi-Agent Orchestration** - Claude Code delegates to Droid, Cursor, Aider
- 🔐 **Secure Remote Access** - Auth0 authentication + Twingate zero-trust networking
- 📺 **Full Observability** - Real-time terminal streaming for all agents
- 💬 **Conversational Interface** - Natural language task assignment
- 🎯 **Task Management** - Visual task flow and status tracking
- ⚡ **Parallel Execution** - Multiple agents work simultaneously

## 🏗️ Architecture

```
Web UI (Next.js) ←→ Twingate ←→ Orchestra Daemon (FastAPI) ←→ tmux Sessions
                                                                  ├── Claude Code (Primary)
                                                                  ├── Droid (Backend)
                                                                  ├── Cursor (Frontend)
                                                                  └── Aider (Git/Tests)
```

## 🚀 Quick Start

### Prerequisites

- Node.js 20+
- Python 3.11+
- tmux 3.0+
- Auth0 account
- Twingate account (for remote access)

### Development Setup

```bash
# Clone repository
git clone https://github.com/DeanSCND/project-orchestra.git
cd project-orchestra

# Install dependencies
pnpm install                    # Install Node packages
cd packages/daemon && poetry install  # Install Python packages

# Configure environment
cp packages/web-ui/.env.example packages/web-ui/.env
cp packages/daemon/.env.example packages/daemon/.env
# Edit .env files with your Auth0/Twingate credentials

# Start development servers
pnpm dev                        # Starts web UI and daemon
```

## 📚 Documentation

- [Architecture Overview](docs/00-OVERVIEW.md)
- [Detailed Architecture](docs/01-ARCHITECTURE.md)
- [Security Model](docs/02-SECURITY.md)
- [API Reference](docs/03-API-REFERENCE.md)
- [Development Guide](docs/05-DEVELOPMENT.md)
- [Deployment Guide](docs/04-DEPLOYMENT.md)

## 🛣️ Roadmap

### Milestone 1: PoC (Weeks 1-2) ✅ In Progress
- Auth0 authentication
- WebSocket communication
- Single agent terminal streaming
- Basic chat interface

### Milestone 2: Multi-Agent (Weeks 3-4)
- Secondary agent spawning
- Task delegation protocol
- Tabbed terminal interface
- Task status tracking

### Milestone 3: Production Security (Weeks 5-6)
- Twingate integration
- JWT hardening
- Audit logging
- Rate limiting

### Milestone 4: Advanced Features (Weeks 7-8)
- Multiple agent types
- Grid terminal view
- Error recovery
- Telemetry dashboard

### Milestone 5: Production Ready (Weeks 9-10)
- Docker containers
- CI/CD pipeline
- Monitoring/alerting
- Load testing

## 🤝 Contributing

This project is in active development. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built on top of:
- [Claude Code](https://claude.ai/code) by Anthropic
- [Factory Droid](https://factory.ai) 
- [Cursor](https://cursor.com)
- [Aider](https://aider.chat)
- [Twingate](https://twingate.com)
- [Auth0](https://auth0.com)

---

**Status:** 🚧 Pre-Alpha - PoC in development

**Current Version:** v0.1.0-alpha

**Last Updated:** January 2025
