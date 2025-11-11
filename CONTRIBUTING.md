# Contributing to Project Orchestra

Thank you for your interest in contributing! This document provides guidelines for contributing to Project Orchestra.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Install dependencies** (see README.md)
4. **Create a branch** for your changes
5. **Make your changes**
6. **Test your changes**
7. **Submit a pull request**

## Development Workflow

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/project-orchestra.git
cd project-orchestra

# Install dependencies
pnpm install
cd packages/daemon && poetry install

# Setup environment files
cp packages/web-ui/.env.example packages/web-ui/.env
cp packages/daemon/.env.example packages/daemon/.env
```

### Running Locally

```bash
# Start all services
pnpm dev

# Or run individually
cd packages/web-ui && pnpm dev
cd packages/daemon && poetry run uvicorn orchestra.main:app --reload
```

### Code Style

**Frontend (TypeScript):**
- Use ESLint + Prettier (auto-formatted on commit)
- Follow React best practices
- Use TypeScript strict mode

**Backend (Python):**
- Use Black + Ruff (auto-formatted on commit)
- Follow PEP 8
- Type hints required

**Pre-commit Hooks:**
All formatting happens automatically via pre-commit hooks. Install them:

```bash
pre-commit install
```

## Pull Request Process

1. **Create an issue first** (unless it's a trivial change)
2. **Reference the issue** in your PR description
3. **Ensure tests pass** (run `pnpm test`)
4. **Update documentation** if needed
5. **Request review** from maintainers

### PR Title Format

```
[Component] Brief description

Examples:
[Frontend] Add terminal tab switching
[Backend] Implement JWT validation
[Docs] Update security model documentation
```

### PR Description Template

```markdown
## What does this PR do?
Brief description of changes

## Related Issue
Closes #123

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing performed
- [ ] Documentation updated

## Screenshots (if applicable)
[Add screenshots for UI changes]
```

## Coding Guidelines

### TypeScript

```typescript
// ✅ Good: Clear type definitions
interface AgentSession {
  id: string;
  type: 'claude' | 'droid' | 'cursor';
  status: 'running' | 'idle' | 'error';
}

// ❌ Bad: Implicit any
function processAgent(agent) {
  // ...
}
```

### Python

```python
# ✅ Good: Type hints and docstrings
async def spawn_agent(agent_type: str, working_dir: str) -> str:
    """
    Spawn new agent in tmux session.
    
    Args:
        agent_type: Type of agent (claude, droid, cursor)
        working_dir: Working directory for agent
    
    Returns:
        session_id: Unique session identifier
    """
    pass

# ❌ Bad: No type hints
async def spawn_agent(agent_type, working_dir):
    pass
```

## Testing

### Unit Tests

**Frontend:**
```bash
cd packages/web-ui
pnpm test
```

**Backend:**
```bash
cd packages/daemon
poetry run pytest
```

### Integration Tests

```bash
# Start services in test mode
pnpm test:integration
```

## Documentation

Update documentation when:
- Adding new features
- Changing API contracts
- Modifying security model
- Adding configuration options

Documentation lives in `docs/`:
- `00-OVERVIEW.md` - High-level architecture
- `01-ARCHITECTURE.md` - Detailed technical design
- `02-SECURITY.md` - Security model
- `03-API-REFERENCE.md` - API documentation
- `05-DEVELOPMENT.md` - Development guide

## Issue Guidelines

### Bug Reports

```markdown
**Describe the bug**
Clear description of what went wrong

**To Reproduce**
1. Step one
2. Step two
3. See error

**Expected behavior**
What you expected to happen

**Environment:**
- OS: [e.g., macOS 14.0]
- Browser: [e.g., Chrome 120]
- Version: [e.g., v0.1.0]

**Logs**
```
Paste relevant logs here
```
```

### Feature Requests

```markdown
**Problem**
What problem does this solve?

**Proposed Solution**
How would you solve it?

**Alternatives**
Other approaches considered?

**Additional Context**
Any other relevant information
```

## Security

**Do NOT open public issues for security vulnerabilities!**

Instead, email: security@project-orchestra.dev

See [SECURITY.md](docs/02-SECURITY.md) for full security policy.

## Community

- **GitHub Discussions** - Ask questions, share ideas
- **GitHub Issues** - Bug reports, feature requests
- **Pull Requests** - Code contributions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
