# CLI Tool Integration Setup

**Prerequisites and setup requirements for each supported tool**

## Overview

Orchestra integrates with CLI tools as stable interfaces. Each tool requires specific setup, authentication, and version pinning for reliability.

---

## Claude Code

### Requirements
- Node.js 18+
- Anthropic API key
- Claude Pro subscription (recommended for higher limits)

### Installation
```bash
npm install -g @anthropic/claude-code
# Or via package manager
brew install claude-code  # macOS
```

### Configuration
```bash
# Setup API key
claude-code config set api_key "sk-ant-..."

# Test installation
claude-code --version
# Expected: claude-code 1.5.0 or higher
```

### API Key Setup
1. Get key from: https://console.anthropic.com/
2. Store in: `~/.config/claude-code/config.json`
3. Never commit to git

### Version Pinning
```bash
# Pin to specific version
npm install -g @anthropic/claude-code@1.5.0
```

### CLI Interface
```bash
# Standard usage (Orchestra will use this format)
claude-code --task "Your task here" --model claude-opus-3

# Output format: Streaming text to stdout
# Exit codes: 0 = success, 1 = error
```

### Known Issues
- **Long tasks:** May timeout after 5 minutes (configure with `--timeout`)
- **Rate limits:** 50 requests/min on free tier, 100 on Pro
- **Context window:** 200K tokens (Opus), 100K (Sonnet)

### Fallback Strategy
If Claude Code unavailable:
1. Check API key validity
2. Verify rate limits not exceeded
3. Fall back to Droid or manual mode

---

## Droid (Factory.ai)

### Requirements
- Factory.ai account
- Droid CLI installed
- API token

### Installation
```bash
# Via Factory's installer
curl -fsSL https://factory.ai/install-droid.sh | sh

# Or via npm
npm install -g @factory/droid-cli
```

### Configuration
```bash
# Login (opens browser)
droid login

# Or set token directly
export FACTORY_TOKEN="fac_..."

# Test
droid --version
# Expected: droid-cli 2.3.0+
```

### API Token Setup
1. Get token from: https://app.factory.ai/settings/api
2. Store in: `~/.config/droid/credentials`
3. Refresh token expires in 30 days

### Version Pinning
```bash
# Pin to specific version
npm install -g @factory/droid-cli@2.3.5
```

### CLI Interface
```bash
# Standard usage
droid --prompt "Your task" --model claude-sonnet

# With workspace
droid --prompt "..." --workspace /path/to/project

# Output: JSON-formatted results to stdout
```

### Known Issues
- **Authentication:** Token refresh needed monthly
- **Context:** Works best with explicit file paths
- **Rate limits:** Depends on Factory.ai plan

### Fallback Strategy
If Droid unavailable:
1. Check token validity (refresh if needed)
2. Verify Factory.ai status
3. Fall back to Claude Code

---

## Cursor

### Requirements
- Cursor IDE installed (free or Pro)
- Cursor agent CLI addon
- OpenAI or Anthropic API key (depending on model)

### Installation
```bash
# Install Cursor IDE first
# Download from: https://cursor.sh

# Install CLI addon (from Cursor settings)
cursor --install-cli

# Test
cursor-agent --version
```

### Configuration
```bash
# Configure API key (in Cursor settings or CLI)
cursor-agent config --api-key "..."

# Set default model
cursor-agent config --model claude-sonnet
```

### API Key Setup
- Uses Cursor's built-in API routing
- Or bring your own key (Anthropic/OpenAI)
- Configured in: `~/.cursor/config.json`

### Version Pinning
```bash
# Cursor updates automatically, but can pin CLI
cursor-agent version lock 0.8.0
```

### CLI Interface
```bash
# Standard usage
cursor-agent --task "Build React component" --file src/App.tsx

# Output: Modified files written to disk
# Logs: Streamed to stderr
```

### Known Issues
- **File locking:** Ensure files not open in other editors
- **UI focus:** Works best when Cursor UI is not active
- **Model switching:** Requires restart to change models

### Fallback Strategy
If Cursor unavailable:
1. Check if Cursor IDE is running (close it)
2. Verify API key configuration
3. Fall back to Droid for non-UI tasks

---

## Aider

### Requirements
- Python 3.8+
- Git installed
- OpenAI API key

### Installation
```bash
# Via pip
pip install aider-chat

# Or via pipx (recommended)
pipx install aider-chat

# Test
aider --version
# Expected: aider 0.30.0+
```

### Configuration
```bash
# Set API key
export OPENAI_API_KEY="sk-..."

# Or in config file
echo "OPENAI_API_KEY=sk-..." > ~/.aider.conf.yml

# Test
aider --help
```

### API Key Setup
1. Get key from: https://platform.openai.com/api-keys
2. Store in: `~/.aider.conf.yml` or environment
3. Never commit to repo

### Version Pinning
```bash
# Pin specific version
pip install aider-chat==0.30.0
```

### CLI Interface
```bash
# Standard usage
aider --message "Your task" --yes --auto-commits

# With specific files
aider --file src/main.py --message "Add logging"

# Output: Git commits created automatically
```

### Known Issues
- **Git required:** Must be in git repo
- **Auto-commits:** Can create messy history (disable with `--no-auto-commits`)
- **Model costs:** Uses GPT-4 by default (expensive)

### Fallback Strategy
If Aider unavailable:
1. Check git repo status (must be clean)
2. Verify OpenAI API key
3. Fall back to manual git operations

---

## O3-mini (via Nano-Agent)

### Requirements
- Nano-agent MCP server running
- Access to OpenAI o3-mini model

### Installation
```bash
# Install nano-agent
npm install -g @anthropic/nano-agent

# Start MCP server
nano-agent serve --port 3000
```

### Configuration
```bash
# Configure API access
nano-agent config --openai-key "sk-..."

# Test
curl http://localhost:3000/health
```

### CLI Interface
```bash
# Via HTTP (Orchestra calls this)
curl -X POST http://localhost:3000/execute \
  -d '{"task": "...", "tier": "simple"}'
```

### Known Issues
- **MCP server:** Must be running before Orchestra starts
- **Model access:** o3-mini requires special API access
- **Rate limits:** Very aggressive on free tier

### Fallback Strategy
If o3-mini unavailable:
1. Fall back to gpt-4o-mini
2. Increase timeout for slower model

---

## Version Compatibility Matrix

| Tool | Tested Version | Min Version | Max Version | Notes |
|------|----------------|-------------|-------------|-------|
| Claude Code | 1.5.0 | 1.2.0 | 2.x | Breaking changes expected in 2.x |
| Droid | 2.3.5 | 2.0.0 | 2.x | Stable interface since 2.0 |
| Cursor | 0.8.0 | 0.6.0 | 0.x | Beta, frequent updates |
| Aider | 0.30.0 | 0.25.0 | 0.x | Stable interface |
| Nano-agent | 1.0.0 | 1.0.0 | 1.x | New, may change |

---

## Security Best Practices

### API Key Management
```bash
# ✅ GOOD - Use environment variables
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."

# ✅ GOOD - Use dedicated config files (with proper permissions)
chmod 600 ~/.config/claude-code/config.json

# ❌ BAD - Hardcode in scripts
ANTHROPIC_API_KEY="sk-ant-..." python script.py

# ❌ BAD - Commit to git
echo "OPENAI_API_KEY=sk-..." >> .env  # Then git commit
```

### Key Rotation
- Rotate API keys quarterly
- Use separate keys for dev/prod
- Revoke keys immediately if compromised

### Cost Controls
```bash
# Set spending limits in provider dashboards
# Anthropic: https://console.anthropic.com/settings/billing
# OpenAI: https://platform.openai.com/account/billing/limits
```

---

## Troubleshooting

### Claude Code Issues
```bash
# Reset configuration
rm -rf ~/.config/claude-code
claude-code config set api_key "..."

# Check API status
curl https://api.anthropic.com/v1/health
```

### Droid Issues
```bash
# Re-authenticate
droid logout
droid login

# Check token
droid whoami
```

### Cursor Issues
```bash
# Reinstall CLI
cursor --uninstall-cli
cursor --install-cli

# Clear cache
rm -rf ~/.cursor/cache
```

### Aider Issues
```bash
# Verify git repo
git status

# Reset aider config
rm ~/.aider.conf.yml
```

---

## Testing Your Setup

Run this script to verify all tools are configured:

```bash
#!/bin/bash
# test-tools.sh

echo "Testing Orchestra tool setup..."

# Claude Code
if command -v claude-code &> /dev/null; then
    echo "✅ Claude Code installed: $(claude-code --version)"
else
    echo "❌ Claude Code not found"
fi

# Droid
if command -v droid &> /dev/null; then
    echo "✅ Droid installed: $(droid --version)"
else
    echo "❌ Droid not found"
fi

# Cursor
if command -v cursor-agent &> /dev/null; then
    echo "✅ Cursor agent installed"
else
    echo "❌ Cursor agent not found"
fi

# Aider
if command -v aider &> /dev/null; then
    echo "✅ Aider installed: $(aider --version)"
else
    echo "❌ Aider not found"
fi

# Check API keys
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not set"
else
    echo "✅ Anthropic API key configured"
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set"
else
    echo "✅ OpenAI API key configured"
fi

echo ""
echo "Setup complete! Ready to run Orchestra."
```

---

**Document Status:** Setup Guide  
**Last Updated:** January 2025  
**Tested Platforms:** macOS, Linux, WSL2  
**Update Frequency:** When tool versions change
